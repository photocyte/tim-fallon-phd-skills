# Choose additional tooling by task

Start with the downloaded `docs/ecosystem.md`, resolved beneath the manifest's `sources.linkml.path`. Core LinkML validation, generators, runtime introspection and the project Copier workflow cover the usual schema-authoring loop. Add a tool only for a concrete gap; these packages are neither installed nor downloaded by `setup-linkml`.

| Need | Candidate and decision guidance |
|---|---|
| Bootstrap a model from existing schemas or data | **schema-automator** can import JSON Schema and infer from tabular data. Treat output as a draft: verify meanings, identifiers, optionality and constraints against requirements, not only observed examples. See its [source README](https://raw.githubusercontent.com/linkml/schema-automator/main/README.md). |
| Execute mappings between different data models | **linkml-map**, formerly **linkml-transformer**, supports declarative transformations. Semantic annotations such as `exact_mappings` are not executable field transformations. Its model is not fully stable and implementation coverage varies; test the specific mapping and any claimed reversibility. See its [source README](https://raw.githubusercontent.com/linkml/linkml-map/main/README.md). |
| Produce a readable view of instance records | **linkml-renderer** generates HTML, Markdown and Mermaid from data. This differs from core `gen-doc`, which documents a schema. The renderer is experimental; its authors note schema-specific templates may give better results. Compare with a small existing renderer before adding it. See its [source README](https://raw.githubusercontent.com/linkml/linkml-renderer/main/README.md). |

Repository identities and scopes were checked on 2026-11-01. These `main` README links are discovery sources, not reproducibility pins. Before adoption, inspect the selected release's documentation, CLI and examples, pin its dependencies, and check compatibility with the project's LinkML version. The cached ecosystem page still uses the older transformer name.

For ontology QC, reference/quotation checks, structured storage/querying, or ontology traversal, use the task-specific skills already linked from [linkml-docs](../SKILL.md). Those checks address different questions: a valid record, a matching quotation, and evidence supporting a claim are distinct outcomes.

Other ecosystem tools remain discoverable through the local index. There is no need to install an ecosystem bundle, documentation MCP server, or another schema-authoring framework merely to use these two skills.
