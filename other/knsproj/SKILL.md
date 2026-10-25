---
name: knsproj
description: Gera projetos editáveis do Kinesis Editor (.knsproj) a partir de uma descrição em linguagem natural — composição, camadas de texto/formas/mídia, objetos 3D, materiais, câmera, luzes, keyframes e curvas — valida contra o schema oficial e empacota o arquivo pronto para importar no app Android. Use quando o usuário pedir uma animação, vídeo, motion graphics, título animado ou cena 3D "para o Kinesis", ou invocar /knsproj.
argument-hint: "<descrição da animação>"
---

# /knsproj — gerar projetos do Kinesis

Você vai transformar o pedido do usuário em um projeto `.knsproj` **válido e editável**: tudo deve continuar
ajustável no app (camadas separadas, keyframes reais, nada "achatado"). O trabalho é feito localmente, sem serviços
do Kinesis: só arquivos JSON, a CLI `tools/knsproj` (Python 3, biblioteca padrão) e o schema em `schema/`. Para
**ver** o resultado antes de entregar, o comando `preview` desenha quadros aproximados (precisa de Pillow e numpy).

Referências (leia quando precisar de detalhes):
- Especificação: `docs/knsproj.md`
- Schema oficial: `schema/knsproj-v11.schema.json` (formato versão 11; arquivos v1 a v10 ainda abrem e são migrados). Escreva sempre `"formatVersion": 11`.
  Novidades por versão: v3 expressões e animadores de texto; v4 camada `null` e câmera por `rotation`; v5 easing `cyclic`; v7 `cyclic.offset` = assimetria (skew) de cada ciclo, `phase` = deslocamento; v8 `markers` (marcadores da timeline) e `eq` (equalizador) em clipes de áudio/vídeo; v9 `editorView` (câmera livre da prévia, não renderizada: exemplo `basicos/vista-do-editor`) o efeito `timeSlice` (exemplo `basicos/fatias-de-tempo`) e `video.roto` (receita do Roto Brush: vídeo de origem e pinceladas; exemplo `basicos/recorte-roto-brush`); v10 os efeitos retrô e de glitch `eightBit`, `pixDither`, `pixelEncoder`, `kernel`, `signalAnalog`, `glitchify` e `dissolveShake` (exemplos `basicos/efeito-*`); v11 o efeito `copyBackground` (Copiar fundo = camada de ajuste: copia o que está embaixo e os efeitos seguintes atuam só onde a camada é opaca; exemplo `basicos/efeito-copiar-fundo`);
  v6 texto 3D (`primitive: "text"`), `material.shading`, sombras (`light.castShadows`), profundidade de campo (`camera.dof`),
  ambiente HDRI (`composition.environment`) e vídeo com transparência (`video.alphaPacked`).
- Expressões (APIs, unidades, matriz de compatibilidade): `docs/expressoes.md`
- Lista completa de efeitos (parâmetros, padrões, faixas): tabela da seção 7 de `docs/knsproj.md` ou `tools/knsproj/effects.json`
- Exemplos: `.claude/skills/knsproj/examples/` (veja "Exemplos" abaixo)

## Exemplos (comece por aqui)

**Antes de escrever o `project.json`, leia o `README.md` do exemplo mais próximo do pedido** (e abra o `project.json`
dele) e adapte em vez de começar do zero. **Sempre rode `validate` antes de empacotar** — nunca entregue um projeto
que não validou.

Tudo em `.claude/skills/knsproj/examples/`; cada pasta tem `project.json` e `README.md` (o que demonstra, quando usar, armadilhas):

