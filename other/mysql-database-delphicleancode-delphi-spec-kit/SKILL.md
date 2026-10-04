---
name: "MySQL Database"
description: "Development patterns with MySQL/MariaDB via FireDAC — connection, stored procedures, AUTO_INCREMENT, JSON, triggers, replication, migrations"
---

# MySQL Database — Skill

Use this skill when working with MySQL or MariaDB databases in Delphi projects via FireDAC.

## When to Use

- When configuring FireDAC connection with MySQL or MariaDB
- When creating tables, stored procedures, functions, triggers and views
- When implementing Repositories with FireDAC + MySQL
- When working with native JSON (MySQL 5.7+), Full-Text Search, Partitioning
- When planning schema migrations (versioned scripts)
- When developing web applications with MySQL backend

## MySQL Versions

| Version | Relevant News |
|--------|----------------------|
| **5.7** | Native JSON, Generated Columns, `sys` schema, Group Replication |
| **8.0** | Recursive CTEs, Window Functions, `DEFAULT (expr)`, Roles, `INVISIBLE` indexes, `NOWAIT`/`SKIP LOCKED` |
| **8.4 LTS** | LTS release, Firewall improvements, Plugin improvements |
| **9.0+** | Vector type, JavaScript stored programs (preview) |

### MariaDB

| Version | Relevant News |
|--------|----------------------|
| **10.2** | Recursive CTEs, Window Functions, `DEFAULT (expr)` |
| **10.3** | `INVISIBLE` columns, `INTERSECT`/`EXCEPT`, Sequences |
| **10.5** | `INET6` type, `JSON_TABLE`, S3 storage engine |
| **11.0+** | Release Calendar, UUID v7, `VECTOR` type |

> **Recommendation:** Use MySQL 8.0+ or ​​MariaDB 10.5+ for new projects.

## FireDAC connection with MySQL

### Minimum Configuration

```pascal
unit MeuApp.Infra.Database.MySQL.Connection;

interface

uses
  FireDAC.Comp.Client,
  FireDAC.Phys.MySQL,       // Driver MySQL
  FireDAC.Phys.MySQLDef,    // Defaults do MySQL
  FireDAC.Stan.Def,
  FireDAC.DApt;

type
  /// <summary>
  ///   Factory de connection MySQL via FireDAC.
  /// </summary>
  TMySQLConnectionFactory = class
  public
    class function CreateConnection(
      const AServer: string;
      const ADatabase: string;
      const AUserName: string = 'root';
      const APassword: string = '';
      APort: Integer = 3306
    ): TFDConnection;
  end;

implementation

uses
  System.SysUtils;

class function TMySQLConnectionFactory.CreateConnection(
  const AServer, ADatabase, AUserName, APassword: string;
  APort: Integer): TFDConnection;
begin
  if ADatabase.Trim.IsEmpty then
    raise EArgumentException.Create('ADatabase não pode ser vazio');

  Result := TFDConnection.Create(nil);
  try
    Result.DriverName := 'MySQL';
    Result.Params.Values['Server'] := AServer;
    Result.Params.Values['Port'] := APort.ToString;
    Result.Params.Database := ADatabase;
    Result.Params.UserName := AUserName;
    Result.Params.Password := APassword;

    { Configurações recomendadas }
    Result.Params.Values['CharacterSet'] := 'utf8mb4';  // ALWAYS utf8mb4 (suporta emoji/4-byte)

    { Opções do driver FireDAC }
    Result.FormatOptions.StrsTrim2Len := True;
    Result.FetchOptions.Mode := fmAll;
    Result.ResourceOptions.AutoReconnect := True;
    Result.TxOptions.Isolation := xiReadCommitted;

    Result.Connected := True;
  except
    Result.Free;
    raise;
  end;
end;
```

### FDPhysMySQLDriverLink — Configure Client Library

```pascal
uses
  FireDAC.Phys.MySQLWrapper,
  FireDAC.Phys.MySQL;

var
  LDriverLink: TFDPhysMySQLDriverLink;
begin
  LDriverLink := TFDPhysMySQLDriverLink.Create(nil);
  try
    { Para MySQL 8.x: libmysql.dll }
    LDriverLink.VendorLib := 'C:\MySQL\lib\libmysql.dll';
    { Para MariaDB: libmariadb.dll }
    // LDriverLink.VendorLib := 'C:\MariaDB\lib\libmariadb.dll';
  finally
    { DriverLink vive por toda a aplicação — criar no DataModule }
  end;
end;
```

