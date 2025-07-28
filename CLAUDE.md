# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Focus

This repository contains Ansible collections under the `o0_o` namespace. Current development focuses on four collections:
- **posix**: Cross-platform utilities with raw fallback support
- **controller**: Ansible controller management
- **inventory**: Inventory and connection management
- **connection**: Connection plugins and utilities

Directories ending in `.wip` are legacy and should be ignored for style reference. However, older Ansible work throughout the repository contains creative automation solutions worth mining for ideas, though it's generally overly complicated due to earlier avoidance of custom modules and plugins.

## Testing Commands

**Individual Collection Testing:**
```bash
# Navigate to collection directory first
cd posix/  # or controller/, inventory/, connection/

# Run all test types
ansible-test sanity --venv
ansible-test units --venv
ansible-test integration --venv
```

**Bulk Testing (Recommended):**
```bash
# Use the ./test.sh script for parallel testing across collections
./test.sh controller inventory posix connection  # All collections
./test.sh posix controller                       # Specific collections
```

**Always validate changes:** Run tests before committing to ensure no regressions.

## Code Style Standards

### File Headers

**Python files must use this exact header:**
```python
# vim: ts=4:sw=4:sts=4:et:ft=python
# -*- mode: python; tab-width: 4; indent-tabs-mode: nil; -*-
#
# GNU General Public License v3.0+
# SPDX-License-Identifier: GPL-3.0-or-later
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Copyright (c) 2025 oØ.o (@o0-o)
#
# This file is part of the o0_o.<collection_name> Ansible Collection.
```

**YAML files must use this exact header:**
```yaml
# vim: ts=2:sw=2:sts=2:et:ft=yaml.ansible
# -*- mode: yaml; yaml-indent-offset: 2; indent-tabs-mode: nil; -*-
---
# GNU General Public License v3.0+
# SPDX-License-Identifier: GPL-3.0-or-later
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Copyright (c) 2025 oØ.o (@o0-o)
#
# This file is part of the o0_o.<collection_name> Ansible Collection.
```

### PEP 8 Compliance

**We use black and flake8 to enforce PEP 8 compliance:**

1. **First, auto-format with black:**
   ```bash
   # From collection directory
   git ls-files | grep "\.py$" | xargs black
   ```

2. **Then check for remaining issues with flake8:**
   ```bash
   git ls-files | grep "\.py$" | xargs flake8
   ```

3. **Manually fix any flake8 issues that black cannot handle**

**Configuration:**
- **Line length**: 79 characters (enforced by black and flake8)
- **Doc/comment length**: 72 characters (enforced by flake8)
- **E402 (imports)**: Ignored for module files only (see setup.cfg)
- **Indentation**: 4 spaces for Python, 2 spaces for YAML
- **Use `from __future__ import annotations` for type hint support**

### String Quoting Standards

**Python:** Black automatically handles string quoting preferences (generally prefers double quotes).

**YAML:** Prefer single quotes for plain strings:
```yaml
# Single quotes for plain strings (preferred)
greeting: 'Hello world'
fail_msg: 'Simple error message'

# Double quotes for special cases (YAML requirement)
content: "Multi-line\nwith escapes"  # Escape sequences need double quotes in YAML
template_var: "{{ jinja_expression }}"  # Jinja2 expressions
apostrophe: "Can't process this"  # Contains single quote
```

**Prefer {} instead of dict():**
```python
# Correct
argument_spec = {
    "gather_subset": {
        "type": "list", 
        "elements": "str",
        "default": ["all"],
        "choices": [
            "all", "kernel", "arch",
            "!all", "!kernel", "!arch"
        ]
    }
}

result.update({
    "skipped": True,
    "skip_reason": "This does not appear to be a POSIX system.",
    "ansible_facts": {}
})

# Incorrect
argument_spec = dict(
    gather_subset=dict(  # Wrong - use {}
        type="list",
        elements="str"
    )
)

# Exception
foo = dict(bar)  # Converting to dict is valid
```

### Bracket vs Dot Notation

**ALWAYS prefer bracket notation over dot notation for dictionary/object value access:**

```python
# Correct
kernel_name = un_s["stdout_lines"][0]
facts = result.get("ansible_facts", {})  # Getters are fine
os_facts = ansible_facts.get("o0_os", {}).copy()  # Methods are fine

# Incorrect
kernel_name = un_s.stdout_lines[0]  # Wrong!
```

