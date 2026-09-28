# Validation and testing

`pvcs test` renders stored prompts with supplied inputs and checks the resulting text. `pvcs validate` checks text supplied on the command line. Both use deterministic rules; neither calls an LLM or measures model quality.

## Run the repository examples

From the repository root, install the package and run the test suite against the root `prompts.yaml`:

```bash
python -m pip install -e .
pvcs test examples/working_test_suite.yaml --project .
pvcs test examples/working_test_suite.yaml --project . --tag smoke
```

To validate supplied text, create a YAML file with a `validation` list:

```yaml
validation:
  - type: contains
    name: has_greeting
    substring: Hello
  - type: length
    min_length: 5
    max_length: 100
```

```bash
pvcs validate user_greeting "Hello, Alice!" --config validation.yaml
```

The `prompt_id` labels the validation report; this command checks the supplied output, not a freshly rendered prompt. The separate [`examples/validation_config.yaml`](../examples/validation_config.yaml) demonstrates more rules, including an email pattern; use matching output when running it.

## Define a test suite

Save test cases under `tests` in a YAML file:

```yaml
name: Greeting tests
tests:
  - prompt_id: user_greeting
    name: greeting_contains_name
    inputs:
      name: Alice
    validation:
      - type: contains
        substring: Alice
  - prompt_id: simple_greeting
    name: exact_greeting
    expected_output: "你好，欢迎使用系统！"
    tags: [smoke]
```

Use `--project` when the prompt project is outside the current directory. Use `--verbose` for rendered output and `--tag smoke` to select tagged cases. A case can also set `skip: true` and `skip_reason`.

## Available rules

| Type | Required fields | Purpose |
| --- | --- | --- |
| `contains` | `substring` | Check for a substring |
| `regex` | `pattern` | Search with a regular expression |
| `length` | `min_length` and/or `max_length` | Bound the character count |
| `json_schema` | `schema` | Check JSON output against a schema |

Rules can also set `name` and `error_message`. Install `prompt-vcs[validation]` to use `json_schema`. Python callers can add a `ValidationType.CUSTOM` rule with a `custom_validator` function; YAML rule loading does not support custom functions.

```python
from prompt_vcs import PromptValidator, ValidationRule, ValidationType

validator = PromptValidator()
validator.add_rule(ValidationRule(
    rule_type=ValidationType.CUSTOM,
    name="nonempty",
    custom_validator=lambda output: bool(output.strip()),
))
results = validator.validate("Hello, Alice!")
assert all(result.passed for result in results)
```

For an end-to-end offline project with its own prompts, tests and output validation, see the [customer-support example](../examples/customer-support-demo/README.md).