> **ATTENTION:** `utf8` in MySQL is only 3 bytes (does not support emoji 🎉). **always use `utf8mb4`** for full charset. MySQL's `utf8` is an alias for `utf8mb3`.

### Connection Pooling

```pascal
{ Via FDManager }
with FDManager.ConnectionDefs.AddConnectionDef do
begin
  Name := 'MySQL_Pool';
  DriverID := 'MySQL';
  Params.Values['Server'] := 'localhost';
  Params.Values['Port'] := '3306';
  Params.Values['Database'] := 'meubanco';
  Params.Values['User_Name'] := 'root';
  Params.Values['Password'] := 'senha';
  Params.Values['CharacterSet'] := 'utf8mb4';
  Params.Values['Pooled'] := 'True';
  Params.Values['POOL_MaximumItems'] := '50';
  Params.Values['POOL_CleanupTimeout'] := '30000';
end;
```

### SSL/TLS

```pascal
Result.Params.Values['SSL_ca'] := '/path/to/ca-cert.pem';
Result.Params.Values['SSL_cert'] := '/path/to/client-cert.pem';
Result.Params.Values['SSL_key'] := '/path/to/client-key.pem';
```

## Data Types — MySQL Mapping ↔ Delphi

| MySQL | Delphi (FireDAC) | Note |
|-------|------------------|------------|
| `INT` / `INTEGER` | `ftInteger` / `AsInteger` | 32-bit signed |
| `BIGINT` | `ftLargeint` / `AsLargeInt` | 64-bit |
| `SMALLINT` | `ftSmallint` / `AsSmallInt` | 16-bit |
| `TINYINT` | `ftSmallint` / `AsSmallInt` | 8-bit (`ftByte` does not exist) |
| `TINYINT(1)` | `ftBoolean` / `AsBoolean` | MySQL Convention for Boolean |
| `VARCHAR(N)` | `ftString` / `AsString` | Limited text |
| `TEXT` | `ftMemo` / `AsString` | Long text (up to 64KB) |
| `LONGTEXT` | `ftMemo` / `AsString` | Very long text (up to 4GB) |
| `DECIMAL(P,S)` | `ftBCD` / `AsCurrency` | Monetary values ​​|
| `DOUBLE` | `ftFloat` / `AsFloat` | Ponto flutuante |
| `FLOAT` | `ftSingle` / `AsSingle` | 32-bit float |
| `DATE` | `ftDate` / `AsDateTime` | Date only |
| `TIME` | `ftTime` / `AsDateTime` | Just in time |
| `DATETIME` | `ftDateTime` / `AsDateTime` | Date + Time (without timezone) |
| `TIMESTAMP` | `ftDateTime` / `AsDateTime` | Data + Hora (auto-update, UTC) |
| `BOOLEAN` / `BOOL` | `ftBoolean` / `AsBoolean` | Alias ​​for `TINYINT(1)` |
| `JSON` | `ftMemo` / `AsString` | Native JSON (MySQL 5.7+) |
| `BLOB` | `ftBlob` / `AsBytes` | Binary data |
| `LONGBLOB` | `ftBlob` / `AsBytes` | Large binary (up to 4GB) |
| `ENUM(...)` | `ftString` / `AsString` | Up to 65535 values ​​|
| `SET(...)` | `ftString` / `AsString` | Combination of values ​​|
| `CHAR(36)` | `ftString` / `AsString` | UUID as string |

## AUTO_INCREMENT

### Table with AUTO_INCREMENT

```sql
CREATE TABLE customers (
  id    INT AUTO_INCREMENT PRIMARY KEY,
  name  VARCHAR(100) NOT NULL,
  email VARCHAR(150)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Get the ID Generated in Delphi

```pascal
/// <summary>
///   Insere customer e obtém o id gerado pelo AUTO_INCREMENT.
///   MySQL NÃO suporta RETURNING — usar LAST_INSERT_ID().
/// </summary>
procedure TMySQLCustomerRepository.Insert(ACustomer: TCustomer);
var
  LQuery: TFDQuery;
