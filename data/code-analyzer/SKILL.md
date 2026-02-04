---
name: code-analyzer
description: Análise estática de código para identificar code smells, complexidade ciclomática, duplicações, violações de padrões, acoplamento excessivo, e métricas de qualidade. Usar para avaliar qualidade de código, identificar pontos de refatoração, medir débito técnico, verificar aderência a padrões PSR/SOLID, e gerar relatórios de qualidade para gestão.
---

# Code Analyzer

Skill para análise estática e métricas de qualidade de código PHP.

## Métricas Principais

| Métrica | Ideal | Alerta | Crítico |
|---------|-------|--------|---------|
| Complexidade Ciclomática | ≤10 | 11-20 | >20 |
| Linhas por Método | ≤20 | 21-50 | >50 |
| Linhas por Classe | ≤200 | 201-500 | >500 |
| Parâmetros por Método | ≤4 | 5-7 | >7 |
| Profundidade de Herança | ≤3 | 4-5 | >5 |
| Acoplamento Aferente (Ca) | ≤20 | 21-40 | >40 |
| Acoplamento Eferente (Ce) | ≤20 | 21-40 | >40 |

## Code Smells Comuns

### 1. God Class (Classe Deus)

```php
// ❌ SMELL: Classe faz muitas coisas
class UserManager
{
    public function create() { }
    public function update() { }
    public function delete() { }
    public function sendEmail() { }        // Responsabilidade de Email
    public function generateReport() { }   // Responsabilidade de Report
    public function processPayment() { }   // Responsabilidade de Payment
    public function exportToCsv() { }      // Responsabilidade de Export
}

// ✅ SOLUÇÃO: Separar responsabilidades
class UserService { }
class UserEmailService { }
class UserReportService { }
class PaymentService { }
class UserExporter { }
```

### 2. Long Method

```php
// ❌ SMELL: Método com 100+ linhas
public function processOrder($data)
{
    // validação (20 linhas)
    // cálculo de preço (30 linhas)
    // aplicar desconto (15 linhas)
    // processar pagamento (25 linhas)
    // enviar notificações (20 linhas)
}

// ✅ SOLUÇÃO: Extrair métodos
public function processOrder(OrderData $data): Order
{
    $this->validateOrder($data);
    $order = $this->createOrder($data);
    $order = $this->applyPricing($order);
    $this->processPayment($order);
    $this->notifyStakeholders($order);
    return $order;
}
```

### 3. Feature Envy

```php
// ❌ SMELL: Método usa mais dados de outra classe
class OrderProcessor
{
    public function calculateTotal(Order $order)
    {
        return $order->getPrice() 
             + $order->getTax() 
             - $order->getDiscount() 
             + $order->getShipping();
    }
}

// ✅ SOLUÇÃO: Mover lógica para classe dona dos dados
class Order
{
    public function calculateTotal(): float
    {
        return $this->price + $this->tax - $this->discount + $this->shipping;
    }
}
```

### 4. Primitive Obsession

```php
// ❌ SMELL: Usar primitivos para conceitos de domínio
function createUser(string $email, string $cpf, string $phone) { }

// ✅ SOLUÇÃO: Value Objects
function createUser(Email $email, Cpf $cpf, Phone $phone) { }

readonly class Email
{
    public function __construct(public string $value)
    {
        if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {
            throw new InvalidArgumentException('Email inválido');
        }
    }
}
```

### 5. Excessive Parameters

```php
// ❌ SMELL: Muitos parâmetros
function createContract(
    $clientId, $value, $date, $status, 
    $notes, $category, $paymentMethod, $installments
) { }

// ✅ SOLUÇÃO: Parameter Object
function createContract(CreateContractDTO $data) { }

readonly class CreateContractDTO
{
    public function __construct(
        public int $clientId,
        public float $value,
        public DateTime $date,
        public string $status = 'pending',
        public ?string $notes = null,
        public ?string $category = null,
        public string $paymentMethod = 'boleto',
        public int $installments = 1,
    ) {}
}
```

### 6. Deep Nesting

```php
// ❌ SMELL: Aninhamento profundo
if ($user) {
    if ($user->isActive()) {
        if ($user->hasPermission('edit')) {
            if ($contract->status === 'pending') {
                if ($contract->value > 0) {
                    // lógica
                }
            }
        }
    }
}

// ✅ SOLUÇÃO: Early returns / Guard clauses
if (!$user || !$user->isActive()) {
    return;
}

if (!$user->hasPermission('edit')) {
    throw new UnauthorizedException();
}

if ($contract->status !== 'pending' || $contract->value <= 0) {
    return;
}

// lógica
```

### 7. Duplicate Code

```php
// ❌ SMELL: Código duplicado em múltiplos lugares
// Em ContractController
$total = 0;
foreach ($contracts as $c) {
    $total += $c->value;
}

// Em ReportService (mesmo código)
$total = 0;
foreach ($contracts as $c) {
    $total += $c->value;
}

// ✅ SOLUÇÃO: Extrair para método reutilizável
// Em Contract (Collection macro ou método)
public static function calculateTotal(Collection $contracts): float
{
    return $contracts->sum('value');
}
```

## Análise por Comando

```bash
# PHPStan - Análise estática
./vendor/bin/phpstan analyse src --level=8

# PHPMD - Mess Detector
./vendor/bin/phpmd src text cleancode,codesize,controversial,design,naming,unusedcode

# PHP_CodeSniffer - Padrões PSR
./vendor/bin/phpcs src --standard=PSR12

# PHPLOC - Métricas de tamanho
./vendor/bin/phploc src

# PHP Copy/Paste Detector
./vendor/bin/phpcpd src
```

## Checklist de Análise

```markdown
## Análise de Código - [PROJETO]

### Estrutura
- [ ] Classes seguem Single Responsibility
- [ ] Métodos têm ≤20 linhas em média
- [ ] Complexidade ciclomática ≤10
- [ ] Sem duplicação significativa

### Padrões
- [ ] PSR-4 autoload
- [ ] PSR-12 coding style
- [ ] Type hints em parâmetros e retornos
- [ ] Documentação PHPDoc onde necessário

### Acoplamento
- [ ] Dependency Injection utilizada
- [ ] Interfaces para abstrações
- [ ] Sem dependências circulares
- [ ] Sem uso de global/static desnecessário

### Smells Identificados
| Arquivo | Linha | Smell | Severidade |
|---------|-------|-------|------------|
| ... | ... | ... | ... |
```

## Output: Relatório de Qualidade

```markdown
# Relatório de Qualidade - [PROJETO]

## Métricas Gerais
- Linhas de código: 15,420
- Classes: 89
- Métodos: 456
- Complexidade média: 8.2

## Distribuição de Complexidade
- Baixa (≤10): 380 métodos (83%)
- Média (11-20): 62 métodos (14%)
- Alta (>20): 14 métodos (3%)

## Top 10 Métodos Críticos
| Método | Complexidade | Linhas | Arquivo |
|--------|--------------|--------|---------|
| ... | ... | ... | ... |

## Recomendações Priorizadas
1. [CRÍTICO] Refatorar UserController::process() - CC=35
2. [ALTO] Extrair lógica de OrderService
3. [MÉDIO] Adicionar types em legacy/
```
