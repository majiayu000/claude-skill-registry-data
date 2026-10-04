---
name: "Firebird Database"
description: "Development patterns with Firebird database via FireDAC — connection, PSQL, generators, transactions, migrations"
---

# Firebird Database — Skill

Use this skill when working with Firebird database in Delphi projects via FireDAC.

## When to Use

- When configuring FireDAC connection with Firebird
- When creating tables, generators, stored procedures, triggers, domains and views
- When implementing Repositories with FireDAC + Firebird
- When working with transactions, isolation levels and concurrency
- When planning schema migrations (versioned scripts)
- When optimizing queries and indexes for Firebird

## Firebird Versions

| Version | Relevant News |
|--------|----------------------|
| **2.5** | Trace API, `LIST()` aggregate, Windows Trusted Auth |
| **3.0** | Native `BOOLEAN`, `IDENTITY` columns, Packages, UDR (replaces UDF), Window Functions (`OVER`), Encryption |
| **4.0** | `DECFLOAT`, `INT128`, `TIME/TIMESTAMP WITH TIME ZONE`, Replication, Batch API, `LATERAL` join |
| **5.0** | `WHEN NOT MATCHED BY SOURCE`, Parallel Backup, SQL Security hardening, Profiler |

> **Recommendation:** Use Firebird 3.0+ for new projects. Avoid deprecated features like UDFs.

## FireDAC connection with Firebird

### Minimum Configuration

```pascal
unit MeuApp.Infra.Database.Connection;

interface

uses
  FireDAC.Comp.Client,
  FireDAC.Phys.FB,        //Driver Firebird
  FireDAC.Phys.FBDef,     //Defaults do Firebird
  FireDAC.Stan.Def,
  FireDAC.Stan.Pool,
  FireDAC.DApt;

type
  ///<summary>
  ///Firebird connection factory via FireDAC.
  ///</summary>
  TFirebirdConnectionFactory = class
  public
    ///<summary>
    ///Creates and configures a Firebird connection.
    ///</summary>
    ///<param name="ADatabasePath">Full path of the .fdb file</param>
    ///<param name="AUserName">User (default: SYSDBA)</param>
    ///<param name="APassword">Bank password</param>
    ///<returns>FireDAC connection configured and opened</returns>
    class function CreateConnection(
      const ADatabasePath: string;
      const AUserName: string = 'SYSDBA';
      const APassword: string = 'masterkey'
    ): TFDConnection;

    ///<summary>
    ///Creates a connection via Embedded Server (without fbserver).
    ///</summary>
    class function CreateEmbeddedConnection(
      const ADatabasePath: string
    ): TFDConnection;
  end;

implementation

uses
  System.SysUtils;

class function TFirebirdConnectionFactory.CreateConnection(
  const ADatabasePath: string;
  const AUserName: string;
  const APassword: string): TFDConnection;
begin
  if ADatabasePath.Trim.IsEmpty then
    raise EArgumentException.Create('ADatabasePath não pode ser vazio');

  Result := TFDConnection.Create(nil);
  try
    Result.DriverName := 'FB';
    Result.Params.Database := ADatabasePath;
    Result.Params.UserName := AUserName;
    Result.Params.Password := APassword;

    { Configurações recomendadas }
    Result.Params.Values['CharacterSet'] := 'UTF8';
    Result.Params.Values['Protocol'] := 'TCPIP';     // Local: 'Local'
    Result.Params.Values['Server'] := 'localhost';
    Result.Params.Values['Port'] := '3050';
    Result.Params.Values['SQLDialect'] := '3';        //ALWAYS Dialect 3
    Result.Params.Values['PageSize'] := '16384';      // 16KB recomendado

    { Opções do driver FireDAC }
    Result.FormatOptions.StrsTrim2Len := True;         //Trim CHAR for VARCHAR
    Result.FetchOptions.Mode := fmAll;                 // Fetch completo
    Result.ResourceOptions.AutoReconnect := True;      //Automatic reconnection
    Result.TxOptions.Isolation := xiReadCommitted;     //Standard isolation

    Result.Connected := True;
  except
    Result.Free;
    raise;
  end;
end;

class function TFirebirdConnectionFactory.CreateEmbeddedConnection(
  const ADatabasePath: string): TFDConnection;
begin
  Result := TFDConnection.Create(nil);
  try
    Result.DriverName := 'FB';
    Result.Params.Database := ADatabasePath;

    { Embedded: sem servidor, sem user/password obrigatórios no FB3+ }
    Result.Params.Values['Protocol'] := 'Local';
    Result.Params.Values['CharacterSet'] := 'UTF8';
    Result.Params.Values['SQLDialect'] := '3';

    Result.Connected := True;
  except
    Result.Free;
    raise;
  end;
end;
```

