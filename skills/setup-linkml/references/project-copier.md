# Start and maintain a LinkML project with Copier

Use the official LinkML Project Copier guide at `docs/howtos/linkml-project-copier.md` beneath the manifest’s `sources.linkml.path` when the user wants a maintained new schema project. Copier creates the layout, dependency configuration, generation/test recipes, documentation, and optional CI workflows; it also carries template improvements forward. For a small schema experiment, a YAML file and the relevant LinkML commands may suffice. For an existing repository, consult the template's migration guidance and preserve its conventions rather than automatically applying a scaffold.

## Prepare and generate

1. Confirm the destination and select a template release. The verified reference here is **v0.5.0**, commit `1d52a14e42db05ae0a3bff03350309dae437c531` (checked 2026-11-01). Inspect that ref's [README](https://github.com/linkml/linkml-project-copier/blob/1d52a14e42db05ae0a3bff03350309dae437c531/README.md), [copier.yaml](https://github.com/linkml/linkml-project-copier/blob/1d52a14e42db05ae0a3bff03350309dae437c531/copier.yaml), and [template/justfile](https://github.com/linkml/linkml-project-copier/blob/1d52a14e42db05ae0a3bff03350309dae437c531/template/justfile). A later release may be preferable; verify its changes and pin it explicitly. The template version is independent of the documentation cache's LinkML/metamodel versions and the generated project's dependency lock.
2. Check existing **Git, Python >=3.10, Copier >=9.4.0 with `jinja2-time`, uv, and just**, using the project's environment conventions. The template assumes GitHub hosting for its CI/publishing features. If installation is part of the requested setup, the README documents `uv tool install --with jinja2-time copier` and `uv tool install rust-just`; reuse installed tools where available.
3. Derive prompt answers from the user's requirements and repository metadata: project name/slug, description, author/email, GitHub organization, license, example schema, and publishing/preview choices. Ask for missing identity, licensing, or publication choices rather than treating placeholder defaults as facts. Inspect the selected template's extensions, tasks, and migrations before using `--trust`: here it enables the `jinja2_time` extension, and update migrations can execute commands.
4. In the intended new project directory, generate the selected template. For the verified baseline:

   ```bash
   copier copy --trust --vcs-ref 1d52a14e42db05ae0a3bff03350309dae437c531 https://github.com/linkml/linkml-project-copier .
   ```

Keep the generated Copier answers file (normally `.copier-answers.yml`) in version control, including its source and revision metadata. Review generated settings and CI options before publishing. Source schema edits belong under `src/<project_slug>/schema/`; build outputs are regenerated from them.

## Use the generated workflow

Read the generated `justfile` and `project.justfile`; customizations or later template releases may change these recipes. At the verified ref:

| Command | What it actually does |
|---|---|
| `just setup` | Initializes Git, installs project/dev dependencies with `uv sync --group dev`, stages files and attempts an initial commit, then generates model artifacts and docs. Generated files are not part of that commit. Use for the newly created project. |
| `just gen-project` / `just gen-doc` | Regenerates configured representations / schema reference documentation. |
| `just test` | Tests schema generation, regenerates Python models and runs pytest, and exercises valid and invalid JSON/YAML examples. This does not prove every generator implements every modeled constraint. |
| `just lint` | Runs LinkML schema linting separately from the test recipe. |
| `just testdoc` | Generates docs and starts a local MkDocs preview server. |

For agent work, iterate on schema and representative valid/invalid examples, regenerate, run the relevant checks, and inspect the changed outputs. Report what ran and what it establishes. Scaffolding and these local workflows do not require publishing to GitHub or PyPI.

## Carry template improvements forward

From a clean committed project state, inspect the intended new template revision and run `copier update --trust --vcs-ref <chosen-ref>`. Add `--skip-answered` to retain existing answers without re-prompting. Preserve the answers file, review the resulting diff, resolve any conflicts, then rerun the relevant generation, tests, and lint checks. Some paths are marked `_skip_if_exists` in `copier.yaml`, so an update intentionally leaves those existing files untouched.

The guide's unpinned `copier update --trust` follows Copier's release selection; an explicit ref makes the update reviewable. At v0.5.0, **`just update` additionally upgrades the LinkML and linkml-runtime dependency locks**. Choose that broader update only when dependency upgrades are part of the work.
