---
name: convex
description: "Especialista em backend reativo Convex: design de schema, funções TypeScript, assinaturas em tempo real, autenticação, armazenamento de arquivos, agendamento e deploy."
risk: safe
source: "https://docs.convex.dev"
date_added: "2026-02-27"
---

# Convex

Você é um especialista em Convex — a plataforma backend reativa e open-source onde queries são código TypeScript. Possui conhecimento profundo de design de schema, autoria de funções (queries, mutations, actions), assinaturas de dados em tempo real, autenticação, armazenamento de arquivos, agendamento e fluxos de deploy em React, Next.js, Angular, Vue, Svelte, React Native e ambientes server-side.

## Quando Usar
- Use ao construir um novo projeto com Convex como backend
- Use ao adicionar Convex a uma aplicação React, Next.js, Angular, Vue, Svelte ou React Native existente
- Use ao projetar schemas para um banco de dados relacional de documentos Convex
- Use ao escrever ou debugar funções Convex (queries, mutations, actions)
- Use ao implementar padrões de dados em tempo real/reativos
- Use ao configurar autenticação com Convex Auth ou provedores terceiros (Clerk, Auth0, etc.)
- Use ao trabalhar com armazenamento de arquivos, funções agendadas ou cron jobs no Convex
- Use ao fazer deploy ou gerenciar projetos Convex

## Conceitos Principais

Convex é um **banco de dados relacional de documentos** com um backend totalmente gerenciado. Diferenciais principais:

- **Reativo por padrão**: Queries re-executam automaticamente e enviam atualizações a todos os clientes conectados quando dados subjacentes mudam
- **Primeiro TypeScript**: Toda a lógica backend — queries, mutations, actions, schemas — é escrita em TypeScript
- **Transações ACID**: Isolamento serializável com controle de concorrência otimista
- **Sem infraestrutura para gerenciar**: Serverless, escala automaticamente, zero config
- **Segurança de tipo ponta a ponta**: Tipos fluem de schema → funções backend → hooks do cliente

### Tipos de Função

| Tipo            | Propósito                  | Pode Ler BD   | Pode Escrever BD  | Pode Chamar APIs Externas | Cache/Reativo |
| :-------------- | :------------------------- | :------------ | :---------------- | :------------------------ | :------------ |
| **Query**       | Ler dados                  | ✅            | ❌                | ❌                       | ✅            |
| **Mutation**    | Escrever dados             | ✅            | ✅                | ❌                       | ❌            |
| **Action**      | Efeitos colaterais         | via `runQuery` | via `runMutation` | ✅                       | ❌            |
| **HTTP Action** | Webhooks/endpoints custom  | via `runQuery` | via `runMutation` | ✅                       | ❌            |

## Configuração do Projeto

### Novo Projeto (Next.js)

```bash
npx create-next-app@latest my-app
cd my-app && npm install convex
npx convex dev
```

### Adicionar a Projeto Existente

```bash
npm install convex
npx convex dev
```

O comando `npx convex dev`:

1. Solicita login (GitHub)
2. Cria um projeto e deployment
3. Gera a pasta `convex/` para funções backend
4. Sincroniza funções com seu deployment de dev em tempo real
5. Cria `.env.local` com `CONVEX_DEPLOYMENT` e `NEXT_PUBLIC_CONVEX_URL`

### Estrutura de Pastas

```
my-app/
├── convex/
│   ├── _generated/        ← Auto-gerado (NÃO EDITE)
│   │   ├── api.d.ts
│   │   ├── dataModel.d.ts
│   │   └── server.d.ts
│   ├── schema.ts          ← Definição de schema do banco
│   ├── tasks.ts           ← Funções query/mutation
│   └── http.ts            ← HTTP actions (opcional)
├── .env.local             ← CONVEX_DEPLOYMENT, NEXT_PUBLIC_CONVEX_URL
└── convex.json            ← Config do projeto (opcional)
```

## Design de Schema

Defina seu schema em `convex/schema.ts` usando a biblioteca validator:

```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    avatarUrl: v.optional(v.string()),
    tokenIdentifier: v.string(),
  })
    .index("by_token", ["tokenIdentifier"])
    .index("by_email", ["email"]),

  messages: defineTable({
    authorId: v.id("users"),
    channelId: v.id("channels"),
    body: v.string(),
    attachmentId: v.optional(v.id("_storage")),
  })
    .index("by_channel", ["channelId"])
    .searchIndex("search_body", { searchField: "body" }),

  channels: defineTable({
    name: v.string(),
    description: v.optional(v.string()),
    isPrivate: v.boolean(),
  }),
});
```

### Tipos de Validator

| Validator                         | Tipo TypeScript       | Notas                                          |
| :-------------------------------- | :-------------------- | :--------------------------------------------- |
| `v.string()`                      | `string`              |                                                |
| `v.number()`                      | `number`              | IEEE 754 float                                 |
| `v.bigint()`                      | `bigint`              |                                                |
| `v.boolean()`                     | `boolean`             |                                                |
| `v.null()`                        | `null`                |                                                |
| `v.id("tableName")`               | `Id<"tableName">`     | Referência de documento                        |
| `v.array(v.string())`             | `string[]`            |                                                |
| `v.object({...})`                 | `{...}`               | Objetos aninhados                              |
| `v.optional(v.string())`          | `string \| undefined` |                                                |
| `v.union(v.string(), v.number())` | `string \| number`    |                                                |
| `v.literal("active")`             | `"active"`            | Tipos literais                                 |
| `v.bytes()`                       | `ArrayBuffer`         | Dados binários                                 |
| `v.float64()`                     | `number`              | Float 64-bit explícito (usado em índices de vetor) |
| `v.any()`                         | `any`                 | Escape hatch                                   |

### Indexes

```typescript
// Index de campo único
defineTable({ email: v.string() }).index("by_email", ["email"]);

// Index composto (ordem importa para range queries)
defineTable({
  orgId: v.string(),
  createdAt: v.number(),
}).index("by_org_and_date", ["orgId", "createdAt"]);

// Index full-text search
defineTable({ body: v.string(), channelId: v.id("channels") }).searchIndex(
  "search_body",
  {
    searchField: "body",
    filterFields: ["channelId"],
  },
);

// Index vector search (para IA/embeddings)
defineTable({ embedding: v.array(v.float64()), text: v.string() }).vectorIndex(
  "by_embedding",
  {
    vectorField: "embedding",
    dimensions: 1536,
  },
);
```

## Escrevendo Funções

### Queries (Ler Dados)

Queries são reativas — clientes recebem automaticamente atualizações quando dados mudam.

```typescript
import { query } from "./_generated/server";
import { v } from "convex/values";

// Query simples — listar todas as tarefas
export const list = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("tasks").collect();
  },
});

// Query com argumentos e filtragem
export const getByChannel = query({
  args: { channelId: v.id("channels") },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .order("desc")
      .take(50);
  },
});

// Query com verificação de auth
export const getMyProfile = query({
  args: {},
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) return null;

    return await ctx.db
      .query("users")
      .withIndex("by_token", (q) =>
        q.eq("tokenIdentifier", identity.tokenIdentifier),
      )
      .unique();
  },
});
```

### Queries com Paginação

Use paginação baseada em cursor para listas ou infinite scroll.

```typescript
import { query } from "./_generated/server";
import { paginationOptsValidator } from "convex/server";

export const listPaginated = query({
  args: {
    paginationOpts: paginationOptsValidator
  },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .order("desc")
      .paginate(args.paginationOpts);
  },
});
```

### Mutations (Escrever Dados)

Mutations executam como transações ACID com isolamento serializável.

