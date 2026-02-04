---
name: modelado-basado-escenarios
description: Skill especializada en modelado de escenarios para Domain Storytelling, enfocada en capturar el "happy path" (80% de casos) sin excepciones, eliminando condicionales y manteniendo numeración secuencial estricta. Útil para modelado de procesos empresariales, documentación de workflows y extracción de conocimiento estructurado de narrativas del dominio.
---

# Modelado Basado en Escenarios

## Overview

Esta skill te guía en la captura y estructuración de historias de dominio enfocándote en el camino principal (happy path) sin excepciones ni variaciones. Se basa en el principio de que el 80% de los casos siguen un flujo ideal, y que documentar este flujo primero genera una base sólida para el modelado posterior.

## When to Use

Usa esta skill cuando necesites:

- **Capturar procesos empresariales** desde la perspectiva del usuario
- **Modelar workflows** sin complicar con casos excepcionales
- **Documentar flujos de trabajo** con orden cronológico claro
- **Crear historias de dominio** para desarrollo de software
- **Simplificar procesos complejos** eliminando condicionales
- **Establecer baseline** antes de documentar variaciones

## Core Capabilities

Esta skill se centra en **tres principios fundamentales**:

### 1. Foco en el "Happy Path"
**¿Qué es?** El flujo ideal que ocurre en el 80% de los casos sin excepciones
**Cómo aplicarlo:**
- Guíar al usuario a narrar primero el caso ideal
- Evitar mencionar variaciones o excepciones al inicio
- Capturar el flujo perfecto antes de las complicaciones
- Construir sobre esta base sólida

### 2. Eliminación de Condicionales
**¿Qué es?** No usar estructuras "if/else" o "gateway" en la narrativa
**Cómo aplicarlo:**
- Cuando el usuario menciona alternativas, redirigir al camino principal
- Registrar variaciones como historias separadas (anotaciones)
- Mantener cada historia lineal y sin ramas
- Un camino = una historia

### 3. Números de Secuencia
**¿Qué es?** Asignar un orden cronológico estricto a cada paso
**Cómo aplicarlo:**
- Numerar cada acción o evento secuencialmente
- Mantener orden temporal estricto (no saltos)
- Cada número = un paso en la secuencia
- Usar la numeración para validar completitud

## Instructions

Sigue este proceso paso a paso para aplicar el modelado basado en escenarios:

### Paso 1: Preparación del Contexto
1. **Pregunta inicial:** "¿Qué proceso quieres modelar?"
2. **Define el alcance:** ¿Proceso actual (As-Is) o futuro (To-Be)?
3. **Establece el nivel de detalle:** Coarse-grained (pájaro) o Fine-grained (peces)
4. **Duración estimada:** ¿Cuánto tiempo toma el proceso completo?

### Paso 2: Invitación a Narrar
1. **Frase clave:** "Cuéntame tu historia paso a paso"
2. **Instrucción:** "Empezemos por el caso ideal, el que ocurre normalmente"
3. **Recordatorio:** "No te preocupes por las excepciones ahora"
4. **Tono:** Invita a la narración, no a la explicación técnica

### Paso 3: Captura del Happy Path
1. **Escucha activa:** Deja que el usuario cuente sin interrumpir
2. **Identifica el inicio:** ¿Qué evento inicia el proceso?
3. **Identifica el final:** ¿Cuándo considera el usuario que termina?
4. **Permite pausas:** "¿Qué sucede después?" para mantener flujo
5. **Mantén enfoque:** Redirige variaciones: "Hablemos de esto después"

### Paso 4: Numeración Secuencial
1. **Por cada paso mencionado:** Asigna un número consecutivo
2. **Un solo actor por paso:** Evita múltiples actores en un mismo paso
3. **Un solo verbo por paso:** Una acción clara y específica
4. **Valida secuencia:** "¿Pasa esto antes o después de lo anterior?"
5. **Verifica orden:** Asegúrate de que la numeración refleja el tiempo

### Paso 5: Eliminación de Condicionales
1. **Cuando menciona variaciones:**
   - "Excelente, eso va en una historia separada"
   - "Anotamos eso para después"
   - "Sigamos con el camino principal primero"
2. **Redirecciona al flujo principal:**
   - "¿En el caso normal qué pasa?"
   - "¿Qué ocurre la mayoría de las veces?"
   - "Concentrémonos en el flujo típico"
