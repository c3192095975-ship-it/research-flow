---
name: research-flow
description: Orchestrate scientific research work and prevent conflicting skill activation. Use for real research projects involving scoping, literature search or management, paper reading, study design, experiment records, data analysis, statistics, scientific figures, manuscript/thesis/review/proposal writing, peer review, revision response, submission, or research presentation. Triage first; select artifact profile, quality tier, and research design; build claim traceability and an argument outline before drafting; run recorded backtracking and executable checks; support overrides and dependency preflight. Fall back to a portable baseline when no research skill is available. Do not use for general scholarly Q&A, ordinary coding, routine business data work, or non-research writing.
metadata:
  version: "3.5.0"
  short-description: Discover skills, resolve capabilities, and route research phases
---

# Research Flow v3.5

本 skill 是跨用户可移植的科研总编排器。它先发现当前用户安装了哪些 skill，再把科研流程的“能力槽”映射到实际可用的 skill。它不要求用户安装固定的 Nature、PaperSpine 或任何特定 skill。

本文件中的 skill 名称都是**首选候选**，不是硬依赖。实际执行前必须根据当前用户的能力清单解析。

## 1. 强制规则

1. 实际科研任务必须先进入 ResearchFlow，再选择领域 skill。
2. 启动时先发现或继承当前用户已安装的 skill 清单；不能假定固定 skill 一定存在。
3. 同一阶段只能有一个主技能。
4. 同一轮最多加载 3 个 skill，且不能有两个 skill 负责同一职责。
5. 先锁路线，不在中途切换写作、图表、引文或评审体系。
6. 通过工件交接，不重复检索、阅读、写作或审稿。
7. 通过阶段质量门后才能进入下一阶段。
8. 不编造引用、数据、方法、统计、实验、作者、伦理审批或结果。
9. 用户当前明确要求优先于项目旧状态；发生改变时写入 decision log。
10. 人类作者负责科学判断、作者身份和最终提交。
11. 适配是运行时能力映射，不自动重写本 skill 或其他 skill 的源文件。
12. 发现结果模糊时允许用户 override；仍无可用候选时使用 baseline，不假装拥有某个能力。
13. 声明了 MCP、API、浏览器或环境变量依赖的 skill 必须标记可用性，不能把“已安装”当成“已就绪”。
14. 进入流程后必须先做任务分级：`BYPASS`、`LIGHT` 或 `FULL`，简单任务不建立完整项目状态。
15. 涉及核心引文、统计结论、伦理、隐私、投稿包或不可逆操作的任务，即使很短也不能因为“看起来简单”而跳过必要证据门。
16. `FULL` 只表示需要完整阶段链，不表示所有可用 skill 都必须上场。
17. FULL 模式在开始写作前必须先通过 pre-write gate：锁定 artifact profile、quality tier、能力图、证据账本、required sections/rubric、claim boundary 和写作 owner。
18. 质量门应按 artifact profile 适用；课程报告、论文、开题和展示不能共用同一套硬性检查。
19. 本地 AI 风格检查不等于 Turnitin AI 率；本地重复预检不等于 Turnitin 查重；格式渲染成功不等于学术合规。
20. artifact profile 决定“产物是什么”，quality tier 决定“要达到什么标准”；两者不能混为一谈。
21. quality tier 改变证据深度、评审强度、质量门和必要能力，不自动等于加载更多 skill。
22. `auto` 只表示推断模式，最终必须解析为 `course_pass`、`course_high`、`research_standard` 或 `publication_standard`。
23. `course_report + publication_standard` 只有在用户明确需要发表级组件时才允许；真正的投稿交付必须切换为 `manuscript` 或相称的 thesis/proposal profile。
24. 每个核心 claim 必须有 `claim_id`，并映射到 section/paragraph/figure/table；证据变化时只重审受影响的 claim 和相关段落。
25. `course_high`、`research_standard` 和 `publication_standard` 在正式写作前必须建立 argument outline。
26. 每个 FULL 项目必须选择 `research_design`：experimental、quantitative_observational、qualitative、systematic_review、theoretical、methods 或 case_analysis。
27. 阶段回退必须有记录：from/to、原因、失效工件、需重跑检查和批准人；不能假装流程永远只能向前。
28. 能确定性检查的项目先运行脚本，再交给作者判断科学意义；脚本通过不等于科学结论正确。
29. `phase_name` 必须覆盖真实阶段，包括 reading 和 argument_outline，不能因模板漏项导致跨会话状态丢失。

