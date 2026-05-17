# CLAUDE.md

MCP server plugin for `personal-history-db`. Exposes the phdb query layer as Claude-compatible tools via the Model Context Protocol.

## Build & Development

```bash
cd personal-history-db-mcp/
uv venv && uv pip install -e ".[dev]"
# Also need phdb available — install from sibling:
uv pip install -e "../personal-history-db"
```

Run commands via `uv run`:

```bash
uv run pytest                          # all tests
uv run ruff check src/ tests/          # lint
uv run ruff format src/ tests/         # auto-format
```

## Running the server

```bash
# Direct invocation (dev):
uv run personal-history-db-mcp

# Via uvx (installed):
uvx --from git+https://github.com/robfischer1/personal-history-db-mcp.git personal-history-db-mcp
```

Required env vars:
- `PHDB_DB_PATH` — path to the SQLite database file
- `PHDB_INSTANCE_DIR` — path to instance config directory (optional but recommended)

## Architecture

Single module at `src/phdb_mcp/server.py`. Each `@mcp.tool()` is a thin wrapper around a function in `phdb.query`. The server handles:
- Config resolution (env vars + instance TOML)
- Connection lifecycle (lazy-init, persistent)
- Engagement tracking (decay scoring on `get_chunk`)

## MCP config for Claude Code

```json
"mcpServers": {
  "personal-history-db": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/robfischer1/personal-history-db-mcp.git", "personal-history-db-mcp"],
    "env": {
      "PHDB_DB_PATH": "/path/to/personal-history-data/personal-history.db",
      "PHDB_INSTANCE_DIR": "/path/to/personal-history-instance"
    }
  }
}
```

## Conventions

- Python 3.11+, ruff lint, no strict mypy (thin wrapper, types come from phdb)
- `uv` is the package manager
- Depends on `personal-history-db>=0.2.0` (the framework package)
- License: Apache 2.0
