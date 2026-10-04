---
name: compilacao-final
description: >
  Use esta skill como última etapa do pipeline projeto-pesquisa, após /elementos-pre-textuais.
  Lê os arquivos gerados por todas as 13 skills anteriores, verifica coerência de forma,
  conteúdo e estilo entre os capítulos, compila tudo em um único documento integrado e
  entrega três arquivos finais: projeto-completo_[AAAAMMDD].md, .docx e .pdf, prontos para
  submissão ao CEP. Acionar quando o usuário solicitar "compilar o projeto", "documento final",
  "projeto completo", "montar o projeto", "integrar os capítulos", "verificar coerência" ou
  similares.
version: 1.0.0
argument-hint: [cole aqui os caminhos dos arquivos .md gerados pelas skills anteriores, ou informe que deseja colar o conteúdo diretamente]

---

# Compilação Final do Projeto de Pesquisa

## REGRA TIPOGRÁFICA GLOBAL

Nunca utilizar o sinal "—" (travessão) em nenhum texto gerado por esta skill. Substituir
por vírgula quando o travessão funcionar como inciso ou aposto, e por dois-pontos quando
introduzir explicação, enumeração ou conclusão. Esta regra se aplica a todos os outputs
sem exceção, incluindo o relatório de coerência e as mensagens ao usuário.

**Estrangeirismos em itálico:** toda palavra ou expressão em idioma diferente do português
brasileiro deve ser grafada em itálico no texto redigido por esta skill.

---

## Objetivo

Compilar os documentos gerados por todas as 13 skills do pipeline `projeto-pesquisa` em
um único documento integrado, aplicando verificação de coerência entre as partes e
gerando os arquivos finais prontos para submissão ao CEP.

Esta skill realiza quatro operações sequenciais:

1. Recebe os arquivos .md gerados pelas skills anteriores (ou o conteúdo colado diretamente)
2. Verifica coerência de forma, conteúdo e estilo entre todos os capítulos
3. Emite relatório de inconsistências com classificação [CRÍTICO] ou [SUGESTÃO]
4. Compila tudo na ordem canônica e gera os documentos finais (.md, .docx, .pdf)

---

## ◈ BLOCO A — Ativação e coleta dos documentos

### GATE DE EXECUÇÃO OBRIGATÓRIO

Antes de qualquer ação, solicitar ao pesquisador que forneça os documentos gerados pelas
skills anteriores. Apresentar a mensagem abaixo:

> "Para compilar o projeto completo, forneça os documentos gerados pelas skills anteriores.
> Escolha uma das vias:
>
> **Via 1 (recomendada):** informe os caminhos completos dos arquivos .md salvos em
> `C:\Users\[usuário]\`. Exemplo:
>
> ```
> C:\Users\aldem\elementos-pre-textuais.md
> C:\Users\aldem\introducao-pesquisa_20260518.md
> C:\Users\aldem\capitulo-02-metodos_20260518.md
> ```
>
> **Via 2:** cole o conteúdo de cada capítulo diretamente aqui, indicando o nome do
> capítulo antes de cada bloco.
>
> Forneça ao menos dois capítulos para iniciar. A compilação parcial é aceita,
> com capítulos ausentes marcados como [CAPÍTULO PENDENTE]."

Após receber os documentos, ler cada arquivo com a ferramenta Read (Via 1) ou registrar
o conteúdo colado (Via 2). Em seguida, exibir o quadro de status abaixo e aguardar
confirmação explícita antes de prosseguir:

```
╔══════════════════════════════════════════════════════════════════════╗
║            QUADRO DE STATUS — DOCUMENTOS RECEBIDOS                   ║
╠══════════════════════════════════════════════════════════════════════╣
║ 01. Elementos pré-textuais                  ✓ recebido / ✗ pendente ║
║ 02. Introdução (Capítulo 1)                 ✓ recebido / ✗ pendente ║
║ 03. Métodos (Capítulo 2)                    ✓ recebido / ✗ pendente ║
║ 04. Etapas e Cronograma (Capítulo 3)        ✓ recebido / ✗ pendente ║
║ 05. Materiais e Equipamentos (Capítulo 4)   ✓ recebido / ✗ pendente ║
║ 06. Orçamento (Capítulo 5)                  ✓ recebido / ✗ pendente ║
║ 07. Monitorização dos Dados (Capítulo 6)    ✓ recebido / ✗ pendente ║
║ 08. Riscos e Benefícios (Capítulo 7)        ✓ recebido / ✗ pendente ║
║ 09. Propriedade Intelectual (Capítulo 8)    ✓ recebido / ✗ pendente ║
║ 10. Responsabilidades (Capítulo 9)          ✓ recebido / ✗ pendente ║
║ 11. Grupos Vulneráveis (Capítulo 10)        ✓ recebido / ✗ pendente ║
║ 12. Anexos (Capítulo 11)                    ✓ recebido / ✗ pendente ║
║ 13. Referências bibliográficas              ✓ recebido / ✗ pendente ║
╠══════════════════════════════════════════════════════════════════════╣
║ Documentos recebidos : N de 13                                       ║
║ Documentos pendentes : N  [listar quais]                             ║
╚══════════════════════════════════════════════════════════════════════╝
Confirma que estão corretos? Só avançarei para a verificação após confirmação explícita.
```

Aguarde confirmação explícita do usuário antes de prosseguir.

---

## ◈ BLOCO B — Verificação de coerência (três dimensões)

Analisar os documentos recebidos e emitir relatório de inconsistências antes da compilação.
Classificar cada pendência como **[CRÍTICO]** (deve ser corrigido antes da submissão ao CEP)
ou **[SUGESTÃO]** (melhoria recomendada, não obrigatória para submissão).

Após apresentar o relatório, perguntar: "Deseja corrigir as inconsistências antes de
prosseguir ou prefere compilar agora e corrigir depois?" Aguardar resposta antes de avançar.

---

### B.1 — Coerência de conteúdo (verificações semânticas cruzadas)

Cruzar as informações entre capítulos para identificar divergências:

| Verificação | Onde cruzar | Classificação |
|---|---|---|
| Objetivo geral é enunciado de forma idêntica em todos os capítulos que o mencionam | Introdução 1.3 ↔ Métodos seção 1 ↔ Plano de intenção | [CRÍTICO] |
| Hipótese da Introdução (1.2) é compatível com o delineamento declarado nos Métodos | Introdução 1.2 ↔ Métodos seção 1 | [CRÍTICO] |
| População e critérios de elegibilidade nos Métodos (3.1–3.4) são compatíveis com os descritos no TCLE (Anexo 11.1) | Métodos 3.x ↔ Anexo 11.1 | [CRÍTICO] |
| Período de coleta de dados indicado no Cronograma (Cap. 3) é compatível com a duração estimada nos Métodos | Capítulo 3 ↔ Métodos | [CRÍTICO] |
| Variáveis definidas nos Métodos (seção 5) são as mesmas coletadas pelos instrumentos descritos nos Anexos | Métodos 5.x ↔ Anexos 11.3 e 11.4 | [CRÍTICO] |
| Todas as referências citadas nos capítulos constam na lista final de referências bibliográficas | Todos os capítulos ↔ Referências bibliográficas | [CRÍTICO] |
| Título do projeto é idêntico em todos os capítulos onde aparece | Todos os capítulos | [CRÍTICO] |
| Orçamento total no Capítulo 5 é coerente com os materiais listados no Capítulo 4 | Capítulo 4 ↔ Capítulo 5 | [SUGESTÃO] |

---

### B.2 — Coerência de forma (verificações estruturais)

Verificar uniformidade formal em todos os capítulos:

- **Sistema de citação:** `(Autor, ano)` aplicado uniformemente; nenhum capítulo usando
  ABNT numérico, rodapé ou outro formato — **[CRÍTICO]** se divergir
- **Numeração de capítulos e subseções:** consistente ao longo de todo o documento
  (Cap. 1, Cap. 2... sem pular ou repetir números) — **[CRÍTICO]** se inconsistente
- **Ausência de travessões (—):** em todo o texto redigido pelas skills —
  **[SUGESTÃO]** se encontrado
- **Estrangeirismos em itálico:** em todos os capítulos — **[SUGESTÃO]** se ausente
- **Siglas:** definidas na primeira ocorrência nos capítulos e presentes na Lista de
  Abreviaturas (pré-textuais) — **[SUGESTÃO]** se inconsistente

---

### B.3 — Coerência de estilo (verificações linguísticas)

Verificar uniformidade de estilo em todos os capítulos:

- **Tempo verbal:** futuro do indicativo aplicado uniformemente ("será realizado",
  "serão coletados", "o estudo avaliará"); capítulo com texto no presente ou passado do
  indicativo deve ser sinalizado — **[CRÍTICO]** se encontrado
- **Ausência de primeira pessoa:** singular ("Eu realizarei", "verifico") ou plural
  ("realizaremos", "analisamos") — **[CRÍTICO]** se encontrada
- **Terminologia consistente:** o mesmo fenômeno, conceito ou procedimento é denominado
  pelo mesmo termo em todos os capítulos — **[SUGESTÃO]** se inconsistente
- **Registro formal homogêneo:** nenhum capítulo discrepa do padrão acadêmico dos demais
  por uso de linguagem coloquial, informalidades ou estruturas não acadêmicas —
  **[SUGESTÃO]** se encontrado

---

### Formato do relatório de coerência

Exibir na conversa antes de prosseguir para a compilação:

```
╔══════════════════════════════════════════════════════════════════════╗
║                RELATÓRIO DE COERÊNCIA — PENDÊNCIAS                   ║
╠══════════════════════════════════════════════════════════════════════╣
║ Inconsistências críticas  : N                                        ║
║ Sugestões de melhoria     : N                                        ║
╠══════════════════════════════════════════════════════════════════════╣
║ CRÍTICAS                                                             ║
║                                                                      ║
║ [C1] Divergência de objetivo geral                                   ║
║      Localização: Introdução 1.3 ↔ Métodos seção 1                  ║
║      Em Introdução 1.3: "[texto encontrado]"                         ║
║      Em Métodos: "[texto divergente]"                                ║
║      Ação recomendada: uniformizar para o enunciado da Introdução    ║
║                                                                      ║
║ SUGESTÕES                                                            ║
║                                                                      ║
║ [S1] Estrangeirismo sem itálico                                      ║
║      Localização: Capítulo 2, seção 4.2                              ║
║      Observação: o termo "follow-up" aparece sem itálico             ║
╚══════════════════════════════════════════════════════════════════════╝
Deseja corrigir as inconsistências antes de compilar, ou prefere
compilar agora e corrigir depois?
```

Se não houver inconsistências, exibir:

```
╔══════════════════════════════════════════════════════════════════════╗
║           RELATÓRIO DE COERÊNCIA — SEM INCONSISTÊNCIAS              ║
║   Todos os capítulos verificados estão coerentes entre si.           ║
╚══════════════════════════════════════════════════════════════════════╝
Prosseguindo para a compilação do documento integrado.
```

---

## ◈ BLOCO C — Compilação e montagem do documento integrado

Montar o documento na ordem canônica abaixo. Para capítulos pendentes, inserir uma
página com o marcador `[CAPÍTULO PENDENTE — incluir antes da submissão ao CEP]`.

**Ordem canônica do documento final:**

```
── ELEMENTOS PRÉ-TEXTUAIS ────────────────────────────────────────────
   Capa (folha de rosto)
   Informações Gerais (CEP / Plataforma Brasil)
   Sumário  [números de página marcados como [•] — atualizar após montagem final]
   Lista de Abreviaturas, Siglas, Símbolos e Sinais

