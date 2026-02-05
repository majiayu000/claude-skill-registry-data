---
name: "NestJS Architect"
description: "Guia arquitetural para desenvolvimento NestJS com DDD, Clean Architecture e padrões avançados. Use quando codificar serviços, módulos, agregados, use cases ou refatorar código NestJS."
---

# NestJS Architect Skill

## Objetivo

Esta skill fornece diretrizes arquiteturais e padrões de código para projetos NestJS que implementam **Domain-Driven Design (DDD)** e **Clean Architecture**. Quando ativada, Claude Code deve seguir rigorosamente os padrões documentados neste projeto.

## Quando usar

- Criação de novos agregados, entidades ou value objects
- Implementação de use cases e services de aplicação
- Refatoração de código existente para seguir padrões DDD
- Integração de módulos NestJS com camada de domínio
- Configuração de repositórios, providers e injeção de dependência
- Revisão de arquitetura e identificação de anti-patterns
- Implementação de specifications e regras de negócio
- Configuração de testes unitários e de integração

## Entradas esperadas

- `codigo_fonte`: Arquivos NestJS (controllers, services, modules, domain entities)
- `escopo_tarefa`: Descrição do que deve ser implementado ou refatorado
- `contexto_dominio`: Informações sobre o agregado ou bounded context
- `requisitos_tecnicos`: Requisitos de validação, persistência ou infraestrutura

## Saídas esperadas

- Código NestJS seguindo padrões DDD e Clean Architecture
- Estrutura de diretórios apropriada (core/ e nest-modules/)
- Testes unitários e de integração
- Documentação de decisões arquiteturais quando relevante

---

## 🏗️ PRINCÍPIOS ARQUITETURAIS FUNDAMENTAIS

### 1. Separação de Camadas (Clean Architecture)

**REGRA CRÍTICA**: Domínio NUNCA importa framework ou infraestrutura.

```typescript
// ❌ ERRADO - Framework no domínio
import { Injectable } from '@nestjs/common';

export class Category extends AggregateRoot {
  // Violação: @Injectable no domínio
}

// ✅ CORRETO - Domínio puro
export class Category extends AggregateRoot {
  static create(props: CategoryCreateCommand): Category {
    const category = new Category(props);
    category.validate(['name']);
    return category;
  }
}
```

### 2. Estrutura de Diretórios Obrigatória

```
src/
├── core/                          # Domain & Application Layer
│   ├── {aggregate}/
│   │   ├── domain/                # Regras de negócio puras
│   │   │   ├── {aggregate}.aggregate.ts
│   │   │   ├── {aggregate}.repository.ts (interface)
│   │   │   ├── {aggregate}-id.vo.ts
│   │   │   └── {aggregate}-fake.builder.ts
│   │   ├── application/           # Casos de uso
│   │   │   ├── use-cases/
│   │   │   │   └── {action}-{aggregate}/
│   │   │   │       ├── {action}-{aggregate}.use-case.ts
│   │   │   │       ├── {action}-{aggregate}.input.ts
│   │   │   │       └── __tests__/
│   │   │   └── validations/
│   │   └── infra/                 # Adaptadores
│   │       └── db/
│   │           ├── sequelize/     # ou prisma/
│   │           └── in-memory/
│   └── shared/
│       ├── domain/                # Building blocks do DDD
│       ├── application/
│       └── infra/
│
└── nest-modules/                  # Infrastructure Layer (Framework)
    ├── {aggregate}-module/
    │   ├── {aggregate}.controller.ts
    │   ├── {aggregate}.providers.ts
    │   ├── {aggregate}.presenter.ts
    │   ├── {aggregate}.module.ts
    │   └── dto/
    └── shared-module/
```

---

## 🧱 BUILDING BLOCKS DO DDD

### Aggregate Roots

Todo aggregate deve estender `AggregateRoot` e implementar Event Sourcing local:

