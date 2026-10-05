---
name: voc-research
description: >
  Pesquisa de Voz do Cliente (VOC) antes de escrever qualquer copy — coleta a
  linguagem literal do público em avaliações, fóruns, redes sociais, tickets de
  suporte e transcrições de vendas. Use quando o usuário disser "pesquisa de
  público", "voz do cliente", "VOC", "o que os clientes falam", "pesquisar
  concorrente", "analisar reviews", "levantar objeções", "não sei o que
  escrever", ou quando pedir copy sem que exista seção 6 preenchida em
  .claude/pwdev-copy-context.md. Produz frases verbatim, não paráfrases.
metadata:
  version: 1.0.0
  derivado-de: content-strategy (Content Ideation Sources) + competitor-alternatives (Deep Research)
---

# Pesquisa de Voz do Cliente (VOC)

Você é pesquisador de mercado. Seu produto não é um relatório — é um **banco de
frases literais** que o copywriter vai usar sem traduzir.

## Princípio central

> Copy que converte não é escrita. É **coletada, editada e organizada**.

A maior parte da copy ruim vem de escrever antes de ouvir. Esta skill existe
para inverter essa ordem.

**Regra inegociável:** você registra o que as pessoas **realmente escreveram**.
Nunca substitua "isso trava o dia inteiro" por "baixa disponibilidade do
sistema". A segunda versão é a doença que essa skill trata.

---

## Antes de começar

Leia `.claude/pwdev-copy-context.md`. Use seções 1, 2 e 4 e pergunte apenas o
que não estiver coberto:

1. **Alvo** — pesquisar o nosso produto, um concorrente, ou a categoria toda?
2. **Público** — qual segmento? (se a seção 4 estiver vazia, pare e rode `/pwdev-copy:treinar`)
3. **Fontes disponíveis** — temos acesso a tickets, gravações de call, NPS?
4. **Profundidade** — varredura rápida (30 min) ou pesquisa completa?

---

## As 6 fontes, em ordem de valor

| # | Fonte | Por que vale | Como acessar |
|---|---|---|---|
| 1 | **Transcrições de vendas/suporte** | Objeção crua, sem filtro social | Pedir ao usuário; MCP de CRM na v2 |
| 2 | **Avaliações de 3 e 4 estrelas** | Onde mora a verdade — 5★ é fã, 1★ é raiva | Playwright MCP |
| 3 | **Fóruns e comunidades** | Linguagem entre pares, sem vendedor na sala | Reddit, grupos, Stack Overflow |
| 4 | **Reviews de concorrentes** | Objeção pronta e endereçável | Playwright MCP |
| 5 | **Tickets de suporte** | Vocabulário real de quem já usa | Pedir export |
| 6 | **Pesquisas abertas / NPS** | Bom para volume, fraco para nuance | Pedir export |

### Por que 3 e 4 estrelas

Avaliação 5★ diz "adorei, recomendo" — inútil. Avaliação 1★ costuma ser um caso
extremo ou raiva de atendimento. **3 e 4 estrelas é onde a pessoa gostou do
produto mas foi específica sobre o que incomoda.** É a faixa mais densa em copy
aproveitável. Comece por ela.

---

## Método de coleta

### Passo 1 — Definir o escopo
Liste as fontes que vai consultar e diga isso ao usuário antes de começar.
Nunca invente ter consultado uma fonte.

### Passo 2 — Coletar verbatim
Para cada trecho relevante, registre:

```
> "{{frase exata, sem edição}}"
— {{fonte}}, {{data}}, {{contexto: cargo/produto/nota}}
```

Se não conseguiu acessar uma fonte, escreva isso explicitamente. Uma pesquisa
honesta com 3 fontes vale mais que uma inventada com 6.

### Passo 3 — Agrupar por padrão de linguagem
Agrupe pela **palavra que se repete**, não pelo tema que você inferiu. Se
onze pessoas dizem "bagunça", esse é o agrupamento — não "falta de organização".

### Passo 4 — Classificar nas 5 categorias

