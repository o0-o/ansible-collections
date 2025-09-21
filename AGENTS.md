# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

**IMPORTANT:** The directory structure has multiple Git repositories:

1. **Parent directory** (`/Users/o0-o/.ansible/collections/ansible_collections/o0_o/`):
   - Has its own Git repository for tracking shared files like AGENTS.md/CLAUDE.md
   - **NEVER add collection content to this repository**
   - Only for cross-collection documentation and configuration

2. **Each collection** is its own independent Git repository:
   - `posix/` - separate Git repository
   - `controller/` - separate Git repository
   - `inventory/` - separate Git repository
   - `connection/` - separate Git repository

**To work with a collection, you must cd into it first:**
```bash
cd posix/     # Enter the posix collection repository
git status    # Now operates on the posix repository

cd ../controller/  # Switch to controller collection repository
git status        # Now operates on the controller repository

cd ..         # Back to parent (only for AGENTS.md, etc.)
git status    # Now operates on the parent repository
```

**CRITICAL:** Never commit collection code to the parent repository. Each collection manages its own code, tests, and documentation.

Current development focuses on the following collections:
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
ansible-test integration --venv
yamllint .  # catches additional formatting issues
```

**Always validate changes:** Run tests before committing to ensure no regressions.
**Never run `pytest` directly, use `ansible-test`**

## GitHub Pages & Docs Reference

- Enable Pages for a collection repo with the GitHub CLI once:
  ```bash
  gh api --method POST \
    -H 'Accept: application/vnd.github+json' \
    /repos/<owner>/<repo>/pages \
    -f build_type=workflow
  ```
  Replace `<owner>/<repo>` as needed.
- For future collections, copy the `utils/` setup when wiring
  `antsibull-docs`, `antsibull-changelog`, and publishing workflows.

## Antsibull Docs & Changelog Standards

- Every collection must ship the same docs layout as `utils/` and `posix/`:
  `docs/requirements.txt`, `docs/source/` with `antsibull-docs.cfg`, `conf.py`,
  `index.rst`, and a `docs/tools/prebuild.sh` helper that populates
  `docs/source/generated/` via `antsibull-docs` before we run Sphinx.
- GitHub Pages workflows should match the pattern in `utils/.github/workflows/docs.yml`:
  run the prebuild script, call `sphinx-build`, upload the `site/` directory, and
  only trigger on version tags unless the collection explicitly needs branch
  previews.
- Changelogs must be managed through `antsibull-changelog` using
  `changelogs/config.yaml`, `changelogs/changelog.yaml`, and fragments under
  `changelogs/fragments/`. Treat fragments as temporary scratch files—create them
  for each notable change, run
  `antsibull-changelog release --version <next>` when preparing a release, then
  let the tool consume the fragments. **Never hand-edit `changelogs/changelog.yaml`
  or `CHANGELOG.rst`.**
- Add collection-specific README notes reminding contributors that CI runs
  `black`, `flake8`, and `yamllint` before the build, so lint failures will block
  the workflow.


## Code Style Standards

### EOF

**Always end files with a newline character (`\n`)!**

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

### Code Style and Linting

**Always rely on automatic formatting first, then check for remaining issues:**

#### Python (PEP 8 Compliance)

1. **ALWAYS run black first for automatic formatting:**
   ```bash
   # From collection directory
   git ls-files | grep "\.py$" | xargs black
   ```

   **Benefits of black:**
   - Consistent formatting across all code
   - No debates about style choices
   - Handles most PEP 8 requirements automatically
   - Saves time on manual formatting
   - Use it liberally - run it often!

2. **Then check for remaining issues with flake8:**
   ```bash
   git ls-files | grep "\.py$" | xargs flake8
   ```

3. **Only manually fix what black cannot handle:**
   - Long docstrings (W505) - break at 72 characters
   - Complex line length issues black couldn't resolve
   - Import order issues in special cases

#### YAML Formatting

4. **Check YAML files with yamllint:**
   ```bash
   yamllint .
   ```

   **Common yamllint fixes:**
   - Line length (79 characters) - use multiline Jinja2 format
   - Indentation issues (2 spaces for YAML)
   - Missing document start (`---`)
   - Trailing spaces

**Complete workflow:**
```bash
# From collection directory
black .                                      # Auto-format Python
git ls-files | grep "\.py$" | xargs flake8  # Check Python issues
yamllint .                                   # Check YAML issues
# Fix only the remaining issues manually
```

**Configuration:**
- **Python line length**: 79 characters (enforced by black and flake8)
- **YAML line length**: 79 characters (enforced by yamllint)
- **Doc/comment length**: 72 characters (enforced by flake8)
- **E402 (imports)**: Ignored for module files only (see pyproject.toml)
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

**Long Jinja2 expressions in YAML:** Use proper multiline format to stay under 79 characters:
```yaml
# Correct - using >- for folded scalar with opening {{ on same line
- name: Parse fstab content
  ansible.builtin.set_fact:
    fstab_parsed: >-
      {{ fstab_content_reg['content']
         | b64decode
         | o0_o.posix.fstab }}

