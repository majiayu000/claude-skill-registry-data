---
name: lead-phase-5
description: Fase 5 do lead-finder — Auto-referencia via perfis similares
user-invocable: false
---

# Fase 5 — Auto-referencia (Similares)

**FERRAMENTAS:** APENAS Playwright MCP. NUNCA instagrapi API.

Leia o state file:
```bash
cat data/_state/lead-finder-progress.json
```

Se ja atingiu --limite: PULE esta fase, va direto para Fase 6.

## 5.1 Selecionar leads QUENTES para referencia

Dos leads encontrados na Fase 4, pegue os classificados como QUENTE (score >= 6).
Se nenhum QUENTE, pegue os MORNOS (score >= 3).
Selecione no maximo 3 perfis para buscar similares.

## 5.2 Buscar similares via navegacao

Para cada perfil selecionado:

### Metodo A — Secao "Sugeridos" na pagina do perfil

```
browser_navigate: https://www.instagram.com/{username}/
```

Espere carregar. No perfil, procure a seta/chevron ao lado de "Seguir" que abre sugeridos:

```javascript
browser_evaluate: (() => {
  // Procurar botao de "sugeridos" ou "similar accounts"
  // Geralmente e um icone de seta para baixo perto do botao Follow
  const svgs = document.querySelectorAll('svg[aria-label*="Similar"], svg[aria-label*="sugest"], button[aria-label*="Similar"]');
  if (svgs.length > 0) {
    svgs[0].closest('button')?.click();
    return 'clicked_similar_button';
  }

  // Alternativa: scroll down e procurar secao de sugeridos
  return 'no_similar_button_found';
})()
```

Se clicou, espere 2 segundos e extraia:

```javascript
browser_evaluate: (() => {
  // Apos clicar, Instagram mostra uma lista de perfis sugeridos
  // Procurar links para perfis
  const links = document.querySelectorAll('a[href^="/"]');
  const usernames = [];
  links.forEach(a => {
    const href = a.getAttribute('href') || '';
    // Filtrar: so usernames (nao /p/, /reel/, /explore/, etc)
    if (href.match(/^\/[a-zA-Z0-9._]+\/$/) && !href.includes('/p/') &&
        !href.includes('/explore/') && !href.includes('/reel/')) {
      const username = href.replace(/\//g, '');
      if (username.length > 2 && username !== 'instagram') {
        usernames.push(username);
      }
    }
  });
  return JSON.stringify([...new Set(usernames)].slice(0, 15));
})()
```

### Metodo B — Google como fallback

Se o Metodo A nao encontrou sugeridos:

```
WebSearch: site:instagram.com "{nicho}" "{cidade}" similar a @{username}
```

Ou buscar com termos da bio do lead:
```
WebSearch: site:instagram.com "{palavras_chave_da_bio}" "{cidade}"
```

Extrair usernames dos resultados (mesmo metodo da Fase 2).

## 5.3 Filtrar e adicionar candidatos

Dos usernames encontrados:
1. Remover usernames ja validados (Fase 4 ou cache)
2. Remover duplicatas
3. Adicionar ao INICIO da lista de candidatos no state

## 5.4 Voltar para Fase 4

Se ha novos candidatos E ainda nao atingiu --limite:
- O orchestrator deve re-invocar `/lead-phase-4` com os novos candidatos
- Fase 4 continua o loop de onde parou

Mostre ao usuario:
```
Auto-referencia: X perfis similares encontrados a partir de @{username}
Novos candidatos: Y (apos dedup)
Continuando validacao...
```

## CRITERIO DE CONCLUSAO
- Leads QUENTES usados como referencia
- Sugeridos extraidos via Playwright ou Google
- Novos candidatos deduplicados e adicionados ao state
- Se nenhum sugerido encontrado: registrar e seguir para Fase 6