── CORPO DO PROJETO ──────────────────────────────────────────────────
   Capítulo 1  — Introdução
     1.1. Contexto e Justificativa
     1.2. Hipótese
     1.3. Objetivo
   Capítulo 2  — Métodos
   Capítulo 3  — Etapas da Pesquisa e Cronograma
   Capítulo 4  — Materiais e Equipamentos
   Capítulo 5  — Orçamento
   Capítulo 6  — Monitorização dos Dados e Proteção dos Participantes
   Capítulo 7  — Análise dos Riscos e dos Benefícios
   Capítulo 8  — Propriedade Intelectual
   Capítulo 9  — Responsabilidades dos Pesquisadores
   Capítulo 10 — Participação de Grupos Vulneráveis
   Capítulo 11 — Anexos

── REFERÊNCIAS ───────────────────────────────────────────────────────
   Referências Bibliográficas (estilo Vancouver, ordem alfabética)
```

---

## ◈ BLOCO D — Geração dos arquivos finais

### Dependências — verificar e instalar antes de gerar

```
python-docx  →  pip install python-docx
docx2pdf     →  pip install docx2pdf
```

Fallback para PDF: `reportlab` → pip install reportlab

### Nome base e diretório

**Nome base:** `projeto-completo_[AAAAMMDD]`
**Diretório:** `C:\Users\aldem\`

### Ordem de geração

**1. Salvar `projeto-completo_[AAAAMMDD].md`**

Arquivo Markdown com o documento completo na ordem canônica. Separar cada capítulo com
`---`. Incluir ao final a nota:

`*Documento compilado pela skill /compilacao-final em [DD/MM/AAAA].
Total de capítulos integrados: N de 13. Capítulos pendentes: [lista ou "nenhum"].*`

**2. Gerar `projeto-completo_[AAAAMMDD].docx`** com python-docx:

Especificações de formatação:
- Corpo do texto: Calibri 11pt, espaçamento 1,5, parágrafos justificados
- Título principal (capa): Calibri bold 16pt, centralizado, maiúsculas
- Títulos de capítulo: Calibri bold 14pt, azul `#1F497D`
- Subseções de primeiro nível (ex.: 1.1, 2.1): Calibri bold 12pt
- Subseções de segundo nível (ex.: 1.1.1, 3.1.1): Calibri bold 11pt, itálico
- Margens: 2,5 cm superior e inferior, 3 cm esquerda e direita
- Cabeçalho: título abreviado do projeto (máx. 60 caracteres) à esquerda; número do capítulo atual à direita
- Rodapé: numeração de páginas centralizada, romana (i, ii, iii...) para pré-textuais e arábica (1, 2, 3...) a partir do Capítulo 1
- Quebra de página antes de cada capítulo
- Referências: Calibri 10pt, espaçamento simples, recuo pendente 0,5 cm

