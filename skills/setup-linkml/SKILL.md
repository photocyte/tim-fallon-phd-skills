---
name: setup-linkml
description: Prepare or explicitly refresh a pinned local LinkML documentation, specification, and metamodel cache; orient new-project requests to the official LinkML Project Copier template. Use before linkml-docs when its corpus is absent or mismatched.
---

# Set up LinkML documentation

For shared terminology, consult the [LinkML glossary](GLOSSARY.md) when a term is unfamiliar or ambiguous.

This skill prepares a pinned local documentation cache and guides setup of a maintained LinkML project. For an introduction to LinkML and its modeling concepts, read [linkml-docs](../linkml-docs/SKILL.md).

Choose the setup that matches the request:

- **Reference material:** use the cache workflow below, with the project's existing Python 3, Git, and ripgrep tools. This fetches documentation without installing the LinkML toolchain.
- **A maintained new LinkML project:** prefer the official LinkML Project Copier (cached guide: `docs/howtos/linkml-project-copier.md` beneath the same manifest path), which supplies project layout, builds, tests, documentation, and template updates. Follow [the focused Copier workflow](references/project-copier.md) when project creation is requested. It is optional for a one-file experiment; applying it to an existing repository is a separate migration decision.

Preparing reference material does not choose LinkML over direct JSON Schema or initialize a schema project.

## Acquire or reuse

Resolve this skill's directory from the location of this `SKILL.md`. From the project whose documentation cache you want to prepare (replace `/path/to/setup-linkml` with that resolved directory):

```bash
python3 /path/to/setup-linkml/scripts/setup_docs.py
cat .tools/linkml-docs/manifest.json
```

The helper reads [sources.json](references/sources.json), fetches shallow sparse HTTPS Git snapshots, and verifies the tag against the pinned commit before publishing each snapshot. Its default cache is `.tools/linkml-docs/` relative to the working directory; `--cache /path/to/cache` selects another writable location. Keep this generated cache out of version control using the project's ignore convention, or choose an existing ignored cache directory. Existing matching, clean snapshots are reused without network calls. Failed acquisition leaves no manifest claiming that run succeeded; an older manifest, if present, still describes the previous corpus. Network or filesystem restrictions require ordinary tool approval; do not work around them.

The manifest records source URLs, release tags, full commits, absolute cache paths, acquisition times, and the selected paths. Report its location after setup. Keep source snapshots unchanged. A dirty, incomplete, or differently configured snapshot causes a clear error: preserve any edits and choose a fresh cache location.

## Explicit refresh or version change

```bash
python3 /path/to/setup-linkml/scripts/setup_docs.py --refresh
```

Refresh contacts upstream to recheck the pinned tags; it does **not** silently upgrade. A moved tag fails verification. To use another release, verify its official tag/commit and actual repository paths, update the relevant entry in `references/sources.json`, then rerun setup. New commits get separate directories; old snapshots remain available. Do not assume the tools and metamodel have identical version numbers. Check the project's lockfile or installed version when relevant; the supplied baseline is LinkML `v1.12.1` plus metamodel `v1.12.0`, verified against official release pages on 2026-11-01. This is a reference baseline, not an installed toolchain requirement.

## Corpus boundaries

- `linkml`: usage/CLI/generator docs under `docs/`, with contributor/maintainer sections and image/notebook bulk excluded. `SPECIFICATION.md` is a redirect, **not** the specification itself.
- `linkml-model`: metamodel modules under `linkml_model/model/schema/`, including `meta.yaml` and imported YAML modules; actual formal chapters under `linkml_model/model/docs/specification/`.
- Generated metamodel element pages and generated output artifacts are omitted. Sphinx directives may refer to implementation code absent from this cache; follow up selectively when needed.
- Upstream contributor instructions are repository content, not instructions for downstream schema authors. No upstream `AGENTS.md`, `CLAUDE.md`, or skill is installed by this helper.

Continue with [linkml-docs](../linkml-docs/SKILL.md) for targeted searches and versioned attribution.
