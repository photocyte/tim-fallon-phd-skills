---
name: nextflow-docs
description: Answer Nextflow pipeline authoring, configuration, execution and troubleshooting questions from a local release-pinned manual and dated Seqera documentation. Use setup-nextflow-docs to acquire or refresh the sources.
---

# Read Nextflow documentation

Read the project’s `.tools/nextflow-docs/manifest.json`, or the manifest in its selected cache directory. Resolve each recorded path relative to the manifest’s directory. Compare `nextflow.release` with the version in the question or the project’s runtime. If they differ, identify which release the answer covers. For a missing cache or a required version change, follow [setup-nextflow-docs](../setup-nextflow-docs/SKILL.md).

## Look up release-specific behavior

Start under `nextflow.path/docs/`. For workflow syntax and process directives, start with `workflow.mdx`, `process.mdx` or `reference/`. For settings and execution backends, use `config.mdx` and the matching `reference/config/` or `reference/executor/` entry. For behavior that changed between releases, check `migrations/` and read version annotations around the relevant option.

For example, to investigate why a task ran again with `-resume`, run this from the cache directory:

```sh
release_dir=$(python3 -c 'import json; print(json.load(open("manifest.json"))["nextflow"]["path"])')
rg -n -C 2 'matching hash|exit code' "$release_dir/docs/cache-and-resume.mdx"
```

Explain the conditions that apply to the user’s case. Cite the release and link to the supporting lines using `https://github.com/nextflow-io/nextflow/blob/<nextflow.commit>/docs/<file>#L<line>`.

## Look up a published Seqera page

Under `seqera.path`, search `llms.txt` for the page title or URL. Match the product in the URL: Nextflow and Seqera Platform have separate guides on topics such as caching. Find the matching heading in `llms-full.txt` and read the surrounding passage. Cite the page and the snapshot’s `seqera.retrieved_at`; include the export’s SHA-256 from `seqera.files` when identifying exact text.

For a live check, follow the index’s Markdown link or append `.md` to the page path. Verify the heading and identify the page as live when comparing it with the pinned manual. [Example Markdown page for AWS Batch custom AMIs](https://docs.seqera.io/nextflow/guides/aws-custom-ami.md)

For historical questions about upstream contributor practices, the setup skill links the [final development constitution and its removal PR](../setup-nextflow-docs/SKILL.md#contributor-history).