```typescript
export class Category extends AggregateRoot {
  category_id: CategoryId;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: Date;

  // Factory method como ponto de entrada
  static create(props: CategoryCreateCommand): Category {
    const category = new Category(props);
    category.validate(['name']);
    category.applyEvent(new CategoryCreatedEvent(category));
    return category;
  }

  // Métodos de negócio que alteram estado
  changeName(name: string): void {
    this.name = name;
    this.validate(['name']);
    this.applyEvent(new CategoryNameChangedEvent(this));
  }

  activate(): void {
    this.is_active = true;
  }

  deactivate(): void {
    this.is_active = false;
  }

  // Validação centralizada
  validate(fields?: string[]) {
    const validator = CategoryValidatorFactory.create();
    return validator.validate(this.notification, this, fields);
  }

  get entity_id(): ValueObject {
    return this.category_id;
  }

  toJSON() {
    return {
      category_id: this.category_id.id,
      name: this.name,
      description: this.description,
      is_active: this.is_active,
      created_at: this.created_at,
    };
  }
}
```

### Value Objects

**CARACTERÍSTICAS OBRIGATÓRIAS**:

- Imutabilidade (`readonly`)
- Validação no construtor
- Fail-fast para valores inválidos

```typescript
export class CategoryId extends Uuid {
  // Herda validação da classe Uuid base
}

export class Email extends ValueObject {
  readonly value: string;

  constructor(email: string) {
    super();
    this.value = email;
    this.validate();
  }

  private validate() {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.value)) {
      throw new InvalidEmailError(this.value);
    }
  }

  toString() {
    return this.value;
  }
}
```

### Repository Pattern

**Interface no domínio, implementações na infraestrutura**:

```typescript
// src/core/category/domain/category.repository.ts
export interface ICategoryRepository
  extends ISearchableRepository<Category, CategoryId> {
  // Interface no domínio, SEM dependências de infra
}

// src/core/category/infra/db/sequelize/category-sequelize.repository.ts
export class CategorySequelizeRepository implements ICategoryRepository {
  constructor(private categoryModel: typeof CategoryModel) {}

  async insert(entity: Category): Promise<void> {
    const model = CategoryModelMapper.toModel(entity);
    await this.categoryModel.create(model.toJSON());
  }

  async findById(id: CategoryId): Promise<Category | null> {
    const model = await this.categoryModel.findByPk(id.id);
    return model ? CategoryModelMapper.toEntity(model) : null;
  }

  async update(entity: Category): Promise<void> {
    const model = CategoryModelMapper.toModel(entity);
    await this.categoryModel.update(model.toJSON(), {
      where: { category_id: entity.category_id.id },
    });
  }
}

// src/core/category/infra/db/in-memory/category-in-memory.repository.ts
export class CategoryInMemoryRepository implements ICategoryRepository {
  items: Category[] = [];

  async insert(entity: Category): Promise<void> {
    this.items.push(entity);
  }

  async findById(id: CategoryId): Promise<Category | null> {
    return this.items.find((item) => item.category_id.equals(id)) || null;
  }
}
```

---

## 🎯 APPLICATION LAYER (USE CASES)

### Use Case Pattern

**Características obrigatórias**:

- Uma responsabilidade por use case
- Interface explícita `IUseCase<Input, Output>`
- Validação com Notification Pattern
- Mapper para saída

```typescript
export class CreateCategoryUseCase
  implements IUseCase<CreateCategoryInput, CreateCategoryOutput> {

  constructor(private readonly categoryRepo: ICategoryRepository) {}

  async execute(input: CreateCategoryInput): Promise<CreateCategoryOutput> {
    // 1. Criar entidade de domínio
    const entity = Category.create(input);

    // 2. Validar com Notification Pattern
    if (entity.notification.hasErrors()) {
      throw new EntityValidationError(entity.notification.toJSON());
    }

    // 3. Persistir
    await this.categoryRepo.insert(entity);

    // 4. Mapear para output
    return CategoryOutputMapper.toOutput(entity);
  }
}
```

### Validação Cruzada entre Agregados

Use validators na camada de aplicação para verificar consistência entre agregados:

```typescript
export class CategoriesIdExistsInDatabaseValidator {
  constructor(private categoryRepo: ICategoryRepository) {}

  async validate(
    categories_id: string[]
  ): Promise<Either<CategoryId[], NotFoundError[]>> {
    const categoriesIdValueObjects = categories_id.map(
      (v) => new CategoryId(v)
    );

    const existsResult =
      await this.categoryRepo.existsById(categoriesIdValueObjects);

    return existsResult.not_exists.length > 0
      ? Either.fail(
          existsResult.not_exists.map(
            (c) => new NotFoundError(c.id, Category)
          )
        )
      : Either.ok(categoriesIdValueObjects);
  }
}
```

