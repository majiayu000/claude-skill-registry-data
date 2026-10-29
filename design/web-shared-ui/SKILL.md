---
name: web-shared-ui
description: Como escrever primitivos de UI, hooks e libs compartilhadas em web/shared no Smaug — forwardRef só nos wrappers de elemento nativo, cn() + objeto clsx (não cva), wrappers Radix com JSDoc, blocos de lançamentos em shared/components/lancamentos, AppShell/Sidebar sem auth (usuário e saídas por props), toast como objeto e "agora" como parâmetro reference.
---

# `shared/` — primitivos de UI, hooks e libs

## Quando usar esta skill

Ao criar/alterar `web/shared/components/*`, `web/shared/hooks/*` ou `web/shared/lib/*`. Também ao
promover um componente de feature para compartilhado.

## Primitivos de UI — `shared/components/`

### Regra 1: `forwardRef` só nos wrappers de elemento nativo

Exatamente três componentes usam `forwardRef` — `Button`, `Input`, `Select` — porque precisam
funcionar com `{...register()}` do React Hook Form. Todos seguem a mesma forma:
`export interface XProps extends XHTMLAttributes<HTMLXElement>`, `...props` espalhado por último,
e `X.displayName = "X";` no fim.

`shared/components/Button.tsx` (arquivo completo):

```tsx
import { ButtonHTMLAttributes, forwardRef } from "react";
import { cn } from "../lib/utils";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    { className, variant = "default", size = "md", isLoading, disabled, children, ...props },
    ref,
  ) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-lg font-medium transition-colors",
          "focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-red focus-visible:ring-offset-2",
          "disabled:pointer-events-none disabled:opacity-50",
          {
            "bg-red text-white hover:bg-red/90": variant === "default" || variant === "danger",
            "border border-border bg-surface hover:bg-bg": variant === "outline",
            "hover:bg-bg": variant === "ghost",
          },
          {
            "h-8 px-3 text-sm": size === "sm",
            "h-10 px-4 text-base": size === "md",
            "h-12 px-6 text-lg": size === "lg",
          },
          className,
        )}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <span className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
        ) : null}
        {children}
      </button>
    );
  },
);

Button.displayName = "Button";
```

Os demais primitivos são `export function X(props: XProps)`: `Modal`, `ConfirmDialog`, `MonthYearSelect`,
`EmptyState`, `Skeleton`, `Tabs`, `TypeBadge`, `MonthNavigator`, `ToastContainer`, `AppShell`,
`Sidebar`, `BottomNav`. `ErrorBoundary` é o único componente de classe.

**O shell não conhece autenticação.** `AppShell` e `Sidebar` recebem quem está logado e as ações de
saída por props; quem chama `useAuth()` é `app/(app)/layout.tsx` (skill `web-arquitetura`):

```tsx
/** O que o menu mostra de quem está logado; `null` enquanto o perfil não chegou. */
export interface ShellUser {
  name: string;
}

export interface SidebarProps {
  user: ShellUser | null;
  onLogout: () => void;
  onLogoutAll: () => void;
  className?: string;
}
```

`AppShellProps` é `{ user, onLogout, onLogoutAll, children }` e repassa os três ao `Sidebar`
(desktop e overlay mobile). `ShellUser` é um tipo **estrutural mínimo** do próprio `shared/` — não
importe `User` de `@/features/auth/types`. As iniciais caem em `"?"` enquanto `user` é `null`.

### Regra 2: variantes por `cn()` + objeto `clsx`, **não** por `cva`

`class-variance-authority` está em `package.json`, mas **não é importado por arquivo nenhum**.
O mecanismo real de variante é o objeto `clsx` dentro do `cn()` (como no `Button` acima) ou um
`Record<Uniao, string>` no módulo:

```tsx
const WIDTHS = {
  sm: "max-w-sm",
  md: "max-w-lg",
  lg: "max-w-2xl",
  xl: "max-w-[680px]",
  "2xl": "max-w-[760px]",
};
```

**Não introduza `cva` em componente novo.**

### Regra 3: vocabulário de props

`variant: "default" | "outline" | "ghost" | "danger"`, `size: "sm" | "md" | "lg"`,
`width: "sm" | "md" | "lg" | "xl" | "2xl"`, `layer: "base" | "top"`, booleanos com prefixo `is` (`isLoading`, `isDanger`, `isOpen`).
Props opcionais recebem **default na desestruturação, com literal em pt-BR**:

```tsx
export function ConfirmDialog({
  isOpen, onClose, onConfirm,
  title = "Confirmar ação",
  message,
  confirmLabel = "Confirmar",
  cancelLabel = "Cancelar",
  isDanger = false,
  isLoading = false,
}: ConfirmDialogProps) {
```

`ConfirmDialog` **compõe** `Modal` em vez de reimplementar — é o padrão para diálogos novos.

