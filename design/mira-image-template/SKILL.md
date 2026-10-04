---
name: mira-image-template
description: >-
  Cria um NOVO template de deck do Mira a partir de imagem(ns) de referência (prints de slides e/ou logomarca): reconhece o design system e a disposição dos elementos e salva o esqueleto index.html (design system no bloco @MIRA:THEME) mais o tema em mira-templates/, para aparecer no /mira-new. Use SEMPRE que o usuário disser "/mira-image-template", "criar template a partir de imagem", "template a partir desse print", "transforma essa tela em template", "monta um template com essa identidade", "usa essa logomarca como template", "extrai o design system dessa imagem", "novo template de deck a partir de imagem", ou anexar imagens pedindo para virarem um template/identidade de slides.
---

# Skill: Template a partir de Imagem (Mira)

## Objetivo

Transformar **imagem(ns) de referência** (prints de slides e/ou logomarca) em um **template de deck reutilizável** do Mira: reconhecer o **design system** e a **disposição dos elementos**, e produzir um template nomeado que o `/mira-new` passa a oferecer.

Pertence ao grupo **Agentes visuais e dados** (ao lado de `/mira-visuals`, `/mira-chart`, `/mira-img-animator`, `/mira-image-prompt`).

## REGRA ZERO: fidelidade à referência

O template **obedece** à imagem, não a reinventa. Cores, fundo, contraste, tipografia, raio dos cantos, sombras e (havendo print) a **disposição dos elementos** saem da imagem. Logo manda na paleta; print manda no layout.

## Regra de ouro (escopo de escrita)

Tudo o que esta skill cria vive **dentro de `mira-templates/`**: o tema em `mira-templates/themes/<nome>.css` e o esqueleto em `mira-templates/decks/<nome>/index.html`. Esta skill **cria o template, não cria decks** (isso é o `/mira-new`).

## Fluxo de Execução

### Passo 1: Receber e ler a(s) imagem(ns)

O usuário pode mandar:

- **Print(s) de tela / slides:** a **disposição dos elementos** importa: leia onde está o título, o subtítulo, as pílulas, o palco de conteúdo, a grade, as margens, a proporção 16:9.
- **Logomarca / identidade de marca:** foco na **paleta e personalidade** (cores, peso tipográfico, clima claro ou escuro).
- **Os dois juntos:** a logomarca dá a cor primária; o print dá o layout e o fundo.

Numa **sequência** de imagens, trate-as como o mesmo sistema: extraia o consistente (paleta recorrente, estilo de card, tipografia) e use o print mais representativo como base do layout.

Olhe a imagem de verdade (o harness é multimodal). Não peça para o usuário descrever o que já está na imagem.

### Passo 2: Reconhecer o design system

Extraia, da(s) imagem(ns), os valores abaixo. Quando um valor não der para inferir, derive-o pelas fórmulas da tabela do Passo 4 (a partir da primária e do fundo), nunca chute fora do sistema.

- **Cor primária / da marca** (`#RRGGBB`): a cor de acento dominante (logo, botões, títulos em destaque).
- **Fundo** (`#RRGGBB`): cor de fundo do palco. Pela luminância do fundo, decida se o tema é **escuro** (fundo escuro, texto claro) ou **claro**.
- **Texto**: cor do texto principal (branco no escuro, quase-preto no claro).
- **Estilo de card**: translucidez (glassmorphism), espessura e cor da borda, raio dos cantos.
- **Acento secundário**: tom mais claro/vivo da primária, usado em realces.
- **Tipografia** (opcional): se a fonte for claramente diferente de Inter (serifada, condensada, geométrica), anote a família para o Passo 5.

### Passo 3: Pedir o nome do template

Mostre ao usuário um resumo curto do que você reconheceu e **peça um nome** para o template:

```
Reconheci este design system:
  Primária: #XXXXXX | Fundo: #XXXXXX (tema <claro|escuro>) | Acento: #XXXXXX
  Cards: <vidro translúcido | sólido> | cantos <suaves|retos>
  Tipografia: <Inter | nome da fonte>
  Layout: <descrição curta da disposição vista no print>

Que nome dou a este template?
```

Gere um **slug** em kebab-case, minúsculo, sem acento (ex.: "Identidade Reversa" → `identidade-reversa`). Se já existir `mira-templates/decks/<slug>/` ou `mira-templates/themes/<slug>.css`, avise e peça outro nome (ou confirme sobrescrever).

### Passo 4: Gerar o tema (design system) — `mira-templates/themes/<nome>.css`

O tema é só o bloco `:root` com o **contrato de variáveis** do Mira (a estrutura visual mora no `base.css` e não muda). Preencha **todas** as variáveis:

| Variável | Como derivar |
|---|---|
| `--mira-primary` | cor primária da marca, `#RRGGBB` |
| `--mira-bg` | cor de fundo do palco, `#RRGGBB` |
| `--mira-text` | cor do texto principal (branco no escuro, quase-preto no claro) |
| `--mira-text-soft` | texto a 70%: `rgba(Tr, Tg, Tb, 0.70)` |
| `--mira-text-softer` | texto a 50%: `rgba(Tr, Tg, Tb, 0.50)` |
| `--mira-card-bg` | cor do texto a ~5%: `rgba(Tr, Tg, Tb, 0.05)` |
| `--mira-card-border` | cor do texto a ~10%: `rgba(Tr, Tg, Tb, 0.10)` |
| `--mira-glow-soft` | primária a 15%: `rgba(R, G, B, 0.15)` |
| `--mira-glow-strong` | primária a 25%: `rgba(R, G, B, 0.25)` |
| `--mira-icon-bg` | primária a 15%: `rgba(R, G, B, 0.15)` |
| `--mira-icon-border` | primária a 30%: `rgba(R, G, B, 0.30)` |
| `--mira-pill-bg` | cor do texto a ~4%: `rgba(Tr, Tg, Tb, 0.04)` |
| `--mira-pill-border` | cor do texto a ~8%: `rgba(Tr, Tg, Tb, 0.08)` |
| `--mira-stage-glow` | primária a 6%: `rgba(R, G, B, 0.06)` |
| `--mira-accent-2` | primária clareada ~35% com branco: para cada componente, `novo = round(C + (255 - C) * 0.35)`, em hex |

Onde `R, G, B` são os componentes da primária e `Tr, Tg, Tb` os do texto principal. Esse esquema garante contraste em tema claro e escuro e mantém compatibilidade com o `base.css` e com o override de cor do `/mira-new`.

Escreva o arquivo com um cabeçalho de comentário curto:

```css
/* MIRA THEME: <nome> (gerado por /mira-image-template a partir de imagem)
   Design system reconhecido: <1 linha descrevendo a referência>. */
:root {
    --mira-primary: #RRGGBB;
    /* ...todas as variáveis acima... */
}
```

### Passo 5: Gerar o esqueleto do deck — `mira-templates/decks/<nome>/index.html`

Não escreva o esqueleto do zero. **Clone** um esqueleto existente como base estrutural (use `mira-templates/decks/aula-capitulo/index.html` por padrão, ou o que mais se parecer com o print) e adapte:

1. **Embuta o design system** entre os marcadores `@MIRA:THEME`: o conteúdo de `mira-templates/themes/<nome>.css` **seguido de** `mira-templates/themes/base.css`, entre `/* @MIRA:THEME:START */` e `/* @MIRA:THEME:END */`. Assim o template abre sozinho (`file://`) e continua compatível com a injeção de tema do `/mira-new`.
2. **Obedeça à disposição do print** (quando houver): posição do título/subtítulo, presença e lugar das pílulas, grade do conteúdo, proporções e margens, mantendo o palco 16:9. Não invente seções ausentes na referência nem remova a espinha que o pipeline espera (cabeçalho, palco de conteúdo, rodapé).
3. **Tipografia** (se diferente de Inter): troque o `<link>` da Google Font no `<head>` pela fonte reconhecida e adicione, logo após o `base.css` dentro do bloco `@MIRA:THEME`, um override curto `body { font-family: '<Fonte>', sans-serif; }`. Se a fonte for Inter, não mexa.
4. Atualize o `<title>` para `Mira — Template: <Nome>`.

Mantenha os mesmos CDNs e a estrutura `<head>` do esqueleto base (Tailwind, AOS, Lucide, D3) para o template seguir compatível com o pipeline.

### Passo 6: Confirmar e apontar para o /mira-new

Mostre o resumo do que foi salvo:

```
Template criado: <nome>
  Esqueleto: mira-templates/decks/<nome>/index.html
  Tema (design system): mira-templates/themes/<nome>.css

Já disponível no /mira-new, junto com os templates existentes.
O tema "<nome>" é o padrão natural deste template (a identidade que veio da imagem).
```

Depois ofereça o próximo passo (não execute sem confirmar):

> "Pronto. Quer criar um deck agora com esse template? Posso acionar o /mira-new."

## Regras Inegociáveis

- Escreva **apenas** dentro de `mira-templates/` (`themes/<nome>.css` e `decks/<nome>/index.html`). Cria template, não deck.
- O tema define **todas** as variáveis `--mira-*` do contrato; o `base.css` é embutido sem alteração estrutural.
- Fidelidade à referência (REGRA ZERO): nada de identidade ou layout que contradiga a imagem.
- O `<nome>` do tema e do deck é o **mesmo slug**, para o `/mira-new` casar template e design system.
- Texto visível em português brasileiro com acentuação correta. Proibido travessão (—); use vírgula ou dois-pontos.
- Regra de idioma do projeto: ver `agents/_shared/idioma.md`.