### FDPhysFBDriverLink — Configure Client Library

```pascal
uses
  FireDAC.Phys.FBWrapper,
  FireDAC.Phys.FB;

var
  LDriverLink: TFDPhysFBDriverLink;
begin
  LDriverLink := TFDPhysFBDriverLink.Create(nil);
  try
    { Apontar fbclient.dll customizado (32/64-bit) }
    LDriverLink.VendorLib := 'C:\Firebird\fbclient.dll';

    { Embedded: usar fbclient.dll local ao .exe }
    //LDriverLink.VendorLib := ExtractFilePath(ParamStr(0)) + 'fbclient.dll';
  finally
    { DriverLink geralmente vive por toda a aplicação — criar no DataModule }
  end;
end;
```

### Connection Pooling

```pascal
{ No FDManager ou no Connection Definition }
FDManager.ConnectionDefs.AddConnectionDef;
with FDManager.ConnectionDefs.ConnectionDefByName('FB_POOL') do
begin
  DriverID := 'FB';
  Database := 'C:\Data\MeuBanco.fdb';
  UserName := 'SYSDBA';
  Password := 'masterkey';
  Params.Values['CharacterSet'] := 'UTF8';
  Params.Values['Pooled'] := 'True';
  Params.Values['POOL_MaximumItems'] := '50';
  Params.Values['POOL_CleanupTimeout'] := '30000';
  Params.Values['POOL_ExpireTimeout'] := '90000';
end;
```

## Dialects — ALWAYS Dialect 3

| Feature | Dialect 1 | Dialect 3 |
|---------|-----------|-----------|
| `DATE` | Includes time | Date only (use `TIMESTAMP` for date+time) |
| `"Identificadores"` | Syntax error | Allows case-sensitive names with double quotes |
| Numerical precision | `DOUBLE PRECISION` | `NUMERIC(18, x)` up to 18 digits |
| Recommendation | ❌ Legacy | ✅ **Mandatory for new projects** |

> ⚠️ **Rule:** Always `SQLDialect := 3`. Dialect 1 is legacy from InterBase and causes ambiguities with `DATE`.

## Data Types — Firebird Mapping ↔ Delphi

| Firebird | Delphi (FireDAC) | Note |
|----------|------------------|------------|
| `INTEGER` | `ftInteger` / `AsInteger` | 32-bit |
| `BIGINT` | `ftLargeint` / `AsLargeInt` | 64-bit |
| `SMALLINT` | `ftSmallint` / `AsSmallInt` | 16-bit |
| `VARCHAR(N)` | `ftString` / `AsString` | Use with `CHARACTER SET UTF8` |
| `CHAR(N)` | `ftFixedChar` | Fill with spaces — prefer `VARCHAR` |
| `NUMERIC(P,S)` | `ftBCD` / `AsCurrency` | Monetary values ​​|
| `DOUBLE PRECISION`| `ftFloat` / `AsFloat` | Ponto flutuante |
| `DATE` | `ftDate` / `AsDateTime` | Date only (Dialect 3) |
| `TIME` | `ftTime` / `AsDateTime` | Just in time |
| `TIMESTAMP` | `ftDateTime` / `AsDateTime` | Data + Hora |
| `BOOLEAN` (FB3+) | `ftBoolean` / `AsBoolean` | `TRUE`/`FALSE` native |
| `BLOB SUB_TYPE TEXT` | `ftMemo` / `AsString` | Texto grande (CLOB) |
| `BLOB SUB_TYPE 0` | `ftBlob` / `AsBytes` | Binary data |

