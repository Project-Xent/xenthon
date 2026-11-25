# cython: language_level=3, boundscheck=False, wraparound=False

import math
import traceback
from enum import IntEnum

from cpython.mem cimport PyMem_Free, PyMem_Malloc
from libc.stddef cimport wchar_t
from libc.stdint cimport int32_t, uint32_t, uint64_t
from libc.string cimport memset

from xenthon._xent cimport *


cdef extern from "Python.h":
    wchar_t *PyUnicode_AsWideCharString(object unicode, Py_ssize_t *size) except NULL


K_BOOL = 1
K_I32 = 2
K_F32 = 3
K_F64 = 4
K_ENUM = 5
K_COLOR = 6
K_STRING = 7
K_RESOURCE = 8

P_NONE = XTK_EVENT_PAYLOAD_NONE
P_BOOL = XTK_EVENT_PAYLOAD_BOOL
P_I32 = XTK_EVENT_PAYLOAD_I32
P_F32 = XTK_EVENT_PAYLOAD_F32
P_F64 = XTK_EVENT_PAYLOAD_F64
P_STRING = XTK_EVENT_PAYLOAD_STRING
P_QUERY = XTK_EVENT_PAYLOAD_QUERY
P_RATING = XTK_EVENT_PAYLOAD_RATING
P_INDEX_BOOL = XTK_EVENT_PAYLOAD_INDEX_BOOL
P_RANGE = XTK_EVENT_PAYLOAD_RANGE
P_SCROLL = XTK_EVENT_PAYLOAD_SCROLL

include "_ids.pxi"


class Theme(IntEnum):
    SYSTEM = FLUX_THEME_SYSTEM
    LIGHT = FLUX_THEME_LIGHT
    DARK = FLUX_THEME_DARK


class ScrollPos:
    __slots__ = ("x", "y", "max_x", "max_y")

    def __init__(self, x, y, max_x, max_y):
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y

    @property
    def at_end(self):
        return self.y >= self.max_y - 1.0


cdef class Spec:
    cdef readonly uint32_t ty
    cdef readonly dict props
    cdef readonly dict events
    cdef readonly bint virtual
    cdef readonly object model

    def __init__(self, ty, props, events, virtual, model):
        self.ty = ty
        self.props = props
        self.events = events
        self.virtual = virtual
        self.model = model


cdef class El:
    cdef public uint32_t ty
    cdef public object key
    cdef public list props
    cdef public dict handlers
    cdef public list kids
    cdef public object items
    cdef public object focus
    cdef public object model


def el(Spec spec, tuple children, dict kw):
    cdef El e = El.__new__(El)
    e.ty = spec.ty
    e.key = None
    e.props = []
    e.handlers = {}
    e.kids = [kid for kid in children if kid is not None]
    e.items = None
    e.focus = None
    e.model = None
    if spec.model == "nav":
        kw = dict(kw)
        nav = (kw.pop("items", None), kw.pop("titlebar", None), kw.pop("title", None))
        if nav != (None, None, None):
            e.model = ("nav", (tuple(nav[0] or ()), bool(nav[1]), nav[2]))
    for name, value in kw.items():
        if value is None:
            continue
        if name == "key":
            e.key = value
        elif name == "focus":
            e.focus = value
        elif name == "items" and spec.virtual:
            count, item = value
            e.items = (count, item)
            e.props.append((XTK_PROP_ITEM_COUNT, K_I32, min(int(count), 2147483647)))
        elif name == "items" and spec.model in ("strings", "tabs", "selector"):
            e.model = (spec.model, tuple(value))
        elif name == "names" and spec.model == "names":
            e.model = ("strings", tuple(value))
        elif name in spec.props:
            pid, kind = spec.props[name]
            e.props.append((pid, kind, int(value) if kind == K_ENUM else value))
        elif name in spec.events:
            event, payload = spec.events[name]
            e.handlers[event] = (payload, value)
        else:
            raise TypeError(f"unknown property or event '{name}'")
    return e


cdef XtkNodeRef existing(XtkCtrl ctrl) noexcept:
    cdef XtkNodeRef r
    r.kind = XTK_REF_EXISTING
    r.u.existing = ctrl
    return r


