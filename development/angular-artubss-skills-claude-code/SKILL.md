---
name: angular
description: Especialista em Angular moderno (v20+) com conhecimento profundo de Signals, Componentes Standalone, aplicações Zoneless, SSR/Hydration e padrões reativos.
risk: safe
source: self
date_added: '2026-02-27'
---

# Especialista em Angular

Domine o desenvolvimento moderno de Angular com Signals, Componentes Standalone, aplicações Zoneless, SSR/Hydration e os últimos padrões reativos.

## Quando Usar Esta Habilidade

- Construir novas aplicações Angular (v20+)
- Implementar padrões reativos baseados em Signals
- Criar Componentes Standalone e migrar de NgModules
- Configurar aplicações Angular Zoneless
- Implementar SSR, pré-renderização e hidratação
- Otimizar performance do Angular
- Adotar padrões e melhores práticas modernas do Angular

## Não Use Esta Habilidade Quando

- Migrar de AngularJS (1.x) → use a habilidade `angular-migration`
- Trabalhar com apps Angular legados que não podem ser atualizados
- Problemas gerais de TypeScript → use a habilidade `typescript-expert`

## Instruções

1. Avalie a versão do Angular e estrutura do projeto
2. Aplique padrões modernos (Signals, Standalone, Zoneless)
3. Implemente com tipagem apropriada e reatividade
4. Valide com build e testes

## Segurança

- Sempre teste mudanças em desenvolvimento antes de produção
- Migração gradual para apps existentes (evite big-bang refactor)
- Mantenha compatibilidade retroativa durante transições

---

## Timeline das Versões do Angular

| Versão         | Lançamento | Recursos-chave                              |
| -------------- | ---------- | ------------------------------------------- |
| **Angular 20** | Q2 2025    | Signals estável, Zoneless estável, hidratação incremental |
| **Angular 21** | Q4 2025    | Signals-first padrão, SSR aprimorado        |
| **Angular 22** | Q2 2026    | Signal Forms, componentes sem seletor       |

---

## 1. Signals: A Nova Primitiva Reativa

Signals são o sistema de reatividade fine-grained do Angular, substituindo a detecção de mudanças baseada em zone.js.

### Conceitos Principais

```typescript
import { signal, computed, effect } from "@angular/core";

// Sinal gravável
const count = signal(0);

// Ler valor
console.log(count()); // 0

// Atualizar valor
count.set(5); // Set direto
count.update((v) => v + 1); // Atualização funcional

// Sinal computado (derivado)
const doubled = computed(() => count() * 2);

// Effect (efeitos colaterais)
effect(() => {
  console.log(`Count alterado para: ${count()}`);
});
```

### Inputs e Outputs Baseados em Signals

```typescript
import { Component, input, output, model } from "@angular/core";

@Component({
  selector: "app-user-card",
  standalone: true,
  template: `
    <div class="card">
      <h3>{{ name() }}</h3>
      <span>{{ role() }}</span>
      <button (click)="select.emit(id())">Selecionar</button>
    </div>
  `,
})
export class UserCardComponent {
  // Inputs de sinal (somente leitura)
  id = input.required<string>();
  name = input.required<string>();
  role = input<string>("Usuário"); // Com padrão

  // Output
  select = output<string>();

  // Binding bidirecional (model)
  isSelected = model(false);
}

// Uso:
// <app-user-card [id]="'123'" [name]="'John'" [(isSelected)]="selected" />
```

### Consultas de Signal (ViewChild/ContentChild)

```typescript
import {
  Component,
  viewChild,
  viewChildren,
  contentChild,
} from "@angular/core";

@Component({
  selector: "app-container",
  standalone: true,
  template: `
    <input #searchInput />
    <app-item *ngFor="let item of items()" />
  `,
})
export class ContainerComponent {
  // Consultas baseadas em Signal
  searchInput = viewChild<ElementRef>("searchInput");
  items = viewChildren(ItemComponent);
  projectedContent = contentChild(HeaderDirective);

  focusSearch() {
    this.searchInput()?.nativeElement.focus();
  }
}
```

