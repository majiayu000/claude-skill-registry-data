---
name: enrich-phase-5
description: Fase 5 do enrich-lead — Canais de venda e extracao por plataforma
user-invocable: false
---

# Fase 5 — Canais de Venda & Plataformas

Leia o state file:
```bash
cat data/_state/enrichment-progress.json
```

Extraia: nome, cidade, nicho, strategy, discovered_urls.

## 5.1 Pesquisar canais por nicho

Execute as pesquisas RELEVANTES ao nicho:

**food (restaurante, hamburgueria, pizzaria, etc):**
```
WebSearch: "{nome}" "{cidade}" site:ifood.com.br
WebSearch: "{nome}" "{cidade}" site:rappi.com.br
WebSearch: "{nome}" "{cidade}" anotaai
WebSearch: "{nome}" "{cidade}" site:ubereats.com
```

**medical, dental, psychology (saude):**
```
WebSearch: "{nome}" "{cidade}" site:doctoralia.com.br
WebSearch: "{nome}" "{cidade}" site:boaconsulta.com
```

**hospitality (hospedagem, hotel, pousada):**
```
WebSearch: "{nome}" "{cidade}" site:booking.com
WebSearch: "{nome}" "{cidade}" site:tripadvisor.com.br
WebSearch: "{nome}" "{cidade}" site:airbnb.com.br
```

**realty (imobiliaria):**
```
WebSearch: "{nome}" "{cidade}" site:zapimoveis.com.br
WebSearch: "{nome}" "{cidade}" site:vivareal.com.br
```

**education (escola):**
```
WebSearch: "{nome}" "{cidade}" site:reclameaqui.com.br
WebSearch: "{nome}" "{cidade}" matricula
```

**beauty (beleza, barbearia):**
```
WebSearch: "{nome}" "{cidade}" agendamento OR reserva
WebSearch: "{nome}" "{cidade}" site:booksy.com
```

**generic / qualquer nicho:**
```
WebSearch: "{nome}" "{cidade}" site:reclameaqui.com.br
```

## 5.2 WebFetch em CADA canal encontrado

Para CADA perfil encontrado, faca WebFetch e extraia dados usando o guia por plataforma:

### INSTAGRAM (se username conhecido)
```
WebFetch: https://www.instagram.com/{username}/
```
Extraia: og:image (foto perfil), og:description (bio + seguidores), og:title (nome).

### IFOOD
URL tipica: `https://www.ifood.com.br/delivery/{cidade}/{slug}/{uuid}`
```
WebFetch: {url_encontrada}
```
Extraia:
- og:image (logo/foto do restaurante)
- JSON-LD (`<script type="application/ld+json">`) → nome, endereco, telefone, cozinha
- Menu items: nome + preco + descricao + imagem (CDN static-images.ifood.com.br)
- Rating e review count

Salve como:
- category "sales_channels" → dados do perfil
- category "menu" → cardapio com itens e precos
- category "images" → fotos de pratos (detail.urls)

### RAPPI
URL tipica: `https://www.rappi.com.br/restaurantes/{id}-{slug}`
```
WebFetch: {url_encontrada}
```
Extraia: og:image, cardapio com precos, fotos.

### DOCTORALIA
URL tipica: `https://www.doctoralia.com.br/{nome}/{especialidade}/{cidade}`
```
WebFetch: {url_encontrada}
```
Extraia:
- og:image (foto profissional)
- JSON-LD (dados estruturados)
- Nota e avaliacoes
- Depoimentos (3 mais recentes)
- Servicos/tratamentos
- Precos e convenios

### TRIPADVISOR
```
WebFetch: {url_encontrada}
```
Extraia: og:image, ranking, nota, avaliacoes, tipo cozinha, faixa preco, fotos, top 3 reviews.

### BOOKING / AIRBNB
```
WebFetch: {url_encontrada}
```
Extraia: og:image, nota, avaliacoes, precos, fotos, comodidades.

### RECLAME AQUI
```
WebFetch: {url_encontrada}
```
Extraia: nota reputacao, taxa resposta, taxa solucao, reclamacoes, se responde.

### FACEBOOK
```
WebFetch: https://www.facebook.com/{pagina}/
```
Extraia: og:image, og:description, curtidas/seguidores.

### GOOGLE MAPS
Se tem google_maps_url:
```
WebFetch: {google_maps_url}
```
Extraia: fotos (googleusercontent.com URLs), avaliacoes, horario, endereco, telefone.

### REGRA GERAL PARA QUALQUER PLATAFORMA
1. Extraia og:image (sempre existe)
2. Procure `<script type="application/ld+json">` (dados estruturados)
3. Procure `<img>` com src relevante (ignore icones pequenos)
4. Extraia textos (og:description, meta description)

## 5.3 Organizacao dos data_points

Para cada plataforma, crie data_points separados:
- `category: "sales_channels"` → presenca, avaliacao, status
- `category: "menu"` → itens com precos e descricoes (se nicho food)
- `category: "images"` → TODAS URLs de imagem com detail.urls + detail.fonte
- `category: "reviews"` → avaliacoes e depoimentos

## Salvar no state

Append todos data_points e atualizar platform_urls no discovered_urls.

## CRITERIO DE CONCLUSAO
- Buscas niche-specific executadas
- WebFetch em CADA perfil encontrado
- Extracao profunda por plataforma (og:image, JSON-LD, dados especificos)
- data_points organizados por categoria
- Se nenhum canal encontrado: registrar e seguir