begin
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := FConnection;

    { Método 1: Duas queries (mais seguro e portável) }
    LQuery.SQL.Text :=
      'INSERT INTO customers (name, cpf, email, status) ' +
      'VALUES (:name, :cpf, :email, :status)';
    LQuery.ParamByName('name').AsString := ACustomer.Name;
    LQuery.ParamByName('cpf').AsString := ACustomer.Cpf;
    LQuery.ParamByName('email').AsString := ACustomer.Email;
    LQuery.ParamByName('status').AsSmallInt := Ord(ACustomer.Status);
    LQuery.ExecSQL;

    { Obter LAST_INSERT_ID() }
    LQuery.SQL.Text := 'SELECT LAST_INSERT_ID() AS new_id';
    LQuery.Open;
    ACustomer.Id := LQuery.FieldByName('new_id').AsInteger;

    { Método 2: Via propriedade FireDAC (mais direto) }
    // ACustomer.Id := FConnection.GetLastAutoGenValue('');
  finally
    LQuery.Free;
  end;
end;
```

> **⚠️ ATTENTION:** MySQL **DOES NOT** support `RETURNING`. Use `LAST_INSERT_ID()` or `FConnection.GetLastAutoGenValue('')`. This is a **critical difference** compared to Firebird and PostgreSQL.

## UPSERT — INSERT ... ON DUPLICATE KEY UPDATE

```sql
-- Inserir ou atualizar se a PK/UNIQUE já existir
INSERT INTO customers (cpf, name, email, status)
VALUES (:cpf, :name, :email, :status)
ON DUPLICATE KEY UPDATE
  name = VALUES(name),
  email = VALUES(email),
  status = VALUES(status);

-- MySQL 8.0.19+: Alias com AS
INSERT INTO customers (cpf, name, email, status)
VALUES (:cpf, :name, :email, :status) AS new_data
ON DUPLICATE KEY UPDATE
  name = new_data.name,
  email = new_data.email,
  status = new_data.status;
```

**In Delphi:**

```pascal
procedure TMySQLCustomerRepository.Upsert(ACustomer: TCustomer);
var
  LQuery: TFDQuery;
begin
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := FConnection;
    LQuery.SQL.Text :=
      'INSERT INTO customers (cpf, name, email, status) ' +
      'VALUES (:cpf, :name, :email, :status) ' +
      'ON DUPLICATE KEY UPDATE ' +
      '  name = VALUES(name), email = VALUES(email), status = VALUES(status)';
    LQuery.ParamByName('cpf').AsString := ACustomer.Cpf;
    LQuery.ParamByName('name').AsString := ACustomer.Name;
    LQuery.ParamByName('email').AsString := ACustomer.Email;
    LQuery.ParamByName('status').AsSmallInt := Ord(ACustomer.Status);
    LQuery.ExecSQL;

    { Obter ID (seja insert ou update) }
    LQuery.SQL.Text := 'SELECT LAST_INSERT_ID() AS new_id';
    LQuery.Open;
    ACustomer.Id := LQuery.FieldByName('new_id').AsInteger;
  finally
    LQuery.Free;
  end;
end;
```

## Native JSON (MySQL 5.7+)

### Storage and Query

```sql
-- Tabela com coluna JSON
CREATE TABLE customer_settings (
  customer_id  INT NOT NULL REFERENCES customers(id),
  settings     JSON NOT NULL,
  PRIMARY KEY (customer_id)
);

-- Inserir JSON
INSERT INTO customer_settings (customer_id, settings)
VALUES (1, '{"theme": "dark", "language": "pt-BR", "notifications": true}');

-- Consultar campo específico (operador ->>)
SELECT JSON_UNQUOTE(JSON_EXTRACT(settings, '$.theme')) AS theme
FROM customer_settings WHERE customer_id = 1;

-- Sintaxe curta com ->>
SELECT settings->>'$.theme' AS theme FROM customer_settings WHERE customer_id = 1;

-- Filtrar por valor JSON
SELECT * FROM customer_settings
WHERE JSON_CONTAINS(settings, '"dark"', '$.theme');

-- Índice virtual para busca em JSON (Generated Column + Index)
ALTER TABLE customer_settings
  ADD COLUMN theme VARCHAR(50) GENERATED ALWAYS AS (settings->>'$.theme') VIRTUAL,
  ADD INDEX idx_theme (theme);
