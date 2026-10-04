---
name: mira-image
description: >-
  Coloca uma imagem que o usuário JÁ TEM (arquivo local ou URL) num slide do
  Mira, novo ou existente, em card limpo (padrão mira-3d/mira-qrcode): só título
  (sem ícone, máx. 6 palavras) e a imagem grande e bem enquadrada. Copia a imagem
  para assets/ do deck por caminho relativo, então abre por file:// sem servidor;
  imagem estática, com o loop da Regra Zero na moldura. NÃO confunda: para GERAR imagem
  nova use mira-visuals ou mira-image-prompt; para ANIMAR a imagem use
  mira-img-animator; este só POSICIONA uma imagem pronta. Use SEMPRE que o
  usuário disser /mira-image, coloca essa imagem no slide, põe essa foto no
  slide, insere essa imagem, adiciona essa figura ao deck, slide com essa imagem,
  mostra esse print no slide, ou fornecer um arquivo de imagem ou URL pedindo
  para exibir.
---

# Skill: Imagem pronta no slide

Coloca uma imagem que o usuário já tem (arquivo local ou URL) num slide, em card limpo, grande e bem enquadrada. É a skill mais simples da família de elementos: só **posiciona uma imagem pronta**, não gera nem anima.

## Desambiguação

- **Gerar imagem nova** (de descrição, dados, diagrama): `mira-visuals` ou `mira-image-prompt`.
- **Animar imagem existente** (mover partes): `mira-img-animator`.
- **Só colocar uma imagem que já existe num slide:** esta skill, `mira-image`.

## Regra Zero (com ressalva da imagem estática)

Todo slide do Mira tem loop interno. Aqui a **imagem fica estática** (nada de distorcer, esticar ou animar o conteúdo); o loop vai na **moldura**: um brilho que respira (`box-shadow` indo e voltando) ou leve flutuar do card. Descreva o loop em uma frase ("a imagem fica firme e a moldura respira um brilho suave").

> **Ken Burns (opcional, não padrão).** Só se o usuário pedir movimento na própria imagem (zoom/pan lento e contínuo), aplique um Ken Burns sutil. "Movimentar a imagem de verdade" é do `mira-img-animator`.

## Sem servidor (diferente do mira-3d)

Uma `<img src="assets/...">` comum **carrega por `file://`**: o bloqueio de CORS que quebra o `.glb` do `mira-3d` é do `fetch`/módulos, não da tag `<img>`. Então este slide abre direto, sem servidor nem Node.

Para o deck ficar autossuficiente e portátil:

1. **Copie a imagem para `assets/` do deck** (crie a pasta se faltar) e referencie por caminho relativo (`assets/nome.jpg`). Nunca use caminho absoluto da máquina (quebra ao mover o deck).
2. Se for **URL**, baixe a imagem para `assets/` e referencie o arquivo local (não deixe `src` na web, senão o slide morre sem internet). Confira a licença antes, como no `mira-3d`.

## Composição do card (padrão mira-3d / mira-qrcode: limpo, elemento maximizado)

- **Só título + imagem.** Título no topo (sem ícone, máximo 6 palavras). **Sem legenda** embaixo, por padrão.
- **Imagem grande e central**, ocupando boa parte da altura útil (no canônico, `height: min(72vh, 760px)`).
- **Enquadramento sem cortar conteúdo:** `object-fit: contain` por padrão (diagramas, prints, logos, qualquer imagem onde o conteúdo importa). `object-fit: cover` só para **foto decorativa/de fundo** que o usuário aceita recortar. **Nunca** distorça (não use `fill`/esticar).
- **Cantos arredondados** e moldura/sombra suave para casar com o glass-card do deck.
- **`alt` sempre preenchido** com descrição curta em português (acessibilidade).

**Crédito/licença:** quando exigir atribuição, vai em **comentário HTML** no slide (e no `assets/README.md` do deck, se for o caso), nunca como texto visível, igual ao `mira-3d`. Legenda visível só se o usuário pedir.

