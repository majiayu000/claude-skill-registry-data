---
name: criar-skill
description: "Cria uma skill nova neste repositório e a publica: pasta em skills/, SKILL.md com frontmatter, entrada no skills.json (catálogo que o site lê), bump de versão e release no GitHub que dispara o publish no npm. Invocar quando pedirem para criar/adicionar uma skill nova, transformar um fluxo dele em skill, ou editar/renomear/remover uma skill existente deste catálogo."
---

# Criar uma skill nova

Este repositório é público (`luizsiqueira-eng/skills`) e alimenta três lugares ao mesmo tempo:

| Onde | O que consome |
|---|---|
| `npx @luizsiqueira/skills add <skill>` | a pasta `skills/<nome>/` |
| luizsiqueira.com.br/skills/ e a home | `skills.json` lido direto do `main` via raw.githubusercontent |
| GitHub | o repositório em si (as pessoas leem o SKILL.md) |

Por isso **catálogo e pacote têm que subir juntos** — ver a etapa 5.

## 1. Levantar o fluxo real (não inventar)

Skill boa é fluxo que já existe e funciona. Antes de escrever:

- Pergunte ao autor como ele faz hoje, passo a passo, e onde costuma dar errado.
- Se o fluxo já existir em alguma skill interna do ambiente do autor (skills privadas de projeto ou `~/.claude/skills/`), **leia primeiro** e use como matéria-prima — e neutralize tudo dela.
- Se ele mandar uma palestra, um PDF ou um print, extraia o fluxo dali.
- Não pergunte o que der para descobrir lendo o repositório.

## 2. Neutralizar (regra que não se negocia)

Nada de empresa, cliente ou instância dele pode ir para o público:

| Sai | Entra |
|---|---|
| Prefixo real do card do tracker (`XYZ-1234`), nome do projeto | `ABC-123` e "o identificador do card no seu tracker" |
| Ids reais de campo customizado, de transição, de board | "o campo de PRs da sua instância", "a transição para o status equivalente" |
| Webhook do Discord, nome de canal, role id | "o canal do time (Slack, Discord, Teams…)" |
| Nome da empresa, do time, de colegas, de repos internos | omitir |
| "o fluxo que uso com meu time" | "fluxo baseado em práticas de mercado (Git Flow, …)" |

Antes de publicar, rode a checagem:

```bash
# nome do autor, empresa, produtos, sistemas, cidades, colegas, ids de tracker — ajuste a lista ao seu caso
grep -rniE "<nome-da-empresa>|<sigla>|<prefixo-do-tracker>-[0-9]|<dominio-da-empresa>|customfield_[0-9]|<nomes de sistemas internos>|<nomes de colegas>|meus times" skills/ README.md skills.json bin/
```

Só pode voltar vazio. A lista é sua e cresce: toda vez que um termo interno escapar, entra aqui.
Menções genéricas a ferramentas de mercado (Jira, Trello, Slack, Discord) como *exemplo* são aceitáveis.

## 3. Escrever a skill

Pasta: `skills/<nome>/SKILL.md` — nome em **inglês, kebab-case**, curto, que descreva o
que a skill faz (`git-flow-delivery`, não `fluxo-1` nem `luiz-skill`). É o nome que a
pessoa digita no `npx`.

Frontmatter — as duas linhas mais importantes da skill:

```markdown
---
name: <igual ao nome da pasta>
description: "O QUE a skill faz, denso e específico (o vocabulário que o agente vai casar), + QUANDO invocar. Uma frase só."
---
```

A `description` é o que faz o agente carregar (ou não) a skill: cite os termos que a
pessoa usaria (branch, commit, PR, release) e termine com "Invocar quando/sempre que…".
Sem ela boa, a skill nunca é acionada.

Corpo — o que funciona na prática:

- Título `#` com o nome legível, e um parágrafo dizendo a tese do fluxo.
- Seções numeradas na ordem de execução (`## 1. Branch`, `## 2. Commit`, …).
- Tabelas para decisões (situação → ação) e **comandos prontos para copiar**.
- Marque as regras rígidas em negrito ("**1 branch = 1 commit — sempre**") e explique o
  porquê em uma linha; agente sem o porquê improvisa.
- Diga também **o que não fazer** e onde parar (ex.: "no máximo 1 retry, depois reporte").
- Onde exige julgamento humano, mande **perguntar** em vez de decidir.
- Termine com `## Checklist rápido` (caixas) e `## Adaptando ao seu time` (tabela dos
  poucos pontos que variam entre times: prefixo do card, nomes de branch, status, canal).
- Integrações opcionais (Jira, Linear…) em seção própria marcada como opcional, via MCP,
  sem IDs concretos e sem credenciais em prompt.

Tamanho: o suficiente para um agente executar sem adivinhar; se passar de ~250 linhas,
provavelmente são duas skills.