```

**In Delphi:**

```pascal
{ Inserir JSON }
LQuery.SQL.Text :=
  'INSERT INTO customer_settings (customer_id, settings) ' +
  'VALUES (:customer_id, :settings)';
LQuery.ParamByName('customer_id').AsInteger := ACustomerId;
LQuery.ParamByName('settings').AsString := AJsonString;
LQuery.ExecSQL;

{ Ler campo JSON }
LQuery.SQL.Text :=
  'SELECT settings->>''$.theme'' AS theme ' +
  'FROM customer_settings WHERE customer_id = :id';
LQuery.ParamByName('id').AsInteger := ACustomerId;
LQuery.Open;
LTheme := LQuery.FieldByName('theme').AsString;
```

## Full-Text Search (InnoDB)

```sql
-- Índice FULLTEXT (InnoDB, MyISAM)
ALTER TABLE products ADD FULLTEXT INDEX ft_product_search (name, description);

-- Busca Natural Language
SELECT *, MATCH(name, description) AGAINST('camisa azul' IN NATURAL LANGUAGE MODE) AS relevance
FROM products
WHERE MATCH(name, description) AGAINST('camisa azul' IN NATURAL LANGUAGE MODE)
ORDER BY relevance DESC;

-- Busca Boolean Mode (mais controle)
SELECT * FROM products
WHERE MATCH(name, description) AGAINST('+camisa +azul -infantil' IN BOOLEAN MODE);
```

## Stored Procedures and Functions

```sql
-- Procedure (equivale a Executable no Firebird)
DELIMITER //
CREATE PROCEDURE sp_deactivate_customer(IN p_id INT)
BEGIN
  UPDATE customers SET status = 1, updated_at = NOW() WHERE id = p_id;
  IF ROW_COUNT() = 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Customer not found';
  END IF;
END //
DELIMITER ;

-- Function escalar
DELIMITER //
CREATE FUNCTION fn_customer_full_name(p_id INT) RETURNS VARCHAR(200)
  READS SQL DATA
BEGIN
  DECLARE v_name VARCHAR(200);
  SELECT name INTO v_name FROM customers WHERE id = p_id;
  IF v_name IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Customer not found';
  END IF;
  RETURN v_name;
END //
DELIMITER ;
```

**Call in Delphi:**

```pascal
{ Procedure }
LQuery.SQL.Text := 'CALL sp_deactivate_customer(:p_id)';
LQuery.ParamByName('p_id').AsInteger := ACustomerId;
LQuery.ExecSQL;

{ Function escalar }
LQuery.SQL.Text := 'SELECT fn_customer_full_name(:p_id) AS full_name';
LQuery.ParamByName('p_id').AsInteger := ACustomerId;
LQuery.Open;
LFullName := LQuery.FieldByName('full_name').AsString;
```

> **Note:** MySQL Procedures are called with `CALL`, Functions with `SELECT`. Procedures can return result sets via `SELECT` inside the body.

## ENUM and SET

```sql
-- ENUM: valor único de uma lista
CREATE TABLE orders (
  id        INT AUTO_INCREMENT PRIMARY KEY,
  status    ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled')
              NOT NULL DEFAULT 'pending',
  priority  ENUM('low', 'medium', 'high') NOT NULL DEFAULT 'medium'
);

-- SET: múltiplos valores de uma lista
CREATE TABLE products (
  id      INT AUTO_INCREMENT PRIMARY KEY,
  name    VARCHAR(100),
  tags    SET('new', 'sale', 'featured', 'limited') NOT NULL DEFAULT ''
);

-- Inserir SET
INSERT INTO products (name, tags) VALUES ('Camisa', 'new,featured');
```

**In Delphi (map to Pascal enum):**

```pascal
type
  TOrderStatus = (osPending, osProcessing, osShipped, osDelivered, osCancelled);

const
  ORDER_STATUS_NAMES: array[TOrderStatus] of string = (
    'pending', 'processing', 'shipped', 'delivered', 'cancelled'
  );

{ Ler do banco }
LOrder.Status := StringToOrderStatus(LQuery.FieldByName('status').AsString);

{ Gravar no banco }
LQuery.ParamByName('status').AsString := ORDER_STATUS_NAMES[AOrder.Status];
```

##Triggers

```sql
DELIMITER //

