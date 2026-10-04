---
name: mira-post-it
description: >-
  Mural de POST-ITS AO VIVO no Mira, em dois slides: no primeiro a pergunta com
  um QR-code, no segundo cada resposta em TEXTO LIVRE da plateia vira um post-it
  que cola na parede, um a um. Diferente do mira-survey e do mira-quiz, aqui a
  resposta é aberta, não há alternativas nem resposta correta, e nada é
  agregado: cada pessoa aparece com a frase dela. Use SEMPRE que o usuário
  disser /mira-post-it, post-it, mural de respostas, parede de respostas, resposta
  aberta, resposta em texto livre, pergunta aberta para a plateia, as respostas
  vão aparecendo no slide, a plateia escreve e aparece na tela, mural ao vivo, ou
  pedir um slide onde a sala escreve uma frase curta pelo celular e ela surge na
  projeção. Para votação em alternativas use /mira-survey; para pergunta com
  resposta correta use /mira-quiz; para um QR sem leitura de respostas use
  /mira-qrcode.
---

# Skill: Mural de post-its ao vivo (pergunta + QR num slide, respostas no outro)

Cria **dois slides no mesmo deck**:

- **Slide 1**: a pergunta grande, o QR-code de resposta e um contador ao vivo.
- **Slide 2**: o mural, onde cada resposta em texto livre cola como um post-it, um a um.

> **Fonte da verdade:** o template completo em
> [`references/postit-template.html`](references/postit-template.html), derivado do deck
> validado `decks/mira-postit-demo/`. Reaproveita a arquitetura provada pelo `mira-survey` e
> pelo `mira-quiz`: Google Forms como interface, Google Sheets como fonte viva, leitura por
> `gviz` + JSONP para funcionar em `file://`.

## Modelo mental

O Mira não hospeda nada. Ele lê respostas já coletadas:

1. A plateia abre o **link de votação** pelo QR e escreve uma frase curta.
2. Cada envio vira uma linha na **planilha** ligada ao Forms.
3. O deck lê a planilha a cada poucos segundos pelo `gviz`.
4. Enquanto o slide 1 está na tela, as respostas se acumulam numa **fila**.
5. Quando o slide 2 fica visível, a fila **drena**: um post-it por vez, com cadência.
6. O mural mostra **15 por página**. A seta vira a página, e a página inédita cola do mesmo
   jeito, um a um.

## As três decisões que fazem a coisa funcionar

Sem elas o slide fica tecnicamente certo e cenicamente morto.

**1. Revelação por visibilidade, não por chegada.** Se o mural renderizasse a cada leitura,
o apresentador viraria o slide e daria de cara com uma parede pronta e parada, porque as
respostas chegaram enquanto o slide 1 estava aberto. A leitura roda sempre; a **colagem** só
começa quando o slide 2 entra na tela (`IntersectionObserver`, threshold `0.6`). Quem
responder com o mural já na tela entra na hora.

**2. Um poller só, dois destinos.** Os dois slides vivem no mesmo documento. Existe um único
`window.miraPostitPoll`, que atualiza o contador do slide 1 e alimenta a fila do slide 2.
Dois pollers dariam duas chamadas JSONP correndo uma contra a outra.

**3. Chave estável.** O `gviz` devolve a tabela inteira a cada leitura. Cada post-it é
identificado pelo **índice da linha** e só vira DOM uma vez. Inclinação, cor e ritmo de
respiração também saem do índice, nunca de `Math.random()` no render: senão a parede inteira
treme a cada 3 segundos.

## Dados obrigatórios

Confirme antes de gerar. Se faltar qualquer item, pergunte e pare.

| Dado | Exemplo | Uso |
|---|---|---|
| Link de votação | `forms.gle/...` | vira o QR-code inline do slide 1 |
| Link da planilha | `docs.google.com/spreadsheets/d/<ID>/...` | fonte viva das respostas |
| Pergunta | `Que atividade repetitiva você faz no trabalho?` | título dos dois slides |

Texto sugerido se faltar algo:

> Para montar o mural de post-its eu preciso do link de votação do Google Forms, do link da
> planilha de respostas e da pergunta. A pergunta precisa ser de **resposta curta ou
> parágrafo** (texto livre, não múltipla escolha), e a planilha precisa estar pública como
> "qualquer pessoa com o link -> Leitor". Pode colar isso aqui?

## Formulário esperado

Uma única pergunta de **resposta curta** ou **parágrafo**. Peça no enunciado um limite de
tamanho ("em três ou quatro palavras"), senão o mural vira parede de texto.

Na planilha, o slide lê sempre a **última coluna**. Não faça casamento por cabeçalho: o
Forms guarda o enunciado inteiro no rótulo, muitas vezes com espaços sobrando no fim.

