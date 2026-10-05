---
name: brain
description: >
  Segundo cérebro persistente em Markdown — LLM Wiki no padrão Karpathy
  mantida como bundle Open Knowledge Format v0.2, com fontes imutáveis em
  raw/ e conceitos citados em wiki/. Use quando o usuário disser "segundo
  cérebro", "second brain", "adiciona isso ao meu brain", "salva na minha
  wiki", "ingere esse artigo/PDF/link", "o que minha wiki diz sobre",
  "o que meu brain sabe sobre", "consulta meu conhecimento", "lint da
  wiki", ou pedir para acumular conhecimento de fontes de forma durável.
  NÃO use para notas do Obsidian (pwdev-obsidian), planejamento de
  features (pwdev-feat) nem PRDs (pwdev-prd).
metadata:
  version: 1.0.0
---

# Brain — segundo cérebro em LLM Wiki (OKF v0.2)

## Papel
Roteador e guardião do formato: leva cada intenção do usuário para a
operação certa e impede escrita fora do fluxo.

## Princípio central
**Nada entra na wiki sem discussão e sem citação.** A wiki acumula valor
porque cada afirmação tem fonte e cada mudança passa pelo usuário — gravar
direto "para agilizar" destrói exatamente o que a torna confiável.

## Antes de começar
1. Leia `.claude/pwdev-brain-context.md` — idioma, caminho do brain,
   identidade e preferências.
2. Sem contexto ou sem `<brain>/wiki/index.md` válido → pare e aponte
   `/pwdev-brain:init`.
3. Idioma conforme `${CLAUDE_PLUGIN_ROOT}/references/language.md`; formato
   conforme `${CLAUDE_PLUGIN_ROOT}/references/okf-spec.md`.

## Framework — intenção → operação

| Intenção do usuário | Operação |
|---|---|
| "adiciona/salva/ingere isso" (arquivo, link, artigo, paper) | `/pwdev-brain:ingest <fonte>` |
| "o que minha wiki/brain diz/sabe sobre X", perguntas sobre o acervo | `/pwdev-brain:query <pergunta>` |
| "gera um relatório/comparativo a partir do meu brain" | `/pwdev-brain:query` (artefato em `wiki/output/`) |
| "valida/limpa/organiza a wiki", "tem link quebrado?" | `/pwdev-brain:lint` |
| "cria/configura meu segundo cérebro" | `/pwdev-brain:init` |
| "como está meu brain?" | `/pwdev-brain:status` |

## Mapa de intenção → tool MCP (leitura rápida)

**Path A — MCP `brain` conectado**: para leituras pontuais em conversa
natural, use as tools direto — mais barato em contexto que abrir arquivos:

| Intenção | Tool |
|---|---|
| Panorama/diagnóstico do brain | `brain_info` (caminho, `resolved_via`, contagens) |
| Ponto de entrada da wiki | `brain_index` |
| Listar conceitos (filtro por `type`/`status`/`tag`) | `brain_list` |
| Buscar por termo (ranqueado, com snippets) | `brain_search` |
| Ler conceito ou fonte (`wiki/…`, `raw/…`) | `brain_get` |
| Histórico de mudanças | `brain_log` |

**Path B — MCP ausente ou falhando**: não simule resultado de tool. Siga o
fluxo filesystem dos comandos (index → conceitos → Grep dirigido). Falha
com brain válido é quase sempre **sessão iniciada antes do plugin/env var**
ou **node ausente** — aponte `/pwdev-brain:status` e reinício de sessão.

O MCP é **somente-leitura**: nenhuma tool grava. Toda escrita passa pelos
comandos (ingest com discussão, incorporação aprovada no query, fix
aprovado no lint), sempre via filesystem.

## Processo
1. Identifique a intenção pela tabela e execute a operação correspondente —
   os fluxos completos vivem nos comandos, não aqui.
2. Pedido ambíguo entre ingerir e perguntar ("olha esse artigo") →
   pergunte: guardar na wiki ou só discutir agora?
3. Em qualquer resposta baseada na wiki, cite os conceitos consultados;
   conhecimento do modelo é sinalizado como externo ao brain.

## Formato de saída
O de cada comando (`## Saída` de cada um). Respostas de consulta terminam
com o rodapé `Conceitos consultados / Incorporado / Artefato`.

## Anti-padrões
- Gravar conceito direto em `wiki/` sem passar pelo fluxo de ingest — pula a
  discussão e quebra índice, log e citações.
- Editar ou apagar qualquer coisa em `raw/` — é a fonte de verdade imutável.
- Responder query sem citar, ou misturar conhecimento do modelo com
  conteúdo da wiki sem sinalizar.
- Criar artefato solto em `wiki/` ou na raiz de `wiki/output/` em vez da
  pasta `YYYY-MM-DD-<slug>/`.
- Inventar metadados de frontmatter para "completar" uma página.
- Tentar gravar via MCP — o servidor `brain` é somente-leitura por design;
  ingestão continua no fluxo com discussão.

## Limites
- Não gerencia notas do Obsidian — ver `pwdev-obsidian`.
- Não planeja features nem escreve specs — ver `pwdev-feat` / `pwdev-code`.
- Não cria PRDs — ver `pwdev-prd`.
- Não executa `Attested Computation` — o OKF descreve a computação, não a
  roda.
- As operações vivem nos comandos; esta skill roteia e guarda o princípio.

## Relacionadas
- Comandos: `/pwdev-brain:init` · `:status` · `:ingest` · `:query` · `:lint`
- Referências: `references/okf-spec.md` · `references/lint-rules.md`
