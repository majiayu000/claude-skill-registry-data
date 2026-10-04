---
name: "lang-markdown"
description: "Fornece diretrizes completas de autorização, engenharia e formatação em Markdown (CommonMark, GitHub Flavored Markdown - GFM e MDX). Cobre estruturação hierárquica de documentos, formatação avançada de código e tabelas, elementos visuais (alertas GFM, diagramas Mermaid), equações matemáticas em LaTeX, padrões de linting (MarkdownLint), documentação técnica (READMEs, ADRs, Changelogs) e integração com JSX/MDX."
---

# Habilidade de IA: Engenharia e Formatação de Markdown (Markdown Specialist)

Esta skill orienta a inteligência artificial a atuar como especialista em **Markdown**, abrangendo especificações **CommonMark**, **GitHub Flavored Markdown (GFM)** e extensões modernas como **MDX**. Ela garante a criação de documentações técnicas, manuais, guias, guias de APIs, registros de decisões de arquitetura (ADRs) e arquivos README visualmente atraentes, legíveis, semânticos e totalmente aderentes aos padrões de linting.

---

## 🎯 Objetivo da Skill

Capacitar o assistente de IA a produzir documentos em Markdown com excelência técnica, semântica e estética, evitando erros comuns de sintaxe, garantindo compatibilidade entre diferentes parsers e aplicando as melhores práticas de marcação técnica.

---

## 🛠️ Diretrizes e Padrões de Formatação

Ao redigir ou refatorar documentos em Markdown, aplique rigidamente as regras descritas a seguir:

### 1. Hierarquia e Estrutura Semântica
- **Título Único Nível 1 (`#`)**: Todo documento isolado deve conter apenas um título principal de nível 1 (`#`).
- **Nivelamento Progressivo**: Nunca pule níveis de cabeçalho (ex: passar de `##` diretamente para `####`).
- **Espaçamento de Cabeçalhos**: Mantenha sempre uma linha em branco antes e depois de cada linha de cabeçalho.
- **Capitalização**: Mantenha padrão consistente (ex: Title Case ou Sentence case) em toda a árvore de cabeçalhos.

### 2. Sintaxe GFM (GitHub Flavored Markdown) Avançada
- **Alertas / Callouts Nativo do GFM**: Utilize a sintaxe oficial de blockquotes com tipo para destacar informações cruciais:
  ```markdown
  > [!NOTE]
  > Informações contextuais e explicações úteis.

  > [!TIP]
  > Dicas de otimização, boas práticas e sugestões.

  > [!IMPORTANT]
  > Requisitos essenciais e avisos indispensáveis.

  > [!WARNING]
  > Alterações que podem quebrar funcionalidade ou avisos de atenção.

  > [!CAUTION]
  > Riscos elevados de perda de dados ou ações destrutivas.
  ```

- **Tabelas Alinhadas e Formatadas**:
  - Sempre inclua a linha separadora com especificação de alinhamento (`:---` para esquerda, `:---:` para centro, `---:` para direita).
  - Mantenha espaçamento visual uniforme nas colunas usando pipes `|` alinhados para facilitar a leitura no código-fonte em texto puro.
  ```markdown
  | Recurso | Suportado | Complexidade | Observação |
  | :--- | :---: | ---: | :--- |
  | CommonMark | Sim | Baixa | Padrão base |
  | GFM | Sim | Média | Suporta tabelas e alertas |
  | MDX | Sim | Alta | Componentes React |
  ```

- **Listas de Tarefas (Task Lists)**:
  - Utilize `- [ ]` para itens pendentes e `- [x]` para concluídos. Mantenha espaço de 1 caractere entre os parênteses.

- **Notas de Rodapé (Footnotes)**:
  - Declare a nota no corpo do texto via `[^1]` ou `[^chave]` e descreva no final do arquivo: `[^1]: Explicação detalhada da nota.`.

- **Tachado e Destaques**:
  - Texto tachado: `~~texto removido~~`.

