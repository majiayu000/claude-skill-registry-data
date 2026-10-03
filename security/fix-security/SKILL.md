---
name: fix-security
description: Checklist de protección de rutas y APIs para aplicaciones Next.js con auth basada en cookies.
---

# Skill: fix-security

Checklist de protección de rutas y APIs para aplicaciones Next.js con auth basada en cookies.

## Cuando Usar
- Después de crear nuevas rutas protegidas
- Al auditar seguridad existente
- Antes de cada release mayor

## Checklist

### 1. Middleware (Server-Side)
```bash
# Verificar que todas las rutas protegidas estén en el matcher
grep -n "matcher" middleware.ts
```
- [ ] Rutas admin en matcher: `/admin/:path*`
- [ ] Rutas upload en matcher: `/upload`
- [ ] Rutas auth en matcher: `/login`, `/register`
- [ ] Validación de cookie `auth_session`
- [ ] Verificación de expiración `session.exp > Date.now()`
- [ ] Verificación de rol `session.role === "admin"`
- [ ] Limpieza de cookie expirada

### 2. API Routes
```bash
# Verificar auth en endpoints sensibles
grep -rn "cookies()" app/api/
```
- [ ] POST/PUT/DELETE validan sesión
- [ ] Operaciones sensibles verifican rol
- [ ] Session viene de cookie (no headers)
- [ ] Errores retornan JSON (no HTML)

### 3. Componentes Client-Side
```bash
# Verificar guards en componentes
grep -rn "useAuth" app/ components/
```
- [ ] Páginas sensibles usan `useAuth()`
- [ ] Redirect si no hay sesión
- [ ] Redirect si rol incorrecto
- [ ] Loading state mientras se verifica

## Archivos de Referencia
- `middleware.ts` — Protección server-side
- `context/AuthContext.tsx` — Hook useAuth
- `app/api/tracks/route.ts` — Ejemplo API protegida
- `app/admin/page.tsx` — Página protegida

## Output Esperado
```markdown
## Security Fix Report

### Protecciones Agregadas
- [ARCHIVO] Descripción del cambio

### Verificación
- [ ] Middleware matcher actualizado
- [ ] API routes con auth
- [ ] Componentes con guards
```
