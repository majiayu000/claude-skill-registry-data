---
name: concorrencia-editor-texto-rico-crdt
description: Implementa edicao colaborativa em tempo real com Strong Eventual Consistency usando CRDTs Yjs e Peritext no editor rico.
---
# concorrencia-editor-texto-rico-crdt

## Descrição
A skill `concorrencia-editor-texto-rico-crdt` implementa as rotinas de edição colaborativa síncrona no editor de texto rico de manuscritos literários longos. Ela garante a consistência eventual forte (SEC - Strong Eventual Consistency) entre réplicas distribuídas usando CRDTs (Conflict-free Replicated Data Types) e o algoritmo Peritext, permitindo a formatação sobreposta estável e a fusão de textos sem conflitos manuais ou degradação na latência local de escrita.

## Quando usar
Gatilhos concretos e observáveis:
- O editor de texto rico ProseMirror/TipTap é inicializado na interface com o documento ativo.
- Um usuário convida ou inicia uma sessão colaborativa ativa com outro coautor na mesma obra.
- Ocorre uma desconexão ou reconexão de rede (sincronização em lote de réplicas locais com o servidor).

Quando NÃO usar:
- Para sincronizar dados relacionais estruturados ou metadados de formulários da wiki (usar a skill `sincronizacao-banco-dados-local-first`).
- Para controle clássico de versionamento por linhas completo (como comandos Git).

## Pré-requisitos
- ProseMirror ou editor visual rico compatível com bindings de estado de documento.
- Biblioteca Yjs (`yjs` e `y-protocols`) instanciada na aplicação.
- Backend ou protocolo Eg-walker para sequenciamento e compactação de metadados.

## Processo (passo a passo executável)
1. **Binding de Documento Replicado:**
   - Instanciar a classe compartilhada de documento do Yjs: `const ydoc = new Y.Doc()`.
   - Obter a estrutura de texto compartilhado ProseMirror vinculando-a a um nó do tipo `Y.XmlFragment` ou `Y.Text`.
   - Conectar o editor visual ao buffer compartilhado via ProseMirror-Yjs binding.
2. **Implementação de Sequência Eg-walker:**
   - Para manuscritos longos (+100.000 palavras), substituir o backend padrão do Yjs pelo motor de compressão Eg-walker.
   - Configurar o Eg-walker para codificar as inserções e remoções de caracteres em lotes hierárquicos menores, reduzindo a pegada em memória gerada pelo acúmulo de caracteres excluídos (tombstones).
3. **Ancoragem de Formatação (Princípio Peritext):**
   - Configurar formatações de texto rico (negrito, itálico, comentários, links) para serem salvas como spans anotados com metadados estruturados.
   - Cada borda do span de estilo deve conter o identificador estável e único do caractere correspondente (character ID composto por `(client_id, sequence_number)`), em vez de usar offsets de posição absolutos.
4. **Coleta de Lixo Cliente-side (Garbage Collection):**
   - Executar a compactação periódica de tombstones no cliente quando o estado do teclado estiver idle por mais de `10` segundos.
   - Compactar os registros de caracteres excluídos contíguos em blocos de metadados resumidos, mantendo a compatibilidade de ordenamento lógico para sincronizações tardias.

## Parâmetros e configuração
- `TYPING_IDLE_GC_DELAY_MS`: Tempo de inatividade na escrita necessário para executar a coleta de lixo de tombstones locais. Padrão: `10000` (10 segundos).
- `WEBSOCKET_SYNC_INTERVAL_MS`: Intervalo de propagação de atualizações de buffer via WebSocket para coautores ativos. Padrão: `100` (sincronização síncrona a cada 100ms de digitação debounced).
- `MAX_TOMBSTONES_LIMIT`: Limite máximo de blocos deletados antes de forçar compressão. Padrão: `5000`.

## Armadilhas e como evitá-las
- **Armadilha:** Marcação Baseada em Offsets Relativos: definir a área de negrito usando contagem numérica de caracteres (ex: de 10 a 20). Se outro autor digitar concorrentemente 5 palavras no início do texto, as posições absolutas se deslocam e o negrito é incorretamente aplicado no meio de outro termo.
  **Mitigação:** Proibir o uso de offsets numéricos para formatação. Vincular os estilos a IDs de caracteres imutáveis gerados pelo CRDT. Ao computar o início e o fim da formatação, buscar as chaves estáveis `(client_id, seq)` dos limites e aplicar a renderização de layout dinamicamente baseando-se nas âncoras (Peritext, 2022).

## Critérios de validação (Definition of Done)
- [ ] A convergência de mesclagem (merge convergence) atinge 100% de consistência sob testes de stress de escrita paralela simulando 1000 inserções simultâneas em ordens aleatórias.
- [ ] A latência de digitação local na interface mantém-se inferior a 2ms, sem sofrer lags decorrentes do cálculo do grafo do CRDT.

## Fundamentação científica
- Gentle, M. & Kleppmann, M. (2025) - Collaborative Text Editing with Eg-walker: Better, Faster, Smaller - EuroSys 2025
- Jahns, K. et al. (2021) - Real-time Collaborative Rich Text Editing with Yjs - Technical Reports 2021
- Schiefer, et al. (2022) - Peritext: A CRDT for Collaborative Rich Text Editing - Ink & Switch 2022

## Requisitos do projeto relacionados
- RF-81 (edição em tempo real)
- RF-82 (IA concorrente)
- UC-424 (editor concorrência)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*A biblioteca Yjs e o ProseMirror-Yjs binding são ferramentas consolidadas em produção de larga escala no mercado Web, fornecendo garantias de SEC estáveis.*

## Exemplos
**Entrada (Edição Concorrente):**
- Usuário 1 insere: "Kael" no início.
- Usuário 2 insere: " de Solaria" logo após "Kael" simultaneamente.
- Ambos os buffers de modificação são propagados.
**Saída esperada (Consolidada em ambas as telas):**
```text
"Kael de Solaria"
```
**Caso de falha conhecido:**
Haver duplicação de texto ("KaelKael de Solaria") ou deslocamento de formatações de negrito após mesclagens assíncronas.