## 4. Registrar no catálogo (`skills.json`)

Uma entrada por skill — é isso que vira o card no site:

```json
{
  "name": "git-flow-delivery",
  "title": "Git Flow Delivery",
  "description": "Branch, commit, PR, release e hotfix seguindo o Git Flow.",
  "tags": ["git-flow", "code-review", "release"],
  "category": "Engenharia",
  "added": "2026-08-25",
  "featured": false
}
```

- `name` **igual** ao nome da pasta (o CI falha se divergir).
- `description`: **uma frase, só o que a skill faz** — sem explicar como funciona, sem
  listar etapas ("entrevista o time…", "detecta a stack…"). Exemplo bom: "Cria, move e
  consulta cards no Jira ou Trello seguindo o fluxo do seu time." Não repita a description do
  frontmatter (ela é longa e cheia de termos técnicos, boa para o agente e ruim para o card).
- `title`: curto, sem subtítulo explicativo depois do travessão ("Web Security Review", não
  "Web Security Review — Laravel, Node e apps com IA").
- `tags`: 3–5, minúsculas, kebab-case; viram os filtros da página.
- `added`: data de hoje em `YYYY-MM-DD` (ordena a home, mais recente primeiro).
- `featured`: no máximo uma skill por vez.

Existe uma cópia do catálogo no site (`~/Projetos/nlake/luiz-siqueira/skills/skills.json`)
usada como fallback **e como fonte do conteúdo estático/SEO** — atualize as duas para ficarem
iguais e, no repositório do site, rode `node skills/build.mjs` (regenera cards estáticos,
JSON-LD, FAQ e `llms.txt`) antes de commitar.

## 5. Publicar

Nova skill = **minor** no `package.json` (`1.0.0 → 1.1.0`); só correção de texto = patch.
A versão do pacote é alinhada pela tag no workflow, mas mantenha o arquivo coerente.

```bash
# validar antes: CLI e catálogo
node bin/cli.mjs list
cd "$(mktemp -d)" && node ~/Projetos/skills/bin/cli.mjs add --all && ls .claude/skills

# commit no padrão do repo (ver a skill git-flow-delivery)
git add -A
git commit -m "feat - Add <nome> skill"
git push

# release → o workflow publish.yml publica no npm via OIDC (sem token, sem 2FA)
gh release create v1.1.0 --generate-notes
gh run watch "$(gh run list --workflow publish.yml --limit 1 --json databaseId -q '.[0].databaseId')"
npm view @luizsiqueira/skills version   # confirmar
```

**Ordem importa:** o site lê o `skills.json` do `main`, então logo que você faz o push o
card aparece com o comando de instalação — e ele só funciona depois da release publicar no
npm. Faça push e release na mesma sessão; se algo travar, avise que o card está no ar
antes do pacote.

Nunca rode `npm publish` na mão: a conta exige 2FA interativo e o pipeline existe para isso.

## 6. Fechar o ciclo

- Teste como um usuário externo, de pasta limpa:
  `npx @luizsiqueira/skills@latest add <nome>`
- Confira o card em luizsiqueira.com.br/skills/ (a home mostra as skills em carrossel).
- Só então diga que está pronto — com o link do npm e o do SKILL.md no GitHub.

## Editar, renomear ou remover

- **Editar texto:** altere o `SKILL.md`, ajuste a `description` do catálogo se mudou o
  sentido, patch de versão, push, release.
- **Renomear:** `git mv` na pasta, `name` no frontmatter, `name` nas duas cópias do
  `skills.json`, e grep no repositório e no site pelo nome antigo — sobrou nome velho em
  README, CLI ou card, o link quebra. Renomear é **minor** (o comando antigo deixa de existir).
- **Remover:** apague a pasta e a entrada do catálogo; no npm, `npm deprecate` na versão
  antiga em vez de despublicar.

## Checklist rápido

- [ ] Fluxo levantado com o autor (ou extraído de material real), não inventado
- [ ] Grep de neutralização limpo
- [ ] Pasta `skills/<nome-en-kebab>/SKILL.md` com `name` igual à pasta
- [ ] `description` do frontmatter diz o que faz **e** quando invocar
- [ ] Corpo com passos numerados, comandos, checklist e "Adaptando ao seu time"
- [ ] Entrada no `skills.json` (repo **e** cópia do site), com `added` de hoje; `node skills/build.mjs` rodado no site
- [ ] Versão do `package.json` ajustada (nova skill = minor)
- [ ] `node bin/cli.mjs list` e `add --all` passando
- [ ] Push + `gh release create` na mesma sessão
- [ ] `npx ... add <nome>` testado de pasta limpa
- [ ] Autor revisou o SKILL.md antes da release (é o processo dele que fica público)