Se o formulário tiver campo de nome ou várias perguntas, avise que o mural usará a última
coluna e peça confirmação.

## Verificação da planilha

Extraia o `SHEET_ID` do link com `/spreadsheets/d/<ID>/` e teste o mesmo endpoint que o slide
vai usar:

```bash
curl -sL "https://docs.google.com/spreadsheets/d/<SHEET_ID>/gviz/tq?tqx=out:json" | head -c 800
```

Se vier `google.visualization.Query.setResponse({...})` com `"status":"ok"`, está legível. Se
vier HTML de login, peça o ajuste de compartilhamento para **qualquer pessoa com o link ->
Leitor**.

**Nunca use "Publicar na web -> CSV".** Esse endpoint fica cacheado por minutos e mataria o
"ao vivo". Só `gviz` + JSONP.

## QR-code local

O QR do link de votação é gerado localmente e embutido como SVG inline, igual ao
`/mira-qrcode`, ao `/mira-survey` e ao `/mira-quiz`. Sem API externa e sem CDN.

1. Instale o pacote uma vez numa pasta temp reaproveitável, se ainda não existir:

```bash
npm install qrcode --no-save --prefix "<pasta-temp>"
```

2. Gere o SVG:

```bash
node -e "require('qrcode').toString('LINK_VOTACAO',{type:'svg',errorCorrectionLevel:'M',margin:0,color:{dark:'#0a0a0a',light:'#ffffff'}},(e,s)=>{if(e)throw e;process.stdout.write(s)})"
```

Não use `npx qrcode`, que trava no Windows.

3. Cole o `<svg>` inteiro dentro de `.qr-card`, mantendo `viewBox` e `shape-rendering`, com o
comentário:

```html
<!-- QR gerado localmente (pacote npm qrcode, ECC M) para LINK_VOTACAO -->
```

O link de votação não aparece por extenso no slide.

**O QR é grande.** Ele não é um selo de canto: é a chamada do slide, e alguém no fundo da sala
precisa escanear. No template ele ocupa `60vh` (`clamp(260px, 60vh, 700px)`), com a pergunta
dividindo o quadro ao lado. Se encolher para caber outra coisa, a outra coisa é que está
sobrando.

## Direção visual

O post-it é papel de verdade, não card de UI: cantos quase retos (`border-radius: 3px`),
sombra projetada, um vinco de cola no topo e inclinação de -4° a +4°.

**A entrada é no lugar.** O post-it não vem voando de fora: ele surge já na vaga dele, no
tamanho final, com um pop curto de escala, sem deslocamento e sem giro, e o texto entra logo
atrás, como se estivesse sendo escrito ali. Isso não é preciosismo, é consequência da grade
de vagas fixas (ver abaixo): com a posição e o tamanho decididos antes, não sobra nada para a
animação mover, e o que resta é a única coisa que interessa, o papel aparecendo.

- Fundo escuro Mira, laranja `#FF904D` na identidade e no halo.

### A regra das cores

Cor de post-it é onde esse tipo de slide costuma ficar berrante. Duas travas evitam isso:

**Varia o matiz, não o brilho.** Os sete papéis (`#F2D98B`, `#F3BC96`, `#B6DCC2`, `#A9CBE3`,
`#E9B7BE`, `#CBBEE0`, `#E4DAC6`) são tons foscos de papel na **mesma faixa de luminância**.
Nenhum grita mais alto que os outros, e a parede lê como uma coisa só, em vez de virar
confete. Amarelo neon e verde-limão saturado estão fora justamente por quebrarem essa faixa.

**Contraste conferido, não chutado.** A tinta é `#2A2118`, um preto quente. Contra os sete
papéis o contraste fica entre **9,0:1 e 11,4:1**, bem acima do 7:1 do WCAG AAA, o que segura a
leitura até em projetor lavado. Ao trocar a paleta, meça de novo: papel escuro demais com
tinta escura é o jeito mais fácil de perder a sala.

**Distribuição com passo 3.** A cor sai do índice, então a mesma resposta mantém a mesma cor
entre leituras. Mas percorrer a paleta de um em um cria listra diagonal na grade: com passo 3
sobre 7 papéis, o vizinho de lado e o de cima nunca caem no mesmo tom.

- Texto escuro sobre o papel, peso 700, centralizado.
- **Regra Zero**: mesmo com ninguém respondendo o mural respira. Cada post-it balança no
  próprio ritmo, com atraso derivado do índice.
- Sem partículas e sem nada que atrapalhe a leitura em projeção.

## A grade de vagas fixas

