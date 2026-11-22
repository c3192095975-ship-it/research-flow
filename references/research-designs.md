# Research Designs

Research design 决定证据类型、材料需求和审查重点。它独立于 route、artifact profile 和 quality tier。

## 1. 选择表

| Design | 适用 | 必有材料 | 主要阶段重点 | 常见排除 |
|---|---|---|---|---|
| `experimental` | 实验、干预、对照研究 | 实验记录、单位、重复、处理/对照 | 分析、统计、图表、可复现性 | 纯理论推断、未提供的原始数据 |
| `quantitative_observational` | 问卷、观察、队列、横断面 | 采样、变量定义、缺失、模型 | 分析、统计、敏感性 | 定性编码、纯案例叙事 |
| `qualitative` | 访谈、民族志、文本/话语分析 | 访谈提纲、编码、伦理、引文定位 | 编码、主题、反例、反思性 | 强行统计推断 |
| `systematic_review` | PRISMA、元分析、系统综述 | 检索式、纳排、偏倚评估、效应量 | 检索、筛选、证据综合、异质性 | 单一案例结论、未系统检索 |
| `theoretical` | 理论、概念、哲学/规范性论文 | 概念定义、前提、反例、论证链 | 论证提纲、反例、边界 | 实证统计（除非有数据） |
| `methods` | 方法、工具、算法、测量论文 | 设计、基线、消融、复现材料 | 方法比较、可复现性、figures | 无比较对象的性能宣称 |
| `case_analysis` | 课程案例、伦理/政策/组织分析 | 案例事实、规则/标准、替代解释 | 论证提纲、规范分析、建议 | 伪造数据、把建议写成已实施结果 |

## 2. 共同底线

无论 design 是什么，都必须：

- 区分事实、解释、规范和推荐；
- 核心 claim 有证据 ID；
- 来源有 locator；
- 不伪造数据、法律、标准、访谈或实验结果；
- 作者确认最终版本。

## 3. 设计选择规则

- 有原始实验/干预：`experimental`。
- 有观测数据但无干预：`quantitative_observational`。
- 有访谈、文本、田野材料：`qualitative`。
- 有系统检索和纳排：`systematic_review`。
- 主要是概念/规范/逻辑：`theoretical` 或 `case_analysis`。
- 主要贡献是方法/工具/算法：`methods`。
- 不确定且材料是课程案例：优先 `case_analysis`。

## 4. 与 quality tier 的关系

- `course_pass`：按课程要求完成最低必要设计检查。
- `course_high`：补齐 design 的结构和证据。
- `research_standard`：加入方法、限制、反例和独立评审。
- `publication_standard`：加入 venue-specific methods/reporting requirements。

## 5. 与 artifact profile 的关系

- `course_report + case_analysis`：伦理/政策案例分析。
- `manuscript + experimental`：实验论文。
- `manuscript + qualitative`：定性研究论文。
- `thesis + systematic_review`：系统综述型学位论文。
- `proposal + methods`：方法研究计划。
