---
name: viviana-blog
description: Asistente para el blog de psicología de Viviana Poveda. Ayuda con implementación Supabase, queries de base de datos, gestión de posts, y desarrollo del admin panel. Usa cuando trabajes en blog, psicología, Supabase, o Viviana Poveda.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
model: sonnet
---

# Blog de Psicología - Viviana Poveda

Skill personalizado para la implementación del blog dinámico con Supabase.

## 📋 Contexto del Proyecto

**Cliente:** Ps. Viviana Poveda - Psicóloga Clínica
**Proyecto:** Blog profesional para atraer pacientes
**Tech Stack:** Supabase + Webpack 5 + Tailwind CSS + jQuery
**Timeline:** 9 semanas en 5 fases
**Supabase Project:** lakuiqqqrbvdjfmcnqho.supabase.co

## 🎯 Objetivo de Negocio

Crear un blog que:
- ✅ Demuestre expertise en temas psicológicos (ansiedad, depresión, relaciones)
- ✅ Capture leads vía newsletter y recursos descargables
- ✅ Genere confianza con casos de estudio y testimonios
- ✅ Facilite conversión a citas con CTAs estratégicos
- ✅ Sea 100% gestionable sin código (admin panel)

## 🗄️ Arquitectura de Base de Datos

**10 Tablas principales:**

1. **posts** - Contenido del blog (con SEO meta tags)
2. **categories** - Temas psicológicos (Ansiedad, Depresión, etc.)
3. **tags** - Cross-referencing de contenido
4. **post_tags** - Relación many-to-many
5. **authors** - Viviana + posibles invitados
6. **comments** - Sistema moderado (pending/approved/rejected)
7. **subscribers** - Newsletter con confirmación por email
8. **resources** - PDFs descargables (lead magnets)
9. **resource_downloads** - Tracking de descargas
10. **post_views** - Analytics de visitas

**Funciones SQL:**
- `increment_view_count(post_id)`
- `get_comment_count(post_id)`
- `get_top_posts(days, limit_count)`

Para schema completo, ver [database-schema.md](database-schema.md)

## 📁 Estructura de Archivos

Se ha implementado una arquitectura modular en JavaScript, separando la lógica en `utils`, `components` y `admin`.

**Archivos clave creados (+30 archivos):**

✅ **JavaScript Modules:**
- `src/assets/js/supabase-client.js` - Core connection + helpers API
- `src/assets/js/blog.js` - Lógica del listado del blog
- `src/assets/js/blog-post.js` - Lógica del post individual
- `src/assets/js/utils/` - Helpers para formato, SEO, UI, caché y widgets.
- `src/assets/js/components/` - Módulos para header, footer y sidebar dinámicos.
- `src/assets/js/admin/` - Lógica completa del panel de administración (auth, posts, comments, etc.).

✅ **HTML & CSS:**
- `src/admin.html` - Panel de administración completo.
- `src/assets/css/admin.css` - Estilos del panel de admin.

✅ **Scripts de Build/Test:**
- `scripts/generate-sitemap.js` - Generador de sitemap dinámico.
- `scripts/run-integration-tests.js` - Runner para tests de integración.
- `scripts/populate-posts.js` - Seeder de contenido.

Ver estructura completa y estado de cada archivo en [file-structure.md](file-structure.md).

## 🚀 Fases de Implementación

**Estado Global:** 98% Completado - Actualizado: 30/12/2025

### ✅ Fase 1: Infraestructura Base - COMPLETADA (100%)
- ✅ Supabase database (10 tablas + RLS policies)
- ✅ Storage buckets (blog-images, resources, etc.)
- ✅ Cliente Supabase y conexión verificada.
- ✅ Funciones SQL y scripts de seeding.

### ✅ Fase 2: Blog Público Dinámico - COMPLETADA (100%)
- ✅ Listado de blog con paginación, búsqueda y filtros.
- ✅ Vista de post individual con SEO, comentarios y vistas.
- ✅ Widgets de sidebar (posts recientes, categorías) dinámicos.

### ✅ Fase 3: Admin Panel - COMPLETADA (100%)
- ✅ Login con Supabase Auth.
- ✅ Dashboard con estadísticas.
- ✅ CRUD completo para posts con editor de texto enriquecido y subida de imágenes.
- ✅ Moderación de comentarios.
- ✅ Gestión y exportación de suscriptores.

### ✅ Fase 4: Email Marketing - COMPLETADA (100%)
- ✅ Sistema de comentarios implementado y funcional
- ✅ Formularios de Newsletter integrados en footer
- ✅ Lógica de suscripción con tokens de confirmación
- ✅ **Edge Function desplegada** para envío automático de emails con Resend
- ✅ **Trigger de DB configurado** (envío automático al suscribirse)
- ✅ Plantilla de email profesional en HTML
- ✅ Botón de confirmación manual en admin panel
- ✅ Sistema de recursos descargables (PDFs, MP3s, etc.)

### ✅ Fase 5: Analytics & Optimización - COMPLETADA (90%)
- ✅ Sitemap dinámico generado con `scripts/generate-sitemap.js`
- ✅ Script de tests de integración (`run-integration-tests.js`) creado
- ✅ **Dashboard con gráficos avanzados** (Chart.js)
- ✅ **Gráficos de visitas y suscriptores** (últimos 7 días)
- ✅ Auditoría de seguridad completada (RLS, search_path fix)
- ✅ Optimización de imágenes configurada (WebP, lazy loading)

Ver checklist detallado en [phase-checklist.md](phase-checklist.md)

## 🎨 Estrategia de Contenido

**Categorías Implementadas:** Ansiedad, Depresión, Relaciones, Autoestima, Duelo, Terapia, Mindfulness, Estrés.
**Lead Magnets Planeados:** Guía de Ansiedad (PDF), Diario de Gratitud (PDF), Audios de Respiración (MP3).
**CTAs:** Implementados en el blog para agendar sesiones.

Ver estrategia completa en [content-strategy.md](content-strategy.md)

## 💡 Convenciones de Código

### Supabase Queries Pattern
```javascript
// Helpers en supabase-client.js
import { supabase } from './supabase-client.js';

export async function getPublishedPosts(page = 1, limit = 6) {
  const offset = (page - 1) * limit;
  const { data, error, count } = await supabase
    .from('posts')
    .select('*, author:authors(*), category:categories(*)', { count: 'exact' })
    .eq('status', 'published')
    .order('published_at', { ascending: false })
    .range(offset, offset + limit - 1);
  return { data, error, count };
}
```

### Naming Conventions
- **Archivos JS:** `kebab-case.js`
- **Funciones:** `camelCase()`
- **Database:** `snake_case`

## 🔧 Comandos Útiles

```bash
# Servidor de desarrollo con Hot Reload
npm run dev

# Build para producción
npm run build

# Ejecutar tests de integración
npm run test:integration
```

## 📊 Métricas Actuales (30/12/2025)

- **Posts publicados:** 3+
- **Archivos JS creados/modificados:** ~25
- **Fases Completadas:** 3 de 5
- **Build time:** ~5-7 segundos
- **Hot reload:** < 2 segundos

## 🎯 Cuándo Usar Este Skill

Actívame cuando:
- Trabajas en cualquier archivo del blog de Viviana.
- Necesitas consultar el schema de la base de datos o la estructura de archivos.
- Escribes queries de Supabase.
- Implementas features del admin panel o del blog público.
- Tienes dudas sobre la arquitectura, convenciones o estado del proyecto.
- Estás trabajando en cualquiera de las fases del plan.
