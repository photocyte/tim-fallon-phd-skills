### III. Dataflow Programming Model

Nextflow's core abstraction MUST adhere to following principles and guidelines:

- The dataflow programming model is the fundamental abstraction in the Nextflow programming model.
- Workflows are defined as dataflow graphs where data flows between processes.
- Processes MUST be stateless, side-effect-free transformations that communicate via channels.
- Workflows should be defined in a platform agnostic manner to enable portability across clusters and clouds.
- The DSL MUST prioritize expressiveness for concurrent and parallel pipeline definition.
- Changes to the language parser (ANTLR grammars in `nf-lang`) MUST preserve backward compatibility with existing pipelines unless explicitly versioned (DSL1 vs DSL2).
- Concurrency primitives (GPars actors/dataflow) MUST be used correctly to maintain the dataflow semantics.

**Rationale**: The dataflow model is Nextflow's fundamental abstraction, enabling automatic parallelization and distribution. Preserving this model ensures existing scientific pipelines continue to work and users can reason about workflow behavior.