# Also correct - for complex expressions with multiple filters
- name: Find root mount
  ansible.builtin.set_fact:
    root_mount: >-
      {{ mount_parsed
         | selectattr('mount', 'equalto', '/')
         | first }}

# For conditionals in when clauses
- name: Assert long hostname exists
  ansible.builtin.assert:
    that:
      - o0_os['hostname']['long'] is defined
  when: >-
    '.' in parsed_default['hostname'].get('long',
                                           parsed_default['hostname']['short'])

# Incorrect - line too long
- name: Parse fstab content
  ansible.builtin.set_fact:
    fstab_parsed: "{{ fstab_content_reg['content'] | b64decode | o0_o.posix.fstab }}"
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

**ALWAYS use bracket notation for dictionary access in both Python AND Ansible/YAML:**

**Python:**
```python
# Correct - bracket notation for dict access
kernel_name = un_s["stdout_lines"][0]
facts = result.get("ansible_facts", {})  # Getters are fine
os_facts = ansible_facts.get("o0_os", {}).copy()  # Methods are fine

# Incorrect - never use dot notation for dicts
kernel_name = un_s.stdout_lines[0]  # Wrong!
```

**Ansible/YAML - This is CRITICAL:**
```yaml
# Correct - ALWAYS use brackets in Jinja2 expressions
- name: Check command result
  ansible.builtin.assert:
    that:
      - command_result_reg['rc'] == 0
      - command_result_reg['stdout'] is defined
      - "'success' in command_result_reg['stdout']"

- name: Use slurped content
  ansible.builtin.set_fact:
    decoded: "{{ slurp_result_reg['content'] | b64decode }}"

- name: Access ansible_failed_result
  rescue:
    - ansible.builtin.assert:
        that:
          - "'expected error' in ansible_failed_result['msg']"

# Incorrect - NEVER use dot notation in Ansible
- name: Wrong way to check
  ansible.builtin.assert:
    that:
      - command_result_reg.rc == 0  # WRONG!
      - slurp_result.content is defined  # WRONG!
      - ansible_failed_result.msg  # WRONG!
```

**Why this matters:**
- Dot notation can break with special characters in keys
- Bracket notation is consistent between Python and Jinja2
- Bracket notation makes it clear you're accessing a dictionary, not an object attribute

**Use dot notation ONLY for actual object attributes/methods:**
```python
# Correct - these are object attributes, not dict keys
self._display.vvv(message)
self._task.check_mode
task.args.clear()
```

### Type Hints and Documentation

**ALWAYS include docstrings - no exceptions:**

**For complex methods - full reST-style documentation:**
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

**For test methods and simple functions - brief docstrings:**
```python
def test_mount_parser_with_spaces():
    """Test that mount parser handles paths with spaces correctly."""
    # No need for :param:, :returns:, etc. for test methods

def get_mount_point(path: str) -> str:
    """Extract mount point from path."""
    # Simple one-liner explanation is sufficient for obvious methods
    return path.split()[0]
```

