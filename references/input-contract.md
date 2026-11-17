# Input Contract | 技术分享到底需要哪些输入？

This workflow supports both **one-line topic tests** and **fully specified talks**. Do not force the user to fill a long form just to start. The purpose of input capture is to prevent silent audience and timing assumptions, not to block progress.

## Priority levels

| Priority | Field | Why it changes the result | If missing |
| --- | --- | --- | --- |
| Required | `topic` (or a clearly named source to explain) | Defines what is being taught | Ask only if no identifiable topic exists |
| Strongly recommended | `audience.knows`, `audience.new_to` | Determines prerequisite depth and analogy choice | Assume software/ML engineering familiarity; flag as **ASSUMED** |
| Strongly recommended | `duration_minutes`, `discussion_minutes` | Controls proof depth, amount of content and interactivity | Default **30 min total, 5 min discussion**, flag as ASSUMED |
| Recommended | `learning_outcome` | Decides what the audience should be able to explain or do | Default: explain mechanism, run through one example, identify one trade-off |
| Recommended | `sources` / user attachments | Determines factual constraints and what must not be invented | Use source-independent conceptual examples; do not fabricate implementation measurements |
| Recommended | `delivery_platform` | Determines Mermaid, HTML, media, export and backup approach | Default Markdown projection + Speaker Notes, static PNG/SVG alternatives |
| Optional | `depth`, `focus`, `excluded_topics` | Specifies what to derive, de-emphasize or omit | Auto-select 1 main derivation/mechanism; put deep tangents in appendix |
| Optional | `demo_available`, `offline_required` | Determines whether interaction is real, mocked, or static | Assume no external runtime, use static or self-contained toy example |
| Optional | `sensitivity`, `source_rights` | Sets distribution limits | Assume private drafts if sensitivity is unknown; never publish proprietary sources |
| Optional | `tone`, `language`, `prior_talk` | Tunes voice and continuity | Natural explanatory Chinese for Chinese requests |

**Important distinction:** a user can test the Skill by supplying only `topic`; this is sufficient to generate a provisional brief, an example map, and draft paired notes using explicit defaults. For a high-stakes public or company talk, audience and duration should be confirmed before calling the output presentation-ready. Never inherit the duration from an unrelated prior talk.

## Modes and behaviors

- `mode=outline`: brief, prerequisite map, driving question, worked-example plan, chapter timing; no full prose required.
- `mode=full` (default when user asks to prepare a complete talk): projection and aligned notes, source ledger, demo storyboard, QA and delivery plan.
- `mode=test`: use one new subject, produce a small sample (3–4 sections) and a **pass/fail rubric** before attempting a full hour.
- `mode=repair`: preserve existing sections/technical claims; repair transitions and pairing instead of rewriting the entire artifact.

Never quietly convert `test` into a full-length production handout, and never interpret an optional missing field as evidence that a user has a particular background.

## How to ask

When critical information is missing but meaningful output is still possible, proceed with labeled assumptions. If the user explicitly wants the final real-world talk and details are essential, ask only the highest-impact missing detail conversationally (usually intended audience or duration), not a long questionnaire.

## JSON request

`assets/talk-request.schema.json` is a cross-client specification. `scripts/validate_request.py` performs dependency-free checks and reports the inferred defaults. For informal chat prompts, extract equivalent fields into the brief; users should not need to write JSON.

```json
{
  "topic": "B+ tree indexes and range queries",
  "audience": {"knows": ["binary search", "Python arrays"], "new_to": ["database page indexes"]},
  "duration_minutes": 30,
  "discussion_minutes": 5,
  "learning_outcome": "Explain why leaf-level links help range scans and what the index costs to maintain",
  "delivery_platform": "Feishu Docs",
  "mode": "test",
  "sources": []
}
```

## User-facing fast prompt

**Minimal:** “用 `technical-talk-workflow` 讲清楚 **[主题]**，先按默认听众和时长做一个测试，输出双稿和验收标准。”

**Recommended:** “主题 **[主题]**；听众懂 **[已有知识]**，不懂 **[新知识]**；总时长 **[分钟]**，含讨论 **[分钟]**；希望他们最后能 **[具体能力]**；平台 **[飞书/PPT/网页]**。请准备逐步演示和严格对齐的 Projection/Notes。”
