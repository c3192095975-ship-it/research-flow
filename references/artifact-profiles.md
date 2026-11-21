# Artifact Profiles

路线回答“语言和学术风格是什么”，profile 回答“最终产物是什么”。两者同时锁定后，ResearchFlow 才能选择正确的阶段和能力，而不是把全部科研 skill 强行塞进每个任务。

## 1. 选择规则

1. 先从用户要求和现有工件判断 profile。
2. 目标不明确但产物是课程作业：`course_report`。
3. 目标是完整期刊/会议论文：`manuscript`。
4. 目标是开题、基金或研究计划：`proposal`。
5. 目标是学位论文或毕业设计：`thesis`。
6. 目标只是组会、答辩或展示：`presentation`。
7. 同一任务可以有一个主 profile 和一个辅助 profile，例如 `thesis + presentation`；但当前阶段只能有一个主 profile。

## 2. Profile: manuscript

适用：完整科研论文、期刊投稿、会议论文。

默认流程：

```text
scope -> search -> read -> evidence -> analysis -> statistics -> figures
-> writing -> production -> review -> response -> delivery
```

必要条件：

- 研究问题和贡献边界；
- 可核验来源和 citation ledger；
- 数据/代码/实验记录（如适用）；
- 统计单位、不确定性、图表 source data（如适用）；
- 目标 venue 的格式与投稿规则。

不使用：把课程报告低标准写成论文，或跳过 evidence/statistics/figures。

## 3. Profile: course_report

适用：课程论文、案例分析、伦理报告、实验报告、有 rubric 的作业。

默认流程：

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

必要条件：

- 作业要求、rubric、允许的资料和提交格式；
- required sections 和字数/页数；
- 引用与独立完成规则；
- 课程/教师提供的案例事实与官方来源分开记录。

通常排除：

- `paper-spine`：完整论文投稿包过重；
- `nature-reviewer`：不是完整科研论文审稿；
- `nature-statistics` / `nature-figure`：没有数据或图表要求时不适用；
- `academic-research-suite`：容易和 `research-flow` 争夺总控；
- `literature-review`：不是系统综述时不应强行加入。

## 4. Profile: proposal

适用：开题、基金申请书、研究计划、项目申请。

默认流程：

```text
research-flow
-> scientific-brainstorming
-> nature-proposal-writer
-> nature-academic-search
-> nature-ref-verifier
-> scientific-writing
-> peer-review
-> documents
```

必要条件：

- 问题、意义、研究空白、研究设计；
- 可行性、资源、时间线、风险和伦理；
- 预实验或已有结果边界；
- 参考文献真实性。

不自动生成虚构预实验、合作方、预算或伦理审批。

## 5. Profile: thesis

适用：本科/硕士/博士学位论文、毕业设计。

默认流程：

```text
research-flow
-> route-specific writing owner
-> evidence ledger
-> analysis/statistics/figures as applicable
-> chapter drafting
-> consistency audit
-> independent review
-> documents/PDF/格式生产
```

必要条件：

- 章节结构和学校模板；
- 章节间数字、术语、引用和图号一致；
- 作者、导师、伦理、数据声明；
- 学校格式与提交规则。

不把课程短报告标准当作学位论文标准，也不把学位论文强行当成期刊投稿包。

## 6. Profile: presentation

适用：组会、答辩、科研汇报、课程展示。

默认流程：

```text
research-flow
-> select manuscript/thesis artifacts
-> narrative compression
-> figure/asset selection
-> presentation owner
-> visual QA
-> delivery
```

必要条件：

- 受众、时长、叙事目标；
- 稿件/数据/图表来源；
- 不改变研究结论来适配版式；
- 引用来源和视觉 QA。

## 7. Pre-write gate

FULL 模式在任何正式写作前必须确认：

```yaml
artifact_profile:
route:
required_sections:
rubric_or_acceptance_criteria:
evidence_ledger:
claim_boundary:
writing_owner:
style_audit_required:
similarity_precheck_required:
format_requirements:
```

缺项时先补缺口，不允许用写作掩盖证据或 rubric 缺失。
