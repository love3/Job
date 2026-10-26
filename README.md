# Job：面试准备与双语简历

从岗位问题建立能力主线，用知识、练习和作品准备面试；从真实经历提炼贡献，生成中英文简历。

## 使用

让 Agent 读取 [AGENTS.md](AGENTS.md)，再提出任务：

| 需要什么 | 请求示例 |
| --- | --- |
| 面试准备 | “用 $jd-interview-prep 准备这个 JD，只准备面试。” |
| 双语简历 | “用 $bilingual-resume 根据这些真实经历和 JD 生成简历。” |
| 完整联动 | “按这个 JD 做完整准备，并用已配置的经历定制双语简历。” |

两个技能可独立安装，需复制整个技能目录。不能自动发现技能的客户端，可直接读取其 `SKILL.md`。学习资料跟随请求语言或个人配置；简历始终中英文成对。

## 资料与产物

| 路径 | 用途 | 是否入库 |
| --- | --- | --- |
| `skills/` | 技能、参考规范、脚本 | 是 |
| `config/preferences.example.yaml` | 配置模板 | 是 |
| `config/preferences.yaml` | 个人偏好 | 否 |
| `JD/preparations/<case-id>/` | 面试包：`artifacts/` 教材与作品，`meta/` 岗位依据与进度 | 否 |
| `Resume/private/` | 自己的 base 与原始参考资料 | 否 |
| `Resume/variants/<case-id>/` | 派生简历及版本说明 | 否 |

没有 base 时可直接提供真实经历。base 默认只读，只有明确要求维护时才修改。技能独立调用的根目录产物 `preparations/`、`resume-variants/` 同样被忽略。

## 个人设置

将配置模板复制为 `config/preferences.yaml`，按需填写；不配置也能运行。键和可选值见[模板](config/preferences.example.yaml)，路径相对项目根目录。

- `auto` 跟随请求语言或岗位选型；`frontend_policy: prefer_config` 可让指定前端优先于 JD，但教学仍完整覆盖 JD。
- `showcase.enabled: false` 取消项目；`resume.enabled: false` 取消完整 JD 后的简历联动，不影响明确的独立简历请求。
- 新任务按“本次要求 → 个人偏好 → 默认”执行；续作先保留原任务已确认设置与手改。明确要求记住偏好时才更新配置。

Showcase 默认本地生成。`publish: public/private` 开启独立仓库发布，`pages: false` 关闭默认的适用静态演示。私有源码的站点也须核实访问范围，不能仅凭 `pages: true` 公开内容。后端保留本地完整流程；具体发布规则见[发布规范](skills/jd-interview-prep/references/github-workflow.md)。

## 验证

需要 Python 3.10+、Git；截图识别、联网核实和项目运行环境按任务提供。在项目根目录运行：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_preferences.py
.venv/bin/python scripts/validate_preferences.py config/preferences.example.yaml
.venv/bin/python -m unittest discover -s scripts/tests
python3 -m unittest discover -s skills/jd-interview-prep/scripts/tests
python3 -m unittest discover -s skills/bilingual-resume/scripts/tests
python3 scripts/check_public_tree.py
```

默认个人配置缺失会跳过；显式指定的文件缺失则报错。准备包校验器仅依赖标准库：

```sh
python3 skills/jd-interview-prep/scripts/validate_pack.py /absolute/path/to/pack
# 无项目追加 --no-project；非技术作品集使用 --portfolio，二者互斥。
```

简历渲染另需系统 Google Chrome：

```sh
.venv/bin/python -m pip install -r skills/bilingual-resume/scripts/requirements.txt
.venv/bin/python skills/bilingual-resume/scripts/render-pdf.py /absolute/path/to/resume.html /absolute/path/to/resume.pdf
```

PDF 须各一页 A4、文字可提取且视觉检查通过。结构校验不证明教学质量、项目实测或用户已掌握。

## 贡献

见[贡献指南](CONTRIBUTING.md)。个人配置、真实 JD、简历和产物留在本地；公开示例使用虚构资料。提交前审阅文件及历史，忽略规则和路径检查不能替代人工检查。

技能遵循 [Agent Skills 规范](https://agentskills.io/specification)，项目采用 [MIT](LICENSE)。
