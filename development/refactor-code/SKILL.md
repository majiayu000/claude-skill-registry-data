---
name: refactor-code
description: Refactors code to improve readability, maintainability, performance, and adherence to best practices while preserving functionality
license: MIT
compatibility: All major programming languages
---

# Refactor Code Skill

Questa skill esegue refactoring professionale del codice, migliorando struttura, leggibilità e manutenibilità senza cambiare il comportamento esterno.

## Obiettivo

Trasformare codice esistente in codice migliore mantenendo la stessa funzionalità, con focus su:
- Clean Code principles
- SOLID principles
- Design Patterns appropriati
- Performance optimization
- Testability

## Processo di Refactoring

### 1. Analisi Pre-Refactoring

Prima di iniziare, valuta:

#### A. Problemi Attuali
- Code smells identificati
- Violazioni di best practices
- Performance bottlenecks
- Complessità eccessiva
- Code duplication

#### B. Obiettivi del Refactoring
- Cosa vogliamo migliorare specificamente?
- Quali sono i vincoli (backward compatibility, performance)?
- Ci sono test esistenti da preservare?

#### C. Rischio Assessment
- Quanto è critico il codice?
- Esistono test per validare il refactoring?
- Impatto su altri moduli?

### 2. Refactoring Patterns

Applica questi pattern comuni di refactoring:

#### A. Extract Method/Function
Quando: Funzione troppo lunga o con logica duplicata

```javascript
// ❌ Before
function processOrder(order) {
  // Validate order
  if (!order.items || order.items.length === 0) {
    throw new Error('Empty order');
  }
  if (!order.customerId) {
    throw new Error('Missing customer');
  }

  // Calculate total
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }

  // Apply discount
  if (order.coupon) {
    total = total * (1 - order.coupon.discount);
  }

  return total;
}

// ✅ After
function processOrder(order) {
  validateOrder(order);
  const subtotal = calculateTotal(order.items);
  return applyDiscount(subtotal, order.coupon);
}

function validateOrder(order) {
  if (!order.items?.length) throw new Error('Empty order');
  if (!order.customerId) throw new Error('Missing customer');
}

function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function applyDiscount(amount, coupon) {
  return coupon ? amount * (1 - coupon.discount) : amount;
}
```

#### B. Replace Magic Numbers with Constants

```javascript
// ❌ Before
if (user.age >= 18 && user.age < 65) {
  // ...
}

// ✅ After
const ADULT_AGE = 18;
const RETIREMENT_AGE = 65;

if (user.age >= ADULT_AGE && user.age < RETIREMENT_AGE) {
  // ...
}
```

#### C. Simplify Conditional Logic

```javascript
// ❌ Before
function getShippingCost(order) {
  if (order.total > 100) {
    return 0;
  } else {
    if (order.weight > 10) {
      return 15;
    } else {
      return 10;
    }
  }
}

// ✅ After
function getShippingCost(order) {
  if (order.total > 100) return 0;
  return order.weight > 10 ? 15 : 10;
}
```

#### D. Replace Type Code with Class/Enum

```javascript
// ❌ Before
const STATUS_PENDING = 1;
const STATUS_APPROVED = 2;
const STATUS_REJECTED = 3;

// ✅ After (TypeScript)
enum OrderStatus {
  Pending = 'pending',
  Approved = 'approved',
  Rejected = 'rejected'
}
```

#### E. Extract Class

Quando: Una classe ha troppo responsabilità

```javascript
// ❌ Before
class User {
  name: string;
  email: string;
  street: string;
  city: string;
  country: string;

  sendEmail() { /* ... */ }
  validateAddress() { /* ... */ }
}

// ✅ After
class Address {
  street: string;
  city: string;
  country: string;

  validate() { /* ... */ }
}

class User {
  name: string;
  email: string;
  address: Address;

  sendEmail() { /* ... */ }
}
```

#### F. Replace Nested Conditionals with Guard Clauses