```typescript
import { mutation } from "./_generated/server";
import { v } from "convex/values";

// Inserir um documento
export const create = mutation({
  args: { text: v.string(), isCompleted: v.boolean() },
  handler: async (ctx, args) => {
    const taskId = await ctx.db.insert("tasks", {
      text: args.text,
      isCompleted: args.isCompleted,
    });
    return taskId;
  },
});

// Atualizar um documento
export const update = mutation({
  args: { id: v.id("tasks"), isCompleted: v.boolean() },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.id, { isCompleted: args.isCompleted });
  },
});

// Deletar um documento
export const remove = mutation({
  args: { id: v.id("tasks") },
  handler: async (ctx, args) => {
    await ctx.db.delete(args.id);
  },
});

// Transação multi-documento (automaticamente atômica)
export const transferCredits = mutation({
  args: {
    fromUserId: v.id("users"),
    toUserId: v.id("users"),
    amount: v.number(),
  },
  handler: async (ctx, args) => {
    const fromUser = await ctx.db.get(args.fromUserId);
    const toUser = await ctx.db.get(args.toUserId);
    if (!fromUser || !toUser) throw new Error("Usuário não encontrado");
    if (fromUser.credits < args.amount) throw new Error("Créditos insuficientes");

    await ctx.db.patch(args.fromUserId, {
      credits: fromUser.credits - args.amount,
    });
    await ctx.db.patch(args.toUserId, {
      credits: toUser.credits + args.amount,
    });
  },
});
```

### Actions (APIs Externas e Efeitos Colaterais)

Actions podem chamar serviços terceiros, mas não conseguem acessar diretamente o banco — devem usar `ctx.runQuery` e `ctx.runMutation`.

```typescript
import { action } from "./_generated/server";
import { v } from "convex/values";
import { api } from "./_generated/api";

export const sendEmail = action({
  args: { to: v.string(), subject: v.string(), body: v.string() },
  handler: async (ctx, args) => {
    // Chamar API externa
    const response = await fetch("https://api.sendgrid.com/v3/mail/send", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.SENDGRID_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        personalizations: [{ to: [{ email: args.to }] }],
        from: { email: "noreply@example.com" },
        subject: args.subject,
        content: [{ type: "text/plain", value: args.body }],
      }),
    });

    if (!response.ok) throw new Error("Falha ao enviar email");

    // Escrever resultado de volta ao BD via mutation
    await ctx.runMutation(api.emails.recordSent, {
      to: args.to,
      subject: args.subject,
      sentAt: Date.now(),
    });
  },
});

// Gerar embeddings de IA
export const generateEmbedding = action({
  args: { text: v.string(), documentId: v.id("documents") },
  handler: async (ctx, args) => {
    const response = await fetch("https://api.openai.com/v1/embeddings", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "text-embedding-3-small",
        input: args.text,
      }),
    });

    const { data } = await response.json();
    await ctx.runMutation(api.documents.saveEmbedding, {
      documentId: args.documentId,
      embedding: data[0].embedding,
    });
  },
});
```

### HTTP Actions (Webhooks)

```typescript
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { api } from "./_generated/api";

const http = httpRouter();

http.route({
  path: "/webhooks/stripe",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const body = await request.text();
    const signature = request.headers.get("stripe-signature");

    // Verificar assinatura do webhook aqui...

    const event = JSON.parse(body);
    await ctx.runMutation(api.payments.handleWebhook, { event });

    return new Response("OK", { status: 200 });
  }),
});

export default http;
```

## Integração no Cliente

### React / Next.js

```typescript
// app/ConvexClientProvider.tsx
"use client";
import { ConvexProvider, ConvexReactClient } from "convex/react";
import { ReactNode } from "react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({ children }: { children: ReactNode }) {
  return <ConvexProvider client={convex}>{children}</ConvexProvider>;
}
```

```typescript
// app/layout.tsx — envolver children
import { ConvexClientProvider } from "./ConvexClientProvider";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>
        <ConvexClientProvider>{children}</ConvexClientProvider>
      </body>
    </html>
  );
}
```

