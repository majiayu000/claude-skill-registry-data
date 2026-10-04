---
name: enrich-phase-6
description: Fase 6 do enrich-lead — Captura de imagens (WebSearch + Playwright MCP)
user-invocable: false
---

# Fase 6 — Captura de Imagens (Abordagem Dupla)

Esta e a fase MAIS IMPORTANTE para material visual. Usa DOIS metodos complementares.

Leia o state file:
```bash
cat data/_state/enrichment-progress.json
```

Extraia: nome, cidade, nicho, strategy, discovered_urls (instagram_username, site_url, platform_urls).

Verifique tambem quantas imagens ja foram coletadas nas fases anteriores (data_points com category "images").

---

## ETAPA A — WebSearch + WebFetch (texto, og:image)

Metodo rapido baseado em texto. Executa TODAS estas buscas:

### A.1 Buscas Google por texto

```
WebSearch: "{nome}" "{cidade}" foto
WebSearch: "{nome}" "{cidade}" foto fachada OR interior OR equipe
WebSearch: "{nome}" logo
```

Se tem Instagram username:
```
WebSearch: "{username}" site:instagram.com
WebSearch: "{nome}" "{cidade}" foto instagram
```

Buscas niche-specific:
- **food:** `"{nome}" site:ifood.com.br` e `"{nome}" site:rappi.com.br`
- **medical/dental:** `"{nome}" site:doctoralia.com.br`
- **hospitality:** `"{nome}" site:tripadvisor.com.br` e `"{nome}" site:booking.com`
- **beauty:** `"{nome}" site:booksy.com`
- **generic:** `"{nome}" "{cidade}" foto fachada OR interior OR equipe`

### A.2 WebFetch para og:image

Para cada resultado relevante encontrado:
```
WebFetch: {url_do_resultado}
```
Extraia `<meta property="og:image" content="...">` de cada pagina.

### A.3 Instagram direto (WebFetch)

Se tem username:
```
WebFetch: https://www.instagram.com/{username}/
```
Procure og:image no HTML — foto de perfil em alta resolucao.
NOTA: Instagram frequentemente retorna apenas CSS/config via WebFetch. Se nao encontrar, a Etapa B resolve.

### A.4 Coletar LINKS de posts do Instagram

Da busca `"{username}" site:instagram.com`, colete TODAS as URLs de posts:
- `instagram.com/p/{shortcode}/`
- `instagram.com/reel/{shortcode}/`

Salve esses links — a Etapa B vai navegar neles para extrair as imagens reais.

### A.5 Fotos profissionais

```
WebSearch: "{nome}" "{cidade}" foto profissional OR retrato OR ensaio
```
Se encontrar portfolio de fotografo, WebFetch para og:image.

---

## ETAPA B — Playwright MCP (navegador real, JS renderizado)

Este metodo captura imagens que WebSearch/WebFetch NAO conseguem porque dependem de JavaScript.

**FERRAMENTAS — Estrategia dual:**

**Para Instagram (precisa stealth):** APENAS Playwright MCP:
- `browser_navigate`, `browser_take_screenshot`, `browser_evaluate`, `browser_click`, `browser_snapshot`

**Para plataformas normais (iFood, Doctoralia, Rappi, TripAdvisor, Booking):** Chrome DevTools MCP (se disponivel):
- Vantagem: Network tab revela TODAS as URLs de imagem CDN carregadas, incluindo lazy-loaded e redirects
- Se Chrome DevTools nao disponivel, usar Playwright normalmente

**NUNCA use claude-in-chrome. NUNCA.**

---

### ARMADILHA CRITICA: Google Images NAO funciona para extrair URLs

**NAO TENTE extrair URLs de imagem diretamente do Google Images.**

