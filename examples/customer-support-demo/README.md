# prompt-vcs 客服场景测试项目

这是一个离线示例，覆盖 Prompt 渲染、版本锁定与切换、YAML 测试、输出验证和 Python 单元测试。

示例不会调用真实 LLM，也不需要 API Key。`app.py` 输出中的“模拟模型响应”是固定测试数据，不能视为模型效果测试。

## 环境要求

- Windows PowerShell
- Python 3.10 或更高版本

首次运行时，在仓库根目录执行：

```powershell
python -m pip install -e ".[dev]"
```

这会以可编辑模式安装当前源码。

## 一条命令完成全部测试

在仓库根目录执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\examples\customer-support-demo\run_all.ps1
```

脚本依次运行示例应用、YAML 测试套件、Python 单元测试、回复验证和版本差异检查。任何一步失败都会停止并返回非零退出码。

成功时，脚本应报告 2 项 YAML 测试通过、3 项 Python 测试通过，并以 `All checks passed.` 结束。

## 分步运行

先进入样例目录：

```powershell
Set-Location .\examples\customer-support-demo
```

### 1. 运行应用

```powershell
python -X utf8 .\app.py
```

也可以传入自定义参数：

```powershell
python -X utf8 .\app.py --name "王女士" --issue "退款五天仍未到账" --tone "耐心" --channel "电话"
```

预期：打印当前版本的完整 Prompt、工单摘要和明确标注的固定模拟回复，命令退出码为 `0`。

### 2. 查看当前锁定版本

```powershell
python -X utf8 -m prompt_vcs.cli status --project .
```

预期：`support_reply` 和 `ticket_summary` 均锁定在 `v1`。

### 3. 运行 Prompt 测试

```powershell
python -X utf8 -m prompt_vcs.cli test .\tests\prompt_suite.yaml --project . --verbose
```

预期：共 `2` 项测试，`2` 项通过，失败和错误均为 `0`。

仅运行冒烟测试：

```powershell
python -X utf8 -m prompt_vcs.cli test .\tests\prompt_suite.yaml --project . --tag smoke
```

### 4. 运行 Python 单元测试

```powershell
python -m unittest discover -s .\tests -p "test_*.py" -v
```

预期：`Ran 3 tests`，最终显示 `OK`。测试在临时目录中分别锁定 `v1` 和 `v2`，不会修改样例自己的锁文件。

### 5. 验证一条模拟回复

```powershell
$mockResponse = (Get-Content -LiteralPath .\tests\mock_response.txt -Encoding UTF8 -Raw).Trim()
python -X utf8 -m prompt_vcs.cli validate support_reply $mockResponse --config .\tests\response_validation.yaml
```

预期：3 条验证规则全部显示 `✓`，最后显示 `All validation rules passed!`。

### 6. 对比两个版本

```powershell
python -X utf8 -m prompt_vcs.cli diff support_reply v1 v2 --project .
```

预期：显示统一差异，其中 `v2` 新增“工单优先级”和“不要提供密码或验证码”等约束。

### 7. 手动切换到 v2

```powershell
python -X utf8 -m prompt_vcs.cli switch support_reply v2 --project .
python -X utf8 -m prompt_vcs.cli switch ticket_summary v2 --project .
python -X utf8 .\app.py
```

预期：应用输出新增工单优先级和密码、验证码提醒。

测试完成后可恢复初始状态：

```powershell
python -X utf8 -m prompt_vcs.cli switch support_reply v1 --project .
python -X utf8 -m prompt_vcs.cli switch ticket_summary v1 --project .
```

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `app.py` | 最小业务程序，渲染两个 Prompt 并输出固定模拟回复 |
| `prompts.yaml` | `support_reply` 和 `ticket_summary` 的 v1/v2 定义 |
| `.prompt_lock.json` | 初始版本锁，两个 Prompt 均锁定为 v1 |
| `tests/prompt_suite.yaml` | `pvcs test` 使用的声明式测试套件 |
| `tests/response_validation.yaml` | `pvcs validate` 使用的输出验证规则 |
| `tests/mock_response.txt` | 一键脚本用于输出验证的 UTF-8 示例文本 |
| `tests/test_app.py` | 覆盖 v1、v2 和固定模拟响应的单元测试 |
| `run_all.ps1` | 一键运行全部检查 |

## 常见问题

如果出现 `No module named prompt_vcs`，说明当前仓库还没有安装，请回到仓库根目录执行：

```powershell
python -m pip install -e ".[dev]"
```

如果 PowerShell 阻止执行脚本，可继续使用文档中的分步命令，或者仅对本次命令使用前文的 `-ExecutionPolicy Bypass`。

如果测试显示 `Prompt ... is locked to missing version`，请检查 `.prompt_lock.json` 中的版本是否确实存在于 `prompts.yaml`。
