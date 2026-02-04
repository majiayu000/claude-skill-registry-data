---
name: vendure
description: Vendure e-commerce framework for Node.js. Use for headless commerce, GraphQL APIs, order management, product catalogs, payment integration, and TypeScript e-commerce development.
---

# Vendure Skill

Comprehensive assistance with Vendure development, generated from official documentation.

## When to Use This Skill

Trigger this skill when:
- **Building headless e-commerce** applications with Node.js/TypeScript
- **Working with GraphQL APIs** for products, orders, or customer management
- **Implementing payment integrations** (Stripe, custom payment handlers)
- **Creating custom plugins** or extending Vendure functionality
- **Setting up order workflows** and state machines
- **Developing Admin UI extensions** with React or Angular
- **Configuring multi-currency** or multi-channel stores
- **Debugging Vendure code** or troubleshooting e-commerce flows
- **Learning Vendure best practices** for TypeScript e-commerce development

## Quick Reference

### Common Patterns

**Pattern 1: Create a New Vendure Project**

The fastest way to get started with Vendure:

```bash
npx @vendure/create my-shop
```

This launches an interactive wizard:

```text
┌  Let's create a Vendure App ✨
│
│◆  How should we proceed?
│  ● Quick Start (Get up and running in a single step)
│  ○ Manual Configuration
│
└
```

---

**Pattern 2: Format Currency Values**

Vendure stores monetary values as integers (e.g., 100 = $1.00). Use this function to display them:

```typescript
export function formatCurrency(value: number, currencyCode: string, locale?: string) {
    const majorUnits = value / 100;
    try {
        return new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: currencyCode,
        }).format(majorUnits);
    } catch (e: any) {
        return majorUnits.toFixed(2);
    }
}
```

**Usage:**
```typescript
formatCurrency(2399, 'USD'); // "$23.99"
```

---

**Pattern 3: Create a Custom Payment Handler**

Integrate a payment provider with a PaymentMethodHandler:

```typescript
import { PaymentMethodHandler, CreatePaymentResult, SettlePaymentResult } from '@vendure/core';

const myPaymentHandler = new PaymentMethodHandler({
    code: 'my-payment-method',
    description: [{
        languageCode: LanguageCode.en,
        value: 'My Payment Provider',
    }],
    args: {
        apiKey: { type: 'string', label: 'API Key' },
    },

    createPayment: async (ctx, order, amount, args, metadata): Promise<CreatePaymentResult> => {
        // Integrate with payment provider SDK
        const result = await paymentProvider.authorize({
            amount,
            token: metadata.paymentToken,
            apiKey: args.apiKey,
        });

        return {
            amount,
            state: 'Authorized',
            transactionId: result.transactionId,
            metadata: result,
        };
    },

    settlePayment: async (ctx, order, payment, args): Promise<SettlePaymentResult> => {
        const result = await paymentProvider.capture(payment.transactionId);
        return { success: true };
    },
});
```

---

**Pattern 4: Email Event Handler**

Send emails when events occur (e.g., order confirmation):

```typescript
import { EmailEventListener } from '@vendure/email-plugin';
import { OrderStateTransitionEvent } from '@vendure/core';

const confirmationHandler = new EmailEventListener('order-confirmation')
    .on(OrderStateTransitionEvent)
    .filter(event => event.toState === 'PaymentSettled')
    .setRecipient(event => event.order.customer.emailAddress)
    .setFrom('{{ fromAddress }}')
    .setSubject(`Order confirmation for #{{ order.code }}`)
    .setTemplateVars(event => ({ order: event.order }));
```

Place template at: `<app root>/static/email/templates/order-confirmation/body.hbs`

---

**Pattern 5: Define a Custom Strategy Interface**

Create pluggable, extensible plugin behavior with strategies:

```typescript
import { InjectableStrategy, RequestContext } from '@vendure/core';

export interface MyCustomStrategy extends InjectableStrategy {
    /**
     * Process some data and return a result
     */
    processData(ctx: RequestContext, data: any): Promise<string>;

    /**
     * Validate the input data
     */
    validateInput(data: any): boolean;
}
```

**Default Implementation:**

```typescript
import { Injector, Logger } from '@vendure/core';

export class DefaultMyCustomStrategy implements MyCustomStrategy {
    private someService: SomeService;

    async init(injector: Injector): Promise<void> {
        this.someService = injector.get(SomeService);
        Logger.info('Strategy initialized');
    }

    async destroy(): Promise<void> {
        // Clean up resources
    }

    async processData(ctx: RequestContext, data: any): Promise<string> {
        if (!this.validateInput(data)) {
            throw new Error('Invalid input data');
        }
        return this.someService.process(data);
    }

    validateInput(data: any): boolean {
        return data != null && typeof data === 'object';
    }
}
```

---

**Pattern 6: Upload Files with Custom Mutation**

Allow customers to upload avatar images:

```typescript
import gql from 'graphql-tag';

// 1. Schema definition
export const shopApiExtensions = gql`
    extend type Mutation {
        setCustomerAvatar(file: Upload!): Asset
    }
`;