O Google Images renderiza thumbnails como **base64 inline** e guarda as URLs reais em scripts codificados que NAO sao acessiveis via DOM. Tentar:
- `document.querySelectorAll('img')` → retorna base64, nao URLs reais
- Clicar na imagem para abrir painel → unreliable, URL nem sempre aparece
- Procurar em scripts com regex → URLs estao codificadas/escapadas
- `data-ou`, `data-src` → nao existem mais na versao atual

**O QUE FUNCIONA:** Usar Google Images apenas para encontrar LINKS de paginas (posts do Instagram, perfis do iFood, etc) e depois navegar diretamente nessas paginas para extrair og:image via Playwright.

---

### B.0 — Profile Pic (OBRIGATORIO — fazer ANTES de qualquer outra captura)

1. Navegar para `https://www.instagram.com/{username}/`
2. `browser_evaluate` para extrair a URL da foto de perfil em alta resolucao:
   - Buscar `img` com alt contendo "perfil" e `naturalWidth >= 150`
   - OU extrair do HTML shared data: `profile_pic_url_hd`
3. Baixar via `curl` para `data/enrichment/{slug}/logo/profile-pic.jpg`
4. **CLAUDE DEVE LER A IMAGEM** (Read tool) e descrever:
   - O que e? (logo, foto pessoal, ilustracao, texto com tipografia)
   - Cores predominantes (preto/branco, colorido, tons quentes/frios)
   - Se e logo: descrever o simbolo/forma/tipografia
   - Se tem fundo branco/colorido: processar versao invertida (Python PIL `ImageOps.invert`) para uso em fundo escuro
5. Salvar como data_point `category: "images"`, `tipo: "profile_pic"`

**IMPORTANTE:** Muitos clientes usam a profile pic como LOGO OFICIAL. Se for logo, criar duas variantes:
- `profile-pic.jpg` (original)
- `logo-white.png` (invertida, fundo transparente, para fundos escuros)

### B.0a — Analise de Padroes Visuais do Grid (OBRIGATORIO)

APOS scrollar o grid e antes de abrir posts individuais:

1. **Tirar screenshot do grid** (`browser_take_screenshot` do perfil scrollado mostrando 12-18 posts)
2. **Ler o screenshot** (Read tool) e analisar:
   - Existe padrao alternado? (ex: foto-foto-card tipografico, cor-BW-cor)
   - Paleta predominante? (warm, cool, B&W, mista)
   - Fotos sao tratadas? (cor natural, grayscale, sepia, saturadas)
   - Existe template recorrente? (cards com fundo preto + texto branco, por ex)
   - Proporcao fotos vs videos vs carousels vs reels
3. **Abrir 3-5 posts individuais** (variados: fotos + cards tipograficos se existirem) e **tirar screenshot de cada**
4. **Ler cada screenshot** e documentar:
   - Tipografia em cards: serif vs sans, peso, caixa (upper/mixed), tracking
   - Alinhamento do texto (centrado, left, right)
   - Elementos recorrentes (logo no topo, CTA no rodape, bordas, filtros)
   - Tom fotografico (studio, natural, editorial, casual, B&W)
5. Salvar como data_point:
```json
{
  "category": "brand_voice",
  "label": "Instagram visual identity analysis",
  "value": "descricao resumida",
  "detail": {
    "grid_pattern": "alternado foto/card tipografico",
    "color_palette": "preto puro + branco + warm studio tones",
    "typography_style": "sans-serif bold uppercase com italic accent",
    "photo_treatment": "cor natural, sem filtro",
    "recurring_template": "fundo preto + texto branco + logo topo + CTA italico rodape"
  },
  "source_type": "briefing",
  "source_name": "instagram_visual_analysis"
}
```

**POR QUE ISSO IMPORTA:** O site-builder (Phase 3a) usa essa analise como RESTRICAO. Se voce nao capturar os padroes visuais, o builder vai inventar uma estetica que contradiz a identidade real do cliente (ex: usar serif quando o cliente usa sans, aplicar grayscale quando fotos sao coloridas, inventar paleta copper quando a marca e preto/branco).

