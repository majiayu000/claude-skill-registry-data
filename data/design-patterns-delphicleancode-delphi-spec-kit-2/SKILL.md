---
name: "Design Patterns GoF — Delphi"
description: "Implementation of the 23 GoF (Gang of Four) patterns in Object Pascal / Delphi with interfaces, TInterfacedObject and SOLID principles. Covers Creational, Structural and Behavioral patterns."
---

# Design Patterns GoF in Delphi — Skill

Use this skill when the user requests implementation of design patterns in Delphi. Always apply together with naming conventions (T/I/E/F/A/L) and memory management (try..finally).

## When to Use

- Create `Factory`, `Abstract Factory` or `Builder` for creating complex objects
- Implement `Strategy` to vary algorithms (calculation of freight, taxes, export)
- Use `Observer` for decoupled notifications (Domain Events)
- Apply `Command` for undo/redo, job queues or auditing
- Use `Decorator` to add responsibilities without inheritance
- Implement `Adapter` for integration with legacy systems
- Use `Facade` to simplify complex subsystems (e.g. NFe emission)
- Apply `Template Method` to algorithms with variations (reports, exports)
- Use `State` for behavior that changes depending on the state of the object
- Use `Chain of Responsibility` for validation or processing pipelines

---

## 🏗️ Creational Patterns

### Singleton — Global Configuration

```pascal
unit MeuApp.Infra.AppConfig;

interface

type
  TAppConfig = class
  private
    class var FInstance: TAppConfig;
    FDatabaseUrl: string;
    FApiKey: string;
    constructor Create;
  public
    class function GetInstance: TAppConfig;
    class procedure ReleaseInstance;
    property DatabaseUrl: string read FDatabaseUrl write FDatabaseUrl;
    property ApiKey: string read FApiKey write FApiKey;
  end;

implementation

constructor TAppConfig.Create;
begin
  inherited Create;
  FDatabaseUrl := 'localhost:5432/myapp';
end;

class function TAppConfig.GetInstance: TAppConfig;
begin
  if not Assigned(FInstance) then
    FInstance := TAppConfig.Create;
  Result := FInstance;
end;

class procedure TAppConfig.ReleaseInstance;
begin
  FreeAndNil(FInstance);
end;

initialization
finalization
  TAppConfig.ReleaseInstance;
end.
```

### Factory Method — Creation with Polymorphism

```pascal
unit MeuApp.Domain.Report.Factory;

interface

uses
  MeuApp.Domain.Report.Intf;

type
  IReportExporter = interface
    ['{A1B2-...}']
    procedure Export(const AData: TReportData; const AFilePath: string);
  end;

  // Factory Method — cada subclasse decide qual exportador criar
  TReportExporterFactory = class abstract
  public
    function CreateExporter: IReportExporter; virtual; abstract;
    // Template Method usando Factory Method
    procedure ExportReport(const AData: TReportData; const AFilePath: string);
  end;

  TPdfReportFactory = class(TReportExporterFactory)
    function CreateExporter: IReportExporter; override;
  end;

  TExcelReportFactory = class(TReportExporterFactory)
    function CreateExporter: IReportExporter; override;
  end;

implementation

procedure TReportExporterFactory.ExportReport(const AData: TReportData; const AFilePath: string);
var
  LExporter: IReportExporter;
begin
  LExporter := CreateExporter;
  LExporter.Export(AData, AFilePath);
end;
```

### Abstract Factory — Family of Related Objects

```pascal
unit MeuApp.Infra.UI.Factory;

interface

type
  IButton = interface ['{...}'] procedure Render; end;
  IInputField = interface ['{...}'] procedure Render; end;
  IDialog = interface ['{...}'] procedure Show(const AMsg: string); end;

  // Abstract Factory
  IUIComponentFactory = interface
    ['{B2C3-...}']
    function CreateButton(const ACaption: string): IButton;
    function CreateInputField(const APlaceholder: string): IInputField;
    function CreateDialog: IDialog;
  end;

  TVCLComponentFactory = class(TInterfacedObject, IUIComponentFactory)
    function CreateButton(const ACaption: string): IButton;
    function CreateInputField(const APlaceholder: string): IInputField;
    function CreateDialog: IDialog;
  end;

  TFMXComponentFactory = class(TInterfacedObject, IUIComponentFactory)
    function CreateButton(const ACaption: string): IButton;
    function CreateInputField(const APlaceholder: string): IInputField;
    function CreateDialog: IDialog;
  end;
```

