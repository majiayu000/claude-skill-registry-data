---
name: web-componentes
description: Como escrever componentes de feature e formulários no web do Smaug — props XProps, apresentacional vs container de feature (Screen/Wizard/Ficha), formulários com React Hook Form + zod (no componente, nos formulários de autenticação ou dentro do hook do assistente), tokens Tailwind, cn() e acessibilidade em pt-BR.
---

# Componente de feature e formulário

## Quando usar esta skill

Ao criar/alterar `web/features/<f>/components/*.tsx`. Para primitivos de `shared/components`, veja
`web-shared-ui`.

## Regras gerais

1. **`interface <Componente>Props` declarada logo acima do componente**, e **não exportada** em
   componente de feature (primitivos de `shared/` exportam).
2. **`"use client"` só quando o componente tem estado/efeito/hook.** `ExpenseWizard`,
   `DespesasScreen` e as Fichas têm; `KpiCard`, `EntryRow`, `MonthStrip` **não têm** — herdam a
   fronteira de quem os usa.
3. **Dois papéis, sem meio-termo:**
   - **Apresentacional** — só props, sem hook de dados, sem `apiClient`, sem query client. É o caso
     de tudo em `shared/components/lancamentos/` e dos cards/formulários de Categorias.
   - **Container de feature** — `<Feature>Screen`, `<X>Wizard` e `<X>Ficha` de Receitas/Despesas.
     Chamam **hooks da própria feature** (`useExpenseMonth`, `useExpenseWizard`,
     `useInstallmentExpense`, `useExpenseMutations`) e compõem os blocos apresentacionais. Nunca
     chamam `apiClient`, service ou hook de outra feature.
4. **"Agora" é injetado por props**, não lido dentro do componente: em Receitas/Despesas é o
   `reference: Competence` do servidor, e a situação do mês chega como `status: CompetenceStatus`.
5. Callbacks são `on<Verbo>` (`onClose`, `onEdit`, `onOpen`, `onNew`, `onRetry`). Excluir recebe o
   id; abrir/editar recebem a entidade.
6. Linha de lista clicável é um `<button>` de largura total (teclado e leitor de tela de graça),
   como `EntryRow`. Os testes consultam por papel e nome, não por `data-testid` — o único que resta
   é o de `CategoryCard`.
7. Modal de feature embrulha `shared/components/Modal`. Quando é montado condicionalmente pelo
   container (`modal?.t === "item" && <ExpenseFicha ... />`), passa `isOpen` fixo e não precisa de
   early-return; enquanto o detalhe carrega, renderiza `FichaPlaceholder`.

## Exemplo canônico — apresentacional

`features/dashboard/components/KpiCard.tsx` (arquivo completo):

```tsx
import { cn } from "@/shared/lib/utils";
import { formatCurrency } from "@/shared/lib/formatCurrency";

interface KpiCardProps {
  label: string;
  value: number;
  sublabel: string;
  colorScheme: "green" | "red" | "positive" | "negative";
}

const COLOR_MAP: Record<KpiCardProps["colorScheme"], string> = {
  green: "border-l-[3px] border-l-green",
  red: "border-l-[3px] border-l-red",
  positive: "border-l-[3px] border-l-green",
  negative: "border-l-[3px] border-l-red",
};

export function KpiCard({ label, value, sublabel, colorScheme }: KpiCardProps) {
  return (
    <div
      className={cn(
        "rounded-lg border border-border bg-surface p-5 flex flex-col gap-1",
        COLOR_MAP[colorScheme],
      )}
    >
      <span className="text-[11.5px] font-bold uppercase tracking-wide text-text-muted">
        {label}
      </span>
      <span className="text-[22px] font-bold text-text">{formatCurrency(value)}</span>
      <span className="text-xs text-text-subtle">{sublabel}</span>
    </div>
  );
}
```

**O padrão de variante do projeto inteiro é esse**: um `const UPPER_SNAKE: Record<Uniao, string>`
(ou `Record<Uniao, { label, cls }>`) no módulo, consultado e passado para `cn()`. Nomes em uso:
`COLOR_MAP`, `WIDTHS`, `STATUS_BADGE`, `STYLES`, `ICONS`, `COLORS`, `NAV_ITEMS`, `OPTIONS`, `TABS`.

## Formulários — React Hook Form + zod

**Sempre React Hook Form + `zodResolver`, com o schema em `features/<f>/types/schemas.ts`.**
Valor monetário digitado é lido por `parseMoneyInput()` de `@/shared/lib/money` (nunca
`parseFloat`); competência passada é validada no schema contra o `reference` do servidor.
Há duas formas de montar, conforme o tamanho do formulário:

### (a) Formulário simples — RHF no próprio componente

Canônico: `CategoryForm.tsx`. O formulário **nunca dispara mutation**: `onSave` recebe o payload
pronto e quem chama `.mutate()` é a página. (`LoginForm`/`RegisterForm` são a exceção — ver
"Formulários de autenticação" abaixo.)

```tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Input } from "@/shared/components/Input";
import { Button } from "@/shared/components/Button";
import { categorySchema, type CategoryFormData } from "../types/schemas";

interface CategoryFormProps {
  initial?: { name: string };
  onSave: (data: CategoryFormData) => void;
  onClose: () => void;
  isLoading?: boolean;
}

export function CategoryForm({ initial, onSave, onClose, isLoading }: CategoryFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CategoryFormData>({
    resolver: zodResolver(categorySchema),
    defaultValues: { name: initial?.name ?? "" },
  });

  return (
    <form onSubmit={handleSubmit(onSave)} className="space-y-4">
      <Input
        label="Nome da categoria"
        placeholder="Ex: Moradia, Alimentação..."
        error={errors.name?.message}
        autoFocus
        {...register("name")}
      />
      <div className="flex justify-end gap-2 border-t border-border pt-4">
        <Button variant="ghost" type="button" onClick={onClose}>
          Cancelar
        </Button>
        <Button type="submit" isLoading={isLoading}>
          {initial ? "Salvar" : "Criar categoria"}
        </Button>
      </div>
    </form>
  );
}
```

Detalhes fixos: desestruture exatamente `{ register, handleSubmit, formState: { errors } }`; o
genérico é o tipo `XFormData`; `defaultValues` vem de `initial?.campo ?? ""`;
**`{...register("campo")}` é espalhado por último no `<Input>`**; o erro entra como
`error={errors.campo?.message}`; o rótulo do submit é ternário sobre `initial`.
`LoginForm` e `RegisterForm` usam `noValidate` no `<form>` — com comentário explicando que a
validação nativa do campo `type="email"` barraria o submit antes do React (o schema é a fonte única).

### Formulários de autenticação — `features/auth/components/`

Não há página-container que dispare a ação (as páginas de `(auth)` são Server Components), então o
próprio formulário chama o hook da feature — sempre da **própria** feature:

- **`LoginForm({ next })`** — `const { login } = useAuth();`, estado local `isLoading`/`error` e
  `await login(data, next)` num `try/catch` que mostra
  `getApiErrorMessage(err, "Não foi possível entrar. Tente novamente.")` no bloco
  `role="alert"`. O `next` chega por prop da página (`?next=` lido no servidor); a validação dele é
  do hook (`safeDestination`), não do componente.
- **`RegisterForm()`** — `const { mutate, isPending, error, isEmailTaken } = useRegister();`. O campo
  `passwordConfirmation` existe só no schema/formulário: `onSubmit` desestrutura
  `{ name, email, password }` e manda só isso para a API. No 409 `EMAIL_ALREADY_EXISTS`, o bloco de
  erro acrescenta um `<Link href="/login">Entrar</Link>`.
- Campos com `autoComplete` correto (`email`, `current-password`, `new-password`, `name`) — os
  gerenciadores de senha e o E2E dependem disso.
- Erro de autenticação é **bloco inline**, nunca toast.

### (b) Assistente em etapas — RHF dentro do hook da feature

`ExpenseWizard.tsx` / `RevenueWizard.tsx`. O `useForm`, as etapas, a prévia e a mutation ficam em
`useExpenseWizard` (skill `web-feature-hooks`); o componente só lê e liga campos:

```tsx
export function ExpenseWizard({
  categories,
  initialCompetence,
  reference,
  edit,
  onClose,
}: ExpenseWizardProps) {
  const wizard = useExpenseWizard({ initialCompetence, reference, edit, onDone: onClose });
  const { values, errors, form } = wizard;

  return (
    <WizardShell
      title={wizard.isEdit ? "Editar despesa" : "Nova despesa"}
      step={wizard.step}
      onBack={wizard.back}
      onContinue={wizard.next}
      onConfirm={wizard.submit}
      /* ... */
    >
      {wizard.step === DETAILS_STEP && (
        <MoneyField
          label={AMOUNT_LABEL[values.kind]}
          tone="expense"
          error={errors.amount?.message}
          {...form.register("amount")}
        />
      )}
    </WizardShell>
  );
}
```

Detalhes fixos:

- Erros vêm de **`wizard.errors`**, nunca de `wizard.form.formState.errors` (não re-renderiza).
- Campos que não são `<input>` nativo (`Stepper`, `CompetenceSelect`, `ChoiceCardGroup`) são
  controlados por `value={values.x}` + `onChange={(v) => form.setValue("x", v)}`.
- Rótulos por tipo vêm de `Record<Kind, string>` no módulo (`AMOUNT_LABEL`, `START_LABEL`).
- Cabeçalho, indicador de etapas e rodapé são do `WizardShell`; não reescreva o rodapé.

A Ficha de série (`SeriesFicha` + `useSeriesActions`) é a exceção documentada: seus dois
formulários pequenos (Nova versão, Encerrar) guardam valores em `useState` e validam com
`schema.safeParse` ao confirmar, porque a prévia da linha do tempo é recalculada a cada tecla a
partir desses mesmos valores. Os schemas continuam vindo da feature.

