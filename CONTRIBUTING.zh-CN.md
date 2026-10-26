# 参与 Job 贡献

[English](CONTRIBUTING.md) | 简体中文

欢迎改进教学、简历取材与排版、可复现工具、测试或文档。较大的行为调整先用 issue 讨论，小而明确的修复可以直接提交 PR。讨论可用中文或英文。

## 修改流程

1. Fork 并 Clone 仓库，为改动建立分支，读取 [AGENTS.md](AGENTS.md)。技能唯一源码位于 `skills/`。
2. 在临时目录使用虚构 JD 与简历事实，不修改真实 base，不以测试为由发布 showcase 仓库。
3. PR 说明具体问题、修改后的行为和真实验证结果。教学改动附输入及简短前后对照，结构检查不能单独证明教学改善。
4. 执行下面的检查，审阅暂存 diff 和将公开的完整历史，提交前清理临时文件。不要强制添加被忽略的私人文件。

## 检查命令

在仓库根目录使用 Python 3.10+：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_preferences.py config/preferences.example.yaml
.venv/bin/python -m unittest discover -s scripts/tests
python3 -m unittest discover -s skills/jd-interview-prep/scripts/tests
python3 -m unittest discover -s skills/bilingual-resume/scripts/tests
python3 scripts/check_public_tree.py
```

存在个人配置时，另运行 `.venv/bin/python scripts/validate_preferences.py`，私下审阅其含义，不要将全文贴到 issue。公开目录检查读取 Git 索引，本地提交前须先暂存已审阅的公开修改；CI 检查已提交内容。它能发现已知私人路径和本机用户目录路径，但不能全面识别个人资料或凭据。

修改简历内容、版式或渲染时，安装 `skills/bilingual-resume/scripts/requirements.txt` 和系统 Google Chrome。用技能渲染器处理虚构的中英文 HTML，检查一页 A4、提取文字，并分别做视觉检查。仅修改来源路径时，不需要重新渲染私人简历。

修改技能行为时，独立测试有代表性的请求：默认设置、本次明确覆盖、修改配置后的续作。指出指令或产物中支持判断的依据。未执行的项目测试或模型集成不得写成通过。现有准备包检查支持中英文映射词汇。

## 文档与偏好

`AGENTS.md`、技能指令和执行参考以英文为主源。README 和贡献指南的中英文版本保持语义一致，包括命令与路径。不增加另一套自动加载的指令译本。请求和产物语言独立于公共文档语言。

仅为真实使用需求增加配置。修改配置合同时，同步修改公开示例、校验器、测试和双语 README。自然语言偏好放在模块的 `notes` 中，不为每种写作偏好扩展枚举。本次要求和任务已确认设置仍有更高优先级。

## 私人资料与公开示例

个人配置、`Resume/private/`、真实准备包和派生简历不能进入提交、issue、日志或截图。不贡献真实雇主保密资料或凭据。公开示例须为经审阅的虚构内容，放在 `examples/` 中；不要取消私人产物目录的忽略来共享示例。保留用户手改及来源只读边界。

原创代码与文档贡献采用仓库的 [MIT 许可证](LICENSE)。包含第三方材料时注明来源和许可证，以便纳入前审阅。