### Builder — Step by Step Construction

```pascal
unit MeuApp.Infra.Query.Builder;

interface

uses
  System.SysUtils,
  System.Classes,
  System.Generics.Collections;

type
  /// <summary>
  ///   Builder para construção fluente de queries SQL parametrizadas.
  /// </summary>
  TQueryBuilder = class
  private
    FSelect: string;
    FFrom: string;
    FWheres: TStringList;
    FOrderBy: string;
    FLimit: Integer;
  public
    constructor Create;
    destructor Destroy; override;

    function Select(const AFields: string): TQueryBuilder;
    function From(const ATable: string): TQueryBuilder;
    function Where(const ACondition: string): TQueryBuilder;
    function OrderBy(const AField: string; ADesc: Boolean = False): TQueryBuilder;
    function Limit(ACount: Integer): TQueryBuilder;
    function Build: string;
  end;

implementation

constructor TQueryBuilder.Create;
begin
  inherited Create;
  FWheres := TStringList.Create;
  FLimit := 0;
end;

destructor TQueryBuilder.Destroy;
begin
  FWheres.Free;
  inherited Destroy;
end;

function TQueryBuilder.Select(const AFields: string): TQueryBuilder;
begin
  FSelect := AFields;
  Result := Self;
end;

function TQueryBuilder.From(const ATable: string): TQueryBuilder;
begin
  FFrom := ATable;
  Result := Self;
end;

function TQueryBuilder.Where(const ACondition: string): TQueryBuilder;
begin
  FWheres.Add(ACondition);
  Result := Self;
end;

function TQueryBuilder.OrderBy(const AField: string; ADesc: Boolean): TQueryBuilder;
begin
  FOrderBy := AField;
  if ADesc then FOrderBy := FOrderBy + ' DESC';
  Result := Self;
end;

function TQueryBuilder.Limit(ACount: Integer): TQueryBuilder;
begin
  FLimit := ACount;
  Result := Self;
end;

function TQueryBuilder.Build: string;
var
  LSql: TStringBuilder;
begin
  LSql := TStringBuilder.Create;
  try
    LSql.Append('SELECT ').Append(FSelect);
    LSql.Append(' FROM ').Append(FFrom);
    if FWheres.Count > 0 then
      LSql.Append(' WHERE ').Append(String.Join(' AND ', FWheres.ToStringArray));
    if not FOrderBy.IsEmpty then
      LSql.Append(' ORDER BY ').Append(FOrderBy);
    if FLimit > 0 then
      LSql.Append(' LIMIT ').Append(FLimit.ToString);
    Result := LSql.ToString;
  finally
    LSql.Free;
  end;
end;
```

---

## 🔧 Structural Patterns

### Adapter — Legacy Integration

```pascal
unit MeuApp.Infra.Payment.Adapter;

interface

type
  // Sistema legado — not pode ser alterado
  TLegacyPaymentGateway = class
    procedure ProcessarPagamento(AValor: Double; ACodigoCartao: string);
  end;

  // Interface esperada pelo domínio moderno
  IPaymentGateway = interface
    ['{C3D4-...}']
    procedure ProcessPayment(AAmount: Currency; const ACardToken: string);
  end;

  // Adapter: traduz a chamada nova para a legada
  TLegacyPaymentAdapter = class(TInterfacedObject, IPaymentGateway)
  private
    FLegacy: TLegacyPaymentGateway;
  public
    constructor Create(ALegacy: TLegacyPaymentGateway);
    destructor Destroy; override;
    procedure ProcessPayment(AAmount: Currency; const ACardToken: string);
  end;

implementation

constructor TLegacyPaymentAdapter.Create(ALegacy: TLegacyPaymentGateway);
begin
  inherited Create;
  if not Assigned(ALegacy) then
    raise EArgumentNilException.Create('ALegacy gateway cannot be nil');
  FLegacy := ALegacy;
end;

destructor TLegacyPaymentAdapter.Destroy;
begin
  FLegacy.Free;  // O adapter possui o legado
  inherited Destroy;
end;

procedure TLegacyPaymentAdapter.ProcessPayment(AAmount: Currency; const ACardToken: string);
begin
  FLegacy.ProcessarPagamento(AAmount, ACardToken);
end;
```