`Modal` aceita os slots `header` (cabeçalho visível rico; `title` continua obrigatório como nome
acessível) e `footer`, e vira folha ancorada na base até 768 px. `ConfirmDialog` abre sempre com
`layer="top"` (acima de uma Ficha) e mostra ícone de lixeira quando `isDanger`. O "Esc fecha só a
confirmação, não a Ficha" vem do aninhamento de diálogos Radix — não trate Esc à mão.

Entrada/saída animadas de `Modal` e `ToastContainer` vêm da `tw-animate-css` (`animate-in`,
`fade-in`, `zoom-in-95`, `slide-in-from-bottom-*`…), sempre sob `motion-safe:` e, no `Modal`, por
`data-[state=open|closed]:` do Radix. Não escreva `@keyframes` próprios nem regra global de
movimento reduzido (congelaria `animate-spin`/`animate-pulse`).

Tela que abre Ficha/assistente **não** os monta só enquanto abertos: envolve-os em `ModalGate`
(`shared/components/Modal.tsx`) com `isOpen`, a `origin` do foco e uma `key` por abertura, como
`DespesasScreen`. Desmontar ao fechar mata a animação de saída. O `Modal` devolve o foco a quem o
abriu — não trate foco à mão.

### Regra 4: Radix com JSDoc justificando

`@radix-ui/react-dialog` e `@radix-ui/react-tabs` sustentam `Modal` e `Tabs`, importados em
namespace (`import * as Dialog from "@radix-ui/react-dialog"`). Todo wrapper carrega um JSDoc **em
português explicando por que o Radix substituiu a versão manual**:

```tsx
/**
 * Apoiado no Radix Dialog: ele entrega focus trap, devolução do foco ao fechar,
 * Escape, trava de scroll e a associação do título via aria-labelledby — tudo o
 * que a versão manual não tinha (o foco escapava para a página atrás).
 */
```

O Radix exige título acessível mesmo sem cabeçalho visível — daí o
`<Dialog.Title className="sr-only">Janela</Dialog.Title>` no ramo sem `title`.

### Regra 5: blocos de lançamentos em `shared/components/lancamentos/`

Receitas e Despesas compartilham extrato, assistente e Ficha. As peças comuns ficam aqui,
**apresentacionais e tipadas sem tipo de feature** (só `Competence`, `EntryKind`, `Tone`,
`LedgerRow<T>` de `shared/lib`):

| Grupo      | Componentes                                                                                                                                                     |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Extrato    | `LedgerLayout`, `MonthHeader`, `MonthStrip`, `MonthSummary`, `EntryGroup`, `EntryRow`, `LedgerEmptyState`, `ErrorNotice`                                        |
| Assistente | `WizardShell`, `StepIndicator`, `ChoiceCard(Group)`, `MiniGrid`, `MoneyField`, `Stepper`, `CompetenceSelect`, `AffectedMonths`                                  |
| Ficha      | `OneTimeFicha`, `SeriesFicha`, `FichaPlaceholder`, `EntryDetailHeader`, `FactGrid`, `ProgressBar`, `MonthCells`, `Legend`, `VersionChips`, `VersionHistoryList` |

- O que varia entre as naturezas entra por prop: textos (`noun`, `emptyHint`), `tone`
  (`"expense"` vermelho / `"revenue"` verde) e `children` para os modais.
- Estado permitido aqui é só de UI (`useId`, confirmação aberta). Dados e mutations chegam prontos:
  `SeriesFicha` recebe o `SeriesActions` de `useSeriesActions` criado pela Ficha da feature.
- Cor, ícone e rótulo de cada tipo vêm de `ENTRY_KIND` (`shared/lib/entry-types.ts`); `TypeBadge`
  usa o mesmo mapa, inclusive no Dashboard.

### Quando promover um componente para `shared/`

Quando **duas features** precisarem dele. Ele entra em `shared/components/`, com props genéricas
(sem tipo de feature) e sem importar nada de `features/`.

## `shared/hooks/`

- **`useToast.ts`** — pub/sub **fora do React** (`toastListeners`/`toastQueue` no módulo) mais
  `useToastState()` para assinar. O consumidor **importa o objeto `toast`, não um hook**:
  `import { toast } from "@/shared/hooks/useToast";` — é isso que permite disparar de dentro de
  `onSuccess`/`onError` de uma mutation.
  ```ts
  export interface Toast {
    id: string;
    type: "success" | "error" | "info" | "warning";
    message: string;
    action?: { label: string; onClick: () => void };
    duration?: number;
  }
  export const toast = { show, success, error, info, warning };
  ```
  O shape `action?: { label, onClick }` é o idioma da casa para "CTA opcional" e reaparece em
  `EmptyStateProps`.
- **`useMediaQuery.ts`** — `useMediaQuery(query: string): boolean` e `useIsMobile()`
  (`"(max-width: 768px)"`).