**For fixtures - describe what they provide:**
```python
@pytest.fixture
def filter_module() -> FilterModule:
    """Create a FilterModule instance for testing."""
    # Brief description of what the fixture provides
    return FilterModule()
```

**Documentation standards:**
- **ALWAYS include a docstring** - even if it's just one line
- Method signatures: Full type annotations (Optional, Dict, List, etc.)
- Return types: Always specify return type annotations
- Complex methods: Full reST-style with params, returns, raises
- Test methods: Brief descriptive docstring only
- Simple getters/setters: One-line docstring is sufficient
- Fixtures: Describe what they provide, not implementation details
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

### Unit Test Best Practices

**Prefer parametrize for testing variations:**
```python
# GOOD - Concise, clear, and maintainable
@pytest.mark.parametrize('input_str,expected', [
    ("/dev/sda1 on / type ext4 (rw)", {"mount": "/", "source": "/dev/sda1", "type": "ext4"}),
    ("tmpfs on /run type tmpfs (rw,nosuid)", {"mount": "/run", "source": "tmpfs", "type": "tmpfs"}),
    ("/dev/sda2 on /mnt/my files type ext4 (rw)", {"mount": "/mnt/my files", "source": "/dev/sda2", "type": "ext4"}),
])
def test_parse_mount_variations(input_str, expected):
    """Test mount parsing with various input formats."""
    result = parse_mount_line(input_str)
    assert result == expected

# BAD - Repetitive separate test functions
def test_parse_mount_basic():
    """Test basic mount parsing."""
    result = parse_mount_line("/dev/sda1 on / type ext4 (rw)")
    assert result["mount"] == "/"
    assert result["source"] == "/dev/sda1"
    assert result["type"] == "ext4"

def test_parse_mount_tmpfs():
    """Test tmpfs mount parsing."""
    result = parse_mount_line("tmpfs on /run type tmpfs (rw,nosuid)")
    assert result["mount"] == "/run"
    assert result["source"] == "tmpfs"
    assert result["type"] == "tmpfs"

def test_parse_mount_with_spaces():
    """Test mount with spaces."""
    # ... yet another similar test
```

**Parametrize benefits:**
- Reduces code duplication dramatically
- Makes it easy to add new test cases
- Clear separation of test data from test logic
- Better test output showing which case failed
- Can combine with fixtures for even more power

**Keep mocking simple and focused:**
```python
# GOOD - Mock only what's necessary for the test
def test_parse_mount_with_spaces(filter_module):
    """Test mount parsing handles paths with spaces."""
    mount_output = "/dev/sda1 on /mnt/my files type ext4 (rw,relatime)"
    result = filter_module.filters()["mount"](mount_output)
    assert result[0]["mount"] == "/mnt/my files"

# BAD - Over-complicated mock setup
def test_parse_mount_complex():
    """Don't create elaborate mock hierarchies."""
    mock_jc = MagicMock()
    mock_jc.parse = MagicMock(return_value=[...])
    mock_module = MagicMock()
    mock_module.jc = mock_jc
    # ... many more mock setups
```

**Focus mocking on edge cases and failures:**
```python
# GOOD - Mock specific failure conditions
def test_jc_parse_error(filter_module):
    """Test filter handles jc parse errors gracefully."""
    with patch("ansible_collections.o0_o.posix.plugins.module_utils.jc_utils.jc.parse",
               side_effect=Exception("Parse error")):
        with pytest.raises(AnsibleFilterError, match="df failed"):
            filter_module.filters()["df"]("invalid output")

# GOOD - Use real functions when possible
def test_normalize_mount_entry():
    """Test mount normalization with real function."""
    from ansible_collections.o0_o.posix.plugins.module_utils.mount_utils import (
        normalize_mount_entry
    )
    entry = {"target": "/mnt", "source": "/dev/sda1"}
    result = normalize_mount_entry(entry)
    assert result["mount"] == "/mnt"
```