### B.1 Google Images → Extrair LINKS de paginas (NAO imagens)

Navegue no Google Images para encontrar links de POSTS e PERFIS:

```
browser_navigate: https://www.google.com/search?tbm=isch&q={username}+site:instagram.com
```

Depois extraia os LINKS das paginas originais (NAO as imagens):
```javascript
browser_evaluate: (() => {
  const links = document.querySelectorAll('a[href*="instagram.com"]');
  const results = [];
  links.forEach(a => {
    const href = a.href || '';
    if (href.includes('instagram.com/p/') || href.includes('instagram.com/reel/')) {
      results.push(href);
    }
  });
  return JSON.stringify([...new Set(results)].slice(0, 20));
})()
```

Combine com os links ja coletados na Etapa A.4. Voce agora tem uma lista de URLs de posts do Instagram.

Repita para outras plataformas se relevante:
```
browser_navigate: https://www.google.com/search?tbm=isch&q="{nome}"+site:ifood.com.br
```
→ Extraia links de paginas do iFood.

```
browser_navigate: https://www.google.com/search?tbm=isch&q="{nome}"+site:doctoralia.com.br
```
→ Extraia links de paginas da Doctoralia.

### B.2 Navegar em cada post do Instagram e extrair og:image

**ESTE E O PASSO MAIS VALIOSO.** O Playwright renderiza o JavaScript do Instagram e consegue extrair og:image que WebFetch nao consegue.

Para cada URL de post coletada (ate 10 posts), navegue e extraia:

```javascript
// Navegar no post
browser_navigate: https://www.instagram.com/p/{shortcode}/

// Extrair og:image e imagens CDN
browser_evaluate: (() => {
  const ogImg = document.querySelector('meta[property="og:image"]');
  const ogDesc = document.querySelector('meta[property="og:description"]');
  const ogTitle = document.querySelector('meta[property="og:title"]');

  const imgs = document.querySelectorAll('img[src*="cdninstagram"], img[src*="scontent"]');
  const cdnUrls = [];
  imgs.forEach(i => cdnUrls.push(i.src));

  return JSON.stringify({
    og_image: ogImg ? ogImg.content : null,
    og_desc: ogDesc ? (ogDesc.content || '').substring(0, 150) : null,
    og_title: ogTitle ? (ogTitle.content || '').substring(0, 100) : null,
    cdn_images: [...new Set(cdnUrls)]
  });
})()
```

**DICA DE PERFORMANCE:** Se a ferramenta `browser_run_playwright` (Run Playwright code) estiver disponivel, use para processar TODOS os posts em batch de uma vez:

```javascript
browser_run_playwright: async (page) => {
  const posts = [
    'https://www.instagram.com/p/SHORTCODE1/',
    'https://www.instagram.com/p/SHORTCODE2/',
    'https://www.instagram.com/p/SHORTCODE3/',
    // ... ate 10 posts
    'https://www.instagram.com/{username}/'  // perfil tambem
  ];

  const results = [];

  for (const url of posts) {
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 10000 });
      await page.waitForTimeout(2000);

      const data = await page.evaluate(() => {
        const ogImg = document.querySelector('meta[property="og:image"]');
        const ogDesc = document.querySelector('meta[property="og:description"]');
        const ogTitle = document.querySelector('meta[property="og:title"]');
        return {
          og_image: ogImg ? ogImg.content : null,
          og_desc: ogDesc ? (ogDesc.content || '').substring(0, 150) : null,
          og_title: ogTitle ? (ogTitle.content || '').substring(0, 100) : null
        };
      });

      results.push({ url, ...data });
    } catch (e) {
      results.push({ url, error: e.message.substring(0, 80) });
    }
  }

  return JSON.stringify(results);
}
```

### B.3 Perfil do Instagram (se tem username)

Navegue no perfil para pegar a foto de perfil (og:image) e os LINKS dos posts:

