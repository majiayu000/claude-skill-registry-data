---
name: beamer-unesp
description: Gerar apresentações Beamer LaTeX no padrão UNESP dark mode. Usar quando o usuário pedir para criar slides, apresentações, ou palestras em Beamer/LaTeX. O template usa tema Madrid com cores escuras (fundo RGB 26,26,26), ícones FontAwesome5, e suporte a código Python/outros. Ideal para apresentações técnicas, acadêmicas ou palestras.
---

# Beamer UNESP Dark Mode

Skill para criar apresentações Beamer no padrão visual do Ney Lemke (UNESP).

## Características do Template

- **Aspecto**: 16:9 (aspectratio=169), fonte 12pt
- **Tema**: Madrid + beaver (customizado dark)
- **Cores**:
  - `accent` (azul): destaque principal, links, estrutura
  - `secondary` (roxo): destaque secundário
  - `success` (verde): exemplos positivos
  - `warning` (amarelo): alertas leves
  - `danger` (vermelho): alertas críticos
- **Ícones**: FontAwesome5 (`\faIcon`)

## Estrutura Padrão

```latex
\section{Nome da Seção}

\begin{frame}{Título do Slide}
    % Conteúdo
\end{frame}
```

## Blocos Disponíveis

```latex
% Bloco padrão (fundo accent)
\begin{block}{Título}
    Conteúdo
\end{block}

% Bloco de alerta (fundo vermelho)
\begin{alertblock}{Atenção}
    Conteúdo crítico
\end{alertblock}

% Bloco de exemplo (fundo verde)
\begin{exampleblock}{Exemplo}
    Conteúdo positivo
\end{exampleblock}
```

## Layout em Colunas

```latex
\begin{columns}
    \begin{column}{0.5\textwidth}
        % Coluna esquerda
    \end{column}
    \begin{column}{0.5\textwidth}
        % Coluna direita
    \end{column}
\end{columns}
```

## Código Fonte

```latex
\begin{frame}[fragile]{Título}
    \begin{block}{Descrição}
        \begin{lstlisting}[language=Python]
def exemplo():
    return "Hello"
        \end{lstlisting}
    \end{block}
\end{frame}
```

## Ícones FontAwesome5 Comuns

| Contexto | Ícones |
|----------|--------|
| Tech | `\faCode`, `\faServer`, `\faDatabase`, `\faNetworkWired` |
| IA | `\faRobot`, `\faBrain`, `\faMicrochip` |
| Docs | `\faFile`, `\faBook`, `\faGraduationCap` |
| Alertas | `\faExclamationTriangle`, `\faCheckCircle`, `\faBug` |
| Misc | `\faLightbulb`, `\faBolt`, `\faArrowRight`, `\faEnvelope` |

## Descrições com Ícones Coloridos

```latex
\begin{description}
    \item[\textcolor{accent}{\faCube} Item] Descrição
    \item[\textcolor{success}{\faBrain} Outro] Descrição
\end{description}
```

## Workflow

1. Copiar `assets/template.tex` e `assets/logo_unesp.png` para o diretório de trabalho
2. Substituir placeholders:
   - `{{TITLE}}`, `{{SHORT_TITLE}}`, `{{SUBTITLE}}`
   - `{{AUTHOR}}`
   - `{{TITLE_ICONS}}` (ex: `\faRobot\, \faCode`)
   - `{{CONTENT}}` (slides e seções)
   - `{{CLOSING_ICON}}`, `{{CLOSING_MESSAGE}}`, `{{FOOTER_ICONS}}`
   - `{{CONTACT_INFO}}` (recursos adicionais)
3. Compilar com `pdflatex` ou `latexmk`

**Importante**: O logo `logo_unesp.png` deve estar no mesmo diretório do arquivo `.tex`.

## Boas Práticas

- Usar `\section{}` para agrupar slides relacionados
- Preferir colunas para comparações lado a lado
- Usar `alertblock` para riscos/limitações, `exampleblock` para benefícios
- Incluir ícones relevantes nos títulos de blocos
- Manter slides concisos (máx 6-7 itens por lista)
- Usar `[fragile]` em frames com código