**Este é o ponto que mais fácil se erra.** O reflexo é dimensionar a grade pelo número de
post-its que existem agora. O resultado é péssimo: uma resposta vira um cartaz gigante no meio
da tela, duas viram dois cartazes, e a parede inteira encolhe a cada chegada até assentar lá
pelo décimo. É movimento que não conta nada e cansa quem está olhando, e ainda faz o post-it
aparecer num tamanho e terminar noutro.

A grade é sempre a da **página cheia**: `POR_PAGINA` vagas, do tamanho que elas terão no fim,
mesmo com a parede vazia. Cada post-it nasce na vaga dele, já no tamanho final, e a única
coisa que muda na tela é ele aparecendo. Vaga não ocupada é só parede.

Por isso o `densidade()` roda com `n = POR_PAGINA`, não com `mural.children.length`, e só é
chamado no carregamento e no `resize`, nunca a cada post-it. E declara as **linhas** também
(`grid-template-rows`), não só as colunas: sem isso a terceira linha só nasceria quando o
décimo primeiro post-it chegasse, e a parede toda pularia naquele instante, que é o mesmo
defeito por outro caminho.

O cálculo em si é uma medida, não um chute: para cada número possível de colunas ele acha o
post-it maior que ainda cabe no quadro e fica com o maior de todos; empate ganha quem usa
menos linhas. Sobrando altura, o post-it cresce para dentro dela em vez de deixar faixa preta,
com o `ASPECTO_ALTO` impedindo que vire uma tira em pé, porque post-it de verdade é quase
quadrado. `MAX_LARGURA` impede que uma vaga vire cartaz; `MIN_LARGURA` é o piso. Resposta
comprida encolhe **só ela**, por `--k`, sem mexer na vaga.

## Paginação

O mural mostra **15 post-its por página**. Nada é descartado: a página é só uma janela sobre a
lista completa de respostas, e o rodapé mostra `página X de Y` (escondido enquanto houver uma
só).

**A seta é a mesma o tempo todo.** No mural, seta para a direita avança a página e seta para a
esquerda volta. O gesto só sai do mural quando não há para onde paginar: na primeira página a
seta para trás volta ao slide da pergunta, e na última a seta para frente segue adiante. Nada
de tecla nova para decorar.

Isso é feito capturando o `keydown` na **fase de captura** do `document`, antes da navegação
padrão do Mira, que escuta a mesma tecla na subida. O evento só é engolido (`stopPropagation`)
quando existe página de destino.

**Página inédita cola, página revista aparece.** Um post-it que a sala nunca viu entra
colando, com a cadência. Voltar uma página traz tudo instantâneo: reanimar o que já foi visto
faria o apresentador esperar oito segundos só para dar um passo atrás. O controle é por
resposta, não por página, então uma página parcialmente revelada mostra na hora o que já
colou e cola só o que chegou depois.

**Resposta que cai na próxima página espera a seta.** Com a página cheia, um envio novo não
empurra nada: ele aparece quando o apresentador vira. O que muda na hora é o `página X de Y`
do rodapé e o contador do slide 1, que é como o apresentador percebe que tem mais gente.

## Velocidade

O ritmo da colagem tem **um botão só**, marcado no arquivo como `@MIRA:VELOCIDADE N/10`, na
mesma escala de 1 a 10 do `/mira-size-animator`. Mexer nele muda as duas coisas que a plateia
percebe como velocidade, e sempre juntas:

- `CADENCIA`, o intervalo entre um post-it e o próximo;
- `ENTRADA`, a duração da animação de cada um, aplicada ao CSS pela variável `--entrada`.

As duas são inversamente proporcionais à velocidade (`1560 / V` e `1.86 / V`). Mexer só numa
delas dá a sensação errada: cadência sem entrada vira tranco, entrada sem cadência vira espera
parada.

Referência: **3/10** é o ritmo contemplativo (520ms de cadência, 0,62s de entrada, página
cheia em cerca de 8 segundos). **6/10**, o padrão do template, é o ritmo de palco (260ms,
0,31s, página cheia em cerca de 4 segundos). Se o autor pedir "mais rápido" ou "mais devagar",
mexa nessa variável e em nada mais.

## Estados e comandos

- **Vazio**: post-it fantasma tracejado e uma linha explicando que o primeiro ainda vai colar.
  Zero resposta não pode parecer deck quebrado.
- **Ao vivo**: bolinha verde pulsando nos dois slides, com o total.
- **Sem conexão**: bolinha cinza e "sem conexão com a planilha".
- **Setas**, PageUp/PageDown e espaço: no slide 1 viram o slide, no mural viram a página. É a
  virada para o slide 2 que dispara a primeira colagem.