### Quando Usar Signals vs RxJS

| Caso de Uso                | Signals         | RxJS                             |
| -------------------------- | --------------- | -------------------------------- |
| Estado local do componente | ✅ Preferido    | Excessivo                        |
| Valores derivados/computados | ✅ `computed()` | `combineLatest` funciona         |
| Efeitos colaterais         | ✅ `effect()`   | operador `tap`                   |
| Requisições HTTP           | ❌              | ✅ HttpClient retorna Observable |
| Fluxos de eventos          | ❌              | ✅ `fromEvent`, operadores       |
| Fluxos assíncronos complexos | ❌              | ✅ `switchMap`, `mergeMap`       |

---

## 2. Componentes Standalone

Componentes standalone são auto-contidos e não exigem declarações NgModule.

### Criar Componentes Standalone

```typescript
import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import { RouterLink } from "@angular/router";

@Component({
  selector: "app-header",
  standalone: true,
  imports: [CommonModule, RouterLink], // Imports diretos
  template: `
    <header>
      <a routerLink="/">Início</a>
      <a routerLink="/about">Sobre</a>
    </header>
  `,
})
export class HeaderComponent {}
```

### Bootstrap Sem NgModule

```typescript
// main.ts
import { bootstrapApplication } from "@angular/platform-browser";
import { provideRouter } from "@angular/router";
import { provideHttpClient } from "@angular/common/http";
import { AppComponent } from "./app/app.component";
import { routes } from "./app/app.routes";

bootstrapApplication(AppComponent, {
  providers: [provideRouter(routes), provideHttpClient()],
});
```

### Lazy Loading de Componentes Standalone

```typescript
// app.routes.ts
import { Routes } from "@angular/router";

export const routes: Routes = [
  {
    path: "dashboard",
    loadComponent: () =>
      import("./dashboard/dashboard.component").then(
        (m) => m.DashboardComponent,
      ),
  },
  {
    path: "admin",
    loadChildren: () =>
      import("./admin/admin.routes").then((m) => m.ADMIN_ROUTES),
  },
];
```

---

## 3. Angular Zoneless

Aplicações zoneless não usam zone.js, melhorando performance e debugging.

### Habilitando Modo Zoneless

```typescript
// main.ts
import { bootstrapApplication } from "@angular/platform-browser";
import { provideZonelessChangeDetection } from "@angular/core";
import { AppComponent } from "./app/app.component";

bootstrapApplication(AppComponent, {
  providers: [provideZonelessChangeDetection()],
});
```

### Padrões de Componente Zoneless

```typescript
import { Component, signal, ChangeDetectionStrategy } from "@angular/core";

@Component({
  selector: "app-counter",
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div>Count: {{ count() }}</div>
    <button (click)="increment()">+</button>
  `,
})
export class CounterComponent {
  count = signal(0);

  increment() {
    this.count.update((v) => v + 1);
    // Sem zone.js necessário - Signal dispara detecção de mudanças
  }
}
```

### Principais Benefícios do Zoneless

- **Performance**: Sem patches zone.js em APIs assíncronas
- **Debugging**: Stack traces limpos sem wrappers de zone
- **Tamanho do bundle**: Menor sem zone.js (~15KB de economia)
- **Interoperabilidade**: Melhor com Web Components e micro-frontends

---

## 4. Server-Side Rendering & Hidratação

### Configuração de SSR com Angular CLI

```bash
ng add @angular/ssr
```

### Configuração de Hidratação

```typescript
// app.config.ts
import { ApplicationConfig } from "@angular/core";
import {
  provideClientHydration,
  withEventReplay,
} from "@angular/platform-browser";

export const appConfig: ApplicationConfig = {
  providers: [provideClientHydration(withEventReplay())],
};
```

### Hidratação Incremental (v20+)

```typescript
import { Component } from "@angular/core";