| Pasta | Use quando o pedido envolve |
|---|---|
| `basicos/texto-animators` | texto aparecendo por caractere/palavra, typewriter, onda |
| `basicos/texto-bounce` | texto que quica letra por letra (animador de texto com expressão, o "Bounce Text" do After Effects) |
| `basicos/expressoes` | `wiggle`, `loopOut`, matemática na opacidade |
| `basicos/shape-trim-path` | linha que se desenha, círculo de loading |
| `basicos/keyframes-easing` | overshoot (`cubicBezier`), bounce, loops `pingpong` |
| `basicos/curva-ciclica` | oscilação entre dois keyframes (pêndulo, pulso, balanço) com `{"cyclic": {"cycles": 3.5}}` |
| `basicos/parent-anchor` | pivô fora do centro, camada filha herdando rotação |
| `basicos/mascara-feather` | revelar uma forma/imagem com máscara de borda suave |
| `basicos/track-matte` | texto revelado por forma (`alpha`), degradê de opacidade (`luma`) |
| `basicos/transicoes` | `transitionIn`/`transitionOut` em camadas e grupos |
| `basicos/efeitos` | glow, sombra, glitch (`chromaticAberration`) |
| `basicos/video-audio` | trecho de vídeo (`sourceStart`, `speed`), fade de volume, trilha |
| `basicos/grupo` | tempo relativo, efeito aplicado a um conjunto |
| `basicos/3d-camera-orbita` | cena 3D com 3 luzes e câmera orbitando (pai `empty`; hoje prefira um nulo 3D, veja `nulo-3d-rig`) |
| `basicos/nulo-2d` | camada nula (`null`) movendo/girando várias camadas 2D como pai |
| `basicos/nulo-3d-rig` | câmera presa a um nulo 3D (`null.threeD`) que gira: órbita/rig |
| `basicos/camera-rotacao` | câmera com `aim: "rotation"`: dolly (posição) e pan (rotação) independentes |
| `basicos/model3d` | modelo GLB com câmera girando |
| `basicos/texto-3d-sombras` | título 3D extrudado (profundidade, bevel) sobre um chão, com sombra projetada e profundidade de campo |
| `basicos/ambiente-hdri` | panorama equiretangular iluminando e refletindo nos objetos; sombreamento `flat`, `toon` e `wireframe` |
| `receitas/lower-third` | tarja de nome/cargo em 16:9 |
| `receitas/intro-logo-glow` | abertura de logo com brilho |
| `receitas/titulo-cinetico` | título animado com matte e motion blur |
| `receitas/slideshow-transicoes-musica` | sequência de slides com transições e música |
| `receitas/video-vertical-legenda-por-palavra` | 1080x1920 com legendas palavra a palavra |
| `efeitos/<categoria>` | um exemplo por categoria de efeito: `cor-e-luz`, `desfoque-e-nitidez`, `distorcao` (inclui **Glass**), `movimentar-e-transformar`, `estilizar`, `glitch`, `desenho-e-borda`, `procedimental`, `fosco-mascara-e-chave`, `tempo-e-transicao`, `texto`, `utilitario` |
| `erros/*` | quando o `validate` acusar `keyframe.order`, `layer.parentKind`, `layer.matteMissing`, `layer.missingAsset` ou `expression.syntax`: o README mostra a causa e o conserto |

Para usar um exemplo como ponto de partida: copie a pasta para `generated/<slug>`, ajuste textos, cores, tempos e
mídias, e valide. Os exemplos de `basicos/`, `receitas/` e `efeitos/` validam com 0 erros e 0 avisos; os de `erros/` falham de propósito.

**Instalação por .zip:** `knsproj-skill.zip` (nesta pasta) é uma cópia autônoma da skill — traz `SKILL.md`, os exemplos,
a CLI (`tools/knsproj`), o schema e a especificação. Crie a pasta `~/.claude/skills/knsproj/` e descompacte o zip dentro dela (o `SKILL.md` e as pastas ficam na raiz do zip; resultado: `~/.claude/skills/knsproj/SKILL.md`)
e rode a CLI de dentro dessa pasta (`python3 tools/knsproj validate …`). Regere-o com `python3 tools/pack_skill.py`.