cdef XtkNodeRef local_ref(XtkLocalId local) noexcept:
    cdef XtkNodeRef r
    r.kind = XTK_REF_LOCAL
    r.u.local = local
    return r


cdef XtkNodeRef no_ref() noexcept:
    cdef XtkNodeRef r
    memset(&r, 0, sizeof(r))
    return r


cdef XtkValue c_value(int kind, object v, list keep) except *:
    cdef XtkValue out
    cdef bytes raw
    memset(&out, 0, sizeof(out))
    if kind == K_BOOL:
        out.kind = XTK_VALUE_BOOL
        out.u.b = bool(v)
    elif kind == K_I32:
        out.kind = XTK_VALUE_I32
        out.u.i32 = int(v)
    elif kind == K_F32:
        out.kind = XTK_VALUE_F32
        out.u.f32 = float(v)
    elif kind == K_F64:
        out.kind = XTK_VALUE_F64
        out.u.f64 = float(v)
    elif kind == K_ENUM:
        out.kind = XTK_VALUE_ENUM
        out.u.u32 = int(v)
    elif kind == K_COLOR:
        out.kind = XTK_VALUE_COLOR
        out.u.color.rgba = int(v)
    elif kind == K_RESOURCE:
        out.kind = XTK_VALUE_RESOURCE
        out.u.resource = int(v)
    else:
        raw = str(v).encode("utf-8")
        keep.append(raw)
        out.kind = XTK_VALUE_STRING
        out.u.string.data = <char *>raw
        out.u.string.len = len(raw)
    return out


cdef object reset_value(int kind, uint32_t pid):
    if kind == K_F32 and (pid == XTK_PROP_WIDTH or pid == XTK_PROP_HEIGHT):
        return math.nan
    if kind == K_BOOL:
        return pid == XTK_PROP_ENABLED
    if kind == K_STRING:
        return ""
    return 0


cdef bint same(object a, object b):
    if isinstance(a, float) and isinstance(b, float) and a != a and b != b:
        return True
    return type(a) is type(b) and a == b


cdef bint wants_focus(object token):
    return token is not None and token is not False


cdef str text(const char *data, uint32_t length):
    if data == NULL or length == 0:
        return ""
    return data[:length].decode("utf-8", "replace")


cdef tuple payload_args(const XtkEventPayload *p):
    cdef int kind = p.kind
    if kind == XTK_EVENT_PAYLOAD_BOOL:
        return (bool(p.u.b),)
    if kind == XTK_EVENT_PAYLOAD_I32:
        return (p.u.i32,)
    if kind == XTK_EVENT_PAYLOAD_F32:
        return (p.u.f32,)
    if kind == XTK_EVENT_PAYLOAD_F64:
        return (p.u.f64,)
    if kind == XTK_EVENT_PAYLOAD_STRING:
        return (text(p.u.string.data, p.u.string.len),)
    if kind == XTK_EVENT_PAYLOAD_QUERY:
        return (text(p.u.query.text, p.u.query.len), p.u.query.index)
    if kind == XTK_EVENT_PAYLOAD_RATING:
        return (p.u.rating.value, p.u.rating.count)
    if kind == XTK_EVENT_PAYLOAD_INDEX_BOOL:
        return (p.u.index_bool.index, bool(p.u.index_bool.value))
    if kind == XTK_EVENT_PAYLOAD_RANGE:
        return (p.u.range.start, p.u.range.end)
    if kind == XTK_EVENT_PAYLOAD_SCROLL:
        return (ScrollPos(p.u.scroll.x, p.u.scroll.y, p.u.scroll.max_x, p.u.scroll.max_y),)
    return ()


cdef class Node:
    cdef Runtime rt
    cdef XtkCtrl ctrl
    cdef long local
    cdef uint32_t ty
    cdef object key
    cdef list props
    cdef dict handlers
    cdef list subs
    cdef list kids
    cdef object window
    cdef XtkChangeStamp echo
    cdef uint32_t user_events
    cdef object focus
    cdef object model

    cdef XtkNodeRef target(self):
        return local_ref(<XtkLocalId>self.local) if self.local >= 0 else existing(self.ctrl)


