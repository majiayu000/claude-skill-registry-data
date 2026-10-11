---
name: liquid-glass-apple
description: >-
  Aplicar a receita Liquid Glass a componentes de qualquer projeto web, criando novas superfícies ou adaptando as existentes. Use quando Liquid Glass inspirado na Apple for solicitado. Preserve a arquitetura, o framework, a identidade visual e as interações do projeto, com refração nas bordas, transparência calibrada, reflexos e conteúdo legível.
metadata:
  version: "1.0.1"
---

# Liquid Glass Apple · V1

Aplicar Liquid Glass aos elementos necessários ao projeto do usuário. A receita define a óptica e o acabamento do material; a função, a composição, o conteúdo e a identidade visual vêm do projeto em que ela será aplicada. Autor: **Heitor Minuzzo**.

Comece pela interface e pela arquitetura existentes. A integração deve funcionar com o framework, a biblioteca de componentes e o sistema de estilos do projeto. O núcleo portátil em `assets/core/` fornece a implementação de referência; `assets/reference/` fornece referências visuais do material em situações de teste. O exemplo portátil é uma ferramenta de verificação opcional, independente da aplicação que receberá o vidro.

## Receita obrigatória

Leia [material](references/material.md) para a especificação óptica e [integração](references/integration.md) para o caminho adequado à tecnologia do projeto. Na implementação DOM/CSS, use o núcleo portátil com `strength:1`, `edgeProfile:'extended'`, `edgeWidth:1.2`, `adaptToPhotos:true`. Em um renderer existente, transporte a mesma geometria, refração, tonalidade e reflexão. Preserve a calibração aprovada; mudanças nos parâmetros ópticos dependem de um pedido explícito de aperfeiçoamento.

Preserve estes resultados em todas as superfícies:

- **Bordas:** alongamento, compressão e um trecho espelhado acompanham topo, fundo, laterais e cantos. O ombro começa no contorno real, avança para dentro e escala com altura/raio. Não pinte faixas brancas nem acrescente ondulação no centro.
- **Centro:** pouco blur (`.25px`). Texto do cenário perde contraste apenas sob o vidro; o texto original fora dele permanece intacto. Não aumente o blur para tornar rótulos legíveis.
- **Fotografias:** cores reconhecíveis, difusão suave e transmissão calibrada: `.56` no claro / `.38` no escuro; crominância `.70` / `.72`. Não adicione uma placa cinza ou branca sobre a lente. Esses valores pertencem ao tratamento óptico, não a `opacity` do componente.
- **Fundo plano:** um reflexo direcional contínuo no ombro, um único limite fino e sombra curta dão volume mesmo sobre branco puro. Não use contorno duplo ou sombra difusa em toda a volta como substitutos.
- **Conteúdo:** rótulos, ícones, campos e controles reais ficam acima da lente, nítidos e interativos. Nunca filtre ou reduza a opacidade do componente inteiro.

