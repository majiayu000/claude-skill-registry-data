---
name: "lang-latex"
description: "Fornece padrões de engenharia e tipografia acadêmica/científica em LaTeX (LaTeX2e e LuaLaTeX/XeLaTeX). Cobre estruturação modular de documentos multinível, gestão de bibliografia com BibLaTeX/Biber, ilustrações com TikZ, formatação matemática rigorosa (amsmath/mathtools), comandos customizados (newcommand/ProvideDocumentCommand) e prevenção de erros comuns de compilação."
---

# Habilidade de IA: Engenharia de LaTeX (LaTeX Specialist)

Esta skill orienta a inteligência artificial a atuar como especialista no ecossistema **LaTeX** (incluindo motores modernizados como XeLaTeX e LuaLaTeX), focando na redação e estruturação profissional de teses, dissertações, livros técnicos, artigos acadêmicos e relatórios científicos.

---

## 🧭 Diretrizes de Desenvolvimento em LaTeX

Ao atuar nesta skill, aplique rigorosamente os seguintes padrões:

### 1. Estruturação Modular do Projeto
- **Documento Mestre Limpo**: O arquivo principal (`main.tex`) deve conter o pré-ambulo estruturado e as chamadas aos capítulos/seções via `\input{sections/nome.tex}` ou `\include{chapters/nome.tex}`.
- **Organização de Pastas**:
  - `figures/`: Imagens e esquemas TikZ.
  - `styles/` ou `packages/`: Pacotes e macros customizadas (`custom.sty`).
  - `bibliography.bib`: Base de dados bibliográfica.

### 2. Escolha de Motor e Pacotes Modernos
- **Prefira LuaLaTeX / XeLaTeX**: Para projetos novos, utilize LuaLaTeX ou XeLaTeX com o pacote `fontspec` para suporte nativo a UTF-8 e fontes do sistema (OTF/TTF).
- **Pacotes Essenciais Recomendados**:
  - Tipografia Matemática: `amsmath`, `amssymb`, `mathtools`.
  - Tabelas Profissionais: `booktabs` (evite linhas verticais em tabelas acadêmicas), `tabularx`, `array`.
  - Imagens e Diagramas: `graphicx`, `tikz`, `pgfplots`.
  - Links e Referências Cruzadas: `hyperref`, `cleveref` (deve ser carregado após o `hyperref`).

### 3. Bibliografia com BibLaTeX + Biber
- **Substituir natbib/BibTeX por BibLaTeX**: Utilize `biblatex` com o backend `biber` para suporte completo a UTF-8 e estilos bibliográficos flexíveis (como ABNT, IEEE, APA):
  ```latex
  \usepackage[backend=biber, style=numeric, sorting=nyt]{biblatex}
  \addbibresource{bibliography.bib}
  ```

### 4. Definição Limpa de Macros e Comandos
- **Sintaxe Moderna (LaTeX3 / `xparse`)**: Defina macros com argumentos opcionais ricos usando `\NewDocumentCommand` em vez de `\newcommand` legado:
  ```latex
  \NewDocumentCommand{\codevar}{m o}{%
    \texttt{#1}\IfValueT{#2}{\space\textnormal{(#2)}}%
  }
  ```

### 5. Boas Práticas de Formatação Tipográfica
- **Aspas Corretas**: Use ``aspas duplas'' em vez de `"aspas simples"`.
- **Hífen vs. Meio-risco vs. Travessão**: Use `-` para palavras compostas, `--` para faixas de valores (ex: 10--20) e `---` para travessões explicativos.

---

## 🧰 Padrões de Código Recomendados

### Documento Mestre Modular (`main.tex`)

