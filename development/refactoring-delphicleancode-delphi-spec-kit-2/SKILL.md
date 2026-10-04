---
name: "Delphi Code Refactoring"
description: "Refactoring techniques for Object Pascal focused on improving readability, removing code smells, and preserving behavior through practices like Extract Method, Guard Clauses, and polymorphism."
---

# Delphi Code Refactoring — Skill

Use this skill when the user requests refactoring, code review or removal of code smells in Object Pascal. Refactoring **never changes observable behavior** — it only improves the internal structure of the code.

## When to Use

- User asks to "improve", "clean up" or "refactor" existing code
- When reviewing code and finding code smells
- When preparing legacy code to receive new functionality
- Before adding tests to untestable code
- When answering "why is this code difficult to understand?"

## Fundamental Principle

> "Refactoring is the art of changing the structure of code without changing its behavior."
> Always write (or check for) tests **before** refactoring.

---

## 📋 Catalog of Code Smells and Techniques

### 1. Extract Method — Long Method

**Detect:** Method with more than 20 lines or that needs comments to explain blocks.

**Before:**
```pascal
procedure TInvoiceService.GenerateInvoice(AOrder: TOrder);
var
  LTax, LSubtotal, LTotal: Currency;
  LItem: TOrderItem;
  LLines: TStringList;
begin
  //Calculate subtotal
  LSubtotal := 0;
  for LItem in AOrder.Items do
    LSubtotal += LItem.UnitPrice * LItem.Quantity;

  //Calculates tax
  if AOrder.IsExempt then LTax := 0
  else LTax := LSubtotal * 0.12;

  LTotal := LSubtotal + LTax;

  //Generates report lines
  LLines := TStringList.Create;
  try
    LLines.Add('NOTA FISCAL');
    LLines.Add(Format('Cliente: %s', [AOrder.Customer.Name]));
    for LItem in AOrder.Items do
      LLines.Add(Format('  %s x%d = R$%.2f',
        [LItem.Product.Name, LItem.Quantity, LItem.UnitPrice * LItem.Quantity]));
    LLines.Add(Format('Total: R$%.2f', [LTotal]));
    LLines.SaveToFile(AOrder.InvoicePath);
  finally
    LLines.Free;
  end;
end;
```

**After:**
```pascal
procedure TInvoiceService.GenerateInvoice(AOrder: TOrder);
var
  LSubtotal, LTax: Currency;
begin
  LSubtotal := CalculateSubtotal(AOrder);
  LTax      := CalculateTax(AOrder, LSubtotal);
  SaveInvoiceFile(AOrder, LSubtotal + LTax);
end;

function TInvoiceService.CalculateSubtotal(AOrder: TOrder): Currency;
var LItem: TOrderItem;
begin
  Result := 0;
  for LItem in AOrder.Items do
    Result := Result + (LItem.UnitPrice * LItem.Quantity);
end;

function TInvoiceService.CalculateTax(AOrder: TOrder; ASubtotal: Currency): Currency;
const
  STANDARD_TAX_RATE = 0.12;
begin
  if AOrder.IsExempt then Result := 0
  else Result := ASubtotal * STANDARD_TAX_RATE;
end;

procedure TInvoiceService.SaveInvoiceFile(AOrder: TOrder; ATotal: Currency);
var
  LLines: TStringList;
  LItem: TOrderItem;
begin
  LLines := TStringList.Create;
  try
    LLines.Add('NOTA FISCAL');
    LLines.Add(Format('Cliente: %s', [AOrder.Customer.Name]));
    for LItem in AOrder.Items do
      LLines.Add(Format('  %s x%d = R$%.2f',
        [LItem.Product.Name, LItem.Quantity, LItem.UnitPrice * LItem.Quantity]));
    LLines.Add(Format('Total: R$%.2f', [ATotal]));
    LLines.SaveToFile(AOrder.InvoicePath);
  finally
    LLines.Free;
  end;
end;
```

---

### 2. Extract Class — Class with Multiple Responsibilities

**Detect:** Class with fields of different nature, methods without cohesion.