O núcleo calcula geometria, máscaras, tonalidade e adaptação fotográfica; a tabela em [material](references/material.md#curva-aprovada) documenta a calibração completa. A [referência fotográfica escolhida pelo autor](assets/reference/scaled-photo-light.png) mostra a transparência e a refração aprovadas. Se outro renderer for necessário, preserve esses cálculos e valide o resultado contra as capturas. Se não houver uma fonte visual sincronizável, explique o limite e use o fallback; não apresente blur CSS como a mesma refração.

## Criar ou converter componentes

1. **Conhecer o projeto:** identifique stack, componentes/primitivas disponíveis, tokens de estilo, temas, interação e escopo do pedido. Determine quais superfícies receberão vidro e de onde virá o conteúdo visual atrás de cada uma.
2. **Escolher a integração:** aproveite a organização e as APIs existentes. A integração pode ser uma classe, um wrapper, uma variante da biblioteca, uma diretiva ou um adapter de renderer, conforme o projeto. A implementação de referência é independente de framework e não exige importar a página de exemplo.
3. **Ao criar:** use a primitiva semântica apropriada à função. Defina tamanho, espaçamento, tipografia e raio conforme a interface. Para controles compactos novos, prefira cápsula ou círculo; superfícies maiores adotam uma geometria coerente com sua função.
4. **Ao converter:** mantenha API, handlers, valores, validação, teclado, ARIA e ciclo de vida. Substitua o preenchimento, a borda e a sombra que encobrem o vidro por suas camadas materiais, com estilos limitados ao componente convertido.
5. **Compor as camadas:** separe fundo óptico, estado/seleção, conteúdo interativo e acabamento de borda. Na integração DOM, correspondem a `.glass-material`, estado quando necessário, `.glass-content` e `.glass-rim`. Em outra abstração, preserve essa separação e a silhueta compartilhada. Use [componentes e estados](references/components.md) conforme os controles presentes no pedido.
6. **Sincronizar:** alinhe a fonte visual com posição, rolagem, resize e tema. A adaptação fotográfica do núcleo usa imagens DOM; um renderer próprio precisa preservar o tratamento separado de texto e fotos. Use mount/unmount e o mecanismo de animação do projeto para atualizar e liberar recursos.
7. **Validar na aplicação:** confira o material nos componentes e cenários reais usando [validação](references/validation.md). Compare a óptica com as referências fornecidas, mantendo a composição e a identidade do projeto.

## Estados também são vidro

Não deixe um menu opaco atrás de um gatilho em vidro. O menu aberto deve revelar e refratar o cenário; a opção selecionada deve ter preenchimento translúcido e seu próprio acabamento de borda. Indicadores de switcher, toggles e seleções compartilham o tratamento do material, com conteúdo acima deles. Evite refiltrar o fundo em cada estado sobreposto.

Não preserve o retângulo preto nativo ao clicar em um campo ou gatilho convertido. Substitua o foco apenas nesse componente por uma indicação coerente com o vidro, mantendo foco perceptível por teclado. Não aplique `outline:none` globalmente. Um `<select>` nativo não ganha um popup Liquid Glass só porque o gatilho recebeu CSS: quando o pedido incluir o menu, use a primitiva acessível de popup/listbox do produto. Detalhes, estrutura e tratamento de portais estão em [componentes e estados](references/components.md).

## Com cores e sem cores

Sempre entregue uma variante de fundo **neutro / sem cores** e outra **com cores**, com a mesma receita de vidro. Em uma aplicação, reutilize as preferências existentes ou ofereça uma alternância simples. Para um componente isolado ou uma entrega estática, inclua as duas variantes ou uma prop/configuração; não acrescente uma tela de configurações à força. Preserve uma escolha explícita do usuário.

Cores do fundo seguem a direção visual do projeto e ficam atrás do vidro. Preserve marca, acentos e cores funcionais. A receita deve produzir vidro também sobre fundos neutros; os presets incluídos no CSS são recursos opcionais para teste ou composição.

## Composição definida pelo projeto

A estrutura da interface é determinada pelo objetivo do usuário e pelo contexto do produto. Escolha os componentes, sua quantidade, hierarquia e disposição a partir desse contexto. Em interfaces existentes, preserve a composição e aplique o material aos elementos solicitados. Em interfaces novas, desenhe a composição que resolve a tarefa usando a linguagem visual do projeto.

As referências visuais servem para conferir refração, transparência, borda e legibilidade. Rótulos, ícones, medidas e arranjos dessas referências são exemplos substituíveis. Cada componente solicitado usa a mesma receita, adaptada à sua geometria e ao seu contexto real.

## Movimento e ciclo de vida

Quando houver movimento, use a biblioteca e o ritmo do projeto. A lente acompanha a geometria real durante deslocamento e resize; o conteúdo continua nítido e interativo. Leia [movimento](references/motion.md) para sincronização, estados de pressão e preferências de acessibilidade. Adicione interações de arraste somente quando fizerem parte da função pedida.

Otimize trabalho repetido, preservando a receita visual: reutilize mapas idênticos e leituras do cenário, mantenha caches limitados e atualize a fonte quando ela mudar. Não reduza resolução, frequência de atualização ou intensidade do efeito para melhorar desempenho sem um pedido explícito. Compare capturas antes/depois e verifique interação e alinhamento; suporte a CSS não comprova fluidez no dispositivo.

## Recursos e conclusão

- `assets/core/`: material, lente ES module sem dependências e tipos; `glass-range.*` é uma integração opcional de slider nativo com barra/bolinha em vidro e crescimento discreto ao pressionar.
- `assets/example/index.html`: laboratório portátil para comparar o material, servido por HTTP. Os controles técnicos são instrumentos de desenvolvimento, não requisitos de interface.
- `assets/reference/` e [origem](references/origin.md): capturas reais, procedência, licença e limites da comparação.

Copie os recursos pertinentes e valide claro/escuro sobre **texto, fotos e fundo plano**, inclusive bordas laterais, tamanho maior, menu aberto, seleção e foco. Respeite transparência reduzida, contraste aumentado e cores forçadas com fallback sólido; movimento reduzido mantém a função sem animação. Informe quais estados/cenários foram verificados e qualquer limitação do renderer ou navegador. Não declare fidelidade completa se só o fallback foi testado.
