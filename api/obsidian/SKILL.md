---
name: obsidian
description: >
  Leitura, escrita e edição estruturada de notas, busca, tags, arquivo ativo
  e comandos da paleta no Obsidian via MCP (plugin Local REST API). Use
  quando o usuário disser "Obsidian", "vault", "nota", "anotação", "criar
  nota", "buscar nota", "tag", "daily note", "frontmatter", "abrir arquivo
  no Obsidian", ou pedir para ler/editar/organizar conteúdo do vault.
metadata:
  version: 1.0.0
---

# Obsidian

Você gerencia o vault do Obsidian do usuário via servidor MCP `obsidian`.

## Pré-requisito e degradação

**Path A — MCP `obsidian` conectado**: use as tools diretamente.

**Path B — tools falhando ou MCP ausente**: não simule conteúdo de nota. O
"servidor" é o **próprio app Obsidian** rodando localmente com o plugin
Local REST API ativado — não é um serviço remoto sempre disponível. Uma
falha quase sempre significa **Obsidian fechado** ou **plugin desativado**,
não config ausente. Diagnostique com
`${CLAUDE_PLUGIN_ROOT}/scripts/check-setup.sh` e aponte
`/pwdev-obsidian:init`. Env var nova só vale após reiniciar a sessão.

## Mapa de intenção → tool

| Intenção | Tool |
|---|---|
| Ler nota inteira | `vault_read` |
| Ler só uma seção/frontmatter | `vault_read` com `targetType`+`target` — economiza contexto vs. ler o arquivo inteiro |
| Descobrir estrutura antes de editar | `vault_get_document_map` (headings, block ids, frontmatter keys, `version`) — **sempre antes de um `vault_patch` targeted** |
| Criar nota nova / sobrescrever inteira | `vault_write` — **sobrescreve sem aviso**; confirmar se o arquivo já existir |
| Acrescentar ao fim | `vault_append` — cria se não existir |
| Editar heading/block/frontmatter específico | `vault_patch` (`replace`\|`prepend`\|`append`\|`delete`) |
| Adicionar/remover tag | `vault_patch` em `targetType: "frontmatter"`, `target: "tags"` (ver `references/mcp-tools.md`) |
| Renomear/mover | `vault_move` |
| Duplicar | `vault_copy` |
| Apagar | `vault_delete` — vai para lixeira por padrão; `permanent: true` é irreversível |
| Listar pasta | `vault_list` |
| Buscar por tag/frontmatter/data/path | `search_query` (JsonLogic) |
| Buscar texto livre por relevância | `search_simple` |
| Tags do vault + contagem | `tag_list` |
| Arquivo aberto no editor | `active_file_get_path` |
| Abrir arquivo na UI | `open_file` |
| Rodar comando da paleta | `command_list` → `command_execute` |

Parâmetros exatos, scopes e pegadinhas: `${CLAUDE_PLUGIN_ROOT}/references/mcp-tools.md`.

## Resource MCP

`obsidian://local-rest-api/openapi.yaml` — spec OpenAPI completa da REST API
subjacente, útil quando o comportamento de uma tool não estiver claro.

## Regras

- **Mutação com impacto sempre com confirmação antes de executar**:
  sobrescrever nota existente (`vault_write`), `vault_delete`
  (especialmente `permanent: true`), `vault_move`/`vault_copy` sobre destino
  existente, e `command_execute` (pode disparar qualquer comando registrado,
  inclusive de outros plugins instalados — sem preview do efeito).
- **Nunca reconstruir manualmente** um heading/block id retornado por
  `vault_get_document_map` — copiar verbatim (pode ter sufixo de
  desambiguação não-imprimível para duplicatas).
- Em `vault_patch`, níveis de heading no `content` são **relativos ao
  target** — não conte `#`s absolutos.
- Leia `.claude/pwdev-obsidian-context.md` (vault, pastas, convenções de
  tag, regra de confirmação) antes de perguntar o que já está registrado.
- Conteúdo criado no vault (título, corpo, frontmatter) segue o idioma do
  vault/usuário — pergunte se houver dúvida, nunca traduza sem pedir.

## Fluxos recomendados

- **Criar nota**: perguntar pasta/título/tags → montar conteúdo → confirmar
  → `vault_write`.
- **Editar seção existente**: `vault_get_document_map` → `vault_patch`
  targeted (com `ifMatch` quando a edição for sensível a concorrência).
- **Panorama do vault**: ver `/pwdev-obsidian:vault`.

## Limites

- Sem acesso a anexos binários (imagens, PDFs) — só arquivos markdown.
- Um único vault por vez: o que estiver aberto no Obsidian no momento da
  chamada.
- Sem sincronização nem gestão de plugins do Obsidian.
- Panorama agregado e persistido → `/pwdev-obsidian:vault`.