## Generators (Sequences)

### Create Generator

```sql
/* Generator clássico (todas as versões) */
CREATE GENERATOR GEN_CUSTOMER_ID;

/* Sequence (Firebird 3+, mais moderno) */
CREATE SEQUENCE SEQ_CUSTOMER_ID;
```

### Get Next Value in Delphi

```pascal
///<summary>
///Gets the next value from a Firebird generator.
///</summary>
function GetNextGeneratorValue(
  AConnection: TFDConnection;
  const AGeneratorName: string): Int64;
var
  LQuery: TFDQuery;
begin
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := AConnection;
    LQuery.SQL.Text := 'SELECT GEN_ID(' + AGeneratorName + ', 1) FROM RDB$DATABASE';
    LQuery.Open;
    Result := LQuery.Fields[0].AsLargeInt;
  finally
    LQuery.Free;
  end;
end;

///<summary>
///Modern alternative with NEXT VALUE FOR (Firebird 3+).
///</summary>
function GetNextSequenceValue(
  AConnection: TFDConnection;
  const ASequenceName: string): Int64;
var
  LQuery: TFDQuery;
begin
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := AConnection;
    LQuery.SQL.Text := 'SELECT NEXT VALUE FOR ' + ASequenceName + ' FROM RDB$DATABASE';
    LQuery.Open;
    Result := LQuery.Fields[0].AsLargeInt;
  finally
    LQuery.Free;
  end;
end;
```

### IDENTITY Columns (Firebird 3+)

```sql
/* Auto-increment nativo — dispensa generator manual */
CREATE TABLE customers (
  id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

/* Para pegar o ID gerado após INSERT: */
INSERT INTO customers (name) VALUES ('João') RETURNING id;
```

### RETURNING in Delphi (get ID after Insert)

```pascal
procedure TFirebirdCustomerRepository.Insert(ACustomer: TCustomer);
var
  LQuery: TFDQuery;
begin
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := FConnection;
    LQuery.SQL.Text :=
      'INSERT INTO customers (name, cpf, email) ' +
      'VALUES (:name, :cpf, :email) RETURNING id';
    LQuery.ParamByName('name').AsString := ACustomer.Name;
    LQuery.ParamByName('cpf').AsString := ACustomer.Cpf;
    LQuery.ParamByName('email').AsString := ACustomer.Email;
    LQuery.Open; { Open, não ExecSQL — pois RETURNING retorna dados }
    ACustomer.Id := LQuery.Fields[0].AsInteger;
  finally
    LQuery.Free;
  end;
end;
```

## Stored Procedures in Firebird

### Selectable (returns resultset — uses SUSPEND)

```sql
CREATE OR ALTER PROCEDURE SP_CUSTOMERS_BY_STATUS (
  P_STATUS SMALLINT
)
RETURNS (
  O_ID       INTEGER,
  O_NAME     VARCHAR(100),
  O_CPF      VARCHAR(14),
  O_STATUS   SMALLINT
)
AS
BEGIN
  FOR SELECT id, name, cpf, status
      FROM customers
      WHERE status = :P_STATUS
      INTO :O_ID, :O_NAME, :O_CPF, :O_STATUS
  DO
    SUSPEND;  /* Retorna cada linha (como um cursor) */
END
```

**Call in Delphi (treated as SELECT):**