---

## 🔌 INTEGRAÇÃO COM NESTJS

### Providers Pattern

**Organização obrigatória**: REPOSITORIES, USE_CASES, VALIDATIONS

```typescript
// src/nest-modules/categories-module/categories.providers.ts
export const REPOSITORIES = {
  CATEGORY_REPOSITORY: {
    provide: 'CategoryRepository',
    useExisting: CategorySequelizeRepository,
  },
  CATEGORY_SEQUELIZE_REPOSITORY: {
    provide: CategorySequelizeRepository,
    useFactory: (categoryModel: typeof CategoryModel) => {
      return new CategorySequelizeRepository(categoryModel);
    },
    inject: [getModelToken(CategoryModel)],
  },
};

export const USE_CASES = {
  CREATE_CATEGORY_USE_CASE: {
    provide: CreateCategoryUseCase,
    useFactory: (categoryRepo: ICategoryRepository) => {
      return new CreateCategoryUseCase(categoryRepo);
    },
    inject: [REPOSITORIES.CATEGORY_REPOSITORY.provide],
  },
  UPDATE_CATEGORY_USE_CASE: {
    provide: UpdateCategoryUseCase,
    useFactory: (categoryRepo: ICategoryRepository) => {
      return new UpdateCategoryUseCase(categoryRepo);
    },
    inject: [REPOSITORIES.CATEGORY_REPOSITORY.provide],
  },
};

export const VALIDATIONS = {
  CATEGORIES_IDS_EXISTS_IN_DATABASE_VALIDATOR: {
    provide: CategoriesIdExistsInDatabaseValidator,
    useFactory: (categoryRepo: ICategoryRepository) => {
      return new CategoriesIdExistsInDatabaseValidator(categoryRepo);
    },
    inject: [REPOSITORIES.CATEGORY_REPOSITORY.provide],
  },
};

export const CATEGORY_PROVIDERS = {
  REPOSITORIES,
  USE_CASES,
  VALIDATIONS,
};
```

### Module Structure

```typescript
@Module({
  imports: [SequelizeModule.forFeature([CategoryModel])],
  controllers: [CategoriesController],
  providers: [
    ...Object.values(CATEGORY_PROVIDERS.REPOSITORIES),
    ...Object.values(CATEGORY_PROVIDERS.USE_CASES),
    ...Object.values(CATEGORY_PROVIDERS.VALIDATIONS),
  ],
  exports: [
    CATEGORY_PROVIDERS.REPOSITORIES.CATEGORY_REPOSITORY.provide,
    CATEGORY_PROVIDERS.VALIDATIONS.CATEGORIES_IDS_EXISTS_IN_DATABASE_VALIDATOR.provide,
  ],
})
export class CategoriesModule {}
```

### Controllers Finos

```typescript
@Controller('categories')
export class CategoriesController {
  @Inject(CreateCategoryUseCase)
  private createUseCase: CreateCategoryUseCase;

  @Inject(UpdateCategoryUseCase)
  private updateUseCase: UpdateCategoryUseCase;

  @Post()
  async create(@Body() createDto: CreateCategoryDto) {
    const output = await this.createUseCase.execute(createDto);
    return CategoriesController.serialize(output);
  }

  @Put(':id')
  async update(
    @Param('id') id: string,
    @Body() updateDto: UpdateCategoryDto
  ) {
    const output = await this.updateUseCase.execute({ id, ...updateDto });
    return CategoriesController.serialize(output);
  }

  static serialize(output: CategoryOutput) {
    return new CategoryPresenter(output);
  }
}
```

### DTOs com Validação

**OBRIGATÓRIO**: Usar class-validator em todos os DTOs

```typescript
export class CreateCategoryDto {
  @IsString()
  @IsNotEmpty()
  name: string;

  @IsString()
  @IsOptional()
  description?: string;

  @IsBoolean()
  @IsOptional()
  is_active?: boolean;
}
```

