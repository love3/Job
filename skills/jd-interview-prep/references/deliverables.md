# 产物与格式

## 目录

```text
<公司>-<岗位>-<日期>/
├── README.md                 # 学习入口
├── artifacts/
│   ├── essential.md
│   ├── qa.md
│   ├── kb/
│   │   ├── 00-roadmap.md
│   │   └── <教学章节与独立练习>
│   └── showcase/             # 项目启用时：README、实现、验证说明
└── meta/
    ├── jd.md
    ├── coverage.md
    ├── progress.md
    ├── sources/              # 按需保留原始附件
    └── resume-handoff.md     # 仅在联动简历时生成
```

`jd.md`、`coverage.md`、`progress.md` 在完整包中必需，取消项目也保留；不新增重复的 JSON 要求台账、研究日志或工具流水。教学文件真实存在，符号链接和缓存不能充当正文或实现证据。链接相对**所在文件**解析：覆盖表到教材用 `../artifacts/...`，KB 章节到 JD 用 `../../meta/jd.md`。

## JD 与覆盖表

`meta/jd.md` 保存来源及访问时间、忠实提取、未知处、用户限制与采用设置。要求编号在首列且每表唯一：显式要求 `JD-*`，必要推断 `INF-*` 并写依据；P0 为核心、P1 为支撑、P2 为扩展。续作保留原编号，新增要求追加。

```markdown
| ID | 来源类型 | JD 要求/补充能力 | 优先级 |
| --- | --- | --- | --- |
| JD-001 | 明确 | 本 JD 的实际要求 | P0 |
| INF-001 | 推断 | 有依据的必要先修 | P1 |
```

`meta/coverage.md` 的 ID 集合、类型与优先级须与 JD 一致；每行对应教学、问答及实际证据或差距：

```markdown
| ID | 类型 | 优先级 | 要求 | Essential | KB | QA | 实践证据/差距 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| JD-001 | 明确 | P0 | 实际要求 | [机制](../artifacts/essential.md) | [教学](../artifacts/kb/01-topic.md) | [追问](../artifacts/qa.md) | [实现与验证](../artifacts/showcase/README.md) |
```

- 核心要求链接对应正文，尽量定位章节。支撑或扩展要求可在 Essential 列写 `非核心：具体原因`，KB、QA 仍承接；不能因难、项目未做或标成 P1 就排除关键主题。
- 学历、年限等写 `非学习项：原因`，保留真实差距与回答。实践列链接包内实际文件或有内容的真实目录，不能借符号链接引用包外证据。
- 未完成或无法证明时用 `差距：原因`、`待完成：原因与下一步`、`未验证：原因`。取消项目写 `已省略：用户取消项目`，同时提供适合的 KB 练习。
- 复合要求在同一行链接各子能力，或在表后按原 ID 简述映射；不插断表格，不重复编号。已有链接不代表内容讲够。

英文产物使用同一格式：JD 表头 `ID | Source type | JD requirement / supplemental capability | Priority`；覆盖表头 `ID | Type | Priority | Requirement | Essential | KB | QA | Practice evidence / gaps`。类型 `Explicit`/`Inferred` 不区分大小写，分别对应明确/推断；状态对应 `Non-core:`、`Non-learning item:`、`Gap:`、`Pending:`、`Unverified:`、`Omitted:`，均须具体理由。

## 各文件职责

教学深度按入口指定的教学规则执行；此处只约定文件责任。

| 文件 | 应包含什么 |
| --- | --- |
| `artifacts/essential.md` | 岗位核心问题总览、独立正文、完整例子、自测与参考推理 |
| `artifacts/kb/00-roadmap.md` | 知识主线、先修回补、章节入口、练习和验收路线 |
| KB 章节 | JD 关联、目标、先修、机制、例子、变式练习及答案；可附独立练习文件 |
| `artifacts/qa.md` | 按主题组织的口述回答、展开推理和追问；项目题关联实际证据 |
| `artifacts/showcase/README.md` | 业务价值、环境/依赖、启动、数据、演示步骤、预期结果和测试命令 |

项目另按需要写设计取舍、验证记录与演示脚本，说明数据流、替代方案、局限、JD 映射，以及实际命令、版本、日期、结果、未测部分。非技术岗位交付有来源、方法和评价标准的可检验作品，不强加软件。

包入口先写岗位主线和学习优先级，再给核心、系统、实践路线，直达 Essential、KB、QA；项目和线上链接仅在存在且验收后添加。最后链接 Meta、事实差距与未完成项，不要求读者先翻运行记录。

## 进度与验收

确定目录即写 `meta/progress.md`，记录输入/采用设置、当前决策、已完成文件、验证摘要、阻塞及下一步。文档、实现、项目验证、源码发布、线上演示、简历各记独立状态；未知字段不补造。源码记录仓库 URL/分支/SHA；Pages 另记实际 URL、workflow run、部署提交和浏览器结果。每阶段更新当前状态，不堆逐次工具输出。

在技能目录运行，或使用脚本绝对路径：

```sh
python3 scripts/validate_pack.py /absolute/path/to/pack
# 项目被取消时追加 --no-project；非技术作品用 --portfolio，二者互斥。
```

结构检查只验证文件、正文存在性、相对文件链接、ID、类型/优先级及映射；不验证锚点、外网链接、教学深度、代码运行或发布。技术项目至少有非文档实现文件，作品集至少有 README 之外的非空作品。内容、项目运行和发布另行验收，未完成状态在入口、进度和交付中一致说明。