**Avoid over-testing wrapper functions:**
```python
# If parse_mount_line() is thoroughly tested:
def test_parse_mount_line_comprehensive():
    """Comprehensive tests for core parsing logic."""
    # ... many test cases for parse_mount_line()

# Then the filter wrapper only needs minimal testing:
def test_mount_filter_wrapper(filter_module):
    """Test filter correctly wraps parse_mount_line."""
    # Just verify the filter exists and calls the function
    mount_filter = filter_module.filters()["mount"]
    assert callable(mount_filter)
    # Maybe one basic test to ensure it's wired correctly
    result = mount_filter("simple mount output")
    assert isinstance(result, list)

# DON'T duplicate all parse_mount_line tests for the filter
```

**Testing guidelines:**
- Use real helper functions and imports when available
- Mock only external dependencies and failure conditions
- Don't create complex mock hierarchies
- If testing a wrapper, focus on wrapper-specific behavior
- Use parametrize for testing multiple similar cases
- Keep test data realistic and minimal

### Test Data Organization

**Store long test data in separate files:**
```python
# BAD - Long test data cluttering the test file
def test_parse_complex_mount():
    """Test parsing complex mount output."""
    mount_output = """
    /dev/mapper/vg0-root on / type ext4 (rw,relatime,errors=remount-ro)
    devtmpfs on /dev type devtmpfs (rw,nosuid,size=4096k,nr_inodes=1048576)
    tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev)
    tmpfs on /run type tmpfs (rw,nosuid,nodev,mode=755)
    # ... many more lines ...
    """
    result = parse_mount(mount_output)

# GOOD - Load test data from files
def test_parse_complex_mount():
    """Test parsing complex mount output."""
    test_data_dir = Path(__file__).parent / "files"
    mount_output = (test_data_dir / "mount_complex.txt").read_text()
    result = parse_mount(mount_output)
```

**Test file structure:**
```
tests/
├── unit/
│   ├── utils/                           # Shared unit test utilities
│   │   ├── __init__.py
│   │   ├── mounts.py                    # Mount-related test helpers
│   │   └── real_cmd.py                  # Real command execution for tests
│   └── plugins/
│       └── filter/
│           ├── files/                   # Test data for unit tests
│           │   ├── mount_basic.txt
│           │   ├── mount_complex.txt
│           │   └── fstab_sample.txt
│           └── test_mount.py
└── integration/
    └── targets/
        └── filter_mount/
            ├── files/                   # Test data for integration tests
            │   ├── expected_output.json
            │   └── mock_mount.txt
            └── tasks/
                └── main.yml
```

**Loading test data in unit tests:**
```python
from pathlib import Path

@pytest.fixture
def test_data_dir():
    """Path to test data files directory."""
    return Path(__file__).parent / "files"

def test_with_file_data(test_data_dir):
    """Test using data from file."""
    input_data = (test_data_dir / "input.txt").read_text()
    expected = json.loads((test_data_dir / "expected.json").read_text())
    result = some_function(input_data)
    assert result == expected
```

**Guidelines:**
- Use separate files for test data longer than 5-10 lines
- Name files descriptively (e.g., `mount_with_spaces.txt`, `fstab_nfs_entries.txt`)
- Keep related input and expected output files together
- Use JSON for structured expected output data
- Document any special characteristics in the filename or a README
- Use `tests/unit/utils/` for shared unit test helper functions

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
          - "'expected error' in ansible_failed_result['msg']"
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
class ActionModule(PosixActionBase):
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

### Filter Plugins

**Filter plugins must follow naming conventions and include proper documentation:**
```python
def mount(data: Union[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Parse mount command output into structured data.

    :param data: Mount command output as string or command result dict
    :returns: List of mount entries with source, mount, type, and options
    """
```

**Standards:**
- Accept multiple input formats (string, command dict, slurp result)
- Return consistent structured data
- Include comprehensive unit tests
- Use shared utilities from module_utils when appropriate

### Module Utils Organization and Imports

