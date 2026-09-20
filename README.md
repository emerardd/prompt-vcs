# prompt-vcs

[![PyPI version](https://img.shields.io/pypi/v/prompt-vcs.svg)](https://pypi.org/project/prompt-vcs/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

Git-native prompt management for Python applications. Keep prompts in code or YAML, pin production versions with a lockfile, and review every change through Git. No database or hosted service is required.

[中文文档](README.zh-CN.md)

## Why prompt-vcs

- Code-first workflow with `p()` and `@prompt`.
- Single-file `prompts.yaml` by default, with a split-file mode for larger projects.
- Explicit version pinning through `.prompt_lock.json`; invalid or missing locked versions fail instead of silently falling back.
- CLI support for extraction, migration, version switching, history, testing, validation, A/B experiments, and export.
- Typed Python API, Jinja sandboxing, atomic state writes, and automatic cache refresh after file changes.

## Install

```bash
pip install prompt-vcs
```

Optional dependencies:

```bash
pip install "prompt-vcs[validation]"  # JSON Schema validation
pip install "prompt-vcs[analysis]"    # Welch's t-test for small A/B samples
```

prompt-vcs requires Python 3.10 or newer.

## Quick start

Initialize a project:

```bash
pvcs init
```

Use a prompt directly in Python:

```python
from prompt_vcs import p

message = p("user_greeting", "Hello {name}", name="Ada")
```

The string in code is the development default. To manage versions in YAML, add them to `prompts.yaml`:

```yaml
user_greeting:
  description: Greeting shown to a signed-in user
  versions:
    v1:
      template: "Hello {{ name }}"
    v2:
      template: "Welcome back, {{ name }}"
```

Pin a version and inspect the result:

```bash
pvcs switch user_greeting v2
pvcs status
pvcs diff user_greeting v1 v2
```

`pvcs switch` records the selected version in `.prompt_lock.json`. Commit that file with `prompts.yaml` so the application and its prompt versions move through Git together.

For prompts already stored in YAML, the code can omit the default string:

```python
message = p("user_greeting", name="Ada")
```

## Storage modes

The default single-file layout keeps the project compact:

```text
your-project/
|-- .prompt_lock.json
|-- prompts.yaml
`-- src/
```

For a larger prompt collection, use `pvcs init --split` to store versions under `prompts/<id>/<version>.yaml`.

## Main workflows

| Workflow | Commands |
| --- | --- |
| Create and inspect | `init`, `list`, `status`, `add`, `delete` |
| Extract or migrate | `scaffold`, `migrate`, `migrate --clean` |
| Control versions | `switch`, `unlock`, `diff`, `log` |
| Test outputs | `test`, `validate` |
| Run experiments | `ab create`, `ab record`, `ab status`, `ab analyze` |
| Integrate elsewhere | `export --format json`, `openai`, or `langchain` |

Run `pvcs --help` or `pvcs <command> --help` for all options.

Prompt tests render templates and apply deterministic assertions. Output validation supports substring, regex, length, JSON Schema, and custom rules. A/B experiments select prompt variants and store application-provided scores. These tools do not call an LLM or judge model quality on their own.

See [Validation and testing](docs/VALIDATION_TESTING.md) for configuration examples.

## Existing codebases

Preview an automatic migration before changing source files:

```bash
pvcs migrate src/ --dry-run
```

Then apply changes interactively or without prompts:

```bash
pvcs migrate src/
pvcs migrate src/ --yes
```

Use `--clean` to move templates into YAML and leave only prompt IDs and variables in code. Migration is implemented with LibCST so Python syntax and formatting remain structured.

## Offline example

The repository includes a customer-support example covering rendering, version switching, YAML test suites, output validation, and Python tests without an API key:

```powershell
python -m pip install -e ".[dev]"
powershell -ExecutionPolicy Bypass -File .\examples\customer-support-demo\run_all.ps1
```

See the [example walkthrough](examples/customer-support-demo/README.md) for the files, commands, and expected output.

## Development

```bash
python -m pip install -e ".[dev]"
npm --prefix vscode-extension ci
python scripts/verify.py --quick
```

Use `python scripts/verify.py` for the full local suite or `python scripts/verify.py --release` to also build and smoke-test distribution artifacts.

## License

[MIT](LICENSE)
