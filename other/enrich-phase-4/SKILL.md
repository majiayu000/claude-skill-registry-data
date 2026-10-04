---
name: enrich-phase-4
description: Fase 4 do enrich-lead — Analise profunda do website
user-invocable: false
---

# Fase 4 — Website Profundo

Leia o state file:
```bash
cat data/_state/enrichment-progress.json
```

Extraia: nome, cidade, discovered_urls.site_url.

## SE NAO TEM SITE

Se `site_url` esta vazio, crie um unico data_point:
```json
{
  "category": "website",
  "label": "Website",
  "value": "Nao possui site",
  "detail": {"status": "sem_site"},
  "source_type": "briefing",
  "source_name": "analise",
  "fetched_at": "..."
}
```
Salve no state, marque fase completa, e PARE aqui.

## SE TEM SITE — WebFetch MULTIPLO

### 4.1 Pagina principal

```
WebFetch: {site_url}
```

Extraia do HTML:
- **Emails**: `mailto:` links + regex `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
- **Telefones**: `tel:` links + regex `\(?\d{2}\)?\s*\d{4,5}-?\d{4}`
- **Meta tags** (EXTRAIR EXATAMENTE):
  - `<meta property="og:image" content="...">` → SALVAR COMO IMAGEM
  - `<meta property="og:title" content="...">`
  - `<meta property="og:description" content="...">`
  - `<meta name="description" content="...">`
  - `<link rel="icon" href="...">` → FAVICON
- **Links de redes sociais**: URLs contendo instagram.com, facebook.com, linkedin.com, youtube.com, twitter.com, tiktok.com
- **Imagens no HTML**: tags `<img>` — capture src de:
  - Imagens com "logo" no src, alt, class ou id
  - Imagens no `<header>` (logo/banner)
  - Imagens hero/banner (primeiras grandes fora do header)
- **Tech stack**:
  - `wp-content` ou `wordpress` → WordPress
  - `wix.com` ou `_wix` → Wix
  - `squarespace` → Squarespace
  - `shopify` → Shopify
  - Nenhum → HTML/CSS puro ou outro
- **SSL**: URL comeca com https?

### 4.2 Pagina "Sobre" (OBRIGATORIO se existir)

Procure no HTML por links contendo: /sobre, /about, /quem-somos, /a-clinica, /a-empresa, /historia, /equipe, /nosso-time

Se encontrar:
```
WebFetch: {site_url}/sobre (ou URL encontrada)
```
Extraia: texto da historia, fundadores, missao/visao, fotos da equipe (img src), data de fundacao.

### 4.3 Pagina "Contato" (se existir)

Procure por links: /contato, /contact, /fale-conosco

Se encontrar:
```
WebFetch: {site_url}/contato
```
Extraia: emails, telefones, endereco, mapa, WhatsApp.

### 4.4 Pagina de servicos/produtos (se relevante)

Se o site tem pagina de servicos ou cardapio:
```
WebFetch: {site_url}/servicos (ou equivalente)
```
Extraia: lista de servicos, precos (se disponiveis), imagens.

## REGRA DE IMAGENS

Toda URL de imagem encontrada (og:image, favicon, img src com logo, fotos equipe, banner) deve ser salva como data_point SEPARADO com category "images".

URLs relativas devem ser convertidas para absolutas:
- `/img/logo.png` → `https://site.com/img/logo.png`
- `../images/team.jpg` → `https://site.com/images/team.jpg`

## Salvar no state

Append todos os data_points e atualize discovered_urls se encontrou novas redes sociais.

Categorias dos data_points desta fase:
- `"website"` → dados gerais (tech stack, SSL, meta tags)
- `"contact"` → emails, telefones, endereco, WhatsApp
- `"images"` → cada URL de imagem separada
- `"history"` → texto da pagina sobre/historia
- `"services"` → lista de servicos/produtos

## CRITERIO DE CONCLUSAO
- Se tem site: pagina principal acessada + pelo menos 1 subpagina tentada
- og:image extraida (se existir)
- Emails e telefones coletados
- Tech stack identificado
- Se nao tem site: marcado "sem_site" e fase completa
