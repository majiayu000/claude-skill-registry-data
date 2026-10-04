---
name: manim
description: Guia abrangente para Manim Community - framework Python para criar animações matemáticas e vídeos educacionais com controle programático
version: 1.0.0
author: manim-community
repo: https://github.com/ManimCommunity/manim
license: MIT
tags: [Video, Python, Animation, Manim, Mathematical, Educational, Visualization, LaTeX, 3Blue1Brown]
dependencies: [manim>=0.19.0, python>=3.8]
---

# Manim Community - Motor de Animação Matemática

Conjunto abrangente de habilidades para criar animações matemáticas usando Manim Community, um framework Python para criar vídeos explicativos de matemática de forma programática, popularizado por 3Blue1Brown.

## Quando usar

Use essa habilidade sempre que estiver trabalhando com código Manim para obter conhecimento específico do domínio sobre:

- Criar animações matemáticas e visualizações
- Construir conteúdo de vídeo educacional de forma programática
- Trabalhar com formas geométricas e transformações
- Animar equações LaTeX e fórmulas matemáticas
- Criar gráficos, diagramas e sistemas de coordenadas
- Implementar sequências de animação baseadas em cenas
- Renderizar diagramas matemáticos de alta qualidade
- Construir conteúdo visual explicativo para ensino

## Conceitos Fundamentais

Manim permite que você crie animações usando:
- **Scenes**: Tela para suas animações onde você orquestra mobjects
- **Mobjects**: Objetos matemáticos que podem ser exibidos (formas, texto, equações)
- **Animations**: Transformações aplicadas a mobjects (Write, Create, Transform, FadeIn)
- **Transforms**: Metamorfose entre diferentes estados de mobjects
- **Integração LaTeX**: Suporte nativo para renderizar notação matemática
- **Simplicidade Python**: Use Python para especificar programaticamente o comportamento da animação

## Recursos Principais

- Posicionamento preciso de objetos matemáticos e transformações
- Renderização nativa de LaTeX para equações e fórmulas
- Biblioteca extensa de formas (círculos, retângulos, setas, polígonos)
- Sistemas de coordenadas e gráficos de funções
- Operações booleanas em formas geométricas
- Controles de câmera e gerenciamento de cenas
- Renderização de vídeo de alta qualidade
- Integração com notebook IPython/Jupyter
- Extensão VS Code com visualização em tempo real

## Como usar

Leia arquivos de regra individuais para explicações detalhadas e exemplos de código:

### Conceitos Fundamentais
- **[references/scenes.md](references/scenes.md)** - Criando cenas e organizando animações
- **[references/mobjects.md](references/mobjects.md)** - Entendendo objetos matemáticos e formas
- **[references/animations.md](references/animations.md)** - Tipos e técnicas de animação principal
- **[references/latex.md](references/latex.md)** - Renderizando equações LaTeX e fórmulas

Para tópicos adicionais incluindo transforms, timing, formas, sistemas de coordenadas, animações 3D, movimento de câmera e recursos avançados, consulte a [documentação abrangente de Manim Community](https://docs.manim.community/).

## Exemplo de Início Rápido

```python
from manim import *

class SquareToCircle(Scene):
    def construct(self):
        # Create a square
        square = Square()
        square.set_fill(BLUE, opacity=0.5)

        # Create a circle
        circle = Circle()
        circle.set_fill(RED, opacity=0.5)

        # Animate square creation
        self.play(Create(square))
        self.wait(1)

        # Transform square into circle
        self.play(Transform(square, circle))
        self.wait(1)

        # Fade out
        self.play(FadeOut(square))
```

Renderize com: `manim -pql script.py SquareToCircle`

## Boas Práticas

1. **Herde de Scene** - Todas as animações devem estar em uma classe que herda de Scene
2. **Use o método construct()** - Coloque todo o código de animação dentro do método construct()
3. **Pense em camadas** - Adicione mobjects à cena antes de animá-los
4. **Use self.play()** - Anime mobjects usando self.play(Animation(...))
5. **Teste com baixa qualidade** - Use a flag `-ql` para renderizações de visualização mais rápidas
6. **Aproveite LaTeX** - Use Tex() e MathTex() para notação matemática
7. **Agrupe objetos relacionados** - Use VGroup para gerenciar múltiplos mobjects juntos
8. **Visualize frequentemente** - Use a flag `-p` para abrir automaticamente vídeos renderizados

## Uso de Linha de Comando

```bash
# Preview at low quality (fast)
manim -pql script.py SceneName

# Render at high quality
manim -pqh script.py SceneName

# Save last frame as image
manim -s script.py SceneName

# Render multiple scenes
manim script.py Scene1 Scene2
```

## Recursos

- **Documentação**: https://docs.manim.community/
- **Repositório**: https://github.com/ManimCommunity/manim
- **Galeria de Exemplos**: https://docs.manim.community/en/stable/examples.html
- **Comunidade Discord**: https://www.manim.community/discord/
- **Canal 3Blue1Brown**: https://www.youtube.com/c/3blue1brown
- **Licença**: MIT