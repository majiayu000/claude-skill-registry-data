---
name: "lang-typst"
description: "Fornece padrões de engenharia e tipografia digital moderna usando Typst. Cobre sintaxe de marcação, funções customizadas, criação de templates reutilizáveis, regras de exibição (show/set rules), matemática avançada, tabelas, layout de páginas e bibliografia via Hayagriva/BibTeX."
---

# Habilidade de IA: Engenharia de Typst (Typst Specialist)

Esta skill orienta a inteligência artificial a atuar como especialista na linguagem e sistema de diagramação **Typst**, focando na criação de documentos acadêmicos, relatórios técnicos, apresentações e artigos de alta qualidade tipográfica com sintaxe limpa, código expressivo e alto desempenho de compilação.

---

## 🧭 Diretrizes de Desenvolvimento em Typst

Ao atuar nesta skill, aplique rigorosamente os seguintes padrões:

### 1. Configuração de Layout e Regras `set` e `show`
- **Separação de Conteúdo e Estilo**: Defina as regras de estilo globais usando instruções `#set` no início do documento ou dentro de um template.
- **Transformação de Seletores (`show`)**: Utilize regras `#show` para customizar a aparência de elementos específicos (como títulos, links, blocos de código ou tabelas) de forma declarativa.
- **Configuração Inicial de Página**:
  ```typst
  #set page(
    paper: "a4",
    margin: (x: 2cm, top: 2.5cm, bottom: 2.5cm),
    header: align(right)[_Relatório Técnico_],
    footer: [
      #align(center)[#counter(page).display("1 / 1", both: true)]
    ]
  )
  #set text(font: "Liberation Serif", size: 11pt, lang: "pt")
  ```

### 2. Modos de Operação (Text, Math e Code)
- **Modo Texto**: Escrita natural com sintaxe leve (`*negrito*`, `_itálico_`, `= Título`).
- **Modo Matemática (`$`)**: Utilize blocos inline `$ x^2 $` ou blocos em destaque `$ sum_(i=1)^n i = (n(n+1))/2 $`.
- **Modo Código (`#`)**: Todo comando ou lógica em Typst começa com `#`. Bloco de código em múltiplas linhas utiliza `#{ ... }`.

### 3. Funções e Modularidade
- **Templates Reutilizáveis**: Exporte uma função principal de template que recebe parâmetros estruturados (título, autores, resumo, corpo) e aplica as regras de layout via `#show: doc => template(doc)`.
- **Parâmetros com Nome**: Dê preferência a parâmetros nomeados com valores padrão razoáveis nas funções customizadas.

### 4. Tabelas, Figuras e Layout Idiomático
- **Tabelas com `table`**: Utilize a nova API de tabela com `table.header` e alinhamento explicito por coluna:
  ```typst
  #table(
    columns: (1fr, 2fr, 1fr),
    align: (left, left, center),
    stroke: 0.5pt + luma(150),
    table.header([*ID*], [*Descrição*], [*Status*]),
    [01], [Atualização de firmware], [OK],
    [02], [Verificação de integridade], [Pendente]
  )
  ```
- **Quadros e Notificações (Callouts)**: Crie blocos visuais estilizados usando `block` com bordas arredondadas e preenchimento sutil.

### 5. Gestão de Bibliografia e Pacotes
- **Bibliografias Nativas**: Use `#bibliography("works.bib", style: "ieee")` para integração transparente com arquivos `.bib` ou `.yml` (Hayagriva).
- **Pacotes do Typst Universe**: Importe pacotes oficiais com a sintaxe `#import "@preview/pacote:versao"`.

---

## 🧰 Padrões de Código Recomendados

### Template Profissional de Relatório / Artigo Técnico

