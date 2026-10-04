---
name: universal-domain-rules-discovery
version: 2.0.0
description: Descoberta universal e rastreável de regras de domínio para agentes de IA.
mode: read-only
compatibility: agent-agnostic
---

# Universal Domain Rules Discovery

## 0. Contrato universal

Este arquivo é o protocolo canônico. Qualquer agente é considerado compatível quando consegue:

1. ler estas instruções;
2. inspecionar ao menos uma fonte de evidência;
3. produzir arquivos Markdown e JSON;
4. declarar limitações quando uma capacidade não estiver disponível.

A skill não depende de marca, modelo, SDK, IDE, MCP, sistema operacional ou provedor. Termos como “ler”, “buscar”, “executar” e “observar” representam capacidades abstratas. O agente deve usar suas ferramentas equivalentes.

### 0.1 Regra de portabilidade

Quando uma ferramenta citada não existir, o agente deve:

1. usar a capacidade equivalente disponível;
2. registrar a limitação em `domain-gaps.md`;
3. reduzir a confiança das conclusões afetadas;
4. nunca fingir que executou uma verificação.

### 0.2 Regra de não alteração

A execução é somente leitura. O agente não deve corrigir bugs, alterar código, migrations, testes, infraestrutura, dados, configurações ou documentação do produto. A única escrita permitida é a criação dos artefatos em `domain-discovery/`.

### 0.3 Resultado esperado

A skill entrega conhecimento verificável para QA. Ela não declara que a aplicação está correta e não substitui validação humana de negócio, jurídica ou regulatória.

## 1. Missão

Analisar profundamente uma aplicação para descobrir as regras específicas que determinam como o sistema deve funcionar e convertê-las em um contrato estruturado para agentes de QA.

Descobrir:

- o que pode ser feito;
- quem pode fazer;
- em quais condições;
- quais dados são necessários;
- quais estados e transições existem;
- quais cálculos, limites e exceções existem;
- quais efeitos colaterais devem ocorrer;
- quais regras são ambíguas, conflitantes, obsoletas ou não implementadas;
- quais riscos são particulares do domínio.

## 2. Invariantes obrigatórios

Todo agente deve respeitar estas regras:

1. **Não inventar regras.** Toda regra precisa de fonte ou deve ser marcada como hipótese.
2. **Separar fato de inferência.** Nunca misturar comportamento observado com intenção presumida.
3. **Manter rastreabilidade.** Regra, fonte, módulo, entidade, ator, operação, risco e cenário de QA devem estar relacionados.
4. **Expor conflitos.** Fontes divergentes nunca podem ser conciliadas silenciosamente.
5. **Preservar evidência.** Registrar caminho, símbolo, endpoint, tabela, tela, ticket, teste ou declaração humana.
6. **Declarar limitações.** Capacidade ausente reduz confiança e cobertura.
7. **Não prometer 100%.** Cobertura só pode ser calculada sobre o universo mapeado.
8. **Não corrigir.** Esta skill diagnostica e documenta; não implementa correções.
9. **Não executar ações destrutivas.** Produção e dados reais não podem ser alterados.
10. **Não tratar ausência de documentação como ausência de regra.** Registrar como lacuna.

## 3. Estados de uma regra

Use exatamente um dos seguintes valores:

- `confirmed`
- `partially_confirmed`
- `inferred`
- `ambiguous`
- `conflicting`
- `undocumented`
- `obsolete`
- `not_implemented`

Confiança:

- `high`: duas ou mais evidências independentes e coerentes, ou uma fonte autoritativa validada pelo comportamento;
- `medium`: uma evidência direta ou múltiplas evidências indiretas coerentes;
- `low`: inferência, fonte antiga, observação incompleta ou conflito não resolvido.

Risco:

- `critical`: segurança, privacidade, integridade financeira, saúde, obrigação legal ou perda grave de dados;
- `high`: bloqueia fluxo principal ou permite ação indevida relevante;
- `medium`: degrada fluxo secundário, consistência ou operação;
- `low`: impacto limitado, cosmético ou de baixa frequência.

## 4. Entradas aceitas

Analise tudo o que estiver autorizado e disponível:

### 4.1 Repositório

README, documentação, código, rotas, controllers, services, use cases, entities, schemas, validators, migrations, seeds, middlewares, guards, policies, testes, mocks, feature flags, variáveis de ambiente, configurações, pipelines e contratos de API.

### 4.2 Produto

Histórias de usuário, critérios de aceite, protótipos, manuais, fluxogramas, documentos funcionais, tickets, issues, pull requests, decisões técnicas e atas.

### 4.3 Aplicação executável

Telas, formulários, mensagens, menus, estados, fluxos, permissões, respostas de API, persistência, logs e efeitos observáveis.

### 4.4 Conhecimento humano

Declarações de Product Owner, especialista de domínio, desenvolvimento, suporte, QA, jurídico, financeiro ou segurança. Registre autor, papel, data e contexto quando fornecidos.

