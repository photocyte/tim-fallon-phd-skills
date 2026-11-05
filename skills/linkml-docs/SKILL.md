---
name: linkml-docs
description: Answer LinkML modeling, validation, and generator questions by searching a pinned local official docs/specification/metamodel corpus, with source path and revision attribution. Use setup-linkml for missing or mismatched documentation.
---

# Read LinkML documentation selectively

For shared terminology, consult the [LinkML glossary](../setup-linkml/GLOSSARY.md) when a term is unfamiliar or ambiguous.

LinkML expresses data models and validation rules in YAML: **classes** describe entities, **slots** their properties, **types** value domains, and **enums** permitted values. Constraints express requirements such as cardinality and patterns; identifiers, vocabulary URIs, and mappings connect the model to other schemas. The toolchain validates schemas/data and generates documentation, JSON Schema, Python/Pydantic models, and other targets, with target-specific limits. Read the cached official overview at `docs/intro/overview.md`; resolve corpus paths from the manifest as described below.

For an LLM agent, the useful loop is to express the agreed data structure, meanings, and validation rules in a schema, generate the needed representations, and use validation and example tests to correct mistakes. The local corpus helps choose the right construct and interpret failures; semantic agreement and support in the chosen target still need checking. For a maintained **new** project, start from the official LinkML Project Copier guide at `docs/howtos/linkml-project-copier.md`; use [its setup and lifecycle workflow](../setup-linkml/references/project-copier.md) when scaffolding is requested. A documentation lookup alone does not create a project.

## Research workflow

