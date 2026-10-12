# 证据数据契约

## 标识符和记录单位

使用稳定 ID，编号是示意格式，可按项目调整；分配后不随排序改变。

| ID | 单位 | 例子及关系 |
| --- | --- | --- |
| `record_id` | 某来源导出的检索记录 | R0001；不同数据库的重复记录保留来源，归到同一报告 |
| `report_id` | 一篇论文、学位论文或其他报告 | P0001；同一研究多篇报告各有 report_id |
| `study_id` | 一项独立原始研究 | S0001；共同样本或同一项目的重复报告原则上归组，是否独立需实际核查 |
| `evidence_id` | 一条有位置的证据单元 | E0001；必须关联 report_id 与 study_id |
| `code_id` | 一个有定义的编码 | C001；一个单元可有多个编码 |
| `theme_id` | 一个描述性或分析性主题 | T01；矩阵逐条链接证据 |
| `relation_id` | 一条概念/主题关系 | L01；支持、反例分别记录 |
| `claim_id` | 正文中需证据支撑的一条论断 | CL001；可关联多个证据 ID |

报告含多个真正独立研究时，`study-register.csv` 每个 `report_id,study_id` 对占一行。不要为方便强制一文等于一研究。仅知道报告数量但尚未识别研究独立性时，不给“独立研究数”；将重复样本状态记为待核查。

`study_id`可以暂归，但暂归编号不同不能证明研究独立。可选`corpus-register.csv`按报告记录资料层级；`independence_status=confirmed`表示独立性实际核定，`pending`表示尚未核定。范围确认人/日期只说明采用报告集，不改写分析的人工状态。

## 文件与最小字段

初始化脚本把空 CSV 复制到项目 `data/`。CSV 使用 UTF-8；长文本用规范引号；同格多个 ID 用分号分隔，例如 `E0001;E0003`。空模板不含示例研究或模拟发现。

| 文件 | 行的单位 | 用途与关键规则 |
| --- | --- | --- |
| `search-log.csv` | 一次真实或计划检索 | 完整检索式、平台/字段/限制、日期、数量、原始导出；query_status 区分 planned/executed |
| `screening-log.csv` | 一条记录在一个阶段的判断 | 多阶段和不同评审者可多行；记录准入、排除、待定和全文未获；duplicate_of 指检索重复记录 |
| `study-register.csv` | 一个报告与研究的配对 | 引用、来源、设计、证据类型、对象、情境、样本说明、重复样本状态和纳入状态 |
| `appraisal.csv` | 一个报告/研究在一条评价项目上的判断 | 实际工具、版本、条目、原文依据、判断、评价者和后续处置；不默认计算总分 |
| `evidence-units.csv` | 一条证据 | 原文、译文、原作者解释、情境、定位、编码和复核状态分开 |
| `codebook.csv` | 一个编码 | 名称、定义、纳入/排除规则、实际示例证据、版本；变更另外留审计记录 |
| `theme-evidence.csv` | 一个主题与一条证据的对应 | 描述性/分析性层级、支持/反例/条件/补充及情境；未提及不填成反例 |
| `relations.csv` | 一条关系 | 起止概念、类型、陈述、支持/反例证据、条件、解释层级；若有计数，填写唯一支持 study_id 数 |
| `claim-ledger.csv` | 一条正文论断 | 论文位置、论断性质、支持/反例、范围、证据信心是否正式评价、人工状态 |
| `audit-log.csv` | 一次有用的研究或 AI 操作 | 日期、阶段、执行者类型、工具模型实际标识、提示版本、输入输出、核查方式、修改说明 |

具体 CSV 表头见 `assets/tables/`，需要额外字段时可以增加，但保留关联字段。优先增加能改变解释的情境信息，不机械填充无关变量。

v1.1增加六张可选过程表，旧项目缺少它们不报缺表错误，新增字段也不要求补造历史值：

| 文件 | 使用场景 | 行单位与要点 |
| --- | --- | --- |
| `corpus-register.csv` | 人工确认文献集、主/拓展/背景及版本 | 一份报告；报告用途、证据主体、全文状态、版本比对与独立性分别登记 |
| `code-assignments.csv` | 细化概念赋值与修订 | 一条证据到一个编码；稳定assignment_id；退役保留，不覆盖旧关系 |
| `revision-log.csv` | 概念拆分、映射退役、字段修订 | 一次字段修订；旧/新值、理由、依据与版本，原文与译文分别保留 |
| `sensitivity-checks.csv` | 关系的范围与移除比较 | 一项范围下的一条关系；规则、移除/保留材料与解释变化，不充当统计检验 |
| `reference-checks.csv` | 正文书目核查 | 一条引用；核对字段、原始路径、用途、限制及日期，不等同全文质量审核 |
| `draft-claim-map.csv` | 将成稿句段链接现有证据 | 一条版本化草稿主张；链接CL/E/L，避免为写作复制为新发现 |

只在有实际记录时填表。项目额外表可保留原命名，续接时说明对应关系；不为满足脚本盲目重建既有数据。

## 状态词与材料层级

