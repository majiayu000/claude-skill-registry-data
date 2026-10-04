---
name: lead-phase-4
description: Fase 4 do lead-finder — Validacao de perfis via navegacao Playwright
user-invocable: false
---

# Fase 4 — Validacao via Navegacao (LOOP)

**FERRAMENTAS:** APENAS Playwright MCP. NUNCA instagrapi API. NUNCA claude-in-chrome.

Leia o state file:
```bash
cat data/_state/lead-finder-progress.json
```

Extraia: candidates (lista de usernames), limite, filtros.

## LOOP PRINCIPAL

Para CADA username candidato, ate atingir --limite de leads:

### 4.1 Navegar no perfil

```
browser_navigate: https://www.instagram.com/{username}/
```

Espere carregar (3-5 segundos).

### 4.2 Verificar se perfil existe e e publico

```
browser_take_screenshot
```

Analise:
- Se "Sorry, this page isn't available" → perfil nao existe → PULAR
- Se "This Account is Private" → perfil privado → registrar e PULAR
- Se ve perfil com foto, bio, grid → continuar

### 4.3 Extrair dados do perfil

```javascript
browser_evaluate: (() => {
  // og:image = foto de perfil HD
  const ogImg = document.querySelector('meta[property="og:image"]');

  // og:description = "X Followers, Y Following, Z Posts - BIO TEXT"
  const ogDesc = document.querySelector('meta[property="og:description"]');
  const desc = ogDesc ? ogDesc.content : '';

  // Parsear contadores da og:description
  // Formatos possiveis: "1,234 Followers" ou "1.2K Followers" ou "1M Followers"
  const match = desc.match(/([\d,.KkMm]+)\s*Followers?,?\s*([\d,.KkMm]+)\s*Following,?\s*([\d,.KkMm]+)\s*Posts?/i);

  // Pegar bio completa do meta description
  const metaDesc = document.querySelector('meta[name="description"]');
  const bioText = metaDesc ? metaDesc.content : '';

  // og:title = nome do perfil
  const ogTitle = document.querySelector('meta[property="og:title"]');

  return JSON.stringify({
    profile_pic: ogImg ? ogImg.content : null,
    og_desc: desc.substring(0, 400),
    full_name: ogTitle ? ogTitle.content.split('(')[0].trim() : null,
    followers_raw: match ? match[1] : null,
    following_raw: match ? match[2] : null,
    posts_raw: match ? match[3] : null,
    bio: bioText.substring(0, 500)
  });
})()
```

### 4.4 Extrair link externo e tipo de conta

```javascript
browser_evaluate: (() => {
  // Link na bio
  const links = document.querySelectorAll('a[href]');
  let externalUrl = null;
  links.forEach(a => {
    const href = a.href || '';
    if (href.includes('l.instagram.com/') || href.includes('linktr.ee') ||
        href.includes('taplink.cc') || href.includes('bio.link')) {
      externalUrl = href;
    }
  });

  // Categoria (visivel em contas Business abaixo do nome)
  // Geralmente e um texto como "Dentist", "Restaurant", "Psychologist"
  const allText = document.body.innerText;

  // Botao de contato/email/telefone (so contas comerciais tem)
  const hasContact = !!document.querySelector('[href*="mailto:"]') ||
                     !!document.querySelector('[href*="tel:"]') ||
                     allText.includes('Contact') || allText.includes('Contato');

  return JSON.stringify({
    external_url: externalUrl,
    has_contact: hasContact,
    page_text_snippet: allText.substring(0, 1000)
  });
})()
```

### 4.5 Pegar links dos posts e thumbnails da grid

```javascript
browser_evaluate: (() => {
  // Links dos posts na grid
  const postLinks = document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]');
  const links = [...new Set([...postLinks].map(a => a.href))].slice(0, 12);

  // Thumbnails da grid (imagens CDN)
  const imgs = document.querySelectorAll('img');
  const gridImgs = [];
  imgs.forEach(img => {
    if (img.src && (img.src.includes('scontent') || img.src.includes('cdninstagram'))
        && img.naturalWidth > 100) {
      gridImgs.push(img.src);
    }
  });

  return JSON.stringify({
    post_links: links,
    grid_thumbnails: [...new Set(gridImgs)].slice(0, 12)
  });
})()
```

### 4.6 Navegar nos top 3 posts (fotos HD + legendas + datas)

Para os primeiros 3 post_links:

```
browser_navigate: https://www.instagram.com/p/{shortcode}/
```

```javascript
browser_evaluate: (() => {
  const ogImg = document.querySelector('meta[property="og:image"]');
  const ogDesc = document.querySelector('meta[property="og:description"]');
  const timeEl = document.querySelector('time[datetime]');

  return JSON.stringify({
    image_hd: ogImg ? ogImg.content : null,
    caption: ogDesc ? (ogDesc.content || '').substring(0, 200) : null,
    date: timeEl ? timeEl.getAttribute('datetime') : null
  });
})()
```

Dos 3 posts, extraia:
- **oldest_post_date**: data do post mais antigo
- **newest_post_date**: data do post mais recente
- **Fotos HD**: og:image de cada post

### 4.7 Scoring

> **MODO INFLUENCER** — se o state tiver `filtros.modo == "influencer"`, NAO use
> a formula abaixo. Use o scoring de `research/influencer-mae-sul-sudeste.md`:
> - **Gate rigido** (reprova = DESCARTE): `followers < min_seguidores` OU
>   `followers > max_seguidores`; conta de loja/marca/meme/agregador; nicho
>   nao-materno; regiao fora de S/SE confirmada.
> - **Score (0–10)**: +3 regiao S/SE explicita; +2 sinais de idade 35–50
>   (filho adolescente, "depois dos 40"); +2 faixa 12k–35k; +1 contato na bio;
>   +1 ativa (<30d); +1 nicho materno + linguagem de mulher.
> - **Classificacao**: >=7 QUENTE, >=4 MORNO, senao REVISAR.
> - **Idade/genero em duvida** → `status=REVISAR` E buscar +2 candidatos
>   (regra do cliente para nao perder ritmo ate a meta).
> Salve no CSV `leads/influencers_mae_sul_sudeste.csv`. Pule 4.8 padrao, va a 4.9.

#### Scoring padrao (vender site) — mesma formula do MCP atual

Calcule o score baseado nos dados extraidos:

```
score = 0
razoes = []

# Link externo
has_real_site = external_url nao e null E nao contem:
  linktr.ee, linktree.com, taplink.cc, beacons.ai, bio.link,
  bio.site, lnk.bio, campsite.bio, hoo.be, snipfeed.co,
  allmylinks.com, solo.to, carrd.co, about.me, flow.page,
  stan.store, whats.link, wa.me, bit.ly, tinyurl.com

Se NAO tem site real: score += 3
Se conta Business/Creator (tem categoria ou botao contato): score += 2
Se followers < 1000: score += 1
Se tem email/telefone visivel: score += 1
Se media_count > 100: score -= 2
Se oldest_post_date < 90 dias: score += 3
Se oldest_post_date 90-180 dias: score += 1

Classificacao:
  score >= 6 → QUENTE
  score >= 3 → MORNO
  score < 3 → FRIO
```

### 4.8 Salvar no CSV

Use o MCP de cache para salvar:
```
instagram_append_lead(lead_json)
instagram_mark_visited(username, param_key, classificacao, score)
```

### 4.9 Aplicar filtros

Se filtros ativos:
- `--so-comercial`: descartar se nao tem categoria/botao contato
- `--sem-site`: descartar se has_real_site = true
- `--max-idade-conta`: descartar se oldest_post_date > N dias
- `--max-idade-post`: descartar se newest_post_date > N dias

### 4.10 Reportar

Se PASSOU nos filtros:
```
LEAD: @{username} ({classificacao}, score {score})
  {full_name} | {followers} seg. | {posts} posts
  Bio: {bio_resumo}
  Site: {external_url ou "nenhum"}
  Fotos: {N} imagens capturadas
  Motivos: {razoes}
```

Se NAO passou: `SALVO: @{username} (FRIO) — {motivo descarte}`

### 4.11 Progresso

A cada 5 perfis:
```
Progresso: X validados, Y leads encontrados (meta: Z)
  QUENTES: A | MORNOS: B | FRIOS: C
```

### 4.12 Delay natural

Entre cada perfil: espere 5-10 segundos.
O Playwright navega rapido demais — um humano levaria pelo menos 5s por perfil.

## CRITERIO DE CONCLUSAO
- Todos candidatos processados OU --limite atingido
- Cada perfil: navegado, dados extraidos, scoring, CSV salvo, cache atualizado
- Fotos HD dos posts salvos para leads QUENTES
- Progresso reportado ao usuario
