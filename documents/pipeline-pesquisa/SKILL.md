---
name: pipeline-pesquisa
description: >
  Use esta skill como ponto de entrada do plugin projeto-pesquisa ou quando o pesquisador
  quiser saber em que etapa do pipeline está, qual skill invocar a seguir, ou retomar o
  trabalho após uma pausa. Acione quando o usuário perguntar "por onde começo?",
  "qual é a próxima etapa?", "quais capítulos já fiz?", "como usar o plugin?",
  "me oriente no pipeline", ou quando não souber qual skill invocar.
  Esta skill não redige nenhum capítulo; apenas orienta e exibe o status do pipeline.
---

# Pipeline Pesquisa — Guia de Orientação do Plugin

Esta skill apresenta o pipeline completo de redação de projetos de pesquisa científica,
verifica o progresso do pesquisador e indica a próxima etapa com as instruções exatas
de invocação.

---

## Fase 1 — Apresentação do pipeline

Ao ser acionada, exibir a tabela abaixo com o pipeline completo:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║        PIPELINE: Redação de Projetos de Pesquisa Científica                ║
║        Plugin: projeto-pesquisa  |  14 skills  |  Sequência obrigatória    ║
╠══╦═══════════════════════════════════════════╦═══════════════════════════════╣
║  ║ Skill                                     ║ Capítulo / Seção              ║
╠══╬═══════════════════════════════════════════╬═══════════════════════════════╣
║ 1║ /research-topic-mapper                    ║ Pré-redação: tema             ║
║ 2║ /pico-research-question                   ║ Pré-redação: pergunta PICO    ║
║ 3║ /plano-intencao                           ║ Pré-redação: plano de intenção║
╠══╬═══════════════════════════════════════════╬═══════════════════════════════╣
║ 4║ /fundamentacao-teorica                    ║ Fundamentação teórica         ║
║ 5║ /introducao-pesquisa                      ║ Capítulo 1 — Introdução       ║
║ 6║ /capitulo-metodos                         ║ Capítulo 2 — Métodos          ║
║ 7║ /etapas-e-cronograma                      ║ Caps. 3, 4 e 5                ║
║ 8║ /capitulo-monitorizacao                   ║ Capítulo 6 — Monitorização    ║
║ 9║ /capitulo-riscos-beneficios               ║ Capítulo 7 — Riscos           ║
║10║ /capitulo-propriedade-responsabilidades   ║ Caps. 8, 9 e 10               ║
║11║ /capitulo-anexos                          ║ Capítulo 11 — Anexos          ║
╠══╬═══════════════════════════════════════════╬═══════════════════════════════╣
║12║ /referencias-bibliograficas               ║ Lista final de referências    ║
║13║ /elementos-pre-textuais                   ║ Capa, sumário, abreviaturas   ║
║14║ /compilacao-final                         ║ Compilação e verificação final║
╚══╩═══════════════════════════════════════════╩═══════════════════════════════╝
```

---

## Fase 2 — Diagnóstico de progresso

Após exibir a tabela, perguntar ao pesquisador:

> "Para indicar sua próxima etapa com precisão, preciso saber o que você já concluiu.
>
> Responda com os números das etapas já realizadas (ex.: 1, 2, 3) ou informe
> 'nenhuma' se está começando agora. Se tiver os arquivos .md salvos, pode listar
> os nomes para eu confirmar."

Aguardar a resposta antes de avançar para a Fase 3.

---

## Fase 3 — Orientação para a próxima etapa

Com base na resposta do pesquisador, identificar a primeira etapa não concluída e
fornecer a orientação abaixo:

### Modelo de orientação (adaptar para a skill correta):

```
PRÓXIMA ETAPA: [número] — /[nome-da-skill]
[Capítulo ou seção correspondente]

Como invocar:
1. Digite /[nome-da-skill] em uma nova mensagem.
2. [Se houver Bloco de Contexto Portátil da etapa anterior]:
   Cole o Bloco de Contexto Portátil gerado ao final da etapa [número anterior].
   Ele contém: [descrever os campos relevantes].
3. [Se for a primeira etapa]:
   Não é necessário nenhum contexto anterior. A skill fará as perguntas necessárias.

O que esta etapa produz:
- Arquivo .md com o texto do capítulo
- Arquivo .docx (Calibri 11pt, margens padrão CEP)
- Arquivo .pdf
- Bloco de Contexto Portátil para a etapa seguinte
```

### Mapa de contexto entre etapas

Ao orientar, usar a tabela abaixo para informar o que passar de uma etapa para a outra:

| Da etapa | Para a etapa | O que passar |
|----------|-------------|--------------|
| 1 research-topic-mapper | 2 pico-research-question | Bloco de Perfil Portátil |
| 2 pico-research-question | 3 plano-intencao | Bloco de Contexto Portátil |
| 3 plano-intencao | 4 fundamentacao-teorica | Bloco de Contexto Portátil |
| 4 fundamentacao-teorica | 5 introducao-pesquisa | Bloco de Contexto Portátil |
| 5 introducao-pesquisa | 6 capitulo-metodos | Bloco de Contexto Portátil |
| 6 capitulo-metodos | 7 etapas-e-cronograma | Bloco de Contexto Portátil |
| 7 etapas-e-cronograma | 8 capitulo-monitorizacao | (retomar a partir dos arquivos .md) |
| 8 capitulo-monitorizacao | 9 capitulo-riscos-beneficios | (retomar a partir dos arquivos .md) |
| 9 capitulo-riscos-beneficios | 10 capitulo-propriedade-responsabilidades | (retomar a partir dos arquivos .md) |
| 10 capitulo-propriedade-responsabilidades | 11 capitulo-anexos | (retomar a partir dos arquivos .md) |
| 11 capitulo-anexos | 12 referencias-bibliograficas | (consolidar todas as referências) |
| 12 referencias-bibliograficas | 13 elementos-pre-textuais | (retomar a partir dos arquivos .md) |
| 13 elementos-pre-textuais | 14 compilacao-final | Caminhos dos 13 arquivos .md |

---

## Fase 4 — Pergunta de encerramento

Ao final da orientação, perguntar:

> "Há algo mais que queira esclarecer antes de começar a próxima etapa?
> Posso detalhar o que a skill `/[próxima-skill]` produz ou como funciona seu fluxo interno."

Se o pesquisador tiver dúvidas, responder com base no conhecimento do pipeline.
Se não tiver, encerrar com:

> "Boa escrita. Quando concluir a etapa, volte aqui e invoque `/pipeline-pesquisa`
> para conferir o próximo passo."

---

## Regras de comportamento

- Esta skill **não redige nenhum conteúdo acadêmico**. Apenas orienta.
- Se o pesquisador pedir para redigir um capítulo dentro desta skill, redirecionar
  para a skill correta: "Para redigir esse capítulo, use `/[skill-correta]`."
- Se o pesquisador não souber em que etapa está e não tiver arquivos salvos,
  recomendar começar pela etapa 1 (`/research-topic-mapper`).
- Nunca pular etapas sem avisar o pesquisador sobre as dependências.
- Se o pesquisador tiver pulado etapas (ex.: fez 1, 2, 3 e 5 sem o 4), alertar:
  > "Atenção: a skill `/introducao-pesquisa` (etapa 5) depende do contexto
  > gerado por `/fundamentacao-teorica` (etapa 4). Recomendo concluir a etapa 4
  > antes de avançar, ou confirmar que possui as informações equivalentes."