```typescript
// Componente usando hooks Convex
"use client";
import { useQuery, useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";

export function TaskList() {
  // Query reativa — auto-atualiza quando dados mudam
  const tasks = useQuery(api.tasks.list);
  const addTask = useMutation(api.tasks.create);
  const toggleTask = useMutation(api.tasks.update);

  if (tasks === undefined) return <p>Carregando...</p>;

  return (
    <div>
      {tasks.map((task) => (
        <div key={task._id}>
          <input
            type="checkbox"
            checked={task.isCompleted}
            onChange={() =>
              toggleTask({ id: task._id, isCompleted: !task.isCompleted })
            }
          />
          {task.text}
        </div>
      ))}
      <button onClick={() => addTask({ text: "Nova tarefa", isCompleted: false })}>
        Adicionar Tarefa
      </button>
    </div>
  );
}
```

```typescript
// Componente usando Queries com Paginação
"use client";
import { usePaginatedQuery } from "convex/react";
import { api } from "@/convex/_generated/api";

export function MessageLog() {
  const { results, status, loadMore } = usePaginatedQuery(
    api.messages.listPaginated,
    {}, // args
    { initialNumItems: 20 }
  );

  return (
    <div>
      {results.map((msg) => (
        <div key={msg._id}>{msg.body}</div>
      ))}

      {status === "LoadingFirstPage" && <p>Carregando...</p>}

      {status === "CanLoadMore" && (
        <button onClick={() => loadMore(20)}>Carregar Mais</button>
      )}
    </div>
  );
}
```

### Com Auth (Convex Auth First-Party)

Convex fornece uma biblioteca de autenticação robusta e nativa (`@convex-dev/auth`) com Magic Links, Senhas e 80+ provedores OAuth sem precisar de um serviço terceiro.

```typescript
// app/ConvexClientProvider.tsx
"use client";
import { ConvexAuthProvider } from "@convex-dev/auth/react";
import { ConvexReactClient } from "convex/react";
import { ReactNode } from "react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({ children }: { children: ReactNode }) {
  return (
    <ConvexAuthProvider client={convex}>
      {children}
    </ConvexAuthProvider>
  );
}
```

```typescript
// Sign in no lado do cliente
import { useAuthActions } from "@convex-dev/auth/react";

export function Login() {
  const { signIn } = useAuthActions();
  return <button onClick={() => signIn("github")}>Entrar com GitHub</button>;
}
```

### Com Auth (Exemplo Clerk Terceiro)

Se preferir uma solução hosted terceira como Clerk:

```typescript
// app/ConvexClientProvider.tsx
"use client";
import { ConvexProviderWithClerk } from "convex/react-clerk";
import { ClerkProvider, useAuth } from "@clerk/nextjs";
import { ConvexReactClient } from "convex/react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({ children }: { children: ReactNode }) {
  return (
    <ClerkProvider publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY!}>
      <ConvexProviderWithClerk client={convex} useAuth={useAuth}>
        {children}
      </ConvexProviderWithClerk>
    </ClerkProvider>
  );
}
```

### Com Auth (Componente Better Auth)

Convex também tem um componente community (`@convex-dev/better-auth`) que integra a biblioteca Better Auth direto no backend Convex. Atualmente em **early alpha**.

```bash
npm install better-auth @convex-dev/better-auth
npx convex env set BETTER_AUTH_SECRET your-secret-here
npx convex env set SITE_URL http://localhost:3000
```

Better Auth fornece email/senha, logins sociais, autenticação de dois fatores e gerenciamento de sessões — tudo rodando dentro de funções Convex em vez de um servidor auth externo.

### Integração Angular

Convex não tem uma biblioteca client oficial para Angular, mas apps Angular podem usar o pacote core `convex` diretamente com Angular's Dependency Injection e Signals.

```typescript
// services/convex.service.ts
import { Injectable, signal, effect, OnDestroy } from "@angular/core";
import { ConvexClient } from "convex/browser";
import { api } from "../../convex/_generated/api";
import { FunctionReturnType } from "convex/server";

@Injectable({ providedIn: "root" })
export class ConvexService implements OnDestroy {
  private client = new ConvexClient(environment.convexUrl);

  // Signal reativo — atualiza automaticamente quando dados mudam
  tasks = signal<FunctionReturnType<typeof api.tasks.list> | undefined>(
    undefined,
  );

  constructor() {
    // Inscrever em uma query reativa
    this.client.onUpdate(api.tasks.list, {}, (result) => {
      this.tasks.set(result);
    });
  }

  async addTask(text: string) {
    await this.client.mutation(api.tasks.create, {
      text,
      isCompleted: false,
    });
  }

  ngOnDestroy() {
    this.client.close();
  }
}
```

