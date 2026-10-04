---
name: destilacao-espinha-dorsal-narrativa
description: Extrai componentes dramaticos fundamentais para gerar loglines e sinopses comerciais impactantes automaticamente.
---
# destilacao-espinha-dorsal-narrativa

## Descrição
A skill `destilacao-espinha-dorsal-narrativa` extrai os componentes dramáticos estruturais fundamentais de uma história para gerar automaticamente sinopses comerciais e loglines (resumos conceituais de uma única sentença) de alto impacto. Ela analisa a progressão do conflito principal do romance, descartando elementos secundários de lore e personagens menores para produzir textos de apresentação comercial e pitch.

## Quando usar
Gatilhos concretos e observáveis:
- O autor solicita a geração de uma logline ou sinopse comercial no painel de metadados da obra.
- O sistema prepara pacotes de exportação da obra para agências literárias ou editoras (metadados de publicação).
- O escritor solicita um resumo de progresso dramático na aba de planejamento de metas.

Quando NÃO usar:
- Para gerar resumos detalhados de capítulos para acompanhamento de escrita (nesse caso, usar a skill `sumarizacao-hierarquica-recursiva`).
- Em universos de contos ou antologias de múltiplas histórias independentes (deve focar em um único arco de espinha dorsal).

## Pré-requisitos
- O resumo global L3 do livro gerado pela skill `sumarizacao-hierarquica-recursiva`.
- Ficha do protagonista cadastrada no banco de dados do romance.
- Acesso ao modelo de linguagem local (SLM) configurado para tarefas de escrita comercial.

## Processo (passo a passo executável)
1. **Extração dos Elementos da Espinha Dorsal (Story Spine Extraction):**
   - Executar o SLM local sobre a sinopse L3 e notas estruturais para extrair em formato JSON os seguintes atributos:
     - `Protagonista`: Nome e motivação interna básica do herói.
     - `Incidente_Incitador`: O evento que tira o protagonista de sua rotina normal e inicia a ação do romance.
     - `Desejo_Central`: A meta imediata que o protagonista quer alcançar.
     - `Obstaculo_Principal`: O antagonista ou barreira física/moral que impede a conclusão.
     - `Consequencia`: O que de terrível acontecerá se o protagonista falhar (estaca/risk factor).
2. **Geração da Logline Estruturada (Template-driven):**
   - Alimentar os dados extraídos no passo 1 em um dos três templates de loglines consolidados de mercado:
     - *Template 1 (Clássico):* "Quando [incidente incitador] acontece, um [protagonista] com o objetivo de [desejo central] deve enfrentar [obstáculo principal], sob o risco de [consequência]."
     - *Template 2 (Antagonista):* "Um [protagonista] busca [desejo central], mas enfrenta a oposição de [obstáculo principal] após [incidente incitador]."
   - Deixar o SLM refinar a fluidez linguística da frase mantendo as variáveis intactas.
3. **Geração de Sinopse Comercial (Plot-guided):**
   - Gerar um resumo de 3 parágrafos focando estritamente na progressão da espinha dorsal:
     - *Parágrafo 1:* Apresentação do herói, mundo inicial e incidente incitador.
     - *Parágrafo 2:* O conflito principal em andamento e os obstáculos.
     - *Parágrafo 3:* O clímax iminente e a estaca de risco (consequência), sem revelar o final/spoiler da obra.

## Parâmetros e configuração
- `MAX_LOGLINE_WORDS`: Limite máximo de palavras para a logline gerada. Padrão: `35`.
- `SYNOPSIS_FORMAT`: Estrutura de saída da sinopse comercial. Padrão: `"3-paragraphs"`.
- `LOGLINE_TEMPLATE_DEFAULT`: Índice do template de logline padrão a ser usado. Padrão: `1`.

## Armadilhas e como evitá-las
- **Armadilha:** Sobrecarga de Subtramas e Nomes: incluir subtramas românticas secundárias, nomes de dezenas de locais fictícios ou múltiplos personagens secundários na logline, tornando-a confusa e sem foco mercadológico.
  **Mitigação:** Proibir explicitamente a menção de qualquer nome próprio na logline que não seja o do protagonista e do antagonista principal. Filtrar e remover da logline termos de worldbuilding complexos (ex: nomes de raças inventadas, magias secundárias ou continentes), substituindo por termos genéricos compreensíveis (ex: "um reino distante", "uma força sombria").

## Critérios de validação (Definition of Done)
- [ ] A logline gerada possui no máximo 35 palavras e contém obrigatoriamente o protagonista, o obstáculo principal e a consequência de falha.
- [ ] A taxa de consistência factual dos elementos dramáticos extraídos em relação ao manuscrito é de no mínimo 90% sob auditoria manual de amostragem.

## Fundamentação científica
- S2tory (2026) - Story Spine Distillation for Movie Script Summarization - arXiv 2026
- Plan-Guided Summarization (2025) - Plan-Guided Summarization for Narrative Texts (SLMs) - arXiv 2025

## Requisitos do projeto relacionados
- RF-170 (gerar sinopse)
- RF-171 (gerar logline)

## Maturidade e riscos de adoção
**Nível:** Emergente.
*Risco: O modelo local pode alucinar ou confundir incidentes incitadores secundários de capítulos com o verdadeiro incidente incitador global do romance.*
*Fallback para v1:* Apresentar um formulário estruturado de 5 campos ("Quem é o protagonista?", "Qual o incidente incitador?", etc.) para o autor preencher manualmente, e usar lógica de concatenação baseada nos templates estáticos de logline, desativando a extração autônoma via NLP.

## Exemplos
**Entrada (Story Spine JSON extraído):**
```json
{
  "Protagonista": "o jovem ferreiro Kael",
  "Incidente_Incitador": "o assassinato de seu mentor pelo feiticeiro Érebo",
  "Desejo_Central": "destruir a Ordem das Sombras",
  "Obstaculo_Principal": "o exército de mortos-vivos",
  "Consequencia": "a escuridão eterna do reino de Solaria"
}
```
**Saída esperada (Logline):**
```text
Quando seu mentor é assassinado pelo feiticeiro Érebo, o jovem ferreiro Kael deve destruir a Ordem das Sombras enfrentando um exército de mortos-vivos, sob o risco de condenar seu reino à escuridão eterna.
```
**Caso de falha conhecido:**
Gerar uma logline prolixa contendo detalhes de como o ferro é forjado e mencionando 4 amigos do herói.
