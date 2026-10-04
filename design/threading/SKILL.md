---
name: "Threading & Multi-Threading"
description: "Threading patterns in Delphi — TThread, TTask, TParallel, Synchronize, Queue, thread-safety, Producer-Consumer, pools, cancellation and debugging"
---

# Threading & Multi-Threading — Skill

Use this skill when working with threads, asynchronous tasks and parallelism in Delphi projects.

## When to Use

- When performing time-consuming operations without blocking the UI (VCL/FMX)
- When implementing parallel data processing
- When creating servers/workers that process concurrent requests
- When synchronizing access to shared resources
- When managing thread pools and work queues
- By implementing graceful thread cancellation

## Golden Rule of Threading in Delphi

> **NEVER access visual components (VCL/FMX) directly from a secondary thread.**
> Use `TThread.Synchronize` or `TThread.Queue` to update the UI.

## Available Approaches

| Approach | When to Use | Complexity |
|-----------|-------------|-------------|
| `TThread` | Full control, long-running threads | Average |
| `TThread.CreateAnonymousThread` | Simple, one-shot tasks | Low |
| `TTask` (PPL) | Modern parallelism, lightweight tasks | Low |
| `TParallel.For` (PPL) | Parallel loops in collections | Low |
| `TFuture<T>` (PPL) | Asynchronous result with return value | Low |
| `TThreadPool` | Reusable Thread Pool | Average |
| Dedicated thread (inheritance) | Permanent workers, servers, queues | High |

## TThread — Classical Approach

### Thread with Inheritance (Recommended for Workers)

```pascal
type
  ///<summary>
  ///Worker thread for background processing.
  ///Demonstrates TThread inheritance with cancellation via Terminated.
  ///</summary>
  TDataProcessorThread = class(TThread)
  private
    FItems: TThreadList<string>;
    FOnProgress: TProc<Integer, Integer>;
    FOnComplete: TProc<Boolean>;
  protected
    procedure Execute; override;
  public
    constructor Create(AItems: TThreadList<string>);
    property OnProgress: TProc<Integer, Integer> write FOnProgress;
    property OnComplete: TProc<Boolean> write FOnComplete;
  end;

constructor TDataProcessorThread.Create(AItems: TThreadList<string>);
begin
  inherited Create(True);   //Create dropdown
  FreeOnTerminate := True;  //Auto-releases when finished
  FItems := AItems;
end;

procedure TDataProcessorThread.Execute;
var
  LList: TList<string>;
  LTotal, I: Integer;
begin
  try
    LList := FItems.LockList;
    try
      LTotal := LList.Count;
    finally
      FItems.UnlockList;
    end;

    for I := 0 to LTotal - 1 do
    begin
      { Verificar cancelamento em cada iteração }
      if Terminated then
        Exit;

      { Processar item }
      ProcessItem(I);

      { Atualizar UI via Queue (não-bloqueante) }
      if Assigned(FOnProgress) then
        TThread.Queue(nil,
          procedure
          begin
            FOnProgress(I + 1, LTotal);
          end);
    end;

    { Notificar conclusão na main thread }
    if Assigned(FOnComplete) then
      TThread.Queue(nil,
        procedure
        begin
          FOnComplete(not Terminated);
        end);
  except
    on E: Exception do
    begin
      TThread.Queue(nil,
        procedure
        begin
          raise EThreadException.Create('Erro no processamento: ' + E.Message);
        end);
    end;
  end;
end;
```

### Use of Dedicated Thread

```pascal
procedure TfrmMain.btnProcessClick(Sender: TObject);
var
  LThread: TDataProcessorThread;
begin
  LThread := TDataProcessorThread.Create(FSharedItems);
  LThread.OnProgress :=
    procedure(ACurrent, ATotal: Integer)
    begin
      pbrProgress.Max := ATotal;
      pbrProgress.Position := ACurrent;
      lblStatus.Caption := Format('Processando %d de %d...', [ACurrent, ATotal]);
    end;
  LThread.OnComplete :=
    procedure(ASuccess: Boolean)
    begin
      if ASuccess then
        ShowMessage('Concluído com sucesso!')
      else
        ShowMessage('Processamento cancelado.');
    end;
  LThread.Start;  //Iniciar a thread
end;

procedure TfrmMain.btnCancelClick(Sender: TObject);
begin
  { Solicitar cancelamento gracioso }
  if Assigned(FCurrentThread) then
    FCurrentThread.Terminate;
end;
```