```javascript
// ❌ Before
function calculateDiscount(user) {
  if (user) {
    if (user.isPremium) {
      if (user.orders > 10) {
        return 0.2;
      } else {
        return 0.1;
      }
    } else {
      return 0.05;
    }
  }
  return 0;
}

// ✅ After
function calculateDiscount(user) {
  if (!user) return 0;
  if (!user.isPremium) return 0.05;
  return user.orders > 10 ? 0.2 : 0.1;
}
```

#### G. Replace Loop with Functional Programming

```javascript
// ❌ Before
const activeUsers = [];
for (let i = 0; i < users.length; i++) {
  if (users[i].isActive) {
    activeUsers.push(users[i]);
  }
}

// ✅ After
const activeUsers = users.filter(user => user.isActive);
```

### 3. SOLID Principles Application

#### S - Single Responsibility Principle
Ogni classe/funzione deve avere una sola ragione per cambiare

#### O - Open/Closed Principle
Aperto per estensione, chiuso per modifica

#### L - Liskov Substitution Principle
Le sottoclassi devono essere sostituibili alle superclassi

#### I - Interface Segregation Principle
Interfacce piccole e specifiche invece di grandi e generiche

#### D - Dependency Inversion Principle
Dipendere da astrazioni, non da implementazioni concrete

### 4. Code Smells da Eliminare

- **Long Method**: Funzioni > 20 linee
- **Large Class**: Classi > 200 linee
- **Duplicate Code**: Logica ripetuta
- **Long Parameter List**: > 3-4 parametri
- **Feature Envy**: Metodo che usa troppo un'altra classe
- **Data Clumps**: Gruppi di dati che appaiono sempre insieme
- **Primitive Obsession**: Uso eccessivo di tipi primitivi
- **Switch Statements**: Sostituire con polimorfismo
- **Speculative Generality**: Codice "per il futuro" non necessario
- **Dead Code**: Codice mai usato

## Output Format

Presenta il refactoring in questo formato:

```
# Refactoring Report

## Analysis

### Current Issues
1. [Issue 1]
2. [Issue 2]
...

### Refactoring Goals
- [Goal 1]
- [Goal 2]

## Changes Made

### Change 1: [Title]
**Why**: [Reason for change]
**Impact**: [What improves]

\`\`\`[language]
// ❌ Before
[old code]

// ✅ After
[new code]
\`\`\`

### Change 2: [Title]
...

## Summary

- **Readability**: [How it improved]
- **Maintainability**: [How it improved]
- **Performance**: [If applicable]
- **Testability**: [How it improved]

## Testing Recommendations

[Suggest tests to verify refactoring didn't break functionality]

## Next Steps (Optional)

[Additional improvements that could be made]
```

## Best Practices

### 1. Refactor Incrementally
- Piccoli step, testando dopo ogni change
- Commit frequenti
- Un pattern alla volta

### 2. Maintain Behavior
- Il codice refactorato deve comportarsi ESATTAMENTE come prima
- Run tests dopo ogni modifica
- Se non ci sono test, considera di scriverli prima

### 3. Improve Names
- Nomi descrittivi e auto-esplicativi
- Evita abbreviazioni oscure
- Usa naming conventions del linguaggio

### 4. Reduce Complexity
- Cyclomatic complexity < 10
- Nesting depth < 4
- Function length < 30 linee

### 5. Balance
- Non over-engineer
- Refactoring deve portare valore tangibile
- Considera il trade-off tempo/beneficio

## Tools Raccomandati

- `read_file`: Per leggere codice da refactorare
- `write_file` o `edit_file`: Per applicare refactoring
- `bash`: Per eseguire test dopo refactoring
- `grep`: Per trovare code duplicato
- `todo_write`: Per tracciare progress in refactoring complessi

## Warnings

⚠️ **Attenzione**:
- Non refactorare e aggiungere features contemporaneamente
- Non refactorare senza test o modo di validare
- Non refactorare codice che sta per essere rimosso
- Comunicare con il team prima di large refactorings