- Tecla `R`: limpa o mural e reapresenta tudo colando do zero. Serve para ensaiar antes da
  plateia chegar e para repetir o efeito sem recarregar. Como as setas, respeita os modos de
  edição (`E`) e pintura (`P`): com um deles ligado, o teclado é deles.

## Passos

1. **Confirmar os dados obrigatórios.** Se faltar algo, peça e pare.
2. **Conferir que a pergunta é de texto livre.** Se for múltipla escolha, o agente certo é o
   `/mira-survey` ou o `/mira-quiz`, não este.
3. **Extrair o `SHEET_ID`** e verificar o `gviz`.
4. **Gerar o QR localmente** e embutir o SVG inline.
5. **Copiar o template** para `decks/<nome-do-deck>/index.html` e preencher `SHEET_ID`,
   `PERGUNTA` e o SVG do QR.
6. **Instalar os módulos de autoria** em `decks/<nome-do-deck>/mira/` (`mira-edit.js`,
   `mira-edit-free.js`, `mira-draw.js`) e criar a pasta `references/`.
7. **Conferir a navegação do Mira.** O template já traz o bloco padrão de navegação slide a
   slide (setas, PageUp/PageDown e espaço, com as guardas dos modos de edição e pintura),
   copiado do `mira-default`, mais a paginação do mural em cima dele. Sem o bloco padrão o
   apresentador não passa da pergunta para o mural com a seta, e é justamente a virada que
   dispara a colagem dos post-its.
8. **Reportar** o caminho absoluto do arquivo, os atalhos (setas para virar, `R` para
   reapresentar) e lembrar que o deck abre por duplo clique em `file://`, mas precisa de
   internet para ler a planilha.

## Ajustes que o autor pode pedir

Estão todos no bloco `CONFIG`, no topo do `<script>`:

| Variável | Padrão | O que muda |
|---|---|---|
| `INTERVALO` | `3000` | de quanto em quanto tempo lê a planilha |
| `VELOCIDADE` | `6` | ritmo da colagem, de 1 a 10 (ver abaixo) |
| `MAX_CHARS` | `90` | onde a resposta comprida é cortada |
| `POR_PAGINA` | `15` | post-its por página do mural |
| `PAPEIS` | 7 tons foscos | paleta dos papéis, na mesma faixa de luminância |
| `PASSO_COR` | `3` | espalha as cores na grade, sem listra diagonal |
| `ASPECTO` | `1.35` | proporção largura/altura do post-it |
| `MAX_LARGURA` | `420` | teto de largura, para uma resposta só não virar cartaz |

## Checklist

- [ ] Dois slides: pergunta com QR, depois o mural.
- [ ] Pergunta do Forms é de texto livre, não múltipla escolha.
- [ ] QR gerado localmente como SVG inline, sem API externa.
- [ ] Link de votação não aparece por extenso no slide.
- [ ] Leitura por `gviz` + JSONP. Nenhum "Publicar na web -> CSV".
- [ ] Um único `window.miraPostitPoll` servindo os dois slides.
- [ ] Colagem disparada por visibilidade do slide 2, não por chegada da resposta.
- [ ] Post-it identificado pelo índice da linha, criado uma vez só.
- [ ] Inclinação, cor e ritmo derivados do índice, nunca de `Math.random()` no render.
- [ ] Grade de vagas fixas: `densidade()` roda com `POR_PAGINA`, declara colunas E linhas, e não é chamado a cada post-it.
- [ ] Post-it entra no lugar, no tamanho final, sem deslocamento e sem a parede reflowar.
- [ ] Encolhimento por card em resposta comprida, sem mexer na vaga.
- [ ] Mural paginado em 15, com `página X de Y` no rodapé e nenhuma resposta descartada.
- [ ] Seta pagina dentro do mural e só troca de slide quando não há página de destino.
- [ ] Página inédita cola um a um; voltar uma página é instantâneo.
- [ ] Velocidade num botão só (`@MIRA:VELOCIDADE`), regendo cadência e entrada juntas.
- [ ] Estado vazio explícito e sinal de conexão nos dois slides.
- [ ] Regra Zero preservada: o mural respira mesmo parado.
- [ ] QR grande, ocupando cerca de `60vh`, com a pergunta dividindo o quadro.
- [ ] Bloco de navegação do Mira presente: seta vira da pergunta para o mural.
- [ ] Deck com `mira-edit.js`, `mira-edit-free.js` e `mira-draw.js` em `mira/` e `references/` criada.
- [ ] Papéis na mesma faixa de luminância, contraste com a tinta conferido e acima de 7:1.
- [ ] Cores espalhadas com passo, sem listra diagonal na grade.
- [ ] Texto revisado, acentuação correta e sem travessão.