### CreateAnonymousThread (Simple Tasks)

```pascal
///<summary>
///Simplest way to run code in the background.
///Ideal for one-shot tasks without the need for advanced control.
///</summary>
procedure TfrmMain.LoadDataAsync;
begin
  btnLoad.Enabled := False;

  TThread.CreateAnonymousThread(
    procedure
    var
      LData: TStringList;
    begin
      LData := TStringList.Create;
      try
        { Trabalho pesado (thread secundária — OK!) }
        LData.LoadFromFile('C:\dados\arquivo_grande.csv');
        Sleep(2000); //Simulate processing

        { Atualizar UI (DEVE usar Synchronize ou Queue) }
        TThread.Synchronize(nil,
          procedure
          begin
            mmoOutput.Lines.Assign(LData);
            btnLoad.Enabled := True;
            lblStatus.Caption := Format('Carregados %d registros', [LData.Count]);
          end);
      finally
        LData.Free;
      end;
    end
  ).Start;
end;
```

## Synchronize vs Queue

| Method | Behavior | When to Use |
|--------|--------------|-------------|
| `TThread.Synchronize` | **Blocking** — waits for the main thread to process | When you need the UI result |
| `TThread.Queue` | **Non-blocking** — queue and continue | Progress, logs, visual updates |

```pascal
{ Synchronize: BLOQUEIA a thread até a main thread processar }
TThread.Synchronize(nil,
  procedure
  begin
    lblStatus.Caption := 'Processando...';
  end);
//The thread only continues HERE after the main thread has executed the code above

{ Queue: NÃO BLOQUEIA — enfileira e continua imediatamente }
TThread.Queue(nil,
  procedure
  begin
    lblStatus.Caption := 'Processando...';
  end);
//The thread continues IMMEDIATELY, without waiting for the main thread
```

> **Recommendation:** Prefer `Queue` whenever possible. Use `Synchronize` only when you need a result from the UI back in the thread.

## PPL — Parallel Programming Library (System.Threading)

### TTask — Light Tasks

```pascal
uses
  System.Threading;

///<summary>
///TTask is the modern way to perform tasks in the background.
///Automatically managed by the system thread pool.
///</summary>
procedure TfrmMain.ExecuteMultipleTasks;
var
  LTask1, LTask2, LTask3: ITask;
begin
  LTask1 := TTask.Create(
    procedure
    begin
      { Tarefa 1: Carregar dados do banco }
      LoadCustomers;
    end);

  LTask2 := TTask.Create(
    procedure
    begin
      { Tarefa 2: Processar relatório }
      GenerateReport;
    end);

  LTask3 := TTask.Create(
    procedure
    begin
      { Tarefa 3: Enviar emails }
      SendPendingEmails;
    end);

  { Iniciar todas as tarefas em paralelo }
  LTask1.Start;
  LTask2.Start;
  LTask3.Start;

  { Aguardar todas completarem (com timeout) }
  TTask.WaitForAll([LTask1, LTask2, LTask3], 30000); //30s timeout

  TThread.Queue(nil,
    procedure
    begin
      ShowMessage('Todas as tarefas concluídas!');
    end);
end;
```

### TTask.Run — Direct Shortcut

```pascal
{ Forma mais simples de executar em background via PPL }
TTask.Run(
  procedure
  begin
    { Código executado no ThreadPool }
    PerformHeavyCalculation;

    TThread.Queue(nil,
      procedure
      begin
        lblResult.Caption := 'Cálculo concluído';
      end);
  end);
```

### TParallel.For — Parallel Loops

