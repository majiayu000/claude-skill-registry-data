---
name: code-quality-standards
description: Code quality standards including SOLID principles, design patterns, code smells, refactoring techniques, naming conventions, and technical debt management. Use when reviewing code, refactoring, ensuring quality, or detecting code smells.
---

# Code Quality Standards

This skill provides comprehensive guidance for writing clean, maintainable, and high-quality code.

## SOLID Principles

### S - Single Responsibility Principle

**Definition**: A class should have only one reason to change.

```typescript
// ❌ BAD - Multiple responsibilities
class UserManager {
  createUser(data: UserData) {
    // Validation logic
    if (!data.email.includes('@')) throw new Error('Invalid email');

    // Database logic
    const user = database.insert('users', data);

    // Email logic
    emailService.send(data.email, 'Welcome!');

    // Logging logic
    logger.info(`User created: ${data.email}`);

    return user;
  }
}

// ✅ GOOD - Single responsibility per class
class UserValidator {
  validate(data: UserData): void {
    if (!data.email.includes('@')) {
      throw new Error('Invalid email');
    }
  }
}

class UserRepository {
  create(data: UserData): User {
    return database.insert('users', data);
  }
}

class UserNotificationService {
  sendWelcomeEmail(email: string): void {
    emailService.send(email, 'Welcome!');
  }
}

class UserService {
  constructor(
    private validator: UserValidator,
    private repository: UserRepository,
    private notificationService: UserNotificationService,
    private logger: Logger
  ) {}

  async createUser(data: UserData): Promise<User> {
    this.validator.validate(data);
    const user = await this.repository.create(data);
    await this.notificationService.sendWelcomeEmail(user.email);
    this.logger.info(`User created: ${user.email}`);
    return user;
  }
}
```

### O - Open/Closed Principle

**Definition**: Classes should be open for extension but closed for modification.

```typescript
// ❌ BAD - Must modify class to add new payment methods
class PaymentProcessor {
  process(type: string, amount: number) {
    if (type === 'credit_card') {
      // Process credit card
    } else if (type === 'paypal') {
      // Process PayPal
    } else if (type === 'bitcoin') {
      // Process Bitcoin
    }
  }
}

// ✅ GOOD - Can extend without modifying
interface PaymentMethod {
  process(amount: number): Promise<PaymentResult>;
}

class CreditCardPayment implements PaymentMethod {
  async process(amount: number): Promise<PaymentResult> {
    // Process credit card
    return { success: true };
  }
}

class PayPalPayment implements PaymentMethod {
  async process(amount: number): Promise<PaymentResult> {
    // Process PayPal
    return { success: true };
  }
}

class PaymentProcessor {
  async process(method: PaymentMethod, amount: number): Promise<PaymentResult> {
    return await method.process(amount);
  }
}

// Add new payment method without modifying existing code
class BitcoinPayment implements PaymentMethod {
  async process(amount: number): Promise<PaymentResult> {
    // Process Bitcoin
    return { success: true };
  }
}
```

### L - Liskov Substitution Principle

**Definition**: Subtypes must be substitutable for their base types.

```typescript
// ❌ BAD - Violates LSP
class Rectangle {
  constructor(protected width: number, protected height: number) {}

  setWidth(width: number) {
    this.width = width;
  }

  setHeight(height: number) {
    this.height = height;
  }

  getArea(): number {
    return this.width * this.height;
  }
}

class Square extends Rectangle {
  setWidth(width: number) {
    this.width = width;
    this.height = width; // Violates expectation
  }

  setHeight(height: number) {
    this.width = height; // Violates expectation
    this.height = height;
  }
}

// ✅ GOOD - Separate abstractions
interface Shape {
  getArea(): number;
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}

  getArea(): number {
    return this.width * this.height;
  }
}

class Square implements Shape {
  constructor(private side: number) {}

  getArea(): number {
    return this.side * this.side;
  }
}
```

### I - Interface Segregation Principle

**Definition**: Clients shouldn't be forced to depend on interfaces they don't use.

