# personal-history-db-mcp

MCP server plugin for [personal-history-db](https://github.com/robfischer1/personal-history-db) — exposes the phdb query layer as Claude-compatible tools via the [Model Context Protocol](https://modelcontextprotocol.io/).

## Install

```bash
# From git (recommended for now):
uvx --from git+https://github.com/robfischer1/personal-history-db-mcp.git personal-history-db-mcp

# From a local checkout:
cd personal-history-db-mcp/
uv venv && uv pip install -e . -e ../personal-history-db
uv run personal-history-db-mcp
```

## Configuration

Set environment variables before running:

| Variable | Required | Description |
|:---|:---|:---|
| `PHDB_DB_PATH` | Yes* | Path to the SQLite database file |
| `PHDB_INSTANCE_DIR` | No | Instance config directory (provides DB path + embedding config via TOML) |
| `PERSONAL_HISTORY_DB` | No | Legacy env var (still honored) |
| `OLLAMA_URL` | No | Override Ollama endpoint (default: `http://localhost:11434`) |
| `OLLAMA_MODEL` | No | Override embedding model (default: `nomic-embed-text`) |
| `DEFAULT_SINCE` | No | Baseline year filter for hybrid search (default: `2018`) |

*Not required if `PHDB_INSTANCE_DIR` is set and contains a valid `paths.toml`.

## Tools exposed

| Tool | Purpose |
|:---|:---|
| `search` | Hybrid semantic + FTS5 retrieval with RRF fusion |
| `get_message` | Full message by ID with recipients/attachments |
| `get_chunk` | Full chunk content + engagement recording |
| `get_thread` | All messages in a thread |
| `list_sources` | Inventory of ingested sources |
| `corpus_stats` | Year/direction/sender distribution |
| `nearest_neighbors` | Semantic similarity from a chunk |
| `server_info` | Diagnostics (DB location, size, Ollama status) |
| `find_messages_by_participant` | Person-based message lookup |
| `find_threads` | Thread lookup by subject |
| `top_correspondents` | Most-frequent contacts in a window |
| `log_engagement` | Manual engagement event for decay scoring |

## Claude Code / Desktop config

```json
{
  "mcpServers": {
    "personal-history-db": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/robfischer1/personal-history-db-mcp.git", "personal-history-db-mcp"],
      "env": {
        "PHDB_DB_PATH": "/path/to/personal-history.db",
        "PHDB_INSTANCE_DIR": "/path/to/personal-history-instance"
      }
    }
  }
}
```

## License

Apache 2.0
