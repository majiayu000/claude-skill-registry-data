---
name: get-brolls
description: 'Coleta, pré-visualiza e entrega B-rolls com revisão humana e origem registrada. Use quando alguém pedir b-roll, vídeos de apoio, imagens de apoio, cutaways, inserts, footage, "um corte do X falando Y", um print da tela de um site ou de uma notícia, ou material para ilustrar um vídeo, Reel ou aula — buscando em YouTube, Instagram, TikTok, Wikimedia Commons, NASA ou bancos (Pexels, Pixabay), gerando prévias para revisão humana e entregando os trechos com origem e condições de uso. Also in English: collect B-roll, cutaways, inserts, supporting footage, stock video, screen grabs. Não serve para editar, montar ou renderizar o vídeo final. Not for editing or rendering the finished video.'
license: MIT
metadata:
  version: "2.5.2"
  type: "skill"
  status: "current"
  created: "2026-09-15"
  updated: "2026-10-23"
  tags: "b-roll, youtube, instagram, tiktok, storyboard"
---

<!-- Fonte canônica do fluxo clone-como-skill. Espelhado em skills/get-brolls/SKILL.md (plugin do Claude Code). Ao editar um, sincronize o outro. -->

# GET B-ROLLS — ENGENHEIRO DE VÍDEO

Você planeja fontes literais, mostra o trecho à pessoa, recebe a decisão dela e só então entrega o corte. Fale português direto, sem jargão de CLI, e nunca transforme a conversa num formulário.

## Três guardas

**Literal primeiro.** Procure o fato, a pessoa, o produto, a notícia ou a tela que a narração cita. Banco genérico não cobre beat sem fonte literal.

**Stock só sob pedido.** Pexels e Pixabay entram quando o usuário pedir stock com todas as letras. Nunca como preenchimento.

**Parada obrigatória na revisão.** Aprovação vem sempre de uma pessoa: pelo Storyboard (`import-review`) ou por fala explícita no chat, registrada com `approve --candidate <ID> --by NOME --channel chat --statement "frase"`. Silêncio não é aprovação. Não se autoaprove.

## Passo 1 — Entreviste antes de buscar

Sem `BRIEF.md` na pasta do projeto, conduza a entrevista de `/get-brolls-brief`. O roteiro está em [`references/interview.md`](references/interview.md): sete perguntas, uma por mensagem, teto de sete — pare assim que 1, 3 e 7 estiverem respondidas. Dois "tanto faz" viram defaults, com o que foi assumido visível na resposta. Nunca invente narração, alvo, link ou responsável.

## Passo 2 — Confirme o brief

Rode o CLI pelo **caminho absoluto da instalação da skill**: os exemplos escrevem `scripts/gb.py` por brevidade. `--project` é sempre a pasta do usuário, também absoluta, e vai em **todo** comando.

Escreva o `BRIEF.md` com `python3 "scripts/gb.py" init-brief --project <projeto>`, preencha o bloco JSON e valide com `brief --validate`. Se a pessoa nomeou a plataforma (Reel, Shorts, horizontal), alinhe o `video_format` do RULES.md antes de validar: `init-rules --format reels --force --project <projeto>`.

**Checkpoint C1.** Em até cinco linhas: o que o vídeo precisa provar, quantos beats, as fontes na ordem, o que ficou por default e quem assina. Feche com "fecho assim?" e espere.

## Passo 3 — Busque fonte literal

`python3 "scripts/gb.py" brief --beat <ID> --project <projeto>` devolve o comando pronto do beat. Todo material entra com `--shot <beat.id>`. Consulte `library --search "termo"` antes: ela lembra o que rendeu, sem aprovar nem permitir. Fontes, presets, lotes e a biblioteca estão em [`references/providers.md`](references/providers.md). **Reel do Instagram: leia [`references/instagram.md`](references/instagram.md) antes de tocar no navegador** — é a rota que quebra primeiro.

**Checkpoint C2.** Liste 5 a 8 candidatos, uma linha cada: título, canal, duração e a janela do `inspect`. Feche com "sigo com estes?".

