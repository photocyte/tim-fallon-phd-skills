#!/usr/bin/env python3
"""Cache release-matched Nextflow docs and keep a history of Seqera's live exports."""

import argparse
import fcntl
import hashlib
import json
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO = "https://github.com/nextflow-io/nextflow.git"
TAG = "v26.10.7"
COMMIT = "0ad848ef3c3a22824cd9eb2ca14568385867702d"
SKILLS_REPO = "https://github.com/seqeralabs/nextflow-plugin.git"
SKILLS_COMMIT = "d5700676b234f52cbc693466eb8d355783fc83fb"
SKILLS_DIR = Path("plugins/nextflow/skills")
EXPORTS = ("llms.txt", "llms-full.txt")
CONSTITUTION = ".specify/memory/constitution.md"
DOCS = ["/docs/", "!/docs/_static/"]
FULL_CONSTITUTION_DOCS = [*DOCS, f"/{CONSTITUTION}"]


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def release_docs(cache, stage, refresh):
    path = cache / f"nextflow-{COMMIT}"
    fresh = not path.exists()
    repo = stage / "repo" if fresh else path
    if fresh:
        repo.mkdir()
        git(repo, "init", "--quiet")
        git(repo, "remote", "add", "origin", REPO)
    if git(repo, "remote", "get-url", "origin") != REPO:
        raise ValueError(f"Unexpected origin in {repo}")
    if fresh or refresh:
        git(repo, "fetch", "--quiet", "--depth=1", "--filter=blob:none", "origin", f"refs/tags/{TAG}")
        if git(repo, "rev-parse", "FETCH_HEAD^{commit}") != COMMIT:
            raise ValueError(f"{TAG} no longer matches {COMMIT}")
    snippet = f"constitution-iii-{COMMIT}.md"
    source = Path(__file__).resolve().parents[1] / "references" / snippet
    content = source.read_bytes()
    cached = cache / snippet
    if cached.exists() and cached.read_bytes() != content:
        raise ValueError(f"Modified constitution excerpt: {cached}. Preserve it and use a fresh cache.")
    if fresh:
        git(repo, "sparse-checkout", "set", "--no-cone", *DOCS)
        git(repo, "checkout", "--quiet", "--detach", COMMIT)
    elif (git(repo, "sparse-checkout", "list").splitlines() == FULL_CONSTITUTION_DOCS
          and git(repo, "rev-parse", "HEAD") == COMMIT and not git(repo, "status", "--porcelain")):
        git(repo, "sparse-checkout", "set", "--no-cone", *DOCS)
    if (git(repo, "rev-parse", "HEAD") != COMMIT or git(repo, "status", "--porcelain")
            or git(repo, "sparse-checkout", "list").splitlines() != DOCS
            or not (repo / "docs/index.mdx").is_file() or (repo / CONSTITUTION).exists()):
        raise ValueError(f"Release checkout changed or incomplete: {repo}. Preserve it and use a fresh cache.")
    if fresh:
        repo.rename(path)
    if not cached.exists():
        staged = stage / snippet
        staged.write_bytes(content)
        staged.replace(cached)
    return {"url": REPO, "release": TAG, "commit": COMMIT, "path": path.name,
            "constitution_section_iii": snippet}


def agent_skills(cache, stage):
    path = cache / f"nextflow-plugin-{SKILLS_COMMIT}"
    fresh = not path.exists()
    repo = stage / "plugin" if fresh else path
    if fresh:
        repo.mkdir()
        git(repo, "init", "--quiet")
        git(repo, "remote", "add", "origin", SKILLS_REPO)
        git(repo, "fetch", "--quiet", "--depth=1", "origin", SKILLS_COMMIT)
        git(repo, "checkout", "--quiet", "--detach", SKILLS_COMMIT)
    if (git(repo, "remote", "get-url", "origin") != SKILLS_REPO
            or git(repo, "rev-parse", "HEAD") != SKILLS_COMMIT or git(repo, "status", "--porcelain")
            or not (repo / SKILLS_DIR / "migrate-nextflow-code/SKILL.md").is_file()):
        raise ValueError(f"Agent skills checkout changed or incomplete: {repo}. Preserve it and use a fresh cache.")
    if fresh:
        repo.rename(path)
    return {"url": SKILLS_REPO, "commit": SKILLS_COMMIT, "path": str(Path(path.name) / SKILLS_DIR)}


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_snapshot(cache, snapshot):
    for name in EXPORTS:
        path = cache / snapshot["path"] / name
        if checksum(path) != snapshot["files"][name]["sha256"]:
            raise ValueError(f"Modified export: {path}. Preserve it and use a fresh cache.")


def fetch_snapshot(cache, stage, previous, now):
    downloads = stage / "exports"
    downloads.mkdir()
    files = {}
    for name in EXPORTS:
        url = f"https://docs.seqera.io/{name}"
        path = downloads / name
        subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location",
                        "--output", str(path), url], check=True)
        content = path.read_text(encoding="utf-8")
        if not content.startswith("# Seqera Docs\n") or "\n# Nextflow\n" not in content:
            raise ValueError(f"Unexpected content at {url}. Check the response before replacing the cache.")
        files[name] = {"url": url, "sha256": checksum(path)}
    if previous and files == previous["files"]:
        print("Seqera exports unchanged")
        return previous
    relative = Path("seqera") / now.strftime("%Y%m%dT%H%M%S.%fZ")
    snapshot = {"path": str(relative), "retrieved_at": now.isoformat(), "files": files,
                "previous_path": previous["path"] if previous else None}
    (downloads / "snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n")
    (cache / relative.parent).mkdir(exist_ok=True)
    downloads.rename(cache / relative)
    for name in EXPORTS:
        if not previous or previous["files"][name] != files[name]:
            print(f"Saved {relative / name}")
    return snapshot


def setup(cache, refresh):
    manifest = cache / "manifest.json"
    old = json.loads(manifest.read_text()) if manifest.exists() else {}
    previous = old.get("seqera")
    if previous:
        verify_snapshot(cache, previous)
    with tempfile.TemporaryDirectory(dir=cache) as temp:
        stage = Path(temp)
        release = release_docs(cache, stage, refresh)
        skills = agent_skills(cache, stage)
        if previous and not refresh and old["nextflow"] == release and old.get("agent_skills") == skills:
            print(f"Reused offline: {manifest}")
            return
        now = datetime.now(timezone.utc)
        snapshot = fetch_snapshot(cache, stage, previous, now) if refresh or not previous else previous
        checked = now.isoformat() if refresh or not previous else old["seqera_checked_at"]
        record = {"nextflow": release, "agent_skills": skills, "seqera": snapshot, "seqera_checked_at": checked}
        staged = stage / "manifest.json"
        staged.write_text(json.dumps(record, indent=2) + "\n")
        staged.replace(manifest)
    print(manifest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=Path(".tools/nextflow-docs"))
    parser.add_argument("--refresh", action="store_true", help="Recheck the release tag and both live exports")
    args = parser.parse_args()
    cache = args.cache.resolve()
    cache.mkdir(parents=True, exist_ok=True)
    with (cache / ".setup.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        setup(cache, args.refresh)


if __name__ == "__main__":
    try:
        main()
    except (OSError, KeyError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Documentation setup failed: {error}")
