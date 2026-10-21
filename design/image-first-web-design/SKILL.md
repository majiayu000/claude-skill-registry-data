---
name: image-first-web-design
description: "Cria landing pages, sites de marketing e portfólios visualmente ambiciosos pelo fluxo image-first: organiza a narrativa, gera uma imagem horizontal independente para cada seção, valida a direção de arte, transforma as imagens aprovadas em wireframe técnico e só então implementa o código. Use quando qualidade visual e diferenciação importam; não use para correções técnicas simples nem quando já existe um design final aprovado."
metadata:
  short-description: "Imagem por seção, wireframe e só depois código"
---

# Image First Web Design

Use esta skill quando começar pelo HTML tenderia a empurrar o projeto para um layout genérico. A imagem é a fonte visual de verdade; o wireframe traduz a imagem para um sistema executável; o código é a última camada.

## Ordem obrigatória

```text
fontes e copy
→ mapa narrativo das seções
→ sistema visual global
→ imagens de calibração
→ uma imagem para cada seção
→ aprovação visual
→ wireframe técnico desktop + mobile
→ aprovação do wireframe
→ código
→ comparação visual e QA
```

Não iniciar HTML, CSS, React, Framer, Webflow, Elementor ou outro construtor antes da aprovação das imagens e do wireframe. Um mapa narrativo preliminar não é wireframe: ele apenas define quantas seções existem e qual função cada uma cumpre.

## Fontes e precedência

Antes de criar, leia os insumos já disponíveis. Não peça novamente o que estiver no contexto ou no projeto.

1. Copy canônica e fatos comerciais.
2. Identidade visual oficial.
3. Referências de estrutura e composição.
4. Moodboard ou referências emocionais.
5. Banco de imagens, provas, pessoas, produtos e entregáveis.

Se houver conflito, a copy decide o conteúdo, a identidade decide a marca, a referência decide a estrutura e o moodboard decide a atmosfera. Marque fatos não confirmados como provisórios; não bloqueie a exploração visual por causa deles.

## Fase 1: mapa narrativo, sem desenhar layout

Divida a copy em seções. Para cada uma, registre apenas:

- nome e ordem;
- mensagem única;
- pergunta não dita que responde;
- função no funil: chamar, identificar, explicar, provar, oferecer ou fechar;
- copy canônica associada;
- material real disponível;
- informação ainda pendente.

A quantidade final de seções determina a quantidade mínima de imagens. Dez seções exigem dez imagens independentes.

## Fase 2: sistema visual global

Defina antes da primeira geração:

- frase-norte da página;
- conceito narrativo recorrente;
- paleta e proporção de uso;
- famílias tipográficas e contraste de escala;
- tratamento global de luz, cor e textura;
- grid, respiro e linguagem de bordas;
- quatro componentes de assinatura;
- dois comportamentos de movimento implícitos;
- padrões proibidos para este projeto.

Varie composição sem variar de marca. A página inteira precisa parecer um único mundo visual.

## Fase 3: gerar as imagens das seções

Antes de gerar, leia [references/section-comps.md](references/section-comps.md).

Use uma ferramenta de geração de imagem disponível. Prefira o gerador de imagem nativo quando existir. O provedor é intercambiável; o processo não pode depender de uma marca específica.

Regras rígidas:

- gerar uma imagem horizontal separada por seção;
- tratar cada imagem como um recorte do mesmo documento web contínuo, nunca como slide, página de livro ou prancha de apresentação;
- nunca comprimir a página inteira em uma prancha vertical;
- nunca substituir várias seções por uma colagem;
- manter nomes estáveis: `s01-hero-v01.png`, `s02-prova-v01.png`;
- usar `s01`, `s02` e demais números somente na organização interna dos arquivos; não renderizar número de seção, fólio, nome de capítulo, rodapé editorial, margem de slide ou paginação, salvo quando fizerem parte explícita da copy canônica;
- gerar novamente uma seção pouco clara; não recortar uma imagem antiga;
- manter a mesma paleta, tipografia, luz, tratamento, raios e linguagem de CTA;
- variar âncora compositiva e modo de background;
- não repetir `texto à esquerda + imagem à direita` por hábito;
- preservar espaço e hierarquia suficientes para futura implementação responsiva.