## 5. Ordem obrigatória de execução

Execute as fases nesta ordem. Uma fase pode ser revisitada, mas não omitida silenciosamente.

### Fase 0 — Preparação

1. Identifique nome, versão, branch e commit quando disponíveis.
2. Defina o modo: `full`, `incremental`, `module`, `review` ou `qa-handoff`.
3. Liste capacidades disponíveis e indisponíveis.
4. Crie `domain-discovery/sources/source-index.md`.
5. Registre escopo, exclusões e data da análise.

### Fase 1 — Inventário técnico e funcional

Mapeie módulos, entradas, interfaces, APIs, jobs, integrações, bancos, filas, armazenamento, atores e pontos de autorização.

### Fase 2 — Atores, entidades e operações

Gere inventários de:

- atores e seus papéis;
- entidades e dados críticos;
- operações possíveis;
- dados sensíveis;
- relações de ownership e tenant.

### Fase 3 — Estados e transições

Para toda entidade com ciclo de vida:

1. liste estados encontrados;
2. identifique estado inicial e estados finais;
3. mapeie ações de transição;
4. identifique ator e condições;
5. registre efeitos colaterais;
6. procure transições impossíveis, órfãs ou não protegidas.

### Fase 4 — Descoberta de regras

Procure sistematicamente por regras de:

- acesso e autorização;
- ownership e multi-tenancy;
- estado;
- tempo e timezone;
- finanças;
- capacidade e quotas;
- validação;
- dependência;
- automação;
- auditoria;
- retenção e privacidade;
- integrações;
- IA e aprovação humana;
- concorrência e idempotência;
- importação e exportação;
- exclusão, restauração e anonimização.

### Fase 5 — Cálculos e limites

Para cada cálculo, registre fórmula, entradas, unidade, moeda, precisão, arredondamento, limites, exceções e local da implementação.

### Fase 6 — Comparação entre camadas

Compare a mesma regra nas seguintes camadas quando existirem:

1. requisito/documentação;
2. interface;
3. API;
4. service/use case;
5. banco;
6. teste;
7. job/integração;
8. comportamento observado.

### Fase 7 — Conflitos e lacunas

Registre divergências e ausências. Não escolha uma fonte como correta sem evidência de autoridade.

### Fase 8 — Risco e confiança

Classifique cada regra por impacto, probabilidade qualitativa, detectabilidade e confiança da descoberta.

### Fase 9 — Cenários de QA

Transforme cada regra em cenários positivos, negativos, limites, exceções, manipulação direta, concorrência e falhas de integração conforme aplicável.

### Fase 10 — Validação e encerramento

1. valide os JSONs contra os schemas;
2. verifique IDs únicos;
3. verifique referências entre regras e cenários;
4. confirme que toda regra possui fonte;
5. confirme que toda regra crítica possui cenário;
6. calcule cobertura do universo mapeado;
7. liste tudo que não pôde ser verificado;
8. finalize sem modificar a aplicação.

## 6. Heurísticas universais de descoberta

O agente deve buscar padrões sem depender de linguagem específica.

### 6.1 Evidência de autorização

Procure por guards, policies, roles, scopes, ownership checks, tenant IDs, filtros por usuário, middleware, decorators, ACL, RBAC, ABAC e verificações manuais.

### 6.2 Evidência de estado

Procure enums, constantes, colunas de status, máquinas de estado, condicionais, comandos de transição, eventos e mensagens de UI.

### 6.3 Evidência de limite

Procure `max`, `min`, `limit`, `quota`, `count`, `size`, `capacity`, comparações numéricas, configurações de plano e mensagens de bloqueio.

### 6.4 Evidência temporal

Procure datas de início/fim, TTL, expiração, renovação, carência, timezone, cron, scheduler, retry e retenção.

### 6.5 Evidência financeira

Procure money types, decimal, currency, preço, desconto, taxa, imposto, juros, parcelas, refund, invoice, ledger e arredondamento.

### 6.6 Evidência de idempotência e concorrência

Procure idempotency keys, unique constraints, locks, transações, versionamento, retries, deduplicação e filas.

### 6.7 Evidência de efeito colateral

Procure eventos, notificações, e-mails, webhooks, logs, auditoria, arquivos, filas, cache e integrações externas.

## 7. Estrutura canônica de uma regra

```yaml
id: BR-001
name: Limite de pacientes por plano
module: Subscriptions
entity: Subscription
type: capacity
description: O terapeuta não pode criar novos pacientes ao atingir o limite do plano.
actors: [therapist]
preconditions:
  - subscription status is active or trialing
trigger:
  action: create_patient
conditions:
  - current_patient_count < plan.patient_limit
expected_behavior:
  allowed: create patient
  blocked: reject operation and return a domain message
side_effects:
  - register denied attempt in audit log
exceptions:
  - unlimited plan
sources:
  - id: SRC-001
    type: code
    location: src/services/patient-service.ts
    reference: checkPatientLimit
status: confirmed
confidence: high
risk: high
qa_scenarios: [QA-BR-001-01]
```