## Passo 4 — Analise e pré-visualize

`python3 "scripts/gb.py" inspect --candidate <ID> --query "fala ou alvo" --project <projeto>` lê duração, capítulos e legendas e devolve janelas pontuadas; escreva a `--query` no idioma da fonte. Escolha `--start/--end` a partir delas, nunca de palpite.

Depois, `python3 "scripts/gb.py" preview --candidate <ID> --start <INICIO> --end <FIM> --project <projeto>` gera poster, contact sheet e GIF: até 10 s por prévia (`GB_PREVIEW_MAX_SECONDS`) e **um `preview` por chamada**, senão a chamada estoura o tempo. A resposta traz `files.contact_sheet` (no `status` e no manifesto, `preview.contact_sheet_path`, relativo a `brolls/`) e `preview.frame_times_s`. **Abra e olhe antes de seguir.** Cite em `--reason` as células e os tempos que viu; se não servirem, ajuste o intervalo. Nunca descreva quadro que não conferiu.

Sem pista, `preview --scan` varre o vídeo inteiro: exploratório, depois de `inspect`, e ignora o intervalo escolhido.

## Passo 5 — Revisão humana

Duas rotas, e você para nas duas.

**Board**, quando quem revisa é outra pessoa: `python3 "scripts/gb.py" review --project <projeto>`, depois `serve --background --project <projeto>`. Entregue a URL, peça a decisão e importe com `import-review --by NOME --project <projeto>` — sem `--file`, ele pega o arquivo mais recente da página.

Antes do C3, rejeite o que descartou: `reject --candidate ID1 --candidate ID2 … --reason "por quê" --project <projeto>`. Assim o status reflete a conversa.

**Chat**, quando a pessoa está aqui. **Checkpoint C3:** descreva o que cada contact sheet mostra e pergunte "aprova todos, ou quais?". Aprove exatamente os IDs que você mostrou: `approve --candidate ID1 --candidate ID2 … --by NOME --channel chat --statement "frase exata" --project <projeto>`; use `--all` só quando todos os candidatos com prévia foram mostrados. No canal chat, `--statement` é obrigatório.

Mudança de intervalo ou de contexto invalida aprovação. A copy pronta das duas rotas está em [`references/templates-de-resposta.md`](references/templates-de-resposta.md).

## Passo 6 — Direitos, corte e entrega

Registre as condições com `permit` (`--evidence`, `--preset` ou `--declared-by/--declaration-text`), depois `fetch`, `verify` e `deliver`. As três rotas estão em [`references/rights.md`](references/rights.md). Não invente licença. `deliver` monta `entrega/`, uma pasta por beat, com `ORIGEM.md`.

## Relate o status

`python3 "scripts/gb.py" status --project <projeto>` diz onde a coleta está sem alterar nada. Ao responder, repasse `summary.do.for_human` **sem parafrasear**: é a frase que já traz o próximo passo na língua da pessoa.

## Quando não há fonte

Diga o que tentou e o motivo real. Pergunte se a pessoa tem material próprio ou um link. Não invente indisponibilidade permanente nem troque de arquitetura sozinho.

## Ambiente

`python3 "scripts/gb.py" doctor` diz o que está pronto e o que falta. No Windows, use `python` no lugar de `python3`. Faltando algo, peça `/get-brolls-setup`. Versão diferente da deste arquivo: leia o [CHANGELOG](CHANGELOG.md).

## Índice de references

- [`references/interview.md`](references/interview.md) — as sete perguntas do brief.
- [`references/providers.md`](references/providers.md) — fontes, ordem, biblioteca e lotes.
- [`references/instagram.md`](references/instagram.md) — o procedimento dos dois streams.
- [`references/rights.md`](references/rights.md) — condições de uso e `permit`.
- [`references/templates-de-resposta.md`](references/templates-de-resposta.md) — copy pronta.
- [`references/glossario.md`](references/glossario.md) — o que cada termo quer dizer.
- [`docs/GUIDE.md`](docs/GUIDE.md) — detalhe técnico por provedor.
