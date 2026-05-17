"""Smoke tests for the MCP server module."""
from __future__ import annotations

import importlib
import sys
from unittest.mock import patch


def test_import():
    """Package imports without error."""
    import phdb_mcp
    assert phdb_mcp.__version__ == "0.1.0"


def test_server_module_loads():
    """Server module can be imported (mcp + phdb must be available)."""
    with patch.dict("os.environ", {"PHDB_DB_PATH": "/tmp/fake.db"}):
        if "phdb_mcp.server" in sys.modules:
            del sys.modules["phdb_mcp.server"]
        mod = importlib.import_module("phdb_mcp.server")
        assert hasattr(mod, "mcp")
        assert hasattr(mod, "main")


def test_tool_count():
    """All 12 tools are registered."""
    with patch.dict("os.environ", {"PHDB_DB_PATH": "/tmp/fake.db"}):
        if "phdb_mcp.server" in sys.modules:
            del sys.modules["phdb_mcp.server"]
        mod = importlib.import_module("phdb_mcp.server")
        tools = mod.mcp._tool_manager._tools
        assert len(tools) == 12, f"Expected 12 tools, got {len(tools)}: {list(tools.keys())}"