- `human_review_status`：`pending`（尚未人工核查）、`verified`（确已核查并通过）、`rejected`（驳回）、`not_applicable`（该行无人工判定需求；不能用于正式研究论断）。审核者和日期另在审计日志记录。
- `extraction_status`：`candidate`、`located`（来源已定位）、`blocked`（缺全文或识别障碍）。`located` 不是人工核查通过。
- `inclusion_status`：`include`、`exclude`、`pending`。助手建议写在备注或候选决定中；只在研究者实际采用后更新为最终决定。
- `unit_type`：`participant_material`、`author_finding`、`author_interpretation`、`theoretical_text`、`practice_recommendation`。没有一阶引文并非自动缺陷，但必须如实区分层级。
- `theme_level`：`descriptive`、`analytical`；`relation_to_theme`：`support`、`counter`、`condition`、`supplement`。未报告通常不创建关系行。
- `interpretive_status`：`author_claim`、`reviewer_interpretation`、`candidate`。采用的解释仍应保留是谁提出的，而非全部标成“事实”。
- `claim_type`：`synthesis_finding`、`interpretive_proposition`、`implication`、`background`。正文正式综合发现和解释命题须在 ledger 中有证据。背景引用可由单独文献核查管理。
- `certainty_status`：未执行正式信心评价记 `not_assessed`；执行则用实际框架与判断，可将长说明放入发现信心表。

新增可选字段约定：

- `corpus_role`：`main`、`extension`、`background`、`pending`、`excluded`，与证据主体独立；不以它代替筛选决定。
- `evidence_subject`：如`target_population`、`indirect_observer`、`mixed_separable`、`theoretical`；可按项目扩展，不强制沿用学生A/导师B标签。
- `contribution_role`：`substantive`、`context_only`；支持/反例/条件仍在主题或关系表分别标记。
- `fulltext_status`：`retrieved`、`not_retrieved`、`partial`、`not_required`；`fulltext_scope`：`body_only`、`body_and_si`，按实际来源说明正文内附录。
- `version_match_status`：`matched`、`pending`、`not_applicable`，描述正文版本核对，不由DOI存在自动判为matched。
- `mapping_status`、`assignment_status`、`code_status`、`relation_status`、`claim_status`：缺字段/空值兼容旧项目；`active`/`candidate`进入当前视图，`retired`/`superseded`仅保留历史。`replaced_by`/`superseded_by`应能回查真实替代ID。
- `analysis_scope`：`main`、`extension`、`background`、`combined`；默认主综合关系不能把背景作为经验支持，combined也不能将理论文本变成经验资料。
- 若理论文本本身是明确界定的研究对象，可额外记录`analysis_basis=theoretical_text`并说明所选文本综合设计；不当作参与者经验研究。普通经验元综合不使用此字段规避证据分层。
- `result_count`仅在可知时表示平台显示命中量；`exported_record_count`表示实际导出量，`count_basis`说明口径。未知留空；planned/access_failed不是零命中。

## 位置、原文和复核

优先记录 `source_path`、1 起算的 `pdf_page`、原有 `print_page` 及章节/段落或表图位置。印刷页码可以为罗马数字或区间，不强制转数字。网页等非 PDF 来源以稳定地址/保存路径及段落定位替代，缺 PDF 页序不自动无效。

`original_text` 只能填来源中的实际文字。省略与合并应明确标示，不能把不相邻句段拼为一个连续引文。译文、概括、观点总结各进入自己的字段。原文不可辨、引用二手来源或没有全文时保留状态，不能写成已核验。

AI 提取和自动字段检查能够支持核查，不能代替研究者读原文的判断。人工 `verified` 必须有实际审核操作；代理以程序核对文字可记录为自动核对，不冒充人工复核。

## 计数与正式报告

关系支持数 = 支持证据关联的唯一 `study_id` 数。重复报告增加 report 数，不增加 study 数；反例单独列出。同一研究可同时包含支持与相反材料，不能因此抹去冲突。

筛选流程必须分别核对记录、报告和研究的数量；合并多个检索来源前处理来源重叠。已获取全文但排除与未获全文是不同去向。关系计数和筛选计数不共用同一个分母。主题频数只说明被纳入材料的覆盖，不能表示人群普遍性、因果强度或效果大小。

可选发现信心表字段：发现 ID/文本、支持研究及数据丰富度、方法学局限、连贯性、充分性、相关性、总体信心与理由、审核者、日期。只有真正执行相应框架，才称为其正式评价。

## 结构审计工具的边界

`scripts/audit_project.py` 读取上述数据，检查关键 ID 重复和关联、定位字段、人工通过的提取是否完整、关系计数是否去重、正式论断是否指向已复核证据。尚无数据时返回 `SCAFFOLD_ONLY`，不是科学审计通过。

工具输出 `ISSUES_FOUND` 时修复结构错误后再运行；`STRUCTURE_OK` 只表示所查结构未见问题，仍须核对原文真实性、完整提取、评价工具适配、主题解释、反例和引用。工具不自动计算 PRISMA 数字，也不验证独立研究归组是否正确。

v1.1审计保留累计行数，并另报活动行数；退役行仍检查ID，但不当作当前正式支持。配置了corpus表时检查主关系的材料用途及仅情境支持；独立性未核定而填写独立研究计数时提示，人工通过的正式计数须具备独立性记录。`summarize_project.py`只汇总登记状态；独立研究数未知返回null并说明原因，不从S编号推断。