## Fluxo

1. **Interpretar o pedido.** Extraia: proporção (vertical 9:16 → 1080×1920; horizontal 16:9 → 1920×1080;
   quadrado → 1080×1080; 4:5 → 1080×1350), duração, fps (30 por padrão), cores, textos exatos, elementos 2D/3D,
   estilo e ritmo. Se algo essencial for ambíguo, escolha um padrão sensato e diga qual escolheu no fim — não
   interrompa o usuário por detalhes.
2. **Criar a pasta do projeto:**
   ```bash
   python3 tools/knsproj new generated/<slug> --title "<Título>" --width 1080 --height 1920 --fps 30 --duration 10 --background "#0A2463"
   ```
3. **Adicionar mídias fornecidas pelo usuário** (imagens, vídeos, áudio, GLB, fontes) — nunca invente arquivos:
   ```bash
   python3 tools/knsproj add-asset generated/<slug> caminho/do/arquivo.png   # imprime o id do asset
   ```
   Sem arquivos do usuário, construa o visual com texto, formas, gradientes, efeitos e primitivas 3D.
4. **Escrever as camadas** editando `generated/<slug>/project.json` (seção "Referência rápida"), partindo do exemplo mais próximo (leia o README dele antes).
5. **Validar** e corrigir até não haver erros:
   ```bash
   python3 tools/knsproj validate generated/<slug>
   ```
   As mensagens trazem o caminho JSON do problema (ex.: `$.layers[3].text.fontSzie: unknown property (did you mean 'fontSize'?)`).
   Trate também os avisos: normalmente indicam intenção errada.
6. **Conferir o resultado** com `python3 tools/knsproj info generated/<slug>` (árvore de camadas e tempos) e
   **olhando os quadros** (seção "Preview visual"):
   ```bash
   python3 tools/knsproj preview generated/<slug>              # contact sheet de 9 quadros → generated/<slug>_preview.png
   ```
   Abra a imagem gerada (ferramenta de leitura de arquivos/imagens) e confira: enquadramento, nada cortado fora da
   tela, texto legível, ordem de entrada, cores. Corrija o `project.json`, valide e rode `preview` de novo até ficar
   bom (2–3 rodadas costumam bastar). Para um momento específico: `--time 1.2,1.5`; para movimento: `--gif`.
7. **Empacotar:**
   ```bash
   python3 tools/knsproj pack generated/<slug> -o generated/<slug>.knsproj
   ```
8. **Entregar:** informe o caminho do `.knsproj` (e do preview/GIF, se ajudar o usuário a ver antes de importar), um resumo (formato, duração, camadas principais, decisões
   tomadas) e como importar: *app Kinesis → tela inicial → ícone "Importar .knsproj" → escolher o arquivo*.

## Preview visual (aproximado)

`preview` reproduz em Python a avaliação de cena do app (tempos, keyframes, easings, loops, pais, nulos, grupos,
transições, animadores de texto, máscaras, track mattes, blend modes, câmera e luzes) e desenha os quadros em
software. **Posição, tempo e enquadramento batem com o app; os pixels são aproximados.**

Funciona igual no desktop do usuário e em sandbox — só Python:

```bash
python3 -c "import PIL, numpy" 2>/dev/null || pip install pillow numpy   # em Python gerenciado: --break-system-packages
python3 tools/knsproj preview <pasta | project.json | arquivo.knsproj> [opções]
```

| Opção | Efeito |
|---|---|
| (nenhuma) | contact sheet com 9 quadros espaçados, cada um com `t=` e número do quadro |
| `--frames N` | N quadros no contact sheet |
| `-t 0,0.5,2.25` | só esses tempos (segundos, absolutos na composição); um tempo só → um PNG |
| `--separate` | um PNG por tempo em vez do contact sheet |
| `--gif anim.gif [--gif-fps 12]` | GIF da composição inteira (bom para mostrar ao usuário; caro para você ler) |
| `--scale 0.5` | resolução (padrão: ~480 px no lado maior por quadro, ~720 px para um quadro só) |
| `-o arquivo.png` | saída (padrão: `<projeto>_preview.png` ao lado da pasta — fora dela, para não ir no `pack`) |
| `--json` | arquivos gerados, tempos e lista de aproximações em JSON |