**Use dot notation only for object attributes:**
```python
# Correct
self._display.vvv(message)
self._task.check_mode
task.args.clear()
```

### Type Hints and Documentation

**All code must include comprehensive type hints and reST-style docstrings:**

```python
def method_name(self, param1: str, param2: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Short description of method purpose.

    Longer description explaining behavior, side effects, and context.

    :param str param1: Description of the parameter
    :param Optional[Dict[str, Any]] param2: Description with default info
    :returns Dict[str, Any]: Description of return value structure
    :raises AnsibleActionFail: When and why this exception occurs

    .. note::
        Important implementation details or warnings
    """
```

**Standards:**
- Method signatures: Full type annotations (Optional, Dict, List, etc.)
- Return types: Always specify return type annotations
- Docstrings: Include parameters, return values, exceptions
- Unit tests: Full type hints but brief descriptive docstrings only
- Variable naming: Use `result` (not `results`), `task_vars` (not `variables`)

## Action Plugins

### Class variables/attributes

**All action plugins must define the following at the class level:**

```python
TRANSFERS_FILES  # does this plugin transfer a file from controller to host?
_requires_connection  # only false if all operations are on the controller
_supports_check_mode  # usually true if any check_mode operations are present
_supports_diff  # true if using writing to text-based files
_supports_async  # usually false unless explicitly set to True
```

None of these should be set within class methods.

If \_supports\_async is False, no async-related operations should be in class methods.


## Testing Standards

### Unit Test Structure

**Use pytest with consistent fixture patterns:**
```python
@pytest.fixture
def plugin(base):
    '''
    Create an ActionModule instance with patched dependencies from the
    shared `base` fixture for testing purposes.
    '''

def test_get_kernel_and_hardware_success(monkeypatch, plugin):
    '''
    Test successful gathering of POSIX kernel and hardware facts using `uname`.
    '''

@pytest.mark.parametrize('subset,expect_os,expect_hw', [
    (['all'], True, True),
    (['kernel'], True, False),
    (['arch'], False, True),
    (['!kernel'], False, True),
])
def test_run_subset_selection(monkeypatch, plugin, subset, expect_os, expect_hw):
    '''
    Test gather_subset filtering and resulting fact inclusion logic.
    '''
```

### Integration Test Structure

**Use YAML with proper task organization:**
```yaml
- name: Run success tests
  ansible.builtin.include_tasks: facts.yml
  loop:
    - true
    - false
  vars:
    ansible_check_mode: '{{ item }}'
```

### Variable Naming Conventions

**ALL Ansible code (not just integration tests) must follow these variable naming standards:**

#### Registered Variables
**ALWAYS use descriptive names with `_reg` suffix:**
```yaml
# Correct
- name: Run command with argv
  o0_o.posix.command:
    argv: [echo, foo]
  register: command_argv_reg

- name: Slurp file content
  o0_o.posix.slurp64:
    src: /path/to/file
  register: slurp_content_reg

- name: Template rendering
  o0_o.posix.template:
    src: hello.j2
    dest: /tmp/hello.txt
  register: template_render_reg

# Incorrect - generic names
- name: Run command
  o0_o.posix.command:
    argv: [echo, foo]
  register: result  # Too generic

- name: Slurp file
  slurp:
    src: /path/to/file
  register: reg     # Too generic
```

#### Variable Declarations
**Use descriptive names with `_var` suffix for declared variables:**
```yaml
# Correct
vars:
  greeting_var: 'Hello world'
  files_dir_var: "{{ playbook_dir }}/files"
  timeout_seconds_var: 30

# Acceptable for well-established patterns
vars:
  dest_path: /tmp/output
  src_file: input.txt
```

#### Facts Access
**Use direct fact access instead of registered variable indirection:**
```yaml
# Correct - direct access
- name: Assert kernel is Linux
  assert:
    that:
      - o0_os['kernel']['name'] == 'Linux'

# Incorrect - unnecessary indirection
- name: Gather facts
  o0_o.posix.facts:
  register: facts_result_reg

- name: Assert kernel is Linux
  assert:
    that:
      - facts_result_reg['ansible_facts']['o0_os']['kernel']['name'] == 'Linux'
```

#### Variable References
**Use bracket notation consistently:**
```yaml
# Correct
- name: Assert command succeeded
  assert:
    that:
      - command_result_reg['rc'] == 0
      - command_result_reg['stdout'] | length > 0
      - "'success' in command_result_reg['stdout']"

# Incorrect - dot notation
- name: Assert command succeeded
  assert:
    that:
      - command_result_reg.rc == 0  # Wrong!
```

