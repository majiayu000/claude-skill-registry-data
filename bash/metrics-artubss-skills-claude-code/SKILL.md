---
name: railway-metrics
description: Consulte métricas de uso de recursos para serviços Railway. Use quando o usuário perguntar sobre uso de recursos, CPU, memória, rede, disco ou desempenho do serviço, como "quanto de memória meu serviço está usando" ou "meu serviço está lento".
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Metrics, Monitoring, Performance, CPU, Memory, Resources, Analytics]
dependencies: [railway-cli]
allowed-tools: Bash(railway:*)
---

# Métricas de Serviço Railway

Consulte métricas de uso de recursos para serviços Railway.

## Quando Usar

- Usuário pergunta "quanto de memória meu serviço está usando?"
- Usuário pergunta sobre uso de CPU, tráfego de rede, uso de disco
- Usuário quer debugar problemas de desempenho
- Usuário pergunta "meu serviço está saudável?" (combine com a skill railway-service)

## Pré-requisitos

Obtenha environmentId e serviceId do projeto vinculado:

```bash
railway status --json
```

Extraia:
- `environment.id` → environmentId
- `service.id` → serviceId (opcional - omita para obter todos os serviços)

## Valores de MetricMeasurement

| Measurement | Descrição |
|-------------|-----------|
| CPU_USAGE | Uso de CPU (cores) |
| CPU_LIMIT | Limite de CPU (cores) |
| MEMORY_USAGE_GB | Uso de memória em GB |
| MEMORY_LIMIT_GB | Limite de memória em GB |
| NETWORK_RX_GB | Rede recebida em GB |
| NETWORK_TX_GB | Rede transmitida em GB |
| DISK_USAGE_GB | Uso de disco em GB |
| EPHEMERAL_DISK_USAGE_GB | Uso de disco efêmero em GB |
| BACKUP_USAGE_GB | Uso de backup em GB |

## Valores de MetricTag (para groupBy)

| Tag | Descrição |
|-----|-----------|
| DEPLOYMENT_ID | Agrupar por deployment |
| DEPLOYMENT_INSTANCE_ID | Agrupar por instância |
| REGION | Agrupar por região |
| SERVICE_ID | Agrupar por serviço |

## Query

```graphql
query metrics(
  $environmentId: String!
  $serviceId: String
  $startDate: DateTime!
  $endDate: DateTime
  $sampleRateSeconds: Int
  $averagingWindowSeconds: Int
  $groupBy: [MetricTag!]
  $measurements: [MetricMeasurement!]!
) {
  metrics(
    environmentId: $environmentId
    serviceId: $serviceId
    startDate: $startDate
    endDate: $endDate
    sampleRateSeconds: $sampleRateSeconds
    averagingWindowSeconds: $averagingWindowSeconds
    groupBy: $groupBy
    measurements: $measurements
  ) {
    measurement
    tags {
      deploymentInstanceId
      deploymentId
      serviceId
      region
    }
    values {
      ts
      value
    }
  }
}
```

## Exemplo: CPU e Memória da Última Hora

Use heredoc para evitar problemas com escape de shell:

```bash
bash <<'SCRIPT'
START_DATE=$(date -u -v-1H +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d "1 hour ago" +"%Y-%m-%dT%H:%M:%SZ")
ENV_ID="your-environment-id"
SERVICE_ID="your-service-id"

VARS=$(jq -n \
  --arg env "$ENV_ID" \
  --arg svc "$SERVICE_ID" \
  --arg start "$START_DATE" \
  '{environmentId: $env, serviceId: $svc, startDate: $start, measurements: ["CPU_USAGE", "MEMORY_USAGE_GB"]}')

${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'query metrics($environmentId: String!, $serviceId: String, $startDate: DateTime!, $measurements: [MetricMeasurement!]!) {
    metrics(environmentId: $environmentId, serviceId: $serviceId, startDate: $startDate, measurements: $measurements) {
      measurement
      tags { deploymentId region serviceId }
      values { ts value }
    }
  }' \
  "$VARS"
SCRIPT
```

## Exemplo: Todos os Serviços no Environment

Omita serviceId e use groupBy para obter métricas de todos os serviços:

```bash
bash <<'SCRIPT'
START_DATE=$(date -u -v-1H +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d "1 hour ago" +"%Y-%m-%dT%H:%M:%SZ")
ENV_ID="your-environment-id"

VARS=$(jq -n \
  --arg env "$ENV_ID" \
  --arg start "$START_DATE" \
  '{environmentId: $env, startDate: $start, measurements: ["CPU_USAGE", "MEMORY_USAGE_GB"], groupBy: ["SERVICE_ID"]}')

${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'query metrics($environmentId: String!, $startDate: DateTime!, $measurements: [MetricMeasurement!]!, $groupBy: [MetricTag!]) {
    metrics(environmentId: $environmentId, startDate: $startDate, measurements: $measurements, groupBy: $groupBy) {
      measurement
      tags { serviceId region }
      values { ts value }
    }
  }' \
  "$VARS"
SCRIPT
```

## Parâmetros de Tempo

| Parâmetro | Descrição |
|-----------|-----------|
| startDate | Obrigatório. Formato ISO 8601 (ex: `2024-01-01T00:00:00Z`) |
| endDate | Opcional. Padrão é agora |
| sampleRateSeconds | Intervalo de amostragem (ex: 60 para amostras de 1 minuto) |
| averagingWindowSeconds | Janela de média para suavização |

**Dica:** Para a última hora, calcule startDate como `agora - 1 hora` em formato ISO.

## Interpretação da Saída

```json
{
  "data": {
    "metrics": [
      {
        "measurement": "CPU_USAGE",
        "tags": { "deploymentId": "...", "serviceId": "...", "region": "us-west1" },
        "values": [
          { "ts": "2024-01-01T00:00:00Z", "value": 0.25 },
          { "ts": "2024-01-01T00:01:00Z", "value": 0.30 }
        ]
      }
    ]
  }
}
```

- `ts` - timestamp em formato ISO
- `value` - valor da métrica (cores para CPU, GB para memória/disco/rede)

## Composição

- **Obter IDs**: Use a skill railway-status ou `railway status --json`
- **Verificar saúde do serviço**: Use a skill railway-service para status de deployment
- **Visualizar logs**: Use a skill railway-deployment se as métricas mostrarem problemas
- **Escalar serviço**: Use a skill railway-environment para ajustar recursos

## Tratamento de Erros

### Métricas Vazias/Nulas

Serviços sem deployments ativos retornam arrays de métricas vazios. Ao processar com jq, trate nulls:

```bash
# Iteração segura - pule nulls
jq -r '.data.metrics[]? | select(.values != null and (.values | length) > 0) | ...'

# Verifique se as métricas existem antes de processar
jq -e '.data.metrics | length > 0' response.json && echo "has metrics"
```

### Sem Dados de Métricas

O serviço pode ser novo ou não ter tráfego. Verifique:
- Serviço tem deployment ativo (serviços parados não têm métricas)
- Intervalo de tempo inclui período de deployment

### ID de Serviço/Environment Inválido

Verifique IDs com `railway status --json`.

### Permissão Negada

O usuário precisa de acesso ao projeto para consultar métricas.