### Decorator — Extension without Inheritance

```pascal
unit MeuApp.Infra.Logger.Decorators;

interface

type
  ILogger = interface
    ['{D4E5-...}']
    procedure Log(const ALevel, AMessage: string);
  end;

  TConsoleLogger = class(TInterfacedObject, ILogger)
    procedure Log(const ALevel, AMessage: string);
  end;

  // Decorator: adiciona timestamp
  TTimestampDecorator = class(TInterfacedObject, ILogger)
  private
    FInner: ILogger;
  public
    constructor Create(AInner: ILogger);
    procedure Log(const ALevel, AMessage: string);
  end;

  // Decorator: filtra por nível mínimo
  TLevelFilterDecorator = class(TInterfacedObject, ILogger)
  private
    FInner: ILogger;
    FMinLevel: string;
  public
    constructor Create(AInner: ILogger; const AMinLevel: string);
    procedure Log(const ALevel, AMessage: string);
  end;

implementation

procedure TConsoleLogger.Log(const ALevel, AMessage: string);
begin
  Writeln(Format('[%s] %s', [ALevel, AMessage]));
end;

procedure TTimestampDecorator.Log(const ALevel, AMessage: string);
begin
  FInner.Log(ALevel, Format('%s | %s', [FormatDateTime('yyyy-mm-dd hh:nn:ss', Now), AMessage]));
end;

procedure TLevelFilterDecorator.Log(const ALevel, AMessage: string);
begin
  if ALevel >= FMinLevel then // Filtra DEBUG em produção
    FInner.Log(ALevel, AMessage);
end;
```

### Facade — Simplifying Subsystems

```pascal
unit MeuApp.Application.NFe.Facade;

interface

uses
  MeuApp.Domain.NFe.Entity,
  MeuApp.Domain.NFe.Repository.Intf;

type
  /// <summary>
  ///   Fachada que simplifica o processo completo de emissão de NF-e,
  ///   ocultando XML, assinatura digital e comunicaction com SEFAZ.
  /// </summary>
  TNFeFacade = class
  private
    FXmlBuilder: TNFeXmlBuilder;
    FSigner: TDigitalSigner;
    FTransmitter: TSefazTransmitter;
    FRepository: INFeRepository;
    procedure GenerateXml(ANFe: TNFe);
    procedure SignXml(ANFe: TNFe);
    procedure TransmitToSefaz(ANFe: TNFe);
    procedure PersistResult(ANFe: TNFe);
  public
    constructor Create(ARepository: INFeRepository);
    destructor Destroy; override;
    /// <summary>Emite NF-e: gera XML → assina → transmite → persiste.</summary>
    procedure EmitirNFe(ANFe: TNFe);
    /// <summary>Cancela NF-e já emitida.</summary>
    procedure CancelarNFe(const AChaveAcesso: string; const AMotivo: string);
  end;
```

### Proxy — Access Control

```pascal
unit MeuApp.Infra.Customer.Repository.Proxy;

interface

uses
  MeuApp.Domain.Customer.Entity,
  MeuApp.Domain.Customer.Repository.Intf,
  MeuApp.Domain.User.Entity;

type
  /// <summary>
  ///   Proxy de segurança que verifica permissões before de delegar ao repositório real.
  /// </summary>
  TSecureCustomerRepositoryProxy = class(TInterfacedObject, ICustomerRepository)
  private
    FReal: ICustomerRepository;
    FCurrentUser: TUser;
    procedure CheckPermission(const AAction: string);
  public
    constructor Create(AReal: ICustomerRepository; ACurrentUser: TUser);
    function FindById(AId: Integer): TCustomer;
    function FindAll: TObjectList<TCustomer>;
    procedure Insert(ACustomer: TCustomer);
    procedure Update(ACustomer: TCustomer);
    procedure Delete(AId: Integer);
  end;

implementation

procedure TSecureCustomerRepositoryProxy.CheckPermission(const AAction: string);
begin
  if not FCurrentUser.HasPermission(AAction) then
    raise EAuthorizationException.CreateFmt(
      'User "%s" does not have permission: %s', [FCurrentUser.Login, AAction]);
end;

procedure TSecureCustomerRepositoryProxy.Delete(AId: Integer);
begin
  CheckPermission('CUSTOMER_DELETE');
  FReal.Delete(AId);
end;
```