- **`useDebounce.ts`** — `useDebounce<T>(value: T, delay = 500): T`.
- **`useCompetenceNavigation.ts`** — navegação por mês do Dashboard, Receitas e Despesas;
  `persistKey` opcional grava em `sessionStorage` (com `try/catch`, lido por
  `useSyncExternalStore` para não quebrar a hidratação). `useLedgerNavigation()` é a versão das
  telas de lançamentos (chave `LEDGER_COMPETENCE_KEY`, `adoptReference`).
- **`useSeriesActions.ts`** — modo, abas, formulários e prévia da Ficha de série; recebe os schemas da
  feature por parâmetro.

## `shared/lib/`

Um arquivo por função ou por conceito, **sem barril**:

| Arquivo             | API                                                                                                                                                                                                                                                                                                       |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `utils.ts`          | `cn(...inputs: ClassValue[])` = `twMerge(clsx(inputs))`                                                                                                                                                                                                                                                   |
| `formatCurrency.ts` | `formatCurrency(value: number): string` (`Intl` pt-BR/BRL)                                                                                                                                                                                                                                                |
| `money.ts`          | `parseMoneyInput` (texto → número, `NaN` para lixo), `isValidMoneyInput`, `toMoneyInput`, `formatCompactCurrency` (`"3.420"`)                                                                                                                                                                             |
| `competence.ts`     | `Competence`, `CompetenceStatus`, `ApiCompetenceStatus`, `fromApiStatus`, `sameCompetence`, `compareCompetences`, `addMonths`, `diffMonths`, `monthRange`, `getCurrentCompetence`, `getCompetenceStatus`, `selectableYears`, `formatCompetenceShort` (`"Mai/26"`), `formatCompetenceLong` (`"Maio 2026"`) |
| `preview.ts`        | `splitInstallments`, `affectedMonths`, `seriesSpan`, `seriesTimeline` — prévias puras que espelham o domínio do servidor                                                                                                                                                                                  |
| `ledger.ts`         | `LedgerRow<T>`, `LedgerGroup<T>`, `groupRows`, `totalLabel`, `seriesPeriod`, `seriesRange`, `buildStripCells`                                                                                                                                                                                             |
| `entry-types.ts`    | `EntryKind`, `ENTRY_KIND` (cor, classe do selo, ícone), `versionTint`, `Tone`, `TONE_TEXT`                                                                                                                                                                                                                |
| `dateUtils.ts`      | `MONTH_NAMES_FULL`, `formatMonthYear(year, month)` → `"Set/26"`                                                                                                                                                                                                                                           |
| `type-guards.ts`    | `isString`, `isNumber`, `isObject`, `hasProperty`, `isApiError`                                                                                                                                                                                                                                           |

**Regra que atravessa todo o `shared/lib`: "agora" é um parâmetro opcional com default, nunca lido
implicitamente.**

```ts
export function getCompetenceStatus(
  competence: Competence,
  reference: Competence = getCurrentCompetence(),
): CompetenceStatus;
export function selectableYears(reference: Competence = getCurrentCompetence()): number[];
```

Em Receitas e Despesas o `reference` vem do servidor (campo `reference` das respostas) e é passado
explicitamente; o default local fica para o Dashboard e o `MonthYearSelect` da área de Dados.

É o que torna essas funções 100% testáveis sem fake timers — e o `web/vitest.config.ts` exige
exatamente 100% de cobertura em `shared/lib/**`.

`parseMoneyInput` (em `money.ts`) é o **exemplar do padrão de comentário do projeto**: JSDoc citando o
bug que ele substituiu (`parseFloat(v.replace(",", "."))` transformando `"1.234,56"` em `1.234`).
Imite esse estilo quando escrever uma lib nova.

## Checklist

- [ ] `forwardRef` + `displayName` **apenas** se embrulhar elemento de formulário nativo.
- [ ] Variante por `cn()` + objeto `clsx` ou `Record<Uniao, string>`; nunca `cva`.
- [ ] Defaults de props em pt-BR na desestruturação.
- [ ] Wrapper de biblioteca com JSDoc em pt-BR justificando a escolha.
- [ ] Nada importado de `features/`.
- [ ] Função de lib com "agora" como parâmetro `reference` default.
- [ ] Teste ao lado, cobrindo os thresholds de `shared/**` em `web/vitest.config.ts`.

## Não faça

- Não use `cva`.
- Não importe de `@/features/...` dentro de `shared/` — nem hook, nem tipo. Precisa de dado de
  uma feature? Declare o tipo mínimo em `shared/` e receba por prop, como `ShellUser` no `Sidebar`.
- Não leia `new Date()` dentro de uma função de `shared/lib`.
- Não crie `shared/lib/index.ts` nem `shared/components/index.ts`.
- Não use `shared/types/index.ts` como destino de tipo novo: ele já está morto (nada o importa) e
  duplica `Toast` e `ApiError`.