```typescript
// ❌ BAD - Fat interface
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
  getPaid(): void;
}

class HumanWorker implements Worker {
  work() { /* ... */ }
  eat() { /* ... */ }
  sleep() { /* ... */ }
  getPaid() { /* ... */ }
}

class RobotWorker implements Worker {
  work() { /* ... */ }
  eat() { /* Not applicable */ }
  sleep() { /* Not applicable */ }
  getPaid() { /* Not applicable */ }
}

// ✅ GOOD - Segregated interfaces
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

interface Payable {
  getPaid(): void;
}

class HumanWorker implements Workable, Eatable, Sleepable, Payable {
  work() { /* ... */ }
  eat() { /* ... */ }
  sleep() { /* ... */ }
  getPaid() { /* ... */ }
}

class RobotWorker implements Workable {
  work() { /* ... */ }
}
```

### D - Dependency Inversion Principle

**Definition**: Depend on abstractions, not concretions.

```typescript
// ❌ BAD - Depends on concrete implementation
class UserService {
  private database = new MySQLDatabase(); // Tight coupling

  async getUser(id: string) {
    return this.database.query(`SELECT * FROM users WHERE id = ${id}`);
  }
}

// ✅ GOOD - Depends on abstraction
interface Database {
  query(sql: string): Promise<any>;
}

class MySQLDatabase implements Database {
  async query(sql: string): Promise<any> {
    // MySQL implementation
  }
}

class PostgreSQLDatabase implements Database {
  async query(sql: string): Promise<any> {
    // PostgreSQL implementation
  }
}

class UserService {
  constructor(private database: Database) {} // Dependency injection

  async getUser(id: string) {
    return this.database.query(`SELECT * FROM users WHERE id = ${id}`);
  }
}

// Can easily swap database implementations
const userService = new UserService(new PostgreSQLDatabase());
```

## DRY (Don't Repeat Yourself)

### Identifying Duplication

```typescript
// ❌ BAD - Repeated validation logic
function createUser(data: UserData) {
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  if (!data.password || data.password.length < 8) {
    throw new Error('Password too short');
  }
  // Create user
}

function updateUser(id: string, data: UserData) {
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  if (!data.password || data.password.length < 8) {
    throw new Error('Password too short');
  }
  // Update user
}

// ✅ GOOD - Extract common logic
function validateUserData(data: UserData): void {
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  if (!data.password || data.password.length < 8) {
    throw new Error('Password too short');
  }
}

function createUser(data: UserData) {
  validateUserData(data);
  // Create user
}

function updateUser(id: string, data: UserData) {
  validateUserData(data);
  // Update user
}
```

## KISS (Keep It Simple, Stupid)

```typescript
// ❌ BAD - Over-engineered
class NumberProcessor {
  private strategy: ProcessingStrategy;

  constructor(strategy: ProcessingStrategy) {
    this.strategy = strategy;
  }

  process(numbers: number[]): number[] {
    return this.strategy.execute(numbers);
  }
}

interface ProcessingStrategy {
  execute(numbers: number[]): number[];
}

class MultiplyByTwoStrategy implements ProcessingStrategy {
  execute(numbers: number[]): number[] {
    return numbers.map(n => n * 2);
  }
}

// ✅ GOOD - Simple and clear
function multiplyByTwo(numbers: number[]): number[] {
  return numbers.map(n => n * 2);
}
```

## YAGNI (You Aren't Gonna Need It)

```typescript
// ❌ BAD - Building features you might need
class User {
  id: string;
  email: string;
  name: string;

  // Future features that aren't needed yet
  preferences?: UserPreferences;
  badges?: Badge[];
  followers?: User[];
  following?: User[];
  achievements?: Achievement[];
  notifications?: Notification[];
}

// ✅ GOOD - Only what you need now
class User {
  id: string;
  email: string;
  name: string;
}

// Add features when actually needed
```

## Design Patterns

### Factory Pattern

```typescript
interface Animal {
  speak(): string;
}

class Dog implements Animal {
  speak(): string {
    return 'Woof!';
  }
}

class Cat implements Animal {
  speak(): string {
    return 'Meow!';
  }
}

class AnimalFactory {
  static create(type: 'dog' | 'cat'): Animal {
    switch (type) {
      case 'dog':
        return new Dog();
      case 'cat':
        return new Cat();
      default:
        throw new Error('Unknown animal type');
    }
  }
}

// Usage
const dog = AnimalFactory.create('dog');
console.log(dog.speak()); // "Woof!"
```

### Strategy Pattern