**3. Converter `projeto-completo_[AAAAMMDD].docx` para `projeto-completo_[AAAAMMDD].pdf`**
com docx2pdf; se falhar, usar reportlab.

**4. Salvar `relatorio-coerencia_[AAAAMMDD].md`**

Arquivo contendo o relatório de coerência completo gerado no Bloco B, com data e
totais de inconsistências. Se não houver inconsistências, registrar:
`Nenhuma inconsistência identificada. Todos os capítulos estão coerentes.`

**5. Remover scripts Python temporários gerados durante o processo**

**6. Confirmar ao pesquisador os quatro caminhos completos dos arquivos gerados**

---

## ◈ BLOCO E — Checklist de qualidade (aplicar antes de entregar os arquivos)

### Estrutura e integridade

- [ ] Todos os capítulos integrados (ou capítulos pendentes marcados com [CAPÍTULO PENDENTE])
- [ ] Ordem canônica respeitada: pré-textuais → capítulos 1–11 → referências
- [ ] Quebra de página antes de cada capítulo no .docx
- [ ] Paginação: romana nos pré-textuais (i, ii, iii...), arábica a partir do Capítulo 1 (1, 2, 3...)
- [ ] Nota de compilação presente ao final do .md

### Coerência de conteúdo

- [ ] Objetivo geral idêntico em todos os capítulos onde é enunciado
- [ ] Hipótese compatível com o delineamento declarado nos Métodos
- [ ] População nos Métodos compatível com a população descrita no TCLE (Anexo 11.1)
- [ ] Período de coleta no Cronograma compatível com a duração estimada nos Métodos
- [ ] Todas as referências citadas nos capítulos constam na lista final de referências
- [ ] Título do projeto idêntico em todos os capítulos

