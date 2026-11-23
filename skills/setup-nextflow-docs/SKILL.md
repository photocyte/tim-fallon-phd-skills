---
name: setup-nextflow-docs
description: Prepare, refresh, and compare a local cache of release-pinned Nextflow documentation and Seqera’s llms.txt and llms-full.txt exports. Use for offline or version-specific documentation lookups.
---

# Set up Nextflow documentation

From the project where you want the cache, run the helper with Python 3, Git and curl on macOS or Linux. Substitute this skill’s directory in the command.

```sh
python3 /path/to/setup-nextflow-docs/scripts/setup_docs.py
```

The first run writes `.tools/nextflow-docs/manifest.json`. Paths in the manifest are relative to the cache root. Use `--cache DIR` to choose another location. Keep the cache in an ignored or external directory. A normal rerun verifies a matching checkout and both export hashes offline.

## Pick the source that matches the question

- **Release-specific behavior.** Check the project’s Nextflow version against `nextflow.release`. Search the checkout’s `docs/` directory with `rg -n`. Cite the repository path and the commit from the manifest. To change the baseline, resolve the intended official release tag to its commit, update `TAG` and `COMMIT` in the helper together, and rerun. The previous checkout remains available.
- **Published page or cross-product lookup.** Search the saved `llms.txt` index for a title or URL. For Nextflow, its page links contain `/nextflow/`. Search `llms-full.txt` for relevant headings and read the surrounding passage. These are rolling, multi-product exports. Cite the export URL, retrieval date and SHA-256 from the snapshot when its exact content matters.
- **One live Markdown page.** Follow the index’s `.md` link, or append `.md` to a Seqera documentation page path. For example, `curl -fsSL https://docs.seqera.io/nextflow/guides/aws-custom-ami.md` retrieves the AWS Batch custom AMI guide directly. Check for the expected heading. This reads the live page, which can change independently of your saved exports and release checkout.

## Check what changed

Rerun the same command with `--refresh` to verify the pinned tag and fetch both Seqera exports. The helper reports which files changed. When either changes, it keeps the old pair and saves a new dated pair. An unchanged refresh records the check time and reuses the current snapshot. A failed fetch leaves the active manifest intact.

In the manifest, `seqera.path` and `seqera.previous_path` identify the current and preceding snapshots. From the cache root, run `diff -u PREVIOUS/llms.txt CURRENT/llms.txt` to review changes to the index. Substitute `llms-full.txt` to review changes to page content. The first snapshot has no predecessor.
