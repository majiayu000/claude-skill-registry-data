---
name: "PostgreSQL Database"
description: "Development patterns with PostgreSQL via FireDAC — connection, PL/pgSQL, sequences, JSONB, UPSERT, full-text search, migrations"
---

# PostgreSQL Database — Skill

Use this skill when working with PostgreSQL database in Delphi projects via FireDAC.

## When to Use

- When configuring FireDAC connection with PostgreSQL
- When creating tables, sequences, functions, triggers and views
- When implementing Repositories with FireDAC + PostgreSQL
- When working with advanced types (JSONB, Arrays, UUID, ENUM)
- When implementing UPSERT, CTEs, Full-Text Search or Window Functions
- When planning schema migrations (versioned scripts)

## PostgreSQL Versions

| Version | Relevant News |
|--------|----------------------|
| **12** | Generated Columns, CTE inlining, Partitioning improvements |
| **13** | Incremental sorting, Parallel vacuum, Deduplication in B-tree |
| **14** | Multirange types, `SEARCH`/`CYCLE` in recursive CTEs |
| **15** | `MERGE` statement, JSON logging, `UNIQUE NULL NOT DISTINCT` |
| **16** | Logical replication from standby, `ANY_VALUE()`, ICU default collations |
| **17** | `RETURNING OLD/NEW` no `MERGE`, `JSON_TABLE`, Identity columns improvements |

> **Recommendation:** Use PostgreSQL 14+ for new projects. Enjoy `MERGE`, JSONB and partitioning.

## FireDAC Connection with PostgreSQL

### Minimum Configuration

```pascal
unit MeuApp.Infra.Database.PostgreSQL.Connection;

interface

uses
  FireDAC.Comp.Client,
  FireDAC.Phys.PG,         // Driver PostgreSQL
  FireDAC.Phys.PGDef,      // Defaults do PostgreSQL
  FireDAC.Stan.Def,
  FireDAC.Stan.Pool,
  FireDAC.DApt;

type
  /// <summary>
  ///   Factory de connection PostgreSQL via FireDAC.
  /// </summary>
  TPostgreSQLConnectionFactory = class
  public
    /// <summary>
    ///   Cria e configura uma connection PostgreSQL.
    /// </summary>
    /// <param name="AServer">Address do servidor</param>
    /// <param name="ADatabase">Nome do banco de data</param>
    /// <param name="AUserName">User (default: postgres)</param>
    /// <param name="APassword">Senha do banco</param>
    /// <param name="APort">Porta (default: 5432)</param>
    /// <returns>Connection FireDAC configurada e aberta</returns>
    class function CreateConnection(
      const AServer: string;
      const ADatabase: string;
      const AUserName: string = 'postgres';
      const APassword: string = '';
      APort: Integer = 5432
    ): TFDConnection;

    /// <summary>
    ///   Cria connection via connection string completa.
    /// </summary>
    class function CreateFromConnectionString(
      const AConnectionString: string
    ): TFDConnection;
  end;

implementation

uses
  System.SysUtils;

class function TPostgreSQLConnectionFactory.CreateConnection(
  const AServer, ADatabase, AUserName, APassword: string;
  APort: Integer): TFDConnection;
begin
  if ADatabase.Trim.IsEmpty then
    raise EArgumentException.Create('ADatabase não pode ser vazio');

  Result := TFDConnection.Create(nil);
  try
    Result.DriverName := 'PG';
    Result.Params.Values['Server'] := AServer;
    Result.Params.Values['Port'] := APort.ToString;
    Result.Params.Database := ADatabase;
    Result.Params.UserName := AUserName;
    Result.Params.Password := APassword;

    { Configurações recomendadas }
    Result.Params.Values['CharacterSet'] := 'UTF8';

    { Opções do driver FireDAC }
    Result.FormatOptions.StrsTrim2Len := True;
    Result.FetchOptions.Mode := fmAll;
    Result.ResourceOptions.AutoReconnect := True;
    Result.TxOptions.Isolation := xiReadCommitted;

    { Schema padrão — 'public' por default, alterar se necessário }
    // Result.Params.Values['MetaDefSchema'] := 'public';

    Result.Connected := True;
  except
    Result.Free;
    raise;
  end;
end;

class function TPostgreSQLConnectionFactory.CreateFromConnectionString(
  const AConnectionString: string): TFDConnection;
begin
  Result := TFDConnection.Create(nil);
  try
    Result.ConnectionString := AConnectionString;
    Result.Connected := True;
  except
    Result.Free;
    raise;
  end;
end;
```

