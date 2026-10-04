---
name: enrich-phase-2
description: Fase 2 do enrich-lead — Pesquisas universais (texto, sem imagens)
user-invocable: false
---

# Fase 2 — Pesquisas Universais

Leia o state file para obter nome, cidade, nicho:
```bash
cat data/_state/enrichment-progress.json
```

## REGRA DE OURO

**WebSearch so encontra LINKS. Para obter dados REAIS voce DEVE fazer WebFetch em cada pagina relevante encontrada.**

Se voce encontrou um link relevante e NAO fez WebFetch nele, a fase esta incompleta.

## 2.1 Presenca geral
```
WebSearch: "{nome}" "{cidade}"
```
Analise os resultados: procure site oficial, perfis de redes sociais, Google Business, noticias, avaliacoes.

## 2.2 Buscar site
```
WebSearch: "{nome}" "{cidade}" site OR website
```
Se encontrar um site, anote a URL — sera usado na Fase 4.

## 2.3 Redes sociais
```
WebSearch: "{nome}" "{cidade}" instagram.com OR facebook.com OR linkedin.com OR youtube.com OR tiktok.com
```
Para cada rede encontrada, anote username e URL.

## 2.4 Avaliacoes e reputacao
```
WebSearch: "{nome}" "{cidade}" avaliacao OR review OR opiniao
```
Capture: nota media, numero de avaliacoes, principais reclamacoes.

## 2.5 Historia da empresa
```
WebSearch: "{nome}" "{cidade}" sobre OR historia OR "quem somos" OR about
```
Busque: quando fundada, por quem, missao, como comecou.

## WebFetch em tudo relevante

Para CADA link relevante encontrado nas buscas acima:
- Site oficial? → WebFetch (sera aprofundado na Fase 4, mas ja anote a URL)
- Perfil Instagram? → Anote username para Fase 6
- Perfil Facebook? → WebFetch para og:image e og:description
- Google Business? → Anote URL
- Artigo/noticia? → WebFetch se menciona o lead

## Salvar discovered_urls no state

Atualize o state file com TODAS as URLs descobertas:
```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
.venv/bin/python3 -c "
import json
with open('data/_state/enrichment-progress.json') as f: state = json.load(f)
state['discovered_urls']['site_url'] = 'URL_OU_VAZIO'
state['discovered_urls']['instagram_username'] = 'USERNAME_OU_VAZIO'
state['discovered_urls']['facebook_url'] = 'URL_OU_VAZIO'
state['discovered_urls']['google_maps_url'] = 'URL_OU_VAZIO'
# Adicionar data_points coletados
new_points = []
# Para cada dado coletado, crie um data_point:
# {'category': 'presence', 'label': '...', 'value': '...', 'detail': {...}, 'source_type': 'briefing', 'source_name': 'WebSearch', 'fetched_at': '...'}
state['data_points'].extend(new_points)
state['current_phase'] = 2
state['phases']['phase_2'] = {'status': 'complete', 'result': 'X URLs descobertas, Y data_points'}
with open('data/_state/enrichment-progress.json', 'w') as f: json.dump(state, f, indent=2, ensure_ascii=False)
print(f'Fase 2 completa. {len(new_points)} data_points adicionados.')
"
```

## Formato de cada data_point

```json
{
  "category": "presence|reviews|history|social",
  "label": "Descricao curta",
  "value": "Valor principal",
  "detail": { "...dados extras..." },
  "source_type": "briefing",
  "source_name": "WebSearch|WebFetch ({url})",
  "fetched_at": "ISO timestamp"
}
```

## CRITERIO DE CONCLUSAO
- 5+ WebSearches executadas
- WebFetch em todo link relevante encontrado
- discovered_urls populado no state (site, instagram, facebook, google_maps)
- data_points de presenca, reviews, historia salvos no state
- Se alguma busca nao retornou resultado: registrar "Nao encontrado" e seguir