以下任务不进入 ResearchFlow：一般概念问答、术语解释、翻译、普通编程、普通业务数据分析、非科研写作和与具体科研项目无关的闲聊。

## 2. 启动协议

按以下顺序执行：

1. **DETECT**：判断是否为真实科研任务。
2. **TRIAGE**：判断应采用 `BYPASS`、`LIGHT` 还是 `FULL`。
3. **DISCOVER**：仅 FULL 模式读取完整 skill 清单；LIGHT 只确认一个相关能力。
4. **NORMALIZE**：合并、去重、读取名称、描述、脚本、引用标题和调用策略。
5. **PREFLIGHT**：检查非标准格式、依赖声明、环境变量和可用性状态。
6. **OVERRIDE**：读取用户/项目 override；用户明确指定的能力映射优先。
7. **CLASSIFY**：识别探索、检索、精读、分析、写作、评审、回复或展示。
8. **ROUTE**：锁定一个路线。
9. **PROFILE**：选择 artifact profile，例如 `manuscript`、`course_report`、`proposal`、`thesis` 或 `presentation`。
10. **QUALITY TIER**：选择质量等级：`course_pass`、`course_high`、`research_standard` 或 `publication_standard`；`auto` 必须解析为具体等级。
11. **RESEARCH DESIGN**：选择 experimental、quantitative_observational、qualitative、systematic_review、theoretical、methods 或 case_analysis。
12. **PHASE**：锁定一个入口阶段，并检查前置工件。
13. **PRE-WRITE GATE**：FULL 模式写作前检查能力图、证据账本、claim traceability、argument outline、rubric/acceptance criteria、claim boundary、写作 owner、quality tier 和 research design。
14. **RESOLVE**：把阶段能力槽解析为一个主技能和一个可选辅助技能，并按 quality tier 决定证据/评审强度。
15. **EXECUTE**：只执行当前阶段，不提前加载后续阶段。
16. **GATE**：用可观察工件或检查结果判断是否通过；可执行检查优先。
17. **BACKTRACK**：必要时记录回退原因、失效工件和需重跑检查，不把流程当成只能前进的直线。
18. **HANDOFF**：输出状态、能力图、工件、未解决问题和下一阶段。

开始时输出：

`ResearchFlow：模式=…；路线=…；profile=…；quality_tier=…；design=…；阶段=…；主技能=…；辅助技能=…；能力源=…；可用性=…`

### 任务分级

#### BYPASS

以下任务不建立完整科研流程：

- 纯概念、定义、公式解释或学习方法；
- 只改一段文字、普通润色或翻译；
- 只做普通格式化；
- 只做一张简单图，且不承载研究结论；
- 只做一次普通数据分析；
- 用户明确要求只要一个简短结果，且不涉及证据、统计、伦理或投稿。

BYPASS 行为：

- 不扫描全部 skill；
- 不建立完整能力图；
- 直接使用一个基础能力或直接回答；
- 不输出完整 ResearchFlow 状态。

#### LIGHT

以下任务只使用轻量流程：

- 只检索一组文献；
- 只精读一篇论文；
- 只核对一组参考文献；
- 只检查一段统计描述；
- 只修改一个论文章节；
- 只做一张有明确数据来源的科研图；
- 只回复一条审稿意见。

LIGHT 行为：

- 只确认一个主能力；
- 必要时加一个不同职责的辅助能力；
- 不建立完整多阶段项目状态；
- 只执行与当前任务直接相关的质量检查。

#### FULL

以下任务使用完整流程：

- 从选题到论文；
- 系统综述或多篇文献综合；
- 数据分析、统计、图表和写作组合；
- 投稿、返修、审稿回复或多轮评审；
- 需要 claim-evidence、来源定位、数据可追溯或投稿包；
- 同时涉及两个以上阶段；
- 涉及核心引文、统计结论、伦理、隐私、数据权限或最终提交。

FULL 行为：

- 完整发现、合并、去重和建立能力图；
- 锁定路线和入口阶段；
- 执行阶段依赖、质量门和工件交接。

