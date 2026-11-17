---
name: technical-talk-workflow
description: 为技术组会、算法与系统培训、论文或工程分享建立问题驱动的叙事，输出同源且逐节对齐的投屏稿、口播稿、图示计划和技术追问底稿，并做时间、内容、导出、保密与交付验收。Use for preparing, revising, rehearsing, aligning, or reviewing audience-facing technical talks, especially when a dense technical outline needs a coherent live explanation; not for ordinary summaries.
license: MIT
compatibility: Python 3.9+ for optional standard-library validators; otherwise Markdown and JSON only.
metadata:
  version: "0.3.0"
  languages: "zh-CN,en"
---

# Technical Talk Workflow | 问题驱动、双轨对齐的技术分享制作

目标：帮助已掌握部分知识、但未必是领域专家的讲者，将资料转成**讲得顺、讲得准、投得清、可讨论、能复盘**的技术分享。重点不是自动生成漂亮幻灯片，而是让每一节自然回答上一节留下的问题。借鉴公开 [LazyAttention Walkthrough](https://lazyagi.github.io/LazyAttention/tutorials/attention-kernel-walkthrough/) 的可迁移讲法：**固定一个输出对象 → 最小计算例子 → 渐增复杂度 → 对比不同实现 → 回到真实异常与证据**。只迁移教学方法，不复制原教程的具体实现和内部材料。

## 触发与工作模式

- **从零准备**：从课程、笔记、项目或论文材料建立可讲的技术故事。
- **修订现稿**：保留经核实的知识内容，优先解决逻辑断点、信息密度、时间与演示问题；不要无故重写。
- **双稿对齐**：投屏稿和 Speaker Notes 内容/编号/时间已经漂移时，重新建立唯一章节清单，按它修复双稿。
- **现场准备或复盘**：生成问答、临场压缩路径、导出检查，或根据实际问答记录复盘。
- 纯粹概念解释、普通摘要、单篇文字润色不必套用完整工作流。

## 输入约定（一个新知识点也能启动）

- **最小输入：** 一个明确的 `topic` 或明确点名的待讲来源。只给主题时仍要能生成**带假设标签**的简报、例子和对齐双稿；默认听众具有基本软件/ML 工程背景，默认 **30 分钟（其中 5 分钟讨论）**。禁止沿用上次 RL 分享的 60 分钟。
- **推荐输入：** `topic`、听众 `knows/new_to`、`duration_minutes`、可验证的 `learning_outcome`、`delivery_platform`。素材、深度、演示资源、保密要求是可选增强项。
- **交付模式：** `test` 先跑 3–4 节小样与验收表；`outline` 只规划；`full` 完整生产；`repair` 优先修现有双稿。用户说“测试这个 Skill”时，优先 `test`，不要默认生成 60 分钟全文。
- 执行前先看 [输入契约](references/input-contract.md) 与 [示例请求](assets/talk-request-minimal.json)；用户不需要自己写 JSON。缺少但影响结果的条件要清楚标为 **ASSUMED**，公开正式分享前再确认。

## 核心原则（所有模式必须遵守）

1. **一条中心问题 + 一个追踪对象**：例如沿一个请求、一条数据、一张输出张量、一次模型推理从头走到尾。讲的是对象经历的问题和机制，不是术语列表；每章都有“前面尚未解决的一个问题”。
2. **从已知到未知**：先唤醒听众已有的框架，再用最小反例提出新需求；优先解释相同点、决定性差异和类比失效处。不要开场灌输完整学科知识树；只补齐下一步真正需要的先修知识。
3. **固定例子、逐步加复杂度**：常用组合是直觉可手算的 A、解释某个特殊机制的微型 B、工程端到端的 C。先让输出能被独立算出，再**一次只引入一个新困难**（如归约、并发、状态、异常形状），维护固定假设；禁止悄悄改变数字、单位、符号。
4. **少数重要推导、其余概念讲清机制**：选 1–2 个真正必要的深推导；明确前提、每步为什么成立、结果如何回到案例。证明与实现细节可放附录，不要挤掉后段工程和讨论。
5. **一张总图贯穿 + 可预测的交互**：开场显示全流程，跟踪一个输出/任务，逐步高亮其依赖和状态；每个重要演示按**预测→改变一个条件→逐步观察→解释机制→指出局限**执行。结束重画或用 Bad Case 回到总图。参阅 [机制漫游规范](references/mechanism-walkthrough.md)。
6. **双轨共用一个 outline**：`outline.json` 是唯一章节/例子/时间契约。投屏稿与讲者稿共享 `[Pxx]` 编号、标题、顺序、核心结论、公式和数字；两稿的*表达密度*可以不同。
7. **投屏稿自身可讲**：每节至少有问题、可信例子、必要公式或机制、辨析、收束/下一问。不能降为“一个标题 + 三个名词”，也不能整段都是照念稿。
8. **讲者稿用于训练表达，不是现场拐杖**：提供说人话的解释、动作和图的指向、互动预期与**预期回答/揭晓时机**、常见追问、前后转场、极短压缩版；现场主要依靠投屏稿。
9. **事实和证据有边界**：定义/定理、假设示例、未经验证推断、真实实测必须分开。既有作者笔记不是自动正确，公开讲义截图不是现场反馈记录。
10. **演示与交付都是产品质量**：对照实验须固定同一输入与评价口径，动画明确**逻辑顺序≠真实运行轨迹**；检查最终的 PDF/飞书/Slides 页面、分页、公式、交互/备份及链接，不以“Markdown 生成成功”视为交付完成。
11. **讲述时间是真约束**：计入公式口头推导、点击演示、等待听众回答、切屏、意外提问；标记核心/可压缩/可跳过段落以及安全收尾点。
12. **公开安全默认严格**：企业会议原文、内部架构、未授权图、员工信息、账号/密钥和私链只能用于获授权的私有准备，不直接塞进公开 Skill、README 或示例。

## 默认产物

- `request.json`（可选，用户可用自然语言输入）：用 [输入 Schema](assets/talk-request.schema.json) 明确哪些是用户提供、哪些按默认假设；依 [输入契约](references/input-contract.md) 运行。
- `brief.md`：受众、目标、时间、媒介、输入来源、公开边界；见 [brief 模板](assets/brief-template.md)。
- `outline.json`：稳定节点 ID、时长、核心问题、结论、三个层级例子、图示 ID、表达优先级、短版出口；见 [模板](assets/outline-template.json)。
- `projection.md`：适合显示和直接跟讲的公开版本；见 [模板](assets/projection-template.md)。
- `speaker_notes.md`：与投屏逐节对齐的口语讲法与临场卡；见 [模板](assets/speaker-notes-template.md)。
- 需要时：`visuals.json`、`demo_storyboard.json`（[模板](assets/demo-storyboard-template.json)）、`claim-ledger.csv`、`run_of_show.md`、`qa_cards.md`、`demo/`、最终导出的投屏 PDF。

## 工作流（必须按顺序完成门槛，不应先写大段全文）

### G0｜读材料、解析输入并界定证据等级

先提取 `topic/audience/duration/learning_outcome/platform`；如仅有主题，以 [输入默认](references/input-contract.md) 填入 ASSUMED 值。执行 `python scripts/validate_request.py request.json`（使用 JSON 时）。明确模式 `outline/test/full/repair`，测试模式优先产出小样与预期验收标准。

核对用户的原始材料：听众要求、既有资料和讲者笔记、实际展示稿、演讲时长与平台限制。分开记录：已证实的内容 / 讲者原本计划 / 真正演示过的文件 / 讲者回忆的效果 / 尚无证据的听众反馈。输出简报和公开范围约束。不要把小批注未经核实当成正式演讲结构。参阅 [来源与证据方法](references/source-to-talk.md)。

### G1｜先设计“能讲出来”的问题链

写出主问题、追踪对象（优先选**一个具体输出**）、主例 A→桥接 B→工程 C 的固定映射；按**输出依赖 → 最小计算 → 新的约束/协作 → 第二种设计 → 真实场景/验证**的梯度逐步暴露复杂度。对比方案时，固定输入和度量、只改变一个主要条件。每节用“已解决 → 新困境 → 为什么必须引入本节 → 得到的结论 → 新疑问”串联。详见 [机制漫游](references/mechanism-walkthrough.md)。先口头用 3–5 分钟试讲全局链路，若只能说“接下来讲 XX”，先修逻辑。参阅 [叙事设计](references/narrative-design.md)。

### G2｜建立讲述契约与时间风险模型

填 `outline.json`（ID/title/minutes/core_question/takeaway/visual_id/example_id/tier/transition/exit_line 等）。总时长包括示例运算、互动、演示和转场；为深推导单独估时。规划 A 核心、B 可压缩、C 可跳过；记录**按时讲 / 落后 5 分钟 / 落后 10 分钟**时要怎么讲及在哪里安全结束。见 [时间与中断](references/timing-and-recovery.md)。

### G3｜先做中密度投屏稿，再做详细讲者稿

按 outline 同步生成两稿：投屏稿的公式、表格、例子和图示足够支撑不看 Notes 的现场解释；讲者稿口语化，包含预测问题、手指/鼠标指向、解释图中对象、正确/错误理解、追问与回到主线。两稿相同节点不能互相矛盾。修改公式或案例时更新两稿与清单；详见 [逐节契约](references/content-contract.md)。

### G4｜建立视觉与演示清单

先选真正需要**逐步操作**的 1–2 个概念；每个写 [Demo Storyboard](assets/demo-storyboard-template.json)：`question/input_state/change_one_thing/predict/steps/reveal/mechanism/boundary/fallback/evidence_level`。可先用静态逐帧图，不必为了教学强行造 HTML。演示代码要正确，按钮必须改变对应状态。

每张图声明 `visual_id / why / cue / location / fallback / ownership / render_check`。结构图用于导航、Grid/时间线用于状态变化、数值例子用于公式、端到端图用于系统边界；禁止为“有视觉”添加无解释价值的配图。交互设计采用“预测→点击→读结果→指出局限”，必须有静态回退。见 [图与平台](references/visual-and-platform.md)。

### G5｜技术备答、事实审查与口头彩排

对核心点准备 L1 定义 / L2 最小例子 / L3 公式或代码机制 / L4 边界与工程后果；核对数学符号、条件、单位和示例计算。像“真实系统性能更快”一类需要证据的说法，不能由类比证明。彩排每个节点的实际耗时并回填；深推导与现场追问需计入。见 [技术 QA](references/technical-qa.md)、[时间与中断](references/timing-and-recovery.md)。

### G6｜多层校验，冻结版本

**输入检查（可运行；无 JSON 时由自然语言提取并记录在 brief 中）：**

```bash
python scripts/validate_request.py request.json
```

**结构检查（可运行）：**

```bash
python scripts/check_alignment.py --outline outline.json --projection projection.md --notes speaker_notes.md
python scripts/audit_talk.py --outline outline.json --projection projection.md --notes speaker_notes.md --visuals visuals.json
```

第二条在缺少 `visuals.json` 时省略该参数，仍能执行。对正式 Demo Storyboard 另运行 `python scripts/check_demo_storyboard.py demo_storyboard.json`，并人工执行至少一次预测与逐步揭晓。脚本检查结构、关键文本锚点、演示资源和可疑时间；无法自动证明数学正确、实际讲述流畅、图渲染好看。

**人工验收（必须）：**逐项抽查公式/示意数值/不同粒度的类比；两稿实际句子与转场；导出后表格和图是否跨页、字是否够大；互动的静态备份；短版结尾是否可用。见 [交付 QA](references/qa-and-delivery.md)。冻结同一版本号的所有产物。

### G7｜发布、复盘、迭代

按用户指定媒介交付，提供真实可打开的链接；失败后优先改交付渠道而非反复打 ZIP。分享结束后用真实记录与自我感受分别归档：实际覆盖范围、超时与问答节点、错误纠正、听众可复述的结论、遗留核验事项。下一次优先升级模板/检查器，不要把具体 RL、CUDA 等课程内容写死在通用 Skill 里。

## 本 Skill 的质量门槛

1. **Teachability**：只看投屏稿能独立说出“为何出现→机制→例子→边界→下一问”。
2. **Alignment**：两稿 `[Pxx]`、重要锚点、数值、例子、图示和章节时间一致。
3. **Truthfulness**：定义有条件，示意有标签，真实结论有来源，开放问题有归宿。
4. **Runtime**：每个深推导有独立时间，正常版/缩时版都有稳定结尾。
5. **Display**：实测最终投屏媒介；不把源码块误当 Mermaid/HTML 运行视图。
6. **Publish safety**：公开版本不含未授权的内部资料、个人信息或截图。
7. **Input adaptability**：只输入新主题能以标注假设的小样运行；给定听众、时长、目标后，例子复杂度和时间分配应发生可解释的变化。
8. **Mechanism visibility**：关键演示能说清输入、只改变的条件、预测、逐帧结果、因果机制、适用边界和静态备份；比较策略必须固定输入，性能结论必须有真实测量。

只需要修订现稿时，优先运行 G0→G2→G5→G6；不要从 G1 重写全部结构，除非确实发现讲述主线断裂。

**下一次回归测试**：先看 [新主题冒烟样例](examples/novel-topic-test/acceptance.md)，用完全不同于 RL/Attention 的技术主题验收是否复用了讲述方法，而不是复述原课程。