```pascal
uses
  System.Threading,
  System.SyncObjs;

///<summary>
///TParallel.For distributes loop iterations among multiple threads.
///Ideal for processing independent collections.
///</summary>
procedure TfrmMain.ProcessImagesParallel;
var
  LFiles: TArray<string>;
  LProcessed: Integer;
  LLock: TCriticalSection;
begin
  LFiles := TDirectory.GetFiles('C:\Images', '*.jpg');
  LProcessed := 0;
  LLock := TCriticalSection.Create;
  try
    TParallel.For(0, High(LFiles),
      procedure(AIndex: Integer)
      begin
        { Cada imagem processada em thread separada }
        ResizeImage(LFiles[AIndex]);

        { Atualizar contador de forma thread-safe }
        LLock.Enter;
        try
          Inc(LProcessed);
        finally
          LLock.Leave;
        end;
      end);

    ShowMessage(Format('%d imagens processadas', [LProcessed]));
  finally
    LLock.Free;
  end;
end;
```

> **⚠️ CAUTION:** Each iteration of `TParallel.For` can run on different threads. Shared variables **MUST** be protected with `TCriticalSection`, `TMonitor` or `TInterlocked`.

### TFuture<T> — Asynchronous Result

```pascal
uses
  System.Threading;

///<summary>
///TFuture runs a task and returns a value when done.
///Reading .Value blocks until the result is available.
///</summary>
procedure TfrmMain.CalculateAsync;
var
  LFuture: IFuture<Double>;
begin
  LFuture := TFuture<Double>.Create(
    function: Double
    begin
      { Cálculo pesado em background }
      Sleep(3000);
      Result := CalculateComplexFormula(FInputData);
    end);

  LFuture.Start;

  { Fazer outras coisas enquanto o cálculo roda... }
  PrepareReport;

  { Pegar o resultado (bloqueia SE ainda não terminou) }
  ShowMessage(Format('Resultado: %.2f', [LFuture.Value]));
end;
```

## Thread-Safety — Resource Protection

### TCriticalSection

```pascal
type
  TThreadSafeCounter = class
  private
    FCount: Integer;
    FLock: TCriticalSection;
  public
    constructor Create;
    destructor Destroy; override;
    procedure Increment;
    procedure Decrement;
    function GetValue: Integer;
  end;

constructor TThreadSafeCounter.Create;
begin
  inherited;
  FLock := TCriticalSection.Create;
  FCount := 0;
end;

destructor TThreadSafeCounter.Destroy;
begin
  FLock.Free;
  inherited;
end;

procedure TThreadSafeCounter.Increment;
begin
  FLock.Enter;
  try
    Inc(FCount);
  finally
    FLock.Leave;  //ALWAYS finally!
  end;
end;

function TThreadSafeCounter.GetValue: Integer;
begin
  FLock.Enter;
  try
    Result := FCount;
  finally
    FLock.Leave;
  end;
end;
```

### TMonitor (Native Object Lock)

```pascal
{ TMonitor usa o próprio objeto como lock — sem criar TCriticalSection }
procedure TThreadSafeList.AddItem(const AItem: string);
begin
  TMonitor.Enter(FList);
  try
    FList.Add(AItem);
  finally
    TMonitor.Exit(FList);
  end;
end;
```

### TInterlocked (Atomic Operations)

```pascal
{ Para operações simples em Integer/Int64 — sem lock explícito }
TInterlocked.Increment(FProcessedCount);
TInterlocked.Decrement(FPendingCount);
TInterlocked.Add(FTotalBytes, LBytesRead);
TInterlocked.Exchange(FOldValue, LNewValue);
TInterlocked.CompareExchange(FTarget, LNewVal, LExpectedVal);
```

### TThreadList<T> (Thread-Safe List)

```pascal
var
  FSharedList: TThreadList<string>;

{ Thread A: adicionar }
LList := FSharedList.LockList;
try
  LList.Add('item');
finally
  FSharedList.UnlockList;
end;

{ Thread B: ler }
LList := FSharedList.LockList;
try
  for LItem in LList do
    ProcessItem(LItem);
finally
  FSharedList.UnlockList;
end;
```

### TMultiReadExclusiveWriteSynchronizer (MREWS)