-- Trigger BEFORE INSERT para validação
CREATE TRIGGER trg_customer_before_insert BEFORE INSERT ON customers
FOR EACH ROW
BEGIN
  SET NEW.created_at = NOW();
  SET NEW.updated_at = NOW();
  IF NEW.name = '' OR NEW.name IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Customer name cannot be empty';
  END IF;
END //

-- Trigger BEFORE UPDATE para atualizar timestamp
CREATE TRIGGER trg_customer_before_update BEFORE UPDATE ON customers
FOR EACH ROW
BEGIN
  SET NEW.updated_at = NOW();
END //

DELIMITER ;
```

## Transactions and Isolation Levels

### Isolation Levels in MySQL

| Level | FireDAC | Usage |
|-------|---------|-----|
| **Read Uncommitted** | `xiDirtyRead` | Almost never — reads uncommitted data |
| **Read Committed** | `xiReadCommitted` | ✅ Recommended pattern |
| **Repeatable Read** | `xiRepeatableRead` | InnoDB default — snapshot at start of tx |
| **Serializable** | `xiSerializable` | Maximum consistency (implicit locks) |

> **Note:** InnoDB's default isolation is `REPEATABLE READ`, unlike Firebird/PostgreSQL which use `READ COMMITTED`.

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

### SAVEPOINT

```pascal
FConnection.StartTransaction;
try
  FCustomerRepo.Insert(LCustomer);

  FConnection.ExecSQL('SAVEPOINT before_order');
  try
    FOrderRepo.Insert(LOrder);
  except
    FConnection.ExecSQL('ROLLBACK TO SAVEPOINT before_order');
  end;

  FConnection.Commit;
except
  FConnection.Rollback;
  raise;
end;
```

## InnoDB vs MyISAM

| Feature | InnoDB | MyISAM |
|---------|--------|--------|
| Transactions | ✅ Yes | ❌ No |
| Foreign Keys | ✅ Yes | ❌ No |
| Row-level Locking | ✅ Yes | ❌ Table-level |
| Full-Text Search | ✅ Yes (5.6+) | ✅ Yes |
| Crash Recovery | ✅ Yes | ❌ No |

> **Rule:** Use **always InnoDB** (`ENGINE=InnoDB`). Never MyISAM in new projects.

## Schema Creation — Migration Script

```sql
/* migration_001_initial_schema.sql */