### FDPhysPGDriverLink — Configure Client Library

```pascal
uses
  FireDAC.Phys.PGWrapper,
  FireDAC.Phys.PG;

var
  LDriverLink: TFDPhysPGDriverLink;
begin
  LDriverLink := TFDPhysPGDriverLink.Create(nil);
  try
    { Apontar libpq.dll customizado (32/64-bit) }
    LDriverLink.VendorLib := 'C:\PostgreSQL\bin\libpq.dll';

    { Windows: precisa também libintl-9.dll, libeay32.dll, ssleay32.dll no PATH }
  finally
    { DriverLink vive por toda a aplicação — criar no DataModule }
  end;
end;
```

### Connection Pooling

```pascal
{ Via FDManager }
FDManager.ConnectionDefs.AddConnectionDef;
with FDManager.ConnectionDefs.ConnectionDefByName('PG_POOL') do
begin
  DriverID := 'PG';
  Server := 'localhost';
  Port := 5432;
  Database := 'meubanco';
  UserName := 'postgres';
  Password := 'senha';
  Params.Values['CharacterSet'] := 'UTF8';
  Params.Values['Pooled'] := 'True';
  Params.Values['POOL_MaximumItems'] := '50';
  Params.Values['POOL_CleanupTimeout'] := '30000';
  Params.Values['POOL_ExpireTimeout'] := '90000';
end;
```

### SSL/TLS

```pascal
{ Conexão segura com SSL }
Result.Params.Values['PGAdvanced'] := 'sslmode=require';
{ Para certificado de cliente: }
// Result.Params.Values['PGAdvanced'] :=
//   'sslmode=verify-full;sslcert=client-cert.pem;sslkey=client-key.pem;sslrootcert=ca.pem';
```

## Data Types — PostgreSQL Mapping ↔ Delphi

| PostgreSQL | Delphi (FireDAC) | Note |
|------------|------------------|------------|
| `INTEGER` / `INT4` | `ftInteger` / `AsInteger` | 32-bit |
| `BIGINT` / `INT8` | `ftLargeint` / `AsLargeInt` | 64-bit |
| `SMALLINT` / `INT2` | `ftSmallint` / `AsSmallInt` | 16-bit |
| `SERIAL` | `ftAutoInc` / `AsInteger` | 32-bit auto-increment |
| `BIGSERIAL` | `ftAutoInc` / `AsLargeInt` | 64-bit auto-increment |
| `VARCHAR(N)` | `ftString` / `AsString` | Limited text |
| `TEXT` | `ftMemo` / `AsString` | Unlimited Text |
| `NUMERIC(P,S)` | `ftBCD` / `AsCurrency` | Monetary values ​​|
| `DOUBLE PRECISION` | `ftFloat` / `AsFloat` | Ponto flutuante |
| `REAL` / `FLOAT4` | `ftSingle` / `AsSingle` | 32-bit float |
| `DATE` | `ftDate` / `AsDateTime` | Date only |
| `TIME` | `ftTime` / `AsDateTime` | Just in time |
| `TIMESTAMP` | `ftDateTime` / `AsDateTime` | Date + Time (without timezone) |
| `TIMESTAMPTZ` | `ftDateTime` / `AsDateTime` | Date + Time (with timezone) |
| `BOOLEAN` | `ftBoolean` / `AsBoolean` | `TRUE`/`FALSE` native |
| `UUID` | `ftGuid` / `AsString` | Use `gen_random_uuid()` (PG 13+) |
| `JSON` | `ftMemo` / `AsString` | JSON text (validated) |
| `JSONB` | `ftMemo` / `AsString` | Binary JSON (indexable) |
| `BYTEA` | `ftBlob` / `AsBytes` | Binary data |
| `ARRAY` | `ftMemo` / `AsString` | PostgreSQL Array as Text |
| `INET` / `CIDR` | `ftString` / `AsString` | Network addresses |

## Sequences and Auto-Increment

### SERIAL / BIGSERIAL (Legacy)

```sql
-- Cria coluna auto-increment automaticamente + sequence
CREATE TABLE customers (
  id    SERIAL PRIMARY KEY,
  name  VARCHAR(100) NOT NULL
);
-- Equivale a criar uma SEQUENCE + DEFAULT nextval('customers_id_seq')
```