cdef uint32_t trampoline(void *arg, const XtkEvent *ev) noexcept with gil:
    cdef Node node = <Node>arg
    try:
        if ev.id == XTK_EVENT_REALIZE:
            node.window = (ev.payload.u.window.first, ev.payload.u.window.last, ev.payload.u.window.lanes)
            node.rt.dirty = True
            node.rt.wake()
            return XTK_EVENT_HANDLED
        if ev.change.revision > node.echo.revision:
            node.echo = ev.change
        if ev.cause == XTK_EVENT_CAUSE_USER and ev.id < 32:
            node.user_events |= 1u << ev.id
        hook = node.handlers.get(ev.id)
        if hook is None:
            return XTK_EVENT_CONTINUE
        payload, handler = hook
        msg = handler(*payload_args(&ev.payload)) if callable(handler) else handler
        node.rt.queue.append(msg)
        node.rt.wake()
        return XTK_EVENT_HANDLED
    except BaseException:
        traceback.print_exc()
        return XTK_EVENT_CONTINUE


cdef void frame_cb(void *ctx) noexcept with gil:
    try:
        (<Runtime>ctx).frame()
    except BaseException:
        traceback.print_exc()


cdef const char *cstr(object s, list keep) except? NULL:
    if s is None:
        return NULL
    raw = str(s).encode("utf-8")
    keep.append(raw)
    return <const char *>raw


cdef bint set_strings(XtkTxn *txn, XtkNodeRef target, tuple items) except *:
    cdef list keep = []
    cdef int n = len(items)
    cdef const char **arr = <const char **>PyMem_Malloc(max(n, 1) * sizeof(char *))
    if arr == NULL:
        raise MemoryError()
    try:
        for i, it in enumerate(items):
            arr[i] = cstr(it, keep)
        return xtk_txn_setitems(txn, target, arr, n)
    finally:
        PyMem_Free(arr)


cdef bint set_tabs(XtkTxn *txn, XtkNodeRef target, tuple items) except *:
    cdef list keep = []
    cdef int n = len(items)
    cdef XtkTabDesc *arr = <XtkTabDesc *>PyMem_Malloc(max(n, 1) * sizeof(XtkTabDesc))
    if arr == NULL:
        raise MemoryError()
    try:
        for i, it in enumerate(items):
            icon, label = (None, it) if isinstance(it, str) else it
            arr[i].icon = cstr(icon, keep)
            arr[i].label = cstr(label, keep)
        return xtk_txn_settabs(txn, target, arr, n)
    finally:
        PyMem_Free(arr)


cdef bint set_selector(XtkTxn *txn, XtkNodeRef target, tuple items) except *:
    cdef list keep = []
    cdef int n = len(items)
    cdef XtkSelectorItem *arr = <XtkSelectorItem *>PyMem_Malloc(max(n, 1) * sizeof(XtkSelectorItem))
    if arr == NULL:
        raise MemoryError()
    try:
        for i, it in enumerate(items):
            it = (None, it) if isinstance(it, str) else it
            arr[i].icon = cstr(it[0], keep)
            arr[i].text = cstr(it[1], keep)
            arr[i].disabled = len(it) > 2 and bool(it[2])
        return xtk_txn_setselitems(txn, target, arr, n)
    finally:
        PyMem_Free(arr)


cdef bint set_nav(XtkTxn *txn, XtkNodeRef target, tuple model) except *:
    cdef list keep = []
    items, titlebar, title = model
    cdef int n = len(items)
    cdef XtkNavDesc desc
    cdef XtkNavItemDesc *arr = <XtkNavItemDesc *>PyMem_Malloc(max(n, 1) * sizeof(XtkNavItemDesc))
    if arr == NULL:
        raise MemoryError()
    try:
        for i, it in enumerate(items):
            it = it if isinstance(it, tuple) else (it, None, None)
            arr[i].kind = int(it[0])
            arr[i].icon = cstr(it[1], keep)
            arr[i].label = cstr(it[2], keep)
        memset(&desc, 0, sizeof(desc))
        desc.items = arr
        desc.nitem = n
        desc.window_title_bar = XTK_NAV_TITLE_BAR_TALL if titlebar == XTK_NAV_TITLE_BAR_TALL else bool(titlebar)
        desc.app_title = cstr(title, keep)
        return xtk_txn_setnav(txn, target, &desc)
    finally:
        PyMem_Free(arr)


