---
name: i18n-enforcer
description: Enforces internationalization best practices for Breath of Now. Use this skill when creating or editing any component, page, or UI element. Ensures NO hardcoded text and proper use of next-intl translations.
---

# i18n Enforcer Skill

Este skill garante que todo o texto visível ao utilizador no projecto Breath of Now está devidamente internacionalizado. **ZERO texto hardcoded é aceitável.**

## Quando Usar

Aplica automaticamente este skill quando:
- Criar novos componentes ou páginas
- Editar elementos UI existentes
- Adicionar mensagens de erro, labels, ou qualquer texto
- Rever código para compliance de i18n

## Regras Core

### 1. NUNCA Hardcodes Texto

```tsx
// ❌ ERRADO:
<h1>Welcome to Breath of Now</h1>
<button>Sign In</button>
<p>Loading...</p>
<span aria-label="Close menu">×</span>

// ✅ CORRECTO:
const t = useTranslations('HomePage');

<h1>{t('title')}</h1>
<button>{t('signIn')}</button>
<p>{t('loading')}</p>
<span aria-label={t('closeMenu')}>×</span>
```

### 2. Sempre Usar useTranslations Hook

```tsx
import { useTranslations } from 'next-intl';

export function MyComponent() {
  const t = useTranslations('MyComponent');
  
  return <div>{t('welcomeMessage')}</div>;
}
```

### 3. Estrutura de Ficheiros de Tradução

Localização: `/messages/{locale}.json`

Locales suportados:
- `en.json` - English (primário)
- `pt.json` - Português
- `es.json` - Español
- `fr.json` - Français

### 4. Organização de Namespaces

```json
{
  "common": {
    "loading": "Loading...",
    "error": "An error occurred",
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "edit": "Edit"
  },
  "nav": {
    "home": "Home",
    "pricing": "Pricing",
    "account": "Account"
  },
  "expenses": {
    "title": "ExpenseFlow",
    "addExpense": "Add Expense",
    "categories": "Categories"
  },
  "fitlog": {
    "title": "FitLog",
    "startWorkout": "Start Workout",
    "history": "History"
  }
}
```

### 5. Valores Dinâmicos

```tsx
// No componente
const t = useTranslations('Dashboard');
<p>{t('greeting', { name: user.name })}</p>
<p>{t('lastSync', { date: formatDate(lastSyncDate) })}</p>

// No ficheiro de tradução
{
  "Dashboard": {
    "greeting": "Hello, {name}!",
    "lastSync": "Last synced: {date}"
  }
}
```

### 6. Pluralização

```tsx
// No componente
<p>{t('itemCount', { count: items.length })}</p>
<p>{t('daysRemaining', { count: daysLeft })}</p>

// No ficheiro de tradução
{
  "itemCount": "{count, plural, =0 {No items} =1 {1 item} other {# items}}",
  "daysRemaining": "{count, plural, =0 {Last day!} =1 {1 day remaining} other {# days remaining}}"
}
```

## Checklist de Verificação

Antes de completar qualquer tarefa, verifica:

- [ ] Nenhuma string hardcoded em JSX/TSX
- [ ] Todo o texto usa hook `useTranslations()`
- [ ] Keys de tradução adicionadas a TODOS os 4 ficheiros de locale
- [ ] Namespace corresponde ao nome do componente/página
- [ ] Valores dinâmicos usam interpolação adequada
- [ ] Pluralização tratada onde necessário
- [ ] Alt text de imagens também traduzido
- [ ] Aria-labels traduzidos

## Erros Comuns

### Erro 1: Esquecer alt text

```tsx
// ❌ ERRADO
<img src={logo} alt="Logo" />

// ✅ CORRECTO
<img src={logo} alt={t('logoAlt')} />
```

### Erro 2: Hardcoded aria-labels

```tsx
// ❌ ERRADO
<button aria-label="Close menu">X</button>

// ✅ CORRECTO
<button aria-label={t('closeMenu')}>X</button>
```

### Erro 3: Placeholders hardcoded

```tsx
// ❌ ERRADO
<Input placeholder="Enter your email" />

// ✅ CORRECTO
<Input placeholder={t('emailPlaceholder')} />
```

### Erro 4: Títulos de página hardcoded

```tsx
// ❌ ERRADO
<title>ExpenseFlow - Breath of Now</title>

// ✅ CORRECTO
<title>{t('pageTitle')}</title>
```

### Erro 5: Mensagens de erro hardcoded

```tsx
// ❌ ERRADO
toast.error('Failed to save');

// ✅ CORRECTO
toast.error(t('errors.saveFailed'));
```

### Permitido: Console messages

```tsx
// ✅ OK - mensagens de console não precisam tradução
console.log('Component mounted');
console.error('Failed to fetch data:', error);
```

## Comandos de Detecção Rápida

Para encontrar texto hardcoded no codebase:

```bash
# Encontrar potenciais strings hardcoded em ficheiros TSX
grep -r ">[A-Z][a-z]" --include="*.tsx" src/

# Encontrar strings que podem estar hardcoded
grep -rn '"[A-Z][a-zA-Z ]{3,}"' --include="*.tsx" src/

# Encontrar elementos com text content directo
grep -rn ">[a-zA-Z].*<" --include="*.tsx" src/
```

## Padrão de Implementação

Quando criar um novo componente:

### Passo 1: Definir namespace no ficheiro

```tsx
'use client';

import { useTranslations } from 'next-intl';

export function NewComponent() {
  const t = useTranslations('NewComponent');
  
  return (
    <div>
      <h2>{t('title')}</h2>
      <p>{t('description')}</p>
    </div>
  );
}
```

### Passo 2: Adicionar traduções a TODOS os locales

```json
// messages/en.json
{
  "NewComponent": {
    "title": "Component Title",
    "description": "Component description here"
  }
}

// messages/pt.json
{
  "NewComponent": {
    "title": "Título do Componente",
    "description": "Descrição do componente aqui"
  }
}

// Repetir para es.json, fr.json
```

### Passo 3: Verificar

```bash
# Verificar que não há texto hardcoded
grep -n ">[A-Z]" src/components/new-component.tsx
```

## Prioridade

Este skill tem **PRIORIDADE MÁXIMA**. Nenhum PR ou mudança de código deve ser aceite sem implementação adequada de i18n. Este é um princípio core da acessibilidade global do Breath of Now.

## Ficheiros de Referência

Verifica sempre:
- `/messages/en.json` - Traduções principais
- `.claude/commands/i18n-check.md` - Comando de verificação
- Componentes existentes para padrões de uso

---

**REGRA DE OURO**: Se um utilizador vai ver o texto, esse texto DEVE ser traduzido. Sem excepções.