### IDENTITY Columns (Modern — SQL Standard)

```sql
-- Preferir sobre SERIAL em novos projetos (PG 10+)
CREATE TABLE customers (
  id    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name  VARCHAR(100) NOT NULL
);

-- GENERATED BY DEFAULT: permite override manual do ID
CREATE TABLE products (
  id    INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  name  VARCHAR(100) NOT NULL
);
```

### Manual Sequences

```sql
CREATE SEQUENCE seq_order_number START WITH 1000 INCREMENT BY 1;

-- Usar no INSERT
INSERT INTO orders (order_number) VALUES (nextval('seq_order_number'));
```

### RETURNING in Delphi

```pascal
/// <summary>
///   Insere customer e obtém o id e created_at gerados pelo banco.
///   RETURNING funciona com Open (igual ao Firebird).
/// </summary>
procedure TPostgreSQLCustomerRepository.Insert(ACustomer: TCustomer);
var
  LQuery: TFDQuery;
begin
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := FConnection;
    LQuery.SQL.Text :=
      'INSERT INTO customers (name, cpf, email, status) ' +
      'VALUES (:name, :cpf, :email, :status) ' +
      'RETURNING id, created_at';
    LQuery.ParamByName('name').AsString := ACustomer.Name;
    LQuery.ParamByName('cpf').AsString := ACustomer.Cpf;
    LQuery.ParamByName('email').AsString := ACustomer.Email;
    LQuery.ParamByName('status').AsSmallInt := Ord(ACustomer.Status);

    { RETURNING: usar Open para receber o resultado }
    LQuery.Open;
    ACustomer.Id := LQuery.FieldByName('id').AsInteger;
    ACustomer.CreatedAt := LQuery.FieldByName('created_at').AsDateTime;
  finally
    LQuery.Free;
  end;
end;
```

## UPSERT — INSERT ... ON CONFLICT

```sql
-- Inserir ou atualizar se já existir (pela constraint unique)
INSERT INTO customers (cpf, name, email, status)
VALUES (:cpf, :name, :email, :status)
ON CONFLICT (cpf) DO UPDATE SET
  name = EXCLUDED.name,
  email = EXCLUDED.email,
  status = EXCLUDED.status;

-- Ignorar se já existir (sem atualizar)
INSERT INTO customer_tags (customer_id, tag)
VALUES (:customer_id, :tag)
ON CONFLICT DO NOTHING;
```

**In Delphi:**

```pascal
procedure TPostgreSQLCustomerRepository.Upsert(ACustomer: TCustomer);
var
  LQuery: TFDQuery;
begin
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := FConnection;
    LQuery.SQL.Text :=
      'INSERT INTO customers (cpf, name, email, status) ' +
      'VALUES (:cpf, :name, :email, :status) ' +
      'ON CONFLICT (cpf) DO UPDATE SET ' +
      '  name = EXCLUDED.name, ' +
      '  email = EXCLUDED.email, ' +
      '  status = EXCLUDED.status ' +
      'RETURNING id';
    LQuery.ParamByName('cpf').AsString := ACustomer.Cpf;
    LQuery.ParamByName('name').AsString := ACustomer.Name;
    LQuery.ParamByName('email').AsString := ACustomer.Email;
    LQuery.ParamByName('status').AsSmallInt := Ord(ACustomer.Status);
    LQuery.Open;
    ACustomer.Id := LQuery.FieldByName('id').AsInteger;
  finally
    LQuery.Free;
  end;
end;
```

## JSONB — Semi-Structured Data

### Storage and Query

```sql
-- Tabela com coluna JSONB
CREATE TABLE customer_settings (
  customer_id  INTEGER REFERENCES customers(id),
  settings     JSONB NOT NULL DEFAULT '{}',
  PRIMARY KEY (customer_id)
);

-- Inserir JSON
INSERT INTO customer_settings (customer_id, settings)
VALUES (1, '{"theme": "dark", "language": "pt-BR", "notifications": true}');

-- Consultar campo específico
SELECT settings->>'theme' AS theme FROM customer_settings WHERE customer_id = 1;

-- Filtrar por valor JSON
SELECT * FROM customer_settings WHERE settings @> '{"theme": "dark"}';

-- Índice GIN para busca rápida em JSONB
CREATE INDEX idx_settings_gin ON customer_settings USING GIN (settings);
```

**In Delphi:**