```
browser_navigate: https://www.instagram.com/{username}/
```

**IMPORTANTE: NAO extraia imagens da grid diretamente.** As imagens renderizadas na grid sao thumbnails 150x150 (parametro `s150x150` na URL) — inutilizaveis para um site.

Em vez disso:
1. Scroll a grid para carregar TODOS os posts (nao apenas os primeiros visiveis)
2. Extraia os LINKS dos posts
3. Navegue em cada post (B.2) para pegar og:image em alta resolucao

```javascript
// PASSO 1: Scroll para carregar mais posts
browser_evaluate: (async () => {
  let prevCount = 0;
  for (let i = 0; i < 8; i++) {
    window.scrollTo(0, document.body.scrollHeight);
    await new Promise(r => setTimeout(r, 2000));
    const links = document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]');
    if (links.length === prevCount) break;
    prevCount = links.length;
  }
  window.scrollTo(0, 0);
  return `Loaded ${prevCount} posts`;
})()
```

```javascript
// PASSO 2: Extrair todos os links de posts
browser_evaluate: (() => {
  const ogImg = document.querySelector('meta[property="og:image"]');
  const postLinks = [];
  document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]').forEach(a => {
    postLinks.push(a.href);
  });
  return JSON.stringify({
    og_image: ogImg ? ogImg.content : null,
    post_links: [...new Set(postLinks)]
  });
})()
```

Depois navegue em CADA post_link usando o metodo B.2 para extrair og:image em alta resolucao.

**IMPORTANTE — Imagens com texto sao valiosas:**
Posts com texto (cardapios, listas de servicos, horarios, promocoes, depoimentos) servem como FONTE DE INFORMACAO para enriquecer o briefing. Ao navegar em cada post:
- Extraia og:description (contem o caption do post)
- Se a imagem contem texto visivel, registre no data_point: `"has_text": true`
- Esses dados serao usados na imersao (site-phase-2) para extrair conteudo real do cliente

### B.4 Plataformas com JS-rendered content

Para URLs de plataformas encontradas nas fases anteriores ou na Etapa B.1:

**Se Chrome DevTools MCP disponivel (preferido para plataformas normais):**
1. Navegar para a URL da plataforma via Chrome DevTools
2. Usar Network tab para capturar TODAS as requests de imagem automaticamente
3. Filtrar por tipo `image` — captura lazy-loaded, CDN redirects, e imagens que o DOM nao expoe
4. Vantagem: nao precisa adivinhar seletores CSS — o Network mostra tudo que carregou

**Se usando Playwright (fallback ou se Chrome DevTools indisponivel):**

**iFood:** Navegar na pagina do restaurante e extrair og:image + fotos de pratos
```
browser_navigate: {url_ifood}
browser_evaluate: (() => {
  const ogImg = document.querySelector('meta[property="og:image"]');
  const imgs = document.querySelectorAll('img[src*="static-images.ifood"]');
  const urls = [];
  imgs.forEach(i => { if (i.naturalWidth > 50) urls.push(i.src); });
  return JSON.stringify({
    og_image: ogImg ? ogImg.content : null,
    food_photos: [...new Set(urls)]
  });
})()
```

**Rappi:** Mesmo padrao — navegar e extrair imagens de pratos.

**Doctoralia:** Navegar e extrair foto do profissional.

**TripAdvisor:** Navegar e extrair fotos do estabelecimento.

### B.5 Se Playwright nao estiver disponivel

Se as ferramentas browser_* nao estiverem disponiveis (MCP desconectado):
- Registre no state: `"playwright_unavailable": true`
- A Etapa A sozinha ja coletou imagens via WebSearch+WebFetch
- Continue normalmente — Playwright e bonus, nao requisito bloqueante
- Avise ao usuario: "Playwright MCP nao disponivel. Imagens limitadas ao WebSearch+WebFetch."

---

## ETAPA C — Imagens Genericas (Stock MCPs)