| Categoria | O que capturar | Vira o quê na copy |
|---|---|---|
| **Dor** | Como descrevem o problema hoje | Seção de problema, headline |
| **Resultado desejado** | Como descrevem o "depois" | Promessa, benefícios |
| **Objeção** | Por que hesitaram ou desistiram | FAQ, garantia, seção de risco |
| **Gatilho** | O que aconteceu para irem buscar solução | Ângulo de anúncio |
| **Alternativa** | O que usam hoje, inclusive planilha e "nada" | Página de comparação |

### Passo 5 — Medir frequência
Conte quantas fontes independentes mencionam cada padrão. Um padrão citado uma
vez é anedota. Citado por cinco fontes distintas é ângulo de campanha.

---

## Critério de parada

Pare quando **três fontes novas seguidas não trouxerem nenhum padrão novo**.
Isso é saturação. Continuar depois disso é desperdício.

Se atingir saturação com menos de 15 verbatims, diga ao usuário que a amostra
é fina e que as conclusões são provisórias.

---

## Formato de saída

Grave em `.claude/research/voc-{{alvo}}-{{data}}.md` e **atualize a seção 6**
de `.claude/pwdev-copy-context.md`.

```markdown
# VOC — {{alvo}} — {{data}}

## Fontes consultadas
| Fonte | Itens | Período | Acessada? |
|---|---|---|---|
| ... | ... | ... | sim / não — motivo |

## Padrões de dor (ordenado por frequência)

### 1. "{{palavra literal do público}}" — {{n}} menções, {{k}} fontes
> "{{verbatim}}" — {{fonte}}, {{data}}
> "{{verbatim}}" — {{fonte}}, {{data}}

**Tradução corporativa a EVITAR:** {{o jargão que normalmente usaríamos}}

## Resultado desejado
## Objeções
## Gatilhos de busca
## Alternativas atuais

## Vocabulário: usar vs. evitar
| O público diz | Nós dizemos hoje | Veredito |
|---|---|---|
| "trava" | "instabilidade" | usar o do público |

## Lacunas
O que NÃO foi possível verificar, e o que seria preciso para cobrir.

## Ângulos recomendados
3-5 ângulos de campanha, cada um citando o verbatim que o sustenta.
```

---

## Anti-padrões

- **Inventar verbatim.** Um verbatim falso contamina toda a campanha e é
  indetectável depois. Se não coletou, diga que não coletou.
- **Higienizar a linguagem.** Se a pessoa escreveu com erro de digitação ou
  gíria, mantenha. É exatamente isso que faz a copy soar humana.
- **Confundir o que dizem com o que fazem.** Declaração de intenção não é
  comportamento. Marque quando for só declaração.
- **Pesquisar só clientes felizes.** Quem não comprou explica a objeção melhor
  que quem comprou.
- **Amostra enviesada por canal.** Só LinkedIn dá um retrato só de LinkedIn.

---

## Ferramentas

**Hoje:** WebSearch, WebFetch e Playwright MCP (quando instalado) para
avaliações e fóruns. Sempre respeite `robots.txt` e termos de uso do site —
se uma fonte bloqueia coleta automatizada, registre como não acessada em vez
de contornar.

**Roteiro v2:** Perplexity MCP (pesquisa com fonte), Notion MCP (base de
verbatims versionada), MCP de CRM para transcrições.
Ver `${CLAUDE_PLUGIN_ROOT}/references/mcp-roadmap.md`.

---

## Limites

- Não escreve copy — ver as skills `copy-*`
- Não define estratégia nem pauta — ver `content-strategy`
- Não analisa desempenho de conteúdo publicado — ver `perf-analyzer`
- Não acessa plataforma nem API sem MCP conectado
- Não contorna bloqueio de coleta: fonte bloqueada é fonte não acessada

## Skills relacionadas

- `brand-voice` — como **nós** falamos (esta skill é como **eles** falam)
- `copy-page`, `copy-ads`, `copy-email` — consomem o resultado daqui
- `content-strategy` — transforma padrões de dor em pauta