#### 风险覆盖

短任务不等于低风险。以下情况即使文字很少，也不能 BYPASS：

- 核心研究主张或引文；
- 统计显著性和因果结论；
- 伦理、隐私、数据权限或作者贡献；
- 投稿、返修、审稿回复或最终交付包。

如果无法判断，优先选择 LIGHT；如果涉及上述高风险项，选择 FULL。

### 能力发现

FULL 模式优先使用宿主已经提供的 skill 清单，并在需要补足本地 skill、override 或依赖信息时运行发现脚本。LIGHT 模式只确认当前任务需要的单个能力，不建立完整能力图。BYPASS 不运行发现。

需要完整发现时，从本 skill 目录运行：

```bash
python3 scripts/discover_skills.py
```

需要扫描额外目录或读取 override 时：

```bash
python3 scripts/discover_skills.py \
  --root "/path/to/skills" \
  --overrides "/path/to/research-flow-overrides.yaml" \
  --include-plugins
```

发现脚本只读取元数据，不执行其他 skill。它会识别：

- 标准 `SKILL.md`；
- `manifest.yaml` fallback；
- `agents/openai.yaml` metadata fallback；
- 目录名、脚本文件名、参考文档标题和 README 摘要；
- MCP/API/环境变量依赖声明；
- 环境变量是否存在（只记录名称，不读取值）；
- 用户级和项目级 override。

若脚本不可用，使用宿主 skill 清单并标记 `catalog_source=host_list`，不得声称已扫描文件系统。

### 歧义处理

- 目标期刊不明确：默认 `general`，不要自动假定 Nature。
- 中文科研写作：默认 `chinese_thesis`；英文论文默认 `general`。
- 阶段不明确：选择完成当前请求所需的最早未满足阶段。
- 路线改变会影响多个阶段时，明确说明并只重启受影响阶段。
- 没有合适候选：先读取 override；仍无候选时使用 baseline 或能力模型中的降级方案，并标记 `degraded`。
- skill 声明了 MCP/API/浏览器/环境变量依赖时，标记 `unverified` 或 `unavailable`，不要假设已就绪。
- 仍无法判断且会显著改变结果时，只问一个最关键的问题。

## 3. 能力槽

科研流程按能力槽解析，不按固定名称解析：

| 能力槽 | 用途 | 默认候选（可用时） |
|---|---|---|
| `scope` | 选题、假设、研究设计 | `scientific-brainstorming`、`nature-proposal-writer` |
| `search` | 文献检索、引文发现 | `nature-academic-search`、`literature-review`、`citation-management` |
| `acquisition` | 全文获取 | `nature-downloader` |
| `reading` | 精读、论文卡 | `nature-reader`、`nature-paper-card` |
| `evidence` | 引文核验、claim-to-source | `nature-ref-verifier`、`nature-citation` |
| `analysis` | 科研计算和数据处理 | `scientific-toolkit-skill` 及其子能力 |
| `statistics` | 统计审查 | `nature-statistics`、`statistical-analysis` |
| `figures` | 数据图、机制图、投稿图 | `scipilot-figure-skill`、`scientific-visualization`、`nature-figure`、`academic-figure-skill` |
| `writing` | 论文、综述、开题、章节写作 | `scientific-writing`、`research-writing-skill`、`nature-writing` |
| `production` | LaTeX/Word、投稿包 | `paper-spine`、`documents`、构建工具 |
| `review` | 自审、同行评审 | `nature-reviewer`、`peer-review`、ARS reviewer |
| `response` | 审稿回复、返修跟踪 | `nature-response` |
| `delivery` | 文档、PPT、表格 | `documents`、`presentations`、`pptx`、`spreadsheets`、`office-academic-skill` |
| `orchestration` | 多阶段总流程 | `paper-spine`、`academic-research-suite`，同一项目二选一 |
| `memory` | 长期偏好和项目背景 | `personal-profile` |
| `style_audit` | AI 文风、自然度和语言风格审计 | `avoid-ai-writing`、`shuorenhua`、`humanizer-zh-academic` |
| `similarity_precheck` | 已知来源的本地重复风险预检 | 本地 n-gram/quote audit；不是 Turnitin |

