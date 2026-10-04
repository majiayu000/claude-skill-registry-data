---
name: remotion
description: Melhores práticas e guia abrangente do Remotion - criação de vídeos programática em React com animações, composições e manipulação de mídia
version: 1.0.0
author: remotion-dev
repo: https://github.com/remotion-dev/skills
license: MIT
tags: [Video, React, Animation, Remotion, Composition, Media, 3D, Audio, Captions, Charts, Lottie, Tailwind]
dependencies: [remotion>=4.0.0, react>=18.0.0]
---

# Remotion - Criação de Vídeo em React

Conjunto abrangente de skills para criar vídeos programaticamente usando Remotion, um framework para criar vídeos de forma programática usando React.

## Quando usar

Use este skill sempre que estiver lidando com código Remotion para obter conhecimento específico do domínio sobre:

- Criar composições de vídeo com componentes React
- Animar elementos usando animações baseadas em frames
- Trabalhar com assets de áudio, vídeo e imagem
- Construir gráficos e visualizações de dados
- Implementar animações de texto e legendas
- Usar conteúdo 3D com Three.js
- Aplicar transições e sequenciamento
- Integrar TailwindCSS e animações Lottie

## Conceitos Centrais

Remotion permite que você crie vídeos usando:
- **Componentes React**: Construa conteúdo de vídeo com sintaxe React familiar
- **Animações Baseadas em Frames**: Todas as animações controladas pelo hook `useCurrentFrame()`
- **Composições**: Defina composições de vídeo com duração, dimensões e props
- **Assets**: Importe e manipule imagens, vídeos, áudio e fontes
- **Renderização**: Exporte vídeos programaticamente com configurações personalizáveis

## Recursos Principais

- Controle quadro a quadro sobre animações
- Cálculo dinâmico de metadados
- Processamento de mídia (corte, volume, velocidade, pitch)
- Geração e exibição de legendas
- Visualização de dados com gráficos
- Integração de conteúdo 3D
- Animações de texto profissionais
- Transições e sequenciamento de cenas

## Como usar

Leia os arquivos de regras individuais para explicações detalhadas e exemplos de código:

### Animação e Timing Principais
- **[references/animations.md](references/animations.md)** - Técnicas fundamentais de animação para Remotion
- **[references/timing.md](references/timing.md)** - Curvas de interpolação: linear, easing, animações spring
- **[references/sequencing.md](references/sequencing.md)** - Atraso, corte e limitação de duração de itens
- **[references/trimming.md](references/trimming.md)** - Corte do início ou fim de animações

### Composições e Metadados
- **[references/compositions.md](references/compositions.md)** - Definindo composições, stills, pastas, props padrão
- **[references/calculate-metadata.md](references/calculate-metadata.md)** - Definir dinamicamente duração, dimensões e props da composição

### Assets e Mídia
- **[references/assets.md](references/assets.md)** - Importando imagens, vídeos, áudio e fontes
- **[references/images.md](references/images.md)** - Incorporando imagens usando o componente Img
- **[references/videos.md](references/videos.md)** - Incorporando vídeos com corte, volume, velocidade, loop, pitch
- **[references/audio.md](references/audio.md)** - Usando áudio e som com corte, volume, velocidade, pitch
- **[references/gifs.md](references/gifs.md)** - Exibindo GIFs sincronizados com a timeline

### Texto e Tipografia
- **[references/text-animations.md](references/text-animations.md)** - Tipografia e padrões de animação de texto
- **[references/measuring-text.md](references/measuring-text.md)** - Medindo dimensões de texto, ajustando texto, verificando estouro
- **[references/fonts.md](references/fonts.md)** - Carregando Google Fonts e fontes locais

### Legendas e Transcrição
- **[references/display-captions.md](references/display-captions.md)** - Exibindo legendas com páginas ao estilo TikTok e realce de palavras
- **[references/import-srt-captions.md](references/import-srt-captions.md)** - Importando arquivos de legendas .srt usando @remotion/captions
- **[references/transcribe-captions.md](references/transcribe-captions.md)** - Transcrevendo áudio para gerar legendas

### Visualização de Dados
- **[references/charts.md](references/charts.md)** - Padrões de gráficos e visualização de dados

### Recursos Avançados
- **[references/3d.md](references/3d.md)** - Conteúdo 3D usando Three.js e React Three Fiber
- **[references/lottie.md](references/lottie.md)** - Incorporando animações Lottie
- **[references/transitions.md](references/transitions.md)** - Padrões de transição de cenas

### Estilo e Layout
- **[references/tailwind.md](references/tailwind.md)** - Usando TailwindCSS em Remotion
- **[references/measuring-dom-nodes.md](references/measuring-dom-nodes.md)** - Medindo dimensões de elementos DOM

### Processamento de Mídia (Mediabunny)
- **[references/can-decode.md](references/can-decode.md)** - Verificar se um vídeo pode ser decodificado pelo navegador
- **[references/extract-frames.md](references/extract-frames.md)** - Extrair frames de vídeos em timestamps específicos
- **[references/get-audio-duration.md](references/get-audio-duration.md)** - Obter a duração de um arquivo de áudio
- **[references/get-video-dimensions.md](references/get-video-dimensions.md)** - Obter a largura e altura de um arquivo de vídeo
- **[references/get-video-duration.md](references/get-video-duration.md)** - Obter a duração de um arquivo de vídeo

## Exemplo de Início Rápido

```tsx
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";

export const MyComposition = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 2 * fps], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ opacity }}>
      <h1>Hello Remotion!</h1>
    </div>
  );
};
```

## Melhores Práticas

1. **Sempre use `useCurrentFrame()`** - Controle todas as animações a partir do frame atual
2. **Evite animações CSS** - Elas não serão renderizadas corretamente em vídeos
3. **Pense em segundos** - Multiplique o tempo em segundos por `fps` para cálculos de frames
4. **Use interpolate para animações suaves** - Interpolação integrada com funções de easing
5. **Limite a extrapolação** - Evite que valores ultrapassem os intervalos pretendidos
6. **Teste frequentemente** - Visualize no Remotion Studio antes de renderizar

## Recursos

- **Documentação**: https://www.remotion.dev/docs
- **Repositório**: https://github.com/remotion-dev/remotion
- **Repositório de Skills**: https://github.com/remotion-dev/skills
- **Comunidade**: Discord e GitHub Discussions
- **Licença**: MIT