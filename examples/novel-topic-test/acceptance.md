# Novel-topic smoke test | 新主题测试与期望结果

This **small fixture is a reference implementation of constraints**, not an LLM evaluation score. The user's next test can replace B+ trees with any new topic; do not hardcode this example into generated talks.

## Input tiers to test

1. **One-line smoke test**: `用 technical-talk-workflow 给我讲清楚「B+ 树为什么适合范围查询」，先做一个 test，输出 Projection/Notes 和验收项。` The Skill should label default audience (basic software background) and default 30/5-minute timing as assumptions, not silently assume a 60-minute RL-style talk.
2. **Recommended input**: use `request.json`. Audience, intended learning outcome, time and platform should change depth, example and visual plans.
3. **Adversarial repair**: change one value in the Notes to `[15,20,25,30]` and make sure content-anchor audit fails when `anchors.both` includes the exact shared result.

## Expected observable quality (manual rubric)

- [ ] **One object**: same `[15, 35]` range query all the way through.
- [ ] **Progressive reveal**: know what a range query asks before discussing tree pages, then root-to-leaf search, then leaf-link scan, then trade-off.
- [ ] **No irrelevant prerequisites**: do not lecture about all DB storage internals or every tree family.
- [ ] **Predict → step → reveal**: one guess before showing the five matching keys.
- [ ] **Controlled contrast**: full scan vs B+ tree uses the *same eight keys* and query.
- [ ] **Evidence discipline**: no claimed benchmark, query latency, or universal index speedup.
- [ ] **Dual-track**: matching IDs/titles/values; Projection can be delivered without reading the Notes.
- [ ] **Time**: total 30 minutes incl 5 min discussion; one explicit short-form exit.
- [ ] **Platform**: works as plain Markdown/ASCII offline; optional HTML must have static backup.
- [ ] **Novelty**: content is about B+ trees, **not** an accidental copy of RL, CUDA, or Attention chapters.

## Machine checks

```bash
python scripts/validate_request.py examples/novel-topic-test/request.json --strict
python scripts/check_demo_storyboard.py examples/novel-topic-test/demo-storyboard.json
python scripts/check_alignment.py --outline examples/novel-topic-test/outline.json --projection examples/novel-topic-test/projection.md --notes examples/novel-topic-test/speaker_notes.md
python scripts/audit_talk.py --outline examples/novel-topic-test/outline.json --projection examples/novel-topic-test/projection.md --notes examples/novel-topic-test/speaker_notes.md --visuals examples/novel-topic-test/visuals.json --strict-warnings
```

Passing the machine checks is a baseline; the manual rubric determines whether a generated talk is actually teachable.