### Failure Testing Standards

**ALWAYS use block/rescue pattern for testing expected failures:**

```yaml
# Preferred approach
- name: 'Fail: Test expected error condition'
  block:

    - name: Run operation that should fail
      module_name:
        invalid_param: value

  rescue:

    - name: Assert failure occurred as expected
      ansible.builtin.assert:
        that:
          - "'expected error' in ansible_failed_result.msg"
```

**DO NOT use ignore_errors for failure testing:**
```yaml
# Incorrect approach - avoid this pattern
- name: Test that should fail
  module_name:
    invalid_param: value
  ignore_errors: true
  register: result

- name: Assert failure
  assert:
    that:
      - result is failed
```

**Exception: ignore_errors is acceptable for version compatibility testing where operations might legitimately succeed or fail based on Ansible version.**

### Integration Test Best Practices

#### Directory Structure
**Follow standard Ansible integration test layout:**
```
tests/integration/targets/<module_name>/
├── tasks/
│   ├── main.yml         # Entry point with test orchestration
│   ├── test_success.yml # Success case tests
│   ├── test_failures.yml# Failure case tests  
│   └── cleanup.yml      # Cleanup operations
├── files/               # Static test files (NOT in tasks/)
│   ├── input.txt
│   └── expected.txt
├── templates/           # Jinja2 templates (NOT in tasks/)
│   └── test_template.j2
└── vars/
    └── main.yml         # Test-specific variables
```

**IMPORTANT:** `files/` and `templates/` directories must be siblings of `tasks/`, not subdirectories within `tasks/`.

#### Test Organization
**Structure integration tests with proper variable scoping:**
```yaml
# main.yml - Test orchestration
- name: Create temporary directory for integration tests
  ansible.builtin.tempfile:
    state: directory
    suffix: module_test
  register: test_tmpdir_reg

- name: Set test directory fact
  ansible.builtin.set_fact:
    test_dir_var: "{{ test_tmpdir_reg.path }}"

- name: Try
  block:

    - name: Run test set with permutations
      ansible.builtin.include_tasks: "{{ item[0] }}"
      loop: "{{ test_sets | product(loop_list) }}"
      vars:
        test_sets:
          - test_success.yml
          - test_failures.yml
        loop_list: "{{ [true, false] | product([true, false]) }}"
        _force_raw: "{{ item[1][0] }}"
        ansible_check_mode: "{{ item[1][1] }}"

  always:

    - name: Clean up temporary test directory
      ansible.builtin.file:
        path: "{{ test_dir_var }}"
        state: absent
```

#### Template Variable Consolidation
**Follow DRY principles - define repeated variables centrally:**
```yaml
# Correct - centralized variable definition
- name: Run template tests
  ansible.builtin.include_tasks: template_test.yml
  vars:
    greeting_var: 'Hello world'
    template_dir_var: "{{ playbook_dir }}/targets/template/templates"

# Incorrect - repeated variable definitions
# template_test.yml would have:
# vars:
#   greeting_var: 'Hello world'  # Repeated in every task file
```

#### File References
**Use consistent directory variables:**
```yaml
# In main.yml
- name: Set directories
  ansible.builtin.set_fact:
    files_dir_var: "{{ playbook_dir }}/targets/{{ ansible_role_name }}/files"
    templates_dir_var: "{{ playbook_dir }}/targets/{{ ansible_role_name }}/templates"

# In task files
- name: Copy test file
  ansible.builtin.copy:
    src: "{{ files_dir_var }}/input.txt"
    dest: "{{ test_dir_var }}/input.txt"

- name: Validate against expected output
  vars:
    expected_content: "{{ lookup('file', files_dir_var + '/expected.txt') }}"
  ansible.builtin.assert:
    that:
      - actual_content == expected_content
```

#### Loop Control
**Avoid variable name collisions in loops:**
```yaml
# Correct - specify loop_var to avoid conflicts
- name: Run tests with different parameters
  ansible.builtin.include_tasks: single_test.yml
  loop: "{{ test_parameters }}"
  loop_control:
    loop_var: test_param    # Avoid conflict with ansible_check_mode
  vars:
    test_value: "{{ test_param }}"

# Incorrect - can cause variable collisions
- name: Run tests
  ansible.builtin.include_tasks: single_test.yml
  loop: "{{ test_parameters }}"
  # Missing loop_control can cause ansible_check_mode conflicts
```