3. **Registra variaciones como anotaciones:**
   - Crea una lista separada de variaciones
   - Nombra cada variación como historia independiente
   - No las ignores, solo postpone su documentación

### Paso 6: Validación del Happy Path
1. **Recapitula la historia:** Resumen paso a paso numerado
2. **Verifica completitud:** "¿Falta algún paso importante?"
3. **Confirma secuencia:** "¿El orden es correcto?"
4. **Valida fluidez:** "¿Hay saltos lógicos?"
5. **Consenso:** "¿Esto refleja el proceso ideal?"

### Paso 7: Documentación de Variaciones (Opcional)
1. **Recupera las anotaciones:** "¿Hablamos de esas variaciones ahora?"
2. **Crea historias separadas:** Cada variación = una historia nueva
3. **Mantén consistencia:** Mismo formato, numeración independiente
4. **Relaciona con principal:** "Esta variación ocurre en el paso X"

## Bundled Resources

**references/** - Ejemplos y casos de uso para modelado de escenarios
- `ejemplos-happy-path.md` - Casos reales de captura del camino ideal
- `eliminacion-condicionales.md` - Técnicas para evitar if/else en narrativas
- `numeracion-secuencial.md` - Métodos de asignación de números de secuencia
- `variaciones-anotaciones.md` - Cómo documentar excepciones y alternativas

## Examples

### Ejemplo 1: Proceso Simple - Contratación

**Usuario:** "Bueno, cuando necesitamos un empleado nuevo..."

**Tú (capturando happy path):**
"Cuéntame paso a paso cómo ocurre normalmente. Empecemos por el principio."

**Usuario:** "RRHH publica la oferta en el portal. Los candidatos envían sus CVs. El recruiter revisa los CVs y selecciona los mejores. Los convoca a entrevista. Después de la entrevista, si están bien, hacemos la oferta. El candidato firma el contrato."

**Análisis y estructuración:**
1. `RRHH publica la oferta en el portal`
2. `Los candidatos envían sus CVs`
3. `El recruiter revisa los CVs`
4. `El recruiter selecciona los mejores candidatos`
5. `El recruiter convoca a entrevista`
6. `Se realiza la entrevista`
7. `Si están bien, hacemos la oferta` ← ¡CONDICIONAL DETECTADO!

**Tú (redirigiendo):**
"Interrumpo un momento. Cuando dices 'si están bien' - en el caso normal, ¿qué ocurre? ¿Siempre hacen oferta?"

**Usuario:** "Sí, en el caso ideal siempre hacemos oferta después de una buena entrevista."

**Continuación (eliminando condicional):**
7. `Hacemos la oferta al candidato`
8. `El candidato firma el contrato`

**Historia final (happy path):**
1. `RRHH publica la oferta en el portal`
2. `Los candidatos envían sus CVs`
3. `El recruiter revisa los CVs`
4. `El recruiter selecciona los mejores candidatos`
5. `El recruiter convoca a entrevista`
6. `Se realiza la entrevista`
7. `Hacemos la oferta al candidato`
8. `El candidato firma el contrato`

**Anotación (variación):**
- `Variación A: Si el candidato no convence en entrevista → No hacemos oferta`

---

### Ejemplo 2: Proceso Complejo - Facturación

**Usuario:** "Para facturar una orden de trabajo..."

**Tú:** "Cuéntame paso a paso, empezando por el inicio del proceso."

**Usuario:** "Cuando el técnico termina la orden, genera el parte de trabajo. Luego el sistema calcula automáticamente los costes. El departamento administrativo crea la factura. Si el cliente es nuevo, necesitamos datos adicionales. El departamento envía la factura al cliente."

**Tú (detectando condicional):**
"Cuando dices 'si el cliente es nuevo' - en el caso normal, ¿el cliente ya está en el sistema?"

**Usuario:** "Sí, normalmente trabajamos con clientes existentes."

**Tú:** "Perfecto. Entonces concentremos primero en el caso normal con clientes existentes."

**Proceso normal numerado:**
1. `El técnico termina la orden`
2. `El técnico genera el parte de trabajo`
3. `El sistema calcula automáticamente los costes`
4. `El departamento administrativo crea la factura`
5. `El departamento administrativo envía la factura al cliente`

**Anotación (variación):**
- `Variación B: Cliente nuevo → Necesitamos recopilar datos adicionales antes de facturar`

---

### Ejemplo 3: Proceso con Múltiples Actores - Órdenes de Compra

**Usuario:** "El proceso de compra de materiales..."

**Tú:** "Empecemos por el inicio. ¿Quién inicia el proceso normalmente?"

**Usuario:** "El departamento de producción solicita materiales porque el stock está bajo."

**Continuando la narración:**
8. `El departamento de compras recibe la solicitud`
9. `El buyer analiza la solicitud`
10. `El buyer busca proveedores`
11. `El sistema genera cotizaciones automáticamente`
12. `El proveedor envía la cotización`
13. `El buyer compara cotizaciones`
14. `El buyer selecciona la mejor opción`
15. `El responsable de compras aprueba la orden`
16. `El sistema envía la orden al proveedor`

**Validación de secuencia:**
"Vamos a verificar el orden: ¿el buyer busca proveedores antes o después de recibir la solicitud?"

---

### Ejemplo 4: Proceso Temporal - Control de Asistencia

**Usuario:** "El control de asistencia diaria..."

**Tú:** "Cuéntame qué pasa desde que el empleado llega hasta que se registra su presencia."

**Proceso secuencial:**
1. `El empleado llega al centro de trabajo`
2. `El empleado se identifica en el sistema`
3. `El sistema registra la hora de entrada`
4. `Durante el día, el empleado registra breaks`
5. `Al finalizar, el empleado registra la salida`
6. `El sistema calcula las horas trabajadas`
7. `El sistema detecta incidencias (retrasos, salidas anticipadas)`
8. `El supervisor recibe reporte de incidencias`

**Validación temporal:**
"Cuando dices 'durante el día' - ¿el empleado puede registrarse múltiples veces? ¿En el caso normal cuántas veces?"

---

## Progressive Disclosure

Para información detallada sobre técnicas específicas:
- **Happy Path**: consulta `references/ejemplos-happy-path.md`
- **Eliminación de Condicionales**: consulta `references/eliminacion-condicionales.md`
- **Numeración Secuencial**: consulta `references/numeracion-secuencial.md`
- **Variaciones**: consulta `references/variaciones-anotaciones.md`

## Principles to Remember

### Happy Path (80% Rule)
- **El 80% de casos** siguen un flujo ideal
- **Documenta primero** este flujo principal
- **Construye sobre** esta base sólida
- **Las excepciones** van después

### Linear Stories (No Branches)
- **Una historia = un camino**
- **Sin if/else** en la narrativa principal
- **Sin gateways** o puntos de decisión
- **Variaciones = historias separadas**

### Sequential Order (Strict Timeline)
- **Cada número = un momento en el tiempo**
- **Sin saltos temporales** sin explicar
- **Orden cronológico** estricto
- **Valida secuencia** constantemente

### Actor Consistency
- **Actores aparecen una vez** por historia
- **Objetos pueden cambiar** de manos varias veces
- **Un verbo por paso** (una acción)
- **Clarity over complexity**

## Tips for Application

1. **Escucha activamente:** Deja que el usuario hable, interviene solo para clarificar secuencia
2. **Usa preguntas simples:** "¿Qué pasa después?" "¿Antes o después de esto?"
3. **Detecta patrones:** Si menciona "a veces", "normalmente", es una pista de variación
4. **Anota todo:** Lleva una lista de variaciones para después
5. **Valida constantemente:** "¿El paso X va antes o después del Y?"
6. **Sé paciente:** El usuario puede necesitar tiempo para recordar la secuencia
7. **Mantén el foco:** Redirige gentilmente hacia el camino principal

## Common Pitfalls to Avoid

❌ **Permitir condicionales en la historia principal**
- "Si pasa X, entonces Y, si no Z" → Dividir en historias separadas

❌ **Numeración no secuencial**
- Paso 5 → Paso 7 → Paso 6 → Usar orden cronológico estricto

❌ **Saltarse pasos obvios**
- Usuario dice "el sistema lo procesa automáticamente" → Pregunta qué hace exactamente

❌ **Mezclar múltiples actores en un paso**
- "RRHH y el candidato firman" → Separar en dos pasos

❌ **Ignorar variaciones**
- Cuando detecta "a veces" o "excepto cuando" → Anotar para historia separada

❌ **Perder el hilo temporal**
- Verificar constantemente el orden: "¿Esto pasa antes o después?"