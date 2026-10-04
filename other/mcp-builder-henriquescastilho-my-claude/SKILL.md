---
name: mcp-builder
description: Criar MCP servers para integrar APIs externas ao Claude. Usar quando precisar conectar a servicos externos, criar ferramentas customizadas, ou integrar APIs de terceiros.
allowed-tools: Read Write Edit Bash Grep Glob
---

# Construtor de MCP Servers -- Padrao DME

## Stack recomendada

| Linguagem | Framework | Quando usar |
|-----------|-----------|-------------|
| Python | FastMCP | Maioria dos casos |
| TypeScript | @modelcontextprotocol/sdk | Projeto ja e TS |

## Estrutura minima (Python)

```python
from fastmcp import FastMCP
mcp = FastMCP("nome-do-servico")

@mcp.tool()
def minha_ferramenta(parametro: str) -> str:
    """Descricao clara do que faz."""
    return resultado
```

## Boas praticas

- Cada tool faz UMA coisa
- Descricoes claras nos tools
- Tipos explicitos em parametros
- Erros retornam mensagem util, nao stack trace
- Auth via env vars
- Rate limiting se API externa tem limites
- Timeout em chamadas externas

## Registro em ~/.claude/.mcp.json

```json
{
  "mcpServers": {
    "nome": {
      "command": "python",
      "args": ["/caminho/server.py"]
    }
  }
}
```

## Seguranca

- Nunca expor credenciais nos logs
- Validar todo input
- HTTPS para chamadas externas
- Permissoes minimas
