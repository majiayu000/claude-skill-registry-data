---
name: fix-branding
description: Workflow de búsqueda y reemplazo de logos/marcas inconsistentes en el codebase.
---

# Skill: fix-branding

Workflow de búsqueda y reemplazo de logos/marcas inconsistentes en el codebase.

## Cuando Usar
- Cuando se detecta un logo incorrecto (ej: Spotify en vez de PressPlay)
- Al renombrar la marca del proyecto
- En auditoría de branding

## Instrucciones para el Agente:

### Paso 1: Buscar Referencias No Deseadas
```bash
# SVGs inline de otras marcas
grep -rn "M12 0C5.4 0" --include="*.tsx" --include="*.ts"

# Links genéricos a plataformas
grep -rn "open.spotify.com" --include="*.tsx" --include="*.ts"

# Aria-labels incorrectos
grep -rn 'aria-label="Spotify"' --include="*.tsx" --include="*.ts"
```

### Paso 2: Clasificar
| Tipo | Acción | Ejemplo |
|------|--------|---------|
| Logo como marca | REEMPLAZAR | SVG en Header/Register |
| Link genérico | REEMPLAZAR/EVALUAR | `open.spotify.com` sin track |
| Link a track | MANTENER | `spotify_url` de track |
| SocialBar links | MANTENER | Links de plataformas del artista |

### Paso 3: Reemplazar
```tsx
// ANTES (logo incorrecto)
<svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
  <path d="M12 0C5.4 0..." />  {/* Spotify SVG */}
</svg>

// DESPUÉS (PressPlay logo)
<img src="/logo.svg" alt="PressPlay" className="w-8 h-8" />
```

### Paso 4: Verificar
- [ ] No hay SVGs de otras marcas en posiciones de logo
- [ ] Links externos son apropiados
- [ ] Logo PressPlay visible en Header y Footer

## Logo Correcto
- **Archivo**: `/public/logo.svg`
- **Clases**: `w-8 h-8` (header), `w-6 h-6` (footer)
- **Alt text**: "PressPlay"

## Archivos Comúnmente Afectados
- `components/Header.tsx`
- `components/Footer.tsx`
- `app/register/page.tsx`
- `components/SocialBar.tsx`
- `app/dashboard/page.tsx`
