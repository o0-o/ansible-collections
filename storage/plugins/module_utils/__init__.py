# vim: ts=4:sw=4:sts=4:et:ft=python
# -*- mode: python; tab-width: 4; indent-tabs-mode: nil; -*-
#
# GNU General Public License v3.0+
# SPDX-License-Identifier: GPL-3.0-or-later
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Copyright (c) 2025 oØ.o (@o0-o)
#
# This file is part of the o0_o.storage Ansible Collection.

"""Module utilities for the o0_o.storage collection."""

from __future__ import annotations

from ansible_collections.o0_o.storage.plugins.module_utils.storage_base import StorageBase
from ansible_collections.o0_o.storage.plugins.module_utils.storage_drivers import STORAGE_DRIVERS

__all__ = [
    "StorageBase",
    "STORAGE_DRIVERS",
]