// 2. Resolver implementation
import { Args, Mutation, Resolver } from '@nestjs/graphql';
import { Allow, AssetService, Ctx, Permission, RequestContext, Transaction } from '@vendure/core';

@Resolver()
export class CustomerAvatarResolver {
    constructor(private assetService: AssetService) {}

    @Transaction()
    @Mutation()
    @Allow(Permission.Authenticated)
    async setCustomerAvatar(
        @Ctx() ctx: RequestContext,
        @Args() args: { file: any },
    ): Promise<Asset | undefined> {
        const asset = await this.assetService.create(ctx, {
            file: args.file,
            tags: ['customer-avatar'],
        });
        return asset;
    }
}
```

---

**Pattern 7: OrderInterceptor - Enforce Min/Max Quantity**

Prevent order operations based on custom validation logic:

```typescript
import { OrderInterceptor, WillAddItemToOrderInput, RequestContext, Order } from '@vendure/core';

export class MinMaxOrderInterceptor implements OrderInterceptor {
    willAddItemToOrder(
        ctx: RequestContext,
        order: Order,
        input: WillAddItemToOrderInput,
    ): Promise<void | string> | void | string {
        const { productVariant, quantity } = input;
        const min = productVariant.customFields?.minOrderQuantity;
        const max = productVariant.customFields?.maxOrderQuantity;

        if (min && quantity < min) {
            return `Minimum order quantity for "${productVariant.name}" is ${min}`;
        }
        if (max && quantity > max) {
            return `Maximum order quantity for "${productVariant.name}" is ${max}`;
        }
    }
}
```

---

**Pattern 8: GraphQL Query - Search Products**

Search for products with faceted filtering:

```typescript
import gql from 'graphql-tag';

const SEARCH_PRODUCTS = gql`
    query SearchProducts($input: SearchInput!) {
        search(input: $input) {
            totalItems
            facetValues {
                count
                facetValue {
                    id
                    name
                    facet {
                        id
                        name
                    }
                }
            }
            items {
                productId
                productName
                productAsset {
                    id
                    preview
                }
                slug
                featuredAsset {
                    preview
                }
                variants {
                    id
                    name
                    currencyCode
                    price
                    priceWithTax
                }
            }
        }
    }
`;
```

---

**Pattern 9: Money & Currency - Store Custom Entity Prices**

Use the `@Money()` decorator for monetary values:

```typescript
import { VendureEntity, Money, CurrencyCode, EntityId, ID } from '@vendure/core';
import { Column, Entity } from 'typeorm';

@Entity()
class Quote extends VendureEntity {
    @Column()
    text: string;

    @Money()
    value: number; // Stored as integer (cents)

    @Column('varchar')
    currencyCode: CurrencyCode;

    @EntityId()
    orderId: ID;
}
```

---

**Pattern 10: Install Vendure Dashboard**

Add the Admin UI to the project:

```bash
npm install @vendure/dashboard
```

Configure in `vendure-config.ts`:

```typescript
import { VendureConfig } from '@vendure/core';
import { DashboardPlugin } from '@vendure/dashboard';

