import argparse
import base64
import hashlib
import pathlib
import tomllib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "src" / "xenthon"
SOURCES = ["__init__.py", "_controls.py", "_controls.pyi"]
PLATFORMS = {"x86_64": "win_amd64", "arm64": "win_arm64"}


def digest(data):
    return "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()


def metadata(project):
    lines = [
        "Metadata-Version: 2.4",
        f"Name: {project['name']}",
        f"Version: {project['version']}",
        f"Summary: {project['description']}",
        f"Requires-Python: {project['requires-python']}",
        f"License-Expression: {project['license']}",
        f"Keywords: {','.join(project['keywords'])}",
    ]
    lines += [f"License-File: {name}" for name in project["license-files"]]
    lines += [f"Classifier: {c}" for c in project["classifiers"]]
    lines += [f"Project-URL: {k}, {v}" for k, v in project["urls"].items()]
    return "\n".join(lines) + "\n"


def entries(project, pyd, tag):
    info = f"{project['name']}-{project['version']}.dist-info"
    files = [(f"xenthon/{name}", (PACKAGE / name).read_bytes()) for name in SOURCES]
    files.append(("xenthon/_reconcile.pyd", pyd.read_bytes()))
    files += [(f"{info}/licenses/{name}", (ROOT / name).read_bytes()) for name in project["license-files"]]
    files.append((f"{info}/METADATA", metadata(project).encode()))
    wheel = f"Wheel-Version: 1.0\nGenerator: xenthon-wheel\nRoot-Is-Purelib: false\nTag: {tag}\n"
    files.append((f"{info}/WHEEL", wheel.encode()))
    record = "".join(f"{name},{digest(data)},{len(data)}\n" for name, data in files)
    files.append((f"{info}/RECORD", (record + f"{info}/RECORD,,\n").encode()))
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pyd", type=pathlib.Path)
    parser.add_argument("--arch", choices=PLATFORMS, default="x86_64")
    parser.add_argument("--out", type=pathlib.Path, default=ROOT / "build" / "wheels")
    args = parser.parse_args()
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    tag = f"cp312-abi3-{PLATFORMS[args.arch]}"
    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / f"{project['name']}-{project['version']}-{tag}.whl"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in entries(project, args.pyd, tag):
            zf.writestr(zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0)), data, zipfile.ZIP_DEFLATED)
    print(f"{target}  {target.stat().st_size} bytes")


main()
