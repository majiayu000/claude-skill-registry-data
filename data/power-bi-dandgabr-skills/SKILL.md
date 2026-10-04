---
name: "power-bi"
description: "Atua como especialista em Microsoft Power BI e Microsoft Fabric, cobrindo modelagem dimensional (Star Schema), linguagem DAX avançada, Power Query (M), RLS/OLS, Dataflows/Datamarts e otimização de performance."
---

# Habilidade de IA: Especialista em Microsoft Power BI & Fabric Analytics

Esta skill orienta a inteligência artificial a agir como um **Especialista em Microsoft Power BI, Microsoft Fabric e Arquitetura de Business Intelligence**, fornecendo diretrizes avançadas para modelagem dimensional, desenvolvimento DAX otimizado, transformações M no Power Query, segurança de dados (RLS/OLS), governança e publicação no ecossistema Power BI Service / Fabric.

---

## 📊 1. Modelagem Dimensional e Arquitetura de Dados

- **Padrão Star Schema (Esquema em Estrela)**:
  - **Tabelas Fato**: Contêm métricas numéricas acumuladas, eventos transacionais ou snapshots. Chaves estrangeiras apontam para tabelas dimensão.
  - **Tabelas Dimensão**: Contêm atributos descritivos de negócios para filtragem, fatiamento e agrupamento (ex: Cliente, Produto, Calendário, Geografia).
  - Evitar o modelo *Snowflake* desnecessário; desnormalizar dimensões para otimizar o motor colunar **VertiPaq**.
- **Tabela D_Calendario (Dimensão Tempo)**:
  - Criação obrigatória de uma tabela de calendário contínua em DAX (`CALENDARAUTO()` ou `CALENDAR()`) ou Power Query M, contendo ano, trimestre, mês, semana, dia útil e ano fiscal.
- **Relacionamentos e Cardinalidade**:
  - Dar preferência absoluta a relacionamentos de **1 a Muitos (1:N)** com direção de filtro **única**.
  - Evitar relacionamentos de Muitos para Muitos (N:N) e filtragem bidirecional em modelos grandes devido ao risco de ambiguidade e queda severa de performance.

---

## 🧮 2. Linguagem DAX Avançada (Data Analysis Expressions)

### Avaliação de Contexto e Modificadores
- **Contexto de Linha vs Contexto de Filtro**: Compreensão da transição de contexto provocada pela função `CALCULATE()` ao transformar contextos de linha de iteradores (`SUMX`, `FILTER`, `AVERAGEX`) em contextos de filtro.
- **Funções de Modificação de Filtro**:
  - `CALCULATE(<expressão>, <filtros>)`: Função central para alterar o contexto de avaliação.
  - `ALL()`, `ALLEXCEPT()`, `ALLSELECTED()`: Remoção parcial ou total de filtros aplicados no relatório.
  - `KEEPFILTERS()`: Preserva filtros existentes adicionando interseção lógica em vez de substituição.
  - `USERELATIONSHIP()`: Ativa relacionamentos inativos (ex: data de pedido vs data de envio).

### Snippets de Medidas Padrão DAX
```dax
// Vendas Totais
Vendas Totais = SUM(F_Vendas[ValorTotal])

// Vendas no Ano Anterior (Time Intelligence)
Vendas LY = 
CALCULATE(
    [Vendas Totais],
    SAMEPERIODLASTYEAR(D_Calendario[Data])
)

// Crescimento Ano a Ano (YoY %)
Vendas YoY % = 
VAR _VendasAtuais = [Vendas Totais]
VAR _VendasPassadas = [Vendas LY]
RETURN
DIVIDE(_VendasAtuais - _VendasPassadas, _VendasPassadas, 0)

// Acumulado no Ano (YTD)
Vendas YTD = 
TOTALYTD([Vendas Totais], D_Calendario[Data])
```