Se apos as Etapas A e B o lead tem POUCAS imagens para backgrounds e texturas, complemente com imagens genericas via MCPs de stock:

**MCPs disponiveis:**
- `mcp__stock-images` — Unsplash + Pexels + Pixabay simultaneamente
- `mcp__mcp-pexels` — Pexels (alta qualidade)
- `mcp__pixabay` — Pixabay (fotos + videos)
- `mcp__freepik` — Freepik (vetores, fotos, PSD)

**Busque pelo conceito, NAO pelo nicho:**
- Ex: restaurante sofisticado → "dark wood texture elegant", "warm ambient restaurant bokeh"
- Ex: clinica medica → "clean abstract medical blue", "minimalist wellness texture"

**Valido APENAS para:**
- ✅ Backgrounds atmosfericos e texturas (wood, marble, abstract, smoke)
- ✅ Elementos decorativos (patterns, grain, bokeh, light leaks)
- ✅ Icones e ilustracoes vetoriais (via freepik)

**NUNCA para (REGRA INVIOLAVEL):**
- ❌ Foto do profissional/dono
- ❌ Fachada/interior do local
- ❌ Produtos/pratos do cardapio
- ❌ Equipe/funcionarios
- ❌ Logo

Salve como data_points com `source_name: "Stock (Pexels)"` etc., tipo `"background"` ou `"texture"`.

---

## ETAPA D — Validacao & Deduplicacao

### D.1 Validar pertencimento
Cada imagem DEVE pertencer ao lead correto:
- Se buscou `"barbeariaancorador" site:instagram.com`, so use se URL contem `/barbeariaancorador/`
- Se buscou `"Barbearia Ancorador" site:ifood.com.br`, verifique se nome no resultado bate
- Se Google retornou perfis parecidos mas diferentes, DESCARTE

### D.2 Deduplicar
Compare URLs encontradas na Etapa B contra imagens ja coletadas nas fases 2-5 e Etapa A.
Remova duplicatas (mesma URL ou mesmo dominio+path).

### D.3 Classificar
Para cada imagem, classifique o tipo:
- `profile_pic` — foto de perfil (Instagram, Facebook)
- `logo` — logotipo (site, Google, iFood)
- `fachada` — foto do local/fachada
- `produto` — foto de produto/prato
- `equipe` — foto da equipe/profissional
- `banner` — banner/capa (Facebook, site)
- `post` — post de rede social
- `outro` — nao classificavel

### D.4 Salvar como data_points

Cada imagem = 1 data_point:
```json
{
  "category": "images",
  "label": "Foto de perfil Instagram",
  "value": "https://scontent-xxx.cdninstagram.com/v/...",
  "detail": {
    "urls": ["url1", "url2"],
    "tipo": "profile_pic",
    "fonte": "Playwright (Instagram post)",
    "width": 320,
    "height": 320
  },
  "source_type": "briefing",
  "source_name": "Playwright MCP",
  "fetched_at": "..."
}
```

Agrupe URLs similares (mesma fonte/tipo) em `detail.urls` para galeria.

## Salvar no state

Append todos data_points de imagem ao state. Mostre ao usuario:
```
IMAGENS CAPTURADAS NESTA FASE:
  Instagram (Playwright): X imagens
  iFood (CDN): X imagens
  Rappi (CDN): X imagens
  WebSearch/WebFetch: X imagens
  Total novos: X | Total acumulado: Y
```

---

## ETAPA E — Download de Videos (Reels Instagram via yt-dlp)

Se o perfil tem reels (URLs com `/reel/` coletadas na Etapa B), baixar os videos para uso no site.

### E.1 Verificar/instalar yt-dlp + ffmpeg
```bash
which yt-dlp || brew install yt-dlp ffmpeg
yt-dlp --version
```

### E.2 Coletar URLs de reels do grid

