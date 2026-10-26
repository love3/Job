# Job

[English](README.md) | 简体中文

把岗位 JD 转化为面试学习包，把真实经历整理为中英文成对简历。项目提供两个可独立使用的 Agent 技能，也能在工作区内串联。欢迎贡献教学改进、可复现示例、工具和文档。

## 开始使用

1. Clone 仓库，用 Agent 打开工作区并读取 [AGENTS.md](AGENTS.md)。需要文件读写能力；截图需要视觉/OCR，来源核实需要联网，项目验证需要对应运行环境。
2. 可选：将 `config/preferences.example.yaml` 复制为 `config/preferences.yaml`，只填写需要的设置。个人配置被 Git 忽略；示例文件不会自动生效。
3. 制作简历时提供真实经历，或将自己的 base 与参考文件放入 `Resume/private/` 并配置路径。Clone 不包含任何私人资料。除非明确要求维护 base，否则原始来源保持只读。
4. 按下面的例子调用技能。学习包默认跟随请求语言，也可在配置中指定；简历始终中英文成对。

| 流程 | 请求示例 |
| --- | --- |
| 只准备面试 | “使用 $jd-interview-prep，按这个 JD 从核心概念准备面试，不更新简历。” |
| 只制作简历 | “使用 $bilingual-resume，根据我提供的真实经历和这个 JD，生成中英文简历。” |
| 完整联动 | “按这个 JD 做完整准备，使用已配置的履历来源定制中英文简历。” |

技能入口：[jd-interview-prep](skills/jd-interview-prep/SKILL.md) 与 [bilingual-resume](skills/bilingual-resume/SKILL.md)。不能自动发现技能的 Agent 可直接读取入口及其相对引用。也可按客户端支持的方式安装或复制整个技能目录；单独的入口文件不包含全部规则。技能独立调用只使用明确提供的设置，不会反查此仓库的私人资料。

## 公开内容与本地产物

```text
Job/
├── AGENTS.md                       # 公共工作区规则
├── skills/                         # 技能唯一源码、脚本与测试
├── config/
│   ├── preferences.example.yaml    # 公开的可选配置模板
│   └── preferences.yaml            # 忽略：个人设置
├── JD/preparations/
│   ├── README.md                   # 跟踪：目录说明
│   └── <case-id>/                  # 忽略：实际学习包
└── Resume/
    ├── private/                    # 忽略：base 与原始参考资料
    └── variants/
        ├── README.md               # 跟踪：目录说明
        └── <case-id>/              # 忽略：HTML/PDF 与版本记录
```

准备包包含根 README、`artifacts/`（独立 Essential、系统 KB、QA、可选 showcase）及 `meta/`（必需的 JD、覆盖与进度记录，按需来源和简历交接）。结构通过不能证明教学深度或项目正确。简历只使用已确认事实，教程答案和自动生成项目不能直接作为本人经历。

Showcase **默认只在本地生成**。设置 `showcase.publish: public` 或 `private`，或在本次请求中明确发布后，才发布独立的 showcase 仓库。允许发布且有适合前端时，`pages: true` 请求提供静态演示；它不托管后端，也不保证私密访问。完整后端流程保留本地可复现。只发布审阅过的项目内容，不发布整个准备包或简历。

个人设置、来源资料、JD 输入和产物均被忽略。`.gitignore` 不会删除已提交的内容，也无法阻止强制添加。公开目录检查会拒绝已知私人路径和本机用户目录路径，但不能全面识别个人信息或密钥，贡献前仍须审阅。公开示例应使用虚构事实，单独放到经审阅的 `examples/` 中。

## 个人偏好

[模板](config/preferences.example.yaml) 列出支持的设置。路径相对 Job 根目录解析。`language: auto` 跟随请求，`zh-CN` 等语言标签固定学习包语言。`resume.enabled` 控制 JD 后的简历联动，不影响明确的独立简历请求。

`frontend_policy: prefer_jd` 优先采用 JD 明确的前端技术；`prefer_config` 允许 showcase 使用配置中的偏好，但教学与 QA 仍覆盖 JD 的真实要求。后端偏好用于 JD 未限定的情况。各模块的 `notes` 保存条件或写作偏好，不得取消事实和验证要求。

新任务按“本次要求 → 个人偏好 → 公共默认”确定设置。续作时，任务已确认的设置和用户修改也优先于后来修改的偏好。仅明确要求记住偏好时才更新 YAML；不要在其中保存凭据或复制履历事实。

## 依赖与验证

使用 Python 3.10+ 和 Git。依赖不要放入私人产物目录；例如，在仓库根目录运行：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_preferences.py
.venv/bin/python scripts/validate_preferences.py config/preferences.example.yaml
.venv/bin/python -m unittest discover -s scripts/tests
python3 -m unittest discover -s skills/jd-interview-prep/scripts/tests
python3 scripts/check_public_tree.py
```

默认个人配置不存在时，校验会成功跳过；显式传入的文件不存在则失败。配置检查只验证语法、类型和选项，不判断文字策略的含义。准备包校验器仅依赖 Python 标准库：

```sh
python3 skills/jd-interview-prep/scripts/validate_pack.py /absolute/path/to/pack
# 用户取消 showcase 时追加 --no-project。
```

简历渲染还需要系统 Google Chrome 以及技能依赖：

```sh
.venv/bin/python -m pip install -r skills/bilingual-resume/scripts/requirements.txt
.venv/bin/python skills/bilingual-resume/scripts/render-pdf.py /absolute/path/to/resume.html /absolute/path/to/resume.pdf
```

渲染器只在 PDF 非空、恰好一页 A4 且检查通过后替换目标文件。`REVIEW` 文件仅供失败诊断，不能作为已验证交付。交付前仍须检查两种语言的提取文字和可见页面。项目运行环境和已认证 GitHub 等能力按需提供，Clone 本仓库不会自动安装。

## 参与贡献

阅读 [中文贡献指南](CONTRIBUTING.zh-CN.md)（[English](CONTRIBUTING.md)）。执行指令以英文为主源，README 与贡献指南保持双语。公共文档语言不决定产物语言。许可证：[MIT](LICENSE)。
