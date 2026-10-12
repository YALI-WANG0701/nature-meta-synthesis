# nature-meta-synthesis

用于教育学与社会科学元综合研究的 Codex Skill。

帮助研究者从研究问题、检索与筛选，推进到质性证据提取、概念编码、主题与关系综合，以及论文撰写。支持从已有材料和项目状态继续工作，保留证据来源、反例及人工复核记录。

当前版本：**1.1.0**

主要语言：**简体中文**

## 适用范围

- 教育学与社会科学中的质性证据综合。
- 文献筛选、质量评价与证据提取。
- 跨研究的概念比较、主题综合和关系框架构建。
- CSSCI 方向论文的结构组织、初稿撰写与证据核查。
- 已有元综合项目的续接与过程记录。

不用于统计效应量合并、仅做文献计量或逐篇摘要。

## 安装

1. 在本仓库页面点击 **Code → Download ZIP**，下载并解压。
2. 找到解压目录中的 `skills/nature-meta-synthesis` 文件夹。
3. 将整个文件夹复制到 Codex 的个人技能目录。Windows 用户可在文件资源管理器地址栏输入 `%USERPROFILE%\.agents\skills`；目录不存在时先创建。
4. 确认安装后的文件位置为 `%USERPROFILE%\.agents\skills\nature-meta-synthesis\SKILL.md`。
5. 如果 Codex 中尚未出现该 skill，重启 Codex。

上述个人技能目录依据 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills)。也可以使用 Codex 内置的 `$skill-installer`，提供本仓库链接并指定技能路径 `skills/nature-meta-synthesis`。

## 使用示例

安装后，在 Codex 中输入：

```text
使用 $nature-meta-synthesis，帮我开展关于【研究主题】的元综合研究。

研究对象和情境为【范围】，已有材料位于【材料路径】。
请先判断方法与证据是否适配，形成研究问题、纳排标准和检索方案。
缺失信息标为暂定，不预告研究结果。
```

继续已有项目时输入：

```text
使用 $nature-meta-synthesis，继续【项目路径】中的研究。

请读取项目状态、最新方案和当前分析表，从【本轮阶段】继续，
沿用既有文献与证据 ID，说明已完成事项和待补材料。
```

完整操作指南位于 `skills/nature-meta-synthesis/references/user-guide.md`。

## 文件说明

- `SKILL.md`：技能入口与工作规则。
- `agents/`：显示名称、默认提示及调用设置。
- `assets/`：项目方案、论文结构与证据表模板。
- `references/`：方法依据、工作流程与用户指南。
- `scripts/`：项目初始化、结构审计与状态汇总工具。

运行随附脚本需要可用的 Python 环境。研究材料和项目产出应保存在独立项目目录中。

## 研究责任与证据边界

研究者负责最终纳入决定、争议裁定、主题解释和论文责任。AI 生成内容须依据实际取得的材料核查；未经人工复核的内容不能标记为已验证。

数据库检索、全文获取和人工复核应按实际完成情况记录。结构审计通过，不代表研究结论已经得到验证。

## 许可证

本项目采用 **MIT License**。版权署名为 **2026 YALI-WANG0701**，完整许可文本见仓库根目录的 `LICENSE`，以及技能目录中的 `skills/nature-meta-synthesis/LICENSE`。

本许可证适用于本项目自行编写的指令、脚本和模板；所引用学术论文及方法指南的原始内容保留其原有权利与许可。