## CSS + HTML canônico (gerar conforme isto)

```html
<style>
  .img-card {
    position: relative;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 24px;
    padding: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    animation: img-glow 4s ease-in-out infinite;   /* loop interno na moldura */
  }
  .img-card img {
    display: block;
    width: 100%;
    height: min(72vh, 760px);
    object-fit: contain;       /* nunca corta; troque para cover só em foto decorativa */
    border-radius: 16px;
  }
  /* Loop interno (Regra Zero): brilho respirando na moldura, imagem firme */
  @keyframes img-glow {
    0%, 100% { box-shadow: 0 10px 30px rgba(0,0,0,0.35), 0 0 0 rgba(255,144,77,0); }
    50%      { box-shadow: 0 10px 40px rgba(0,0,0,0.40), 0 0 40px rgba(255,144,77,0.18); }
  }
</style>

<section class="min-h-screen flex flex-col items-center justify-center px-6 pt-3 pb-6">
  <div class="w-full max-w-6xl flex flex-col items-center" data-aos="fade-up" data-aos-delay="100">
    <!-- Título do slide: SEM ícone, no máximo 6 palavras -->
    <div class="text-center mb-4">
      <h2 class="text-4xl md:text-5xl font-bold mb-2">
        Título <span class="primary-color italic">com ênfase</span>
      </h2>
    </div>
    <div class="img-card w-full">
      <!-- Imagem fornecida pelo usuário, copiada para assets/. Crédito (se exigido) aqui: Fonte / Licença -->
      <img src="assets/minha-imagem.jpg" alt="Descrição curta da imagem">
    </div>
  </div>
</section>
```

Para **foto decorativa de ponta a ponta**: troque `object-fit: contain` por `cover` e, se quiser proporção fixa, use `height` ou `aspect-ratio` no `.img-card img`. Para **PNG/logo com fundo transparente**: mantenha `contain` e considere remover a moldura/sombra para a transparência respirar.

## Passos

1. **Receber a imagem e o destino.** O arquivo (caminho ou URL) e o slide (novo, ou slide N do deck X). Se faltar a imagem, peça. Se for URL, confirme a licença antes de baixar.
2. **Levar a imagem para o deck.** Copie (ou baixe) para `decks/<deck>/assets/`, com nome limpo. Referencie por caminho relativo.
3. **Montar o card limpo:** título no topo (sem ícone, máx. 6 palavras, sem legenda embaixo), imagem grande e central, `object-fit` adequado (contain por padrão), moldura com glow. Inserir como `<section>` no padrão do deck; preservar o sistema de navegação.
4. **Conferir:** imagem não cortada (salvo cover pedido) nem distorcida, `alt` preenchido, caminho relativo válido, crédito em comentário se exigido.
5. **Reportar.** Caminho do arquivo do slide, nome do asset copiado, `object-fit` usado e o loop em uma frase. Lembre que abre por `file://` sem servidor. Se o usuário quiser a imagem em movimento, aponte o `/mira-img-animator`.

## Checklist

- [ ] Imagem copiada/baixada para `assets/` do deck e referenciada por caminho **relativo** (nada de caminho absoluto da máquina nem `src` apontando para a web).
- [ ] Slide abre por `file://` sem servidor (é `<img>`, não `fetch`/`.glb`).
- [ ] Card limpo: só título + imagem; sem legenda por extenso embaixo (salvo pedido).
- [ ] Título sem ícone, no máximo 6 palavras.
- [ ] Imagem grande e central; `object-fit: contain` (ou `cover` só em foto decorativa); nunca distorcida.
- [ ] Cantos arredondados e moldura suave; `alt` preenchido com descrição curta.
- [ ] Imagem estática; loop interno só na moldura (glow respirando), nada animando/distorcendo a imagem.
- [ ] Crédito/licença (quando exigido) em comentário HTML, nunca visível.
- [ ] Nenhum travessão (—); acentuação UTF-8 correta (segue `agents/_shared/idioma.md`).
```