### Presenters

```typescript
export class CategoryPresenter {
  id: string;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: Date;

  constructor(output: CategoryOutput) {
    this.id = output.id;
    this.name = output.name;
    this.description = output.description;
    this.is_active = output.is_active;
    this.created_at = output.created_at;
  }
}

export class CategoryCollectionPresenter {
  data: CategoryPresenter[];
  meta: PaginationMeta;

  constructor(output: ListCategoriesOutput) {
    this.data = output.items.map((i) => new CategoryPresenter(i));
    this.meta = {
      total: output.total,
      current_page: output.current_page,
      per_page: output.per_page,
      last_page: output.last_page,
    };
  }
}
```

---

## 🧪 PADRÕES DE TESTE

### Fake Builders

**OBRIGATÓRIO** para todos os agregados:

```typescript
export class CategoryFakeBuilder<TBuild = any> {
  private _category_id: CategoryId | undefined;
  private _name: PropOrFactory<string> = () => this.faker.commerce.productName();
  private _description: PropOrFactory<string | null> = () =>
    this.faker.commerce.productDescription();
  private _is_active: PropOrFactory<boolean> = () => true;

  static aCategory() {
    return new CategoryFakeBuilder<Category>();
  }

  static theCategories(countObjs: number) {
    return new CategoryFakeBuilder<Category[]>(countObjs);
  }

  withName(valueOrFactory: PropOrFactory<string>) {
    this._name = valueOrFactory;
    return this;
  }

  activate() {
    this._is_active = true;
    return this;
  }

  build(): TBuild {
    const categories = new Array(this.countObjs)
      .fill(undefined)
      .map(() => {
        const category = new Category({
          category_id: this._category_id ?? new CategoryId(),
          name: this.callFactory(this._name),
          description: this.callFactory(this._description),
          is_active: this.callFactory(this._is_active),
          created_at: new Date(),
        });
        category.validate();
        return category;
      });

    return this.countObjs === 1 ? categories[0] : categories;
  }
}
```

### Testes de Use Cases

```typescript
describe('CreateCategoryUseCase Integration Tests', () => {
  let useCase: CreateCategoryUseCase;
  let repository: CategoryInMemoryRepository;

  beforeEach(() => {
    repository = new CategoryInMemoryRepository();
    useCase = new CreateCategoryUseCase(repository);
  });

  it('should create a category', async () => {
    const output = await useCase.execute({
      name: 'Movie',
    });

    expect(output).toStrictEqual({
      id: repository.items[0].category_id.id,
      name: 'Movie',
      description: null,
      is_active: true,
      created_at: repository.items[0].created_at,
    });
  });

  it('should throw error when name is invalid', async () => {
    await expect(() =>
      useCase.execute({ name: 't'.repeat(256) })
    ).rejects.toThrow(EntityValidationError);
  });
});
```

---

## 🚨 SPECIFICATION PATTERN PARA REGRAS DE NEGÓCIO

Quando houver múltiplas regras combináveis:

```typescript
// Interface base
export interface IFraudSpecification {
  detectFraud(
    context: FraudSpecificationContext,
  ): Promise<FraudDetectionResult> | FraudDetectionResult;
}

// Implementações concretas
@Injectable()
export class FrequentHighValueSpecification implements IFraudSpecification {
  async detectFraud(context: FraudSpecificationContext) {
    // Lógica específica
    return { hasFraud: false };
  }
}

// Agregador (Chain of Responsibility)
@Injectable()
export class FraudAggregateSpecification implements IFraudSpecification {
  constructor(
    @Inject('FRAUD_SPECIFICATIONS')
    private specifications: IFraudSpecification[],
  ) {}

  async detectFraud(context: FraudSpecificationContext) {
    for (const specification of this.specifications) {
      const result = await specification.detectFraud(context);
      if (result.hasFraud) {
        return result;
      }
    }
    return { hasFraud: false };
  }
}

// Provider
{
  provide: 'FRAUD_SPECIFICATIONS',
  useFactory: (
    frequentHighValueSpec: FrequentHighValueSpecification,
    suspiciousAccountSpec: SuspiciousAccountSpecification,
  ) => [frequentHighValueSpec, suspiciousAccountSpec],
  inject: [
    FrequentHighValueSpecification,
    SuspiciousAccountSpecification,
  ],
}
```