export const config: VendureConfig = {
    plugins: [
        DashboardPlugin.init({
            route: 'admin',
            port: 3002,
        }),
    ],
};
```

## Key Concepts

Core Vendure architecture concepts (see `references/core_concepts.md` and `references/developer_guide.md` for detailed explanations):

- **Money & Currency** - Integer storage (100 = $1.00) avoids floating-point errors, multi-currency support at Channel level
- **Order State Machine** - Customizable workflow (AddingItems → Delivered) via OrderProcess with interceptors
- **Payment Flow** - Two-step (authorize/settle) or single-step via PaymentMethodHandler
- **Collections** - Organize products with filters, inheritance, and custom CollectionFilter logic
- **Custom Fields** - Add custom properties to entities via VendureConfig, automatically extend GraphQL schema, support relations and 10+ field types
- **Plugins** - Core extensibility via @VendurePlugin decorator, lifecycle hooks (onApplicationBootstrap, etc.), InjectableStrategy pattern for pluggable behavior

## Reference Files

This skill includes comprehensive documentation in `references/`:

### API Documentation (`api.md` - 800 pages)
Complete TypeScript API reference covering:
- **Core Entities**: Order, Product, Customer, Payment, Fulfillment
- **Services**: OrderService, ProductService, CustomerService, AssetService
- **Strategies**: PaymentMethodHandler, ShippingCalculator, TaxCalculationStrategy
- **Plugins**: EmailPlugin, AssetServerPlugin, StripePlugin, DashboardPlugin
- **Dashboard API**: React hooks (useLocalFormat, useWidgetFilters, useDetailPage), components, defineDashboardExtension
- **Admin UI**: Custom components, routes, alerts, navigation
- **GraphQL**: Schema types, queries, mutations, subscriptions

**Finding API components**: Use grep to locate specific classes:
```bash
grep -n "^## PaymentMethodHandler" references/api.md
grep -n "^## DashboardPlugin" references/api.md
grep -n "useLocalFormat" references/api.md
```

### Core Concepts (`core_concepts.md` - 16 pages)
Foundational architecture and patterns:
- **Collections**: Organizing products with filters and hierarchies
- **Money & Currency**: Integer storage, multi-currency support, formatting
- **Images & Assets**: AssetServerPlugin, transformations, storage strategies
- **Taxes**: Calculation, zones, categories, strategies
- **Payment**: Authorization, settlement, custom handlers

### Developer Guide (`developer_guide.md` - 48 pages)
Building and extending Vendure:
- **CLI**: Vendure CLI for scaffolding plugins, entities, services
- **Security**: OWASP assessment, HardenPlugin, best practices
- **File Uploads**: GraphQL multipart requests, custom upload mutations
- **Custom Strategies**: Creating pluggable plugin implementations
- **Migration**: V1 to V2 breaking changes, upgrade guide

### Getting Started (`getting_started.md`)
Quick start guides and initial setup:
- Creating a new project with `@vendure/create`
- Configuration basics
- First plugin creation
- Database setup

### How-To Guides (`how_to.md`)
Task-specific tutorials:
- Adding custom fields
- Creating custom payment integrations
- Building Admin UI extensions
- Implementing custom shipping calculators
- Multi-tenant setups

### Other Documentation (`other.md`)
Miscellaneous topics:
- **Dashboard Widgets**: Creating custom Insights page widgets with useWidgetFilters and DashboardBaseWidget
- **Relation Selectors**: Single/multi selection components for dashboard forms
- Deployment strategies
- Performance optimization
- Testing approaches
- Community resources

### User Guide (`user_guide.md`)
Admin UI usage and merchant workflows:
- Managing products and variants
- Processing orders
- Customer management
- Configuring shipping and taxes

Use the Read tool to access specific reference files when detailed information is needed.

## Working with This Skill

### Getting Started Workflow
1. **Start here**: Read `references/getting_started.md` for foundational setup
2. **Understand core concepts**: Review `references/core_concepts.md` for Money, Orders, Payment flows
3. **Build first features**: Follow Quick Reference patterns above
4. **Explore examples**: Check `references/developer_guide.md` for real-world implementations

### Intermediate Development Workflow
1. **Custom functionality**: Use `references/api.md` to find services and strategies
2. **Plugin development**: Reference "Custom Strategies in Plugins" pattern above
3. **Payment integration**: Follow Pattern 3 (Custom Payment Handler)
4. **Email workflows**: Implement Pattern 4 (Email Event Handler)

### Advanced Architecture Workflow
1. **Architecture decisions**: Study strategy patterns in `references/developer_guide.md`
2. **Performance**: Review caching, database optimization in `references/other.md`
3. **Security**: Consult OWASP assessment in `references/developer_guide.md`
4. **Complex state machines**: Custom OrderProcess, FulfillmentProcess implementations

### Navigation Tips
- **API lookup**: Search `references/api.md` for specific class/interface names
- **Code examples**: All reference files include real examples from official docs
- **Error troubleshooting**: Check pattern implementations for common gotchas
- **Version compatibility**: Note version indicators (e.g., "v3.1.0") in examples

## Common Tasks Quick Links

| Task | Quick Reference Pattern | Reference File |
|------|------------------------|----------------|
| Start new project | Pattern 1 | getting_started.md |
| Display prices | Pattern 2 | core_concepts.md (Money & Currency) |
| Accept payments | Pattern 3 | core_concepts.md (Payment) |
| Send emails | Pattern 4 | api.md (EmailPlugin) |
| Create plugin | Pattern 5 | developer_guide.md (Custom Strategies) |
| Upload files | Pattern 6 | developer_guide.md (Uploading Files) |
| Validate orders | Pattern 7 | api.md (OrderInterceptor) |
| Query products | Pattern 8 | api.md (GraphQL) |
| Store prices | Pattern 9 | core_concepts.md (Money) |
| Install Admin UI | Pattern 10 | getting_started.md |
| Dashboard widgets | - | other.md (Insights Widgets) |

## Resources

### references/
Organized documentation extracted from official Vendure docs (https://docs.vendure.io). These files contain:
- **Detailed explanations** of concepts and architecture
- **Real code examples** with TypeScript/GraphQL language annotations
- **Links to original documentation** for latest updates
- **Table of contents** for quick navigation within each category

### scripts/
Add helper scripts here for common Vendure automation tasks:
- Database seeding scripts
- Migration utilities
- Custom CLI commands
- Build/deployment automation

### assets/
Add templates, boilerplate, or example projects here:
- Plugin templates
- Custom field configurations
- Email templates (Handlebars)
- Admin UI component examples

## Notes

- This skill was automatically generated from official Vendure documentation (docs.vendure.io)
- Reference files preserve structure and examples from source docs (as of October 2025)
- Code examples include language detection for proper syntax highlighting
- Quick reference patterns extracted from most common usage examples in the docs
- All monetary values represented as integers (divide by 100 for display)
- GraphQL is the primary API interface (Shop API for storefront, Admin API for management)

## Updating

To refresh this skill with updated documentation:
1. Re-run the Skill Seeker scraper with the same Vendure configuration
2. The skill will be rebuilt with the latest information from docs.vendure.io
3. Enhancement can be re-applied to update Quick Reference with new patterns