```pascal
type
  TThreadSafeCache = class
  private
    FData: TDictionary<string, string>;
    FLock: TMultiReadExclusiveWriteSynchronizer;
  public
    constructor Create;
    destructor Destroy; override;
    function TryGet(const AKey: string; out AValue: string): Boolean;
    procedure Put(const AKey, AValue: string);
  end;

function TThreadSafeCache.TryGet(const AKey: string; out AValue: string): Boolean;
begin
  FLock.BeginRead;  //Multiple threads can read simultaneously
  try
    Result := FData.TryGetValue(AKey, AValue);
  finally
    FLock.EndRead;
  end;
end;

procedure TThreadSafeCache.Put(const AKey, AValue: string);
begin
  FLock.BeginWrite;  //Only one thread can write at a time
  try
    FData.AddOrSetValue(AKey, AValue);
  finally
    FLock.EndWrite;
  end;
end;
```

## Producer-Consumer Pattern

```pascal
type
  ///<summary>
  ///Producer-Consumer com TThreadedQueue (fila thread-safe).
  ///</summary>
  TProducerConsumerDemo = class
  private
    FQueue: TThreadedQueue<string>;
    FProducerThread: TThread;
    FConsumerThread: TThread;
  public
    constructor Create;
    destructor Destroy; override;
    procedure Start;
    procedure Stop;
  end;

constructor TProducerConsumerDemo.Create;
begin
  inherited;
  { QueueDepth=100, PushTimeout=1000ms, PopTimeout=1000ms }
  FQueue := TThreadedQueue<string>.Create(100, 1000, 1000);
end;

procedure TProducerConsumerDemo.Start;
begin
  { Producer: gera itens continuamente }
  FProducerThread := TThread.CreateAnonymousThread(
    procedure
    var
      I: Integer;
    begin
      I := 0;
      while not TThread.Current.CheckTerminated do
      begin
        Inc(I);
        FQueue.PushItem(Format('Item_%d', [I]));
        Sleep(100);
      end;
    end);
  FProducerThread.FreeOnTerminate := False;

  { Consumer: processa itens da fila }
  FConsumerThread := TThread.CreateAnonymousThread(
    procedure
    var
      LItem: string;
      LResult: TWaitResult;
    begin
      while not TThread.Current.CheckTerminated do
      begin
        LResult := FQueue.PopItem(LItem);
        if LResult = wrSignaled then
          ProcessItem(LItem);
      end;
    end);
  FConsumerThread.FreeOnTerminate := False;

  FProducerThread.Start;
  FConsumerThread.Start;
end;

procedure TProducerConsumerDemo.Stop;
begin
  FProducerThread.Terminate;
  FConsumerThread.Terminate;
  FProducerThread.WaitFor;
  FConsumerThread.WaitFor;
  FProducerThread.Free;
  FConsumerThread.Free;
end;
```

## Events and Signage

### TEvent

```pascal
uses
  System.SyncObjs;

var
  FStopEvent: TEvent;

{ Criar }
FStopEvent := TEvent.Create(nil, True, False, ''); //Manual reset, initially unsignaled

{ Thread: esperar sinal }
procedure TWorkerThread.Execute;
begin
  while not Terminated do
  begin
    { Esperar até 500ms por sinal de parada }
    if FStopEvent.WaitFor(500) = wrSignaled then
      Break;

    { Fazer trabalho }
    DoWork;
  end;
end;

{ Main thread: sinalizar parada }
FStopEvent.SetEvent;
```

### TSemaphore (Competition Threshold)

```pascal
uses
  System.SyncObjs;

var
  FSemaphore: TSemaphore;

{ Limitar a 5 threads simultâneas }
FSemaphore := TSemaphore.Create(nil, 5, 5, '');

{ Em cada thread: }
FSemaphore.Acquire;
try
  { Apenas 5 threads podem estar aqui simultaneamente }
  PerformLimitedWork;
finally
  FSemaphore.Release;
end;
```

## Custom Thread Pool