### Coerência de forma

- [ ] Sistema de citação `(Autor, ano)` uniforme em todos os capítulos
- [ ] Ausência de travessões em todo o documento compilado
- [ ] Estrangeirismos grafados em itálico em todos os capítulos
- [ ] Numeração de capítulos e subseções consistente ao longo do documento

### Coerência de estilo

- [ ] Futuro do indicativo uniforme em todos os capítulos
- [ ] Ausência de primeira pessoa do singular ou plural em todo o documento
- [ ] Terminologia consistente para os conceitos centrais do projeto

### Arquivos

- [ ] .md gerado sem truncamento ou perda de conteúdo
- [ ] .docx com formatação correta: fonte, margens, cabeçalho, rodapé e quebras de página
- [ ] .pdf gerado com cabeçalho, rodapé e numeração de páginas; caminho confirmado ao usuário
- [ ] Relatório de coerência gerado e salvo como arquivo .md; caminho confirmado ao usuário

---

## ◈ MENSAGEM DE ENCERRAMENTO

```
PROJETO COMPLETO COMPILADO.

  Total de capítulos integrados : N de 13
  Capítulos pendentes           : [lista ou "nenhum"]
  Inconsistências críticas      : N  (detalhes no relatório de coerência)
  Sugestões de melhoria         : N  (detalhes no relatório de coerência)

Arquivos gerados:
  MD        ->  C:\Users\aldem\projeto-completo_[AAAAMMDD].md
  DOCX      ->  C:\Users\aldem\projeto-completo_[AAAAMMDD].docx
  PDF       ->  C:\Users\aldem\projeto-completo_[AAAAMMDD].pdf
  Relatório ->  C:\Users\aldem\relatorio-coerencia_[AAAAMMDD].md

Antes da submissão ao CEP, verifique:
  1. Revise e corrija as inconsistências críticas listadas no relatório de coerência.
  2. Complete todos os campos marcados como [a preencher] ou [PREENCHER].
  3. Imprima os Anexos 11.6, 11.7, 11.8, 11.9 e 11.10 em papel timbrado da
     instituição e assine à tinta antes da submissão.
  4. Insira a logomarca da instituição na capa (campo [LOGOMARCA]).
  5. Atualize os números de página marcados como [•] no Sumário após a
     revisão e montagem final no editor de texto.
```

Este é o último passo do pipeline `projeto-pesquisa`. O documento compilado está
pronto para revisão final e submissão ao CEP.


---

## SINALIZAÇÃO DE CONCLUSÃO

Quando todos os entregáveis desta etapa estiverem gerados e a etapa estiver
completa — e somente então —, adicione a seguinte linha como **última linha** da resposta:

=== ETAPA CONCLUÍDA ===

**Regras:**
- Emita o marcador **apenas uma vez**, na última resposta da etapa.
- **Não emita** em respostas intermediárias, enquanto aguardar dados do usuário,
  ou antes de todos os documentos/seções solicitados estarem prontos.
- Se o usuário pedir ajustes após a sinalização, **não** emita o marcador novamente
  nas respostas de ajuste.