```typescript
// Uso do componente
import { Component, inject } from "@angular/core";
import { ConvexService } from "./services/convex.service";

@Component({
  selector: "app-task-list",
  template: `
    @if (convex.tasks(); as tasks) {
      @for (task of tasks; track task._id) {
        <div>{{ task.text }}</div>
      }
    } @else {
      <p>Carregando...</p>
    }
    <button (click)="convex.addTask('Nova tarefa')">Adicionar Tarefa</button>
  `,
})
export class TaskListComponent {
  convex = inject(ConvexService);
}
```

> **Nota:** A biblioteca community `@robmanganelly/ngx-convex` fornece uma experiência mais Angular-nativa com hooks tipo-React adaptados para Angular DI e Signals.

## Agendamento e Cron Jobs

### Funções Agendadas Únicas

```typescript
import { mutation } from "./_generated/server";
import { api } from "./_generated/api";

export const sendReminder = mutation({
  args: { userId: v.id("users"), message: v.string(), delayMs: v.number() },
  handler: async (ctx, args) => {
    await ctx.scheduler.runAfter(args.delayMs, api.notifications.send, {
      userId: args.userId,
      message: args.message,
    });
  },
});
```

### Cron Jobs

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { api } from "./_generated/api";

const crons = cronJobs();

crons.interval("limpar logs antigos", { hours: 24 }, api.logs.clearOld);

crons.cron(
  "digestão semanal",
  "0 9 * * 1", // Toda segunda às 9 AM
  api.emails.sendWeeklyDigest,
);

export default crons;
```

## Armazenamento de Arquivos

```typescript
// Gerar URL de upload (mutation)
export const generateUploadUrl = mutation({
  args: {},
  handler: async (ctx) => {
    return await ctx.storage.generateUploadUrl();
  },
});

// Salvar referência de arquivo após upload (mutation)
export const saveFile = mutation({
  args: { storageId: v.id("_storage"), name: v.string() },
  handler: async (ctx, args) => {
    await ctx.db.insert("files", {
      storageId: args.storageId,
      name: args.name,
    });
  },
});

// Obter URL para servir um arquivo (query)
export const getFileUrl = query({
  args: { storageId: v.id("_storage") },
  handler: async (ctx, args) => {
    return await ctx.storage.getUrl(args.storageId);
  },
});
```

## Variáveis de Ambiente

```bash
# Definir variáveis de ambiente para seu deployment
npx convex env set OPENAI_API_KEY sk-...
npx convex env set SENDGRID_API_KEY SG...

# Listar variáveis de env atuais
npx convex env list

# Remover uma variável de env
npx convex env unset OPENAI_API_KEY
```

Acessar em actions (NÃO em queries ou mutations):

```typescript
// Apenas disponível em actions
const apiKey = process.env.OPENAI_API_KEY;
```

## Deploy e CLI

```bash
# Desenvolvimento (observa mudanças, sincroniza com deployment de dev)
npx convex dev

# Deploy para produção
npx convex deploy

# Importar dados
npx convex import --table tasks data.jsonl

# Exportar dados
npx convex export --path ./backup

# Abrir dashboard Convex
npx convex dashboard

# Executar uma função via CLI
npx convex run tasks:list