### Rodapé de formulário simples

```tsx
<div className="flex justify-end gap-2 border-t border-border pt-4">
  <Button variant="ghost" type="button" onClick={onClose}>
    Cancelar
  </Button>
  <Button type="submit" isLoading={isLoading}>
    ...
  </Button>
</div>
```

Modais com `footer` (Fichas, `WizardShell`) passam os botões pelo slot `footer` do `Modal`.

## Tailwind

- **Só tokens do tema**, nunca hex cru: `bg-surface`, `bg-bg`, `border-border`, `text-text`,
  `text-text-muted`, `text-text-subtle`, `text-red`, `bg-red-light`, `border-red-mid`, `text-green`,
  `bg-green-light`, `w-nav`, e as cores por tipo de lançamento `tipo.{avulsa,parcelada,recorrente,fixa}`
  (com `.light`). Definidos no bloco `@theme` de `web/app/globals.css` (Tailwind 4, CSS-first, sem arquivo
  de config JS); token novo entra ali como `--color-*`. Cor/ícone/rótulo de cada tipo vêm de
  `ENTRY_KIND` em `@/shared/lib/entry-types` — não repita o mapa numa feature.
- Utilitários `bg-stripes` (prévia de nova versão) e `bg-hatch` (meses que deixam de existir) estão
  em `app/globals.css` como `@utility`.
- **Tamanhos de fonte arbitrários são intencionais** e fazem parte do design:
  `text-[11px]`, `text-[11.5px]`, `text-[13px]`, `text-[13.5px]`, `text-[14.5px]`, `text-[18px]`,
  `text-[22px]`.
- Superfície de card: `rounded-lg border border-border bg-surface p-4|p-5`.
- Título de seção: `text-[13px] font-bold uppercase tracking-wide text-text-muted`.
- Ritmo vertical: `space-y-4` em formulário, `space-y-6` em página, `gap-2.5` em lista de cards.
- Foco: `focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-red` — sempre com a cor
  explícita: na v4 o anel herda `currentColor`. Contorno é `outline-2` sozinho (já é sólido); não
  acrescente `outline` junto, que o `cn()` funde no mesmo grupo.
- **`cn()` sempre que a classe for condicional** ou o componente aceitar `className`; string literal
  simples caso contrário. Condicional: `cn(base, cond && "classes")`.
- Ícones de `lucide-react`, sempre com `size` numérico explícito (12/14/16/18/20/40) e
  `className="mr-1"` quando precedem texto.

## Acessibilidade

`aria-label` em **pt-BR** em todo botão só-ícone (`"Fechar"`, `"Excluir"`, `"Editar"`,
`"Mês anterior"`, `"Próximo mês"`, `"Abrir menu"`, `"Sair"`; o botão com texto
`"Sair de todos os dispositivos"` dispensa `aria-label`), `aria-invalid` / `aria-describedby`
nos campos, `aria-label="Navegação principal"` no `<nav>`. Os testes consultam por papel e nome
acessível — quebrar o rótulo quebra o teste.

## Checklist

- [ ] `interface <Componente>Props` acima do componente, não exportada.
- [ ] `"use client"` só se houver estado/efeito.
- [ ] Apresentacional sem hook de dados; container só com hooks da própria feature; nunca `apiClient`.
- [ ] "Agora" recebido por prop (`reference`/`status` do servidor).
- [ ] Variantes por `Record<Uniao, string>` + `cn()`.
- [ ] Formulário com RHF + zod; `onSave` com payload pronto (simples) ou mutation no hook (assistente).
- [ ] Rodapé no formato padrão ou no slot `footer` do `Modal`.
- [ ] Tokens Tailwind; nada de hex.
- [ ] `aria-label` em pt-BR nos botões só-ícone; linha clicável como `<button>`.
- [ ] Teste ao lado do arquivo (skill `web-testes`).

## Não faça

- Não chame `useMutation`/`apiClient` dentro do componente — mutation mora no hook da feature.
- Não leia `new Date()` dentro de componente — receba `reference` por prop.
- Não interpole classe com template literal (``className={`... ${cond ? "x" : ""}`}``); use `cn()`.
  Só `FilterBar.tsx` e `AppShell.tsx` fazem isso, e é dívida.
- Não use hex arbitrário para cor de tema (os poucos `bg-[#f5f0ff]` existentes são paletas pontuais
  de badge, não precedente).
- Não volte ao formulário com `useState` + bag de erros `Record<string, string>`; use RHF + zod.
- Não guarde/limpe sessão nem navegue depois do login dentro do componente — isso é do `useAuth`/
  `useRegister`. Não mande `passwordConfirmation` para a API.
- Não duplique entre Receitas e Despesas um bloco que caberia em `shared/components/lancamentos/`.