---

## 🎭 Behavioral Patterns

### Strategy — Variation of Algorithms

```pascal
unit MeuApp.Domain.Tax.Strategies;

interface

type
  ITaxStrategy = interface
    ['{E5F6-...}']
    function Calculate(ABaseValue: Currency): Currency;
    function GetDescription: string;
  end;

  TSimplesTaxStrategy = class(TInterfacedObject, ITaxStrategy)
  public
    function Calculate(ABaseValue: Currency): Currency;
    function GetDescription: string;
  end;

  TLucroPresumidoStrategy = class(TInterfacedObject, ITaxStrategy)
  public
    function Calculate(ABaseValue: Currency): Currency;
    function GetDescription: string;
  end;

  TIsencaoStrategy = class(TInterfacedObject, ITaxStrategy)
  public
    function Calculate(ABaseValue: Currency): Currency;
    function GetDescription: string;
  end;

implementation

const
  SIMPLES_RATE = 0.06;
  LUCRO_PRESUMIDO_RATE = 0.15;

function TSimplesTaxStrategy.Calculate(ABaseValue: Currency): Currency;
begin
  Result := ABaseValue * SIMPLES_RATE;
end;

function TSimplesTaxStrategy.GetDescription: string;
begin
  Result := 'Simples Nacional (6%)';
end;

function TIsencaoStrategy.Calculate(ABaseValue: Currency): Currency;
begin
  Result := 0;
end;

function TIsencaoStrategy.GetDescription: string;
begin
  Result := 'Isento de impostos';
end;
```

### Observer — Domain Events

```pascal
unit MeuApp.Domain.Order.Events;

interface

uses
  System.Generics.Collections,
  MeuApp.Domain.Order.Entity;

type
  IOrderEventObserver = interface
    ['{F6A7-...}']
    procedure OnOrderPlaced(AOrder: TOrder);
    procedure OnOrderCancelled(AOrder: TOrder);
  end;

  TOrderEventPublisher = class
  private
    FObservers: TList<IOrderEventObserver>;
  public
    constructor Create;
    destructor Destroy; override;
    procedure Subscribe(AObserver: IOrderEventObserver);
    procedure Unsubscribe(AObserver: IOrderEventObserver);
    procedure NotifyOrderPlaced(AOrder: TOrder);
    procedure NotifyOrderCancelled(AOrder: TOrder);
  end;

  // Observers concretos
  TEmailOrderNotifier = class(TInterfacedObject, IOrderEventObserver)
    procedure OnOrderPlaced(AOrder: TOrder);    // envia confirmaction por e-mail
    procedure OnOrderCancelled(AOrder: TOrder); // envia aviso de cancelamento
  end;

  TStockReservationObserver = class(TInterfacedObject, IOrderEventObserver)
    procedure OnOrderPlaced(AOrder: TOrder);    // reserva estoque
    procedure OnOrderCancelled(AOrder: TOrder); // libera estoque
  end;

implementation

constructor TOrderEventPublisher.Create;
begin
  inherited Create;
  FObservers := TList<IOrderEventObserver>.Create;
end;

destructor TOrderEventPublisher.Destroy;
begin
  FObservers.Free;
  inherited Destroy;
end;

procedure TOrderEventPublisher.NotifyOrderPlaced(AOrder: TOrder);
var
  LObserver: IOrderEventObserver;
begin
  for LObserver in FObservers do
    LObserver.OnOrderPlaced(AOrder);
end;
```

### Command — Wrapping Actions

