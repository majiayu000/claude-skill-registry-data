---
name: sincronizacao-e-armazenamento-offline-first
description: Sincroniza bases SQLite com indice vetorial entre dispositivos usando Delta-State CRDTs e resolucao LWW offline-first.
---
# sincronizacao-e-armazenamento-offline-first

## Descrição
A skill `sincronizacao-e-armazenamento-offline-first` especifica as rotinas de persistência e sincronização de dados relacionais e vetoriais em ambientes sem conexão (offline-first). Ela garante a replicação incremental de deltas de dados lógicos e busca híbrida distribuída, mantendo o banco de dados SQLite local dos aplicativos desktop/web sincronizado com o servidor remoto sem corromper alterações e sem substituir arquivos brutos do banco de dados.

## Quando usar
Gatilhos concretos e observáveis:
- O aplicativo detecta perda ou retorno de conexão com a internet (eventos `online` / `offline` do navegador ou sistema operacional).
- Ocorre alteração local de dados (digitação de texto, movimentação no Kanban, atualização de ficha na wiki) necessitando salvar em background.
- O sistema realiza rotinas de sincronização periódica programada (cron job em background).

Quando NÃO usar:
- Para transmissão em tempo real tecla-a-tecla (digitação colaborativa ativa no mesmo parágrafo - nesses casos usar a skill `concorrencia-editor-texto-rico-crdt`).
- Para exclusão definitiva lógica de blocos físicos sob a LGPD (Hard-Delete).

## Pré-requisitos
- Banco de dados relacional e vetorial local (SQLite + SQLite-VSS) instalado nos dispositivos clientes.
- Sistema de controle de versão lógica por mutações (clocks de vetor lógicos).
- Conexão e autenticação com servidor central na nuvem configurada.

## Processo (passo a passo executável)
1. **Gravação Local de Mutações (Offline Write):**
   - Quando o usuário faz alterações em modo offline, gravar as ações na tabela de mutações local (`mutation_log`) contendo a query SQL executada, a chave de versão lógica do registro e a alteração dos metadados.
   - Salvar localmente no arquivo SQLite físico do usuário na máquina.
2. **Delta-State CRDT Synchronization (Ao Reconectar):**
   - Ao detectar o retorno de sinal de internet, abrir um canal seguro com a API de sincronização do servidor.
   - Computar o vetor de estado local (versão atual do banco do cliente) e enviar ao servidor.
   - O servidor responde enviando apenas a diferença lógica (deltas de transações) ocorridas no banco remoto que o cliente ainda não possua.
   - Aplicar os deltas sequencialmente na base SQLite local dentro de blocos de transações protegidos (`BEGIN TRANSACTION ... COMMIT`).
3. **Resolução de Conflitos Last-Write-Wins (LWW):**
   - Se ocorrer edição simultânea do mesmo campo (ex: Usuário A editou o nome da espada no dispositivo offline 1; Usuário B editou o nome da mesma espada no dispositivo online 2):
     - Comparar os timestamps físicos (sincronizados via NTP) e clocks de vetor lógicos.
     - A alteração com o timestamp mais recente vence e é persistida. A perdedora é descartada ou arquivada em tabela de histórico secundária de reconciliação.
4. **Distribuição de QoS de Busca Híbrida (Princípio VELO):**
   - Monitorar a carga de CPU/GPU e consumo de bateria do dispositivo cliente.
   - Se o hardware estiver sobrecarregado ou sem aceleração de GPU local, executar a busca vetorial densa na máquina cliente (borda) e terceirizar as requisições de geração de resumos ou GraphRAG longas ao servidor remoto na nuvem, otimizando o consumo de energia e mantendo a latência estável.

## Parâmetros e configuração
- `SYNC_RETRY_INTERVAL_SECONDS`: Tempo de espera para tentar restabelecer sincronização em caso de queda de rede no meio da transação. Padrão: `15`.
- `MAX_BATCH_MUTATIONS_SIZE`: Quantidade máxima de queries enviadas em um único lote (batch) de sincronização. Padrão: `100`.
- `NTP_SYNC_TOLERANCE_MS`: Tolerância máxima aceitável de dessincronização de relógio físico entre cliente e servidor. Padrão: `500` (ms).

## Armadilhas e como evitá-las
- **Armadilha:** Sobrescrita de Arquivo de Banco de Dados Físico: substituir de forma integral o arquivo SQLite do cliente (`romance.db`) baixando a versão do servidor em background. Isso apaga instantaneamente todas as modificações offline feitas pelo escritor no dispositivo, gerando perda irreversível de dados.
  **Mitigação:** Proibir a substituição ou download direto do arquivo de banco de dados do servidor durante o uso. A replicação e atualização devem ser feitas estritamente em nível de transações de dados lógicos e logs de mutação incrementais de forma atômica (Kleppmann et al., 2019).

## Critérios de validação (Definition of Done)
- [ ] A sincronização incremental em lote atinge 100% de consistência sem corromper registros lógicos sob simulações de desligamento abrupto de rede no meio da transmissão.
- [ ] O banco de dados local SQLite permanece responsivo e operacional para leitura/escrita com latência zero sob falha de internet.

## Fundamentação científica
- Shapiro, M. et al. (2011) - Conflict-Free Replicated Data Types - DISC 2011
- Kleppmann, M. et al. (2019) - Local-first Software: You own your data, in spite of the cloud - IEEE Software
- VELO (2024) - A Vector Database-Assisted Cloud-Edge Collaborative LLM QoS Optimization Framework - arXiv 2024

## Requisitos do projeto relacionados
- RF-127 (sincronização offline)
- RF-90 (sincronização de dados)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*A engenharia de replicação de dados baseada em transações e reconciliações LWW em bancos locais leves (SQLite) é amplamente difundida e madura no ecossistema mobile e desktop.*

## Exemplos
**Entrada (Log de mutações offline a sincronizar):**
```json
{
  "client_id": "client_123",
  "vector_clock": {"client_123": 4, "server": 2},
  "mutations": [
    {"table": "personagens", "action": "UPDATE", "fields": {"id": "char_kael", "idade": 31}, "timestamp": 1783948500}
  ]
}
```
**Saída esperada (Confirmação de Sync):**
```json
{
  "status": "SUCCESS",
  "applied_mutations": 1,
  "server_vector_clock": {"client_123": 4, "server": 3}
}
```
**Caso de falha conhecido:**
Duplicar linhas no banco de dados central do servidor após reconexão devido a falhas no rastreamento de IDs lógicos dos registros.
