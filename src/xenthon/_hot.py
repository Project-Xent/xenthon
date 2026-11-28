import ast
import hashlib
import importlib
import os
import sys
import threading
import traceback
import types

from . import _reconcile

_SKIP = {"__pycache__", ".git", ".venv", "venv", "build", "dist", ".mypy_cache", ".pytest_cache", ".ruff_cache"}
_POLL = 0.25
_SETTLE = 0.2
_RELOADED_NAME = "__xenthon_hot__"


def _say(text):
    print(f"[hot] {text}", file=sys.stderr, flush=True)


def _norm(path):
    return os.path.normcase(os.path.abspath(path))


def _py_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _SKIP]
        yield from (_norm(os.path.join(dirpath, name)) for name in filenames if name.endswith(".py"))


def _mtime(path):
    try:
        return os.stat(path).st_mtime_ns
    except OSError:
        return None


def _code_hash(path):
    try:
        with open(path, "rb") as f:
            tree = ast.parse(f.read(), filename=path)
    except (OSError, SyntaxError, ValueError):
        return None
    return hashlib.sha1(ast.dump(tree).encode()).hexdigest()


class Session:
    def __init__(self, update, view):
        self.update_name = update.__name__
        self.view_name = view.__name__
        self.module_name = update.__module__
        self.file = _norm(sys.modules[self.module_name].__file__)
        self.root = os.path.dirname(self.file)
        self.generation = 0
        self.stopping = threading.Event()
        self.thread = None
        self.mtimes = self._scan()
        self.codes = {path: _code_hash(path) for path in self.mtimes}

    def start(self):
        self.thread = threading.Thread(target=self._loop, name="xenthon-hot", daemon=True)
        self.thread.start()
        _say("loaded, watching for changes")

    def stop(self):
        self.stopping.set()
        if self.thread is not None:
            self.thread.join(timeout=1.0)

    def _scan(self):
        found = {}
        for path in _py_files(self.root):
            mtime = _mtime(path)
            if mtime is not None:
                found[path] = mtime
        return found

    def _changed(self):
        now = self._scan()
        changed = {path for path, mtime in now.items() if self.mtimes.get(path) != mtime}
        self.mtimes = now
        return changed

    def _settle(self, changed):
        while not self.stopping.wait(_SETTLE):
            more = self._changed()
            if not more:
                return changed
            changed |= more
        return changed

    def _loop(self):
        while not self.stopping.wait(_POLL):
            changed = self._changed()
            if changed:
                batch = frozenset(self._settle(changed))
                _reconcile.invoke(lambda b=batch: self._reload(b))

    def _reload(self, changed):
        fresh = {path: _code_hash(path) for path in changed}
        if all(code is not None and code == self.codes.get(path) for path, code in fresh.items()):
            _say("code unchanged")
            return
        _reconcile._set_hot_reloading(True)
        try:
            self._reload_dependencies(changed)
            update, view = self._reload_target()
        except BaseException:
            traceback.print_exc()
            _say("reload failed, kept the previous code")
            return
        finally:
            _reconcile._set_hot_reloading(False)
        if not _reconcile.hot_swap(update, view):
            _say("new view failed, kept the previous one")
            return
        self.codes.update(fresh)
        self.generation += 1
        _say(f"reloaded, generation {self.generation}")

    def _reload_dependencies(self, changed):
        skip = {self.module_name, "__main__", _RELOADED_NAME}
        for module in list(sys.modules.values()):
            path = getattr(module, "__file__", None)
            if path and module.__name__ not in skip and _norm(path) in changed:
                importlib.reload(module)

    def _reload_target(self):
        if self.module_name != "__main__":
            namespace = vars(importlib.reload(sys.modules[self.module_name]))
            return namespace[self.update_name], namespace[self.view_name]
        with open(self.file, "rb") as f:
            code = compile(f.read(), self.file, "exec")
        module = types.ModuleType(_RELOADED_NAME)
        module.__file__ = self.file
        previous = sys.modules.get(_RELOADED_NAME)
        sys.modules[_RELOADED_NAME] = module
        try:
            exec(code, module.__dict__)
        except BaseException:
            if previous is not None:
                sys.modules[_RELOADED_NAME] = previous
            raise
        return module.__dict__[self.update_name], module.__dict__[self.view_name]
