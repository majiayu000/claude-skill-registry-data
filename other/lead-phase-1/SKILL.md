---
name: lead-phase-1
description: Fase 1 do lead-finder — Gerar queries inteligentes e checar cache local
user-invocable: false
---

# Fase 1 — Gerar Queries + Cache Local

Leia os argumentos: $ARGUMENTS

## 1.1 Parsear parametros

Extraia:
- `--nicho "X"` → profissao/nicho (obrigatorio sem --perfil-exemplo)
- `--cidade "X"` → cidade
- `--perfil-exemplo @X` → perfil modelo (pula direto pra validacao)
- `--max-idade-conta N` → so contas com 1o post nos ultimos N dias
- `--max-idade-post N` → so contas que postaram nos ultimos N dias
- `--so-comercial` → so contas Business/Creator
- `--sem-site` → so sem site na bio
- `--limite N` → max leads desejados (default: 10)
- `--modo influencer` → ativa MODO INFLUENCER (queries + scoring de criadora)
- `--min-seguidores N` / `--max-seguidores N` → gate de faixa (modo influencer)
- `--regiao "Sul,Sudeste"` / `--genero F` / `--faixa-idade "35-50"` → modo influencer

> **MODO INFLUENCER**: se `--modo influencer`, salve em `filtros.modo="influencer"`
> e gere queries cruzando **cidades de S/SE** × **keywords de bio materna**
> (banco completo em `research/influencer-mae-sul-sudeste.md`). Ex.:
> `site:instagram.com "maternidade real" "curitiba"`,
> `site:instagram.com "mãe de adolescente" "porto alegre"`. Cache/CSV =
> `leads/influencers_mae_sul_sudeste.csv`. Pule a logica de nicho-profissional padrao.

## 1.2 Gerar queries inteligentes

PENSE como um profissional desse nicho se apresenta no Instagram.

**Como o profissional escreve na bio:**
- Psicologo: "psicologa", "terapia", "saude mental", "atendimento", "CRP"
- Medico: "dra.", "dr.", "clinica", "CRM", "consultorio"
- Dentista: "odontologia", "sorriso", "CRO", "implante"
- Advogado: "advogado", "escritorio", "OAB", "direito"
- Nutricionista: "nutri", "nutricionista", "alimentacao", "CRN"
- Restaurante: "restaurante", "gastronomia", "delivery", "comida"
- Barbearia: "barbeiro", "barbearia", "corte", "barba"

**Como o username e formatado:**
- `psicologa.nome`, `dra.nome`, `nome.nutri`, `odonto.nome`, `adv.nome`

**Variacoes de cidade:**
- Florianopolis → "floripa", "florianopolis", "florianópolis"
- Belo Horizonte → "BH", "belo horizonte", "beaga"
- Sao Paulo → "SP", "sao paulo", "sampa"

**Gere 5-8 queries no formato:**
```
site:instagram.com "psicologa" "florianopolis"
site:instagram.com "psicologo" "floripa"
site:instagram.com "terapia" "florianopolis"
site:instagram.com "saude mental" "floripa"
site:instagram.com "CRP" "florianopolis"
site:instagram.com "psicologa" "florianópolis"
```

## 1.3 Checar cache local (ZERO custo)

Leia TODOS os CSVs em leads/*.csv:
```bash
ls leads/*.csv 2>/dev/null
```

Filtre por parametros da busca atual:
- Se --nicho: filtrar pela coluna "bio" ou "category" contendo o nicho
- Se --cidade: filtrar pela coluna "bio" contendo a cidade
- Se --sem-site: filtrar has_real_site = false
- Se --so-comercial: filtrar account_type != Personal

Se encontrar perfis que batem:
```
Encontrei X perfis no banco local que batem com sua busca:
@user1 (QUENTE, score 7) | @user2 (MORNO, score 4) ...
Preciso buscar mais Y perfis. Iniciando Google + Playwright...
```

Se meta atingida: "Todos os leads ja estao no banco!"

## 1.4 Montar chave de cache

Combine para dedup: `"nicho|cidade|filtros"` → param_key
Ex: `"psicologo|florianopolis|sem_site"`

## 1.5 Salvar no state

Salve: nicho, cidade, limite, filtros, queries, param_key, leads_do_cache.

## CRITERIO DE CONCLUSAO
- Params parseados
- 5-8 queries geradas
- Cache local checado
- Meta calculada (limite - encontrados_cache = faltam)
- State file atualizado
