---
name: dl-qt-qml-ui
description: "Create, redesign, or review modern desktop interfaces in Qt 6 / QML / Qt Quick with the polish of modern desktop products (Linear, VS Code, Notion, Raycast). Use for Qt Quick dashboards, sidebars, design systems, dark/light themes, responsive desktop layouts, animations, component libraries, and UI modernization. Do not use for HTML-only apps or Qt Widgets-only tasks unless migrating the UI to QML."
license: MIT
compatibility: codex, claude-code, opencode
metadata:
  language: pt-BR
  stack: qt6-qml-qtquick
---

# Qt/QML desktop UI with web-app polish

**Missão:** construir UI desktop **nativa em Qt 6 / QML**, com refinamento visual, fluidez, acessibilidade e padrões de UX de produtos desktop modernos. **Referências visuais são inspiração, não exigências de tecnologia nem de estilo.**

## Quando ativar

Use esta skill quando a tarefa envolver criação/refatoração de interface com Qt Quick, QML, Qt Quick Controls ou PySide6/PyQt6 + QML: dashboard, IDE, painel de configurações, aplicativo de produtividade, biblioteca de componentes, design tokens, temas, animações, acessibilidade e layout responsivo.

Não a use para converter aplicações web desnecessariamente nem para impor QML a um projeto de Qt Widgets sem solicitação explícita de migração.

## Procedimento obrigatório

1. **Inspecione antes de alterar.** Leia arquivos de build (`CMakeLists.txt`, `pyproject.toml`, `.pro`), `main.cpp`/bootstrap Python, QML existentes, assets, convenções e versão instalada do Qt. Descubra sistema operacional e sistema de navegação. Preserve as integrações e a arquitetura do projeto. Se for um projeto novo, tome como base Qt **6.5+**, CMake e Qt Quick Controls Basic; adapte à versão do ambiente.
2. **Defina o produto visual.** Determine público, tarefa central da tela, estrutura de informação e uma direção de design (p.ex. developer tool, productivity workspace, data console). Não produza o "dashboard genérico" quando o domínio pede outra metáfora. Se a solicitação for aberta, faça uma escolha visual coerente sem bloquear o trabalho por perguntas dispensáveis.
3. **Estabeleça tokens antes dos componentes.** Cores semânticas, tipografia, espaçamentos (escala de 4/8), raios, bordas, estados, densidade e motion. Use um singleton QML (`Theme.qml`) para tokens compartilhados. Leia [`references/design-language.md`](references/design-language.md).
4. **Construa a composição macro antes dos detalhes.** Determine sidebar/nav, cabeçalho, hierarquia, área de conteúdo, scroll e estados vazios. Priorize alinhamento, espaçamento e legibilidade. Faça uma tela principal convincente antes de multiplicar páginas.
5. **Implemente com controles reais.** Prefira `QtQuick.Controls.Basic` para controles redesenhados, `QtQuick.Layouts`, bindings declarativos e componentes reutilizáveis. Preserve teclado, foco, semântica e feedback. Leia [`references/qml-implementation.md`](references/qml-implementation.md). Para projeto novo, consulte `assets/starter/` como referência funcional.
6. **Complete os estados.** Hover, pressed, focus, disabled, loading, empty, error, selected, scroll e feedback de ação. O modo claro, se exigido, precisa ser realmente legível. Use animações discretas e configuráveis; não anime todo elemento sem propósito.
7. **Valide execução e aparência.** Compile e rode se houver toolchain. Execute lint (`qmllint`) quando disponível e inspecione a UI em tamanhos desktop distintos. Se puder gerar screenshots, examine-as, corrija falhas e reporte o que realmente testou. Sem toolchain, faça validação estática e **deixe explícito que não executou**. Siga [`references/quality-gates.md`](references/quality-gates.md).

## Princípios visuais que devem aparecer no código

