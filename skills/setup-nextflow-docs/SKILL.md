---
name: setup-nextflow-docs
description: Prepare, refresh, and compare a local cache of release-pinned Nextflow documentation, official agent skills and Seqera’s llms.txt and llms-full.txt exports. Use when the cache is missing, needs a different release, or needs an upstream change check.
---

# Set up Nextflow documentation

From the project where you want the cache, run the helper with Python 3, Git and curl on macOS or Linux. Substitute this skill’s directory in the command.

```sh
python3 /path/to/setup-nextflow-docs/scripts/setup_docs.py
```

The first run writes `.tools/nextflow-docs/manifest.json`. Paths in the manifest are relative to the cache root. Use `--cache DIR` to choose another location. Keep the cache in an ignored or external directory. Rerunning setup upgrades an older docs-only checkout in place. The first upgrade needs network access to fetch any missing constitution and agent skills. Subsequent reruns verify both checkouts and both export hashes offline.

For questions about workflow syntax, configuration, execution or troubleshooting, use the companion [nextflow-docs](../nextflow-docs/SKILL.md) skill to search and cite the cache.

To change the release baseline, resolve the intended official release tag to its commit, update `TAG` and `COMMIT` in the helper together, and rerun. The previous checkout remains available.

## Local Nextflow agent skills

The manifest’s `agent_skills.path` points directly to the skill folders in a complete checkout of [Seqera’s Nextflow plugin](https://github.com/seqeralabs/nextflow-plugin). Each folder contains its `SKILL.md` and any supporting files. The former [agent-skills repository](https://github.com/nextflow-io/agent-skills) identifies this plugin as its successor. Setup caches the files for offline reading. To update that independent pin, change `SKILLS_COMMIT` to the desired upstream commit and rerun setup.

## Contributor history

Read `.specify/memory/constitution.md` under the manifest’s `nextflow.path`. Nextflow’s final development constitution records the project’s principles for architecture, testing and releases. The copy in `v26.10.7` matches the last version on `master` before the maintainers removed Spec Kit. Their October 2026 PR explains the removal, the switch to a shorter `AGENTS.md`, and the move of design records under `docs/`. [Final constitution](https://github.com/nextflow-io/nextflow/blob/0ad848ef3c3a22824cd9eb2ca14568385867702d/.specify/memory/constitution.md) · [PR #7970](https://github.com/nextflow-io/nextflow/pull/7970)

## Check what changed

Rerun the same command with `--refresh` to verify the pinned tag and fetch both Seqera exports. The helper reports which files changed. When either changes, it keeps the old pair and saves a new dated pair. An unchanged refresh records the check time and reuses the current snapshot. A failed fetch leaves the active manifest intact.

In the manifest, `seqera.path` and `seqera.previous_path` identify the current and preceding snapshots. From the cache root, run `diff -u PREVIOUS/llms.txt CURRENT/llms.txt` to review changes to the index. Substitute `llms-full.txt` to review changes to page content. The first snapshot has no predecessor.
