---
name: gerindo-expedicao
description: Consulta e opera dados logisticos da Nacom Goya. Consulta pedidos, estoque, disponibilidade, lead time. Cria separacoes. Resolve entidades (pedido, produto, cliente, grupo). Use para perguntas como 'tem pedido do Atacadao?', 'quanto tem de palmito?', 'quando fica disponivel?', 'crie separacao do VCD123'.
allowed-tools: Read, Bash, Glob, Grep
---

# Gerindo Expedicao

Skill para consultas e operacoes logisticas da Nacom Goya.

---

## Indice

1. [Quando Usar Esta Skill](#quando-usar-esta-skill)
2. [DECISION TREE - Qual Script Usar?](#decision-tree---qual-script-usar)
   - [Mapeamento Rapido](#mapeamento-rapido)
   - [Regras de Decisao](#regras-de-decisao-em-ordem-de-prioridade)
   - [Como Decidir (Raciocinio)](#como-decidir-raciocinio-obrigatorio)
   - [Termos Ambiguos](#termos-ambiguos---pergunte-antes-de-agir)
   - [Exemplos](#exemplos-de-boas-e-mas-escolhas)
3. [Scripts Disponiveis](#scripts-disponiveis)
   - [analisando_disponibilidade_estoque.py](#1-analisando_disponibilidade_estoquepy)
   - [consultando_situacao_pedidos.py](#2-consultando_situacao_pedidospy)
   - [consultando_produtos_estoque.py](#3-consultando_produtos_estoquepy)
   - [calculando_leadtime_entrega.py](#4-calculando_leadtime_entregapy)
   - [criando_separacao_pedidos.py](#5-criando_separacao_pedidospy)
   - [consultando_programacao_producao.py](#6-consultando_programacao_producaopy)
4. [Fluxo de Criacao de Separacao](#fluxo-de-criacao-de-separacao)
5. [Referencias](#referencias) (tables, business, glossary, synonyms, products, examples)

---

## Quando Usar Esta Skill

USE para:
- Consultas de pedidos: "tem pedido do Atacadao?", "pedido VCD123 esta em separacao?"
- Consultas de estoque: "quanto tem de palmito?", "chegou cogumelo?"
- Analise de disponibilidade: "quando VCD123 fica disponivel?", "o que vai dar falta?"
- Calculo de prazo: "se embarcar amanha, quando chega?"
- Criacao de separacao: "crie separacao do VCD123 pra amanha"
- Resolucao de entidades: identificar pedido, produto, cliente por termos parciais

NAO USE para:
- Analise COMPLETA da carteira com decisoes (use o Agent `analista-carteira`)
- Comunicacao com PCP ou Comercial (use o Agent)
- Decisoes de priorizacao P1-P7 (use o Agent)

---

## REGRAS CRITICAS (NUNCA VIOLAR)

<regras_criticas>

### 1. GUARDRAIL ANTI-ALUCINACAO

**PROIBIDO** criar, calcular ou inferir dados que NAO foram retornados pelo script.

| PERMITIDO | PROIBIDO |
|-----------|----------|
| Mostrar dados retornados pelo script | Inventar "cobertura de X dias" sem calculo |
| Formatar/agrupar dados existentes | Criar campos que nao existem no JSON |
| Resumir informacoes do JSON | Estimar valores sem base no script |

**Se precisar de dado que nao veio no script:** EXECUTE o script com flag adequado ou PERGUNTE ao usuario.

### 2. REGRA DE FALLBACK (NUNCA TRAVAR)

**Se um script falhar ou retornar erro:** SEMPRE responda ao usuario.

| Situacao | Acao |
|----------|------|
| Script retornou erro | Explicar o erro e sugerir alternativa |
| Parametro nao suportado | Usar parametros disponiveis ou perguntar |
| Entidade nao encontrada | Informar "nao encontrei X, voce quis dizer Y?" |
| Timeout/falha tecnica | "Houve um problema ao consultar. Posso tentar de outra forma?" |

**NUNCA:** Ficar em silencio, travar, ou tentar criar scripts customizados.

### 3. SIMULAR ANTES DE EXECUTAR (ACOES)

**Para QUALQUER acao que modifica dados (criar separacao):**
1. Executar SEM --executar (simular)
2. Mostrar resultado ao usuario
3. AGUARDAR confirmacao explicita
4. So entao executar COM --executar

</regras_criticas>

---

## DECISION TREE - Qual Script Usar?

<decision_tree>
SEMPRE consulte esta secao ANTES de executar qualquer script.
A escolha correta evita resultados errados e retrabalho.
</decision_tree>

### Mapeamento Rapido

<mapeamento>

| Se a pergunta menciona... | Use este script | Com estes parametros |
|---------------------------|-----------------|----------------------|
| **PRODUTO + CLIENTE/GRUPO** ("quanto de X pro Y?") | `consultando_situacao_pedidos.py` | `--grupo Y --produto X` ou `--cliente Y --produto X` |
| **Pedidos de um grupo** ("tem pedido do atacadao?") | `consultando_situacao_pedidos.py` | `--grupo atacadao` |
| **Pedidos de um cliente** ("tem pedido do Carrefour?") | `consultando_situacao_pedidos.py` | `--cliente Carrefour` |
| **Pedidos atrasados** | `consultando_situacao_pedidos.py` | `--atrasados` |
| **Estoque de produto** ("quanto tem de X?") | `consultando_produtos_estoque.py` | `--produto X --completo` |
| **Entradas recentes** ("chegou X?") | `consultando_produtos_estoque.py` | `--produto X --entradas` |
| **Ruptura/falta** ("vai faltar X?") | `consultando_produtos_estoque.py` | `--ruptura --dias 7` |
| **Quando pedido fica disponivel** | `analisando_disponibilidade_estoque.py` | `--pedido VCD123` |
| **Disponibilidade de grupo** | `analisando_disponibilidade_estoque.py` | `--grupo atacadao --completude` |
| **Prazo de entrega** ("quando chega?") | `calculando_leadtime_entrega.py` | `--pedido X --data-embarque Y` |
| **Criar separacao** | `criando_separacao_pedidos.py` | `--pedido X --expedicao Y` (SEM --executar primeiro!) |
| **Programacao de producao** | `consultando_programacao_producao.py` | `--listar --dias 7` |

</mapeamento>

### Regras de Decisao (em ordem de prioridade)

<regras_decisao>

1. **Se pergunta tem PRODUTO + CLIENTE/GRUPO juntos:**
   → Use `consultando_situacao_pedidos.py --grupo X --produto Y` ou `--cliente X --produto Y`
   → Exemplo: "quantas caixas de ketchup tem pro atacadao?" → `--grupo atacadao --produto ketchup`

2. **Se pergunta e sobre PEDIDOS de um cliente/grupo (sem produto):**
   → Use `consultando_situacao_pedidos.py --grupo X` ou `--cliente X`
   → Exemplo: "tem pedido do assai?" → `--grupo assai`

3. **Se pergunta e sobre ESTOQUE de produto (sem cliente):**
   → Use `consultando_produtos_estoque.py --produto X --completo`
   → Exemplo: "quanto tem de palmito?" → `--produto palmito --completo`

4. **Se pergunta e sobre DISPONIBILIDADE de pedido:**
   → Use `analisando_disponibilidade_estoque.py --pedido X`
   → Exemplo: "quando VCD123 fica disponivel?" → `--pedido VCD123`

5. **Se pergunta e sobre PRAZO de entrega:**
   → Use `calculando_leadtime_entrega.py`
   → Exemplo: "se embarcar amanha, quando chega?" → `--pedido X --data-embarque amanha`

6. **Se for ACAO de criar separacao:**
   → Use `criando_separacao_pedidos.py` (SEMPRE simular antes de executar!)
   → Exemplo: "crie separacao do VCD123" → `--pedido VCD123 --expedicao [data]` (SEM --executar)

</regras_decisao>

### Como Decidir (Raciocinio Obrigatorio)

<instrucao_raciocinio>
ANTES de escolher qualquer script, faca este raciocinio mentalmente:

**PASSO 1 - IDENTIFICAR**: O que o usuario quer saber?
- E sobre PEDIDOS? (quem comprou, quanto, quando entregar)
- E sobre ESTOQUE? (tem, vai faltar, chegou, quanto sobra)
- E sobre DISPONIBILIDADE? (quando pedido fica pronto)
- E sobre PRAZO? (quando chega se embarcar dia X)
- E uma ACAO? (criar separacao)

**PASSO 2 - VERIFICAR**: Tem cliente/grupo mencionado?
- SIM + produto → `consultando_situacao_pedidos --grupo/--cliente + --produto`
- SIM sem produto → `consultando_situacao_pedidos --grupo/--cliente`
- NAO → provavelmente `consultando_produtos_estoque`

**PASSO 3 - CONFIRMAR**: A escolha faz sentido?
- Se escolhi ESTOQUE mas usuario perguntou "pro atacadao" → **ERRADO** (use PEDIDOS)
- Se escolhi PEDIDOS mas usuario perguntou "quanto tem em estoque" → **ERRADO** (use ESTOQUE)
- Se escolhi DISPONIBILIDADE mas usuario perguntou "quando chega" → **ERRADO** (use LEADTIME)

**PASSO 4 - PERGUNTAR**: Se ainda em duvida apos os 3 passos → pergunte ao usuario!
</instrucao_raciocinio>

---

### Leitura de References (Sob Demanda)

<filosofia_50_50>
**FILOSOFIA: 50% Regra / 50% IA**

Esta skill implementa um equilibrio entre scripts e IA:

**SCRIPTS fazem:**
- Resolver entidades (cliente, grupo, produto)
- Buscar dados no banco
- Retornar TODOS os candidatos (sem truncar)

**IA decide:**
- Como agrupar/apresentar resultados
- Se precisa perguntar algo ao usuario
- Quando usar references para contexto
</filosofia_50_50>

<leitura_references>
ANTES de executar scripts, o agente DEVE ler os references relevantes baseado na pergunta:

| Gatilho na Pergunta | Reference a Ler | Motivo |
|---------------------|-----------------|--------|
| Produto mencionado | `references/products.md` | Entender abreviacoes (CI, AZ VF, BD) |
| Cliente/Grupo | `references/business.md` | Prefixos CNPJ, constantes |
| Termo desconhecido | `references/glossary.md` | "matar", "ruptura", "FOB" |
| Variacao de escrita | `references/synonyms.md` | ketchup→catchup |
| Comunicar PCP/Comercial | `references/communication.md` | Templates de mensagem |
| Duvida de script | `references/examples.md` | Validar escolha |
</leitura_references>

<exemplo_fluxo_50_50>
**Exemplo de Fluxo Completo**

Pergunta: "quanto tem de palmito pro atacadao 183"

1. IA le `references/glossary.md` → "pendente" = qtd_saldo > 0
2. IA le `references/business.md` → atacadao = grupo com prefixos CNPJ
3. IA executa: `python consultando_situacao_pedidos.py --grupo atacadao --produto palmito`
4. Script encontra 18 candidatos de palmito
5. Script busca TODOS na carteira do cliente (nao para por multiplos)
6. Script retorna 2 SKUs com saldo: Tolete 15x300g (2.592 un), Rodela 15x300g (1.053 un)
7. IA apresenta tabela consolidada ao usuario

**IMPORTANTE:** Quando script retorna `ia_decide: true`, a IA DEVE processar os dados e decidir a melhor forma de apresentar.
</exemplo_fluxo_50_50>

---

### Termos Ambiguos - PERGUNTE antes de agir!

<termos_ambiguos>

**Se o usuario usar estes termos, PARE e PERGUNTE antes de executar.**

#### "programacao de entrega" (CRITICO - 4 interpretacoes)

| Opcao | Significado | Campo | Tabela |
|-------|-------------|-------|--------|
| A | Data que cliente solicitou | `data_entrega_pedido` | CarteiraPrincipal |
| B | Data que vamos expedir | `expedicao` | Separacao |
| C | Data que vai chegar no cliente | `agendamento` | Separacao |
| D | Protocolo de agendamento | `protocolo` | Separacao |

**PERGUNTAR:** "Voce quer saber: A) data que o cliente solicitou, B) data de expedicao programada, C) data de chegada no cliente, ou D) protocolo de agendamento?"

#### "quantidade pendente"

| Opcao | Significado | Fonte |
|-------|-------------|-------|
| Carteira | Ainda nao separado | CarteiraPrincipal |
| Separacao | Separado mas nao faturado | Separacao (sincronizado_nf=False) |
| Total | Ambos | Carteira + Separacao |

**ACAO PADRAO:** Mostrar AMBOS e explicar: "Na carteira: X un | Em separacao: Y un | Total pendente: Z un"

#### "itens" vs "unidades"

**NUNCA usar "itens" sozinho.** SEMPRE especificar:
- "X linhas de produto" (SKUs diferentes)
- "X unidades" ou "X caixas" (quantidade)

#### Multiplas lojas do mesmo grupo

Se resultado tiver mais de 1 loja do mesmo grupo (ex: Atacadao):
**PERGUNTAR:** "Encontrei pedidos em X lojas do [grupo]. Qual loja especificamente, ou quer ver todas?"

#### Outros termos ambiguos

| Termo | Possibilidades | O que PERGUNTAR |
|-------|---------------|-----------------|
| "quando fica disponivel?" | Pedido ou produto? | "Voce quer saber quando um PEDIDO fica disponivel ou quando um PRODUTO estara em estoque?" |
| "situacao" | De que? | "Situacao de qual pedido ou produto?" |
| "crie separacao" | Data faltando | "Para qual data de expedicao?" |

</termos_ambiguos>

### Exemplos de Boas e Mas Escolhas

> **VER references/examples.md** para exemplos detalhados de uso correto e anti-patterns.

**Resumo rapido:**
- PRODUTO + CLIENTE → `consultando_situacao_pedidos --grupo/--cliente + --produto`
- So ESTOQUE (sem cliente) → `consultando_produtos_estoque --produto X --completo`
- QUANDO DISPONIVEL → `analisando_disponibilidade_estoque --pedido X`
- QUANDO CHEGA (prazo) → `calculando_leadtime_entrega --pedido X --data-embarque Y`
- CRIAR SEPARACAO → `criando_separacao_pedidos` (SEM --executar primeiro!)

---

## Scripts Disponiveis

### Ambiente Virtual

Sempre ativar antes de executar:
```bash
source .venv/bin/activate
```

---

### 1. analisando_disponibilidade_estoque.py

**Proposito:** Analisa disponibilidade de estoque para pedidos ou grupos de clientes.

**Queries cobertas:** Q1, Q2, Q3, Q4, Q5, Q6, Q9, Q11, Q12

```bash
source .venv/bin/activate && \
python .claude/skills/gerindo-expedicao/scripts/analisando_disponibilidade_estoque.py [parametros]
```

| Parametro | Descricao | Exemplo |
|-----------|-----------|---------|
| `--pedido` | Numero do pedido ou "grupo termo" | `--pedido VCD123` ou `--pedido "atacadao 183"` |
| `--grupo` | Grupo empresarial | `--grupo atacadao`, `--grupo assai`, `--grupo tenda` |
| `--loja` | Identificador da loja (em raz_social_red) | `--loja 183` |
| `--uf` | Filtrar por UF | `--uf SP` |
| `--data` | Data para analise (hoje, amanha, dd/mm, YYYY-MM-DD) | `--data amanha` |
| `--sem-agendamento` | Apenas pedidos sem exigencia de agendamento | flag |
| `--sugerir-adiamento` | Sugerir pedidos para adiar (liberar estoque) | flag |
| `--diagnosticar-origem` | Distinguir falta absoluta vs relativa | flag |
| `--completude` | Calcular % faturado vs pendente | flag |
| `--atrasados` | Analisar pedidos com expedicao vencida | flag |
| `--diagnosticar-causa` | Detalhar causa do atraso | flag |
| `--ranking-impacto` | Ranking de pedidos que mais travam carteira | flag |
| `--limit` | Limite de resultados (default: 100) | `--limit 20` |

---

### 2. consultando_situacao_pedidos.py

**Proposito:** Consulta pedidos por diversos filtros e perspectivas.

**Queries cobertas:** Q8, Q10, Q14, Q16, Q19

```bash
source .venv/bin/activate && \
python .claude/skills/gerindo-expedicao/scripts/consultando_situacao_pedidos.py [parametros]
```

| Parametro | Descricao | Exemplo |
|-----------|-----------|---------|
| `--pedido` | Numero do pedido ou termo de busca | `--pedido VCD123` |
| `--grupo` | Grupo empresarial (atacadao, assai, tenda) | `--grupo atacadao` |
| `--cliente` | ⭐ **NOVO** CNPJ ou nome parcial do cliente | `--cliente Carrefour`, `--cliente "45.543.915"` |
| `--produto` | Filtrar por produto (combina com --grupo ou --cliente) | `--produto palmito` |
| `--atrasados` | Listar pedidos atrasados | flag |
| `--verificar-bonificacao` | Verificar bonificacoes faltando | flag |
| `--status` | Mostrar status detalhado | flag |
| `--consolidar-com` | Buscar pedidos para consolidar | `--consolidar-com "assai 123"` |
| `--ate-data` | Data limite de expedicao | `--ate-data amanha`, `--ate-data 15/12` |
| `--em-separacao` | Buscar em Separacao (nao CarteiraPrincipal) | flag |
| `--limit` | Limite de resultados (default: 100) | `--limit 20` |

**Combinacoes suportadas:**
- `--grupo atacadao --produto ketchup` → Pedidos do Atacadao com ketchup
- `--cliente Carrefour --produto palmito` → Pedidos do Carrefour com palmito
- `--cliente "45.543.915"` → Busca por CNPJ

---

### 3. consultando_produtos_estoque.py

**Proposito:** Consulta estoque atual, movimentacoes, pendencias, projecoes e SITUACAO COMPLETA.

**Queries cobertas:** Q13, Q17, Q18, Q20 + SITUACAO COMPLETA

```bash
source .venv/bin/activate && \
python .claude/skills/gerindo-expedicao/scripts/consultando_produtos_estoque.py [parametros]
```

| Parametro | Descricao | Exemplo |
|-----------|-----------|---------|
| `--produto` | Nome ou termo do produto | `--produto palmito`, `--produto "az verde"` |
| `--completo` | ⭐ **SITUACAO COMPLETA** (estoque, separacoes, demanda, producao, projecao) | flag |
| `--entradas` | Mostrar entradas recentes (qtd > 0) | flag |
| `--saidas` | Mostrar saidas recentes (qtd < 0) | flag |
| `--pendente` | Quantidade pendente de embarque + lista pedidos | flag |
| `--sobra` | Calcular sobra de estoque apos demanda | flag |
| `--ruptura` | Previsao de rupturas | flag |
| `--dias` | Horizonte de projecao em dias (default: 7) | `--dias 14` |
| `--limit` | Limite de resultados (default: 100) | `--limit 50` |
| `--limit-entradas` | Limite de movimentacoes por produto (default: 100) | `--limit-entradas 20` |

**Opcao --completo retorna:**
- Estoque atual e menor estoque nos proximos 7 dias
- Separacoes por data de expedicao (detalhado com pedidos)
- Demanda total (Carteira bruta/liquida + Separacoes)
- Programacao de producao (proximos 14 dias)
- Projecao dia a dia (estoque projetado)
- Indicadores: sobra, cobertura em dias, % disponivel, previsao de ruptura

---

### 4. calculando_leadtime_entrega.py

**Proposito:** Calcula data de entrega OU data de expedicao sugerida (calculo reverso).

**Queries cobertas:** Q7 + CALCULO REVERSO

```bash
source .venv/bin/activate && \
python .claude/skills/gerindo-expedicao/scripts/calculando_leadtime_entrega.py [parametros]
```

| Parametro | Descricao | Exemplo |
|-----------|-----------|---------|
| `--pedido` | Numero do pedido ou termo de busca | `--pedido VCD123`, `--pedido "atacadao 183"` |
| `--cidade` | Cidade de destino (alternativa ao pedido) | `--cidade "Sao Paulo"` |
| `--uf` | UF de destino (requerido se usar --cidade) | `--uf SP` |
| `--data-embarque` | Data de embarque (calcula data de entrega) | `--data-embarque amanha` |
| `--data-entrega` | ⭐ **NOVO** Data de entrega desejada (calcula data de embarque) | `--data-entrega 25/12` |
| `--limit` | Limite de opcoes de transportadora (default: 10) | `--limit 3` |

**Modos de operacao:**

| Modo | Parametro | Descricao |
|------|-----------|-----------|
| Previsao de entrega | `--data-embarque` | Se embarcar dia X, quando chega? |
| Sugestao de embarque | `--data-entrega` | Para chegar dia Y, quando embarcar? |
| Auto (usa pedido) | Apenas `--pedido` | Usa data_entrega_pedido para calculo reverso |

---

### 5. criando_separacao_pedidos.py

**Proposito:** Cria separacoes de pedidos via linguagem natural.

**IMPORTANTE:** Sempre executar primeiro SEM `--executar` para simular!

```bash
source .venv/bin/activate && \
python .claude/skills/gerindo-expedicao/scripts/criando_separacao_pedidos.py [parametros]
```

| Parametro | Descricao | Exemplo |
|-----------|-----------|---------|
| `--pedido` | Numero do pedido (OBRIGATORIO) | `--pedido VCD123` |
| `--expedicao` | Data de expedicao (OBRIGATORIO) | `--expedicao amanha`, `--expedicao 20/12` |
| `--tipo` | Tipo de separacao | `--tipo completa`, `--tipo parcial` |
| `--pallets` | Quantidade de pallets desejada | `--pallets 28` |
| `--pallets-inteiros` | Forcar pallets inteiros por item | flag |
| `--apenas-estoque` | Separar apenas o que tem em estoque | flag |
| `--excluir-produtos` | JSON array de produtos a excluir | `--excluir-produtos '["KETCHUP","MOSTARDA"]'` |
| `--agendamento` | Data de agendamento | `--agendamento 22/12` |
| `--protocolo` | Protocolo de agendamento | `--protocolo AG12345` |
| `--agendamento-confirmado` | Marcar agendamento como confirmado | flag |
| `--executar` | Efetivamente criar (sem isso, apenas simula) | flag |

**Modos de operacao:**

| Modo | Descricao |
|------|-----------|
| Sem `--executar` | SIMULA e mostra o que seria criado |
| Com `--executar` | CRIA efetivamente a separacao |

**Tipos de separacao:**

| Tipo | Parametros | Descricao |
|------|------------|-----------|
| Completa | `--tipo completa` | Todos os itens com qtd total |
| Parcial | `--tipo parcial` | N itens com qtds especificas |
| Por pallets | `--pallets N` | Distribuir N pallets proporcionalmente |
| Pallets inteiros | `--pallets N --pallets-inteiros` | Cada item = pallets inteiros |
| Apenas estoque | `--apenas-estoque` | So o que tem disponivel |
| Excluindo produtos | `--excluir-produtos '[...]'` | Tudo exceto lista |

---

### 6. consultando_programacao_producao.py

**Proposito:** Lista programacao de producao e simula alteracoes para resolver ruptura.

**Queries cobertas:** Q15 + LISTAGEM COMPLETA

```bash
source .venv/bin/activate && \
python .claude/skills/gerindo-expedicao/scripts/consultando_programacao_producao.py [parametros]
```

| Parametro | Descricao | Exemplo |
|-----------|-----------|---------|
| `--listar` | ⭐ **NOVO** Lista TODA a programacao de producao | flag |
| `--dias` | Horizonte em dias (default: 14) | `--dias 7` |
| `--por-dia` | Mostrar detalhes agrupados por dia | flag |
| `--por-linha` | Mostrar detalhes agrupados por linha | flag |
| `--linha` | Filtrar por linha de producao | `--linha "Linha A"` |
| `--produto` | Produto em ruptura (para reprogramacao) | `--produto "VF pouch 150"` |

**Modos de operacao:**

| Modo | Parametro | Descricao |
|------|-----------|-----------|
| Listagem | `--listar` | Toda a programacao dos proximos N dias |
| Reprogramacao | `--produto` | Opcoes para resolver ruptura |

**Exemplo de listagem completa:**
```bash
python .claude/skills/gerindo-expedicao/scripts/consultando_programacao_producao.py --listar --dias 7 --por-dia
```

---

### 7. resolver_entidades.py

**Proposito:** Modulo utilitario para resolver entidades do dominio.

**Uso interno pelos outros scripts.** Resolve:
- Pedidos por numero parcial ou termo
- Produtos por nome ou abreviacoes
- Grupos empresariais por nome
- Cidades por nome (normalizado)

---

## Fluxo de Criacao de Separacao

### Checklist Obrigatorio

| Campo | Obrigatorio | Como Obter |
|-------|-------------|------------|
| Pedido | SIM | Usuario informa |
| Data expedicao | SIM | Usuario informa |
| Tipo (completa/parcial) | SIM | Perguntar se nao especificado |
| Agendamento | CONDICIONAL | Verificar ContatoAgendamento pelo CNPJ |
| Protocolo | CONDICIONAL | Se exige agendamento |

### Sequencia

1. **SIMULAR** primeiro (sem --executar)
2. Verificar alertas de estoque
3. Mostrar resultado ao usuario
4. Solicitar confirmacao
5. **EXECUTAR** (com --executar)

---

## Nivel de Detalhes (Progressive Disclosure)

1. **Resposta inicial**: Resumo com 3-5 itens principais
2. **Se pedir mais**: Mostrar mais itens do mesmo JSON
3. **Se pedir "todos"**: Lista completa

---

## Referencias

<progressive_disclosure>
Os arquivos em `references/` sao carregados sob demanda.
**NAO leia todos de uma vez** - consulte apenas quando necessario.
</progressive_disclosure>

### Gatilhos para Consulta de References

| Se pergunta menciona... | Consultar | Motivo |
|-------------------------|-----------|--------|
| PRIORIZACAO, qual cliente primeiro | `context.md` → Top Clientes | Atacadao=50%, Assai=13% |
| ATRASO, agenda, gargalo | `context.md` → Gargalos | Agendas sao o maior gargalo |
| PARCIAL vs AGUARDAR, decisao | `context.md` → Contexto Estrategico | Fundos limitam estoques |
| "Chegou?", entradas | `glossary.md` → Usar --entradas | Mapeamento de acao |
| Abreviacao (CI, AZ VF, BD) | `products.md` | Resolver abreviacao |
| Termo desconhecido (matar, FOB) | `glossary.md` | Entender jargao |
| Cliente importante (Atacadao, Assai) | `context.md` → SLAs | SLA 45 dias Atacadao |

### Tabela de Referencias

| Arquivo | Quando Consultar |
|---------|------------------|
| [business.md](references/business.md) | Constantes, limites veiculos, formulas de calculo |
| [glossary.md](references/glossary.md) | Termos do dominio (ruptura, matar, FOB, RED, "Chegou?") |
| [synonyms.md](references/synonyms.md) | Termos criticos nao obvios (c car, RED, OP) |
| [products.md](references/products.md) | Abreviacoes de produto (CI, AZ VF, BD, IND) |
| [examples.md](references/examples.md) | Exemplos de uso e anti-patterns |
| [context.md](references/context.md) | Contexto estrategico, clientes top, gargalos, SLAs |
| [communication.md](references/communication.md) | Templates de mensagem para PCP ou Comercial |

> **NOTA:** Para schemas de tabelas, consulte `CLAUDE.md` na raiz do projeto (secao "MODELOS CRITICOS").

**Grupos Empresariais:** `--grupo atacadao`, `--grupo assai`, `--grupo tenda`