Usar o scroll cumulativo da Etapa B.3 ou o thumbnails.json se ja salvo:
```bash
# Se tem thumbnails.json com posts tipados:
jq -r '.posts[] | select(.type == "reel") | .href | capture("/reel/(?<c>[^/]+)") | .c' \
  data/enrichment/{slug}/thumbnails.json > reel_codes.txt

# OU se so tem lista de URLs, filtrar reels:
grep "/reel/" post_urls.txt | sed 's|.*/reel/||;s|/||' > reel_codes.txt
```

### E.3 Download em paralelo (max 4 simultaneos)
```bash
mkdir -p data/enrichment/{slug}/videos
cat reel_codes.txt | xargs -P 4 -I {} yt-dlp -q --no-warnings --no-progress \
  -o "data/enrichment/{slug}/videos/reel_{}.%(ext)s" \
  "https://www.instagram.com/{username}/reel/{}/"
```

**yt-dlp automaticamente:**
- Detecta o formato otimo (1080p/720p/540p)
- Usa ffmpeg para muxar video + audio em MP4
- Resolve DASH segmentation (video-only + audio-only → MP4 final)

### E.4 Limites
- Se perfil tem > 50 reels, baixar apenas os 30 mais recentes
- Se yt-dlp falhar (rate limit Instagram), registrar no report e continuar com thumbnails
- NAO baixar reels de perfis que NAO sao do cliente (tagged posts de @outrousuario)
- Se for perfil da MARCA (ex: @cervusbarbearia), baixar so os 15 top (referencia visual)

### E.5 Data point
```json
{
  "category": "media",
  "label": "Videos (reels) do Instagram",
  "value": "30 videos MP4 (232MB)",
  "detail": {
    "path": "data/enrichment/{slug}/videos/",
    "total": 30,
    "tool": "yt-dlp",
    "quality": "auto (1080p preferred)",
    "format": "MP4 H.264 + AAC muxed"
  },
  "source_type": "briefing",
  "source_name": "yt-dlp"
}
```

### E.6 Captura de captions (legendas) dos posts

Para TODOS os posts (nao so reels), capturar captions via fetch() dentro da pagina logada:

```javascript
// Dentro do browser_evaluate, apos login:
const res = await fetch('/p/{shortcode}/', { credentials: 'include' });
const html = await res.text();
const desc = html.match(/<meta property="og:description" content="([^"]+)"/);
// Parse: "X likes, Y comments - user no Date: \"caption\"."
```

Salvar as captions em `data/enrichment/{slug}/captions.json`. Sao fonte de copy para o site.

---

---

## ETAPA F — Vision Analysis Per-Image (OBRIGATORIO)

Apos baixar TODAS as imagens (Etapas A-E completas), Claude precisa **abrir cada imagem com Read tool** e produzir um manifesto semantico. Sem isso, o site-builder atribui imagens por filename (heuristica burra) e a maioria das imagens fica orfa.

### F.1 Iterar imagens baixadas

Lista todos os arquivos de imagem:
```bash
find data/enrichment/{slug}/ -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.webp" \) -size +5k
```

Pra cada arquivo, fazer:
```
Read: data/enrichment/{slug}/{path-to-image}
```

A Read tool entrega a imagem visualmente pro Claude. **NAO pular**: cada imagem MUST ser aberta individualmente.

### F.2 Tagging semantico por imagem

Apos abrir cada imagem, escrever um objeto JSON com TAGS DERIVADAS DO QUE VOCE REALMENTE VE NA IMAGEM (nao do filename):

