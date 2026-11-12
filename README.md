# Technical Talk Workflow · 技术分享工作流

**Agent Skill for narrative-first technical talks, paired projection & speaker notes, and reliable delivery.**

**一套面向技术组会、算法分享和工程培训的可复用 Agent Skill：让投屏稿能独立支撑讲解，让口播稿讲得自然，而且两者始终严格对应。**

[中文](#中文说明) · [English](#english)

---

## 中文说明

### 为什么做这个项目？

技术资料齐全，并不意味着一场分享讲得顺。准备技术分享时，经常会遇到：知识点罗列但缺少因果链、公式只写结论、案例频繁更换、投屏稿压缩得过头、口播稿和展示稿错位，以及演示文档导出后图表损坏等问题。

`technical-talk-workflow` 把这些问题转化成一个可执行的制作与验收流程。它不是一套固定的 PPT 皮肤，也不是某一门学科专用教程。

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
│   └── sample-talk/               # 通用的“长尾任务调度”示例，含可跑的校验输入
└── .github/workflows/validate.yml
```

### 安装与使用

将**整个目录**放入支持 Agent Skills 的客户端的 Skill 搜索路径。常用位置例如：

- Codex（项目级）：`.agents/skills/technical-talk-workflow/`
- Claude Code（项目级）：`.claude/skills/technical-talk-workflow/`

不同客户端是否自动加载、需要什么命令，请以对应官方文档为准。

**示例提示词：**

> 用 `technical-talk-workflow` 帮我准备一场 45 分钟的“FSDP 与分布式训练”技术分享。听众理解 PyTorch 和反向传播，但不熟悉分布式训练。请先用一个具体训练任务建立贯穿主线，确定唯一重点推导，再生成共同编号的 `projection.md` 和 `speaker_notes.md`。投屏版不能仅有提纲；讲者稿需要口语过渡、互动和常见追问。最后验证时间、重要公式锚点和图示静态备份，提供缩时方案。

**本地校验：**（Python 3.9+，无需第三方依赖）

```bash
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/check_alignment.py \
  --outline examples/sample-talk/outline.json \
  --projection examples/sample-talk/projection.md \
  --notes examples/sample-talk/speaker_notes.md
python scripts/audit_talk.py \
  --outline examples/sample-talk/outline.json \
  --projection examples/sample-talk/projection.md \
  --notes examples/sample-talk/speaker_notes.md \
  --visuals examples/sample-talk/visuals.json --strict-warnings
python scripts/privacy_scan.py .
```

**注意：**自动检查不能证明公式正确、实际口播好听或 PDF 渲染完美。必须在真实展示设备上打开最终产物，检查图文、公式、字号、分页与备用演示。

### 安全、适用范围和版本

- Skill 只包含通用方法与匿名示例；**不包含企业内部会议资料、未授权技术图、账号密钥或实际训练日志**。
- 优先在私有 GitHub 仓库测试，公开前进行人工的版权、隐私和内部信息审查。
- `v0.2.0`：对齐校验、时间风险、演示备份、最终导出检查与双语说明。已具备结构化自动测试；**尚不保证每个主题的实际演讲效果**。
- [Agent Skills 标准](https://agentskills.io/specification) · [发布指引](PUBLISH_GITHUB.md) · [版本记录](CHANGELOG.md)

---

## English

### Why this project?

A complete technical outline is not automatically a coherent talk. Speakers may know the definitions yet struggle to explain why one idea follows another. The projected document may become too terse to present from, while the full speaker script drifts into a different order. Long derivations, broken diagrams, and untested export formats only surface at the last minute.

**Technical Talk Workflow** is a portable [Agent Skill](https://agentskills.io/specification) that turns technical source material into a **narrative, teachable, source-aware and delivery-checked** presentation. It is subject-agnostic: use it for algorithms, infrastructure, papers, demos, or engineering retrospectives.

### Design principles

1. **Track one object end to end.** Follow a request, trajectory, tensor, experiment, or user action to keep the entire talk causally connected.
2. **Bridge familiar concepts to new mechanisms.** Introduce each new idea to solve a concrete problem, then explain its assumptions and failure cases.
3. **Reuse stable examples.** Start with a tiny worked example, add a small bridging example if needed, and migrate to an end-to-end engineering case. Keep numerical assumptions consistent.
4. **Keep two documents synchronized.** The projection contains enough technical substance to speak from; the more conversational notes provide explanations, questions, transitions and interruption recovery. Both share one outline and section IDs.
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

**Version:** 0.2.0 · MIT License · [Changelog](CHANGELOG.md) · [Publishing guide](PUBLISH_GITHUB.md)