1. Read `.tools/linkml-docs/manifest.json` (or the explicitly selected cache's manifest). Check source versions against the question and any project lockfile or known installed tools. For missing, changed, or mismatched documentation, use [setup-linkml](../setup-linkml/SKILL.md); its normal run verifies and reuses clean snapshots offline. Do not call an old pin “latest” or substitute a current web page for an older release without saying so.
2. Choose the smallest relevant source area below. Use `rg -l` to find files, `rg -n` for hits, then `sed -n` or `nl -ba` for a bounded passage. Read surrounding conditions and linked/imported definitions before interpreting a match. Do not ingest the entire cache.
3. Answer with the release, repository-relative path, full commit (or a unique abbreviation with the full revision in the link), and relevant lines/section. Distinguish language semantics from what a particular generator or validator implements. Conflicting or incomplete evidence should stay explicit.

## Navigation

All corpus paths below refer to the downloaded Markdown/reStructuredText sources, not hosted HTML or paths relative to this skill. Resolve `linkml:` paths beneath `DOCS` and `linkml-model:` paths beneath `MODEL`; the cache location is configurable.

Assign `DOCS` and `MODEL` from the manifest's `sources.linkml.path` and `sources.linkml-model.path`; do not assume versioned directory names. Keep these assignments and dependent searches in the **same shell invocation**; variables do not persist between tool calls:

```bash
DOCS=$(python3 -c 'import json; print(json.load(open(".tools/linkml-docs/manifest.json"))["sources"]["linkml"]["path"])')
MODEL=$(python3 -c 'import json; print(json.load(open(".tools/linkml-docs/manifest.json"))["sources"]["linkml-model"]["path"])')
rg -n '^##|^###|supports arrays' "$DOCS/docs/schemas/arrays.md"
rg -n '^  (array|array_expression|dimensions|maximum_number_dimensions):' "$MODEL/linkml_model/model/schema/meta.yaml"
rg -n '^  (multivalued|inlined|inlined_as_list|identifier|key|slot_usage|status):' "$MODEL/linkml_model/model/schema/meta.yaml"
rg -n 'additionalProperties|extra_slots|gen-json-schema|array' "$DOCS/docs/generators/json-schema.rst"
```

| Question | Start here, relative to the matching repository |
|---|---|
| What LinkML does; how its concepts fit together | `linkml: docs/intro/overview.md` |
| Decide whether LinkML fits the task | `linkml: docs/faq/why-linkml.md`: compare modeling needs with direct JSON Schema and other alternatives. |
| Start a maintained project; build, test, and update its scaffold | `linkml: docs/howtos/linkml-project-copier.md`; [Copier workflow](../setup-linkml/references/project-copier.md) |
| Model measured quantities | `linkml: docs/howtos/model-measurements.md`: choose scalar versus nested representations based on fixed/flexible units, uncertainty or ranges, per-measurement metadata, and exchange needs. |
| Choose inheritance, conformance, or metamodel extension | `linkml: docs/howtos/implements-instantiates-guide.md`: `is_a`/`mixins` inherit slots; `implements` declares structural conformance; `instantiates` concerns schema-element metadata. The latter two do not inherit data slots; check actual enforcement in the selected tools. |
| Include ontology terms as data values | `linkml: docs/howtos/ontologies-as-values.md`: distinguish terms represented as identifiers/objects in data from mappings on schema elements. Ontology and LinkML class hierarchies need not mirror each other; verify term-membership or vocabulary validation coverage separately. |
| Language semantics and validation rules | `linkml-model: linkml_model/model/docs/specification/`; read preamble/scope when interpreting normative force |
| Align concepts across schemas | `linkml: docs/schemas/uris-and-mappings.md`: distinguish `class_uri`/`slot_uri`, enum `meaning`, and `*_mappings`; a vocabulary mapping does not itself transform data. |
| Resolve imported or inherited definitions | `linkml: docs/schemas/imports.md`, `docs/schemas/derived-models.md`: inspect effective definitions with runtime `SchemaView.induced_slot()` / `class_induced_slots()` or materialize a derived schema with `gen-linkml -f yaml`, rather than interpreting raw YAML alone. |
| Exact metamodel slot names, ranges, defaults, inheritance | `linkml-model: linkml_model/model/schema/meta.yaml`; follow its imports into sibling YAML modules |
| Multidimensional arrays vs multivalued slots | `linkml: docs/schemas/arrays.md`, `docs/_includes/arrays/`, `docs/howtos/multidimensional-arrays.md`; `linkml-model: linkml_model/model/schema/meta.yaml` (`array`, `array_expression`, dimensions); sibling `array.yaml` is a separate array library |
| Identifier references vs inline objects/lists | `linkml: docs/schemas/inlining.md`; metamodel definitions of `inlined` and `inlined_as_list` |
| Compare generator feature support | `linkml: docs/generators/dashboard.md`: source Markdown tables with a legend, category summaries, and per-test details from upstream compliance tests. |
| JSON Schema generation | `linkml: docs/generators/json-schema.rst`; compare generator limitations with the relevant metamodel definitions |
| Schema/data validation and linting | `linkml: docs/cli/validate.md`, `docs/cli/lint.md`, `docs/data/validating-data.rst` |
| Bootstrap, transform, or render data | `linkml: docs/ecosystem.md`; [focused tool-selection guidance](references/ecosystem.md). Optional tools, not setup dependencies. |

Consult the relevant modeling guide before committing to schema structure; these are design tradeoffs, not recipes every project needs.

When advising schema changes, distinguish metamodel validation (`linkml validate schema.yaml`), quality checks (`linkml lint schema.yaml`), and instance validation (`linkml validate -s schema.yaml --target-class Class data.yaml`). Check the installed CLI/version. The default instance validator uses generated JSON Schema; it is not automatically broader than that target. `--fix` normalizes/coerces data and emits corrected output, so treat it as a transformation rather than a strict check of the original. Test representative valid and invalid examples against the actual consumer; inspect root selection, inlining, unknown properties and null behavior. Successful validation does not establish factual correctness or scientific support.

For generator capability questions, read the dashboard legend and relevant per-test rows before the target generator guide. Distinguish partial/mixed support, not implemented, not applicable, and not yet tested; an aggregate coverage score is not a project suitability score. Treat the dashboard as a versioned report of upstream tests, not proof for an arbitrary schema. Its one link to the compliance test suite targets `main`: resolve follow-up tests at the cached commit when investigating that release. Compliance tests and `scripts/generate_dashboard.py` are outside the documentation-only cache; fetch them selectively if needed.

The specification/metamodel define the language; usage docs explain idioms. Generated API/element pages summarize source and may be stale. Third-party indexes and AI-written commentary are navigation leads, not normative evidence. Check `status`/profile annotations and documented support limits, especially for arrays. A valid metamodel construct does not prove every target generator supports it. This skill performs documentation research; do not report a schema/generator as tested unless it was actually run.

## Attribution and justified fallback

Use immutable links such as `https://github.com/linkml/linkml/blob/<full-commit>/docs/schemas/arrays.md#L34`, with the actual lines checked locally. For metamodel sources use the `linkml/linkml-model` repository and its separate commit. Include the local path when it helps the user inspect the evidence.

When local text cannot answer the question (for example, an `automodule` directive with no rendered options, a missing implementation example, or a suspected post-release fix), explain the gap and fetch only the needed official page or source file. Prefer the same commit's GitHub raw/blob source. For freshness, consult official release notes, issues, or `linkml.io`; record access date and version differences. Current Sphinx `_sources/<page>.md.txt` can provide one page cheaply but is unpinned. Do not repeatedly crawl the whole HTML site or install a service. If the target version cannot be obtained, state that limitation instead of blending versions.

## Related skills—use when

Use a matching locally installed skill first. These external skill sources are **not downloaded or installed by setup-linkml**. Otherwise inspect the linked, pinned raw Markdown and its relevant references; install only when requested or within an authorized setup task, never automatically for a documentation lookup. Pins below were checked on 2026-11-01.

| Skill source | Use when |
|---|---|
| [linkml-term-validator](https://raw.githubusercontent.com/linkml/linkml-term-validator/5c7b51756b30555ef083317849445ec693ac7a8f/skills/linkml-term-validator/SKILL.md) | Configure ontology QC or interpret identifier, label, enum/binding, and coverage findings. |
| [linkml-reference-validator](https://raw.githubusercontent.com/linkml/linkml-reference-validator/8ab0ba1e3f980ce600816ca1b564fadd1d48a16a/skills/linkml-reference-validator/SKILL.md) | Configure reference checks or diagnose title/quotation matching and unchecked evidence. Matching text does not establish scientific claim support. |
| [linkml-store](https://raw.githubusercontent.com/linkml/linkml-store/f19c1d9d3263887b3bb276234f2749de8a5b24a3/skills/linkml-store/SKILL.md) | Work with structured-data storage, import, query, validation, or ranked similarity search. |
| [ontology-access-kit](https://raw.githubusercontent.com/ai4curation/curation-skills/6a35d07bc4a2f0d458b78f109579bd9608d8e44a/ontology-access-kit/SKILL.md) | Perform complex ontology access, relationship traversal, or set queries with OAK; its guidance favors available OLS tooling for basic external ontology searches. |

Documentation availability is not a modeling decision; preserve the project's choice of schema technology.
