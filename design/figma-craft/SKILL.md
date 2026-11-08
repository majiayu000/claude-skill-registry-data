---
name: figma-craft
description: "Craft de layout ao DESENHAR no Figma via MCP (code-to-design). Ativa sempre que a tarefa for criar, montar, editar, corrigir ou reorganizar qualquer coisa dentro de um arquivo Figma -- tela, frame, card, componente, variante, topbar, sidebar, tabela, FigJam. Triggers: 'criar no Figma', 'montar a tela no Figma', 'desenhar no Figma', 'atualizar o Figma', 'arrumar o auto layout', 'o layout quebrou', 'ficou desalinhado', 'consertar spacing no Figma', 'construir componente no Figma', 'use_figma', 'Plugin API', 'push pro Figma'. Cobre a camada que as skills oficiais do Figma NAO cobrem: decidir a arvore de frames antes de criar, escolher HUG/FILL/FIXED por papel do elemento, validar por propriedades em vez de screenshot, e os erros que ja custaram retrabalho em projeto real. NAO ativa para design-to-code (ler Figma e implementar em React) -- ali vale a skill oficial figma-design-to-code."
---

# Figma Craft -- desenhar certo na primeira passada

O `use_figma` executa JS pela Plugin API. Ele nao "desenha": ele constroi uma arvore de nos.
Layout quebrado quase nunca e erro de API -- e arvore errada, ou sizing decidido no reflexo.

Esta skill cobre a decisao. As regras de API vivem nas skills oficiais do MCP.

## 1. Pre-voo obrigatorio

Antes de QUALQUER escrita no Figma, carregar via `get_figma_skill`:

| Sempre | `skill://figma/figma-use/SKILL.md` |
|---|---|
| Tela, pagina, modal, secao composta | `+ skill://figma/figma-generate-design/SKILL.md` |
| Componente, variante, variable, token | `+ skill://figma/figma-generate-library/SKILL.md` |
| FigJam (board) | `+ skill://figma/figma-use-figjam/SKILL.md` |
| Arquivo novo | `+ skill://figma/figma-create-new-file/SKILL.md` |
| Layout ja quebrado, conserto | `+ skill://figma/figma-use/references/gotchas.md` |

Passar `skillNames: "resource:figma-use,resource:figma-craft"` na chamada `use_figma`.

Nao pular por ser "uma mudanca pequena". As falhas de auto layout aparecem justamente nas pequenas.

Alem das skills, dois groundings antes de gerar:

- **Design system primeiro.** Arquivo com library/tokens: analisar o DS antes de gerar
  ("Analyze this design system file"), ativar a library no arquivo destino e construir com
  instancias reais bindadas a tokens. Componente que ja existe na library nunca e redesenhado.
  Ordem de descoberta: Code Connect → engenharia reversa de telas existentes → `search_design_system`.
- **Fonte real do produto.** Descobrir a font-family verdadeira antes de criar texto -- sem isso o
  gerador cai no Inter. Depois do build, validar por assercao (ler `fontName` dos textos criados).

## 2. Desenhar a arvore ANTES de escrever codigo

Erro numero um: comecar a criar nos e resolver o layout depois. Nao funciona -- no Figma o
sizing depende do pai, entao a arvore errada obriga a consertar tudo no fim.

**Escrever a arvore em texto primeiro**, na mensagem, antes do primeiro `use_figma`:

```
Screen (V, FILL x FIXED 1080, pad 0, gap 0)
├─ Topbar (H, FILL x HUG, pad 12/24, gap 16, align center/space-between)
│  ├─ Logo (FIXED 120x32)
│  └─ Actions (H, HUG x HUG, gap 8)
└─ Body (H, FILL x FILL, pad 24, gap 24)
   ├─ Sidebar (V, FIXED 280 x FILL, pad 16, gap 4)
   └─ Content (V, FILL x FILL, pad 0, gap 16)
```

Notacao: `(direcao, sizingH x sizingV, padding, gap, alinhamento)`.
Se nao souber dizer o sizing de um no, o layout ainda nao esta decidido -- decidir antes de criar.

Regras da arvore:
- Todo container com 2+ filhos relacionados e auto layout (`figma.createAutoLayout()`), nunca frame com x/y.
- Nunca GROUP. Group nao tem sizing, nao tem padding, e quebra quando o conteudo muda.
- Um no so existe se tem papel: estrutura, agrupamento semantico ou espaco. Wrapper sem funcao vira ruido no painel de camadas e no handoff.
- Profundidade util raramente passa de 4-5 niveis. Se passou, provavelmente tem wrapper sobrando.
- Elemento repetido (card de grid, linha de tabela, chip) vira UM componente local + instancias --
  nunca N frames quase iguais. Override de texto em instancia com `setProperties()`, nao `characters`.
