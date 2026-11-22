# Argument Outline and Claim Traceability

本文件连接“证据账本”和“正文”。目标是让每个核心段落、图表和结论都能追溯到 claim 和 evidence。

## 1. 论证提纲

在证据核验后、正式写作前建立：

```markdown
# Argument Outline

## Section: Introduction
- Question:
- Core claim:
- Supporting evidence IDs:
- Counterevidence / alternative explanation:
- Limitation / boundary:
- Link to next section:

## Section: Results
...
```

每个 section 至少要有一个核心 claim、证据、反例/替代解释和边界。没有这些内容的 section 不应进入正式写作。

## 2. Claim register

推荐字段：

```csv
claim_id,section_id,paragraph_id,figure_id,claim_text,evidence_ids,support_strength,allowed_wording,status,notes
```

规则：

- `claim_id` 唯一；
- 每个核心段落或图表有 `section_id`/`paragraph_id`/`figure_id`；
- `evidence_ids` 必须在 evidence ledger 中存在；
- `status` 只能是 `supported`、`partially_supported`、`unsupported`、`needs_author_input`；
- `allowed_wording` 限制因果、机制、预测或建议强度。

## 3. 正文 marker

使用：

```text
{{C001}}
```

示例：

```text
The intervention reduces processing time under the tested conditions {{C012}}.
```

规则：

- 一个段落可以有多个 claim marker；
- 一个核心段落不能完全没有 marker；
- 摘要、结果、讨论复用同一 claim 时必须使用同一 ID 或明确映射；
- 正文中的数字、图号、表号与 claim register 对应。

## 4. 变更影响分析

当证据或数据发生变化：

1. 定位受影响的 `claim_id`；
2. 找到对应 section/paragraph/figure；
3. 只重审受影响的位置；
4. 如果 claim 的核心含义变化，回退到 argument outline；
5. 如果证据不足，回退到 evidence 或 analysis；
6. 记录 backtrack log。

## 5. 可执行检查

运行：

```bash
python3 scripts/check_quality.py \
  --manuscript path/to/manuscript.md \
  --claims path/to/claim-evidence.csv \
  --evidence path/to/evidence-ledger.csv
```

脚本只检查确定性问题：

- claim ID 重复；
- claim marker 缺失；
- evidence ID 不存在；
- evidence 未核验；
- 占位符；
- 空字段。

科学解释、论证有效性和作者责任仍由人判断。
