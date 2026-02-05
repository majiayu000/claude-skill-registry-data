---
name: planificador-mvp
description: Crea planes de implementación realistas para MVPs de 2-4 semanas. Define alcance mínimo, stack tecnológico, tareas priorizadas y cronograma. Úsalo después de validar una idea para planificar la construcción del producto mínimo viable.
---

# Planificador de MVP (2-4 Semanas)

## Propósito

Este skill te ayuda a convertir una idea validada en un plan de ejecución concreto y realista para construir un MVP funcional en 2-4 semanas como desarrollador solitario.

## Filosofía del MVP

### Principios Fundamentales

**MENOS ES MÁS**: Un MVP que funciona bien con 3 características es infinitamente mejor que uno con 10 características a medias.

**REGLAS DE ORO:**
1. Si una característica no es absolutamente esencial para demostrar el valor core, NO va en el MVP
2. El MVP debe resolver UN problema específico extremadamente bien
3. Cada día cuenta - si algo toma más de 2 días, busca alternativas
4. La perfección es enemiga del lanzamiento
5. Validación > Perfección técnica

### ¿Qué NO es un MVP?

- ❌ Un producto completo con menos features
- ❌ Una beta con bugs
- ❌ Una versión para "ver qué pasa"
- ❌ Todo lo que se te ocurre en versión simple

### ¿Qué SÍ es un MVP?

- ✅ La mínima funcionalidad que demuestra tu propuesta de valor única
- ✅ Algo que un early adopter usaría y pagaría (incluso con limitaciones)
- ✅ Un experimento para validar tu hipótesis principal
- ✅ Una herramienta funcional, no un demo

## Proceso de Planificación

### PASO 1: Definir el Valor Core

**Pregunta fundamental:** ¿Cuál es la ÚNICA cosa que hace tu producto valioso?

Completa esta frase:
"Este producto permite a [usuario objetivo] hacer [acción específica] de manera [ventaja única] para que [resultado deseado]"

**Ejemplo:**
- ❌ Malo: "Mi app ayuda a las personas a ser más productivas"
- ✅ Bueno: "Este producto permite a freelancers registrar tiempo automáticamente mientras codean para que puedan facturar clientes con precisión sin interrumpir su flow"

### PASO 2: Identificar el Happy Path Crítico

**El Happy Path** es el flujo más simple posible que demuestra el valor core.

**Estructura:**
1. Usuario llega/se registra
2. Usuario realiza acción core
3. Usuario obtiene resultado valioso
4. [Opcional] Usuario paga/se compromete

**Elimina todo lo demás** - autenticación social, onboarding elaborado, dashboards complejos, etc.

### PASO 3: Stack Tecnológico Pragmático

**Criterios de selección:**
- ✅ Ya lo conoces o puedes aprenderlo en 1 día
- ✅ Tiene documentación excelente y comunidad activa
- ✅ Deployment simple (no Kubernetes en el MVP)
- ✅ Escala suficiente para 100-1000 usuarios

**Stacks recomendados para solo developer:**

**Para SaaS/Web Apps:**
- Frontend: Next.js + Tailwind + shadcn/ui
- Backend: Next.js API routes o Supabase
- Base de datos: PostgreSQL (Supabase/Neon)
- Auth: Clerk o Supabase Auth
- Payments: Stripe Checkout (modo one-click)
- Hosting: Vercel

**Para Herramientas/CLIs:**
- Python + Typer + Rich
- Node.js + Commander
- Distribución: PyPI o npm

**Para Apps Móviles:**
- React Native + Expo
- Backend: Supabase o Firebase

**Regla:** Si necesitas más de 3 servicios externos, estás sobrecomplicando.

### PASO 4: Definir Alcance Mínimo

**Metodología de las 3 Listas:**

#### 🟢 LISTA VERDE: En el MVP (Semana 1-4)
Características absolutamente esenciales para el valor core.
Máximo 5 características.

#### 🟡 LISTA AMARILLA: Post-MVP (Mes 2)
Mejoras importantes pero no bloqueantes.
Agregar solo después de validar tracción.

#### 🔴 LISTA ROJA: Futuro Lejano
Nice-to-haves que no importan ahora.
Olvidar completamente por ahora.

**Ejemplo para un "Time Tracker para Developers":**

🟢 **Verde (MVP):**
1. Detectar cuando el usuario está codeando (monitorear procesos)
2. Registrar tiempo automáticamente por proyecto
3. Generar reporte semanal simple
4. Exportar a CSV
5. Configuración básica (qué proyectos trackear)

🟡 **Amarilla (Post-MVP):**
- Dashboard con gráficos
- Integraciones con Jira/Linear
- Facturación automática
- App móvil

🔴 **Roja (Futuro):**
- Team features
- AI para categorizar tareas
- Timesheet approval workflow
- Integraciones contables

## Recordatorios Finales

- Cada semana que pasa sin lanzar es una semana de aprendizaje perdido
- Los usuarios te dirán qué construir después - no lo adivines ahora
- Un MVP feo que funciona > Un producto bonito que nunca terminas
- El mejor momento para lanzar fue ayer, el segundo mejor es hoy
- La vergüenza de lanzar algo imperfecto dura una semana; el arrepentimiento de no lanzar dura años
