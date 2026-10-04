---
name: desfazer-refazer-colaborativo-seletivo
description: Implementa undo/redo distribuido por cliente permitindo reverter seletivamente blocos de IA sem afetar edicoes humanas paralelas.
---
# desfazer-refazer-colaborativo-seletivo

## Descrição
A skill `desfazer-refazer-colaborativo-seletivo` implementa mecanismos distribuídos de desfazer e refazer (Undo/Redo) que preservam a intenção criativa dos autores em sessões de escrita colaborativa. Ela permite que cada autor execute o Ctrl+Z apenas nas suas próprias edições ou que faça o rollback seletivo de blocos de texto inteiros inseridos por assistentes de IA generativa (copiloto), sem reverter ou bagunçar as inserções simultâneas de outros coautores humanos em partes distintas do documento.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor dispara o atalho de teclado `Ctrl+Z` (Undo) ou `Ctrl+Y` (Redo) no editor de texto.
- O autor clica no botão "Rejeitar/Desfazer Sugestão de IA" em uma caixa de edição lateral.
- O sistema reverte a aplicação de uma revisão automática de texto após falha de validação gramatical.

Quando NÃO usar:
- Em operações de exclusão física permanente de dados sob a LGPD (nesse caso, usar exclusão direta do banco).
- Para reversão global de versão de capítulos completos (onde a restauração de backups do histórico resolve de forma mais simples).

## Pré-requisitos
- Motor Yjs instanciado e gerenciador de estado colaborativo ativo.
- Mapeador de transações do cliente (Client-side Transaction Tracker).
- Clocks de vetor lógicos configurados por réplica.

## Processo (passo a passo executável)
1. **Rastreamento de Transações Locais:**
   - Para cada operação de edição local (inserção ou exclusão de texto), gerar um log de transação contendo: o conjunto de IDs de caracteres afetados `(client_id, seq)`, o tipo de alteração e o clock de vetor correspondente na réplica local.
   - Salvar as transações em uma fila local (pilha de Undo local por cliente), nunca em uma pilha global unificada.
2. **Geração de Contra-operações (Undo Distribuído):**
   - Ao receber o sinal de `Undo` do cliente local, desempilhar a última transação local.
   - Em vez de mover ponteiros de histórico, gerar uma contra-operação explícita:
     - Se a transação original inseriu um bloco de texto: gerar uma operação de exclusão explícita visando exatamente os IDs de caracteres daquele bloco.
     - Se a transação original excluiu um bloco de texto: re-inserir os mesmos caracteres preservando seus IDs lógicos originais.
   - Propagar a contra-operação gerada como uma nova alteração CRDT comum na rede.
3. **Undo Seletivo (Rollback de IA):**
   - Identificar transações cujo metadado do autor seja rotulado como `AI_GENERATED`.
   - Caso o escritor solicite reverter a ação da IA, varrer o log de transações do documento e disparar a contra-operação apenas sobre a fatia de IDs correspondentes ao texto gerado pela IA.
   - Preservar intactas as edições humanas paralelas cujo timestamp de clock seja concorrente ou posterior, desde que não tenham alterado diretamente os mesmos caracteres da IA.

## Parâmetros e configuração
- `MAX_UNDO_STACK_SIZE`: Limite máximo de transações mantidas na pilha local de undo para evitar vazamento de memória. Padrão: `100`.
- `METADATA_AUTHOR_TYPE`: Tags de identificação de autoria do bloco. Padrão: `["HUMAN_WRITER", "AI_CO_WRITER"]`.

## Armadilhas e como evitá-las
- **Armadilha:** Undo Linear em Pilha Global: usar uma fila única de histórico no servidor faz com que o Ctrl+Z de um escritor reverta a última palavra escrita por outro coautor que está digitando no final do livro, destruindo o fluxo de escrita de terceiros.
  **Mitigação:** Isolar as filas de Undo por réplica cliente. Cada cliente gerencia estritamente o seu histórico de modificações locais. O comando Undo só atua sobre os IDs gerados pelo `client_id` local ou tags de IA explicitamente delegadas (Stewen; Kleppmann, 2024).

## Critérios de validação (Definition of Done)
- [ ] A reversão de spans específicos de texto afetados por Undo atinge 100% de precisão sob testes de concorrência com 10 editores simultâneos.
- [ ] O Ctrl+Z local não reverte nenhuma inserção feita por outro usuário ativo na mesma sessão colaborativa.

## Fundamentação científica
- Stewen, N. & Kleppmann, M. (2024) - Undo and Redo Support for Replicated Registers - arXiv 2024
- Weiss, S., Urso, P. & Molli, P. (2010) - Logoot-undo: Distributed Collaborative Editing on P2P Networks - IEEE TPDS

## Requisitos do projeto relacionados
- RF-84 (histórico de alterações)
- RF-2 (desfazer/refazer)

## Maturidade e riscos de adoção
**Nível:** Emergente.
*Risco: Gerar contra-operações de inserção de texto preservando IDs deletados pode causar comportamentos complexos de ordenamento (interleaves) em mesclagens tardias.*
*Fallback para v1:* Implementar Undo linear local comum no editor (ProseMirror Yjs UndoManager) que reverta as últimas digitações locais de forma sequencial na réplica ativa, sem permitir reversão seletiva avançada de blocos não-lineares da IA.

## Exemplos
**Entrada (Histórico de Edições Concorrentes):**
- Usuário A insere "O guerreiro ".
- IA insere "era temido em Solaria" (marcado como `AI_CO_WRITER`).
- Usuário A adiciona " e respeitado." após a inserção da IA.
- Usuário A aciona: "Desfazer alteração de IA" (reversão seletiva).
**Saída esperada (Texto consolidado):**
```text
"O guerreiro  e respeitado."
```
**Caso de falha conhecido:**
Ao acionar o desfazer, a frase humana posterior (" e respeitado.") ser excluída junto com a sugestão da IA.