Como usar bem:
- Comece pelo contact sheet: uma imagem só mostra a animação inteira gastando pouco contexto. Use `-t` para
  investigar um trecho (ex.: o quadro em que um texto termina de entrar).
- Leia a lista **"approximations"** que o comando imprime: diz o que não foi simulado *neste* projeto. Não "corrija"
  o projeto por causa de algo da lista — no app aquilo aparece certo.
- Vídeos usam `ffmpeg` se estiver instalado (sem ele, um placeholder do tamanho do vídeo). Fontes: a do asset, ou a
  mais próxima do sistema.

O que é aproximado ou ignorado: expressões JavaScript (usa o valor/keyframes de base), PBR simplificado, sem
sombras, sem DOF, sem motion blur, sem ambiente HDRI (reflexo de céu genérico), texto 3D plano (sem extrusão), efeitos
fora deste subconjunto — `blur`, `glow`, `deepGlow`, `dropShadow`, `fill`, `tint`, `saturation`,
`brightnessContrast`, `exposure`, `hueShift`, `invert`, `posterize`, `pixelate`, `vignette`, `posterizeTime` e os de
movimento (`autoShake`, `spin`, `oscillate`, `float`, `pulse`) — e o recorte do Roto Brush.

## Referência rápida do formato

- Origem no **centro** da composição; +x direita, +y **para baixo**, +z se afasta da câmera. Unidades: pixels.
- Tempos em segundos. **Keyframes usam tempo relativo ao `start` da camada.**
- Camadas em ordem de pintura: a primeira fica **embaixo**. Ids únicos em todo o projeto.
- Cor: `"#RRGGBB"` ou `"#RRGGBBAA"`. Escala: `1` = 100%. Rotação em graus (horário). Opacidade 0..1.
- Propriedade animável: valor simples **ou** `{"keyframes": [{"time": 0, "value": …, "easing": "easeOutCubic"}, …], "loop": "cycle"}`.
  O `easing` vale para o segmento que **começa** naquele keyframe.
- **Expressões (formato 3):** qualquer propriedade animável aceita `"expression": "<JavaScript>"`, junto de `"value"` (sem
  keyframes) ou de `"keyframes"`. O resultado é a **última instrução avaliada**. `"expressionEnabled": false` desliga sem apagar.
  Veja a seção "Expressões" abaixo e `docs/expressoes.md`.

Esqueleto de camada (campos comuns): `id`, `type`, `name`, `start`, `duration`, `parent`, `blendMode`,
`motionBlur`, `transform` (2D) ou `transform3d` (3D), `effects`, `masks`, `matte`, `transitionIn`, `transitionOut`,
e o objeto de conteúdo com o **mesmo nome do tipo**.

