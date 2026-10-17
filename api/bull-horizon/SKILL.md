---
name: bull-horizon
description: Configura, instrumenta e depura o Bull Horizon (@bull-horizon/*), o painel de filas Bull e BullMQ montado dentro da app (Express, NestJS, Fastify, Koa, Hapi) ou via CLI. Use ao "montar o painel /bull", "instalar bull-horizon", "adicionar fila no painel", "agrupar filas na sidebar", "ligar métricas/histórico/throughput", "expor Prometheus/Grafana", "instrumentar fila de IA/agente", "mostrar run do agente", usar createAgentRun com generateText do AI SDK, "declarar flow", "rastrear item entre filas", "trace id", usar startTrace/withTrace/continueTrace, escrever ou revisar um BullMonitorService/BullMonitorExpress com BullAdapter ou BullMQAdapter, proteger a rota do painel, depurar "a fila não aparece", "sem histórico", "aba Agents sumiu", "run não aparece", custo "sem preço", "trace não aparece", "aba Flows vazia", ou migrar de @bull-monitor para @bull-horizon.
---

# Bull Horizon

Bull Horizon é um dashboard (UI React + API GraphQL) para filas **Bull** (v3/v4) e **BullMQ**, distribuído como biblioteca: você monta o router/plugin dentro da sua app Node e ele lê as filas direto do Redis. Mostra jobs (listar, buscar com `jsonata`, retry, remove, promote), contagens ao vivo, histórico de throughput opcional, endpoint Prometheus opcional e, para filas de agente de IA, cada tentativa como um **run** (passos LLM, tools, tokens, custo). Com **flows** declarados, mostra o pipeline entre filas e o caminho de um item pelo trace id.

Fork mantido do `bull-monitor` (s-r-x, arquivado em 2023). Desde a v6 o escopo npm é `@bull-horizon/*`; as classes mantiveram o nome (`BullMonitorExpress`, `BullMonitorFastify`...).

## Quando usar esta skill

- Montar o painel numa app (NestJS é o caso mais comum) ou rodar o CLI standalone.
- Adicionar uma fila nova ao painel, separar filas em grupos, marcar fila como readonly.
- Ligar métricas (throughput, tela Metrics history), ajustar retenção, expor Prometheus.
- Instrumentar uma fila de agente de IA (`ai` na fila + `createAgentRun` no worker).
- Declarar um flow (pipeline que atravessa filas) e propagar o trace nos workers (`flows` no monitor + `startTrace`/`withTrace`/`continueTrace`).
- Proteger a rota do painel (ele não tem auth própria).
- Depurar: fila não aparece, sem histórico, aba Agents ausente, run ausente, contagem `lost`, custo sem preço, trace quebrado ou ausente na aba Flows.
- Migrar um projeto de `@bull-monitor/*` para `@bull-horizon/*`.

## Pacotes

| Pacote | Papel |
|---|---|
| `@bull-horizon/root` | Núcleo: `BullAdapter`, `BullMQAdapter`, tipos de config, `createAgentRun`. Dependência dos adapters |
| `@bull-horizon/express` | `BullMonitorExpress`: expõe `monitor.router` (Express e NestJS) |
| `@bull-horizon/fastify` | `BullMonitorFastify`: `init({ app })` + `app.register(monitor.plugin)` |
| `@bull-horizon/koa` | `BullMonitorKoa`: `monitor.router.routes()` (peer `koa-router`) |
| `@bull-horizon/hapi` | `BullMonitorHapi`: `server.register(monitor.plugin)`. Congelado em `apollo-server-hapi` v3 |
| `@bull-horizon/cli` | Binário `bull-horizon`, painel standalone sem integrar com app |

Todos os pacotes têm a mesma versão. Instale o adapter **e** o root na mesma versão (o adapter de fila é importado do root):

```sh
# estável (latest)
npm i @bull-horizon/express @bull-horizon/root
# beta com runs de agente (tag `beta`): fixe a versão exata nos dois
npm i @bull-horizon/express@6.5.0-beta.0 @bull-horizon/root@6.5.0-beta.0
```

Runs de agente (`ai`, `createAgentRun`, tela Agents) existem a partir da `6.5.0-beta.0`. Pre-release não casa com range: `^6.5.0` **não** instala a beta, e `^6.4.0` nunca sobe sozinho para ela. Enquanto estiver em beta, use a versão exata. Quando a `6.5.0` sair como `latest`, troque para `^6.5.0`.

Bull vs BullMQ: o adapter de fila define o provider. Mesmas opções nos dois.

```ts
import { BullAdapter } from '@bull-horizon/root/dist/bull-adapter';       // fila do pacote `bull`
import { BullMQAdapter } from '@bull-horizon/root/dist/bullmq-adapter';   // fila do pacote `bullmq`

new BullAdapter(queue, { group: 'App', readonly: false, ai: undefined });
```

| Opção da fila | Efeito |
|---|---|
| `group` | Rótulo cosmético: agrupa filas numa entrada recolhível da sidebar |
| `readonly` | Esconde/bloqueia ações que alteram jobs (retry, remove, add...) |
| `ai` | Marca fila de agente (`true` ou `AgentQueueConfig`). Ver `references/agent-runs.md` |

Config do monitor (`new BullMonitorX({...})`): `queues` (obrigatório), `metrics` (off por padrão), `prometheus` (off), `ai` (pricing e `recentRuns`), `flows` e `flowsOptions` (ver `references/flows.md`), `baseUrl` (Fastify/Koa/Hapi), `gqlIntrospection` (default: true fora de produção), `textSearchScanCount` (500).

## Fluxo de decisão

1. **Qual framework?** NestJS ou Express: `@bull-horizon/express`. Fastify, Koa, Hapi: o pacote correspondente. Só quer olhar filas sem mexer na app: CLI. Receitas em `references/setup-nestjs.md`.
2. **Qual lib de fila?** `bull` → `BullAdapter`. `bullmq` → `BullMQAdapter`. Uma instância de adapter por fila.
3. **Quais filas?** Todas as que o time precisa ver. Cada uma passada explicitamente em `queues`.
4. **Grupos?** Mais de ~4 filas ou fluxos distintos: um mapa `QUEUE_GROUPS` nome → grupo.
5. **Histórico?** Precisa de gráfico de throughput, tela Metrics history, ou abas Metrics/Runs de agente: `metrics: {}` (ou com retenção custom). Ver `references/metrics-and-prometheus.md`.
6. **Prometheus/Grafana?** `prometheus: true` + `metrics`. Rota sem auth: proteja igual ao painel.
7. **Fila de agente de IA?** `ai` na fila, `createAgentRun` no worker (job que não chama o modelo: `await recorder.skip('motivo')` ou `markAgentRunSkipped`), `removeOnComplete` numérico, `ai.pricing` no monitor. Ver `references/agent-runs.md`.
8. **Item de negócio atravessa várias filas?** Declare o flow em `flows` (etapas = filas), `startTrace` nas entradas, `withTrace` em todo `queue.add` do flow, `encodeTrace`/`continueTrace` em elo por webhook, `metrics` ligado, retenção numérica. Ver `references/flows.md`.
9. **Quem acessa?** Defina a proteção da rota antes de subir (Cloudflare Access, VPN, basic auth, middleware de sessão).

## Regras de ouro

1. **Fila não passada ao monitor não aparece.** Registrar a fila no módulo (`BullModule.registerQueue`) não basta: o painel lista só as filas em `queues`. Fila nova = `@InjectQueue` no service do monitor + adapter na lista + grupo no mapa.
2. **Um grupo por fila**, num mapa central (`QUEUE_GROUPS[queue.name]`). Fila sem entrada no mapa fica fora de grupo (aparece solta).
3. **Toda fila embrulhada num adapter.** Passar a `Queue` crua (ou um adapter de outra cópia de `@bull-horizon/root`) faz a fila ser descartada com `console.error('Since version 3.0.0 every queue should be wrapped...')`.
4. **Métricas são opt-in.** Sem `metrics` não há throughput, Metrics history, nem abas Metrics/Runs de agente. Contagens ao vivo funcionam sem.
5. **Métricas só contam com o monitor no ar.** Nada é retroativo; restart deixa buraco. É observabilidade, não contabilidade.
6. **Fila de agente exige retenção numérica.** `removeOnComplete: true`/`removeOnFail: true` apaga o run junto com o job (vira `lost`). Use número ou `{ age, count }`.
7. **Dado sensível = `detail: 'basic'`** (o default). `full` grava inputs/outputs de tool, textos e a fala do usuário no Redis e nos backups.
8. **Mesmo `AgentQueueConfig` no monitor e no worker.** Um objeto exportado de um arquivo de constantes da fila.
9. **Sem auth nativa.** Quem alcança a rota lê e altera tudo (inclusive logs de job e GraphQL). Proteja a rota com algo **antes** do router.
10. **`await monitor.init()` antes de montar** o router/plugin.
11. **Run de agente mora no `job.log`, gravado pelo `createAgentRun`.** `job.data` leva só ids, o processor dá `await` no `finish`/`fail` e retorna só uma referência, nunca o run. Ler o run do `returnvalue` é só compatibilidade com worker antigo (ver `references/agent-runs.md` § 0).
12. **Flow: trace em todo elo.** `startTrace` em toda entrada e `withTrace(job, data)` em todo `add` do flow; um `add` sem ele quebra o caminho ali. Um trace por item (lote grande = um trace por item com `parent`), mesmo `FlowConfig` no monitor e no worker.
13. **Chave de negócio do flow é id interno opaco** (UUID, chave do banco). Nunca email, telefone, documento, nome, nem hash deles: a busca roda sem auth e vira oráculo de existência.

## Snippet mínimo (Express)

```ts
import Express from 'express';
import Queue from 'bull';
import { BullMonitorExpress } from '@bull-horizon/express';
import { BullAdapter } from '@bull-horizon/root/dist/bull-adapter';

const app = Express();
const monitor = new BullMonitorExpress({
  queues: [new BullAdapter(new Queue('emails', process.env.REDIS_URL), { group: 'App' })],
  metrics: {}, // opcional: liga histórico
});
await monitor.init();
app.use('/bull', requireAuth, monitor.router); // requireAuth: seu middleware
```

Para NestJS (padrão canônico com `BullMonitorService` + módulo), use `references/setup-nestjs.md`.

## Migração de @bull-monitor

1. Trocar dependências: `@bull-monitor/<pkg>` → `@bull-horizon/<pkg>` (mesma versão em todos).
2. Trocar imports, inclusive `@bull-monitor/root/dist/bull-adapter` → `@bull-horizon/root/dist/bull-adapter`.
3. Classes, opções e a chave Redis de métricas (`bull_monitor::metrics::`) **não mudaram**: o histórico existente continua.
4. CLI: binário `bull-monitor` → `bull-horizon`.
5. Versões antigas (<6) dependiam de `apollo-server-*` v2/v3; a v6 usa `@apollo/server` v4 (exceto Hapi). Se o app já usa body parser próprio no Express, `init({ disableBodyParser: true })`.
6. Defaults de métricas mudaram na v6: `collectInterval` 1 min e retenção em camadas de 90 dias (antes 1 h e 100 pontos). Ajuste se dependia do antigo.

## Referências

- `references/setup-nestjs.md`: NestJS canônico (service + módulo), proteção da rota, snippets Express/Fastify/Koa/Hapi/CLI.
- `references/metrics-and-prometheus.md`: `metrics`, retenção em camadas, o que cada tela mostra, Prometheus e scrape.
- `references/agent-runs.md`: filas de agente de IA, `createAgentRun` com AI SDK v6, basic vs full, conversa, pricing, erros comuns.
- `references/flows.md`: flows e traces: declarar o flow, `startTrace`/`withTrace`/`continueTrace`, retenção, status do trace, tetos, erros comuns.
- `references/troubleshooting.md`: sintoma → causa → correção.

Documentação completa no repositório: `README.md`, `docs/agent-runs.md`, `docs/flows.md`, `examples/` (nest, express, fastify, koa, hapi, grafana) em https://github.com/marconneves/bull-horizon.
