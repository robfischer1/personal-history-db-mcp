"""Smoke tests for the MCP server module."""
from __future__ import annotations

import importlib
import sys
from unittest.mock import patch


def test_import():
    """Package imports without error."""
    import phdb_mcp
    assert phdb_mcp.__version__ == "0.2.0"


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


# ---------------------------------------------------------------------------
# Behavioral tests for _resolve_config and module-level constants
# ---------------------------------------------------------------------------


def _reload_server(**env_overrides: str):
    """Re-import phdb_mcp.server with a controlled environment.

    Clears the cached module so _resolve_config runs again with the
    patched env vars.
    """
    with patch.dict("os.environ", env_overrides, clear=False):
        for mod_name in list(sys.modules):
            if mod_name.startswith("phdb_mcp"):
                del sys.modules[mod_name]
        return importlib.import_module("phdb_mcp.server")


def test_resolve_config_uses_phdb_db_path():
    """PHDB_DB_PATH env var is honored as the DB path."""
    mod = _reload_server(PHDB_DB_PATH="/custom/path/my.db")
    from pathlib import Path
    assert Path("/custom/path/my.db") == mod.DB_PATH


def test_resolve_config_falls_back_to_legacy_env():
    """PERSONAL_HISTORY_DB is the legacy fallback when PHDB_DB_PATH is unset."""
    env = {"PERSONAL_HISTORY_DB": "/legacy/path.db"}
    with patch.dict("os.environ", env, clear=False):
        # Remove PHDB_DB_PATH and PHDB_INSTANCE_DIR so the legacy path wins
        import os
        os.environ.pop("PHDB_DB_PATH", None)
        os.environ.pop("PHDB_INSTANCE_DIR", None)
        for mod_name in list(sys.modules):
            if mod_name.startswith("phdb_mcp"):
                del sys.modules[mod_name]
        mod = importlib.import_module("phdb_mcp.server")
    from pathlib import Path
    assert Path("/legacy/path.db") == mod.DB_PATH


def test_resolve_config_defaults():
    """When no env vars are set, module-level defaults are used."""
    import os
    with patch.dict("os.environ", {}, clear=False):
        os.environ.pop("PHDB_DB_PATH", None)
        os.environ.pop("PHDB_INSTANCE_DIR", None)
        os.environ.pop("PERSONAL_HISTORY_DB", None)
        os.environ.pop("OLLAMA_URL", None)
        os.environ.pop("OLLAMA_MODEL", None)
        for mod_name in list(sys.modules):
            if mod_name.startswith("phdb_mcp"):
                del sys.modules[mod_name]
        mod = importlib.import_module("phdb_mcp.server")
    from pathlib import Path
    assert Path(mod._DEFAULT_DB_FILENAME) == mod.DB_PATH
    assert mod._DEFAULT_EMBED_URL == mod.OLLAMA_URL
    assert mod._DEFAULT_EMBED_MODEL == mod.OLLAMA_MODEL


def test_default_constants_are_sensible():
    """Module-level default constants have expected values."""
    mod = _reload_server(PHDB_DB_PATH="/tmp/fake.db")
    assert mod._DEFAULT_DB_FILENAME == "personal-history.db"
    assert mod._DEFAULT_EMBED_URL == "http://localhost:11434"
    assert mod._DEFAULT_EMBED_MODEL == "nomic-embed-text"
    assert mod._DEFAULT_SINCE_YEAR == "2018"
