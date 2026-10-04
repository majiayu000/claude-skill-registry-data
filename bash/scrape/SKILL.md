---
name: scrape
description: Extraia conteúdo de qualquer página web como markdown limpo via API Web Unlocker do Bright Data. Desativa detecção de bots e CAPTCHA. Requer as variáveis de ambiente BRIGHTDATA_API_KEY e BRIGHTDATA_UNLOCKER_ZONE.
---

# Bright Data - Web Scraper

Extraia conteúdo de qualquer página web e obtenha markdown limpo usando a API Web Unlocker do Bright Data. Desativa automaticamente detecção de bots e CAPTCHA.

## Configuração

**1. Obtenha sua chave de API:**
Obtenha uma chave no [Bright Data Dashboard](https://brightdata.com/cp).

**2. Crie uma zona Web Unlocker:**
Crie uma zona em brightdata.com/cp clicando em "Add" (canto superior direito) e selecionando "Unlocker zone".

**3. Defina as variáveis de ambiente:**
```bash
export BRIGHTDATA_API_KEY="your-api-key"
export BRIGHTDATA_UNLOCKER_ZONE="your-zone-name"
```

## Uso

```bash
bash scripts/scrape.sh "url"
```

**Parâmetros:**
- `url` (obrigatório): A URL da página web a ser extraída

**Exemplos:**
```bash
# Extrair um artigo de notícias
bash scripts/scrape.sh "https://example.com/article"

# Extrair uma página de produto
bash scripts/scrape.sh "https://shop.example.com/product/123"
```

## Formato de Saída

Retorna conteúdo markdown limpo extraído da página web:
```markdown
# Page Title

Main content of the page converted to markdown format...

## Section Heading

More content...
```

## Funcionalidades

- **Desativação de Detecção de Bots**: Lida automaticamente com medidas anti-bot
- **Resolução de CAPTCHA**: Desativa desafios de CAPTCHA
- **Markdown Limpo**: Retorna conteúdo markdown bem formatado
- **Renderização JavaScript**: Trata páginas com muito JavaScript

## Dependências

- `curl` - Para requisições de API