- Criar o frame wrapper da tela PRIMEIRO, longe do conteudo existente, e construir dentro dele.
  Nunca criar secoes como filhas top-level da pagina pra reparentar depois -- mover no falha em silencio.
- Uma secao por chamada `use_figma`, nunca a tela inteira num script so. Imports em lote com `Promise.all`.

## 3. Sizing por papel do elemento

Decidir por papel, nao por "o que parece certo agora". Tabela de referencia:

| Elemento | Horizontal | Vertical | Por que |
|---|---|---|---|
| Frame da tela | FIXED (largura do breakpoint) | FIXED ou HUG | Ancora do canvas |
| Topbar / header | FILL | HUG | Acompanha a largura, altura vem do conteudo |
| Sidebar | FIXED | FILL | Largura e decisao de design, altura acompanha a tela |
| Area de conteudo | FILL | FILL | Absorve o espaco que sobra |
| Card em grid | FILL | HUG | Divide a linha, cresce com o texto |
| Linha de lista | FILL | HUG | -- |
| Botao | HUG (ou FILL se full-width) | HUG | Padding define o tamanho |
| Icone | FIXED (16/20/24) | FIXED | Nunca FILL, nunca HUG |
| Texto de uma linha (label) | HUG | HUG | -- |
| Texto que quebra linha | FILL + `textAutoResize = 'HEIGHT'` | HUG | **FILL sozinho colapsa o texto pra largura ~0** |
| Divider | FILL | FIXED 1 | -- |
| Avatar / thumb | FIXED | FIXED | -- |

Ordem de operacoes que evita a maioria dos erros:

1. `figma.createAutoLayout(direcao)` no pai
2. `parent.appendChild(filho)`
3. `resize()` se precisar de dimensao fixa
4. **so entao** `layoutSizingHorizontal / layoutSizingVertical`

`resize()` reseta sizing pra FIXED -- por isso vem antes. E `HUG`/`FILL` sao rejeitados se o no
ainda nao esta dentro de um auto layout, por isso o `appendChild` vem antes.

Nao confundir os dois enums:
- filho: `layoutSizingHorizontal/Vertical` = `FIXED | HUG | FILL`
- frame: `primaryAxisSizingMode/counterAxisSizingMode` = `FIXED | AUTO`

## 4. Spacing e alinhamento

- Padding e gap sempre em multiplos de 4; preferir a escala 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64.
- Nunca simular espaco com frame vazio, texto em branco ou x/y solto. Espaco e `itemSpacing` e padding.
- Distribuir extremos com `primaryAxisAlignItems = 'SPACE_BETWEEN'`, nao com spacer.
- Alinhamento vertical de linha com icone + texto: `counterAxisAlignItems = 'CENTER'` no pai. Nunca ajustar y do icone.
- Espaco negativo (avatares sobrepostos) e `itemSpacing` negativo, nao posicao absoluta.
- Se o container e so estrutura, limpar o fill: `figma.createAutoLayout()` vem com fill branco padrao
  e ele aparece como retangulo branco sobre fundo tonal.

## 5. Gotchas que ja custaram retrabalho

Verificados em projeto real de cliente, nao teoricos:

1. **No movido entre containers carrega o layout antigo.** Depois de `appendChild`, resetar
   `layoutSizingHorizontal/Vertical` E `layoutPositioning = 'AUTO'`. Sintomas: elemento colado no vizinho
   ignorando o gap, altura colapsada pra 1px, conteudo cortado.
2. **`node.screenshot()` renderiza o no ISOLADO** -- mostra o elemento certo enquanto no canvas real
   esta quebrado. Validar por propriedades primeiro, imagem depois (secao 6).
3. **Nunca usar `rotation` pra virar icone dentro de auto layout.** A rotacao gira em torno da origem e
   joga o no pra fora da caixa reservada. Usar `instance.swapComponent(outroComponente)`.
4. **No herdado que resiste a duas tentativas de conserto: remontar.** Recriar o container com
   `createAutoLayout()` e reanexar os filhos custa menos chamadas do que insistir.
5. **`query()` nao aceita nome com espaco** (`FRAME[name=Product Context]` retorna null).
   Usar `findOne(n => n.name === '...')`.