```pascal
type
  TCustomThreadPool = class
  private
    FThreads: TObjectList<TThread>;
    FQueue: TThreadedQueue<TProc>;
    FMaxThreads: Integer;
  public
    constructor Create(AMaxThreads: Integer = 4);
    destructor Destroy; override;
    procedure QueueWork(AProc: TProc);
  end;

constructor TCustomThreadPool.Create(AMaxThreads: Integer);
var
  I: Integer;
begin
  inherited Create;
  FMaxThreads := AMaxThreads;
  FQueue := TThreadedQueue<TProc>.Create(1000, INFINITE, 500);
  FThreads := TObjectList<TThread>.Create(True);

  for I := 0 to FMaxThreads - 1 do
  begin
    var LThread := TThread.CreateAnonymousThread(
      procedure
      var
        LProc: TProc;
        LResult: TWaitResult;
      begin
        while not TThread.Current.CheckTerminated do
        begin
          LResult := FQueue.PopItem(LProc);
          if (LResult = wrSignaled) and Assigned(LProc) then
          try
            LProc();
          except
            on E: Exception do
              { Log error, don't crash the pool thread }
              TThread.Queue(nil,
                procedure
                begin
                  // Logger.LogError(E);
                end);
          end;
        end;
      end);
    LThread.FreeOnTerminate := False;
    LThread.Start;
    FThreads.Add(LThread);
  end;
end;

procedure TCustomThreadPool.QueueWork(AProc: TProc);
begin
  FQueue.PushItem(AProc);
end;
```

## Cancellation with Token

```pascal
type
  ICancellationToken = interface
    ['{CANCEL01-0001-0001-0001-000000000001}']
    function IsCancelled: Boolean;
    procedure Cancel;
    procedure ThrowIfCancelled;
  end;

  TCancellationToken = class(TInterfacedObject, ICancellationToken)
  private
    FCancelled: Integer;  //0=false, 1=true (atomic)
  public
    function IsCancelled: Boolean;
    procedure Cancel;
    procedure ThrowIfCancelled;
  end;

function TCancellationToken.IsCancelled: Boolean;
begin
  Result := TInterlocked.Read(FCancelled) = 1;
end;

procedure TCancellationToken.Cancel;
begin
  TInterlocked.Exchange(FCancelled, 1);
end;

procedure TCancellationToken.ThrowIfCancelled;
begin
  if IsCancelled then
    raise EOperationCancelled.Create('Operação cancelada pelo usuário');
end;

{ Uso: }
procedure ProcessWithCancellation(AToken: ICancellationToken);
begin
  for var I := 0 to 999 do
  begin
    AToken.ThrowIfCancelled;
    ProcessItem(I);
  end;
end;
```

## Important Standards

### Pattern: Background Worker with Result

```pascal
type
  ///<summary>
  ///Generic background worker that executes a function and returns
  ///the result in the main thread.
  ///</summary>
  TBackgroundWorker<T> = class
  public
    class procedure Execute(
      AWorkFunc: TFunc<T>;
      AOnSuccess: TProc<T>;
      AOnError: TProc<Exception>);
  end;

class procedure TBackgroundWorker<T>.Execute(
  AWorkFunc: TFunc<T>;
  AOnSuccess: TProc<T>;
  AOnError: TProc<Exception>);
begin
  TTask.Run(
    procedure
    var
      LResult: T;
    begin
      try
        LResult := AWorkFunc();
        TThread.Queue(nil,
          procedure
          begin
            AOnSuccess(LResult);
          end);
      except
        on E: Exception do
          TThread.Queue(nil,
            procedure
            begin
              AOnError(E);
            end);
      end;
    end);
end;

{ Uso elegante: }
TBackgroundWorker<TObjectList<TCustomer>>.Execute(
  function: TObjectList<TCustomer>
  begin
    Result := FCustomerRepo.FindAll;
  end,
  procedure(ACustomers: TObjectList<TCustomer>)
  begin
    FillGrid(ACustomers);
    lblStatus.Caption := Format('%d clientes carregados', [ACustomers.Count]);
  end,
  procedure(AError: Exception)
  begin
    ShowMessage('Erro: ' + AError.Message);
  end);
```

### Default: Timer Thread (Periodic Execution)

