# Quality Tiers

`artifact_profile` 决定产物是什么，`quality_tier` 决定要以什么标准完成它。两者必须同时记录。

## 1. 等级

### `course_pass`

目标：满足课程/作业的最低明确要求。

重点：

- rubric 覆盖；
- 基本证据和引用；
- 结构完整；
- 格式和提交要求；
- Gate A/B/C/E/F。

不自动要求：

- 系统综述；
- 统计或图表；
- 完整投稿包；
- 多轮 red-team review。

### `course_high`

目标：课程中的高质量作业或以高分为目标。

增加：

- 结构化 brainstorming；
- argument outline；
- claim/evidence 映射；
- 更强的来源核验；
- 独立 peer review；
- 语言和 claim strength 检查；
- Gate A-F（Gate D 按课程规则）。

仍不自动要求完整投稿包或 Nature 审稿。

### `research_standard`

目标：在适用的科研深度、证据和可复核性上完成产物。

增加：

- argument outline；
- claim-evidence matrix；
- 来源定位和引用核验；
- 方法、限制、竞争解释；
- 独立 red-team review；
- 统计、图表和可复现性检查（适用时）；
- 任何质量评估都要说明适用范围，不能把课程评分冒充科研质量。

允许的典型组合：

```text
profile=course_report
quality_tier=research_standard
```

这表示产物仍是课程报告，但证据、论证、评审和 claim 检查按科研标准执行。

### `publication_standard`

目标：满足具体期刊/会议/投稿目标。

额外要求：

- 目标 venue 的当前规则；
- 完整统计、图表和 source data；
- 引用、作者、伦理、数据/代码可用性；
- 投稿包一致性；
- 可能需要 `paper-spine`、`nature-writing`、`nature-figure`、`nature-response` 等。

限制：

- 真正的投稿交付通常要求 `profile=manuscript`，而不是 `course_report`。
- `course_report + publication_standard` 只能在用户明确要求发表级组件时使用，不能把课程报告伪装成期刊投稿。

### `custom`

用户明确列出标准和检查项。必须记录来源和优先级，不得用模型臆造一个“更高标准”。

## 2. 自动推断

| Profile | 默认 tier | 允许升级 |
|---|---|---|
| `course_report` | `course_high` | `course_pass`、`research_standard`；`publication_standard` 需说明限制 |
| `manuscript` | `research_standard` | `publication_standard`（明确 venue 时） |
| `proposal` | `research_standard` | `custom` 或按资助方标准 |
| `thesis` | `research_standard` | `publication_standard` 仅用于单篇论文组件 |
| `presentation` | `course_high` | `research_standard` |

用户明确说“只要过”“按科研标准”“按投稿标准”时，优先遵从并解析为具体 tier。不能静默忽略。

## 3. 等级对能力选择的影响

### Evidence

- `course_pass`：基本来源真实、引用匹配。
- `course_high`：增加来源定位和多源核对。
- `research_standard`：增加 claim-level evidence matrix、反对证据和限制。
- `publication_standard`：增加 venue-specific citation 和完整引文审计。

### Review

- `course_pass`：结构/格式检查。
- `course_high`：独立 `peer-review`。
- `research_standard`：更强的 red-team review、方法和 claim 边界。
- `publication_standard`：正式审稿/期刊要求检查（按 profile）。

### Style and similarity

- `course_pass`：基本语言校对；D 仅在规则要求时。
- `course_high`：语言、claim 和适合时的 AI 风格检查。
- `research_standard`：需要明确原创性和引用边界；本地预检结果必须说明不是 Turnitin。
- `publication_standard`：按 venue 规范执行；不把本地检查当作官方检测。

### Production

- `course_pass`：满足作业格式。
- `course_high`：格式 + 视觉 QA + A11y（适用时）。
- `research_standard`：完整文档/图表/数据一致性。
- `publication_standard`：投稿包、补充材料、源数据和目标 venue 规则。

## 4. Pre-write gate additions

FULL 模式必须记录：

```yaml
artifact_profile:
quality_tier:
tier_source: user | inferred | override
required_sections:
rubric_or_acceptance_criteria:
evidence_depth:
review_depth:
style_audit_required:
similarity_precheck_required:
format_requirements:
```

如果 profile 与 tier 冲突，必须说明并让用户选择：

```text
course_report + publication_standard
```

不能静默把课程报告当成期刊投稿，也不能静默降低用户的科研标准要求。