```pascal
{ Inserir JSONB }
LQuery.SQL.Text :=
  'INSERT INTO customer_settings (customer_id, settings) ' +
  'VALUES (:customer_id, :settings::jsonb)';
LQuery.ParamByName('customer_id').AsInteger := ACustomerId;
LQuery.ParamByName('settings').AsString := AJsonString;
LQuery.ExecSQL;

{ Ler campo JSONB }
LQuery.SQL.Text :=
  'SELECT settings->>''theme'' AS theme ' +
  'FROM customer_settings WHERE customer_id = :id';
LQuery.ParamByName('id').AsInteger := ACustomerId;
LQuery.Open;
LTheme := LQuery.FieldByName('theme').AsString;
```

## Full-Text Search (FTS)

```sql
-- Coluna tsvector para busca textual
ALTER TABLE products ADD COLUMN search_vector TSVECTOR;

-- Trigger para atualizar automaticamente
CREATE OR REPLACE FUNCTION update_search_vector() RETURNS TRIGGER AS $$
BEGIN
  NEW.search_vector :=
    setweight(to_tsvector('portuguese', COALESCE(NEW.name, '')), 'A') ||
    setweight(to_tsvector('portuguese', COALESCE(NEW.description, '')), 'B');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_product_search BEFORE INSERT OR UPDATE
  ON products FOR EACH ROW EXECUTE FUNCTION update_search_vector();

-- Índice GIN para FTS
CREATE INDEX idx_product_search ON products USING GIN (search_vector);

-- Buscar
SELECT * FROM products
WHERE search_vector @@ plainto_tsquery('portuguese', 'camisa azul')
ORDER BY ts_rank(search_vector, plainto_tsquery('portuguese', 'camisa azul')) DESC;
```

**In Delphi:**

```pascal
function TProductRepository.Search(const ASearchTerm: string): TObjectList<TProduct>;
var
  LQuery: TFDQuery;
begin
  Result := TObjectList<TProduct>.Create(True);
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := FConnection;
    LQuery.SQL.Text :=
      'SELECT id, name, price, description ' +
      'FROM products ' +
      'WHERE search_vector @@ plainto_tsquery(''portuguese'', :term) ' +
      'ORDER BY ts_rank(search_vector, plainto_tsquery(''portuguese'', :term)) DESC ' +
      'LIMIT :limit';
    LQuery.ParamByName('term').AsString := ASearchTerm;
    LQuery.ParamByName('limit').AsInteger := 50;
    LQuery.Open;

    while not LQuery.Eof do
    begin
      Result.Add(MapToProduct(LQuery));
      LQuery.Next;
    end;
  finally
    LQuery.Free;
  end;
end;
```

## CTEs (Common Table Expressions)

```sql
-- CTE para queries complexas e legíveis
WITH active_customers AS (
  SELECT id, name, email
  FROM customers
  WHERE status = 0
),
customer_orders AS (
  SELECT customer_id, COUNT(*) AS total_orders, SUM(total_amount) AS total_spent
  FROM orders
  GROUP BY customer_id
)
SELECT ac.name, ac.email, co.total_orders, co.total_spent
FROM active_customers ac
LEFT JOIN customer_orders co ON co.customer_id = ac.id
ORDER BY co.total_spent DESC NULLS LAST;
```

### Recursive CTE

```sql
-- Hierarquia de categorias
WITH RECURSIVE category_tree AS (
  SELECT id, name, parent_id, 0 AS level
  FROM categories
  WHERE parent_id IS NULL

  UNION ALL

  SELECT c.id, c.name, c.parent_id, ct.level + 1
  FROM categories c
  JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY level, name;
```

## WindowFunctions

```sql
-- Ranking de clientes por valor gasto
SELECT
  c.name,
  SUM(o.total_amount) AS total_spent,
  RANK() OVER (ORDER BY SUM(o.total_amount) DESC) AS ranking,
  ROW_NUMBER() OVER (ORDER BY SUM(o.total_amount) DESC) AS row_num,
  SUM(o.total_amount) / SUM(SUM(o.total_amount)) OVER () * 100 AS percent_total
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name;

-- Média móvel de vendas por dia
SELECT
  order_date::DATE AS day,
  SUM(total_amount) AS daily_total,
  AVG(SUM(total_amount)) OVER (ORDER BY order_date::DATE ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM orders
GROUP BY order_date::DATE
ORDER BY day;
```

## Functions (PL/pgSQL)

