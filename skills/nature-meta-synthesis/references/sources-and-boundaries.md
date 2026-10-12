# 依据、适用范围与迁移边界

## 用户材料与本 skill 的关系

| 材料 | 已读取位置 | 采用的内容 | 迁移时的限制 |
| --- | --- | --- | --- |
| 仇星月等《大语言模型支持的元综合研究：基于智能体的方法》 | 全文，印刷第 63–72 页；PDF 页序 1–10 | 质性证据跨研究比较、四项应用原则、两模块六角色、人在回路中 | 是特定教育任务的工具与案例研究，不是覆盖所有综述传统的通用方法手册 |
| 原文图 1、图 2及工具实现 | 印刷第 65–67 页；PDF 页序 3–5 | 逐项评价、规则判断、观点存储、概念主题与关系汇总的衔接 | 不强制使用 COZE、GPT-3.5/GPT-4 或原文上下文窗口 |
| 原文评价与案例 | 印刷第 67–70 页；PDF 页序 5–8 | 模型输出具有概率性，需要研究者审阅与集体反思 | 九项指标、A–D 分级、B 级准入、20 篇/两组各 10 篇均属原案例做法；不设为通用门槛 |
| 用户 `meta_synthesis.pptx` | 全部 25 页及演讲备注；第 7–15 页为八步流程，第 16–20 页为 AI 工作流，第 23 页为交付清单 | 设计、检索、筛选、提取、主题、关系、质控、写作；来源定位与过程记录 | PPT 已说明其八步为操作整理，不能转述为原文固定八步法或 Hoon 八步法 |
| 用户 PPT 第 21、22 页 | 教学示例与原论文案例边界 | 区分演示与真实发现；覆盖面和稳定性不等于正确性 | 第 21 页 A/B/C 是虚构教学材料，不能成为正式论文证据 |

本 skill 新增：研究阶段状态文件、数据字段、稳定 ID、空白模板、初始化与结构审计工具、论文写作模板。这些是为实施与可追溯性整理的设计，不归为仇星月等原文贡献。没有把原 PDF 或 PPT 全文打包进 skill。

原论文书目信息：仇星月，陈向东，陈鹏，褚乐阳，崔萌（2025）. 大语言模型支持的元综合研究：基于智能体的方法.《现代教育技术》，35(1)，63–72. [DOI](https://doi.org/10.3969/j.issn.1009-8097.2025.01.007)。元数据来自用户提供的 PDF。

## 核验的方法来源

以下链接于 2026-10-10 核查；后续实质项目在确定方法、工具版本或投稿要求时重新核对原始来源。

| 来源 | 支持的具体事项 | 不应据此声称 |
| --- | --- | --- |
| Thomas, J., & Harden, A. (2008). Methods for the thematic synthesis of qualitative research in systematic reviews. *BMC Medical Research Methodology, 8*, 45. [原始论文](https://link.springer.com/article/10.1186/1471-2288-8-45) | 主题综合中编码、描述性主题、分析性主题的区分；保持解释与原研究文本的联系 | 所有元综合都必须使用同一主题分析算法 |
| Hoon, C. (2013). Meta-Synthesis of Qualitative Case Studies: An Approach to Theory Building. *Organizational Research Methods, 16*(4), 522–556. [出版商页面](https://journals.sagepub.com/doi/10.1177/1094428113484969) | 质性案例元综合服务于理论建构；摘要确认作者提出八步 | 本次已核查受限全文的每一步；本 skill 八步与 Hoon 八步相同 |
| Tong, A., Flemming, K., McInnes, E., Oliver, S., & Craig, J. (2012). Enhancing transparency in reporting the synthesis of qualitative research: ENTREQ. *BMC Medical Research Methodology, 12*, 181. [原始论文](https://link.springer.com/article/10.1186/1471-2288-12-181) | 质性综合透明报告；21 个项目覆盖介绍、方法、检索选择、评价和综合等领域 | 报告清单就是研究分析方法；教育类期刊均强制要求 ENTREQ |
| Page, M. J., et al. (2021). The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ, 372*, n71. [官方入口](https://www.prisma-statement.org/prisma-2020-statement) | 按适用项目报告系统综述流程，区分过程记录和综合方法 | 全部元综合都适用所有项目；只有流程图即可声称符合报告规范 |
| Lewin, S., et al. (2018). Applying GRADE-CERQual to qualitative evidence synthesis findings: introduction to the series. *Implementation Science, 13*(Suppl 1), 2. [原始论文](https://link.springer.com/article/10.1186/s13012-017-0688-3) | 各条综合发现的证据信心：方法学局限、连贯性、数据充分性、相关性 | 为单篇研究打质量总分；未经评价自动赋予高信心 |
| JBI. Critical Appraisal Checklist for Qualitative Research (2017). [官方清单](https://jbi.global/sites/default/files/2019-05/JBI_Critical_Appraisal-Checklist_for_Qualitative_Research2017_0.pdf)；[官方工具入口](https://jbi.global/critical-appraisal-tools) | 2017 质性清单包含十项；按条目判断并说明综合处置，采用时记录版本 | 原文九项就是所有版本；存在通用 B 级阈值；期刊等级等同研究质量 |
| Improving reporting of meta-ethnography: the eMERGe reporting guidance. [原始报告指南](https://link.springer.com/article/10.1186/s12874-018-0600-0) | 采用元民族志时选择与其概念转译程序匹配的报告要求 | 本 skill 已提供完整元民族志程序；一般主题综合可直接改名为元民族志 |

## 不能从原案例推出的结论

原文是高中物理“运动学”教学模式场景下的探索性应用，12 名本科师范生参与，研究者使用 20 篇论文分组开展活动。它可以启发任务拆解与人机协同，不能证明任意教育学/社科元综合交给智能体即可完成。

原文报告评分一致性 Kendall W = 0.544，并观察多轮生成趋稳；这不能替代事实核查、方法学有效性检验或真实独立评审。原文“涵盖主题与关系更全面”的比较也不能直接转述为模型必然更准确。skill 不要求复现十次生成、固定文献篇数或据此宣称饱和。

教育学社科研究的适配建议——如数据库选择、情境字段、反例检查、分层处理理论材料和证据 ID——属于本次实施设计。选具体领域后应结合其研究传统、原始方法指南和目标期刊进一步调整。

## v1.1的实践改进来源

2026-10-11至12的GenAI与学生创造性问题解决项目检验了数据库导出、人工复核子集、七维适配、主/拓展/背景分层、主题关系、反例质控、CSSCI初稿和Word转换的实际衔接。v1.1据此完善状态、字段和程序边界，不把该项目的篇数、主题数、评价门槛、教学理论或格式环境设为通用规范。

用户提供李会军、席酉民（2019）的商业模式创新案例元综合，以及冉连、吴铭洋（2024）的政府数据开放安全元综合作为中文写作参照。采用其由研究问题、设计与编码推进到框架和讨论的篇章思路，不复制其具体验证程序或质量等级。范文全文未打包进skill。

本次用户指定的七维评价与Glynn原工具、姜婷婷等[19]的确切出处仍未唯一核定。新增七维指导明确作为可适配的项目维度，不声称补齐了这些缺失的原始方法依据。现有方法链接的历史核查日期保留；没有把本轮编写技能的日期改写成重新核验全部学术来源的日期。
