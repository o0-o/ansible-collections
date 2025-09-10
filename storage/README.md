# o0_o.storage

Storage utilities and filesystem classification for Ansible

## Overview

This collection provides utilities for working with storage devices, filesystems, and mount points in Ansible. It includes base classes and driver definitions for classifying and processing storage-related data across different platforms.

## Installation

```bash
ansible-galaxy collection install o0_o.storage
```

## Dependencies

This collection has no external dependencies.

## Usage

### Module Utilities

The collection provides module utilities that can be used by other collections:

- `storage_base.StorageBase`: Base class for storage classification and facts formatting
- `storage_drivers.STORAGE_DRIVERS`: Comprehensive dictionary of filesystem driver definitions

### Basic Examples

```python
from ansible_collections.o0_o.storage.plugins.module_utils import (
    StorageBase,
    STORAGE_DRIVERS,
)
```

### Advanced Usage

The storage utilities can classify filesystems into categories:
- Regular filesystems (ext4, xfs, ntfs, etc.)
- Virtual filesystems (proc, sysfs, tmpfs, etc.)
- Network filesystems (nfs, cifs, sshfs, etc.)
- Overlay filesystems (overlayfs, aufs, etc.)
- FUSE-based filesystems with automatic detection

## Plugins

### Module Utilities

- **storage_base**: Base class for storage classification and facts formatting
- **storage_drivers**: Comprehensive filesystem driver definitions

## Development & Testing

```bash
ansible-test sanity --venv
ansible-test units --venv
ansible-test integration --venv
```

## License

Licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.txt) or later (GPLv3+)