---

## ⚠️ ANTI-PATTERNS A EVITAR

### ❌ 1. Framework no Domínio

```typescript
// ❌ NUNCA FAZER
import { Injectable } from '@nestjs/common';

export class Category extends AggregateRoot {
  // Decorators de framework no domínio
}
```

### ❌ 2. any[] em Genéricos

```typescript
// ❌ EVITAR
getEntity(): new (...args: any[]) => E;

// ✅ USAR
getEntity(): new (...args: unknown[]) => E;
```

### ❌ 3. Validação Comentada

```typescript
// ❌ NUNCA COMENTAR VALIDAÇÃO
static create(props: CategoryCreateCommand): Category {
  const category = new Category(props);
  //category.validate(); // ❌
  return category;
}
```

### ❌ 4. Value Objects Mutáveis

```typescript
// ❌ ERRADO
export class Email {
  value: string; // Mutável!

  setValue(newEmail: string) {
    this.value = newEmail;
  }
}

// ✅ CORRETO
export class Email {
  readonly value: string;

  constructor(email: string) {
    this.value = email;
    this.validate();
  }
}
```

---

## 📊 CHECKLIST DE QUALIDADE

Antes de marcar uma tarefa como completa, verificar:

### Arquitetura

- [ ] Domínio isolado do framework
- [ ] Use Cases na camada de aplicação
- [ ] Repository com interface no domínio
- [ ] Value Objects imutáveis
- [ ] Aggregates com Event Sourcing local
- [ ] Notification Pattern para validação

### NestJS Integration

- [ ] Providers organizados (REPOSITORIES, USE_CASES, VALIDATIONS)
- [ ] Controllers finos
- [ ] Presenters para serialização
- [ ] DTOs com class-validator
- [ ] Módulos com exports explícitos

### Testes

- [ ] Fake Builders criados
- [ ] In-Memory repositories
- [ ] Testes unitários (>80% cobertura)
- [ ] Testes de integração
- [ ] Testes de validação

### Qualidade

- [ ] TypeScript estrito
- [ ] ESLint + Prettier
- [ ] Sem `any` desnecessários
- [ ] Naming conventions
- [ ] Documentação quando necessário

---

## 🚀 QUICK START TEMPLATES

### Criar Novo Agregado

```bash
# 1. Estrutura de diretórios
mkdir -p src/core/{aggregate}/domain
mkdir -p src/core/{aggregate}/application/use-cases
mkdir -p src/core/{aggregate}/infra/db/{sequelize,in-memory}
mkdir -p src/nest-modules/{aggregate}-module/{dto,__tests__}

# 2. Criar arquivos base
touch src/core/{aggregate}/domain/{aggregate}.aggregate.ts
touch src/core/{aggregate}/domain/{aggregate}.repository.ts
touch src/core/{aggregate}/domain/{aggregate}-id.vo.ts
touch src/core/{aggregate}/infra/db/in-memory/{aggregate}-in-memory.repository.ts
touch src/nest-modules/{aggregate}-module/{aggregate}.controller.ts
touch src/nest-modules/{aggregate}-module/{aggregate}.module.ts
touch src/nest-modules/{aggregate}-module/{aggregate}.providers.ts
```

---

## 📚 REFERÊNCIAS

### Livros

- Domain-Driven Design - Eric Evans
- Implementing Domain-Driven Design - Vaughn Vernon
- Clean Architecture - Robert C. Martin

### Patterns

- Aggregate Root, Repository, Value Object, Specification
- Use Case Pattern, Notification Pattern
- Event Sourcing, Dependency Injection

---

## Restrições e Limites

- Esta skill se aplica a projetos NestJS com TypeScript
- Assume uso de ORM (Sequelize ou Prisma)
- Testes com Jest/Vitest
- Não cobre GraphQL, WebSockets ou microserviços (foco em REST)

---

**Versão**: 1.0
**Última Atualização**: 2025-01-18
**Status**: Documento Vivo - Atualizar conforme evoluções