```latex
% !TEX program = lualatex
\documentclass[12pt, a4paper, oneside]{article}

% --- Pré-ambulo: Pacotes Fundamentais ---
\usepackage{fontspec}
\setmainfont{Latin Modern Roman}

% Idioma e Ajustes de Margem
\usepackage[portuguese]{babel}
\usepackage[top=3cm, bottom=2cm, left=3cm, right=2cm]{geometry}

% Matemática e Símbolos
\usepackage{amsmath, amssymb, mathtools}

% Tabelas e Figuras
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{tikz}

% Bibliografia Avançada
\usepackage[backend=biber, style=alphabetic, sorting=nyt]{biblatex}
\addbibresource{bibliography.bib}

% Links e Referências Inteligentes
\usepackage[colorlinks=true, linkcolor=blue, citecolor=teal, urlcolor=magenta]{hyperref}
\usepackage{cleveref}

% --- Macros Customizadas ---
\NewDocumentCommand{\vectornorm}{m}{%
  \left\lVert #1 \right\rVert
}

\title{\textbf{Modelagem Estocástica de Redes Complexas}}
\author{Dandara Gabriel \and Equipe de Pesquisa}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
Este trabalho apresenta um modelo matemático para previsão de convergência em grafos direcionados orientados a eventos.
\end{abstract}

\tableofcontents
\newpage

% --- Conteúdo Modular ---
\section{Introdução}
A análise de grafos dinâmicos é fundamental para a compreensão de sistemas complexos~\cite{smith2024}.

\section{Fundamentação Matemática}
Dada uma matriz de adjacência $A \in \mathbb{R}^{n \times n}$, a norma Frobenius do operador de transição é dada pela \cref{eq:norma}:

\begin{equation}
\label{eq:norma}
\vectornorm{A}_F = \sqrt{\sum_{i=1}^{n} \sum_{j=1}^{n} |a_{ij}|^2}
\end{equation}

\section{Resultados e Tabelas}
A \cref{tab:resultados} resume o desempenho obtido.

\begin{table}[htbp]
  \centering
  \caption{Desempenho de Convergência do Algoritmo}
  \label{tab:resultados}
  \begin{tabular}{@{}llrr@{}}
    \toprule
    \textbf{Grafo} & \textbf{Método} & \textbf{Iterações} & \textbf{Tempo (s)} \\
    \midrule
    Erdős--Rényi & Standard Power Iter & 1.420 & 3,45 \\
    Erdős--Rényi & Accelerated Krylov  & 310   & 0,82 \\
    Barabási--Albert & Accelerated Krylov & 540 & 1,12 \\
    \bottomrule
  \end{tabular}
\end{table}

\printbibliography

\end{document}
```

### Caixa de Destaque Estilizada com `tcolorbox` e Diagrama `TikZ`

```latex
\usepackage[many]{tcolorbox}

% Definindo uma caixa de teorema/aviso elegante
\newtcolorbox{alertbox}[2][]{%
  colback=blue!5!white,
  colframe=blue!75!black,
  fonttitle=\bfseries,
  title=#2,
  arc=2mm,
  #1
}

% Exemplo de Uso:
\begin{alertbox}{Teorema Fundamental de Limite}
Se uma sequência $\{a_n\}$ é limitada e monotônica, então a sequência $\{a_n\}$ é convergente.
\end{alertbox}

% Exemplo de Diagrama TikZ Limpo:
\begin{figure}[htbp]
  \centering
  \begin{tikzpicture}[node distance=2cm, auto, >=stealth']
    \node [draw, circle, fill=blue!10] (A) {Nó A};
    \node [draw, circle, fill=green!10, right of=A, node distance=3cm] (B) {Nó B};
    \node [draw, circle, fill=orange!10, below of=B] (C) {Nó C};

    \draw[->, thick] (A) -- node {$\lambda_{ab}$} (B);
    \draw[->, thick] (B) -- node {$w_{bc}$} (C);
    \draw[->, thick] (C) -| node[near start] {$\mu_{ca}$} (A);
  \end{tikzpicture}
  \caption{Grafo de Transição de Estados}
  \label{fig:tikz_state}
\end{figure}
```

## 🔒 Questões de Segurança e Práticas Seguras

- **Shell Escape (Execução de Código)**: Desabilite a flag `--shell-escape` ao compilar documentos LaTeX contendo código de terceiros não confiáveis, prevenindo chamadas à diretiva `\write18`.
- **Inclusão Arbitrária de Arquivos**: Limite o acesso a diretivas como `\input`, `\include` e `\import` para evitar leitura arbitrária de arquivos confidenciais do sistema host.
- **Negação de Serviço (DoS)**: Evite loops de recursão infinita em definições de macros personalizadas que possam paralisar ou travar a CPU do servidor de compilação.

