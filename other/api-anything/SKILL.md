---
name: API Anything (Web-to-API Engine)
description: Transforma qualquer portal web externo em operações de API REST locais ultrarrápidas (Tier 1) usando api-anything, eliminando navegadores pesados e economizando tokens.
---

# API Anything — Sovereign Web Distiller

Esta skill permite ao Agente Áquila Pro aprender o funcionamento de qualquer portal web externo uma única vez e, a partir de então, chamá-lo diretamente via HTTP/JSON leve sem precisar abrir o Chrome/Playwright.

## 🚀 Capacidades

- **Zero-Browser Inference:** Após aprender a rota com 2 exemplos, as consultas rodam em Tier 1 (HTTP nativo com latência < 200ms).
- **Redução Drástica de Tokens:** Retorna JSON enxuto em vez de carregar HTML/DOM inteiro no contexto.
- **Integração MCP:** Expõe `list_sites`, `list_operations`, `call_operation` e `login`.

## 🛠️ Comandos Principais

Executáveis localizados em: `c:\aquila\external\api-anything\dist\cli.js`

```powershell
# Listar sites aprendidos
node c:\aquila\external\api-anything\dist\cli.js sites

# Chamar operação existente
node c:\aquila\external\api-anything\dist\cli.js call <site> <operacao> chave=valor

# Aprender nova página
node c:\aquila\external\api-anything\dist\cli.js add <site> <op> --trigger '<url_template>' --example chave=val1 --example2 chave=val2 --html '{"items":"seletor","fields":{"titulo":"seletor_filho"}}'
```

## 🎯 Aplicação no Áquila Pro
- Consulta a calendários e diários oficiais de Secretarias de Educação (SEDUC).
- Coleta de dados educacionais do INEP / MEC.
- Monitoramento de notas e gabaritos de vestibulares/ENEM.