O texto renderizado pela IA não é fonte canônica e a IA generativa não aplica com fidelidade uma fonte local específica. Quando a identidade exigir tipografia, logotipo ou elementos gráficos exatos, gere a camada artística sem texto e componha a imagem de aprovação por meios determinísticos com os ativos oficiais. A copy verdadeira deve estar legível já nessa composição final e volta como dado estruturado no wireframe e no código.

### Calibração

Gere primeiro três seções representativas:

1. hero;
2. uma seção de mecanismo, conteúdo ou prova;
3. oferta ou fechamento.

Apresente-as juntas como uma direção visual coerente e pare para validação. Após aprovação, gere todas as seções restantes sem trocar silenciosamente o sistema visual.

### Gate visual

Entregue cada imagem individualmente e, opcionalmente, uma contact sheet apenas para navegação. Não avance ao wireframe até a usuária aprovar o conjunto ou indicar ajustes. Ajuste somente as seções afetadas e versione os arquivos.

## Fase 4: imagem para wireframe

Depois da aprovação visual, leia [references/wireframe-and-code.md](references/wireframe-and-code.md).

Analise cada imagem aprovada como especificação. Extraia:

- hierarquia e percurso do olhar;
- grid e proporções;
- posição e largura do texto;
- backgrounds, texturas, imagens e sobreposições;
- tipografia e escala relativa;
- componentes e estados;
- CTA e prioridade;
- movimento sugerido;
- comportamento desktop, tablet e mobile;
- dependências de conteúdo e mídia.

Reconstrua a seção em wireframe técnico usando a copy canônica, não o texto eventualmente inventado dentro da imagem. O wireframe deve ser executável, não uma descrição de clima.

Pare para aprovação do wireframe antes do código.

## Fase 5: implementação fiel

Somente depois dos dois gates aprovados:

1. extraia tokens e componentes compartilhados;
2. implemente a estrutura real, sem usar screenshots como página pronta;
3. use imagens reais ou ativos gerados nos slots previstos;
4. preserve os momentos distintivos das composições;
5. use bibliotecas de componentes apenas como apoio técnico;
6. não deixe a conveniência do framework substituir a direção aprovada;
7. faça a adaptação responsiva definida no wireframe.

21st.dev ou outra biblioteca pode ajudar com accordion, carousel, sticky CTA e microinterações. Ela não define a identidade nem autoriza trocar a composição aprovada por um template.

## Fase 6: comparação e QA

Renderize pelo menos desktop e mobile. Compare seção por seção com as imagens aprovadas e com o wireframe.

Verifique:

- fidelidade de composição, ritmo e escala;
- copy correta e fatos confirmados;
- consistência de fontes, cores, bordas e tratamento de imagem;
- leitura em tela pequena;
- contraste, foco, teclado e redução de movimento;
- peso de imagens e estabilidade de layout;
- funcionamento de CTA, accordion, carousel e navegação.

Não chamar de final enquanto a comparação visual não tiver sido feita.

## Entregáveis mínimos

```text
art-direction/
  visual-system.md
  prompts/
  section-comps/
    s01-hero-v01.png
    s02-...
  contact-sheet.png        # opcional, nunca substitui os arquivos individuais
wireframe/
  wireframe.md
  media-inventory.md
implementation/
  ...
```

Adapte os diretórios à estrutura real do projeto. Preserve prompts, arquivos aprovados e versões; não sobrescreva uma direção aprovada.

## Critérios de parada

- Se faltarem copy ou identidade essenciais, interrompa antes da geração e peça apenas o que falta.
- Se o gerador de imagem estiver indisponível, informe o bloqueio; não improvise o visual em HTML.
- Se a calibração for reprovada, corrija o sistema antes de gerar o restante.
- Se uma seção estiver ilegível, gere uma nova imagem independente.
- Se o código começar a divergir, volte à imagem e ao wireframe; não normalize a diferença como limitação do HTML.