```jsonc
// Texto com entrada por caractere
{ "id": "titulo", "type": "text", "name": "Título", "start": 0.3, "duration": 9.7,
  "transform": { "position": [0, -620] },
  "text": { "content": "OLÁ", "font": { "family": "sans-serif", "weight": 900 }, "fontSize": 150, "color": "#FFFFFF",
            "letterSpacing": 0.08,
            "animators": [{ "type": "slideUp", "unit": "character", "stagger": 0.05, "unitDuration": 0.5, "easing": "easeOutCubic", "amount": 90 }] },
  "transitionOut": { "type": "fade", "duration": 0.5 } }

// Forma com gradiente e brilho
{ "id": "fundo", "type": "shape", "start": 0, "duration": 10,
  "shape": { "kind": "rectangle", "size": [1080, 1920],
             "fill": { "gradient": { "type": "radial", "start": [0, 0], "end": [0, 1100],
                                     "stops": [{ "offset": 0, "color": "#1E4FBF" }, { "offset": 1, "color": "#061638" }] } } } }

// Linha que se desenha (trim path)
{ "id": "linha", "type": "shape", "start": 1, "duration": 5,
  "shape": { "kind": "path", "path": { "closed": false, "points": [{ "point": [-300, 0] }, { "point": [300, 0] }] },
             "fill": { "enabled": false }, "stroke": { "color": "#FFC857", "width": 8 },
             "trim": { "end": { "keyframes": [{ "time": 0, "value": 0, "easing": "easeInOutCubic" }, { "time": 1, "value": 1 }] } } } }

// Pêndulo/pulso com 2 keyframes: easing cíclico (onda entre os dois valores; cycles com meio = sem salto)
{ "id": "pendulo", "type": "shape", "duration": 5, "shape": { "kind": "ellipse", "size": [200, 200] },
  "transform": { "position": { "keyframes": [
    { "time": 0, "value": [-300, 0], "easing": { "cyclic": { "offset": 0, "cycles": 3.5 } } },
    { "time": 5, "value": [300, 0] }] } } }

// Cubo metálico girando
{ "id": "cubo", "type": "object3d", "start": 0, "duration": 10, "motionBlur": true,
  "transform3d": { "rotation": { "keyframes": [{ "time": 0, "value": [-25, 0, 0] }, { "time": 10, "value": [-25, 360, 0] }] } },
  "object3d": { "primitive": "cube", "size": 420,
                "material": { "color": "#DDE3EA", "metallic": 1, "roughness": 0.22 } } }

// Órbita: filho de um nulo 3D que gira (loop infinito)
{ "id": "pivo", "type": "null", "duration": 10, "null": { "threeD": true },
  "transform3d": { "rotation": { "keyframes": [{ "time": 0, "value": [0, 0, 0] }, { "time": 4, "value": [0, 360, 0] }], "loop": "cycle" } } }
{ "id": "lua", "type": "object3d", "duration": 10, "parent": "pivo", "transform3d": { "position": [380, 0, 0] },
  "object3d": { "primitive": "sphere", "size": 80, "material": { "color": "#C9CCD3", "roughness": 0.9 } } }

// Pai: a posição do filho é medida A PARTIR do pai. O app, ao trocar o pai, recalcula a posição para a camada não
// mudar de lugar; quem escreve o JSON à mão já escreve a posição relativa ao pai (ex.: [0, -220] = 220 px acima do nulo).

// Nulo: camada invisível que só carrega transformação (2D por padrão; 3D com "threeD": true)
{ "id": "controle", "type": "null", "duration": 10, "transform": { "position": [0, 0] } }
{ "id": "rig", "type": "null", "duration": 10, "null": { "threeD": true }, "transform3d": { "rotation": [0, 45, 0] } }

// Câmera por alvo (órbita) e luzes
{ "id": "camera", "type": "camera", "duration": 10, "camera": { "position": [0, -250, -2600], "target": [0, 0, 0], "fov": 40 } }
// Câmera por rotação: posição X/Y/Z independente da rotação X/Y/Z (rotação 0 olha para +z)
{ "id": "camera2", "type": "camera", "duration": 10, "camera": { "aim": "rotation", "position": [0, 0, -2600], "rotation": [0, -15, 0], "fov": 40 } }
{ "id": "luz", "type": "light", "duration": 10, "light": { "kind": "directional", "intensity": 1.3, "position": [-900, -1300, -1400] } }
{ "id": "ambiente", "type": "light", "duration": 10, "light": { "kind": "ambient", "color": "#A8C0FF", "intensity": 0.3 } }

// Formato 6 — texto 3D extrudado com chanfro, luz com sombra e câmera com profundidade de campo
{ "id": "titulo3d", "type": "object3d", "duration": 10,
  "object3d": { "primitive": "text",
                "text": { "content": "KINESIS", "font": { "family": "sans-serif", "weight": 900 }, "fontSize": 200, "depth": 70, "bevel": 6 },
                "material": { "color": "#E8C547", "metallic": 0.9, "roughness": 0.3, "shading": "pbr" } } }
{ "id": "sol", "type": "light", "duration": 10,
  "light": { "kind": "directional", "intensity": 1.3, "position": [-600, -1400, -900], "castShadows": true, "shadowDarkness": 0.8, "shadowSoftness": 2 } }
{ "id": "cam", "type": "camera", "duration": 10,
  "camera": { "aim": "rotation", "position": [0, -250, -2200], "rotation": [-6, 0, 0], "fov": 40,
              "dof": { "focusDistance": 2200, "range": 300, "blur": 22 } } }
// Ambiente: em "composition": "environment": { "asset": "<id de imagem 2:1>", "intensity": 1.2, "rotation": 0 }
// Vídeo com transparência (metade esquerda = cor, direita = alfa): "video": { "asset": "clip", "alphaPacked": true }
```