**Before:**
```pascal
TEmployee = class
private
  //Personal data
  FName: string;
  FBirthDate: TDate;
  FCpf: string;
  //Salary data
  FBaseSalary: Currency;
  FBonusPercentage: Double;
  FDepartmentId: Integer;
  //HR Data
  FHiredDate: TDate;
  FVacationDaysLeft: Integer;
  FPerformanceScore: Integer;
public
  function CalculateGrossSalary: Currency;
  function CalculateNetSalary: Currency;
  function CalculateVacationPay: Currency;
  function GetNextVacationDate: TDate;
  function GetYearsOfService: Integer;
  function IsEligibleForBonus: Boolean;
end;
```

**After:**
```pascal
//Value Object — immutable
TEmployeePersonalData = record
  Name: string;
  BirthDate: TDate;
  Cpf: string;
end;

//Cohesive class: salary responsibility
TEmployeeSalary = class
private
  FBaseSalary: Currency;
  FBonusPercentage: Double;
public
  constructor Create(ABaseSalary: Currency; ABonusPercentage: Double);
  function CalculateGross: Currency;
  function CalculateNet: Currency;
  function IsEligibleForBonus: Boolean;
end;

//Cohesive class: HR responsibility
TEmployeeHrRecord = class
private
  FHiredDate: TDate;
  FVacationDaysLeft: Integer;
  FPerformanceScore: Integer;
public
  function GetYearsOfService: Integer;
  function GetNextVacationDate: TDate;
  function CalculateVacationPay(AGrossSalary: Currency): Currency;
end;

//Main entity — now just aggregates the parts
TEmployee = class
private
  FPersonalData: TEmployeePersonalData;
  FSalary: TEmployeeSalary;
  FHrRecord: TEmployeeHrRecord;
public
  constructor Create(AData: TEmployeePersonalData;
    ASalary: TEmployeeSalary; AHr: TEmployeeHrRecord);
  destructor Destroy; override;
  property PersonalData: TEmployeePersonalData read FPersonalData;
  property Salary: TEmployeeSalary read FSalary;
  property HrRecord: TEmployeeHrRecord read FHrRecord;
end;
```

---

### 3. Replace Nested Conditionals with Guard Clauses

**Detect:** More than 2 levels of `if..then..begin..end` nested.

**Before:**
```pascal
function TBankService.Withdraw(AAccount: TAccount; AAmount: Currency): Boolean;
begin
  Result := False;
  if Assigned(AAccount) then
  begin
    if AAccount.IsActive then
    begin
      if AAmount > 0 then
      begin
        if AAccount.Balance >= AAmount then
        begin
          if not AAccount.IsBlocked then
          begin
            AAccount.Balance := AAccount.Balance - AAmount;
            FRepository.Save(AAccount);
            Result := True;
          end;
        end;
      end;
    end;
  end;
end;
```

**After:**
```pascal
function TBankService.Withdraw(AAccount: TAccount; AAmount: Currency): Boolean;
begin
  if not Assigned(AAccount) then
    raise EArgumentNilException.Create('Conta não pode ser nula');
  if not AAccount.IsActive then
    raise EBusinessRuleException.Create('Conta inativa');
  if AAmount <= 0 then
    raise EValidationException.Create('Valor do saque deve ser positivo');
  if AAccount.Balance < AAmount then
    raise EInsufficientFundsException.CreateFmt(
      'Saldo insuficiente. Disponível: R$%.2f', [AAccount.Balance]);
  if AAccount.IsBlocked then
    raise EBusinessRuleException.Create('Conta bloqueada');

  AAccount.Balance := AAccount.Balance - AAmount;
  FRepository.Save(AAccount);
  Result := True;
end;
```

---

### 4. Replace Magic Numbers with Constants

**Detect:** Numeric or string literals without an explanatory name in the code.

**Before:**
```pascal
if AProduct.Stock < 5 then NotifyLowStock(AProduct);
LInstallmentValue := AOrder.Total / 12;
if APassword.Length < 8 then raise ...;
if AUser.FailedLogins >= 3 then LockAccount(AUser);
LInterest := ADebt * 0.02;  //late payment interest
```