```typescript
interface SortStrategy {
  sort(data: number[]): number[];
}

class QuickSort implements SortStrategy {
  sort(data: number[]): number[] {
    // Quick sort implementation
    return data.sort((a, b) => a - b);
  }
}

class MergeSort implements SortStrategy {
  sort(data: number[]): number[] {
    // Merge sort implementation
    return data.sort((a, b) => a - b);
  }
}

class Sorter {
  constructor(private strategy: SortStrategy) {}

  setStrategy(strategy: SortStrategy) {
    this.strategy = strategy;
  }

  sort(data: number[]): number[] {
    return this.strategy.sort(data);
  }
}

// Usage
const sorter = new Sorter(new QuickSort());
sorter.sort([3, 1, 4, 1, 5]);

sorter.setStrategy(new MergeSort());
sorter.sort([3, 1, 4, 1, 5]);
```

### Observer Pattern

```typescript
interface Observer {
  update(data: any): void;
}

class Subject {
  private observers: Observer[] = [];

  attach(observer: Observer): void {
    this.observers.push(observer);
  }

  detach(observer: Observer): void {
    const index = this.observers.indexOf(observer);
    if (index > -1) {
      this.observers.splice(index, 1);
    }
  }

  notify(data: any): void {
    for (const observer of this.observers) {
      observer.update(data);
    }
  }
}

class EmailNotifier implements Observer {
  update(data: any): void {
    console.log(`Sending email: ${data}`);
  }
}

class SMSNotifier implements Observer {
  update(data: any): void {
    console.log(`Sending SMS: ${data}`);
  }
}

// Usage
const subject = new Subject();
subject.attach(new EmailNotifier());
subject.attach(new SMSNotifier());
subject.notify('New user registered!');
```

### Singleton Pattern

```typescript
class Database {
  private static instance: Database;
  private connection: any;

  private constructor() {
    // Private constructor prevents direct instantiation
    this.connection = this.createConnection();
  }

  static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }

  private createConnection() {
    // Create database connection
    return {};
  }

  query(sql: string) {
    // Execute query
  }
}

// Usage - Always returns same instance
const db1 = Database.getInstance();
const db2 = Database.getInstance();
console.log(db1 === db2); // true
```

## Code Smells and Detection

### Long Method

```typescript
// ❌ BAD - Method too long (>20 lines)
function processOrder(order: Order) {
  // Validate order (10 lines)
  // Calculate totals (15 lines)
  // Apply discounts (20 lines)
  // Process payment (25 lines)
  // Send confirmation (10 lines)
  // Update inventory (15 lines)
  // Log transaction (5 lines)
}

// ✅ GOOD - Extract methods
function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order);
  const discounted = applyDiscounts(total, order.promoCode);
  processPayment(discounted);
  sendConfirmation(order.email);
  updateInventory(order.items);
  logTransaction(order.id);
}
```

### Large Class

```typescript
// ❌ BAD - Too many responsibilities
class User {
  // User properties (20+ fields)
  // User validation (10 methods)
  // User persistence (10 methods)
  // User authentication (5 methods)
  // User notifications (5 methods)
  // User reporting (5 methods)
}

// ✅ GOOD - Split into focused classes
class User {
  id: string;
  email: string;
  name: string;
}

class UserValidator {
  validate(user: User): boolean { /* ... */ }
}

class UserRepository {
  save(user: User): Promise<void> { /* ... */ }
  find(id: string): Promise<User> { /* ... */ }
}

class UserAuthService {
  authenticate(credentials: Credentials): Promise<Token> { /* ... */ }
}
```

### Duplicate Code

```typescript
// ❌ BAD - Duplicated logic
function calculateEmployeeSalary(employee: Employee) {
  let salary = employee.baseSalary;
  salary += employee.baseSalary * 0.1; // 10% bonus
  salary += employee.baseSalary * 0.05; // 5% tax deduction
  return salary;
}

function calculateContractorSalary(contractor: Contractor) {
  let salary = contractor.baseSalary;
  salary += contractor.baseSalary * 0.1; // 10% bonus
  salary += contractor.baseSalary * 0.05; // 5% tax deduction
  return salary;
}

// ✅ GOOD - Extract common logic
function calculateSalary(baseSalary: number): number {
  let salary = baseSalary;
  salary += baseSalary * 0.1; // 10% bonus
  salary += baseSalary * 0.05; // 5% tax deduction
  return salary;
}

function calculateEmployeeSalary(employee: Employee) {
  return calculateSalary(employee.baseSalary);
}

function calculateContractorSalary(contractor: Contractor) {
  return calculateSalary(contractor.baseSalary);
}
```

### God Object

