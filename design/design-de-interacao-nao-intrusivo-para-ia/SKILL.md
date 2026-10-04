---
name: design-de-interacao-nao-intrusivo-para-ia
description: Especifica politicas de UX para assistentes de IA que preservam o flow criativo e a sensacao de propriedade autoral do manuscrito.
---
# design-de-interacao-nao-intrusivo-para-ia

## Descrição
A skill `design-de-interacao-nao-intrusivo-para-ia` especifica os padrões de interface do usuário (UX/UI) para assistentes de escrita baseados em IA generativa. Ela estabelece as políticas de exibição, gatilhos de ativação e comportamento de descarte de sugestões de conteúdo que preservam o estado de flow criativo do escritor, garantindo que o romancista mantenha sempre a sensação de posse (ownership) do manuscrito.

## Quando usar
Gatilhos concretos e observáveis:
- O sistema precisa exibir qualquer resultado de assistência de IA no editor de texto (autocompletes, ganchos, nomes, tropos).
- O autor ativa um painel de brainstorming interativo.
- A equipe de engenharia de frontend implementa novos módulos de interação de co-piloto no editor.

Quando NÃO usar:
- Em modais de gerenciamento de conta, licenças ou exportações de arquivo (contextos administrativos sem conteúdo de IA).
- Para exibir alertas críticos de segurança ou erros de sincronização do banco de dados.

## Pré-requisitos
- Sistema de sugestões de IA local operacional.
- Componente de sidebar responsiva implementado no framework frontend do editor.
- Mecanismo de rastreamento de interações do usuário (aceite/rejeição de sugestões).

## Processo (passo a passo executável)
1. **Sidebar Passiva como Padrão:**
   - Configurar o painel de sugestões de IA como uma sidebar lateral que atualiza silenciosamente sem animações, sons ou notificações no final de parágrafos e sem interromper o fluxo de digitação.
   - A sidebar deve ter baixa saliência visual quando inativa (opacidade reduzida a `0.6`), tornando-se totalmente visível (`1.0`) apenas ao ser focalizada com o mouse ou teclado.
2. **Gatilhos de Modo Ativo Explícito (Opt-in):**
   - Sugestões flutuantes ou pop-ups próximos ao cursor de digitação só devem aparecer mediante ativação explícita por gatilhos criados e compreendidos pelo escritor:
     - Gatilho Textual: O autor digita tokens especiais reservados (ex: `[nome?]`, `[gancho?]`, `[ref?]`).
     - Atalho Explícito: `Ctrl+Space` ativa o sugestor inline.
   - Pop-ups devem ter tempo máximo de exibição de `6` segundos sem interação, desaparecendo com transição suave.
3. **Fechamento Automático sob Atividade:**
   - Ao detectar que o autor começou a digitar novamente após a exibição de um sugestor inline, fechar e descartar o balão de sugestão imediatamente (em no máximo 300ms) sem processar nenhuma tecla de aceitação por engano.
4. **Interface de Brainstorming Separada (Modo Isolado):**
   - A funcionalidade de sessão de brainstorming interativo deve ser ativada em uma tela/aba separada do editor principal, nunca em overlay sobre o manuscrito em edição.
   - Disponibilizar nessa tela técnicas estruturadas de geração de ideias: inversão de premissas, método SCAMPER e mapas de consequências dramáticas.

## Parâmetros e configuração
- `SUGGESTION_POPUP_TIMEOUT_MS`: Tempo máximo de exibição de uma sugestão flutuante sem interação do usuário antes de ser ocultada. Padrão: `6000` (6 segundos).
- `SIDEBAR_PASSIVE_OPACITY`: Nível de opacidade da sidebar ao não estar em foco. Padrão: `0.60`.
- `TRIGGER_TOKENS`: Lista de tokens reservados no editor que ativam sugestões contextuais inline. Padrão: `["[nome?]", "[gancho?]", "[ref?]", "[local?]"]`.

## Armadilhas e como evitá-las
- **Armadilha:** Perda de Sensação de Autoria: implementar modos de continuação automática de frases longas ("escrever pelo usuário") em que o sistema propõe parágrafos inteiros sem qualquer gatilho explícito do romancista, fazendo-o sentir que o livro não é mais de sua autoria.
  **Mitigação:** Bloquear toda geração textual proativa longa não acionada por gatilhos explícitos. O sistema de IA deve fornecer sugestões de insumos criativos secundários (nomes, conceitos, pistas de enredo), nunca prosa narrada pronta para inserção direta como se fosse voz do autor. O texto narrativo do romance deve ser redigido estritamente pelo escritor humano (Human Agency, 2024).

## Critérios de validação (Definition of Done)
- [ ] A taxa de abandono ou interrupção forçada de escrita durante exibição de sugestões de IA é igual ou inferior a 5% nas sessões de teste de usabilidade de escrita real.
- [ ] O índice de agência criativa declarada pelos escritores é igual ou superior a 6 em 7 na escala Likert de controle autoral nas avaliações de satisfação.

## Fundamentação científica
- Ippolito, D. et al. (2022) - Creative Writing with an AI-Powered Writing Assistant (Wordcraft) - arXiv 2022
- CoAuthor (2022) - CoAuthor: Designing a Human-AI Collaborative Writing Dataset - CHI 2022
- CreativeFlow (2024) - Measuring Creative Flow in AI-Assisted Writing Interfaces - arXiv 2024
- Human Agency (2024) - Preserving Human Agency in AI Co-Creation: Guidelines for Literary Assistants - arXiv 2024

## Requisitos do projeto relacionados
- RF-33 (sugestões sidebar)
- RF-81 (sugestões inline)
- RF-193 (brainstorm interativo)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*Os princípios de UX de interação não intrusiva passiva como padrão em assistentes de IA criativa são bem documentados e validados empiricamente na literatura de HCI.*

## Exemplos
**Cenário de Interação (Gatilho textual):**
```text
O autor digita: "O capitão da frota tinha um nome peculiar: [nome?]"
Sistema responde na sidebar: ["Roald Vinter", "Marek da Proa", "Ibsen Salgado"]
O autor escolhe ou continua digitando algo diferente.
```
**Cenário de Rejeição Implícita:**
```text
Sistema exibe popup: "Gancho: Kael descobre que o traidor é seu primo."
O autor continua digitando: "A chuva caia forte no porto."
Sistema fecha popup após 300ms sem intervenção do cursor ou teclado.
```
**Caso de falha conhecido:**
O editor exibir um parágrafo de texto gerado automaticamente por extensão sobre o que Kael fez a seguir e inserir o texto no arquivo sem o autor ter pressionado nenhum botão de confirmação.