每个能力槽还要记录 `availability`：

- `ready`：未发现依赖问题；
- `likely`：依赖看起来存在，但未执行真实调用；
- `unverified`：声明了 MCP/API/浏览器依赖，发现阶段没有验证；
- `unavailable`：必要的环境变量、命令或文件缺失。

全部角色、选择规则、override 和降级方案见 `references/capability-model.md`。

## 4. 路线锁

路线表示写作、图表、引文和评审体系；实验、基金和展示是叠加模式。

| 路线 | 适用 | 写作偏好 | 图表偏好 | 引文偏好 | 评审偏好 |
|---|---|---|---|---|---|
| `general` | 通用英文论文、报告、课程科研 | `scientific-writing` | `scipilot-figure-skill` | `nature-academic-search` + `nature-ref-verifier` | `peer-review` |
| `chinese_thesis` | 中文论文、毕业论文、课程研究 | `research-writing-skill` | `scipilot-figure-skill` | `nature-ref-verifier` | `nature-reviewer` |
| `nature` | 明确目标为 Nature/CNS 系列 | `nature-writing` | `nature-figure` | `nature-citation` + `nature-ref-verifier` | `nature-reviewer` |
| `systematic_review` | 正式系统综述、元分析、ARS 协议 | `academic-research-suite` 流程 | `scipilot-figure-skill` 或领域专用 | `academic-research-suite` 流程 | `peer-review` 或 ARS reviewer |
| `competition` | 数学建模等竞赛科研 | `cumcm-live-workflow` | `scientific-toolkit-skill` | 竞赛流程 | 竞赛审阅流程 |

模式修饰：`lab` 加 `nature-experiment-log`；`proposal` 加 `nature-proposal-writer`；`recurring_literature` 在 `daily-paper-zotero` 和 `nature-literature-pipeline` 中二选一；`presentation` 在展示适配器中三选一。

路线规则：

- 路线表里的名称是偏好，不是依赖；不存在时从同一能力槽降级。
- `paper-spine` 只作为阶段 9 的 production 能力，不作为整个研究生命周期的总入口。
- `academic-research-suite` 与 `paper-spine` 不能同时担任同一项目的 orchestration owner。
- 一个能力槽不能同时有两个 selected owner。
- `personal-profile` 只提供 memory，不控制科研阶段。

## 4.1 Artifact profiles

路线回答“语言和学术风格是什么”，profile 回答“最终产物是什么”。两者必须同时锁定。

| Profile | 适用 | 默认主路径 | 明确排除 |
|---|---|---|---|
| `manuscript` | 完整科研论文、期刊投稿 | 标准 0-12 阶段；按需加入统计、图表、投稿包 | 不适用于短作业 |
| `course_report` | 课程报告、案例分析、伦理报告、实验报告 | `scientific-writing` + `nature-ref-verifier` + `peer-review` + `documents` | 不用 `paper-spine` 和 `nature-reviewer` 强行拉满 |
| `proposal` | 开题、基金、研究计划 | `scientific-brainstorming` + `nature-proposal-writer` + 证据核验 | 不自动生成虚构预实验 |
| `thesis` | 学位论文、毕业设计 | 中文/英文写作 owner + 章节证据门 + 格式生产 | 不把课程作业标准当论文标准 |
| `presentation` | 组会、答辩、科研汇报 | 写作/图表产物 + 展示适配器 | 不改写研究结论以适配版式 |

`course_report` 默认流程图：

```text
research-flow
-> skill-triage
-> scientific-brainstorming
-> nature-ref-verifier
-> scientific-writing
-> nature-polishing
-> style_audit（适用时）
-> similarity_precheck（适用时）
-> peer-review
-> documents
-> format/accessibility/integrity gate
```

FULL 模式并不要求所有阶段都执行；只执行 artifact profile 真正需要的阶段。详细 profile 规则见 `references/artifact-profiles.md`。

## 4.2 Quality tiers

Quality tier 决定“做到什么程度”，而不是“换一个产物”。