**After:**
```pascal
const
  LOW_STOCK_THRESHOLD       = 5;
  MAX_INSTALLMENTS          = 12;
  MIN_PASSWORD_LENGTH       = 8;
  MAX_FAILED_LOGIN_ATTEMPTS = 3;
  MONTHLY_INTEREST_RATE     = 0.02;

if AProduct.Stock < LOW_STOCK_THRESHOLD then NotifyLowStock(AProduct);
LInstallmentValue := AOrder.Total / MAX_INSTALLMENTS;
if APassword.Length < MIN_PASSWORD_LENGTH then raise ...;
if AUser.FailedLogins >= MAX_FAILED_LOGIN_ATTEMPTS then LockAccount(AUser);
LInterest := ADebt * MONTHLY_INTEREST_RATE;
```

---

### 5. Replace Conditional with Polymorphism (Strategy/State)

**Detect:** `case` or `if/else if` string that checks the type or regime of an object.

**Before:**
```pascal
function TShippingService.CalculateFreight(AOrder: TOrder): Currency;
begin
  case AOrder.ShippingMethod of
    smPAC:     Result := AOrder.Weight * 2.50 + 8.0;
    smSEDEX:   Result := AOrder.Weight * 4.80 + 15.0;
    smTransp:  Result := AOrder.Weight * 1.20;
    smRetirada:Result := 0;
  end;
end;
```

**After:**
```pascal
//Interface Strategy
IFreightStrategy = interface
  ['{GUID}']
  function Calculate(AWeightKg: Double): Currency;
  function GetCarrierName: string;
end;

//Implementations: one per variation
TPACFreightStrategy = class(TInterfacedObject, IFreightStrategy)
  function Calculate(AWeightKg: Double): Currency;   //weight * 2.50 + 8.0
  function GetCarrierName: string;
end;

TSEDEXFreightStrategy = class(TInterfacedObject, IFreightStrategy)
  function Calculate(AWeightKg: Double): Currency;   //weight * 4.80 + 15.0
  function GetCarrierName: string;
end;

TTransportadoraFreightStrategy = class(TInterfacedObject, IFreightStrategy)
  function Calculate(AWeightKg: Double): Currency;   //weight * 1.20
  function GetCarrierName: string;
end;

TRetiradaFreightStrategy = class(TInterfacedObject, IFreightStrategy)
  function Calculate(AWeightKg: Double): Currency;   //always 0
  function GetCarrierName: string;
end;

//Context — no longer needs the case
function TShippingService.CalculateFreight(AOrder: TOrder;
  AStrategy: IFreightStrategy): Currency;
begin
  Result := AStrategy.Calculate(AOrder.WeightKg);
end;
```

---

### 6. Introduce Parameter Object

**Detect:** Method with > 4 parameters, especially if several are optional.

**Before:**
```pascal
function TReportService.GenerateSalesReport(
  AStartDate: TDate;
  AEndDate: TDate;
  const AProductCategory: string;
  const ASalesRepId: string;
  AMinAmount: Currency;
  AGroupByMonth: Boolean;
  AIncludeReturns: Boolean): TReportResult;
```

**After:**
```pascal
TSalesReportFilter = record
  StartDate: TDate;
  EndDate: TDate;
  ProductCategory: string;
  SalesRepId: string;
  MinAmount: Currency;
  GroupByMonth: Boolean;
  IncludeReturns: Boolean;
  //Constructor with defaults
  class function Default: TSalesReportFilter; static;
end;

class function TSalesReportFilter.Default: TSalesReportFilter;
begin
  Result.StartDate       := StartOfYear(Date);
  Result.EndDate         := Date;
  Result.ProductCategory := '';
  Result.SalesRepId      := '';
  Result.MinAmount       := 0;
  Result.GroupByMonth    := False;
  Result.IncludeReturns  := False;
end;

function TReportService.GenerateSalesReport(
  AFilter: TSalesReportFilter): TReportResult;
```

---

### 7. Remove `with` Statement

**Detect:** Any `with Objeto do begin...end` in the code.

**Rule:** Never use `with`. Prefer local variables or explicit qualification.

**Before:**
```pascal
procedure TCustomerForm.LoadData;
begin
  with qryCustomers do
  begin
    Close;
    SQL.Text := 'SELECT * FROM customers WHERE id = :id';
    ParamByName('id').AsInteger := FCustomerId;
    Open;
    with FieldByName('address') do
    begin
      edtStreet.Text := AsString;
    end;
  end;
end;
```

