---
name: "framework-react"
description: "Fornece padrões de engenharia e arquitetura para a biblioteca React (React 18+ / React 19) e seu ecossistema. Cobre componentes funcionais, Hooks avançados, Server Components (RSC), gerenciamento de estado (Context, Zustand, TanStack Query), roteamento, otimização de performance e testes."
---

# Habilidade de IA: Engenharia e Arquitetura React (framework-react)

Esta skill orienta a inteligência artificial a atuar como especialista na biblioteca **React** (versões 18 e 19) e no seu ecossistema moderno, alinhada à documentação oficial mantida pela Meta ([react.dev](https://react.dev/)). Cobre arquitetura de componentes funcionais, React Server Components (RSC), Hooks, gerenciamento de estado global e de servidor, otimização de renderização e testes.

---

## 🧭 Arquitetura de Componentes e React Server Components (RSC)

### 1. Separação entre Server Components e Client Components
- **Server Components (RSC - Padrão no React 19 / Next.js App Router)**:
  - Componentes executados exclusivamente no servidor sem envio de bundle JavaScript ao cliente.
  - Ideais para acesso direto a bancos de dados, APIs internas e renderização estática/dinâmica pesada.
- **Client Components (`'use client'`)**:
  - Componentes hidratados no navegador que utilizam estado local (`useState`), efeitos (`useEffect`) ou escutadores de eventos DOM (`onClick`, `onChange`).

### 2. Padrões de Hooks Fundamentais e Avançados
```tsx
import React, { useState, useTransition, useId } from 'react';

interface SearchBoxProps {
  onSearch: (query: string) => void;
}

export const SearchBox: React.FC<SearchBoxProps> = ({ onSearch }) => {
  const [input, setInput] = useState('');
  const [isPending, startTransition] = useTransition();
  const inputId = useId();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInput(value);
    
    // Atualização de baixa prioridade sem congelar a interface
    startTransition(() => {
      onSearch(value);
    });
  };

  return (
    <div className="search-container">
      <label htmlFor={inputId}>Buscar Produtos:</label>
      <input
        id={inputId}
        type="text"
        value={input}
        onChange={handleChange}
        placeholder="Digite para pesquisar..."
      />
      {isPending && <span className="spinner">Atualizando resultados...</span>}
    </div>
  );
};
```

---

## 🛠️ Gerenciamento de Estado Global e Estado de Servidor

### 1. Estado de Servidor vs. Estado de UI
- **Estado de Servidor (Server State)**: Utilize **TanStack Query (React Query)** ou **SWR** para caching, revalidação automática em segundo plano, paginação e mutações assíncronas com rollback otimista.
- **Estado de UI Global (Client State)**:
  - Para estados simples: React Context API.
  - Para estados complexos de alta performance: **Zustand** ou **Jotai** (evitando re-renderizações desnecessárias da árvore inteira).

---

## ⚡ Otimização de Performance e Medição de Web Vitals

1. **Evitar Re-renderizações Indesejadas**:
   - Mantenha o estado o mais próximo possível de onde ele é utilizado (*Lift state up* apenas quando necessário).
   - Utilize a compilação automática do **React Compiler** (React 19) ou memoização manual consciente com `useCallback` e `useMemo`.
2. **Code-Splitting e Lazy Loading**:
   - Importe componentes pesados dinamicamente via `React.lazy()` encapsulados em `<Suspense fallback={<Loading />}>`.

---

## 🧪 Estratégias de Testes

- **React Testing Library & Vitest/Jest**:
  - Teste comportamentos visíveis do ponto de vista do usuário final (usando seletores como `getByRole`, `getByText`) em vez de testar detalhes de implementação interna do estado.

---

## 🔗 Integração com Outras Skills

- Para desenvolvimento completo de interfaces com TypeScript e acessibilidade (WCAG), consulte [frontend-developer](../../roles/frontend-developer/SKILL.md) e [lang-typescript](../../languages/lang-typescript/SKILL.md).
- Para automação de suítes de testes em componentes e aplicações web, consulte [framework-testing-javascript](../framework-testing-javascript/SKILL.md) e [qa-engineer](../../roles/qa-engineer/SKILL.md).
- Para proteção contra vulnerabilidades web (XSS, CSRF, Secure Headers), consulte [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