## Plugin Development Patterns

### Class Structure
```python
class ActionModule(PosixBase):
    '''Brief description of the plugin\'s purpose'''

    TRANSFERS_FILES = False
    _requires_connection = False
    _supports_check_mode = True
    _supports_async = False
```

### Argument Validation
```python
argument_spec = {
    "gather_subset": {
        "type": "list",
        "elements": "str",
        "default": ["all"],
        "choices": [
            "all", "kernel", "arch",
            "!all", "!kernel", "!arch"
        ]
    }
}

validation_result, new_module_args = self.validate_argument_spec(
    argument_spec=argument_spec
)
```

### Error Handling
```python
try:
    result = self._execute_action(task_vars=task_vars)
except AnsibleConnectionFailure:
    raise  # Re-raise connection failures
except Exception as e:
    self._display.vvv(
        f"Operation failed: {type(e).__name__}: {e}"
    )
    result.update({
        "failed": True,
        "msg": f"Error during execution: {e}"
    })
    return result
```

### Dictionary Operations
```python
# Always use bracket notation and {}
result.update({
    "skipped": True,
    "skip_reason": "This does not appear to be a POSIX system.",
    "ansible_facts": {}
})

# Prefer .get() with defaults
facts = result.get("ansible_facts", {})
config = task_vars.get("hostvars", {}).get(inventory_hostname, {})
```

## Module Documentation

**All modules must include comprehensive DOCUMENTATION:**
```python
DOCUMENTATION = r'''
---
module: facts
short_description: Gather POSIX facts from the managed host
version_added: "1.1.0"
description:
  - Collects minimal OS and hardware facts from POSIX-compatible remote hosts.
  - Uses raw shell commands like C(uname) to gather kernel name, version,
    and CPU architecture.
  - Does not require Python on the managed host.
options:
  gather_subset:
    description:
      - Specify which fact subsets to gather.
    type: list
    elements: str
    default: ['all']
    choices: ['all', 'kernel', 'arch', '!all', '!kernel', '!arch']
'''
```

## Release Management

### Changelogs
Use Ansible changelog format following Keep a Changelog conventions:

```yaml
# changelog.yml
releases:
  1.3.0:
    release_date: '2025-01-15'
    changes:
      major_changes:
        - Added raw fallback support for systems without Python
      minor_changes:
        - Enhanced error handling in connection plugins
      bugfixes:
        - Fixed regex compilation issue in lineinfile_dedupe
      breaking_changes:
        - Removed deprecated legacy_mode parameter
```

### Git Workflow

**Branch Strategy:**
- `main`: Stable release branch  
- `formatting-consistency`: Active development branch for style improvements
- Feature branches: For specific enhancements or fixes

**Commit Standards:**
```bash
# Descriptive messages with attribution
git commit -m "$(cat <<'EOF'
Brief summary of changes

Detailed description of what was changed and why.
Include validation that tests pass.

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Git Tagging
Use semantic versioning with v prefix:
```bash
git tag -a v1.3.1 -m 'Release v1.3.1 - Description of changes'
git tag -a v1.0.1 -m 'Release v1.0.1 - Description of changes'
```

### README Structure
All collection READMEs must follow this rigid structure:

```markdown
# o0_o.<collection_name>

Brief description and purpose.

## Overview

Detailed description of the collection's functionality and key features.

## Installation

```bash
ansible-galaxy collection install o0_o.<collection_name>
```

## Dependencies

List required collections and external dependencies.

## Usage

### Basic Examples
Provide simple, practical examples.

### Advanced Usage
More complex examples and patterns.

## Plugins

### Action Plugins
List and describe each plugin.

### Modules
List and describe each module.

### Roles
List and describe each role (if applicable).

## Development & Testing

```bash
ansible-test sanity --venv
ansible-test units --venv
ansible-test integration --venv
```

## License

Licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.txt) or later (GPLv3+)
```

## Architecture Notes

### Base Classes
- Extend `PosixBase` for action plugins requiring raw fallback
- Use `self._display.vvv()` for verbose logging
- Always implement proper check mode support

### Connection Handling
- Support multiple connection types (ssh, network_cli, local)
- Implement graceful fallbacks for systems without Python
- Test connection capabilities before complex operations

### Collections Interdependencies
- `posix` provides base utilities used by other collections
- `inventory` and `connection` work together for host management
- `controller` manages Ansible infrastructure itself

When making changes, ensure consistency with these established patterns and always include comprehensive tests and documentation.