Valores possíveis (o schema é a fonte da verdade):
- `type` de camada: `text`, `shape`, `image`, `video`, `audio`, `group`, `object3d`, `model3d`, `camera`, `light`, `null`.
- `shape.kind`: `rectangle`, `ellipse`, `polygon`, `star`, `path`. `primitive`: `cube`, `sphere`, `cylinder`, `cone`, `torus`, `plane`, `text`, `empty`.
- `material.shading`: `pbr` (padrão), `flat`, `toon`, `wireframe`. Texto 3D: `fontSize` 4–2000, `depth` 1–2000, `bevel` 0..`depth`/2
  (o validador acusa `text3d.range`). Sombras: só `directional`/`point` com `castShadows`; `shadowSoftness` 0–8.
  `camera.dof`: `focusDistance` ≈ distância da câmera ao objeto em foco (com a câmera em `[0, y, -2200]` e o objeto em z=0, ~2200).
- Efeitos (`effects[].type`): 68 efeitos em 11 categorias (Cor e luz, Desfoque e nitidez, Distorção, Movimentar e
  transformar, Estilizar, Glitch, Desenho e borda, Procedimental, Fosco/máscara/chave, Tempo e transição, Utilitário).
  Consulte a tabela (seção 7 de `docs/knsproj.md`) antes de usar um efeito: os nomes dos parâmetros são exatos e o
  schema rejeita os desconhecidos. Regras: parâmetros omitidos valem o padrão; números, cores e pontos são animáveis;
  escolhas (`mode`…), liga/desliga e `stops` são estáticos; pontos (`center`…) são px relativos à origem da camada;
  efeitos aleatórios usam `seed` inteiro. Principais:
  - cor: `gradientMap` (stops), `exposure`, `brightnessContrast`, `saturation`, `hueShift`, `fill`, `deepGlow`, `lensFlare`, `glow`, `tint`;
  - desfoque: `blur` (radius), `lensBlur`, `directionalBlur`, `radialBlur` (`mode`: spin/zoom), `sharpen`;
  - distorção: `glass` (refrata as camadas **abaixo** dela), `pinchBulge` (amount −1..1), `warp` (wave/fractal), `mirror`, `twirl`, `ripple`;
  - movimento sem keyframes: `autoShake`, `spin`, `oscillate`, `float`, `pulse`;
  - estilo/glitch: `pixelate`, `dropShadow`, `vignette`, `halftone`, `posterize`, `filmGrain`, `scanlines`, `eightBit` (pixeliza + paleta reduzida), `pixDither` (dithering de Bayer), `pixelEncoder` (ASCII), `kernel` (convolução 3×3), `blockGlitch`, `lineGlitch`, `vhs`, `chromaticAberration`, `rgbSplit`, `staticNoise`, `signalAnalog`, `glitchify` (`speed` 0 congela), `dissolveShake` (`progress` 0..1) — exemplos em `basicos/efeito-*`;
  - borda: `outline`, `findEdges`, `emboss`, `sketch`; geradores: `fractalNoise`, `gradientRamp`, `checkerboard`, `grid` (`mode` + `mix`);
  - chave: `chromaKey`, `lumaKey`, `spillSuppressor`, `matteChoker`; tempo: `echo`, `posterizeTime`, `strobe`, `timeSlice`;
  - utilitário: `depthMap` (só `object3d`/`model3d`), `channelShuffle`, `alphaFromLuma`.
  O antigo `colorAdjust` (v1) não existe mais: use `brightnessContrast`, `saturation` e `hueShift`.