```sql
-- Function que retorna valor (equivale a function no Delphi)
CREATE OR REPLACE FUNCTION fn_customer_full_name(p_id INTEGER)
RETURNS VARCHAR AS $$
DECLARE
  v_name VARCHAR;
BEGIN
  SELECT name INTO v_name FROM customers WHERE id = p_id;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'Customer % not found', p_id;
  END IF;
  RETURN v_name;
END;
$$ LANGUAGE plpgsql;

-- Function que retorna tabela (equivale a Selectable Procedure no Firebird)
CREATE OR REPLACE FUNCTION fn_customers_by_status(p_status SMALLINT)
RETURNS TABLE (
  o_id     INTEGER,
  o_name   VARCHAR,
  o_email  VARCHAR,
  o_status SMALLINT
) AS $$
BEGIN
  RETURN QUERY
    SELECT id, name, email, status
    FROM customers
    WHERE status = p_status
    ORDER BY name;
END;
$$ LANGUAGE plpgsql;

-- Procedure (PG 11+ — sem retorno, apenas ação)
CREATE OR REPLACE PROCEDURE sp_deactivate_customer(p_id INTEGER)
LANGUAGE plpgsql AS $$
BEGIN
  UPDATE customers SET status = 1, updated_at = NOW() WHERE id = p_id;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'Customer % not found', p_id;
  END IF;
END;
$$;
```

**Call in Delphi:**

```pascal
{ Function escalar }
LQuery.SQL.Text := 'SELECT fn_customer_full_name(:id)';
LQuery.ParamByName('id').AsInteger := ACustomerId;
LQuery.Open;
LFullName := LQuery.Fields[0].AsString;

{ Function que retorna table (como SELECT) }
LQuery.SQL.Text := 'SELECT * FROM fn_customers_by_status(:status)';
LQuery.ParamByName('status').AsSmallInt := Ord(csActive);
LQuery.Open;

{ Procedure (PG 11+) }
LQuery.SQL.Text := 'CALL sp_deactivate_customer(:id)';
LQuery.ParamByName('id').AsInteger := ACustomerId;
LQuery.ExecSQL;
```

## ENUM Types

```sql
-- Tipo enum nativo do PostgreSQL
CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');

CREATE TABLE orders (
  id          SERIAL PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  status      order_status NOT NULL DEFAULT 'pending',
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Inserir
INSERT INTO orders (customer_id, status) VALUES (1, 'processing');
```

**In Delphi (map to Pascal enum):**

```pascal
type
  TOrderStatus = (osPending, osProcessing, osShipped, osDelivered, osCancelled);

const
  ORDER_STATUS_NAMES: array[TOrderStatus] of string = (
    'pending', 'processing', 'shipped', 'delivered', 'cancelled'
  );

function StringToOrderStatus(const AValue: string): TOrderStatus;
var
  LStatus: TOrderStatus;
begin
  for LStatus := Low(TOrderStatus) to High(TOrderStatus) do
    if SameText(ORDER_STATUS_NAMES[LStatus], AValue) then
      Exit(LStatus);
  raise EArgumentException.CreateFmt('Status inválido: "%s"', [AValue]);
end;

{ Ler do banco }
LOrder.Status := StringToOrderStatus(LQuery.FieldByName('status').AsString);

{ Gravar no banco }
LQuery.ParamByName('status').AsString := ORDER_STATUS_NAMES[AOrder.Status];
```

## UUID as Primary Key

```sql
-- Usar gen_random_uuid() nativo (PG 13+)
CREATE TABLE sessions (
  id         UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id    INTEGER NOT NULL,
  token      VARCHAR(255),
  expires_at TIMESTAMPTZ
);

-- Para PG < 13: CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Então: DEFAULT uuid_generate_v4()
```

**In Delphi:**

```pascal
LQuery.SQL.Text :=
  'INSERT INTO sessions (user_id, token, expires_at) ' +
  'VALUES (:user_id, :token, :expires_at) RETURNING id';
LQuery.ParamByName('user_id').AsInteger := AUserId;
LQuery.ParamByName('token').AsString := AToken;
LQuery.ParamByName('expires_at').AsDateTime := AExpiresAt;
LQuery.Open;
LSessionId := LQuery.FieldByName('id').AsString; { UUID como string }
```

## Transactions and Isolation Levels

### Isolation Levels in PostgreSQL