```json
{
  "file": "post-hero-8.jpg",
  "size_kb": 142,
  "content_type": "interior_atmospheric|portrait|process_at_work|community_group|product|texture|logo|exterior|other",
  "subjects": ["barbearia", "cadeira de couro", "iluminacao quente", "espelho"],
  "people_count": 0,
  "people_age_estimate": "n/a|child|young_adult|adult|elderly",
  "tone": "warm|cool|neutral|mixed",
  "lighting": "low|natural|studio|golden_hour|harsh",
  "color_palette": ["#3a2515", "#a08050", "#1c1410"],
  "has_text_overlay": false,
  "text_content_if_any": null,
  "is_logo_or_brand_mark": false,
  "looks_professional": true,
  "looks_staged_or_candid": "candid",
  "best_use_case": "S1 hero background — atmospheric tavern interior",
  "do_not_use_for": ["portrait section", "service catalog"],
  "recommended_sections": ["s1", "s2_background"],
  "fingerprint_summary": "Dark wood barbershop interior, leather chair, warm low light, no people"
}
```

**Regras de tagging:**
- `content_type` deve ser UMA das categorias listadas, baseado no conteudo principal
- `recommended_sections` use slugs genericos: `s1` (hero/opening), `s2` (about/portrait), `s3` (services/process), `s4` (social proof/community), `s5` (contact/closing). O builder mapeia depois pra Section Purpose Map real.
- Se a imagem tem play button overlay (Reel thumbnail), `content_type: "video_thumbnail_with_overlay"` E `do_not_use_for` deve incluir `"any direct rendering"` — descartar visualmente, mas registrar que existe video correspondente
- Se a imagem e claramente o LOGO da marca (simbolo + tipografia, fundo neutro), `is_logo_or_brand_mark: true` E `recommended_sections: ["s1_seal", "s5_seal", "navbar"]`
- Se a imagem tem 1 pessoa em pose de retrato (rosto centralizado), `content_type: "portrait"` E `recommended_sections: ["s2"]`
- Se mostra trabalho em andamento (maos no produto/cliente), `content_type: "process_at_work"` E `recommended_sections: ["s3"]`
- Se mostra grupo (2+ pessoas interagindo), `content_type: "community_group"` E `recommended_sections: ["s4"]`

### F.3 Salvar manifesto

```bash
mkdir -p data/enrichment/{slug}/
# Escrever todos os objetos como array JSON em:
data/enrichment/{slug}/images-manifest.json
```

Schema final:
```json
{
  "version": 1,
  "lead_slug": "{slug}",
  "generated_at": "ISO8601",
  "vision_analyzer": "claude-via-read-tool",
  "total_analyzed": N,
  "entries": [ ... objetos da F.2 ... ]
}
```

### F.4 Salvar tambem como data_point

```json
{
  "category": "images",
  "label": "Vision analysis manifest (per-image semantic tags)",
  "value": "data/enrichment/{slug}/images-manifest.json",
  "detail": { "total_analyzed": N, "categories_distribution": {...} },
  "source_type": "briefing",
  "source_name": "Claude vision (Read tool)"
}
```

### F.5 Reels videos: cross-reference

Se Etapa E baixou reels MP4, adicionar entrada por video tambem (mesmo schema, com `content_type: "video_reel"` e `file` apontando pro MP4). Os videos aparecem no manifesto junto com as imagens — Phase 4 do build-site usa pra decidir onde embedar vídeo background.

---

## CRITERIO DE CONCLUSAO
- Etapa A executada: WebSearch + WebFetch + coleta de links de posts
- Etapa B executada: Playwright navegou nos posts e extraiu og:image (se disponivel)
- **B.0: Profile pic capturada e ANALISADA visualmente (Read tool)**
- **B.0a: Analise visual do grid documentada (padroes, paleta, tipografia)**
- NAO tentou extrair URLs de imagem do Google Images DOM (armadilha!)
- URLs validadas (pertencem ao lead correto)
- Deduplicadas contra fases anteriores
- Classificadas por tipo
- **Etapa E: Videos (reels) baixados via yt-dlp (se perfil tem reels)**
- **Etapa F: Vision analysis per-image executada, images-manifest.json gerado**
- Pelo menos 1 imagem capturada (ou "nenhuma encontrada" registrado explicitamente)
