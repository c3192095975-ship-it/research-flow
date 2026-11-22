# Artifact Quality Gates

质量门是交付条件，不是装饰性检查。每个 profile 将门标记为 `required`、`optional` 或 `not_applicable`，并记录证据。

## Gate A: Task and rubric coverage

检查：

- 所有 required sections 是否存在；
- 作业/期刊的 rubric 或 acceptance criteria 是否逐项覆盖；
- 字数、页数、格式、受众、截止时间是否满足；
- 案例事实、作者观点和推荐是否分开；
- 是否有未说明的缺失材料。

通过条件：没有未解释的 rubric 缺口。失败时补结构或说明不适用项，不用空泛段落填充。

## Gate B: Evidence and citation

检查：

- 每个来源的身份、标题、年份、作者、URL/DOI；
- 每个核心 claim 是否有来源、定位和 claim marker；
- claim/evidence 是否存在断裂、未知 ID 或未核验记录；
- 来源是否真的支持该主张；
- 引用是否与 bibliography 一致；
- 案例事实、法律/标准、作者推论是否分开。

通过条件：没有伪造、错配或无法定位的核心来源；claim register 与 evidence ledger 可以互相解析。先运行 `scripts/check_quality.py`，再做人工科学判断。失败时回退 evidence 或 argument outline，不用更漂亮的文字掩盖。

## Gate C: Language and claim strength

检查：

- 主张强度是否匹配证据；
- 相关是否被写成因果；
- 建议是否被写成已实施结果；
- 术语、语气和时态是否一致；
- 是否存在过度防御、模糊归因或重复限定。

通过条件：没有 unsupported strengthening 或 meaning drift。失败时回到写作 owner 或 claim calibration，不切换到第二套写作体系。

## Gate D: Originality and style precheck

检查：

- 与 provided prompt / known source set 的 8/10-word n-gram 重合；
- 引用是否完整；
- 内部重复段落；
- AI 风格审计（英文适用 `avoid-ai-writing`；中文按 profile 选择）；
- 独立完成规则是否被明确提醒。

边界：

- 本地风格检查不等于 Turnitin AI 率；
- 本地相似度预检不等于 Turnitin 查重；
- 不能伪造官方分数或宣称必然低重复；
- 提交后仍需查看正式报告和课程规则。

通过条件：没有未处理的高风险重合或引用问题，并明确记录官方检测不可预知。

## Gate E: Production and format

检查：

- DOCX/PDF/PPTX 是否成功构建；
- 页面尺寸、字体、字号、行距、页眉页脚；
- 页码、标题层级、图表编号、参考文献；
- 姓名/学号/作者信息是否完整；
- 占位符、乱码、空链接和损坏图片；
- 图表 source data 和视觉 QA；
- 可访问性和阅读顺序。

通过条件：实际文件可打开、可读、通过视觉检查。不能把“生成成功”当成“格式合格”。

## Gate F: Human accountability

检查：

- 作者是否完整阅读；
- 作者是否核对学生/作者信息、课程信息、数据和引用；
- 作者是否确认独立完成、AI 使用和提交规则；
- 作者是否批准最终版本；
- 是否区分内部质量评估和正式成绩/录用结果。

通过条件：作者明确批准。AI 不能代替作者签字、提交或承担学术责任。

## Executable checks

可运行检查只处理确定性事实：

- 重复 claim ID；
- claim marker 不在 claim register；
- evidence ID 不存在；
- 未核验 evidence；
- `TODO/TBD/AUTHOR_INPUT_NEEDED` 等占位符；
- 基础 CSV 字段完整性；
- argument outline 的必要字段。

```bash
python3 scripts/check_quality.py --manuscript manuscript.md --claims claim-evidence.csv --evidence evidence-ledger.csv
```

脚本通过不等于科学结论正确，也不等于 Turnitin 通过。

## Applicability matrix

| Profile | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| `manuscript` | required | required | required | optional/required by venue | required | required |
| `course_report` | required | required | required | required when AI/similarity rules apply | required | required |
| `proposal` | required | required | required | optional | required | required |
| `thesis` | required | required | required | required when institution requires | required | required |
| `presentation` | required | required for factual claims | required | optional | required | required |

`not_applicable` 必须有理由，不能用来逃避检查。

## Failure handling

1. 记录失败门和具体证据。
2. 只修复受影响的阶段。
3. 复验同一个门。
4. 默认最多两轮。
5. 第三轮必须有新证据、范围变化、用户明确要求或新风险。
6. 不能因为某个门失败就换一个写作/图表/评审 skill 绕过。

## Tier-strength matrix

| Tier | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| `course_pass` | required | required | required | optional | required | required |
| `course_high` | required | required | required | required when rules apply | required | required |
| `research_standard` | required | required + claim matrix | required | required when originality rules apply | required | required |
| `publication_standard` | required | required + venue audit | required | required per venue | required + package | required |
| `custom` | define | define | define | define | define | required |

Higher quality tier can increase evidence and review depth without adding irrelevant skills. A higher tier does not automatically mean `paper-spine`, `nature-reviewer`, `nature-statistics`, or `nature-figure` are applicable.