| Level | FireDAC | Usage |
|-------|---------|-----|
| **Read Committed** | `xiReadCommitted` | ✅ Standard — see committed data |
| **Repeatable Read** | `xiRepeatableRead` | Reports — snapshot at start of transaction |
| **Serializable** | `xiSerializable` | Maximum consistency (may result in serialization failure) |

### Explicit Transaction

```pascal
procedure ExecuteInTransaction(AConnection: TFDConnection; AProc: TProc);
begin
  AConnection.StartTransaction;
  try
    AProc;
    AConnection.Commit;
  except
    AConnection.Rollback;
    raise;
  end;
end;
```

### SAVEPOINT (Partial Transaction)

```pascal
{ PostgreSQL suporta SAVEPOINT para rollback parcial }
FConnection.StartTransaction;
try
  FCustomerRepo.Insert(LCustomer);

  FConnection.ExecSQL('SAVEPOINT before_order');
  try
    FOrderRepo.Insert(LOrder);
  except
    FConnection.ExecSQL('ROLLBACK TO SAVEPOINT before_order');
    { Customer foi salvo, order não }
  end;

  FConnection.Commit;
except
  FConnection.Rollback;
  raise;
end;
```

## LISTEN / NOTIFY (Bank Events)

```sql
-- No PostgreSQL: notificações assíncronas
-- Em uma trigger:
CREATE OR REPLACE FUNCTION notify_new_order() RETURNS TRIGGER AS $$
BEGIN
  PERFORM pg_notify('new_order', json_build_object('id', NEW.id, 'customer_id', NEW.customer_id)::TEXT);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_order_notify AFTER INSERT ON orders
  FOR EACH ROW EXECUTE FUNCTION notify_new_order();
```

```pascal
{ No Delphi: escutar eventos via FireDAC Event Alerter }
uses
  FireDAC.Phys.PG;

var
  LAlerter: TFDEventAlerter;
begin
  LAlerter := TFDEventAlerter.Create(nil);
  try
    LAlerter.Connection := FConnection;
    LAlerter.DriverName := 'PG';
    LAlerter.Names.Text := 'new_order';
    LAlerter.Options.Timeout := 0;
    LAlerter.OnAlert := HandleNewOrderEvent;
    LAlerter.Active := True;
  finally
    { Manter vivo enquanto a aplicação rodar }
  end;
end;

procedure TMyService.HandleNewOrderEvent(ASender: TFDCustomEventAlerter;
  const AEventName: string; const AArgument: Variant);
begin
  { AArgument contém o payload JSON enviado pelo pg_notify }
  if AEventName = 'new_order' then
    ProcessNewOrderNotification(VarToStr(AArgument));
end;
```

## Schemas

```sql
-- Schemas para organizar objetos do banco
CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS audit;

-- Tabelas em schemas diferentes
CREATE TABLE app.customers (...);
CREATE TABLE audit.log (...);

-- Search path: define schemas visíveis por padrão
SET search_path TO app, public;
```

**In Delphi:**

```pascal
{ Definir schema padrão na conexão }
FConnection.Params.Values['MetaDefSchema'] := 'app';

{ Ou via SQL }
FConnection.ExecSQL('SET search_path TO app, public');
```

## Partitioning (PG 10+)

```sql
-- Particionamento por intervalo de data
CREATE TABLE orders (
  id          SERIAL,
  customer_id INTEGER NOT NULL,
  order_date  DATE NOT NULL,
  total       NUMERIC(15,2),
  status      SMALLINT DEFAULT 0
) PARTITION BY RANGE (order_date);

-- Partições por ano
CREATE TABLE orders_2024 PARTITION OF orders
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
CREATE TABLE orders_2025 PARTITION OF orders
  FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
CREATE TABLE orders_2026 PARTITION OF orders
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

-- Índice na tabela particionada (criado em todas as partições)
CREATE INDEX idx_orders_customer ON orders (customer_id);
```

## Schema Creation — Migration Script