```typescript
// ❌ BAD - Knows/does too much
class Application {
  database: Database;
  emailService: EmailService;
  paymentProcessor: PaymentProcessor;

  createUser() { /* ... */ }
  sendEmail() { /* ... */ }
  processPayment() { /* ... */ }
  generateReport() { /* ... */ }
  validateInput() { /* ... */ }
  // ... 50 more methods
}

// ✅ GOOD - Focused classes
class UserService {
  createUser() { /* ... */ }
}

class NotificationService {
  sendEmail() { /* ... */ }
}

class PaymentService {
  processPayment() { /* ... */ }
}
```

## Refactoring Patterns

### Extract Method

```typescript
// Before
function printOwing(invoice: Invoice) {
  console.log('***********************');
  console.log('**** Customer Owes ****');
  console.log('***********************');

  let outstanding = 0;
  for (const order of invoice.orders) {
    outstanding += order.amount;
  }

  console.log(`Name: ${invoice.customer}`);
  console.log(`Amount: ${outstanding}`);
}

// After
function printOwing(invoice: Invoice) {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
  printDetails(invoice.customer, outstanding);
}

function printBanner() {
  console.log('***********************');
  console.log('**** Customer Owes ****');
  console.log('***********************');
}

function calculateOutstanding(invoice: Invoice): number {
  return invoice.orders.reduce((sum, order) => sum + order.amount, 0);
}

function printDetails(customer: string, outstanding: number) {
  console.log(`Name: ${customer}`);
  console.log(`Amount: ${outstanding}`);
}
```

### Introduce Parameter Object

```typescript
// Before
function createUser(
  firstName: string,
  lastName: string,
  email: string,
  phone: string,
  address: string,
  city: string,
  state: string,
  zip: string
) {
  // Too many parameters
}

// After
interface UserDetails {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  address: Address;
}

interface Address {
  street: string;
  city: string;
  state: string;
  zip: string;
}

function createUser(details: UserDetails) {
  // Much cleaner
}
```

### Replace Conditional with Polymorphism

```typescript
// Before
class Bird {
  type: 'european' | 'african' | 'norwegian';

  getSpeed(): number {
    switch (this.type) {
      case 'european':
        return 35;
      case 'african':
        return 40;
      case 'norwegian':
        return 24;
    }
  }
}

// After
abstract class Bird {
  abstract getSpeed(): number;
}

class EuropeanBird extends Bird {
  getSpeed(): number {
    return 35;
  }
}

class AfricanBird extends Bird {
  getSpeed(): number {
    return 40;
  }
}

class NorwegianBird extends Bird {
  getSpeed(): number {
    return 24;
  }
}
```

## Naming Conventions

### Variables

```typescript
// ✅ Descriptive, clear names
const userEmail = 'user@example.com';
const totalPrice = 100;
const isActive = true;
const hasPermission = false;

// ❌ Vague, unclear names
const e = 'user@example.com';
const temp = 100;
const flag = true;
const data = {};
```

### Functions

```typescript
// ✅ Verb + Noun for actions
function getUserById(id: string): User { /* ... */ }
function calculateTotalPrice(items: Item[]): number { /* ... */ }
function isValidEmail(email: string): boolean { /* ... */ }
function hasPermission(user: User, resource: string): boolean { /* ... */ }

// ❌ Unclear names
function user(id: string): User { /* ... */ }
function price(items: Item[]): number { /* ... */ }
function email(email: string): boolean { /* ... */ }
```

### Classes

```typescript
// ✅ Noun or noun phrase
class UserRepository { /* ... */ }
class EmailValidator { /* ... */ }
class PaymentProcessor { /* ... */ }
class DatabaseConnection { /* ... */ }

// ❌ Vague or verb names
class Manager { /* ... */ }
class Handler { /* ... */ }
class Process { /* ... */ }
```

### Constants

```typescript
// ✅ SCREAMING_SNAKE_CASE for true constants
const MAX_RETRY_ATTEMPTS = 3;
const API_BASE_URL = 'https://api.example.com';
const DEFAULT_TIMEOUT_MS = 5000;

// ✅ camelCase for config objects
const databaseConfig = {
  host: 'localhost',
  port: 5432,
};
```

## Function/Method Size Guidelines

### Keep Functions Under 20 Lines