| Tier | 目标 | 典型变化 |
|---|---|---|
| `course_pass` | 满足课程/作业最低要求 | rubric 覆盖、基本证据与格式、人工确认 |
| `course_high` | 课程高分标准 | brainstorm、更强证据、独立评审、语言与格式检查 |
| `research_standard` | 接近科研论文标准 | claim-evidence 深度、方法/限制、独立 red-team review、统计/图表按需强化 |
| `publication_standard` | 期刊/会议投稿标准 | venue 规则、完整统计/图表、投稿包、严格引用与合规 |
| `custom` | 用户自定义 | 明确列出额外标准和检查 |

### 自动推断

- `course_report`：默认 `course_high`；用户明确只求通过时用 `course_pass`。
- `manuscript`：默认 `research_standard`；有明确 venue/投稿目标时用 `publication_standard`。
- `proposal` / `thesis`：默认 `research_standard`。
- `presentation`：课程展示默认 `course_high`，科研答辩/组会可用 `research_standard`。
- 用户说“按科研标准”“按投稿标准”“只要过作业要求”时，必须明确解析为具体 tier。

### 标准冲突

- `course_report + research_standard` 合法：保持课程产物，但提高证据、论证、评审和 claim 检查。
- `course_report + publication_standard` 只适用于用户明确要求发表级组件的情况；真正投稿必须切换为 `manuscript` 或相称 profile。
- `presentation + publication_standard` 通常不合法，除非目标是正式会议论文而不是展示。
- quality tier 不是“越多 skill 越好”。它改变质量门和审查深度，不自动增加无关 skill。

详细规则见 `references/quality-tiers.md`。

## 4.3 Research designs

Research design 决定证据和审查重点，避免所有项目都走“数据分析→统计→图表”。

| Design | 适用 | 重点材料 | 审查重点 |
|---|---|---|---|
| `experimental` | 实验、干预、对照 | 实验记录、单位、重复、随机/盲法 | 混杂、误差、可复现、统计单位 |
| `quantitative_observational` | 问卷、观测、横断面/队列 | 采样、变量、缺失、模型 | 选择偏差、混杂、模型假设 |
| `qualitative` | 访谈、民族志、文本分析 | 访谈提纲、编码、反思性、引文 | 可信度、编码、研究者位置、伦理 |
| `systematic_review` | PRISMA/元分析 | 检索式、纳排、偏倚评估、效应量 | 覆盖度、可复现、异质性 |
| `theoretical` | 理论、概念、哲学论证 | 概念定义、前提、反例、逻辑链 | 概念清晰、反例、论证有效性 |
| `methods` | 方法/工具/算法论文 | 设计、基线、消融、复现材料 | 新颖性、比较公平、可复现 |
| `case_analysis` | 课程案例、伦理/政策分析 | 案例事实、规则/标准、替代解释 | 事实与规范分离、适用边界、建议可执行 |

不能确定时，优先选择 `case_analysis` 或 `theoretical`；如果用户提供实验数据，选择 `experimental`；如果用户提供访谈材料，选择 `qualitative`。

## 4.4 Claim traceability

核心 claim 必须形成连续链：

```text
claim_id
-> section_id
-> paragraph_id
-> figure/table id
-> evidence_ids
-> allowed wording
```

建议 `claim-evidence.csv` 字段：

```csv
claim_id,section_id,paragraph_id,figure_id,claim_text,evidence_ids,support_strength,allowed_wording,status,notes
```

正文中的 claim marker 使用：

```text
{{C001}}
```

规则：

- 每个核心段落或图表至少绑定一个 claim；
- claim marker 缺失时不能通过 Gate B；
- 证据变化时，通过 claim_id 定位受影响的段落/图表并只重审这些位置；
- 摘要、结果、讨论中的同一 claim 必须使用同一 ID 或明确映射。

详细规则见 `references/argument-and-traceability.md`。

## 5. 阶段顺序

```text
0 立项 -> 1 定向 -> 2 检索 -> 3 精读 -> 4 证据 -> 5 分析
-> 6 统计 -> 7 图表 -> 7.5 论证提纲 -> 8 写作 -> 9 生产
-> 10 评审 -> 11 回复 -> 12 交付
```

强制依赖：

- 写作前必须有证据账本；course_high/research_standard/publication_standard 还需要 argument outline；实证论文还需要结果和统计审查。
- 图表前必须有数据、分析结果和科学问题。
- 生产前必须有稿件、图表、引用和统计审查。
- 评审前必须有冻结到可审查版本的产物。
- 回复前必须有审稿意见和修改稿。
- 最终交付前必须有作者确认和一致性检查。

