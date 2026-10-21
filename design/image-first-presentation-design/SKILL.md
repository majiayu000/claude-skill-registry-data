---
name: image-first-presentation-design
description: "Cria apresentacoes, pitches, aulas e decks comerciais pelo fluxo image-first: fecha a narrativa, valida um sistema visual em slides representativos, gera uma composicao individual para cada slide e so depois monta o deck editavel. Use quando direcao de arte, ritmo e diferenciacao importam; nao use para pequenos ajustes em um deck ja aprovado nem quando a tarefa e apenas converter ou revisar texto."
metadata:
  short-description: "Key visual antes do deck editavel"
---

# Image First Presentation Design

Use esta skill quando comecar diretamente no PowerPoint, Canva ou Google Slides tenderia a produzir um deck de template. As imagens de aprovacao sao a fonte visual de verdade; o arquivo de apresentacao e a traducao editavel dessa direcao.

## Ordem obrigatoria

```text
fontes, objetivo e audiencia
-> arco narrativo
-> mapa de slides
-> sistema visual e familias de layout
-> slides de calibracao
-> aprovacao da direcao
-> uma composicao por slide
-> aprovacao do conjunto
-> deck editavel
-> exportacao e QA
```

Nao construir o deck completo antes da aprovacao visual. Um outline textual nao e wireframe e uma colecao de referencias nao e direcao de arte.

## Fontes e precedencia

Antes de criar, recupere o que ja existe.

1. Objetivo do deck e decisao que ele precisa provocar.
2. Audiencia, contexto de apresentacao e tempo disponivel.
3. Copy, dados, provas e fontes canonicas.
4. Identidade visual, fontes e logotipos oficiais.
5. Referencias de estrutura e atmosfera.
6. Imagens, pessoas, produtos, cases e ativos reais.

Se houver conflito, o objetivo decide o que permanece, a fonte canonica decide o conteudo, a identidade decide a marca e as referencias decidem a linguagem. Nao invente dados, citacoes, resultados, clientes ou prova visual.

## Fase 1: arco narrativo e mapa de slides

Defina primeiro:

- o que a audiencia sabe no inicio;
- o que precisa entender, acreditar ou decidir no final;
- tensao central;
- viradas do raciocinio;
- provas necessarias;
- proxima acao.

Para cada slide, registre apenas:

- numero interno e titulo de trabalho;
- funcao narrativa;
- mensagem unica;
- copy ou dados canonicos;
- evidencia ou midia;
- transicao a partir do slide anterior;
- informacao pendente.

Um slide nao precisa conter todo o argumento. Divida quando duas ideias competirem pela mesma hierarquia.

## Fase 2: sistema visual do deck

Antes da primeira composicao, defina:

- frase-norte e conceito visual;
- proporcao e ambiente de exibicao;
- paleta e distribuicao;
- tipografia e escala para projecao ou leitura individual;
- tratamento de fotografia, ilustracao, mockup e grafico;
- grid, margens e alinhamentos;
- familias de layout, nao templates rigidos;
- tres ou quatro componentes de assinatura;
- ritmo entre impacto, explicacao, prova e respiro;
- movimento ou transicoes permitidos;
- elementos proibidos.

Leia [references/slide-comps.md](references/slide-comps.md) antes de gerar ou compor os slides.

## Fase 3: calibracao

Use quatro slides representativos quando existirem no deck:

1. capa;
2. abertura de capitulo ou virada narrativa;
3. slide denso de conteudo, dados ou mecanismo;
4. fechamento, oferta ou proxima acao.

Para decks curtos, reduza a calibracao sem perder o slide mais denso. Para uma familia visual ja aprovada, uma capa e um slide de conteudo podem bastar.

Apresente os comps juntos e explique decisoes concretas: escala, familias de layout, uso da midia, sistema de graficos, ritmo e continuidade.

Pare para aprovacao. Se a calibracao falhar, corrija o sistema antes de compor o restante.

## Fase 4: uma composicao por slide

Depois da calibracao aprovada:

- gere ou componha uma imagem independente para cada slide;
- preserve a mesma proporcao e as areas seguras;
- mantenha uma mensagem dominante por slide;
- varie familias de layout conforme a narrativa, sem trocar de marca;
- use dados e provas reais;
- componha texto, logotipo, graficos e numeros de forma deterministica;
- nao aceite texto inventado pela IA como copy final;
- nao comprima o deck inteiro em um storyboard vertical;
- use a contact sheet apenas para revisar ritmo;
- nao renderize notas de producao, nome de arquivo ou numero interno no slide, salvo quando a numeracao fizer parte do design aprovado.

Use nomes internos estaveis:

```text
deck-s01-cover-v01.png
deck-s02-tension-v01.png
deck-s07-mechanism-v01.png
deck-s14-close-v01.png
```

Versoes aprovadas nunca sao sobrescritas.

## Fase 5: imagem aprovada para deck editavel

Depois da aprovacao do conjunto, leia [references/from-comp-to-deck.md](references/from-comp-to-deck.md).

Reconstrua os slides na ferramenta solicitada. Se houver uma skill ou ferramenta especifica para apresentacoes no ambiente, use-a na fase de producao.

Regras:

- copy, titulos, dados, graficos, tabelas e CTA precisam ser elementos reais;
- nao use cada comp inteiro como screenshot de fundo para simular editabilidade;
- preserve as familias de layout, assimetrias e vazios aprovados;
- mantenha imagens complexas como ativos rasterizados quando fizer sentido;
- preserve fontes oficiais ou documente substituicoes inevitaveis;
- graficos devem nascer dos dados, nao de pixels inventados;
- notas do apresentador e fontes entram quando fizerem parte do escopo.

## QA

Revise o deck como narrativa e como arquivo:

- ordem e progressao do argumento;
- uma mensagem dominante por slide;
- leitura a distancia no ambiente-alvo;
- copy correta, sem overflow ou cortes;
- fontes, cores, margens e masters consistentes;
- imagens sem distorcao e com resolucao suficiente;
- graficos fieis aos dados e rotulos legiveis;
- contrastes e elementos essenciais acessiveis;
- animacoes e transicoes funcionais e parcimoniosas;
- arquivo editavel abre corretamente;
- PDF ou exportacao final preserva fontes e proporcao.

Nao chamar de final apenas porque o arquivo abriu ou exportou.

## Entregaveis minimos

```text
art-direction/
  narrative-map.md
  visual-system.md
  prompts/
  slide-comps/
    deck-s01-cover-v01.png
    deck-s02-...png
  contact-sheet.png          # opcional
deck/
  presentation-editable.*
  presentation.pdf           # quando solicitado
qa/
  review.md
```

Adapte a estrutura ao projeto. Preserve fontes, ativos de origem, prompts e versoes aprovadas.

## Criterios de parada

- Se objetivo, audiencia, copy ou dados essenciais estiverem ausentes, pare antes da geracao e peca apenas o que falta.
- Se a audiencia ou o ambiente mudar a proporcao e isso nao puder ser inferido, confirme antes dos comps.
- Se a calibracao for reprovada, nao construa silenciosamente o restante.
- Se o gerador estiver indisponivel e o conceito depender de imagem nova, informe o bloqueio; nao substitua a etapa por um template generico.
- Se o deck editavel divergir dos comps, volte a eles e corrija a traducao.
