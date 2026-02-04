---
name: guia-diseno-ui-moderno
description: Enseña principios de diseño UI/UX profesional para crear interfaces hermosas y modernas. Incluye paletas de colores contemporáneas, tipografía, espaciado y componentes. Evita clichés como gradientes azul-púrpura. Úsalo al diseñar cualquier interfaz de usuario.
---

# Guía de Diseño UI Moderno

## Propósito

Este skill te ayuda a crear interfaces de usuario hermosas, profesionales y modernas que no se ven genéricas ni amateur. Nos alejamos de los clichés (gradientes azul-púrpura, colores saturados, sombras excesivas) y adoptamos diseño contemporáneo de alta calidad.

## Filosofía de Diseño

### Principios Fundamentales

**MENOS ES MÁS**: El diseño moderno es limpio, espaciado y respira.

**REGLAS DE ORO:**
1. La funcionalidad siempre antes que la estética
2. La consistencia es más importante que la creatividad
3. El espacio en blanco es un elemento de diseño, no espacio desperdiciado
4. Los colores deben tener propósito, no decoración
5. La jerarquía visual guía al usuario sin pensar

### Anti-Patrones a EVITAR

**❌ NO HAGAS ESTO:**
- Gradientes azul-púrpura (#667eea → #764ba2)
- Colores neón o altamente saturados (hsl(*, *, >80%))
- Sombras box-shadow excesivas (0 20px 60px rgba(...))
- Fuentes decorativas para texto de contenido
- Botones con border-radius >12px (pastillas)
- Más de 3 colores primarios
- Animaciones innecesarias
- Glassmorphism excesivo
- Degradados en todos lados

**✅ SÍ HAZ ESTO:**
- Paletas monocromáticas o dicromáticas sutiles
- Colores con saturación moderada (hsl(*, 30-70%, 40-70%))
- Sombras sutiles y elevaciones realistas
- Tipografía limpia y legible
- Border-radius consistente (4px, 6px, 8px)
- Color de acento único y estratégico
- Micro-interacciones significativas
- Transparencias sutiles donde tengan sentido
- Color donde agregue significado

## Sistema de Colores Modernos

### Paletas Profesionales (NO usar gradientes cliché)

#### Opción 1: Monocromático Moderno (Minimalista)
```css
/* Base: Grises refinados */
--bg-primary: #fafafa;
--bg-secondary: #f4f4f5;
--bg-tertiary: #e4e4e7;

--text-primary: #18181b;
--text-secondary: #52525b;
--text-tertiary: #a1a1aa;

--border: #e4e4e7;

/* Acento: Un solo color estratégico */
--accent: #16a34a; /* Verde bosque profesional */
--accent-hover: #15803d;
--accent-light: #dcfce7;
```

#### Opción 2: Dark Mode Profesional
```css
--bg-primary: #0a0a0a;
--bg-secondary: #171717;
--bg-tertiary: #262626;

--text-primary: #fafafa;
--text-secondary: #d4d4d8;
--text-tertiary: #71717a;

--border: #2d2d2d;

--accent: #22c55e; /* Verde esmeralda */
--accent-hover: #16a34a;
--accent-light: #052e16;
```

## Tipografía

### Fuentes Recomendadas

**Sans-serif modernas (99% de los casos):**
```css
/* Opción 1: Inter (versátil, profesional) */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

/* Opción 2: System stack (performance, nativo) */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 
             Roboto, Oxygen, Ubuntu, sans-serif;
```

### Escala Tipográfica

```css
/* Mobile-first, crece en desktop */
--text-xs: 0.75rem;    /* 12px - Labels, captions */
--text-sm: 0.875rem;   /* 14px - Body small, metadata */
--text-base: 1rem;     /* 16px - Body text */
--text-lg: 1.125rem;   /* 18px - Large body, subtitles */
--text-xl: 1.25rem;    /* 20px - Section headings */
--text-2xl: 1.5rem;    /* 24px - Card titles */
--text-3xl: 1.875rem;  /* 30px - Page titles */
```

## Componentes UI Modernos

### Botones

```css
/* Primary - Acción principal */
.btn-primary {
  background: var(--accent);
  color: white;
  padding: 0.625rem 1.25rem;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.875rem;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-primary:hover {
  background: var(--accent-hover);
  transform: translateY(-1px);
}
```

## Sombras y Elevación

```css
/* Apenas perceptible (hover states) */
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);

/* Elevación ligera (cards, dropdowns) */
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.05),
             0 2px 4px -2px rgb(0 0 0 / 0.05);
```

## Checklist de Diseño Moderno

- [ ] ¿Usé máximo 2-3 colores (más grises neutros)?
- [ ] ¿Evité gradientes azul-púrpura y colores neón?
- [ ] ¿Las sombras son sutiles (no 0 20px 60px)?
- [ ] ¿El border-radius es consistente (6-8px)?
- [ ] ¿Usé espaciado de la escala (8px, 16px, 24px)?
- [ ] ¿La tipografía tiene máximo 3 pesos?
- [ ] ¿Hay suficiente espacio en blanco?
- [ ] ¿Los botones tienen estados hover/active?
- [ ] ¿El contraste de texto pasa WCAG AA (4.5:1)?

## Referencias de Inspiración

**Estudia estos sitios (NO copies, inspírate):**
- Linear.app - Minimalismo profesional perfecto
- Vercel.com - Espaciado y tipografía ejemplares
- Stripe.com - Elegancia B2B
- Cal.com - Limpieza moderna
- Resend.com - Simplicidad efectiva

## Recordatorios Finales

- El buen diseño es invisible - el usuario no piensa en él
- La consistencia > Creatividad
- Menos colores, más impacto
- Los mejores diseños se sienten familiares y obvios