允许的快捷入口：

- 单篇论文精读：2 -> 3 -> 4。
- 只做数据分析：5，必要时 6。
- 已有数据只做图：5 -> 6（如需要）-> 7。
- 已有证据只写论文：4 -> 8。
- 已有完整稿件：9。
- 只做自审或审别人稿：10。
- 只回复审稿：11。
- 只做科研汇报：12。

中途进入前必须检查前置工件；缺失时先执行最小前置检查，不补造结果。

详细阶段合同见 `references/activation-order.md`。

## 6. 阶段能力和首选候选

| 阶段 | 能力槽 | 首选候选 | 质量门 |
|---|---|---|---|
| 0 立项 | `orchestration` | `research-flow` 自身 | 问题、目标、约束和路线明确 |
| 1 定向 | `scope` | `scientific-brainstorming` | 核心假设可检验，成功/失败标准明确 |
| 2 检索 | `search` + `acquisition` | `nature-academic-search`；需要时 `nature-downloader` | 检索可复现，覆盖反对证据 |
| 3 精读 | `reading` | `nature-reader` 或 `nature-paper-card` | 全文可读，页码/章节定位可复核 |
| 4 证据 | `evidence` | `nature-ref-verifier`；Nature 路线加 `nature-citation` | 每条核心主张有证据或明确缺口 |
| 5 分析 | `analysis` | `scientific-toolkit-skill`；实验型加 `nature-experiment-log` | 结果可复现，独立单位和样本量明确 |
| 6 统计 | `statistics` | `nature-statistics` | 设计、分析单位、检验和主张一致 |
| 7 图表 | `figures` | `scipilot-figure-skill`；Nature 路线用 `nature-figure` | 每个 panel 有科学问题，图和 source data 一致 |
| 7.5 论证提纲 | `writing` 的 argument mode 或 `scope` | 每节问题、核心 claim、支持/反对证据、限制、章节关系 | 论证顺序清楚，claim 有证据 ID，反例和边界已列出 |
| 8 写作 | `writing` | 路线对应的写作候选 | 每条事实主张有证据或 `AUTHOR_INPUT_NEEDED` |
| 9 生产 | `production` | `paper-spine` 或通用文档构建工具 | 构建、编号、图注、引用和投稿包通过 |
| 10 评审 | `review` | 自审用 `nature-reviewer`；审别人用 `peer-review` | 无未解决 P0，重大问题有证据定位 |
| 11 回复 | `response` | `nature-response` 或通用回复流程 | 每条意见和修改可追溯，包一致 |
| 12 交付 | `delivery` | `documents` / `presentations` / `pptx` / `office-academic-skill` 三选一 | 作者批准、声明和最终审计完成 |

## 7. 冲突裁决

按能力槽裁决，不按品牌裁决：

- `search` 只能有一个主入口；`acquisition` 可以在其后作为辅助。
- `reading` 只能有一个主入口；另一个 reader 不能同时生成第二份默认阅读产物。
- `analysis` 和 `statistics` 可以是计算与审查的关系，但不能由写作 skill 生成结果。
- `figures` 只能有一个视觉设计 owner；导出/色板/元数据工具可以作为辅助。
- `writing` 只能有一个主写 owner；润色和 claim calibration 只能作为后续辅助。
- `production` 只能有一个构建 owner；`paper-spine` 不再重新做检索或分析。
- `review` 只能有一个正式评审 owner；自审与正式同行评审不能在同一轮伪装成两个独立审稿人。
- `delivery` 只能有一个主要展示/文档 owner；底层格式工具只能辅助。

具体禁止组合：

- `paper-spine` + `academic-research-suite` 同时担任 orchestration。
- `scientific-writing` + `research-writing-skill` 同时主写。
- `scientific-writing` + `nature-writing` 同时主写。
- `scipilot-figure-skill` + `nature-figure` 同时设计同一组图。
- `nature-reviewer` + `peer-review` 同一轮冒充两个独立审稿人。
- `daily-paper-zotero` + `nature-literature-pipeline` 同时订阅。

## 8. 同轮组合

允许：