```pascal
LQuery.SQL.Text := 'SELECT * FROM SP_CUSTOMERS_BY_STATUS(:P_STATUS)';
LQuery.ParamByName('P_STATUS').AsSmallInt := Ord(csActive);
LQuery.Open;
```

### Executable (performs action — does not use SUSPEND)

```sql
CREATE OR ALTER PROCEDURE SP_DEACTIVATE_CUSTOMER (
  P_CUSTOMER_ID INTEGER
)
AS
BEGIN
  UPDATE customers SET status = 1 WHERE id = :P_CUSTOMER_ID;
END
```

**Call in Delphi:**

```pascal
LQuery.SQL.Text := 'EXECUTE PROCEDURE SP_DEACTIVATE_CUSTOMER(:P_CUSTOMER_ID)';
LQuery.ParamByName('P_CUSTOMER_ID').AsInteger := ACustomerId;
LQuery.ExecSQL;
```

## Execute Block (Anonymous SQL with PSQL)

```sql
/* Útil para lotes e scripts sem criar procedure permanente */
EXECUTE BLOCK (P_LIMIT INTEGER = :P_LIMIT)
RETURNS (O_NAME VARCHAR(100), O_TOTAL INTEGER)
AS
BEGIN
  FOR SELECT name, COUNT(*) FROM orders
      GROUP BY name
      HAVING COUNT(*) > :P_LIMIT
      INTO :O_NAME, :O_TOTAL
  DO
    SUSPEND;
END
```

## Domains (Reusable Types)

```sql
/* Domínios centralizam validações e tipos no schema */
CREATE DOMAIN DM_ID        AS INTEGER NOT NULL;
CREATE DOMAIN DM_NAME      AS VARCHAR(100) NOT NULL;
CREATE DOMAIN DM_CPF       AS VARCHAR(14);
CREATE DOMAIN DM_EMAIL     AS VARCHAR(150);
CREATE DOMAIN DM_MONEY     AS NUMERIC(15, 2) DEFAULT 0;
CREATE DOMAIN DM_STATUS    AS SMALLINT DEFAULT 0 CHECK (VALUE IN (0, 1, 2));
CREATE DOMAIN DM_BOOLEAN   AS SMALLINT DEFAULT 0 CHECK (VALUE IN (0, 1)); /* Firebird 2.5 */
/* Firebird 3+: usar BOOLEAN nativo em vez de DM_BOOLEAN */

CREATE TABLE customers (
  id     DM_ID,
  name   DM_NAME,
  cpf    DM_CPF,
  email  DM_EMAIL,
  status DM_STATUS,
  PRIMARY KEY (id)
);
```

##Triggers

```sql
/* Trigger para auto-increment com Generator */
CREATE OR ALTER TRIGGER TRG_CUSTOMER_BI FOR customers
  ACTIVE BEFORE INSERT POSITION 0
AS
BEGIN
  IF (NEW.id IS NULL OR NEW.id = 0) THEN
    NEW.id = GEN_ID(GEN_CUSTOMER_ID, 1);
END

/* Trigger de auditoria */
CREATE OR ALTER TRIGGER TRG_CUSTOMER_AU FOR customers
  ACTIVE AFTER UPDATE POSITION 0
AS
BEGIN
  INSERT INTO audit_log (table_name, record_id, action, changed_at)
    VALUES ('customers', NEW.id, 'UPDATE', CURRENT_TIMESTAMP);
END
```

## Transactions and Isolation Levels

### Isolation Levels in Firebird

| Level | FireDAC | Usage |
|-------|---------|-----|
| **Read Committed** | `xiReadCommitted` | ✅ Standard — reads committed data, without dirty reads |
| **Snapshot** (Concurrency) | `xiSnapshot` | Reports — consistent view of START momentum |
| **Snapshot Table Stability** | `xiSerializable` | Rare — exclusive lock on table |

### Manual Transaction Control