```typescript
// ❌ BAD - Too long (40+ lines)
function processOrder(order: Order) {
  // 40+ lines of logic
}

// ✅ GOOD - Split into smaller functions
function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order);
  const payment = processPayment(order, total);
  sendConfirmation(order, payment);
  updateInventory(order);
}

function validateOrder(order: Order) {
  // 5-10 lines
}

function calculateTotal(order: Order): number {
  // 5-10 lines
}
```

### Maximum 3-4 Parameters

```typescript
// ❌ BAD - Too many parameters
function createUser(
  firstName: string,
  lastName: string,
  email: string,
  phone: string,
  role: string,
  department: string
) { /* ... */ }

// ✅ GOOD - Use object parameter
interface CreateUserParams {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  role: string;
  department: string;
}

function createUser(params: CreateUserParams) { /* ... */ }
```

## Cyclomatic Complexity

### Keep Complexity Under 10

```typescript
// ❌ BAD - Complexity > 10
function calculatePrice(item: Item, user: User): number {
  let price = item.basePrice;

  if (user.isPremium) {
    price *= 0.9;
  }

  if (item.category === 'electronics') {
    if (item.brand === 'Apple') {
      price *= 1.2;
    } else if (item.brand === 'Samsung') {
      price *= 1.1;
    }
  }

  if (user.location === 'CA') {
    price *= 1.08;
  } else if (user.location === 'NY') {
    price *= 1.09;
  } else if (user.location === 'TX') {
    price *= 1.06;
  }

  return price;
}

// ✅ GOOD - Split into focused functions
function calculatePrice(item: Item, user: User): number {
  let price = item.basePrice;
  price = applyUserDiscount(price, user);
  price = applyBrandMarkup(price, item);
  price = applyLocationTax(price, user.location);
  return price;
}

function applyUserDiscount(price: number, user: User): number {
  return user.isPremium ? price * 0.9 : price;
}

function applyBrandMarkup(price: number, item: Item): number {
  const markups = {
    'Apple': 1.2,
    'Samsung': 1.1,
  };
  return item.category === 'electronics'
    ? price * (markups[item.brand] || 1)
    : price;
}

function applyLocationTax(price: number, location: string): number {
  const taxRates = {
    'CA': 1.08,
    'NY': 1.09,
    'TX': 1.06,
  };
  return price * (taxRates[location] || 1);
}
```

## Technical Debt Management

### Document Technical Debt

```typescript
/**
 * TODO: Refactor this function - it's too complex
 * DEBT: Using deprecated API, need to migrate to v2
 * HACK: Workaround for bug in third-party library
 * FIXME: Race condition occurs under heavy load
 * OPTIMIZE: Query is slow, add database index
 */
```

### Track in Issue Tracker

```markdown
## Technical Debt Items

### High Priority
- [ ] Refactor UserService - violates SRP (Est: 8h)
- [ ] Replace deprecated payment API (Est: 16h)
- [ ] Fix race condition in order processing (Est: 4h)

### Medium Priority
- [ ] Optimize slow database queries (Est: 8h)
- [ ] Add missing unit tests for AuthService (Est: 6h)

### Low Priority
- [ ] Improve error messages (Est: 2h)
- [ ] Update documentation (Est: 4h)
```

### Allocate Time for Refactoring

**20% Rule**: Spend 20% of sprint capacity on technical debt
- 4 out of 10 story points
- 1 out of 5 days per sprint
- Prevents debt from accumulating

## Code Review Checklist

**Functionality**:
- [ ] Code does what it's supposed to do
- [ ] Edge cases handled
- [ ] Error handling in place

**Design**:
- [ ] Follows SOLID principles
- [ ] No code smells
- [ ] Appropriate design patterns used

**Readability**:
- [ ] Clear naming conventions
- [ ] Functions under 20 lines
- [ ] Cyclomatic complexity under 10
- [ ] Comments explain "why" not "what"

**Tests**:
- [ ] Unit tests added/updated
- [ ] Test coverage adequate
- [ ] Tests follow AAA pattern

**Performance**:
- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] No N+1 query problems

**Security**:
- [ ] Input validation in place
- [ ] No SQL injection vulnerabilities
- [ ] Secrets not hardcoded

## When to Use This Skill

Use this skill when:
- Reviewing code in pull requests
- Refactoring existing code
- Setting code standards for team
- Onboarding new developers
- Conducting code quality audits
- Planning technical debt reduction
- Designing new features
- Improving codebase maintainability
- Training team on best practices
- Establishing coding guidelines

---

**Remember**: Code quality is not about perfection, but about maintainability. Write code that your future self and team members will thank you for.