```pascal
unit MeuApp.Application.Commands;

interface

uses
  MeuApp.Domain.Customer.Entity,
  MeuApp.Domain.Customer.Repository.Intf;

type
  ICommand = interface
    ['{A7B8-...}']
    procedure Execute;
    procedure Undo;
    function GetDescription: string;
  end;

  TCreateCustomerCommand = class(TInterfacedObject, ICommand)
  private
    FRepository: ICustomerRepository;
    FCustomerData: TCustomerDTO;
    FCreatedId: Integer;
  public
    constructor Create(ARepository: ICustomerRepository; AData: TCustomerDTO);
    procedure Execute;
    procedure Undo;
    function GetDescription: string;
  end;

  TDeleteCustomerCommand = class(TInterfacedObject, ICommand)
  private
    FRepository: ICustomerRepository;
    FCustomerId: Integer;
    FBackup: TCustomer;
  public
    constructor Create(ARepository: ICustomerRepository; ACustomerId: Integer);
    destructor Destroy; override;
    procedure Execute;
    procedure Undo;
    function GetDescription: string;
  end;

  // Histórico de Commands (para Undo/Redo)
  TCommandHistory = class
  private
    FHistory: TStack<ICommand>;
    FRedoStack: TStack<ICommand>;
  public
    constructor Create;
    destructor Destroy; override;
    procedure Execute(ACommand: ICommand);
    procedure Undo;
    procedure Redo;
    function CanUndo: Boolean;
    function CanRedo: Boolean;
  end;
```

### Template Method — Algorithm Skeleton

```pascal
unit MeuApp.Application.Report.Generator;

interface

type
  TReportData = record
    Title: string;
    StartDate: TDate;
    EndDate: TDate;
  end;

  /// <summary>
  ///   Base abstrata que define o esqueleto do algoritmo de geraction de relatório.
  ///   Subclasses implementam os passos variáveis.
  /// </summary>
  TReportGenerator = class abstract
  protected
    FData: TReportData;
    procedure LoadData; virtual; abstract;
    procedure ValidateData; virtual;           // hook com implementaction default
    procedure ProcessData; virtual; abstract;
    procedure FormatOutput; virtual; abstract;
    procedure SaveOutput(const APath: string); virtual; abstract;
    procedure SendNotification; virtual;       // hook opcional — default: noop
  public
    // Template Method — not pode ser sobrescrito (final)
    procedure Generate(AData: TReportData; const ASavePath: string);
  end;

  TSalesReportGenerator = class(TReportGenerator)
  protected
    procedure LoadData; override;
    procedure ProcessData; override;
    procedure FormatOutput; override;
    procedure SaveOutput(const APath: string); override;
    procedure SendNotification; override;
  end;

implementation

procedure TReportGenerator.Generate(AData: TReportData; const ASavePath: string);
begin
  FData := AData;
  LoadData;
  ValidateData;
  ProcessData;
  FormatOutput;
  SaveOutput(ASavePath);
  SendNotification;
end;

procedure TReportGenerator.ValidateData;
begin
  if FData.Title.Trim.IsEmpty then
    raise EValidationException.Create('Report title cannot be empty');
  if FData.StartDate > FData.EndDate then
    raise EValidationException.Create('StartDate must be before EndDate');
end;

procedure TReportGenerator.SendNotification;
begin
  // Hook default: vazio. Subclasses podem sobrescrever para enviar e-mail etc.
end;
```

### Chain of Responsibility — Validation Pipeline

```pascal
unit MeuApp.Application.Validation.Chain;

interface

uses
  MeuApp.Domain.Customer.Entity;

type
  TValidationResult = record
    IsValid: Boolean;
    ErrorMessage: string;
    class function Ok: TValidationResult; static;
    class function Fail(const AMessage: string): TValidationResult; static;
  end;

  IValidationHandler = interface
    ['{B8C9-...}']
    procedure SetNext(AHandler: IValidationHandler);
    function Validate(ACustomer: TCustomer): TValidationResult;
  end;

  TBaseValidationHandler = class(TInterfacedObject, IValidationHandler)
  private
    FNext: IValidationHandler;
  public
    procedure SetNext(AHandler: IValidationHandler);
    function Validate(ACustomer: TCustomer): TValidationResult; virtual;
  end;

  TNameValidationHandler = class(TBaseValidationHandler)
    function Validate(ACustomer: TCustomer): TValidationResult; override;
  end;

  TCpfValidationHandler = class(TBaseValidationHandler)
    function Validate(ACustomer: TCustomer): TValidationResult; override;
  end;

  TEmailValidationHandler = class(TBaseValidationHandler)
    function Validate(ACustomer: TCustomer): TValidationResult; override;
  end;

implementation

function TBaseValidationHandler.Validate(ACustomer: TCustomer): TValidationResult;
begin
  // Delega para o próximo handler se houver
  if Assigned(FNext) then
    Result := FNext.Validate(ACustomer)
  else
    Result := TValidationResult.Ok;
end;

function TNameValidationHandler.Validate(ACustomer: TCustomer): TValidationResult;
begin
  if ACustomer.Name.Trim.IsEmpty then
    Exit(TValidationResult.Fail('Nome é obrigatório'));
  if ACustomer.Name.Length < 3 then
    Exit(TValidationResult.Fail('Nome deve ter ao menos 3 caracteres'));
  Result := inherited Validate(ACustomer);  // continua a cadeia
end;
```