```pascal
///<summary>
///Performs operation within explicit transaction.
///</summary>
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

{ Uso }
ExecuteInTransaction(FConnection,
  procedure
  begin
    FCustomerRepo.Insert(LCustomer);
    FOrderRepo.Insert(LOrder);
    FStockRepo.DecreaseStock(LOrder.Items);
  end
);
```

### Transaction with Specific Isolation Level

```pascal
var
  LTransaction: TFDTransaction;
begin
  LTransaction := TFDTransaction.Create(nil);
  try
    LTransaction.Connection := FConnection;
    LTransaction.Options.Isolation := xiSnapshot; { Leitura consistente }
    LTransaction.Options.ReadOnly := True;
    LTransaction.StartTransaction;
    try
      { Queries de relatório aqui — snapshot imutável }
      LTransaction.Commit;
    except
      LTransaction.Rollback;
      raise;
    end;
  finally
    LTransaction.Free;
  end;
end;
```

## Event Alerter (Bank Events)

```sql
/* No Firebird: */
CREATE OR ALTER TRIGGER TRG_ORDER_NOTIFY FOR orders
  ACTIVE AFTER INSERT POSITION 0
AS
BEGIN
  POST_EVENT 'NEW_ORDER';
END
```

```pascal
{ No Delphi: escutar eventos do banco }
uses
  FireDAC.Phys.FB; //TFDPhysFBEventAlerts

var
  LAlerter: TFDEventAlerter;
begin
  LAlerter := TFDEventAlerter.Create(nil);
  try
    LAlerter.Connection := FConnection;
    LAlerter.Names.Text := 'NEW_ORDER';
    LAlerter.Options.Timeout := 0;  { Sem timeout — espera indefinidamente }
    LAlerter.OnAlert := HandleNewOrderEvent;
    LAlerter.Active := True;
  finally
    { Manter vivo enquanto a aplicação rodar — liberação no Destroy }
  end;
end;

procedure TMyService.HandleNewOrderEvent(ASender: TFDCustomEventAlerter;
  const AEventName: string; const AArgument: Variant);
begin
  if AEventName = 'NEW_ORDER' then
    RefreshOrderList;
end;
```

## Schema Creation — Migration Script