**After:**
```pascal
procedure TCustomerForm.LoadData;
var LAddressField: TField;
begin
  qryCustomers.Close;
  qryCustomers.SQL.Text := 'SELECT * FROM customers WHERE id = :id';
  qryCustomers.ParamByName('id').AsInteger := FCustomerId;
  qryCustomers.Open;

  LAddressField := qryCustomers.FieldByName('address');
  edtStreet.Text := LAddressField.AsString;
end;
```

---

### 8. Extract Interface / Invert Dependency

**Detect:** Service or class depending directly on concrete class (not interface).

**Before:**
```pascal
TOrderService = class
private
  FEmailSender: TSmtpEmailSender;      //concrete class
  FRepository:  TFireDACOrderRepo;     //concrete class
public
  constructor Create;  //instance internally — impossible to test
end;

constructor TOrderService.Create;
begin
  FEmailSender := TSmtpEmailSender.Create('smtp.server.com', 587);
  FRepository  := TFireDACOrderRepo.Create(GetDatabaseConnection);
end;
```

**After:**
```pascal
//1. Extract interfaces
IEmailSender = interface
  ['{GUID}']
  procedure Send(const ATo, ASubject, ABody: string);
end;

IOrderRepository = interface
  ['{GUID}']
  function FindById(AId: Integer): TOrder;
  procedure Save(AOrder: TOrder);
end;

//2. Inject into the constructor — testable and flexible
TOrderService = class
private
  FEmailSender: IEmailSender;
  FRepository:  IOrderRepository;
public
  constructor Create(ARepository: IOrderRepository; AEmailSender: IEmailSender);
end;

//3. Em testes, injete fakes
TFakeEmailSender = class(TInterfacedObject, IEmailSender)
  FSentMessages: TStringList;
  procedure Send(const ATo, ASubject, ABody: string);
end;
```

---

### 9. Rename — Self-Descriptive Names

**Detect:** Variables like `x`, `tmp`, `data`, `flag`; methods like `Proc1`, `DoIt`, `Handle`.

```pascal
//❌ BEFORE
var x, tmp: Integer;
    s: string;
    flag: Boolean;
procedure Handle(d: TData);
function Calc(v: Double): Double;

//✅ AFTER
var LRetryCount, LMaxRetries: Integer;
    LCustomerFullName: string;
    LIsPaymentApproved: Boolean;
procedure ProcessCustomerOrder(AOrderData: TOrderData);
function CalculateShippingCost(AWeightKg: Double): Currency;
```

---

### 10. Inline Method — Unnecessarily Delegate Method

**Detect:** Method that just calls another method, without additional logic.

```pascal
//❌ BEFORE — unnecessary delegation
function TOrder.GetTotal: Currency;
begin
  Result := CalculateOrderTotal;  //just delegate
end;

function TOrder.CalculateOrderTotal: Currency;
begin
  Result := FSubtotal + FTax - FDiscount;
end;

//✅ AFTER — just a method with a descriptive name
function TOrder.GetTotal: Currency;
begin
  Result := FSubtotal + FTax - FDiscount;
end;
```

---

## 🔄 Secure Refactoring Process

```
1. ENTENDER  → Leia e compreenda o código atual
2. TESTAR    → Escreva/execute testes que cobrem o comportamento atual
3. PEQUENO   → Faça uma refatoração por vez (não tudo de uma vez)
4. TESTAR    → Execute os testes novamente — devem continuar passando
5. COMMIT    → Commit atômico por refatoração (mensagem: "refactor: extract CalculateTax")
6. REPETIR   → Próxima refatoração
```

## ✅ Final Checklist

- [ ] Is there testing covering the behavior before refactoring?
- [ ] Does the observable behavior remain the same?
- [ ] No `with` was introduced?
- [ ] No nameless magic number?
- [ ] Resulting method has ≤ 20 lines?
- [ ] Name of the extracted method needs no comment?
- [ ] Dependencies are now via interface?
- [ ] Do guard clauses replace deep nesting?
- [ ] Were excess parameters grouped in DTO/Record?