cdef void set_model(XtkTxn *txn, XtkNodeRef target, object model) except *:
    kind, value = model
    if kind == "strings":
        ok = set_strings(txn, target, value)
    elif kind == "tabs":
        ok = set_tabs(txn, target, value)
    elif kind == "selector":
        ok = set_selector(txn, target, value)
    else:
        ok = set_nav(txn, target, value)
    if not ok:
        raise ValueError(f"invalid {kind} items: {value!r}")


cdef object empty_model(object model):
    kind = model[0]
    return (kind, ((), False, None) if kind == "nav" else ())


cdef class Recon:
    cdef Runtime rt
    cdef XtkTxn *txn
    cdef list graveyard
    cdef Node focus

    cdef void realize(self, El e, object window) except *:
        if e.items is None:
            return
        count, item = e.items
        height = 600.0
        item_h = 40.0
        for pid, kind, value in e.props:
            if pid == XTK_PROP_HEIGHT and value > 0:
                height = value
            elif pid == XTK_PROP_ITEM_HEIGHT and value > 0:
                item_h = value
        first, last, lanes = window if window is not None else (0, math.ceil(height / item_h) + 3, 1)
        if last >= count:
            span = last - first
            last = count - 1
            first = max(last - span, 0)
            first -= first % max(lanes, 1)
        first = max(first, 0)
        e.props.append((XTK_PROP_REALIZED_FIRST, K_I32, first))
        span = max(last - first + 1, 1)
        for i in range(first, last + 1):
            row = El.__new__(El)
            row.ty = XTK_CTRL_LISTITEM
            row.key = i % span
            row.props = []
            row.handlers = {}
            row.kids = [item(i)]
            row.items = None
            row.focus = None
            row.model = None
            e.kids.append(row)

    cdef void subscribe(self, Node node, uint32_t event) except *:
        cdef XtkSubRef token = xtk_txn_on(self.txn, node.target(), event, XTK_EVENT_PHASE_MASK_TARGET,
                                          trampoline, <void *>node)
        if token == 0xFFFFFFFFu:
            raise RuntimeError(f"subscribe event {event} failed")
        node.subs.append([event, True, token, 0])

    cdef void subscribe_all(self, Node node, El e) except *:
        have = {s[0] for s in node.subs}
        for event in e.handlers:
            if event not in have:
                self.subscribe(node, event)
        if e.items is not None and XTK_EVENT_REALIZE not in have:
            self.subscribe(node, XTK_EVENT_REALIZE)

    cdef Node create(self, El e, XtkNodeRef parent, XtkNodeRef before):
        self.realize(e, None)
        cdef list keep = []
        cdef Py_ssize_t n = len(e.props)
        cdef XtkPropPatch *patches = <XtkPropPatch *>PyMem_Malloc(max(n, 1) * sizeof(XtkPropPatch))
        cdef XtkLocalId local
        if patches == NULL:
            raise MemoryError()
        try:
            for i, (pid, kind, value) in enumerate(e.props):
                patches[i].id = pid
                patches[i].value = c_value(kind, value, keep)
                patches[i].change.source = 0
                patches[i].change.revision = 0
            local = xtk_txn_create(self.txn, e.ty, parent, before, patches, <uint32_t>n)
        finally:
            PyMem_Free(patches)
        if local == 0xFFFFFFFFu:
            raise RuntimeError(f"create control type {e.ty} failed")
        cdef Node node = Node.__new__(Node)
        node.rt = self.rt
        node.ctrl = 0
        node.local = local
        node.ty = e.ty
        node.key = e.key
        node.props = list(e.props)
        node.handlers = e.handlers
        node.subs = []
        node.kids = []
        node.window = None
        node.user_events = 0
        node.focus = e.focus
        if wants_focus(e.focus):
            self.focus = node
        node.model = e.model
        if e.model is not None:
            set_model(self.txn, local_ref(local), e.model)
            self.reselect(local_ref(local), e)
        self.subscribe_all(node, e)
        for kid in e.kids:
            node.kids.append(self.create(kid, local_ref(local), no_ref()))
        return node

    cdef set forced(self, Node node):
        cdef XtkPropertyId out[XTK_MIRROR_MAX]
        cdef uint32_t n
        ids = set()
        for event in range(1, 32):
            if node.user_events & (1u << event):
                n = xtk_catalog_mirrors(node.ty, event, out)
                for i in range(n):
                    ids.add(out[i])
        node.user_events = 0
        return ids

    cdef void reselect(self, XtkNodeRef target, El e) except *:
        # Loading items resets the selection, and a selection sent before the items exist is dropped.
        # So send the selection again once the items are in.
        cdef list keep = []
        cdef XtkChangeStamp zero
        zero.source = 0
        zero.revision = 0
        for pid, kind, value in e.props:
            if pid == XTK_PROP_SELECTED_INDEX:
                if not xtk_txn_set(self.txn, target, pid, c_value(kind, value, keep), zero):
                    raise RuntimeError("set selection failed")

    cdef void set_prop(self, XtkCtrl ctrl, uint32_t pid, int kind, object value, XtkChangeStamp stamp) except *:
        cdef list keep = []
        if not xtk_txn_set(self.txn, existing(ctrl), pid, c_value(kind, value, keep), stamp):
            raise RuntimeError(f"set property {pid} failed")

    cdef void diff_props(self, Node node, El e) except *:
        cdef XtkChangeStamp zero
        zero.source = 0
        zero.revision = 0
        forced = self.forced(node)
        old = {pid: value for pid, kind, value in node.props}
        for pid, kind, value in e.props:
            if pid in old and same(old[pid], value) and pid not in forced:
                continue
            self.set_prop(node.ctrl, pid, kind, value, node.echo)
        now = {pid for pid, kind, value in e.props}
        for pid, kind, value in node.props:
            if pid not in now:
                self.set_prop(node.ctrl, pid, kind, reset_value(kind, pid), zero)

    cdef void diff_subs(self, Node node, El e) except *:
        kept = []
        for sub in node.subs:
            event = sub[0]
            wanted = event in e.handlers or (event == XTK_EVENT_REALIZE and e.items is not None)
            if wanted:
                kept.append(sub)
            elif not sub[1]:
                xtk_txn_off(self.txn, sub[3])
        node.subs = kept
        self.subscribe_all(node, e)

    cdef void update(self, Node node, El e) except *:
        self.realize(e, node.window)
        self.diff_props(node, e)
        if not same(node.model, e.model):
            set_model(self.txn, existing(node.ctrl), e.model if e.model is not None else empty_model(node.model))
            self.reselect(existing(node.ctrl), e)
        node.model = e.model
        node.handlers = e.handlers
        self.diff_subs(node, e)
        node.props = list(e.props)
        node.key = e.key
        if wants_focus(e.focus) and not same(node.focus, e.focus):
            self.focus = node
        node.focus = e.focus
        node.kids = self.reconcile_kids(node.kids, e.kids, existing(node.ctrl))

    cdef list match(self, list old, list new):
        keyed = {}
        for j, n in enumerate(old):
            if (<Node>n).key is not None:
                keyed[((<Node>n).key, (<Node>n).ty)] = j
        unkeyed = [j for j, n in enumerate(old) if (<Node>n).key is None]
        cursor = 0
        out = []
        for e in new:
            if (<El>e).key is not None:
                out.append(keyed.pop(((<El>e).key, (<El>e).ty), None))
                continue
            if cursor < len(unkeyed) and (<Node>old[unkeyed[cursor]]).ty == (<El>e).ty:
                out.append(unkeyed[cursor])
            else:
                out.append(None)
            cursor += 1
        return out

    cdef list reconcile_kids(self, list old, list new, XtkNodeRef parent):
        assign = self.match(old, new)
        taken = [False] * len(old)
        out = [None] * len(new)
        cdef XtkNodeRef next_ref = no_ref()
        cdef Node node
        min_after = len(old) + 1
        for i in range(len(new) - 1, -1, -1):
            oi = assign[i]
            if oi is not None:
                taken[oi] = True
                node = <Node>old[oi]
                self.update(node, new[i])
                if oi < min_after:
                    min_after = oi
                else:
                    xtk_txn_move(self.txn, parent, node.target(), next_ref)
            else:
                node = self.create(new[i], parent, next_ref)
            next_ref = node.target()
            out[i] = node
        for j, n in enumerate(old):
            if not taken[j]:
                xtk_txn_drop(self.txn, existing((<Node>n).ctrl))
                self.graveyard.append(n)
        return out