/* ===== Tabelas ===== */
CREATE TABLE IF NOT EXISTS customers (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  name       VARCHAR(100) NOT NULL,
  cpf        VARCHAR(14) UNIQUE,
  email      VARCHAR(150),
  status     TINYINT NOT NULL DEFAULT 0 COMMENT '0=active, 1=inactive, 2=suspended',
  notes      TEXT,
  metadata   JSON,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_customer_name (name),
  INDEX idx_customer_cpf (cpf)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS products (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(100) NOT NULL,
  price       DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
  stock_qty   INT NOT NULL DEFAULT 0,
  description TEXT,
  status      TINYINT NOT NULL DEFAULT 0,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FULLTEXT INDEX ft_product (name, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS orders (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  customer_id   INT NOT NULL,
  order_date    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total_amount  DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
  status        ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled')
                  NOT NULL DEFAULT 'pending',
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_order_customer (customer_id),
  INDEX idx_order_date (order_date),
  FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS order_items (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  order_id    INT NOT NULL,
  product_id  INT NOT NULL,
  quantity    INT NOT NULL,
  unit_price  DECIMAL(15, 2) NOT NULL,
  total_price DECIMAL(15, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/* ===== Triggers ===== */
DELIMITER //
CREATE TRIGGER trg_customer_validate BEFORE INSERT ON customers
FOR EACH ROW
BEGIN
  IF NEW.name = '' OR NEW.name IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Name cannot be empty';
  END IF;
END //
DELIMITER ;

/* ===== Procedures ===== */
DELIMITER //
CREATE PROCEDURE sp_deactivate_customer(IN p_id INT)
BEGIN
  UPDATE customers SET status = 1 WHERE id = p_id;
  IF ROW_COUNT() = 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Customer not found';
  END IF;
END //
DELIMITER ;
```

## Schema migration in Delphi

```pascal
/// <summary>
///   Verifica se uma tabela existe no MySQL.
/// </summary>
function TableExists(AConnection: TFDConnection;
  const ATableName: string): Boolean;
var
  LQuery: TFDQuery;
begin
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := AConnection;
    LQuery.SQL.Text :=
      'SELECT COUNT(*) FROM information_schema.tables ' +
      'WHERE table_schema = DATABASE() AND table_name = :name';
    LQuery.ParamByName('name').AsString := ATableName;
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
  const ATableName, AColumnName: string): Boolean;
var
  LQuery: TFDQuery;
begin
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := AConnection;
    LQuery.SQL.Text :=
      'SELECT COUNT(*) FROM information_schema.columns ' +
      'WHERE table_schema = DATABASE() AND table_name = :table AND column_name = :col';
    LQuery.ParamByName('table').AsString := ATableName;
    LQuery.ParamByName('col').AsString := AColumnName;
    LQuery.Open;
    Result := LQuery.Fields[0].AsInteger > 0;
  finally
    LQuery.Free;
  end;
end;
```

## MySQL Error Handling

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
        raise EConflictException.Create('Registro bloqueado — deadlock');
      ekServerGone:
        raise EConnectionLostException.Create('Conexão com MySQL perdida');
    else
      raise;
    end;
  end;
end;

{ Verificar código de erro MySQL específico }
except
  on E: EFDDBEngineException do
  begin
    { Códigos de erro MySQL comuns: }
    { 1062 = ER_DUP_ENTRY (duplicate key) }
    { 1451 = ER_ROW_IS_REFERENCED_2 (FK restrict) }
    { 1452 = ER_NO_REFERENCED_ROW_2 (FK no parent) }
    { 1213 = ER_LOCK_DEADLOCK }
    { 1205 = ER_LOCK_WAIT_TIMEOUT }
    { 2006 = CR_SERVER_GONE_ERROR }
    { 2013 = CR_SERVER_LOST }
    if E.Errors[0].ErrorCode = 1062 then
      raise EDuplicateException.Create('Valor duplicado')
    else
      raise;
  end;
end;
```

## CTEs and Window Functions (MySQL 8.0+)

```sql
-- CTE (MySQL 8.0+)
WITH active_customers AS (
  SELECT id, name, email FROM customers WHERE status = 0
)
SELECT ac.name, COUNT(o.id) AS total_orders
FROM active_customers ac
LEFT JOIN orders o ON o.customer_id = ac.id
GROUP BY ac.id, ac.name;

-- CTE Recursiva (hierarquia)
WITH RECURSIVE category_tree AS (
  SELECT id, name, parent_id, 0 AS level
  FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.id, c.name, c.parent_id, ct.level + 1
  FROM categories c JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY level, name;

-- Window Functions (MySQL 8.0+)
SELECT name, total_spent,
  RANK() OVER (ORDER BY total_spent DESC) AS ranking,
  ROW_NUMBER() OVER (ORDER BY total_spent DESC) AS row_num
FROM (
  SELECT c.name, SUM(o.total_amount) AS total_spent
  FROM customers c JOIN orders o ON o.customer_id = c.id
  GROUP BY c.id, c.name
) ranked;
```

## UUID as Primary Key

```sql
-- Gerar UUID no MySQL
CREATE TABLE sessions (
  id        CHAR(36) NOT NULL DEFAULT (UUID()) PRIMARY KEY,
  user_id   INT NOT NULL,
  token     VARCHAR(255),
  INDEX idx_session_user (user_id)
) ENGINE=InnoDB;

-- MySQL 8.0+: UUID() como DEFAULT
-- MySQL < 8.0: gerar no Delphi e enviar como parâmetro
```

**In Delphi:**

```pascal
uses
  System.SysUtils;

{ Gerar UUID no Delphi para MySQL < 8.0 }
LQuery.ParamByName('id').AsString := TGUID.NewGuid.ToString;
```

## Partitioning

```sql
-- Particionamento por RANGE
CREATE TABLE orders (
  id          INT AUTO_INCREMENT,
  customer_id INT NOT NULL,
  order_date  DATE NOT NULL,
  total       DECIMAL(15,2),
  PRIMARY KEY (id, order_date)
) ENGINE=InnoDB
PARTITION BY RANGE (YEAR(order_date)) (
  PARTITION p2024 VALUES LESS THAN (2025),
  PARTITION p2025 VALUES LESS THAN (2026),
  PARTITION p2026 VALUES LESS THAN (2027),
  PARTITION pmax  VALUES LESS THAN MAXVALUE
);
```

## Key Differences: MySQL vs Firebird vs PostgreSQL

| Feature | MySQL | Firebird | PostgreSQL |
|---------|-------|----------|------------|
| Auto-increment | `AUTO_INCREMENT` | Generator + BI Trigger | `SERIAL` / `IDENTITY` |
| Get generated ID | `LAST_INSERT_ID()` | `RETURNING id` | `RETURNING id` |
| UPSERT | `ON DUPLICATE KEY UPDATE` | Non-native (partial FB5) | `ON CONFLICT` |
| JSON | `JSON` (5.7+) | Non-native | `JSONB` (indexable) |
| Full-Text Search | `FULLTEXT` index | Non-native | `tsvector` |
| ENUM | `ENUM(...)` native | Domain + CHECK | `CREATE TYPE` |
| Embedded | No | Yes (fbclient.dll) | No |
| Engine Choice | InnoDB, MyISAM, etc. | Single engine | Single engine |
| Recommended Charset | `utf8mb4` | `UTF8` | `UTF8` |
| FireDAC Driver | `MySQL` | `FB` | `PG` |
| Client Library | `libmysql.dll` | `fbclient.dll` | `libpq.dll` |
| Default Isolation | Repeatable Read | Read Committed | Read Committed |
| StoredProcs | `CALL sp()` | `EXECUTE PROCEDURE` | `CALL sp()` (PG 11+) |
| Windows Functions | 8.0+ | 3.0+ (basic) | Ample |
| CTEs | 8.0+ | 3.0+ | All versions |

## MySQL Anti-Patterns to Avoid

```pascal
// ❌ Concatenar SQL
LQuery.SQL.Text := 'SELECT * FROM customers WHERE name = ''' + AName + '''';

// ✅ Parâmetros parametrizados
LQuery.SQL.Text := 'SELECT * FROM customers WHERE name = :name';
LQuery.ParamByName('name').AsString := AName;

// ❌ Usar utf8 (3 bytes, not suporta emoji)
Result.Params.Values['CharacterSet'] := 'utf8';

// ✅ Usar utf8mb4 (4 bytes, suporte completo)
Result.Params.Values['CharacterSet'] := 'utf8mb4';

// ❌ Tentar usar RETURNING (not existe no MySQL!)
LQuery.SQL.Text := 'INSERT INTO ... RETURNING id';

// ✅ Usar LAST_INSERT_ID()
LQuery.ExecSQL;
LQuery.SQL.Text := 'SELECT LAST_INSERT_ID()';
LQuery.Open;

// ❌ Usar MyISAM para tabelas novas
CREATE TABLE t (...) ENGINE=MyISAM;

// ✅ Usar InnoDB sempre
CREATE TABLE t (...) ENGINE=InnoDB;

// ❌ SELECT * sem LIMIT
LQuery.SQL.Text := 'SELECT * FROM orders';

// ✅ LIMIT para paginaction
LQuery.SQL.Text := 'SELECT id, customer_id, total FROM orders LIMIT :limit OFFSET :offset';

// ❌ Ignorar índices em colunas de WHERE/JOIN
// ✅ Criar índices para colunas usadas em filtros
```

## MySQL Checklist

- [ ] Driver `MySQL` configured on FireDAC?
- [ ] `CharacterSet := 'utf8mb4'` (NOT `utf8`)?
- [ ] `libmysql.dll` (32/64-bit) in PATH or `VendorLib`?
- [ ] Tables created with `ENGINE=InnoDB`?
- [ ] `AUTO_INCREMENT` in PKs with `LAST_INSERT_ID()` in Delphi?
- [ ] Parameterized queries (without concatenation)?
- [ ] Explicit transactions for compound operations?
- [ ] Errors handled via `EFDDBEngineException.Kind`?
- [ ] Indexes created for columns in WHERE and JOIN?
- [ ] Foreign Keys with appropriate `ON DELETE`/`ON UPDATE`?
- [ ] `COLLATE utf8mb4_unicode_ci` in the tables for correct comparison?
- [ ] `information_schema` to check metadata?
