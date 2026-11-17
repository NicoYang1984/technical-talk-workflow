# Mechanism Walkthrough | 跟着一个输出，把抽象机制讲透

## Public inspiration and boundaries

The public [LazyAttention interactive walkthrough](https://lazyagi.github.io/LazyAttention/tutorials/attention-kernel-walkthrough/) uses a concrete output tile `O` as the recurring object: “先看依赖，再看分组，最后看 GPU 怎样执行”. Its source is the public [LazyAGI/LazyAttention](https://github.com/LazyAGI/LazyAttention/tree/main/docs/tutorials/attention-kernel-walkthrough) repository. The page is **inspiration for pedagogical method**, not a source of general-purpose GPU speed claims, hidden internal details, or material that this Skill may copy verbatim.

The site's lessons include a useful shape: CUDA prerequisites (Arange → reduction → BN), basic Forward → input grouping → alternative implementations, Backward and its actual implementation, workload/mask atlas, then optimization and evidence. Interactive frames explicitly warn when a simulation is logical rather than a GPU trace. Transfer these **structural moves**, not its particular algorithm or exact page count.

## Seven moves

1. **Choose one object/result that must be produced.** E.g. one request, one output row, one cache entry, one tensor tile, one trajectory. Let the audience follow it through every layer.
2. **Start from the output's dependency graph.** Ask: “To obtain this result, what must we already know or compute?” Introduce only missing prerequisites, not the whole subject catalog.
3. **Build a complexity ladder.** First a no-cooperation toy (like elementwise work), then an example requiring combination or state (like reduction), then one realistic nonuniform/bad case. Reuse the same input whenever possible; increase exactly one source of complexity at a time.
4. **Offer a prediction before a formula or click.** The audience should predict which value changes, what step becomes more expensive, or which path fails; the next frame reveals the result and why. Do not require a quiz every 30 seconds.
5. **Compare two strategies under a controlled common input.** Keep input size, assumptions and evaluation criterion fixed. Explain how each partitions work, where coordination happens, and what costs appear. Don't declare a winner without evidence.
6. **Reveal scale or real-world irregularity.** Explain why a tidy toy case hides pathological shapes, data distributions, long tails or state problems. If real workload evidence is unavailable, label all quantities as *illustrative* and leave performance claims open.
7. **Close the loop with evidence and a design trade-off.** State: problem → hypothesis → changed mechanism → controlled comparison → observed result → remaining uncertainty. For conceptual talks without measurement, substitute a verifiable small computation/trace and explicitly state that runtime performance remains untested.

**One question per transition:** “We can compute X; what breaks when Y changes?” This is stronger than a section title such as “Next: Algorithm B.”

## The demo contract (the key addition in v0.3)

Each important visualization or interaction must answer a single causal question. Record:

| Field | Required content |
| --- | --- |
| `question` | One falsifiable or checkable audience question |
| `input_state` | Fully specified starting data and invariants |
| `change_one_thing` | The only control or condition varied |
| `predict` | What to ask the audience before revealing results |
| `steps` | Ordered steps, each tied to a highlighted object/state |
| `reveal` | The observable outcome, with actual computation or source |
| `mechanism` | Why the outcome follows from the formula or implementation |
| `boundary` | Toy assumptions, omitted concurrency or runtime differences |
| `fallback` | Screenshot/static frames if HTML / Mermaid cannot run |
| `evidence_level` | `illustrative`, `derived`, `source-backed`, or `measured` |

Use [assets/demo-storyboard-template.json](../assets/demo-storyboard-template.json). When the user does not request working HTML, a static storyboard is sufficient. Never create unrelated flashy simulations as decoration.

## Display behaviors that teach

- **Focus + context**: keep the whole flow visible, highlight the currently active state and hide unrelated details instead of redrawing unrelated diagrams.
- **Step / reset / compare**: controls must actually change the illustration; include a reset and preserve context where possible.
- **Same input, different strategy**: when comparing two alternatives, use matching axes, units, color semantics and timing convention.
- **Progressive reveal**: every step carries “what changed → why” text; a visual highlight alone is not a proof.
- **Static fallback**: all essential steps must be understandable as stills. Never make essential comprehension depend on embedded HTML support.
- **Avoid false authority**: animation time is not measured execution time; toy scheduler/CTA visualization is not a GPU cycle trace; an output diagram is not a benchmark.

## Platform-neutral proof of teaching

An audience member should be able to explain the mechanism by tracing a representative input **without the speaker** and answer three questions:

1. What exactly changed in the example?
2. What mathematical or implementation rule caused the change?
3. Which conclusion is supported, and which stronger conclusion would require new evidence?

If only the high-level diagram is memorable but the audience cannot answer those questions, the demo did not teach enough.

## Adapting to other topics

- Algorithms: trace one input and output; compare a naïve and optimized method with the same data.
- Systems: trace one request/record through states; progressively add contention, recovery or failure conditions.
- Papers: trace one motivating example through baseline limitation → proposed mechanism → measured evidence.
- Non-empirical theory: use a small mathematical counterexample and correct derivation rather than fabricate engineering benchmarks.

Do not force CUDA, GPU blocks, or a second strategy on a subject where that comparison is irrelevant.
