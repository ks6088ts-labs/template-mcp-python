# template-mcp-python

This repository is a template repository for Python projects.

## Logs

- [MCP Python SDK / Installation](https://modelcontextprotocol.github.io/python-sdk/installation/)
- [MCP Python SDK / Quick Example](https://modelcontextprotocol.github.io/python-sdk/)

```shell
# Test with the MCP Inspector
uv run mcp dev template_mcp_python/mcp_servers/quick_example.py
```

- [MCP Python SDK / API Reference](https://modelcontextprotocol.github.io/python-sdk/api/)

```shell
uv run pytest --capture=no -vv
```

- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)

```shell
npx @modelcontextprotocol/inspector
```

- [LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters)

```shell
# Example: Multi-Server MCP with Image Transfer and Image Analyzer
uv run python scripts/mcp_runner.py multi-server-mcp \
    --prompt "image-transfer の store_image を呼び出し、返り値として取得できた ID を使って、image-analyzer で解析した結果を日本語で説明して"

# Example: Multi-Server MCP with Playwright-MCP
uv run python scripts/mcp_runner.py multi-server-mcp \
    --prompt "Playwright-MCPを使って、はてなブックマークのテクノロジーカテゴリの人気エントリのタイトルを5つ取得して表示して"
```
