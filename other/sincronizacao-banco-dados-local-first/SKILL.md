---
name: sincronizacao-banco-dados-local-first
description: Sincroniza dados relacionais estruturados (fichas, cronogramas) offline-first entre IndexedDB e PostgreSQL sem conflitos.
---
# sincronizacao-banco-dados-local-first

## Descrição
A skill `sincronizacao-banco-dados-local-first` implementa a sincronização bidirecional e offline-first de dados relacionais complexos estruturados (como fichas de lore, cronogramas de escrita e outlines de capítulos). Ela garante a fusão automática de atualizações concorrentes feitas em IndexedDB local e no servidor PostgreSQL remoto sem perdas de dados e sem exigir resolução de conflitos manuais pelo escritor.

## Quando usar
Gatilhos concretos e observáveis:
- A aplicação inicia sem conexão com a internet (leitura instantânea de snapshots binários locais do IndexedDB).
- A conexão com a internet é restabelecida após um período de escrita offline (disparado pelo listener de status de rede).
- O escritor reorganiza a árvore de capítulos no editor (arraste de arquivos do outline/Kanban).

Quando NÃO usar:
- Para sincronizar texto corrido enriquecido (nesses casos, utilizar a skill `concorrencia-editor-texto-rico-crdt`).
- Para chamadas diretas de APIs transacionais de cobrança ou autenticação de conta.

## Pré-requisitos
- IndexedDB no navegador ou banco SQLite local no aplicativo desktop.
- Extensão Yjs para mapeamento JSON (`Y.Map` e `Y.Array`).
- Banco relacional PostgreSQL na nuvem atuando como repositório central.

## Processo (passo a passo executável)
1. **Modelagem de Dados Estruturados em Yjs:**
   - Mapear a ficha da wiki de personagens/locais como um `Y.Map` contendo pares de chave-valor. As listas ordenadas (ex: inventário) devem ser estruturadas em `Y.Array`.
   - Salvar as modificações no banco local IndexedDB instantaneamente sob formato binário compactado.
2. **Algoritmo de Movimentação em Árvore com Prevenção de Ciclos (Move Operation):**
   - Para drag-and-drop da árvore de capítulos/cenas, usar o algoritmo de movimentação CRDT (princípios Da & Kleppmann, 2023).
   - **Checagem de Ciclo:** Antes de aceitar a operação de re-aninhamento (ex: mover pasta $A$ para dentro da pasta $B$), varrer a hierarquia lógica de pais no cliente. Se $B$ for descendente de $A$, bloquear a alteração na UI para evitar ciclo de órfãos (pastas invisíveis perdidas).
3. **Replicação Relacional Comutativa (CRR):**
   - Na reconciliação de dados entre o IndexedDB do cliente e o PostgreSQL do servidor, aplicar o algoritmo Last-Write-Wins-Element-Set baseado em clocks físicos sincronizados (NTP) e clocks de vetor locais.
   - Atualizar as linhas da base SQL aplicando as modificações no nível granular de atributo (coluna), não substituindo a linha física inteira, permitindo que o Usuário A edite a idade do personagem e o Usuário B edite a cor dos cabelos simultaneamente sem sobrescrever um ao outro.

## Parâmetros e configuração
- `OFFLINE_SYNC_RETRY_MS`: Tempo de espera para tentar nova sincronização sob falha de conexão de rede. Padrão: `5000` (5 segundos).
- `CONFLICT_RESOLUTION_STRATEGY`: Estratégia padrão para conflitos concorrentes de chave-valor idênticas no mesmo instante. Padrão: `"LWW"` (Last-Write-Wins).

## Armadilhas e como evitá-las
- **Armadilha:** Conflito de Loop por Movimentação: dois autores movendo pastas simultaneamente de forma cruzada (Usuário A move Pasta A para dentro de B; Usuário B move Pasta B para dentro de A concorrentemente). Isso quebra o sistema de arquivos fazendo com que ambas as pastas desapareçam da árvore lógica do projeto por falta de nó raiz válido.
  **Mitigação:** Implementar a lógica de checagem de ciclo na aresta local antes de empacotar a alteração no CRDT. Se a transação recebida do servidor tentar criar uma dependência circular, a operação mais antiga no clock lógico deve prevalecer, e a concorrente mais recente deve ser abortada e redirecionada para a pasta raiz global `[Romance_Root]` (Da; Kleppmann, 2023).

## Critérios de validação (Definition of Done)
- [ ] A taxa de resolução de conflitos em fichas relacionais e reordenações de diretórios é de 100% de comutatividade (ambos os clientes convergem para o mesmo estado exato de dados).
- [ ] A aplicação inicializa e renderiza dados da wiki em menos de 100ms em modo offline carregando do IndexedDB local.

## Fundamentação científica
- Kleppmann, M. & Beresford, A. (2016) - A Conflict-Free Replicated JSON Datatype - IEEE TPDS 2016
- Da, Liang & Kleppmann, M. (2023) - Extending JSON CRDTs with Move Operations - arXiv 2023
- CRR Group (2020) - Conflict-free Replicated Relation: A CRDT for Shared Relational Databases - PaPoC 2020
- Kleppmann, M. et al. (2019) - Local-first Software: You own your data, in spite of the cloud - IEEE Software

## Requisitos do projeto relacionados
- RF-2 (reorganização)
- RF-81 (edição concorrente)
- RF-90 (IndexedDB/PostgreSQL sync)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*A modelagem JSON CRDT e a sincronização local-first com SQLite/IndexedDB é estável, com diversas implementações consolidadas em frameworks de produção.*

## Exemplos
**Entrada (Edição Concorrente em Ficha de Lore):**
- Usuário A atualiza: `ficha_kael.idade = 30` (t=1).
- Usuário B atualiza: `ficha_kael.cabelo = "cinza"` (t=2).
- Sincronização remota é restabelecida.
**Saída esperada (Objeto reconciliado no banco central):**
```json
{
  "nome": "Kael",
  "idade": 30,
  "cabelo": "cinza"
}
```
**Caso de falha conhecido:**
Uma pasta sumir da barra lateral de arquivos após o autor arrastá-la sem sinal de internet ativo.
