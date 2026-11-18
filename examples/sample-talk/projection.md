# A task queue's long-tail latency — Projection

## Question｜A batch of tasks is slow

**Problem:** Why does a batch take 20 seconds when most tasks take two? A single long-tail task could matter more than average speed.

## Mechanism｜The task queue and barrier

**Setup:** Three workers receive four independent tasks. After processing, a batch-level barrier waits for all four to finish.

**Interpretation:** Speeding up an unrelated short task need not reduce the wait for the slowest task.

## Diagnosis｜Measure before optimizing

Check elapsed time by phase, work distribution, the 95th percentile, and whether a slow task sits on the critical path. The numerical example is illustrative, not a measured benchmark.

## Discussion｜Where would you intervene?

With a shared queue, would you first split the slow task, start it earlier, or change the barrier? What evidence distinguishes those approaches?