```pascal
type
  TTimerThread = class(TThread)
  private
    FInterval: Cardinal;
    FOnTimer: TProc;
  protected
    procedure Execute; override;
  public
    constructor Create(AIntervalMs: Cardinal; AOnTimer: TProc);
  end;

constructor TTimerThread.Create(AIntervalMs: Cardinal; AOnTimer: TProc);
begin
  inherited Create(True);
  FreeOnTerminate := False;
  FInterval := AIntervalMs;
  FOnTimer := AOnTimer;
end;

procedure TTimerThread.Execute;
begin
  while not Terminated do
  begin
    Sleep(FInterval);
    if not Terminated and Assigned(FOnTimer) then
      FOnTimer();
  end;
end;
```

## Anti-Patterns to Avoid

```pascal
//❌ NEVER access UI directly from secondary thread
TThread.CreateAnonymousThread(
  procedure
  begin
    lblStatus.Caption := 'Processando...';  //CRASH or unpredictable behavior!
  end).Start;

//✅ ALWAYS use Synchronize/Queue for UI
TThread.CreateAnonymousThread(
  procedure
  begin
    TThread.Queue(nil,
      procedure
      begin
        lblStatus.Caption := 'Processando...';  //Safe!
      end);
  end).Start;

//❌ NEVER create thread with FreeOnTerminate=True and keep reference
FMyThread := TMyThread.Create(True);
FMyThread.FreeOnTerminate := True;
FMyThread.Start;
//... after
FMyThread.WaitFor;  //CRASH! The object may have already been released!

//✅ If you need WaitFor, DO NOT use FreeOnTerminate
FMyThread := TMyThread.Create(True);
FMyThread.FreeOnTerminate := False;
FMyThread.Start;
//... after
FMyThread.WaitFor;
FMyThread.Free;

//❌ NEVER access shared variables without protection
Inc(FSharedCounter);  //Race condition!

//✅ ALWAYS secure shared access
TInterlocked.Increment(FSharedCounter);  //Atomic!
// ou
FLock.Enter;
try
  Inc(FSharedCounter);
finally
  FLock.Leave;
end;

//❌ NEVER use Sleep() in the main thread
Sleep(5000);  //Freeze UI for 5 seconds!

//✅ Move heavy work to thread
TTask.Run(
  procedure
  begin
    Sleep(5000);  //OK in secondary thread
    TThread.Queue(nil,
      procedure
      begin
        lblStatus.Caption := 'Concluído';
      end);
  end);

//❌ NEVER ignore exceptions in threads (they are silent!)
TThread.CreateAnonymousThread(
  procedure
  begin
    RiskyOperation;  //If you throw an exception, no one will know!
  end).Start;

//✅ ALWAYS handle exceptions in threads
TThread.CreateAnonymousThread(
  procedure
  begin
    try
      RiskyOperation;
    except
      on E: Exception do
        TThread.Queue(nil,
          procedure
          begin
            HandleError(E.Message);
          end);
    end;
  end).Start;
```

## Thread Debugging

### Name Threads (Facilitates Debug)

```pascal
TThread.CreateAnonymousThread(
  procedure
  begin
    TThread.NameThreadForDebugging('DataLoader');
    //...code
  end).Start;

{ Para TThread herdado: }
procedure TMyThread.Execute;
begin
  TThread.NameThreadForDebugging('MyWorker_' + FId.ToString);
  // ...
end;
```

### Thread Window in IDE

- **View → Debug Windows → Threads:** Lists all active threads
- Each named thread appears with its custom name
- Useful for identifying deadlocks and race conditions

## Threading Checklist

- [ ] Are heavy operations on secondary threads (not the main thread)?
- [ ] Does every UI update use `Synchronize` or `Queue`?
- [ ] Shared variables protected with locks (`TCriticalSection`, `TMonitor`, `TInterlocked`)?
- [ ] `FreeOnTerminate` configured correctly (True for fire-and-forget, False if you need WaitFor)?
- [ ] Threads check `Terminated` in loops for graceful cancellation?
- [ ] Exceptions handled within threads (do not propagate silently)?
- [ ] Threads named with `NameThreadForDebugging` to facilitate debugging?
- [ ] `TCriticalSection.Leave` always on `finally`?
- [ ] Without `Sleep()` in the main thread?
- [ ] No deadlocks (locks nested in the same order)?