cdef void resolve(Node node, XtkBatchResult *result):
    if node.local >= 0:
        node.ctrl = result.controls[node.local].control
        node.local = -1
    for sub in node.subs:
        if sub[1]:
            sub[3] = result.subscriptions[<uint32_t>sub[2]].id
            sub[1] = False
    for kid in node.kids:
        resolve(<Node>kid, result)


cdef class Runtime:
    cdef object model
    cdef object update_fn
    cdef object view_fn
    cdef public list queue
    cdef public bint dirty
    cdef FluxApp *flux
    cdef XtkScene scene
    cdef XtkCtrl root
    cdef object tree

    cdef void wake(self) noexcept:
        if self.flux != NULL:
            flux_app_redraw(self.flux)

    cdef void frame(self) except *:
        drained = False
        while self.queue:
            msg = self.queue.pop(0)
            result = self.update_fn(self.model, msg)
            if result is not None:
                self.model = result
            drained = True
        if not drained and not self.dirty and self.tree is not None:
            return
        self.dirty = False
        top = self.view_fn(self.model)
        cdef XtkTxn txn
        cdef XtkBatchDiag diag
        cdef XtkBatchResult *result_ptr
        memset(&txn, 0, sizeof(txn))
        memset(&diag, 0, sizeof(diag))
        if not xtk_txn_begin(&self.scene, &txn):
            raise RuntimeError("begin transaction failed")
        cdef Recon recon = Recon.__new__(Recon)
        recon.rt = self
        recon.txn = &txn
        recon.graveyard = []
        recon.focus = None
        try:
            old = [self.tree] if self.tree is not None else []
            nodes = recon.reconcile_kids(old, [top], existing(self.root))
        except BaseException:
            xtk_txn_abort(&txn)
            self.dirty = True
            raise
        result_ptr = xtk_txn_commit(&txn, &diag)
        if result_ptr == NULL:
            raise RuntimeError(f"commit failed: stage {diag.stage} error {diag.error} op {diag.failed_op}")
        resolve(<Node>nodes[0], result_ptr)
        xtk_batchresult_destroy(result_ptr)
        self.tree = nodes[0]
        if recon.focus is not None:
            flux_app_setfocus(self.flux, recon.focus.ctrl)