6. **Comentarios do Figma nao sao acessiveis** pela Plugin API (`figma.comments` nao existe).
   Pedir o texto colado.
7. **Cor em 0-1**, nao 0-255. Sem canal `a` dentro de `color` -- opacidade fica no nivel do paint.
8. **O canvas do usuario fica em cache depois de escrita via plugin.** Ele reporta texto cortado,
   elemento fora do lugar ou artefato flutuando, e no arquivo esta tudo certo. Antes de "consertar" o
   que nao esta quebrado: medir as propriedades e renderizar com `get_screenshot` (render do servidor,
   e a prova do estado salvo). Batendo os dois, pedir reload -- nao mexer no layout. Ja custou duas
   idas e voltas em producao (seletor de area de topbar, campos de formulario).
9. **`textAutoResize = 'HEIGHT'` e rejeitado silenciosamente se o no esta com altura fixa.**
   Em auto layout, soltar `layoutSizingVertical = 'HUG'` ANTES. Sintoma: setar HEIGHT e continuar
   lendo `NONE` -- o pior modo, porque o texto nao cresce nem em altura, so corta.
10. **`maxWidth` de texto nao pode ser sobrescrito em instancia.** Erro: `This property cannot be
    overridden in an instance: max-size`. Pra limitar um rotulo num contexto (nome longo no topo),
    ponha `maxWidth` na **raiz da instancia** e o texto em `FILL` + `textAutoResize = 'HEIGHT'`.
    O limite padrao (largura maxima, `maxLines`, `textTruncation`) mora no componente.
11. **Opacidade de paint ligado a variavel pode nao chegar na instancia.** O componente leu
    `opacity: 0.08` no fill e a instancia renderizou o mesmo fill a 100% -- um slot vazio virou
    bloco solido. Transparencia que importa vai em **camada propria com `node.opacity`**, nao na
    opacidade do paint bindado. Conferir lendo `fills` da instancia, nao so do componente.

## 6. Validar antes de dizer que esta pronto

Ordem obrigatoria: **propriedades → screenshot do container pai → screenshot do canvas**.
Screenshot do no isolado nunca e prova.

Rodar o script de auditoria em `references/audit-layout.md` no frame trabalhado. Ele varre a arvore
e sinaliza: GROUP, frame com varios filhos sem auto layout, `layoutPositioning = ABSOLUTE` dentro de
auto layout, dimensao colapsada, texto com FILL sem `textAutoResize = HEIGHT`, spacing fora da grade de 4.

Zero flags e o criterio de pronto. Flag que for decisao consciente, dizer qual e por que.

Complementos por secao, enquanto o conserto e barato:

- Screenshot da secao logo depois de construi-la (nao so no fim da tela): pega texto cortado,
  overlap, variante errada e placeholder esquecido.
- Assercao de fonte: ler `fontName` dos textos criados e comparar com a fonte do produto.

## 7. Checklist final

- [ ] Arvore foi escrita em texto antes do primeiro `use_figma`
- [ ] Todo container com filhos relacionados e auto layout; nenhum GROUP
- [ ] Sizing decidido por papel (tabela da secao 3), nao no reflexo
- [ ] `appendChild` antes de `HUG`/`FILL`; `resize()` antes do sizing
- [ ] Texto que quebra linha: FILL + `textAutoResize = 'HEIGHT'`, e `width > 0`
- [ ] Padding e gap na grade de 4; nenhum spacer falso
- [ ] Containers de estrutura com `fills = []`
- [ ] Cor bindada em variable/token, nao hex solto (quando o arquivo tem tokens)
- [ ] Camadas nomeadas por papel (`Topbar`, `Card / Header`), nao `Frame 427`
- [ ] Script de auditoria rodado, zero flags
- [ ] DS analisado e library ativada antes de gerar (quando o projeto tem DS)
- [ ] Componente existente na library entrou como instancia; elemento repetido virou componente local + instancias
- [ ] Fonte real do produto validada por assercao (nao caiu no Inter)
- [ ] Wrapper criado primeiro; uma secao por chamada; nenhuma secao reparentada de top-level
- [ ] Todos os IDs criados/mutados retornados no `return`

## Fronteiras

- Craft visual estatico (cor, tipografia, hierarquia, polish) → `/ui-designer`
- Tokens, arquitetura de DS, auditoria de consistencia → `/design-system`
- Fluxo, IA, psicologia da tela → `/ux-designer`
- Ler Figma e implementar em React → skill oficial `figma-design-to-code`