- `research-flow` + `search` owner + `acquisition` owner
- `research-flow` + `analysis` owner + `statistics` reviewer
- `research-flow` + `figures` owner + 导出/色板/元数据工具
- `research-flow` + `writing` owner + `stss` 或语言润色
- `research-flow` + `production` owner + 构建/引用审计

禁止：

- 两个主写 owner
- 两个主图 owner
- 两个正式 review owner
- 两个 orchestration owner
- 两个长期文献订阅流程

## 8.1 Recorded backtracking

科研不是只能向前。出现以下情况时必须允许并记录回退：

- 写作时发现证据缺口：8/7.5 -> 2/4；
- 评审后发现分析错误：10 -> 5；
- 统计审查失败：6 -> 5；
- 图表和正文冲突：7/9 -> 5/7；
- 最终声明不一致：12 -> 9/10；
- 证据被替换：4/7.5/8 中受影响的部分重审。

回退记录：

```yaml
from_phase:
to_phase:
reason:
invalidated_artifacts: []
checks_to_rerun: []
approved_by:
timestamp:
```

回退不是失败，而是科研流程的正常控制流。禁止无记录地悄悄回退或重复整套流程。

## 9. 能力图与交接

文件型项目读取 `references/handoff-schemas.md`。每阶段至少交接：

- 路线、入口阶段、当前阶段；
- 能力图：每个能力槽的 selected、alternatives、availability、confidence；
- 主技能和辅助技能；
- 工件路径；
- 质量门状态；
- 已锁定决定；
- 未解决问题；
- 下一阶段和下一主技能。

能力图示例：

```yaml
route: chinese_thesis
modifiers: [lab]
phase: figures
skills:
  analysis:
    selected: scientific-toolkit-skill
    availability: available
    confidence: high
  figures:
    selected: scipilot-figure-skill
    alternatives: [scientific-visualization]
    availability: available
    confidence: high
unresolved_roles: []
degraded_roles: []
```

## 10. 质量门与返修

三个硬门：

1. **方向锁**：问题、目标、路线、资源和成功标准。
2. **证据/结果锁**：来源、数据、统计、图表和 claim boundary。
3. **提交锁**：作者、贡献、伦理、披露、引用和最终交付包。

自动检查优先于人工确认：

- 检索记录和去重结果；
- 来源可打开、定位可复核；
- claim-evidence 完整性和 claim marker 可定位；
- manifest/claim/evidence/占位符等确定性检查；
- 数据/代码/环境可复现；
- 图表 source data 和视觉 QA；
- 文档构建和投稿包一致性。

返修规则：

1. 用具体工件或检查失败定位问题。
2. 做最小修复。
3. 用同一个门复验。
4. 默认最多两轮。
5. 第三轮必须有新证据、范围变化、用户明确要求或新发现的高风险问题。
6. 不能靠切换到另一个 skill 绕过失败门；先修复当前阶段或回退。

## 11. 停止、降级与适配失败

出现以下情况时暂停：核心问题不可检验、关键引文无法核验、数据不支持结论、分析单位或样本量不清、图表缺 source data、伦理/隐私/权限未解决、投稿包不一致、作者未确认。

主能力不可用时：

- 报告缺失能力；
- 在同能力槽中寻找替代；
- 没有替代时使用标准降级流程；
- 标记 `degraded`，不假装已调用；
- 详细能力降级表见 `references/capability-model.md`。

发现脚本无法运行时，使用宿主 skill 清单；不能声称扫描了本地文件。

### 用户 override

如果自动推断不准确，可以读取：

- `./.research-flow/overrides.yaml`
- `./.research-flow-overrides.yaml`
- `~/.codex/research-flow-overrides.yaml`
- `~/.config/research-flow/overrides.yaml`
- `RESEARCH_FLOW_OVERRIDES` 指定的路径
- `--overrides` 指定的路径

示例：

```yaml
roles:
  search: my-literature-tool
  figures: my-plot-tool
  writing: my-thesis-writer
```

override 只决定能力槽，不修改任何 skill 源文件。override 指定的 skill 不存在时标记 `unavailable`，不静默换成其他同名品牌。

### 无 skill baseline

