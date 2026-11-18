# Technical Talk Workflow · 技术分享工作流

**Agent Skill for narrative-first technical talks, paired projection & speaker notes, and reliable delivery.**

**一套面向技术组会、算法分享和工程培训的可复用 Agent Skill：让投屏稿能独立支撑讲解，让口播稿讲得自然，而且两者始终严格对应。**

[中文](#中文说明) · [English](#english)

---

## 中文说明

### 为什么做这个项目？

技术资料齐全，并不意味着一场分享讲得顺。准备技术分享时，经常会遇到：知识点罗列但缺少因果链、公式只写结论、案例频繁更换、投屏稿压缩得过头、口播稿和展示稿错位，以及演示文档导出后图表损坏等问题。

`technical-talk-workflow` 把这些问题转化成一个可执行的制作与验收流程！

### 只给一个主题也能跑：输入设计

**最小输入**：只需主题，例如“用这个 Skill 测试讲清楚 B+ 树为什么适合范围查询”。此时采用**明示的假设**：软件/ML 工程听众、总共 30 分钟（含 5 分钟讨论），默认先生成 3–4 小节小样与验收表。不要沿用上次 RL 组会的 60 分钟。

**推荐输入**：主题 + 听众已知/未知知识 + 总时长（含讨论）+ 听完后的可检验能力 + 投屏平台。来源、深度、演示资源、离线要求和保密等级为可选增强项。自然语言即可；不强制填 JSON。

| 输入 | 建议 | 缺省时如何处理 |
| --- | --- | --- |
| `topic` | **必需** | 无法判断主题时再问 |
| `audience` | 强烈推荐 | 假设懂基本软件/ML，不熟主题，标为 ASSUMED |
| `duration_minutes` | 强烈推荐 | 默认总计 30 分钟，5 分钟讨论；标为 ASSUMED |
| `learning_outcome` | 推荐 | 默认能解释一个机制、追踪一个例子、指出一个取舍 |
| `delivery_platform` | 推荐 | Markdown 投屏稿 + Speaker Notes，附静态备选 |
| `sources/depth/demo/privacy` | 按需 | 不杜撰实测，保密优先 |

完整契约见 [Input Contract](references/input-contract.md)；机器可读的 [Request Schema](assets/talk-request.schema.json) 与 [Minimal](assets/talk-request-minimal.json) / [Recommended](assets/talk-request-recommended.json) 示例均已提供。


### 这套方法有什么特点？

1. **沿同一个对象解释完整流程**：先选一个核心问题，再固定一条请求、一个轨迹、一张张量或一次实验作为叙事主线。
2. **旧知识 → 新问题 → 新机制 → 边界**：让每个知识点因为上一节留下的问题而自然出现。
3. **固定案例 + 逐层映射**：小例子解释直觉，数值示例解释机制，工程案例解释整个系统；同一例子的规则和符号不乱改。
4. **双轨同步**：`projection.md` 保留足够的公式、例子和过渡，讲者现场可以直接对着讲；`speaker_notes.md` 提供口语展开、互动和追问，但不会重排讲述顺序。
5. **有限时间内做深度选择**：核心推导单独安排时间，准备正常版、晚 5 分钟和晚 10 分钟的收束路径。
6. **可校验而非只凭感觉**：脚本检查章节和时间、指定的内容锚点、演示图及静态备份；人工检查数学、图示渲染、页面可读性与事实来源。

### 工作流程

```text
资料与受众 → 主问题与贯穿对象 → 固定案例/叙事链 → 单一 outline.json
                                             ↓
                           projection.md ↔ speaker_notes.md
                                             ↓
                        追问准备 + 图示清单 + 实际彩排
                                             ↓
                         自动校验 + 最终媒介导出验收
                                             ↓
                               分享 → 复盘 → 改模板
```

### 项目目录

```text
technical-talk-workflow/
├── SKILL.md                        # Agent Skill 指令
├── README.md                       # 本文件 / bilingual
├── CHANGELOG.md
├── PUBLISH_GITHUB.md
├── LICENSE
├── assets/                         # 听众简报、大纲、双稿与演示清单模板
├── references/                     # 叙事、证据、时间、内容对齐、技术与媒介规范
├── scripts/                        # 双稿校验、内容/演示审核、隐私扫描及测试
├── examples/
│   ├── anonymized-rl-retrospective.md
│   ├── sample-talk/               # 通用的“长尾任务调度”示例
│   └── novel-topic-test/          # 用 B+ 树题目做跨领域冒烟测试
└── .github/workflows/validate.yml
```

### 安装与使用

将**整个目录**放入支持 Agent Skills 的客户端的 Skill 搜索路径。常用位置例如：

- Codex（项目级）：`.agents/skills/technical-talk-workflow/`
- Claude Code（项目级）：`.claude/skills/technical-talk-workflow/`

不同客户端是否自动加载、需要什么命令，请以对应官方文档为准。

**示例提示词：**

> 用 `technical-talk-workflow` 帮我准备一场 45 分钟的“FSDP 与分布式训练”技术分享。听众理解 PyTorch 和反向传播，但不熟悉分布式训练。请先用一个具体训练任务建立贯穿主线，确定唯一重点推导，再生成标题一致、**不带章节编号**的 `projection.md` 和 `speaker_notes.md`。投屏版不能仅有提纲；讲者稿需要口语过渡、互动和常见追问。最后验证时间、重要公式锚点和图示静态备份，提供缩时方案。

**默认简洁交付**：除非用户要求详细开发过程，最终优先展示 `projection.md` 与 `speaker_notes.md` 两份文件；内部大纲 ID 用于校验，不出现在标题中。

**新主题一键测试（推荐）**：参照 [验收清单](examples/novel-topic-test/acceptance.md) 直接输入一个陌生技术主题；先看是否正确采用听众和时长默认值，再看同一例子、逐步推导、静态备用及双稿对齐，最后才扩展成长篇。

**本地校验：**（Python 3.9+，无需第三方依赖）

```bash
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/validate_request.py assets/talk-request-minimal.json
python scripts/validate_request.py assets/talk-request-recommended.json --strict
python scripts/check_demo_storyboard.py assets/demo-storyboard-template.json --allow-template
python scripts/check_alignment.py \
  --outline examples/sample-talk/outline.json \
  --projection examples/sample-talk/projection.md \
  --notes examples/sample-talk/speaker_notes.md
python scripts/audit_talk.py \
  --outline examples/sample-talk/outline.json \
  --projection examples/sample-talk/projection.md \
  --notes examples/sample-talk/speaker_notes.md \
  --visuals examples/sample-talk/visuals.json --strict-warnings
python scripts/check_alignment.py --outline examples/novel-topic-test/outline.json --projection examples/novel-topic-test/projection.md --notes examples/novel-topic-test/speaker_notes.md
python scripts/privacy_scan.py .
```

**注意：**自动检查不能证明公式正确、实际口播好听或 PDF 渲染完美。必须在真实展示设备上打开最终产物，检查图文、公式、字号、分页与备用演示。

### 安全、适用范围和版本

- Skill 只包含通用方法与匿名示例；**不包含企业内部会议资料、未授权技术图、账号密钥或实际训练日志**。
- 优先在私有 GitHub 仓库测试，公开前进行人工的版权、隐私和内部信息审查。
- `v0.3.1`：取消展示稿标题编号，改为内部 ID + 自然标题对齐，保留旧稿兼容。
- `v0.3.0`：新增分层输入契约、输出跟踪、渐进式示例与同条件策略对照、交互 Storyboard 及新主题测试。已具备结构化自动测试；**尚不保证每个主题的实际演讲效果**。
- [Agent Skills 标准](https://agentskills.io/specification) · [发布指引](PUBLISH_GITHUB.md) · [版本记录](CHANGELOG.md)

---

## English

### Why this project?

A complete technical outline is not automatically a coherent talk. Speakers may know the definitions yet struggle to explain why one idea follows another. The projected document may become too terse to present from, while the full speaker script drifts into a different order. Long derivations, broken diagrams, and untested export formats only surface at the last minute.

**Technical Talk Workflow** is a portable [Agent Skill](https://agentskills.io/specification) that turns technical source material into a **narrative, teachable, source-aware and delivery-checked** presentation. It is subject-agnostic: use it for algorithms, infrastructure, papers, demos, or engineering retrospectives.

### Inputs: one topic is enough, context improves quality

**Minimal:** the `topic` alone is enough for a provisional **test** (3–4 sections with acceptance criteria). Unless supplied, assume basic software/ML audience and **30 minutes total including 5 minutes of discussion**, and label those as assumptions. Do not silently reuse the duration of a prior talk.

**Recommended:** topic, what the audience already knows and does not know, duration + discussion budget, measurable learning outcome, and delivery platform. Sources, depth, demo/availability, offline access and privacy level are optional. Natural-language input works; JSON is not required. See [Input Contract](references/input-contract.md), [Schema](assets/talk-request.schema.json), and [Test Fixture](examples/novel-topic-test/acceptance.md).

### Design principles

1. **Track one object end to end.** Follow a request, trajectory, tensor, experiment, or user action to keep the entire talk causally connected.
2. **Bridge familiar concepts to new mechanisms.** Introduce each new idea to solve a concrete problem, then explain its assumptions and failure cases.
3. **Reuse stable examples.** Start with a tiny worked example, add a small bridging example if needed, and migrate to an end-to-end engineering case. Keep numerical assumptions consistent.
4. **Keep two documents synchronized.** The projection contains enough technical substance to speak from; the more conversational notes provide explanations, questions, transitions and interruption recovery. Both share one internal outline and identical natural section headings; IDs remain hidden in the outline, never shown in the handouts.
5. **Budget depth, not just slide count.** Reserve time for the primary derivation, demos, Q&A, and fallback endings when running five or ten minutes late.
6. **Validate delivery.** Check section IDs, deliberately chosen technical anchors, media manifests, static fallbacks, privacy risks, and the actual rendered artifact.

### Workflow

```text
Source audit & audience brief
    → driving question, tracked object, example map
    → outline.json (single source of truth)
    → projection.md + speaker_notes.md (paired sections)
    → Q&A preparation + visuals manifest + timed rehearsal
    → structural/content checks + final display review
    → live discussion + evidence-aware retrospective
```

### Installation

Copy the entire `technical-talk-workflow/` directory into a Skill directory supported by your agent. Example repository-scoped locations:

```text
.agents/skills/technical-talk-workflow/   # Codex
.claude/skills/technical-talk-workflow/   # Claude Code
```

Activation and reloading vary by client; consult that client's documentation.

### Example request

> Use `technical-talk-workflow` to prepare a 45-minute technical talk on distributed training for engineers who already understand PyTorch. Start with one driving question and a stable example, identify a single deep derivation, and generate an aligned projection and speaker-notes pair. The projection must remain independently presentable. Include Q&A, shortened timing paths, a media manifest, and final alignment checks.

### Validate the sample

Run the four Python commands in the Chinese section above. No third-party Python packages are required. The scripts check explicit structure and stated anchors; they **cannot prove mathematical correctness, visual quality, teaching success or public-release authorization**.

### Privacy and release policy

This repository contains generic workflow instructions and fictitious examples only. Do not commit employer transcripts, nonpublic architecture, sensitive credentials, employee details, proprietary benchmark numbers, or unlicensed illustrations. Prefer a private repository until source permissions and output quality are reviewed.

**Version:** 0.3.1 · MIT License · [Changelog](CHANGELOG.md) · [Publishing guide](PUBLISH_GITHUB.md)