```sql
/* migration_001_initial_schema.sql */

/* ===== Extensions ===== */
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

/* ===== ENUM Types ===== */
CREATE TYPE customer_status AS ENUM ('active', 'inactive', 'suspended');
CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');

/* ===== Tables ===== */
CREATE TABLE IF NOT EXISTS customers (
  id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name       VARCHAR(100) NOT NULL,
  cpf        VARCHAR(14) UNIQUE,
  email      VARCHAR(150),
  status     customer_status NOT NULL DEFAULT 'active',
  notes      TEXT,
  metadata   JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS products (
  id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name        VARCHAR(100) NOT NULL,
  price       NUMERIC(15, 2) NOT NULL DEFAULT 0,
  stock_qty   INTEGER NOT NULL DEFAULT 0 CHECK (stock_qty >= 0),
  description TEXT,
  tags        TEXT[] DEFAULT '{}',
  status      customer_status NOT NULL DEFAULT 'active',
  search_vector TSVECTOR,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
  id            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id   INTEGER NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
  order_date    TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  total_amount  NUMERIC(15, 2) NOT NULL DEFAULT 0,
  status        order_status NOT NULL DEFAULT 'pending',
  created_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS order_items (
  id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  order_id    INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id  INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  quantity    INTEGER NOT NULL CHECK (quantity > 0),
  unit_price  NUMERIC(15, 2) NOT NULL,
  total_price NUMERIC(15, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

/* ===== Indices ===== */
CREATE INDEX idx_customer_name     ON customers (name);
CREATE INDEX idx_customer_cpf      ON customers (cpf);
CREATE INDEX idx_order_date        ON orders (order_date);
CREATE INDEX idx_order_customer    ON orders (customer_id);
CREATE INDEX idx_item_order        ON order_items (order_id);
CREATE INDEX idx_product_search    ON products USING GIN (search_vector);

/* ===== Functions ===== */
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_customer_updated BEFORE UPDATE ON customers
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## Schema migration in Delphi

```pascal
/// <summary>
///   Verifica se uma tabela existe no PostgreSQL.
/// </summary>
function TableExists(AConnection: TFDConnection; const ATableName: string;
  const ASchema: string = 'public'): Boolean;
var
  LQuery: TFDQuery;
begin
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := AConnection;
    LQuery.SQL.Text :=
      'SELECT COUNT(*) FROM information_schema.tables ' +
      'WHERE table_schema = :schema AND table_name = :name';
    LQuery.ParamByName('schema').AsString := ASchema;
    LQuery.ParamByName('name').AsString := ATableName.ToLower;
    LQuery.Open;
    Result := LQuery.Fields[0].AsInteger > 0;
  finally
    LQuery.Free;
  end;
end;

/// <summary>
///   Verifica se uma coluna existe em uma tabela.
/// </summary>
function ColumnExists(AConnection: TFDConnection;
  const ATableName, AColumnName: string;
  const ASchema: string = 'public'): Boolean;
var
  LQuery: TFDQuery;
begin
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := AConnection;
    LQuery.SQL.Text :=
      'SELECT COUNT(*) FROM information_schema.columns ' +
      'WHERE table_schema = :schema AND table_name = :table AND column_name = :col';
    LQuery.ParamByName('schema').AsString := ASchema;
    LQuery.ParamByName('table').AsString := ATableName.ToLower;
    LQuery.ParamByName('col').AsString := AColumnName.ToLower;
    LQuery.Open;
    Result := LQuery.Fields[0].AsInteger > 0;
  finally
    LQuery.Free;
  end;
end;
```

## PostgreSQL Error Handling

```pascal
except
  on E: EFDDBEngineException do
  begin
    case E.Kind of
      ekUKViolated:
        raise EDuplicateException.Create('Registro duplicado: ' + E.Message);
      ekFKViolated:
        raise EDependencyException.Create('Violação de FK: ' + E.Message);
      ekRecordLocked:
        raise EConflictException.Create('Registro bloqueado por outra transação');
      ekServerGone:
        raise EConnectionLostException.Create('Conexão com PostgreSQL perdida');
    else
      raise;
    end;
  end;
end;

{ Verificar código de erro PostgreSQL específico }
except
  on E: EFDDBEngineException do
  begin
    { Códigos SQLSTATE do PostgreSQL: }
    { 23505 = unique_violation }
    { 23503 = foreign_key_violation }
    { 23502 = not_null_violation }
    { 40001 = serialization_failure }
    { 40P01 = deadlock_detected }
    if E.Errors[0].ErrorCode = 23505 then
      raise EDuplicateException.Create('Valor duplicado')
    else
      raise;
  end;
end;
```

## Useful Extensions

```sql
-- pgcrypto: criptografia
CREATE EXTENSION IF NOT EXISTS pgcrypto;
SELECT crypt('senha123', gen_salt('bf'));  -- bcrypt hash