# Ver logs
npx convex logs
```

## Melhores Práticas

- ✅ Defina schemas — adiciona segurança de tipo em toda a sua pilha
- ✅ Use indexes para queries — evita full table scans
- ✅ Use indexes compostos com filtros de igualdade primeiro, filter de range por último
- ✅ Confie no determinismo nativo — `Date.now()` e `Math.random()` são 100% seguros em queries e mutations porque Convex congela o tempo no início de toda execução de função!
- ✅ Use `v.id("tableName")` para referências de documentos em vez de strings simples
- ✅ Use actions para chamadas de API externa (nunca chame APIs externas de queries ou mutations)
- ✅ Use `ctx.runQuery` / `ctx.runMutation` de actions — nunca acesse `ctx.db` diretamente em actions
- ✅ Adicione validadores de argumentos a todas as funções — eles aplicam segurança de tipo em runtime
- ✅ Retorne `null` quando um documento não for encontrado em vez de lançar erro, a menos que ausência seja excepcional
- ✅ Prefira `withIndex` ao `.filter()` para performance de query

## Anti-Patterns para Evitar

1. **❌ Chamadas de API externa em queries/mutations**: Apenas actions podem chamar serviços externos. Queries e mutations rodam no motor de transação Convex.
2. **❌ Fazer trabalho CPU-bound pesado em mutations**: Mutations bloqueiam commits do banco; transfira processamento pesado para actions.
3. **❌ Usar `.collect()` em tabelas grandes sem limites**: Carrega todos os documentos na memória. Use `.take(N)` ou `.paginate()`.
4. **❌ Pular definição de schema**: Sem schema você perde segurança de tipo ponta a ponta, a principal vantagem Convex.
5. **❌ Usar `.filter()` em vez de indexes**: `.filter()` faz full table scan. Defina um index e use `.withIndex()`.
6. **❌ Armazenar blobs grandes em documentos**: Use armazenamento de arquivos Convex (`_storage`) para arquivos; mantenha documentos enxutos.
7. **❌ Cadeias circulares `runQuery`/`runMutation`**: Actions chamando mutations que agendando actions podem criar loops infinitos.

## Armadilhas Comuns

- **Problema:** "Query retorna `undefined` na primeira renderização"
  **Solução:** Isso é esperado — queries Convex são async. Verifique `undefined` antes de renderizar (significa carregando, não vazio).

- **Problema:** "Mutation lança `Document not found`"
  **Solução:** Documentos podem ter sido deletados entre sua leitura e escrita devido a controle de concorrência otimista. Releia dentro da mutation.

- **Problema:** "`process.env` é undefined em query/mutation"
  **Solução:** Variáveis de ambiente estão acessíveis apenas em **actions** (não queries ou mutations) porque queries/mutations rodam no motor de transação determinístico.

- **Problema:** "Handler de função é muito lento"
  **Solução:** Adicione indexes para seus padrões de query. Use `withIndex()` em vez de `.filter()`. Para operações complexas, quebre em mutations menores.

- **Problema:** "Schema push falha com dados existentes"
  **Solução:** Convex valida dados existentes contra novos schemas. Ou migre documentos existentes primeiro, ou use `v.optional()` para novos campos.

## Limitações

- Queries e mutations não conseguem chamar APIs HTTP externas (use actions em vez disso)
- Sem SQL bruto — você trabalha com a API do query builder Convex
- Variáveis de ambiente disponíveis apenas em actions, não em queries ou mutations
- Limite de tamanho de documento de 1MB
- Limites de tempo de execução de função se aplicam
- Sem server-side rendering de dados Convex sem padrões SSR específicos (use preloading)
- Schemas são aplicados em write-time; mudar schemas requer migração de dados para documentos existentes

## Skills Relacionadas

- `@firebase` — BaaS alternativo com Firestore (comparar: Convex é TypeScript-first com transações ACID)
- `@supabase-automation` — Alternativa com backend PostgreSQL (comparar: Convex é relacional de documentos com reatividade nativa)
- `@prisma-expert` — ORM para bancos tradicionais (Convex substitui ORM e banco)
- `@react-patterns` — Padrões frontend que funcionam bem com hooks Convex React
- `@nextjs-app-router` — Padrões de integração Next.js App Router
- `@authentication-oauth` — Padrões de auth (Convex suporta Clerk, Auth0, Convex Auth)
- `@stripe` — Integração de pagamento via actions Convex e webhooks HTTP

## Recursos

- [Documentação Oficial](https://docs.convex.dev)
- [Convex Stack (Blog)](https://