```sql
/* migration_001_initial_schema.sql */

/* ===== Domains ===== */
CREATE DOMAIN DM_ID       AS INTEGER NOT NULL;
CREATE DOMAIN DM_NAME     AS VARCHAR(100) NOT NULL;
CREATE DOMAIN DM_CPF      AS VARCHAR(14);
CREATE DOMAIN DM_EMAIL    AS VARCHAR(150);
CREATE DOMAIN DM_MONEY    AS NUMERIC(15,2) DEFAULT 0 NOT NULL;
CREATE DOMAIN DM_STATUS   AS SMALLINT DEFAULT 0 CHECK (VALUE BETWEEN 0 AND 2);
CREATE DOMAIN DM_MEMO     AS BLOB SUB_TYPE TEXT SEGMENT SIZE 4096;

/* ===== Generators ===== */
CREATE GENERATOR GEN_CUSTOMER_ID;
CREATE GENERATOR GEN_PRODUCT_ID;
CREATE GENERATOR GEN_ORDER_ID;
CREATE GENERATOR GEN_ORDER_ITEM_ID;

/* ===== Tables ===== */
CREATE TABLE customers (
  id       DM_ID,
  name     DM_NAME,
  cpf      DM_CPF,
  email    DM_EMAIL,
  status   DM_STATUS,
  notes    DM_MEMO,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT PK_CUSTOMER PRIMARY KEY (id),
  CONSTRAINT UQ_CUSTOMER_CPF UNIQUE (cpf)
);

CREATE TABLE products (
  id         DM_ID,
  name       DM_NAME,
  price      DM_MONEY,
  stock_qty  INTEGER DEFAULT 0 NOT NULL,
  status     DM_STATUS,
  CONSTRAINT PK_PRODUCT PRIMARY KEY (id)
);

CREATE TABLE orders (
  id            DM_ID,
  customer_id   INTEGER NOT NULL,
  order_date    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  total_amount  DM_MONEY,
  status        DM_STATUS,
  CONSTRAINT PK_ORDER PRIMARY KEY (id),
  CONSTRAINT FK_ORDER_CUSTOMER FOREIGN KEY (customer_id)
    REFERENCES customers (id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE order_items (
  id          DM_ID,
  order_id    INTEGER NOT NULL,
  product_id  INTEGER NOT NULL,
  quantity    INTEGER NOT NULL CHECK (quantity > 0),
  unit_price  DM_MONEY,
  total_price DM_MONEY,
  CONSTRAINT PK_ORDER_ITEM PRIMARY KEY (id),
  CONSTRAINT FK_ITEM_ORDER FOREIGN KEY (order_id)
    REFERENCES orders (id) ON DELETE CASCADE,
  CONSTRAINT FK_ITEM_PRODUCT FOREIGN KEY (product_id)
    REFERENCES products (id) ON DELETE RESTRICT
);

/* ===== Indices ===== */
CREATE INDEX IDX_CUSTOMER_NAME    ON customers (name);
CREATE INDEX IDX_ORDER_DATE       ON orders (order_date);
CREATE INDEX IDX_ORDER_CUSTOMER   ON orders (customer_id);
CREATE INDEX IDX_ITEM_ORDER       ON order_items (order_id);

/* ===== Triggers (Auto-Increment) ===== */
SET TERM ^;

CREATE TRIGGER TRG_CUSTOMER_BI FOR customers
  ACTIVE BEFORE INSERT POSITION 0
AS
BEGIN
  IF (NEW.id IS NULL OR NEW.id = 0) THEN
    NEW.id = GEN_ID(GEN_CUSTOMER_ID, 1);
END^

CREATE TRIGGER TRG_PRODUCT_BI FOR products
  ACTIVE BEFORE INSERT POSITION 0
AS
BEGIN
  IF (NEW.id IS NULL OR NEW.id = 0) THEN
    NEW.id = GEN_ID(GEN_PRODUCT_ID, 1);
END^

CREATE TRIGGER TRG_ORDER_BI FOR orders
  ACTIVE BEFORE INSERT POSITION 0
AS
BEGIN
  IF (NEW.id IS NULL OR NEW.id = 0) THEN
    NEW.id = GEN_ID(GEN_ORDER_ID, 1);
END^

CREATE TRIGGER TRG_ORDER_ITEM_BI FOR order_items
  ACTIVE BEFORE INSERT POSITION 0
AS
BEGIN
  IF (NEW.id IS NULL OR NEW.id = 0) THEN
    NEW.id = GEN_ID(GEN_ORDER_ITEM_ID, 1);
END^

SET TERM ;^
```

## Schema migration in Delphi

```pascal
///<summary>
///Schema version control via migration table.
///</summary>
procedure EnsureMigrationTable(AConnection: TFDConnection);
begin
  AConnection.ExecSQL(
    'CREATE TABLE IF NOT EXISTS (SELECT 1 FROM RDB$RELATIONS ' +
    'WHERE RDB$RELATION_NAME = ''SCHEMA_MIGRATIONS'') ' +
    '/* Alternativa segura: */'
  );
  { No Firebird, CREATE TABLE IF NOT EXISTS não existe nativamente.
    Verificar via metadata: }
  if not TableExists(AConnection, 'SCHEMA_MIGRATIONS') then
    AConnection.ExecSQL(
      'CREATE TABLE SCHEMA_MIGRATIONS (' +
      '  version INTEGER NOT NULL PRIMARY KEY,' +
      '  description VARCHAR(200),' +
      '  applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP' +
      ')'
    );
end;

function TableExists(AConnection: TFDConnection; const ATableName: string): Boolean;
var
  LQuery: TFDQuery;
begin
  LQuery := TFDQuery.Create(nil);
  try
    LQuery.Connection := AConnection;
    LQuery.SQL.Text :=
      'SELECT COUNT(*) FROM RDB$RELATIONS ' +
      'WHERE RDB$RELATION_NAME = :name AND RDB$SYSTEM_FLAG = 0';
    LQuery.ParamByName('name').AsString := ATableName.ToUpper;
    LQuery.Open;
    Result := LQuery.Fields[0].AsInteger > 0;
  finally
    LQuery.Free;
  end;
end;
```