- Transições: `fade`, `slideLeft`, `slideRight`, `slideUp`, `slideDown`, `zoomIn`, `zoomOut`, `spin`, `blur`, `wipeLeft`, `wipeRight`.
- Animadores de texto: `typewriter`, `fade`, `slideUp`, `slideDown`, `slideLeft`, `slideRight`, `scale`, `rotate`, `wave`;
  `unit`: `character` | `word` | `line`; `order`: `forward` | `backward` | `center` | `random`; `mode`: `in` | `out`.
- Easings: `linear`, `hold`, `ease`, `easeIn`, `easeOut`, `easeInOut`, `easeIn/Out/InOut` + `Sine|Quad|Cubic|Quart|Quint|Expo|Circ|Back|Bounce|Elastic`,
  `{"cubicBezier": [x1, y1, x2, y2]}` ou a onda `{"cyclic": {"offset": 0, "cycles": 3.5}}` (oscila entre os dois keyframes; `offset` −1..1 assimetria: negativo sobe rápido/desce devagar, positivo o contrário;
  `offset` 0 e `cycles` com meio, como 2,5 ou 3,5, para começar em 0 e terminar em 1 sem salto).
- Track matte: `"matte": {"layer": "<id irmão>", "mode": "alpha"}` — a camada-fonte some automaticamente.
- Máscaras: `"masks": [{"shape": "ellipse", "mode": "add", "size": [600, 400], "feather": 30}]`.

## Expressões (opcional, formato 3)

Use expressões só quando keyframes seriam trabalhosos ou impossíveis: movimento contínuo (`wiggle`), loops (`loopOut`),
pulsos (`Math.sin`), ou animação **por caractere**. Prefira keyframes normais para entradas e saídas simples.

```jsonc
// Tremor contínuo na posição; loop de ida e volta na rotação; pulso na opacidade
"transform": {
  "position": { "value": [0, 0], "expression": "wiggle(3, 40)" },
  "rotation": { "keyframes": [{ "time": 0, "value": 0 }, { "time": 1, "value": 90 }], "expression": "loopOut(\"pingpong\")" },
  "opacity":  { "value": 1, "expression": "linear(Math.sin(time * 4), -1, 1, 20, 100)" }
}

// Texto que quica letra por letra: animador de texto cujo seletor (amount) tem a expressão
"text": { "content": "BOUNCE", "fontSize": 150,
  "propertyAnimators": [{ "name": "Bounce", "unit": "character", "scale": [0, 0],
    "amount": { "value": 100, "expression": "delay = 0.030;\nmyDelay = delay * textIndex;\nt = (time - inPoint) - myDelay;\nif (t >= 0) {\n  s = 50 * Math.cos(2 * t * 2 * Math.PI) / Math.exp(8 * t);\n  [s, s]\n} else {\n  value\n}" } }] }
```

Regras que evitam erro:
- **Unidades do After Effects dentro da expressão:** escala e opacidade em % (100 = normal), posição medida do canto
  superior esquerdo (`[thisComp.width / 2, thisComp.height / 2]` = centro), cores `[r, g, b, a]` de 0 a 1, rotação em graus. O
  arquivo guarda os valores no formato do Kinesis; a conversão é automática.