### State — Behavior by State

```pascal
unit MeuApp.Domain.Order.States;

interface

uses
  MeuApp.Domain.Order.Entity;

type
  IOrderState = interface
    ['{C9D0-...}']
    procedure Confirm(AOrder: TOrder);
    procedure Ship(AOrder: TOrder);
    procedure Deliver(AOrder: TOrder);
    procedure Cancel(AOrder: TOrder);
    function GetStatusDescription: string;
  end;

  // Estado: Novo (a confirmar)
  TNewOrderState = class(TInterfacedObject, IOrderState)
  public
    procedure Confirm(AOrder: TOrder);
    procedure Ship(AOrder: TOrder);   // lança EInvalidOperationException
    procedure Deliver(AOrder: TOrder);
    procedure Cancel(AOrder: TOrder);
    function GetStatusDescription: string;
  end;

  // Estado: Confirmado (aguardando envio)
  TConfirmedOrderState = class(TInterfacedObject, IOrderState)
  public
    procedure Confirm(AOrder: TOrder);  // lança EInvalidOperationException
    procedure Ship(AOrder: TOrder);
    procedure Deliver(AOrder: TOrder);
    procedure Cancel(AOrder: TOrder);
    function GetStatusDescription: string;
  end;

  // Estado: Em trânsito
  TShippedOrderState = class(TInterfacedObject, IOrderState)
  public
    procedure Confirm(AOrder: TOrder);
    procedure Ship(AOrder: TOrder);
    procedure Deliver(AOrder: TOrder);
    procedure Cancel(AOrder: TOrder);  // requer chamada a transportadora
    function GetStatusDescription: string;
  end;

implementation

procedure TNewOrderState.Confirm(AOrder: TOrder);
begin
  AOrder.ConfirmedAt := Now;
  AOrder.SetState(TConfirmedOrderState.Create);  // transição
end;

procedure TNewOrderState.Ship(AOrder: TOrder);
begin
  raise EInvalidOperationException.Create('Pedido ainda não confirmado. Confirme antes de enviar.');
end;

function TNewOrderState.GetStatusDescription: string;
begin
  Result := 'Novo — aguardando confirmação';
end;
```

---

## 📌 Guide to Choosing the Right Pattern

| Need | Standard |
|---|---|
| Create objects with type variation | Factory Method / Abstract Factory |
| Create complex objects step by step | Builder |
| Ensure Global Single Instance | Singleton |
| Copy objects | Prototype |
| Adapt incompatible interface | Adapter |
| Add responsibilities dynamically | Decorator |
| Simplify complex system | Facade |
| Control access to an object | Proxy |
| Compose objects in tree structure | Composite |
| Vary algorithm without changing context | Strategy |
| Notify multiple objects about changes | Observer |
| Encapsulate actions with undo/redo | Command |
| Algorithm with variations | Template Method |
| Pass request through handler chain | Chain of Responsibility |
| Behavior that changes with the state | State |

## ✅ Final Checklist

- [ ] All dependencies injected via constructor (DIP)
- [ ] Every interface implementation uses `TInterfacedObject` (ARC)
- [ ] No `.Create` without `try..finally` (except on ARC interfaces)
- [ ] Each class has a single responsibility (SRP)
- [ ] DUnitX tests cover each pattern with Fakes/Stubs
- [ ] XMLDoc in Portuguese in public methods
- [ ] Prefixes: `T` class, `I` interface, `E` exception, `F` field, `A` param, `L` location