```typst
// template.typst
#let project(
  title: "",
  authors: (),
  abstract: none,
  logo: none,
  body
) = {
  // Configuração global de página
  set page(
    paper: "a4",
    margin: (x: 2.5cm, y: 3cm),
    numbering: "1",
  )
  
  // Configuração de tipografia
  set text(font: "DejaVu Serif", size: 11pt, lang: "pt", region: "BR")
  set par(justify: true, leading: 0.65em)
  set heading(numbering: "1.1")

  // Personalização visual dos títulos
  show heading: it => [
    #v(0.5em)
    #text(fill: rgb("#1a365d"), weight: "bold")[#it]
    #v(0.3em)
  ]

  // Cabeçalho / Capa resumida
  align(center)[
    #if logo != none {
      image(logo, width: 25%)
      v(1em)
    }
    #text(size: 20pt, weight: "bold", fill: rgb("#1a365d"))[#title]
    #v(1em)
    #grid(
      columns: (1fr,) * calc.min(authors.len(), 3),
      gutter: 1em,
      ..authors.map(author => align(center)[
        #text(weight: "medium")[#author.name] \
        #text(size: 9pt, fill: luma(100))[#author.email]
      ])
    )
    #v(1.5em)
  ]

  // Resumo (se houver)
  if abstract != none {
    rect(
      width: 100%,
      fill: rgb("#f7fafc"),
      inset: 12pt,
      radius: 4pt,
      stroke: 0.5pt + rgb("#e2e8f0")
    )[
      #text(weight: "bold", fill: rgb("#2d3748"))[Resumo] \
      #v(0.3em)
      #abstract
    ]
    #v(1.5em)
  }

  // Corpo do Documento
  body
}
```

### Exemplo de Uso do Template com Blocos e Matemática

```typst
#import "template.typst": project

#show: doc => project(
  title: "Análise de Desempenho de Algoritmos Distribuídos",
  authors: (
    (name: "Dandara Gabriel", email: "dandara@example.com"),
    (name: "Alex Silva", email: "alex@example.com")
  ),
  abstract: [
    Este documento apresenta uma avaliação comparativa de throughput e latência entre arquiteturas de mensageria assíncrona operando sob alta carga.
  ],
  doc
)

= Introdução

A escalabilidade de sistemas distribuídos modernos depende diretamente do padrão de comunicação adotado entre os nós receptores e emissores.

#let callout(title: "Nota", body, color: blue) = {
  block(
    fill: color.lighten(90%),
    stroke: (left: 4pt + color),
    inset: 10pt,
    radius: (right: 4pt),
    width: 100%,
    [
      #text(weight: "bold", fill: color.darken(20%))[#title] \
      #body
    ]
  )
}

#callout(title: "Importante", color: rgb("#2b6cb0"))[
  Certifique-se de que os nós do cluster estejam sincronizados via protocolo NTP antes de iniciar os testes de carga.
]

= Formulacão Matemática

O tempo médio de resposta $T(n)$ para um sistema de fila com $n$ requisições concorrentes é modelado pela equação:

$ T(n) = sum_(k=1)^n (lambda_k / (mu_k - lambda_k)) + float("overhead") $

Onde $lambda_k$ representa a taxa de chegada e $mu_k$ a taxa de serviço do canal $k$.

= Resultados Experimentais

#figure(
  table(
    columns: (1fr, 1.5fr, 1fr),
    align: (center, left, right),
    stroke: 0.5pt + luma(180),
    table.header([*Métrica*], [*Algoritmo*], [*Valor Médio*]),
    [Throughput], [Event-Driven Reactive], [45.200 req/s],
    [Latência p99], [Event-Driven Reactive], [1.2 ms],
    [Throughput], [Blocking I/O Standard], [12.800 req/s],
  ),
  caption: [Comparativo de Desempenho entre Arquiteturas]
)
```

## 🔒 Questões de Segurança e Práticas Seguras

- **Sandbox Escaping**: Configure o compilador do Typst no modo restrito (sandbox ativo) para prevenir operações arbitrárias de leitura de arquivos locais ou caminhos de rede não autorizados.
- **Negação de Serviço (DoS)**: Otimize laços, funções recursivas e regras de formatação dinâmica para evitar que scripts maliciosos induzam recursão infinita e consumam toda a CPU do servidor.

