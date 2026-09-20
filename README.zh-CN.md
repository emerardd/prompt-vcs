# prompt-vcs

[![PyPI version](https://img.shields.io/pypi/v/prompt-vcs.svg)](https://pypi.org/project/prompt-vcs/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

面向 Python 应用的 Git 原生 Prompt 管理工具。你可以在代码或 YAML 中维护 Prompt，通过 lockfile 固定生产版本，并使用 Git 审查每次变更；无需数据库或托管服务。

[English](README.md)

## 为什么使用 prompt-vcs

- 使用 `p()` 和 `@prompt`，保持代码优先的开发方式。
- 默认采用单个 `prompts.yaml`，大型项目也可切换为多文件模式。
- 通过 `.prompt_lock.json` 显式锁定版本；锁定版本缺失或配置损坏时直接失败，不静默回退。
- CLI 覆盖提取、迁移、版本切换、历史查看、测试、验证、A/B 实验和导出。
- 提供完整类型标注、Jinja 沙箱、原子状态写入和文件变化后的缓存刷新。

## 安装

```bash
pip install prompt-vcs
```

可选依赖：

```bash
pip install "prompt-vcs[validation]"  # JSON Schema 验证
pip install "prompt-vcs[analysis]"    # 小样本 A/B 实验的 Welch t 检验
```

prompt-vcs 需要 Python 3.10 或更高版本。

## 快速开始

初始化项目：

```bash
pvcs init
```

直接在 Python 中使用 Prompt：

```python
from prompt_vcs import p

message = p("user_greeting", "你好，{name}", name="小林")
```

代码中的字符串是开发默认值。需要在 YAML 中管理版本时，将版本写入 `prompts.yaml`：

```yaml
user_greeting:
  description: 用户登录后显示的问候语
  versions:
    v1:
      template: "你好，{{ name }}"
    v2:
      template: "欢迎回来，{{ name }}"
```

锁定版本并查看结果：

```bash
pvcs switch user_greeting v2
pvcs status
pvcs diff user_greeting v1 v2
```

`pvcs switch` 会把选择的版本写入 `.prompt_lock.json`。将它与 `prompts.yaml` 一同提交，应用代码和 Prompt 版本就能通过 Git 同步演进。

如果 Prompt 已经保存在 YAML 中，代码可以省略默认字符串：

```python
message = p("user_greeting", name="小林")
```

## 存储模式

默认的单文件布局适合大多数项目：

```text
your-project/
|-- .prompt_lock.json
|-- prompts.yaml
`-- src/
```

Prompt 数量较多时，可使用 `pvcs init --split`，将版本分别存放在 `prompts/<id>/<version>.yaml` 中。

## 主要工作流

| 工作流 | 命令 |
| --- | --- |
| 创建与查看 | `init`、`list`、`status`、`add`、`delete` |
| 提取与迁移 | `scaffold`、`migrate`、`migrate --clean` |
| 版本控制 | `switch`、`unlock`、`diff`、`log` |
| 测试输出 | `test`、`validate` |
| 运行实验 | `ab create`、`ab record`、`ab status`、`ab analyze` |
| 对接其他工具 | `export --format json`、`openai` 或 `langchain` |

使用 `pvcs --help` 或 `pvcs <command> --help` 查看完整参数。

Prompt 测试会渲染模板并执行确定性的断言；输出验证支持子字符串、正则、长度、JSON Schema 和自定义规则；A/B 实验负责选择版本并保存业务侧提供的评分。这些工具本身不会调用 LLM，也不会自动判断模型质量。

配置示例见[验证与测试文档](docs/VALIDATION_TESTING.md)。

## 迁移现有项目

修改源码前先预览自动迁移结果：

```bash
pvcs migrate src/ --dry-run
```

确认后可交互式应用，或一次性应用全部修改：

```bash
pvcs migrate src/
pvcs migrate src/ --yes
```

使用 `--clean` 可将模板移入 YAML，代码中只保留 Prompt ID 和变量。迁移基于 LibCST 实现，以结构化方式保留 Python 语法和格式。

## 离线示例

仓库内置一个无需 API Key 的客服场景示例，覆盖 Prompt 渲染、版本切换、YAML 测试套件、输出验证和 Python 测试：

```powershell
python -m pip install -e ".[dev]"
powershell -ExecutionPolicy Bypass -File .\examples\customer-support-demo\run_all.ps1
```

文件说明、分步命令和预期输出见[示例指南](examples/customer-support-demo/README.md)。

## 开发与验证

```bash
python -m pip install -e ".[dev]"
npm --prefix vscode-extension ci
python scripts/verify.py --quick
```

使用 `python scripts/verify.py` 运行完整本地检查；使用 `python scripts/verify.py --release` 额外构建并冒烟测试发布产物。

## 许可证

[MIT](LICENSE)
