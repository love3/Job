# Job 工作区

路径相对本目录；`skills/` 是技能唯一源码。公共说明使用中文，配置键与代码标识符保留英文。

## 任务入口

| 任务 | 先读 | 默认输出 |
| --- | --- | --- |
| 面试准备 | [JD/AGENTS.md](JD/AGENTS.md) | `JD/preparations/<case-id>/` |
| 简历 | [Resume/AGENTS.md](Resume/AGENTS.md) | `Resume/variants/<case-id>/` |

完整 JD 默认先准备面试，再按同一 case-id 交接简历。只准备面试或 `resume.enabled: false` 跳过交接；不要项目只取消项目。缺履历时先完成面试资料，再补真实经历。

## 设置与续作

存在 `config/preferences.yaml` 时，使用已安装 `requirements-dev.txt` 的 Python 校验并读取；依赖命令见 [README](README.md#验证)。示例文件不生效，配置路径相对项目根目录。

- 新任务：本次要求 > 个人偏好 > 技能默认。
- 续作：本次要求 > 原任务确认设置与手改 > 个人偏好 > 默认。先读 `meta/progress.md` 或 `changes.md`，只改本次范围。
- 仅明确要求保存偏好时更新 YAML；错误设置明确指出，不静默忽略。设置含义见配置模板及相应技能。
- 独立技能只用明确提供或工作区已加载的资料，不从安装位置搜索个人文件。

## 边界与验证

真实经历只从来源正文和用户确认取得，不另建事实库；base 与原始参考默认只读。个人配置、准备包和简历留在本地，作品按明确授权独立发布。

按 [README](README.md#验证) 检查；修改技能遵循[贡献指南](CONTRIBUTING.md)。测试使用临时虚构资料并清理，不生成正式包、改真实 base 或顺带发布远程项目。