@Component({
  selector: "app-page",
  standalone: true,
  template: `
    <app-hero />

    @defer (hydrate on viewport) {
      <app-comments />
    }

    @defer (hydrate on interaction) {
      <app-chat-widget />
    }
  `,
})
export class PageComponent {}
```

### Triggers de Hidratação

| Trigger            | Quando Usar                                   |
| ------------------ | --------------------------------------------- |
| `on idle`          | Baixa prioridade, hidratar quando navegador inativo |
| `on viewport`      | Hidratar quando elemento entra na viewport    |
| `on interaction`   | Hidratar na primeira interação do usuário     |
| `on hover`         | Hidratar quando usuário passa o mouse         |
| `on timer(ms)`     | Hidratar após atraso especificado             |

---

## 5. Padrões Modernos de Roteamento

### Guards de Rota Funcionais

```typescript
// auth.guard.ts
import { inject } from "@angular/core";
import { Router, CanActivateFn } from "@angular/router";
import { AuthService } from "./auth.service";

export const authGuard: CanActivateFn = (route, state) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (auth.isAuthenticated()) {
    return true;
  }

  return router.createUrlTree(["/login"], {
    queryParams: { returnUrl: state.url },
  });
};

// Uso em rotas
export const routes: Routes = [
  {
    path: "dashboard",
    loadComponent: () => import("./dashboard.component"),
    canActivate: [authGuard],
  },
];
```

### Resolvedores de Dados em Nível de Rota

```typescript
import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { UserService } from './user.service';
import { User } from './user.model';

export const userResolver: ResolveFn<User> = (route) => {
  const userService = inject(UserService);
  return userService.getUser(route.paramMap.get('id')!);
};

// Em rotas
{
  path: 'user/:id',
  loadComponent: () => import('./user.component'),
  resolve: { user: userResolver }
}

// No componente
export class UserComponent {
  private route = inject(ActivatedRoute);
  user = toSignal(this.route.data.pipe(map(d => d['user'])));
}
```

---

## 6. Padrões de Injeção de Dependência

### Função inject() Moderna

```typescript
import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UserService } from './user.service';

@Component({...})
export class UserComponent {
  // inject() moderno - sem construtor necessário
  private http = inject(HttpClient);
  private userService = inject(UserService);

  // Funciona em qualquer contexto de injeção
  users = toSignal(this.userService.getUsers());
}
```

### Tokens de Injeção para Configuração

```typescript
import { InjectionToken, inject } from "@angular/core";

// Definir token
export const API_BASE_URL = new InjectionToken<string>("API_BASE_URL");

// Fornecer na config
bootstrapApplication(AppComponent, {
  providers: [{ provide: API_BASE_URL, useValue: "https://api.example.com" }],
});

// Injetar no serviço
@Injectable({ providedIn: "root" })
export class ApiService {
  private baseUrl = inject(API_BASE_URL);

  get(endpoint: string) {
    return this.http.get(`${this.baseUrl}/${endpoint}`);
  }
}
```

---

## 7. Composição de Componentes & Reusabilidade

### Projeção de Conteúdo (Slots)

```typescript
@Component({
  selector: 'app-card',
  template: `
    <div class="card">
      <div class="header">
        <!-- Selecionar por atributo -->
        <ng-content select="[card-header]"></ng-content>
      </div>
      <div class="body">
        <!-- Slot padrão -->
        <ng-content></ng-content>
      </div>
    </div>
  `
})
export class CardComponent {}

// Uso
<app-card>
  <h3 card-header>Título</h3>
  <p>Conteúdo do corpo</p>
</app-card>
```

### Host Directives (Composição)

```typescript
// Comportamentos reutilizáveis sem herança
@Directive({
  standalone: true,
  selector: '[appTooltip]',
  inputs: ['tooltip'] // Alias de input Signal
})
export class TooltipDirective { ... }

