#!/usr/bin/env python3
"""Acquire pinned official documentation only; no LinkML installation."""

import argparse
import datetime
import json
from pathlib import Path
import subprocess
import tempfile


def git(path, *args, input=None):
    return subprocess.check_output(
        ["git", "-C", str(path), *args], input=input, text=True
    ).strip()


def verify(path, source):
    if git(path, "rev-parse", "HEAD") != source["commit"]:
        raise ValueError(f"Wrong revision in {path}; preserve it and use a new --cache")
    if git(path, "remote", "get-url", "origin") != source["url"]:
        raise ValueError(f"Unexpected origin in {path}")
    if git(path, "status", "--porcelain", "--untracked-files=all"):
        raise ValueError(f"Modified cache {path}; preserve edits and use a new --cache")
    if git(path, "sparse-checkout", "list").splitlines() != source["patterns"]:
        raise ValueError(f"Changed selection in {path}; use a new --cache")
    for relative in source["required"]:
        if not (path / relative).is_file():
            raise ValueError(f"Missing documentation: {path / relative}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=Path(".tools/linkml-docs"))
    parser.add_argument("--refresh", action="store_true", help="Recheck pinned tags online; do not upgrade")
    args = parser.parse_args()
    pins = Path(__file__).resolve().parents[1] / "references/sources.json"
    sources = json.loads(pins.read_text())
    cache = args.cache.resolve()
    cache.mkdir(parents=True, exist_ok=True)
    records = {}
    for name, source in sources.items():
        path = cache / f"{name}-{source['commit']}"
        if path.exists():
            verify(path, source)
            if args.refresh:
                git(path, "fetch", "--depth=1", "--filter=blob:none", "origin", f"refs/tags/{source['version']}")
                if git(path, "rev-parse", "FETCH_HEAD^{commit}") != source["commit"]:
                    raise ValueError(f"Upstream tag moved for {name}; investigate before changing pins")
            action = "REFRESHED" if args.refresh else "REUSED (offline)"
        else:
            # Publish a snapshot only after both fetch and content checks succeed.
            with tempfile.TemporaryDirectory(prefix=f".{name}-", dir=cache) as staging:
                stage = Path(staging) / "repo"
                stage.mkdir()
                git(stage, "init", "--quiet")
                git(stage, "remote", "add", "origin", source["url"])
                git(stage, "fetch", "--depth=1", "--filter=blob:none", "origin", f"refs/tags/{source['version']}")
                if git(stage, "rev-parse", "FETCH_HEAD^{commit}") != source["commit"]:
                    raise ValueError(f"Tag does not match pinned commit for {name}")
                git(stage, "sparse-checkout", "init", "--no-cone")
                git(stage, "sparse-checkout", "set", "--no-cone", "--stdin", input="\n".join(source["patterns"]) + "\n")
                git(stage, "checkout", "--quiet", "--detach", source["commit"])
                verify(stage, source)
                acquired = datetime.datetime.now(datetime.timezone.utc).isoformat()
                (stage / ".git/acquired-at").write_text(acquired + "\n")
                stage.rename(path)
            action = "FETCHED"
        records[name] = {**source, "path": str(path), "acquired_at": (path / ".git/acquired-at").read_text().strip()}
        print(f"{action}: {name} {source['version']} {source['commit']} {path}")
    manifest = {"format": 1, "cache": str(cache), "sources": records}
    # Never publish a manifest describing a partially successful run.
    with tempfile.NamedTemporaryFile(mode="w", dir=cache, prefix=".manifest-", delete=False) as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")
    Path(handle.name).replace(cache / "manifest.json")
    print(f"Manifest: {cache / 'manifest.json'}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Documentation setup failed: {error}")
