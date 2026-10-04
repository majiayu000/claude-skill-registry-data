---
name: geracao-perfis-psicologicos-e-roleplay
description: Extrai perfis psicologicos de personagens e configura LLM local para entrevistas in-character sem drift de persona.
---
# geracao-perfis-psicologicos-e-roleplay

## Descrição
A skill `geracao-perfis-psicologicos-e-roleplay` extrai perfis psicológicos estruturados (fichas) de personagens a partir de suas ações descritas no manuscrito e configura agentes de linguagem locais para encenar o personagem em entrevistas interativas (chatbot in-character). Ela permite ao autor debater ideias, testar a consistência das falas e explorar o subtexto dramático conversando diretamente com a persona do personagem criado.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor solicita a criação de uma nova ficha de personagem ou clica em "Atualizar Ficha por NLP".
- O autor ativa o painel de "Chat de Entrevista de Personagem" na interface lateral do editor.
- O sistema precisa auditar se uma cena em digitação respeita as características psicológicas cadastradas do personagem (consistência comportamental).

Quando NÃO usar:
- Para responder a perguntas factuais da wiki sobre o mundo (usar a skill `recuperacao-conhecimento-qfs-narrativo`).
- Em brainstorms de ideias soltas sem definição de personagens específicos.

## Pré-requisitos
- Modelo de linguagem local de alta capacidade instrucional (ex: Qwen-2.5-7B ou Llama-3-8B quantizado).
- Snapshots do Grafo Temporal de Entidades (GTE) contendo o histórico de ações do personagem.
- Ficha de personagem base (Markdown/JSON) com campos de Metas e Medos.

## Processo (passo a passo executável)
1. **Extração de Papéis de Ação (Agent/Patient Classification):**
   - Varrer o grafo de eventos narrativos extraído do livro.
   - Classificar as aparições do personagem em:
     - `Agent` (quando o personagem executa a ação ativa, ex: confrontar, construir, ferir).
     - `Patient` (quando o personagem sofre a ação passiva, ex: ser atacado, receber doação).
2. **Derivação de Traços de Personalidade:**
   - Analisar a proporção das categorias de ação no histórico do personagem.
   - Atribuir classificações de traços sob o modelo Big Five (OCEAN) ou perfis arquétipos:
     - Alta taxa de ações agressivas/combate $\rightarrow$ Perfil: *Confrontador / Assertivo*.
     - Alta taxa de ações de diálogo conspiratório/mentira $\rightarrow$ Perfil: *Cauteloso / Manipulador*.
3. **Compilação da Ficha de Personagem (Markdown):**
   - Alimentar os dados estruturados no arquivo da wiki do personagem contendo a descrição de seus traços derivados, sua rede social ativa, seu arco de valência atual e suas metas pendentes.
4. **Prompting do Chatbot In-Character (ArcANE):**
   - Montar o prompt de sistema do LLM local contendo:
     - Biografia, idade, traços psicológicos e vocabulário estilístico do personagem.
     - Histórico de eventos importantes sofridos pelo personagem até a cena ativa.
     - Instrução estrita de encenação (ex: *"Responda às perguntas do autor fingindo ser o personagem [Nome]. Fale em primeira pessoa. Respeite as informações contidas na sua ficha e no seu histórico. Não mencione que você é um modelo de IA."*)
5. **Orquestração da Conversação:**
   - Iniciar o chat interativo na UI. A cada turno de resposta, injetar no contexto da janela a cena e as restrições mais recentes do GTE para evitar desvios lógicos.

## Parâmetros e configuração
- `MAX_ROLEPLAY_CONTEXT_TOKENS`: Limite máximo de tokens de contexto da conversa para evitar perda de foco de persona. Padrão: `4096`.
- `PERSONA_CREATIVITY_TEMP`: Temperatura do LLM configurada para o chatbot de persona (um valor menor evita alucinações de fatos). Padrão: `0.70`.
- `MIN_ACTION_SAMPLES`: Quantidade mínima de eventos necessários no histórico para disparar a derivação automática de traços. Padrão: `10`.

## Armadilhas e como evitá-las
- **Armadilha:** Drift de Persona e Fatos: o chatbot simulador de personagem começa a alucinar e inventar fatos ou parentescos que não existem na história original do romance, rompendo a consistência do livro.
  **Mitigação:** Bloquear a geração livre sem ancoragem. Injetar no prompt do chatbot um filtro de contexto estrito contendo os nós vizinhos do personagem no Grafo Temporal de Entidades. O System Prompt deve conter a instrução de rejeição: *"Se o autor perguntar algo sobre o seu passado que não esteja listado na sua biografia ou histórico fornecidos, responda que você não se lembra ou desvie do assunto mantendo a sua persona."* (ArcANE, 2026).

## Critérios de validação (Definition of Done)
- [ ] A ficha gerada e os traços psicológicos derivados de forma autônoma atingem no mínimo 90% de acurácia factual sob auditoria manual de amostragem.
- [ ] O chatbot in-character não cita que é uma inteligência artificial em 100% dos testes de regressão de diálogo e recusa-se a inventar fatos não-ancorados.

## Fundamentação científica
- MARCUS (2022) - Event-Centric NLP Pipeline for Character Arcs - arXiv 2022
- ArcANE Benchmark (2026) - Do Role-Playing Language Agents Stay in Character? - arXiv 2026
- AustenAlike Benchmark (2024) - Evaluating Computational Representations of Character - arXiv 2024

## Requisitos do projeto relacionados
- RF-166 (biografias)
- RF-167 (ficha estruturada)
- RF-168 (chatbot interativo)

## Maturidade e riscos de adoção
**Nível:** Emergente/Experimental.
*Risco: Manter a persona de forma estável por longas conversas sem sofrer desvios estilísticos ou alucinações é um desafio em aberto em LLMs de 7B locais.*
*Fallback para v1:* O chatbot atua apenas como gerador de fichas passivo em markdown. Desativar a entrevista de chat in-character interativa baseada em grafos temporais dinâmicos na v1 se o modelo de 7B local apresentar falhas constantes de drift.

## Exemplos
**Entrada (Prompt de Entrevista):**
```text
[Autor]: "Kael, por que você odeia o feiticeiro Érebo?"
[Snapshot da Ficha]: { "Nome": "Kael", "Inimigo": "Érebo", "Motivo": "Érebo assassinou o mentor de Kael" }
```
**Saída esperada (Resposta do Chatbot):**
```text
"Aquele desgraçado tirou a única pessoa que acreditou em mim. O Érebo vai pagar por cada gota de sangue do meu mestre."
```
**Caso de falha conhecido:**
O chatbot responder: "Eu odeio o Érebo porque ele roubou minha nave espacial" (em um romance medieval de fantasia pura, sofrendo de drift de contexto do modelo).