**ALWAYS prefer the shortest available import path:**
```python
# CORRECT - use __init__.py exports when available
from ansible_collections.o0_o.posix.plugins.module_utils import (
    PosixActionBase
)

# WRONG - don't use full path if __init__ export exists
from ansible_collections.o0_o.posix.plugins.module_utils.posix_action_base import (  # noqa: E501
    PosixActionBase  # Wrong! Use the shorter import above
)

# CORRECT - for utilities not exported via __init__
from ansible_collections.o0_o.posix.plugins.module_utils.mount_utils import (
    parse_mount_line
)

# For unavoidably long imports, use noqa comment
from ansible_collections.o0_o.posix.plugins.module_utils.some_long_module import (  # noqa: E501
    VerySpecificUtilityFunction
)
```

**NEVER import parent modules to use with dot notation:**
```python
# WRONG - never do this
from ansible_collections.o0_o.posix.plugins import module_utils
result = module_utils.PosixActionBase.some_method()  # Wrong!

# CORRECT - import what you need directly
from ansible_collections.o0_o.posix.plugins.module_utils import (
    PosixActionBase
)
result = PosixActionBase.some_method()
```

**In docstrings, use backslash for long imports:**
```python
"""Example docstring with imports.

Usage:
    from ansible.plugins.action import ActionBase
    from ansible_collections.o0_o.posix.plugins.module_utils \
        import PosixActionBase

    class ActionModule(PosixActionBase, ActionBase):
        pass
"""
```

**Standards:**
- Check `module_utils/__init__.py` first for available exports
- Use the shortest import path available
- Export commonly used classes/functions via `module_utils/__init__.py`
- Group related functionality in dedicated module_utils files
- Use consistent naming patterns (e.g., `mount_utils.py`, `fstab_utils.py`)
- Include comprehensive type hints and documentation
- Shared utilities like `process_registered_result` should be in appropriate util modules
- Use noqa comment for unavoidably long imports in code
- Use backslash for line continuation in docstrings

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
We are migrating to antsibull-changelog for changelog management. Use standard Ansible changelog format:

```yaml
# changelog.yml or changelogs/changelog.yaml (depending on collection)
releases:
  1.3.0:
    # Do not include release_date unless it's part of antsibull-changelog behavior
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

**Do not mention specific linters**: black, flake8, ansible-lint, etc.

**Do not manually add release_date** - let antsibull-changelog handle this automatically.

The changelog location varies by collection - check for `changelog.yml` or `changelogs/changelog.yaml`

### Git Workflow

**Branch Strategy:**
- `main`: Stable release branch
- `formatting-consistency`: Active development branch for style improvements
- Feature branches: For specific enhancements or fixes

**Commit Standards:**

**For Claude (claude.ai/code) - include signature:**
```bash
git commit -m "$(cat <<'EOF'
Fix mount filter to use merged dict for options

Changed mount options from list of dicts to merged dict format.
Unlike fstab which needs list for order preservation, mount
options are now stored as a single dictionary.

Updated all unit and integration tests to match new format.
Tests pass with ansible-test sanity, units, and integration.

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**For other AI agents or tools - NO Claude signature:**
```bash
git commit -m "$(cat <<'EOF'
Fix mount filter to use merged dict for options

Changed mount options from list of dicts to merged dict format.
Unlike fstab which needs list for order preservation, mount
options are now stored as a single dictionary.

Updated all unit and integration tests to match new format.
Tests pass with ansible-test sanity, units, and integration.
EOF
)"
```

**For human developers - standard format:**
```bash
git commit -m "Fix mount filter to use merged dict for options

Changed mount options storage format for better performance
and cleaner API. All tests updated and passing."
```

**IMPORTANT:** The Claude signature (🤖 and Co-Authored-By lines) should ONLY be used by Claude itself. Other AI agents should either:
- Use their own attribution if they have one
- Use no attribution at all
- Never impersonate Claude by using Claude's signature

**Do not mention specific linters in commit messages**

**Do not use origin as a remote**, use `github` or similar descriptive name

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
- Extend `PosixActionBase` for action plugins requiring raw fallback
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

**Important:** For ansible-test commands, always use the --venv at the very end. Anything after --venv will be silently ignored.