-- pg_trgm: busca por similaridade (LIKE otimizado)
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_customer_name_trgm ON customers USING GIN (name gin_trgm_ops);
SELECT * FROM customers WHERE name % 'Joao';  -- busca fuzzy

-- uuid-ossp: geração de UUID (PG < 13, se gen_random_uuid não disponível)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

## PostgreSQL Anti-Patterns to Avoid

```pascal
// ❌ Concatenar SQL — SQL Injection
LQuery.SQL.Text := 'SELECT * FROM customers WHERE name = ''' + AName + '''';

// ✅ Parâmetros parametrizados
LQuery.SQL.Text := 'SELECT * FROM customers WHERE name = :name';
LQuery.ParamByName('name').AsString := AName;

// ❌ ExecSQL com RETURNING — perde o resultado
LQuery.SQL.Text := 'INSERT INTO ... RETURNING id';
LQuery.ExecSQL;

// ✅ Open com RETURNING
LQuery.SQL.Text := 'INSERT INTO ... RETURNING id';
LQuery.Open;

// ❌ SELECT * em tabelas grandes
LQuery.SQL.Text := 'SELECT * FROM orders';

// ✅ Selecionar only colunas necessárias + LIMIT
LQuery.SQL.Text := 'SELECT id, customer_id, total FROM orders LIMIT :limit';

// ❌ N+1 queries (loop com query dentro)
for I := 0 to LCustomers.Count - 1 do
begin
  LQuery.SQL.Text := 'SELECT COUNT(*) FROM orders WHERE customer_id = :id';
  // ...
end;

// ✅ JOIN ou subquery
LQuery.SQL.Text :=
  'SELECT c.*, (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS order_count ' +
  'FROM customers c';

// ❌ Usar SERIAL quando IDENTITY é melhor
CREATE TABLE t (id SERIAL PRIMARY KEY);

// ✅ Usar IDENTITY (SQL Standard)
CREATE TABLE t (id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY);

// ❌ Ignorar índices em colunas filtradas
SELECT * FROM orders WHERE customer_id = 1;  -- sem índice = full scan

// ✅ Criar índices para colunas usadas em WHERE, JOIN, ORDER BY
CREATE INDEX idx_order_customer ON orders (customer_id);
```

## Key Differences: PostgreSQL vs Firebird

| Feature | PostgreSQL | Firebird |
|---------|-----------|----------|
| Auto-increment | `SERIAL`, `IDENTITY` | Generator + Trigger BI |
| UPSERT | `ON CONFLICT` | Non-native (partial MERGE FB5) |
| JSON | `JSONB` (indexable) | Non-native |
| Full-Text Search | `tsvector` native | Non-native |
| Arrays | `TEXT[]`, `INT[]` native | Non-native |
| ENUM | `CREATE TYPE ... AS ENUM` | Domain + CHECK |
| Embedded | No (server required) | Yes (fbclient.dll) |
| Schemas | Yes (schema separation) | No (single namespace) |
| IF EXISTS | `CREATE TABLE IF NOT EXISTS` | ✅ Does not exist (use `RDB$RELATIONS`) |
| Partitioning | Native (PG 10+) | Non-native |
| Procedures | `CREATE PROCEDURE` (PG 11+) | `CREATE PROCEDURE` (with `SUSPEND`) |
| WindowFunctions | Extensive support | FB 3+ (basic support) |
| FireDAC Driver | `PG` | `FB` |
| Client Library | `libpq.dll` | `fbclient.dll` |

## PostgreSQL Checklist

- [ ] Driver `PG` configured?
- [ ] Connection string with `Server`, `Port`, `Database`, `UserName`, `Password`?
- [ ] `CharacterSet := 'UTF8'` defined?
- [ ] Parameterized queries (without string concatenation)?
- [ ] `RETURNING` with `Open` (not `ExecSQL`)?
- [ ] `IDENTITY` instead of `SERIAL` for new projects?
- [ ] Explicit transactions for compound operations?
- [ ] Errors handled via `EFDDBEngineException.Kind`?
- [ ] libpq.dll (32/64-bit) in PATH or configured in VendorLib?
- [ ] Indexes created for columns used in WHERE and JOIN?
- [ ] Foreign Keys with appropriate `ON DELETE`/`ON UPDATE`?
- [ ] JSONB for semi-structured data (instead of TEXT)?
- [ ] `information_schema` to check metadata (not `RDB$`)?