@Component({
  selector: 'app-button',
  standalone: true,
  hostDirectives: [
    {
      directive: TooltipDirective,
      inputs: ['tooltip: title'] // Mapear input
    }
  ],
  template: `<ng-content />`
})
export class ButtonComponent {}
```

---

## 8. Padrões de Gerenciamento de Estado

### Serviço de Estado Baseado em Signal

```typescript
import { Injectable, signal, computed } from "@angular/core";

interface AppState {
  user: User | null;
  theme: "light" | "dark";
  notifications: Notification[];
}

@Injectable({ providedIn: "root" })
export class StateService {
  // Sinais graváveis privados
  private _user = signal<User | null>(null);
  private _theme = signal<"light" | "dark">("light");
  private _notifications = signal<Notification[]>([]);

  // Computados públicos somente leitura
  readonly user = computed(() => this._user());
  readonly theme = computed(() => this._theme());
  readonly notifications = computed(() => this._notifications());
  readonly unreadCount = computed(
    () => this._notifications().filter((n) => !n.read).length,
  );

  // Ações
  setUser(user: User | null) {
    this._user.set(user);
  }

  toggleTheme() {
    this._theme.update((t) => (t === "light" ? "dark" : "light"));
  }

  addNotification(notification: Notification) {
    this._notifications.update((n) => [...n, notification]);
  }
}
```

### Padrão Component Store com Signals

```typescript
import { Injectable, signal, computed, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { toSignal } from "@angular/core/rxjs-interop";

@Injectable()
export class ProductStore {
  private http = inject(HttpClient);

  // Estado
  private _products = signal<Product[]>([]);
  private _loading = signal(false);
  private _filter = signal("");

  // Seletores
  readonly products = computed(() => this._products());
  readonly loading = computed(() => this._loading());
  readonly filteredProducts = computed(() => {
    const filter = this._filter().toLowerCase();
    return this._products().filter((p) =>
      p.name.toLowerCase().includes(filter),
    );
  });

  // Ações
  loadProducts() {
    this._loading.set(true);
    this.http.get<Product[]>("/api/products").subscribe({
      next: (products) => {
        this._products.set(products);
        this._loading.set(false);
      },
      error: () => this._loading.set(false),
    });
  }

  setFilter(filter: string) {
    this._filter.set(filter);
  }
}
```

---

## 9. Formulários com Signals (Chegando em v22+)

### Formulários Reativos Atuais

```typescript
import { Component, inject } from "@angular/core";
import { FormBuilder, Validators, ReactiveFormsModule } from "@angular/forms";

@Component({
  selector: "app-user-form",
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="name" placeholder="Nome" />
      <input formControlName="email" type="email" placeholder="Email" />
      <button [disabled]="form.invalid">Enviar</button>
    </form>
  `,
})
export class UserFormComponent {
  private fb = inject(FormBuilder);

  form = this.fb.group({
    name: ["", Validators.required],
    email: ["", [Validators.required, Validators.email]],
  });

  onSubmit() {
    if (this.form.valid) {
      console.log(this.form.value);
    }
  }
}
```

### Padrões de Formulário Conscientes de Signal (Preview)

```typescript
// API futura de Signal Forms (experimental)
import { Component, signal } from '@angular/core';

@Component({...})
export class SignalFormComponent {
  name = signal('');
  email = signal('');

  // Validação computada
  isValid = computed(() =>
    this.name().length > 0 &&
    this.email().includes('@')
  );

  submit() {
    if (this.isValid()) {
      console.log({ name: this.name(), email: this.email() });
    }
  }
}
```

---

## 10. Otimização de Performance

### Estratégias de Detecção de Mudanças

```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  // Verifica apenas quando:
  // 1. Input signal/referência muda
  // 2. Handler de evento é executado
  // 3. Async pipe emite
  // 4. Valor de Signal muda
})
```

### Blocos Defer para Carregamento Preguiçoso

```typescript
@Component({
  template: `
    <!-- Carregamento imediato -->
    <app-header />

    <!-- Lazy load quando visível -->
    @defer (on viewport) {
      <app-heavy-chart />
    } @placeholder {
      <div class="skeleton" />
    } @loading (minimum 200ms) {
      <app-spinner />
    } @error {
      <p>Falha ao carregar gráfico</p>
    }
  `
})
```

### NgOptimizedImage

```typescript
import { NgOptimizedImage } from '@angular/common';

@Component({
  imports: [NgOptimizedImage],
  template: `
    <img
      ngSrc="hero.jpg"
      width="800"
      height="600"
      priority
    />

    <img
      ngSrc="thumbnail.jpg"
      width="200"
      height="150"
      loading="lazy"
      placeholder="blur"
    />
  `
})
```

---

## 11. Testando Angular Moderno

### Testando Componentes com Signal

```typescript
import { ComponentFixture, TestBed } from "@angular/core/testing";
import { CounterComponent } from "./counter.component";

describe("CounterComponent", () => {
  let component: CounterComponent;
  let fixture: ComponentFixture<CounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CounterComponent], // Import standalone
    }).compileComponents();

    fixture = TestBed.createComponent(CounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("deve incrementar count", () => {
    expect(component.count()).toBe(0);

    component.increment();

    expect(component.count()).toBe(1);
  });

  it("deve atualizar DOM ao mudar signal", () => {
    component.count.set(5);
    fixture.detectChanges();

    const el = fixture.nativeElement.querySelector(".count");
    expect(el.textContent).toContain("5");
  });
});
```

### Testando com Signal Inputs

```typescript
import { ComponentFixture, TestBed } from "@angular/core/testing";
import { ComponentRef } from "@angular/core";
import { UserCardComponent } from "./user-card.component";

describe("UserCardComponent", () => {
  let fixture: ComponentFixture<UserCardComponent>;
  let componentRef: ComponentRef<UserCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserCardComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(UserCardComponent);
    componentRef = fixture.componentRef;

    // Definir signal inputs via setInput
    componentRef.setInput("id", "123");
    componentRef.setInput("name", "John Doe");

    fixture.detectChanges();
  });

  it("deve exibir nome do usuário", () => {
    const el = fixture.nativeElement.querySelector("h3");
    expect(el.textContent).toContain("John Doe");
  });
});
```

---

## Resumo de Melhores Práticas

| Padrão               | ✅ Faça                        | ❌ Não Faça                     |
| -------------------- | ------------------------------ | ------------------------------- |
| **Estado**           | Use Signals para estado local  | Abuse de RxJS para estado simples |
| **Componentes**      | Standalone com imports diretos | SharedModules inchados          |
| **Detecção de Mudanças** | OnPush + Signals               | CD padrão em tudo               |
| **Lazy Loading**     | `@defer` e `loadComponent`     | Carregar tudo com urgência      |
| **DI**               | Função `inject()`              | Injeção em construtor (verbosa) |
| **Inputs**           | Função signal `input()`        | Decorador `@Input()` (legado)   |
| **Zoneless**         | Habilitar em novos projetos    | Forçar em apps legados sem testes |

---

## Recursos

- [Documentação Angular.dev](https://angular.dev)
- [Guia de Angular Signals](https://angular.dev/guide/signals)
- [Guia de Angular SSR](https://angular.dev/guide/ssr)
- [Guia de Atualização do Angular](https://angular.dev/update-guide)
- [Blog do Angular](https://blog.angular.dev)

---

## Troubleshooting Comum

| Problema                    | Solução                                             |
| --------------------------- | --------------------------------------------------- |
| Signal não atualiza UI      | Garanta `OnPush` + chame signal como função `count()` |
| Incompatibilidade de hidratação | Verifique consistência entre conteúdo servidor/cliente |
| Dependência circular        | Use `inject()` com `forwardRef`                     |
| Zoneless não detecta mudanças | Dispare via atualizações de signal, não mutações   |
| Falha de fetch do SSR       | Use `TransferState` ou `withFetch()`                |