cdef Runtime running = None


cdef void wake_cb(void *ctx) noexcept nogil:
    flux_app_redraw(<FluxApp *>ctx)


def post(msg):
    """Queue ``msg`` for ``update`` and wake the window thread. Safe to call from any thread.

    Returns False when no app is running; the message is dropped then.
    """
    cdef Runtime rt = running
    if rt is None or rt.flux == NULL:
        return False
    rt.queue.append(msg)
    flux_app_invoke(rt.flux, wake_cb, <void *>rt.flux)
    return True


def run(model, update, view, *, title="xenthon", width=960, height=640, theme=Theme.SYSTEM):
    cdef Runtime rt = Runtime.__new__(Runtime)
    cdef FluxAppCfg cfg
    cdef XtkHost *host
    cdef int code
    cdef wchar_t *wide = PyUnicode_AsWideCharString(str(title), NULL)
    memset(&cfg, 0, sizeof(cfg))
    cfg.title = wide
    cfg.width = width
    cfg.height = height
    cfg.theme = int(theme)
    cfg.backdrop = FLUX_BACKDROP_MICA
    flux_controls_all()
    rt.flux = flux_app_create(&cfg)
    PyMem_Free(wide)
    if rt.flux == NULL:
        return 1
    host = flux_app_attachhost(rt.flux)
    if host == NULL:
        flux_app_destroy(rt.flux)
        return 1
    rt.model = model
    rt.update_fn = update
    rt.view_fn = view
    rt.queue = []
    rt.dirty = True
    rt.tree = None
    rt.scene = xtk_scene_fromhost(host)
    rt.root = xtk_scene_root(&rt.scene)
    flux_app_onframe(rt.flux, frame_cb, <void *>rt)
    flux_app_redraw(rt.flux)
    global running
    running = rt
    try:
        with nogil:
            code = flux_app_run(rt.flux)
    finally:
        running = None
    flux_app_onframe(rt.flux, NULL, NULL)
    flux_host_destroy(host)
    flux_app_destroy(rt.flux)
    rt.flux = NULL
    rt.tree = None
    return code


include "_controls.pxi"