---

### 3. Blocos de Código e Diffs
- **Blocos Cercados (Fenced Code Blocks)**: Sempre declare o identificador de linguagem explicitamente nas três crases (```json, ```typescript, ```bash, etc.).
- **Blocos de Diff**: Para demonstrar alterações em código, utilize a linguagem `diff`:
  ```diff
  - const antigo = "obsoleto";
  + const novo = "atualizado";
  ```
- **Escapando Crases**: Para exibir blocos de código dentro de blocos de instrução em Markdown, use delimitação com quatro crases (````).

---

### 4. Diagramas Visualizáveis e Matemática
- **Diagramas Mermaid**: Integre fluxogramas, diagramas de sequência, gráficos e mapas mentais utilizando o identificador `mermaid`:
  ```mermaid
  flowchart LR
      A[Entrada Markdown] --> B[Parser GFM / MDX]
      B --> C[Renderização HTML/UI]
  ```
- **Equações Matemáticas (KaTeX / MathJax)**:
  - Inline: `$E = mc^2$`
  - Bloco em linha própria:
    ```markdown
    $$
    \hat{f}(\xi) = \int_{-\infty}^{\infty} f(x) e^{-2\pi i x \xi} dx
    $$
    ```

---

### 5. Cabeçalhos de Metadados (Frontmatter) e MDX
- **YAML Frontmatter**: Posicione no topo do arquivo delimitado por `---`:
  ```yaml
  ---
  title: "Guia Completo de Markdown"
  description: "Manual de referência rápida e avançada para marcação em Markdown."
  author: "Equipe de Engenharia"
  date: "2026-08-06"
  tags: ["markdown", "gfm", "mdx", "docs"]
  ---
  ```
- **Sintaxe MDX (React em Markdown)**:
  - Permite importar e utilizar componentes JSX dentro do arquivo Markdown:
  ```mdx
  import { Button, Alert } from '@/components/ui';

  <Alert type="success">
    Componente React renderizado via MDX!
  </Alert>

  <Button onClick={() => alert("Clicado!")}>Ação</Button>
  ```

---

### 6. Padrões de Qualidade e Prevenção de Erros (MarkdownLint)
- **Quebras de Linha**: Prefira `<br>` explícito quando precisar de quebra de linha forçada, evitando o uso de dois espaços em branco ao fim da linha (invisíveis e fáceis de apagar acidentalmente).
- **Linha Final**: Garanta sempre que o arquivo encerre com exatamente uma linha em branco em seu final (regra MD047).
- **URLs Brutas**: Em vez de colar URLs soltas (`https://example.com`), envolva-as em marcadores (`<https://example.com>`) ou crie links semânticos (`[Nome do Link](https://example.com)`).
- **Textos de Alt em Imagens**: Toda imagem deve obrigatoriamente possuir um texto alternativo descritivo: `![Texto alternativo descritivo](https://example.com/imagem.png)`.

---

## 📚 Estrutura da Skill

- [SKILL.md](SKILL.md): Guias centrais e especificações de engenharia em Markdown.
- **`scripts/`**: Scripts executáveis de automação e validação de Markdown.
- **`examples/`**: Modelos e templates padrão (README técnico, ADR, Changelog).
- **`resources/`**: Recursos auxiliares e paletas de ícones/badges.
- **`references/`**: Documentações de referência das especificações CommonMark, GFM e MarkdownLint.

## 🔒 Questões de Segurança e Práticas Seguras

- **Cross-Site Scripting (XSS)**: Sempre sanitize ou desabilite a renderização de tags HTML brutas dentro do Markdown quando o HTML final for exibido em navegadores web.
- **Injeção de Links**: Use validadores para links e caminhos gerados pelo usuário, garantindo o bloqueio de esquemas perigosos como `javascript:` ou `data:`.
- **Validação de Imagens e Media**: Redirecione URLs de imagens externas através de proxies de imagens (Image Proxy) para evitar vazamento de IPs de usuários finais.