- Aparência de aplicação de trabalho, não de página web: navegação persistente, sidebar limpa, hierarquia de informação, ações previsíveis, áreas de rolagem apropriadas.
- Densidade controlada: boa quantidade de informação visível sem sacrificar respiro; tipografia legível, textos curtos, valores com destaque, dados secundários discretos.
- Superfícies coordenadas: fundo, sidebar, painéis, bordas discretas, acentos usados com parcimônia; evite sombras, gradientes e vidro excessivos.
- Design tokens **semânticos** e consistentes. Não espalhe códigos hexadecimais pelos arquivos de componentes.
- Layout adaptável a janelas redimensionáveis, DPI e textos longos. Utilize `RowLayout`, `ColumnLayout`, `GridLayout`, `Layout.*`, `ScrollView`, `ListView`/`TableView` conforme o caso.
- Motion cuidadoso: 120–220 ms para hover/seleção, ~180–280 ms para transições de áreas leves quando apropriado. Use `Behavior`/`Transition` com moderação. Evite efeitos que prejudiquem a fluidez.
- Ícones coesos: preferir SVGs locais licenciados e incorporados como recursos; não substituir iconografia por emoji. Se não houver ícones, use texto e geometria simples.
- Acessibilidade: contraste legível, navegação por teclado, foco visível, labels acessíveis, alvos confortáveis, suporte a configurações de movimento reduzido quando disponíveis.

## Restrições técnicas importantes

- **Não** troque o backend Qt/C++/Python nem acrescente WebView ou HTML/CSS só para reproduzir o visual, a menos que seja pedido.
- **Não** personalize os estilos nativos de Windows/macOS. Para controles customizados, use `QtQuick.Controls.Basic` ou um estilo customizado construído sobre templates Qt Quick Controls. Não misture vários estilos de Controls no mesmo componente.
- **Não** crie uma titlebar frameless por padrão: ela exige implementação correta de drag, resize, maximize, menus e comportamento multiplataforma. Mantenha a moldura do SO, salvo solicitação.
- **Não** misture `anchors` para a geometria de um item que esteja sendo dimensionado/posicionado por `Layout` pai. Anchors são adequados **dentro** dos componentes.
- **Não** faça I/O pesado, timers frequentes ou computações caras no thread da UI; use backend/modelos. Prefira `ListView`/`TableView` a `Repeater` em listas extensas.
- Use as APIs **disponíveis na versão instalada do Qt**; não suponha módulos gráficos, fontes ou bibliotecas de ícones extras.
- Evite demo enganosa: ações visuais devem ter um efeito real ou ser descritas claramente como placeholders.

## Entrega esperada

Para cada implementação, retorne: (1) o que mudou; (2) escolhas de design; (3) arquivos afetados; (4) como executar; (5) validações realmente feitas e pendências. Na revisão de UI, cite defeitos concretos (hierarquia, contraste, espaçamento, estados e performance) e proponha correções aplicáveis.

## Material de referência — carregamento sob demanda

- `references/design-language.md`: tokens, composição, padrões desktop e estados.
- `references/qml-implementation.md`: arquitetura, QML/Qt, CMake/Python, anti-patterns e componentes.
- `references/quality-gates.md`: critérios de aceite, testes e revisão visual.
- `assets/starter/`: shell de dashboard desktop em **Qt 6.5+ + CMake + Qt Quick Controls Basic**, com temas claro/escuro e componentes prontos para adaptação. **Não copie o domínio ou layout do starter automaticamente.**

## Comandos úteis de verificação

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
# qmlformat / qmllint: execute se estiverem instalados e configurados no projeto
```

Fontes técnicas: https://doc.qt.io/qt-6/qtquick-bestpractices.html ; https://doc.qt.io/qt-6/qtquickcontrols-customize.html ; https://doc.qt.io/qt-6/qtquick-performance.html ; https://doc.qt.io/qt-6/qml-singleton.html