## 8. Fontes e precedência

Não existe precedência universal automática. Registre a autoridade aparente de cada fonte:

- `authoritative`: contrato legal, requisito aprovado, decisão formal vigente;
- `implementation`: comportamento implementado;
- `verification`: teste ou comportamento observado;
- `informative`: comentário, README, mensagem ou hipótese.

Quando fontes autoritativas e implementação divergirem, a regra deve ser `conflicting` ou `not_implemented`, nunca “confirmada”.

## 9. Matrizes obrigatórias

### 9.1 Regras

| ID | Módulo | Regra | Tipo | Ator | Pré-condição | Ação | Resultado esperado | Exceção | Fonte | Status | Confiança | Risco |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

### 9.2 Estados

| Entidade | Estado atual | Ação | Próximo estado | Permitido | Ator | Condição | Efeito colateral | Fonte |
|---|---|---|---|---:|---|---|---|---|

### 9.3 Permissões

| Recurso | Operação | Ator | UI protegida | API protegida | Serviço protegido | Banco restringe | Condições | Fonte |
|---|---|---|---:|---:|---:|---:|---|---|

### 9.4 Cálculos

| ID | Nome | Fórmula | Entradas | Precisão | Arredondamento | Limites | Exceções | Fonte |
|---|---|---|---|---|---|---|---|---|

### 9.5 Conflitos

| ID | Regra | Fonte A | Comportamento A | Fonte B | Comportamento B | Implementação atual | Impacto | Decisão necessária |
|---|---|---|---|---|---|---|---|---|

### 9.6 Lacunas

| ID | Lacuna | Módulo | Risco | Evidência | Informação ausente | Impacto no QA |
|---|---|---|---|---|---|---|

### 9.7 Rastreabilidade

| Regra | Fontes | Código | Endpoint/UI | Banco | Testes existentes | Cenários QA | Risco |
|---|---|---|---|---|---|---|---|

## 10. Cenários de QA por regra

Para cada regra aplicável, gere:

1. cenário positivo;
2. cenário negativo;
3. imediatamente abaixo do limite;
4. exatamente no limite;
5. imediatamente acima do limite;
6. exceções conhecidas;
7. chamada direta à API;
8. alteração de identificador, ator ou tenant;
9. repetição da operação;
10. concorrência;
11. falha de dependência externa;
12. estado inicial, resposta, persistência, estado final e efeitos colaterais.

Não gere cenários irrelevantes apenas para aumentar quantidade. Use `not_applicable_reason` quando necessário.

## 11. Artefatos obrigatórios

Produza exatamente esta estrutura:

```text
domain-discovery/
├── domain-overview.md
├── domain-rules.json
├── business-rules-matrix.md
├── state-transition-matrix.md
├── permission-matrix.md
├── calculation-rules.md
├── domain-conflicts.md
├── domain-gaps.md
├── domain-risks.md
├── qa-domain-scenarios.json
├── traceability-matrix.md
└── sources/
    └── source-index.md
```

Use os arquivos em `templates/` como base. Os JSONs devem obedecer aos schemas em `schemas/`.

## 12. Critérios de parada

A execução pode ser encerrada quando:

- todos os módulos dentro do escopo foram inventariados;
- atores e entidades principais foram mapeados;
- estados encontrados foram documentados;
- regras possuem ao menos uma fonte;
- conflitos e lacunas foram registrados;
- regras críticas possuem cenários de QA;
- JSONs foram validados;
- limitações foram explicitadas.

A execução deve ser marcada como `incomplete` quando uma fonte essencial não está acessível ou quando um módulo crítico não pôde ser analisado.

## 13. Métricas

Calcule:

```text
mapped_rule_coverage = tested_mapped_rules / mapped_rules * 100
critical_rule_coverage = tested_critical_mapped_rules / critical_mapped_rules * 100
domain_scenario_coverage = executed_domain_scenarios / mapped_domain_scenarios * 100
traceability_coverage = rules_with_complete_traceability / mapped_rules * 100
```

Nunca apresente essas métricas como cobertura das regras reais desconhecidas. Nomeie-as como cobertura do universo mapeado.

## 14. Handoff para QA

A skill de QA consumidora deve:

1. importar regras confirmadas e parcialmente confirmadas;
2. priorizar risco crítico e alto;
3. testar conflitos como hipóteses concorrentes;
4. registrar lacunas como risco não avaliado;
5. relacionar cada defeito a uma regra, cenário e fonte;
6. indicar regras não testadas;
7. impedir recomendação de produção quando regra crítica mapeada não foi testada, salvo aceite explícito de risco.

## 15. Formato da resposta final do agente

Ao concluir, responder apenas com:

- status: `complete`, `partial` ou `incomplete`;
- caminho dos artefatos;
- total de regras por status e risco;
- conflitos e lacunas críticos;
- cobertura do universo mapeado;
- limitações relevantes;
- resultado da validação dos schemas.

Não incluir correções de código.