## Backup and Restore via GBak (Command Line)

```bash
# Backup
gbak -b -v -user SYSDBA -password masterkey localhost:C:\Data\MeuBanco.fdb C:\Backup\MeuBanco.fbk

# Restore
gbak -c -v -page_size 16384 -user SYSDBA -password masterkey C:\Backup\MeuBanco.fbk localhost:C:\Data\MeuBanco_Restored.fdb

# Backup via Services API (no local path)
gbak -b -se localhost:service_mgr C:\Data\MeuBanco.fdb C:\Backup\MeuBanco.fbk -user SYSDBA -password masterkey
```

## Firebird Anti-Patterns to Avoid

```pascal
//❌ Dialect 1 — ambiguity with DATE
Result.Params.Values['SQLDialect'] := '1';

//✅ Dialect 3 — ALWAYS
Result.Params.Values['SQLDialect'] := '3';

//❌ Concatenar SQL — SQL Injection
LQuery.SQL.Text := 'SELECT * FROM customers WHERE name = ''' + AName + '''';

//✅ Parameterized parameters
LQuery.SQL.Text := 'SELECT * FROM customers WHERE name = :name';
LQuery.ParamByName('name').AsString := AName;

//❌ Ignore CharacterSet — problems with accents
Result.DriverName := 'FB';
Result.Params.Database := APath;
Result.Connected := True;  //Sem CharacterSet!

//✅ Always set CharacterSet
Result.Params.Values['CharacterSet'] := 'UTF8';

//❌ ExecSQL with RETURNING — returns nothing!
LQuery.SQL.Text := 'INSERT INTO ... RETURNING id';
LQuery.ExecSQL;  //go LOST!

//✅ Open with RETURNING — returns the resultset
LQuery.SQL.Text := 'INSERT INTO ... RETURNING id';
LQuery.Open;  //id available in Fields[0]
ACustomer.Id := LQuery.Fields[0].AsInteger;

//❌ Create database without appropriate Page Size
CREATE DATABASE '...' PAGE_SIZE 4096;  //Too small for large tables

//✅ Optimized Page Size
CREATE DATABASE '...' PAGE_SIZE 16384 DEFAULT CHARACTER SET UTF8;

//❌ Do not treat deadlocks
LQuery.ExecSQL;  //can cause deadlock in competition

//✅ Tratar deadlocks com retry
try
  LQuery.ExecSQL;
except
  on E: EFDDBEngineException do
  begin
    if E.Kind = ekRecordLocked then
      raise EConflictException.Create('Registro bloqueado por outra transação')
    else
      raise;
  end;
end;
```

## Packages (Firebird 3+)

```sql
/* Packages agrupam procedures e functions relacionadas */

/* Header (interface) */
CREATE OR ALTER PACKAGE PKG_CUSTOMER
AS
BEGIN
  PROCEDURE DEACTIVATE(P_ID INTEGER);
  FUNCTION GET_FULL_NAME(P_ID INTEGER) RETURNS VARCHAR(200);
END

/* Body (implementation) */
CREATE OR ALTER PACKAGE BODY PKG_CUSTOMER
AS
BEGIN
  PROCEDURE DEACTIVATE(P_ID INTEGER)
  AS
  BEGIN
    UPDATE customers SET status = 1 WHERE id = :P_ID;
  END

  FUNCTION GET_FULL_NAME(P_ID INTEGER) RETURNS VARCHAR(200)
  AS
    DECLARE VARIABLE V_NAME VARCHAR(200);
  BEGIN
    SELECT name FROM customers WHERE id = :P_ID INTO :V_NAME;
    RETURN V_NAME;
  END
END
```