- Disponíveis: `time`, `value`, `inPoint`, `outPoint`, `index`, `thisComp`, `thisLayer`, `thisProperty`, `wiggle`, `loopOut`,
  `loopIn` (`cycle`, `pingpong`, `offset`, `continue`), `linear`, `ease`, `easeIn`, `easeOut`, `posterizeTime`, `random`,
  `seedRandom`, `clamp`, `length`, `normalize`, `add`/`sub`/`mul`/`div`, `Math`, e em animadores de texto `textIndex` (a
  partir de 1), `textTotal`, `selectorValue`. **Nada além disso existe** (`effect()`, `sourceText`, `gaussRandom`... não):
  consulte a matriz em `docs/expressoes.md`.
- Vetores são arrays: some com `add(a, b)`, não com `a + b`. Sem parâmetros padrão nem `...spread`.
- Em animador de texto, `scale` e `opacity` do animador são em %; o `amount` (do seletor) é o quanto dessas propriedades cada
  caractere recebe (`textIndex` conta caracteres, `index` é a camada).
- Sempre rode `validate`: ele acusa `expression.syntax` (a CLI só confere parênteses, aspas e comentários; o app mostra a
  linha exata do erro de JavaScript).

## Boas práticas de motion design

- **Hierarquia temporal:** fundo primeiro, elemento principal em seguida, textos por último; escalone entradas
  (0.1–0.3 s entre elementos) em vez de fazer tudo aparecer junto.
- **Easing:** entradas com `easeOutCubic`/`easeOutExpo`/`easeOutBack`, saídas com `easeInCubic`, movimentos de ida e
  volta com `easeInOut*`. Rotação contínua: dois keyframes `linear` (ou `loop: "cycle"`).
- **Leitura:** cada texto fica legível por pelo menos ~1,5 s. Em 1080×1920 use 120–180 px para títulos e 40–64 px para
  apoio; mantenha textos dentro de ±470 px em x e ±820 px em y (margem de segurança).
- **3D:** uma câmera levemente acima (`y` negativo) e afastada dá profundidade; combine luz principal, contraluz
  colorida e ambiente fraca. Metais ficam bons com `metallic: 1` e `roughness` 0.15–0.35. Camadas `null` com `"threeD": true`
  servem de pivô para órbitas, rigs de câmera e grupos 3D (uma câmera/luz pode ser **filha** de um nulo 3D).
  Para sombras visíveis, ponha um `plane` grande como chão (girado `[90, 0, 0]`, abaixo dos objetos) e uma luz com
  `castShadows`. Profundidade de campo: foque no objeto principal e use `blur` 10–30 para não borrar demais.
- **Profundidade 2D:** halos com `blur` grande, sombras suaves (`dropShadow`) e `motionBlur: true` em elementos rápidos.
- **Oscilações regulares** (pêndulo, pulso, balanço): use 2 keyframes com `easing: {"cyclic": {…}}` em vez de dezenas de keyframes.
- Termine animações antes do fim da composição ou use `transitionOut` para sair de forma limpa.
- Prefira poucos keyframes bem escolhidos a muitos keyframes lineares.

## Checklist antes de entregar

- [ ] `validate` sem erros (e avisos compreendidos)
- [ ] `preview` conferido: enquadramento, legibilidade e ritmo ok (ignorando o que está em "approximations")
- [ ] Todos os `parent`/`matte` apontam para irmãos do mesmo contêiner; 2D só com 2D, 3D só com 3D (nulo 3D = `null.threeD`)
- [ ] Assets copiados com `add-asset`; nenhum caminho fora de `assets/`
- [ ] Tempos de keyframe relativos ao início de cada camada
- [ ] `.knsproj` gerado com `pack` e caminho informado ao usuário