当没有任何可用科研 skill、发现来源为空，或所有候选都不可用时，读取 `references/baseline-protocol.md`。baseline 使用内置研究 brief、检索日志、证据账本、分析清单、图表计划、写作和评审清单，并明确标注 `catalog_source=baseline` 和 `degraded_roles`。

## 12. 并行、记忆与外部 Agent

适合并行：检索与已有数据分析、数据锁后的图表生产与评审准备、稿件冻结后的独立评审与补充材料整理。

不适合并行：两个写作 skill 修改同一稿件、两个 figure skill 设计同一组图、多个 agent 修改同一文件、作者写作与“独立”评审共享同一论证上下文。

`personal-profile` 只用于长期偏好和项目背景；缺失时按当前请求推断，不阻断科研流程。

外部 agent 只承担边界清晰的独立任务，结果由主线程复核。未发表或敏感材料未经授权不得发送。方向是否继续、暂停或转向时，按全局 `AGENTS.md` 的多智能体对抗评审规则执行。

## 12.1 Artifact quality gates

FULL 和适用的 LIGHT 任务使用以下门；按 profile 和 quality tier 标记 `required`、`optional` 或 `not_applicable`：

- **Gate A：任务与 rubric 覆盖**：required sections、评分项、格式和受众全部覆盖。
- **Gate B：证据与引用**：来源身份、使用方式、定位和 claim-evidence 可核验。
- **Gate C：语言与 claim strength**：主张强度不超过证据，术语和语气一致。
- **Gate D：原创性与风格预检**：AI 风格审计、已知来源重复风险、引用和题目重合；明确不是 Turnitin。
- **Gate E：生产与格式**：构建、页面尺寸、字号、页眉页脚、占位符、图和 source data、可访问性。
- **Gate F：独立完成与人工确认**：作者阅读、核对学生/作者信息、确认独立完成和最终提交。

不是所有 profile 都要求 Gate D 或统计/图表检查。课程报告需要的是 rubric coverage、证据、语言、格式和人工确认；完整论文才通常需要更强的引用、统计和投稿包审计。详细规则见 `references/quality-gates.md`。

## 13. 输出契约

阶段开始：

```text
ResearchFlow：模式=BYPASS | LIGHT | FULL；路线=…；profile=…；quality_tier=…；阶段=…；主技能=…；辅助技能=…；能力源=…；可用性=…
```

首次建立能力图时，可补充：

```text
ResearchFlow capability map：已发现 X 个 skill；当前解析 Y 个能力槽；缺失/降级 Z 项。
```

阶段结束：

```text
ResearchFlow gate：pass / fail / pending
工件：…
未解决：…
下一阶段：…
下一主技能：…
```

复杂或跨轮任务使用完整 handoff，不复制整段对话。

## 14. 快速路径

- 单篇论文摘要/精读：2 -> 3 -> 4。
- 文献综述：2 -> 3 -> 4 -> 8。
- 只做数据分析和图：5 -> 6（如需）-> 7。
- 单段改写：8 + claim calibration 或语言润色。
- 只回复审稿：11。
- 只做汇报：12。
- 只要概念解释：不进入 ResearchFlow。

## 15. 参考文件

- `references/capability-model.md`：能力槽、路线偏好、候选排序、冲突和降级矩阵。
- `references/adaptation-protocol.md`：发现、合并、规范化、override、依赖预检、能力图、安全和失败处理。
- `references/activation-order.md`：任务分级、路线决策树、阶段入口、阶段合同、场景和测试清单。
- `references/artifact-profiles.md`：课程报告、论文、开题、学位论文和展示的产物 profile。
- `references/quality-tiers.md`：质量等级、自动推断、标准冲突和门槛升级规则。
- `references/quality-gates.md`：A-F 质量门、适用性、失败处理和本地检查边界。
- `references/handoff-schemas.md`：项目状态、激活记录、能力图、可用性、证据账本、数据分析清单、图表计划、审稿和回复模板。
- `references/baseline-protocol.md`：没有任何科研 skill 时的最低可运行流程。
- `scripts/discover_skills.py`：只读扫描已安装 skill 并输出能力清单。
- `scripts/check_quality.py`：检查 claim ID、evidence ID、占位符和基础一致性。

只有当前任务需要时再读取参考文件，不要预加载全部参考资料。