**Call in Delphi:**

```pascal
LQuery.SQL.Text := 'EXECUTE PROCEDURE PKG_CUSTOMER.DEACTIVATE(:ID)';
LQuery.ParamByName('ID').AsInteger := ACustomerId;
LQuery.ExecSQL;

{ Function }
LQuery.SQL.Text := 'SELECT PKG_CUSTOMER.GET_FULL_NAME(:ID) FROM RDB$DATABASE';
LQuery.ParamByName('ID').AsInteger := ACustomerId;
LQuery.Open;
LFullName := LQuery.Fields[0].AsString;
```

## Integration Testing with Firebird Embedded

```pascal
[TestFixture]
TCustomerRepositoryFirebirdTest = class
private
  FConnection: TFDConnection;
  FDriverLink: TFDPhysFBDriverLink;
  FRepository: ICustomerRepository;
  FTestDbPath: string;
public
  [Setup]
  procedure Setup;

  [TearDown]
  procedure TearDown;

  [Test]
  procedure Insert_ValidCustomer_ShouldReturnGeneratedId;
end;

procedure TCustomerRepositoryFirebirdTest.Setup;
begin
  FTestDbPath := TPath.Combine(TPath.GetTempPath, 'test_' + TGUID.NewGuid.ToString + '.fdb');

  { Configurar driver embedded }
  FDriverLink := TFDPhysFBDriverLink.Create(nil);
  FDriverLink.VendorLib := 'fbclient.dll'; { Embedded no path da aplicação }

  { Criar banco de teste }
  FConnection := TFDConnection.Create(nil);
  FConnection.DriverName := 'FB';
  FConnection.Params.Database := FTestDbPath;
  FConnection.Params.UserName := 'SYSDBA';
  FConnection.Params.Password := 'masterkey';
  FConnection.Params.Values['Protocol'] := 'Local';
  FConnection.Params.Values['CharacterSet'] := 'UTF8';
  FConnection.Params.Values['CreateDatabase'] := 'Yes';  { Cria o .fdb automaticamente }
  FConnection.Connected := True;

  { Criar schema de teste }
  FConnection.ExecSQL('CREATE TABLE customers (id INTEGER PRIMARY KEY, name VARCHAR(100))');
  FConnection.ExecSQL('CREATE GENERATOR GEN_CUSTOMER_ID');

  FRepository := TFirebirdCustomerRepository.Create(FConnection);
end;

procedure TCustomerRepositoryFirebirdTest.TearDown;
begin
  FConnection.Connected := False;
  FConnection.Free;
  FDriverLink.Free;

  { Limpar banco temporário }
  if TFile.Exists(FTestDbPath) then
    TFile.Delete(FTestDbPath);
end;
```

## Firebird Checklist

- [ ] Dialect 3 configured (`SQLDialect := '3'`)?
- [ ] CharacterSet UTF8 defined?
- [ ] Page Size ≥ 8192 (ideal: 16384)?
- [ ] Parameterized queries (without string concatenation)?
- [ ] Generators/Sequences for auto-increment with BI trigger?
- [ ] `RETURNING` with `Open` (not `ExecSQL`)?
- [ ] Explicit transactions for compound operations?
- [ ] Deadlocks treated with `EFDDBEngineException.Kind = ekRecordLocked`?
- [ ] Correct FBClient.dll (32/64-bit) configured in VendorLib?
- [ ] Indexes created for columns used in WHERE and JOIN?
- [ ] Foreign Keys with appropriate `ON DELETE`/`ON UPDATE`?
- [ ] Regular backup via `gbak`?
- [ ] Versioned migration scripts?