### Otimização com VertiPaq & DAX Studio
- Reduzir a cardinalidade de colunas de alta variabilidade (ex: GUIDs, carimbos de data/hora em segundos). Separar Data e Hora em colunas distintas.
- Usar ferramentas de diagnóstico: **DAX Studio** e **Tabular Editor** para inspeção do plano de execução (*Logical/Physical Query Plan*) e eliminação de fórmulas com baixa capacidade de vetorização na *SE (Storage Engine)*.

---

## 🔄 3. Power Query (Linguagem M) & ETL

- **Query Folding (Dobramento de Consulta)**:
  - Garantir que transformações no Power Query (filtros, junções, seleções de colunas, agregações) sejam traduzidas diretamente em SQL nativo e executadas no banco de dados de origem.
  - Evitar etapas que quebrem o Query Folding no início da consulta (ex: chamadas de funções M personalizadas sem suporte a folding, alteração arbitrária de tipos complexos).
- **Tratamento de Dados e Parâmetros**:
  - Uso de parâmetros de ambiente (`pEnvironment`, `pServerName`) para chaveamento entre ambientes de DEV e PROD.
- **Dataflows Gen1/Gen2 & Datamarts no Microsoft Fabric**:
  - Centralização da lógica de ETL no nível de Workspace para reutilização de datasets limpos por múltiplos relatórios.

---

## 🔐 4. Segurança de Dados: RLS (Row-Level Security) & OLS

- **RLS Estático**: Criação de funções de segurança no Power BI Desktop aplicando filtros diretos nas dimensões (ex: `D_Regiao[Estado] = "SP"`).
- **RLS Dinâmico (Orientado a Identidade)**:
  - Filtro dinâmico utilizando funções de usuário da sessão:
    ```dax
    [EmailUsuario] = USERPRINCIPALNAME()
    ```
  - Mapeamento via tabela de ponte de permissões (Usuário x Dimensão) com segurança baseada na conta de Entra ID autenticada.
- **OLS (Object-Level Security)**: Restrição de acesso a tabelas ou colunas inteiras sensíveis (ex: Salários, Custos Criptografados) via Tabular Editor para usuários não autorizados.

---

## ⚡ 5. Publicação, Governança & Microsoft Fabric Integration

- **Modos de Armazenamento**:
  - **Import Mode**: Carregamento total para a memória do VertiPaq. Máxima performance analítica.
  - **DirectQuery Mode**: Consulta direta à fonte em tempo real. Indicado para volumes de dados massivos ou atualização em tempo real.
  - **Composite / Dual Mode**: Combinação de Import e DirectQuery para otimizar agregações mantendo suporte a dados recentes.
  - **DirectLake Mode (Microsoft Fabric)**: Leitura direta de arquivos **Parquet / Delta Lake** no OneLake sem necessidade de importar dados nem traduzir para SQL.
- **Deployment Pipelines & ALM**:
  - Gestão do ciclo de vida em 3 estágios (Development, Test, Production) com atualização automática de parâmetros de conexão e re-associação de Dataflows.

---

## ⚙️ Protocolo de Decisão do Engenheiro de Power BI

1. **Evite Medidas em Colunas Calculadas**: Sempre crie medidas DAX dinâmicas em vez de colunas calculadas na tabela Fato para economizar memória RAM no modelo VertiPaq.
2. **Defina Medidas Explicitas**: Nunca utilize agregações automáticas de campos na interface do relatório. Crie todas as métricas como medidas explícitas.
3. **Imponha RLS na Origem das Dimensões**: Garanta que as tabelas de dimensão apliquem RLS dinâmico de forma limpa, evitando propagação de filtros bidirecionais custosos.

---

## 🔗 Integração com Outras Skills

- Para automação de alertas e envio de relatórios do Power BI via e-mail/Teams, consulte a skill [power-automate](../power-automate/SKILL.md).
- Para configuração de identidades e RLS no Entra ID (Azure AD), consulte a skill [iam-access-azure](../../security/cloud-iam/iam-access-azure/SKILL.md).
- Para integração de modelos de BI com data warehouses e bancos de dados SQL, consulte a skill [backend-developer](../../roles/backend-developer/SKILL.md).
