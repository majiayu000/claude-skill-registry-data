---
name: react19
description: Patrones y APIs de React 19. Usa cuando trabajes con componentes, hooks, o cualquier codigo React para asegurar que se usen las APIs mas recientes.
---

# React 19 - Patrones Modernos

Cuando escribas codigo React para PROSEGUIT, usa exclusivamente APIs de React 19:

## APIs nuevas de React 19
- **`use()` hook**: Para leer promesas y contexto directamente
- **`useActionState()`**: Reemplaza `useReducer` para form actions
- **`useFormStatus()`**: Estado de formularios en componentes hijos
- **`useOptimistic()`**: Actualizaciones optimistas de UI
- **React Compiler**: No usar `useMemo`, `useCallback`, `memo` manualmente - el compilador los maneja

## Patrones a seguir
- Formularios con `<form action={...}>` nativo (Server Actions pattern)
- `ref` como prop normal (ya no necesita `forwardRef`)
- `<Context>` como provider directo (ya no `<Context.Provider>`)
- Metadata con `<title>`, `<meta>`, `<link>` directamente en componentes
- Stylesheet precedence con `precedence` prop en `<link>`

## Patrones a EVITAR (obsoletos)
- NO usar `forwardRef` -> pasar `ref` como prop
- NO usar `<Context.Provider>` -> usar `<Context>` directo
- NO usar `useMemo`/`useCallback`/`memo` innecesariamente -> React Compiler
- NO usar `useEffect` para fetch -> usar `use()` con Suspense
- NO usar `useContext` -> usar `use(Context)`

## Estructura de componentes PROSEGUIT
```tsx
// Componente funcional simple con CSS modules
import styles from './MiComponente.module.css';

function MiComponente({ datos, ref }) {
  return (
    <div className={styles.container} ref={ref}>
      {datos}
    </div>
  );
}
```
