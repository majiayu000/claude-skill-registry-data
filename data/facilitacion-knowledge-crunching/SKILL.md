---
name: facilitacion-knowledge-crunching
description: Skill especializada en facilitación y knowledge crunching para Domain Storytelling, enfocada en detectar huecos lógicos en narrativas (plot holes), usar anotaciones para registrar variaciones sin complicar el diagrama principal, e identificar pain points donde los expertos mencionan problemas o ineficiencias. Útil para refinar historias de dominio, asegurar completitud lógica y capturar problemas del proceso actual.
---

# Facilitación y Knowledge Crunching

## Overview

Esta skill te ayuda a refinar y completar historias de dominio mediante la detección proactiva de inconsistencias lógicas, el registro sistemático de variaciones, y la identificación de problemas en los procesos actuales. Se basa en técnicas de facilitación para extraer conocimiento completo del experto del dominio mientras mantienes la narrativa principal clara y enfocada.

## When to Use

Usa esta skill cuando necesites:

- **Refinar historias** y asegurar completitud lógica
- **Detectar inconsistencias** en flujos de proceso
- **Registrar variaciones** sin complicar la narrativa principal
- **Identificar problemas** en procesos actuales (pain points)
- **Validar coherencia** de historias complejas
- **Facilitar sesiones** de Domain Storytelling efectivas
- **Crunch knowledge** (extraer conocimiento oculto) del experto

## Core Capabilities

Esta skill se centra en **tres capacidades fundamentales**:

### 1. Detección de "Plot Holes" (Huecos de la Trama)
**¿Qué son?** Saltos lógicos donde la historia omite pasos importantes o conexiones
**Cómo detectarlos:**
- Escuchar qué falta entre pasos consecutivos
- Preguntar "¿Cómo pasa de X a Y?"
- Identificar acciones implícitas no mencionadas
- Verificar causalidad entre eventos

### 2. Uso de Anotaciones
**¿Qué son?** Notas registradas aparte para capturar información sin complicar el diagrama
**Cómo aplicarlas:**
- Registrar variaciones, errores, asunciones
- Mantener narrativa principal limpia
- Clasificar anotaciones por tipo
- Usar sistema de referencias cruzadas

### 3. Identificación de "Pain Points"
**¿Qué son?** Pasos donde el experto menciona problemas, ineficiencias o frustraciones
**Cómo identificarlos:**
- Escuchar quejas, sighs, "esto es problemático"
- Marcar pasos con "normalmente...", "típicamente..."
- Detectar workarounds o soluciones temporales
- Identificar puntos de fricción del usuario

## Instructions

Sigue este proceso para aplicar facilitación y knowledge crunching:

### Paso 1: Facilitación Activa
1. **Escucha activa:** Enfócate en palabras clave de problemas
2. **Preguntas clarificadoras:** "¿Cómo exactamente...?"
3. **Observa lenguaje corporal:** sighs, pausas, expresiones de frustración
4. **Mantén ambiente seguro:** "Esto es normal", "Entiendo el problema"
5. **No soluciones aún:** Solo registra, no propongas soluciones

### Paso 2: Detección de Plot Holes
1. **Escucha la secuencia completa** sin interrumpir
2. **Identifica saltos lógicos** entre pasos
3. **Formula preguntas de conexión:**
   - "¿Cómo pasa exactamente de X a Y?"
   - "¿Qué sucede entre estos dos pasos?"
   - "¿Quién hace [acción implícita]?"
4. **Documenta el gap** como pregunta o anotación
5. **No llenes con asunciones** - pregunta al experto

### Paso 3: Registro Sistemático de Anotaciones
1. **Crea lista de anotaciones** separada de la historia principal
2. **Clasifica por tipo:**
   - **V:** Variación de flujo
   - **E:** Error/Excepción
   - **A:** Asunción
   - **P:** Pain point
   - **Q:** Pregunta/Gap
   - **I:** Información adicional
3. **Referencia el contexto:** "¿En qué paso aparece?"
4. **Usa formato consistente:** `[TIPO] Título - Contexto - Descripción`

### Paso 4: Identificación de Pain Points
1. **Escucha indicadores verbales:**
   - "Esto es un problema..."
   - "Aquí siempre se atasca..."
   - "Normalmente tardamos mucho..."
   - "Esta parte es muy tediosa..."
2. **Observa indicadores emocionales:**
   - Sighs, pausas largas
   - Cambios de tono
   - Lenguaje de frustración
3. **Marca el paso:** Nota el número donde ocurre
4. **Profundiza:** "¿Qué hace esto difícil?"
5. **Registra impacto:** "¿Cuánto tiempo se pierde?"

### Paso 5: Knowledge Crunching (Extracción de Conocimiento)
1. **Asunciones implícitas:** "¿Por qué asumimos que...?"
2. **Conocimiento tácito:** "Cuéntame más sobre cómo funciona esto internamente"
3. **Reglas no documentadas:** "¿Hay alguna regla que no hemos mencionado?"
4. **Excepciones importantes:** "¿Qué pasa cuando esto no funciona como esperamos?"
5. **Contextualización:** "¿Por qué hacemos esto de esta manera?"

### Paso 6: Validación y Clarificación
1. **Repite la historia** con las correcciones
2. **Verifica que los gaps estén llenos**
3. **Confirma que las anotaciones están completas**
4. **Valida que los pain points estén marcados**
5. **Consenso:** "¿Esto refleja exactamente lo que ocurre?"

## Bundled Resources

**references/** - Ejemplos y casos de uso para facilitación y knowledge crunching
- `deteccion-plot-holes.md` - Casos reales de identificación de gaps lógicos
- `sistema-anotaciones.md` - Metodología para registro sistemático
- `identificacion-pain-points.md` - Técnicas para detectar problemas
- `knowledge-crunching.md` - Métodos para extraer conocimiento tácito
- `ejemplos-facilitacion.md` - Sesiones completas de facilitación

## Examples

### Ejemplo 1: Detección de Plot Hole

**Historia original del usuario:**
"El empleado solicita vacaciones. El supervisor aprueba. El empleado se va de vacaciones."

**Tú (detectando plot hole):**
"Interrumpo un momento. Cuando el supervisor aprueba - ¿cómo se entera el empleado? ¿Recibe un email? ¿Ve una notificación?"

**Usuario:** "Ah, sí, el sistema le envía un email automático."

**Tú:** "Perfecto. Lo anoto y completamos la historia."

**Historia corregida:**
1. `El empleado solicita vacaciones`
2. `El supervisor aprueba la solicitud`
3. `El sistema envía email de aprobación al empleado`
4. `El empleado recibe la notificación`
5. `El empleado disfruta las vacaciones`

**Anotación:**
- `[Q] Gap detectado - Comunicación de aprobación: Paso 3 faltante`

---

### Ejemplo 2: Uso de Anotaciones

**Historia principal (Happy Path):**
1. `El cliente solicita presupuesto`
2. `El vendedor prepara propuesta`
3. `El vendedor envía presupuesto`
4. `El cliente aprueba presupuesto`
5. `El vendedor cierra la venta`

**Anotaciones registradas en paralelo:**
```
[V1] Cliente premium (20% casos)
Contexto: Paso 2 (preparar propuesta)
Descripción: Aplica descuento automático del 15%

[E1] Cliente rechaza precio (30% casos)
Contexto: Paso 4 (aprobar presupuesto)
Descripción: Solicita descuento adicional

[P1] Pain point identificado
Contexto: Paso 2 (preparar propuesta)
Descripción: "Normalmente tardamos 2-3 días en preparar propuesta porque hay que consultar precios manualmente"

[A1] Asunción crítica
Contexto: General
Descripción: Asumimos que siempre hay stock disponible

[I1] Información adicional
Contexto: Paso 3 (enviar presupuesto)
Descripción: El email incluye PDF + enlace a portal web para tracking
```

---

### Ejemplo 3: Identificación de Pain Point

**Usuario narrando:**
"Y entonces el empleado tiene que ir a RRHH para que le impriman el certificado. Pero siempre está la impresora rota o sin papel. A veces esperamos 20 minutos..."

**Tú (identificando pain point):**
"Pausa aquí. Esto suena como un problema recurrente. ¿Con qué frecuencia pasa esto?"

**Usuario:** "Casi siempre. Es muy frustrante."

**Tú:** "Entiendo. Lo marco como pain point."

**Historia principal (sin complicar):**
1. `El empleado necesita certificado`
2. `El empleado va a RRHH`
3. `RRHH imprime certificado`
4. `El empleado recibe certificado`

**Anotación de pain point:**
```
[P1] Pain point: Impresora de RRHH
Contexto: Paso 3 (imprimir certificado)
Frecuencia: 90% de casos
Problema: Impresora rota/sin papel
Tiempo perdido: 15-20 minutos promedio
Impacto: Alto - afecta satisfacción empleado
Solución actual: Workaround manual - imprimir desde otra oficina
```

---

### Ejemplo 4: Knowledge Crunching Completo

**Usuario:** "Y entonces el sistema envía la orden al proveedor."

**Tú (knowledge crunching):**
"¿Cómo exactamente envía la orden? ¿Se genera un PDF? ¿Se envía por email? ¿Se sube a un portal?"

**Usuario:** "Se genera un PDF y se envía por email al proveedor. Pero algunos proveedores prefieren el portal, entonces tenemos que subirlo manualmente..."

**Tú:** "Interesante. ¿Cuántos proveedores prefieren portal?"

**Usuario:** "Unos 30%. Y a veces el email va a spam..."

**Historia principal:**
1. `El sistema genera orden de compra`
2. `El sistema envía email al proveedor`
3. `El proveedor recibe la orden`

**Anotaciones de knowledge crunching:**
```
[I1] Conocimiento tácito: Métodos de envío
Contexto: Paso 2 (enviar orden)
Detalles:
- 70% proveedores: Email con PDF
- 30% proveedores: Portal web (manual)
- Problema: Emails van a spam (frecuencia desconocida)

[A1] Asunción identificada
Descripción: Asumimos que email funciona siempre
Realidad: No siempre llega

[Q] Pregunta abierta
¿Cómo detectamos si el proveedor recibió la orden?
```

---

### Ejemplo 5: Sesión de Facilitación Completa

**Contexto:** Modelando proceso de facturación

**Usuario:** "Cuando la orden se completa, el técnico genera el parte. Luego el administrativo crea la factura. El cliente paga."

**Tú (facilitación activa):**
"Cuéntame paso a paso. Empecemos desde el principio."

**Usuario:** "El técnico completa la orden. Genera el parte en el tablet. Luego va al sistema de oficina, busca la orden, copia los datos a la factura... Es un rollo, siempre nos equivocamos en los números."

**Tú (detectando pain point + plot hole):**
"Dos cosas aquí. Primero, ese copiar datos entre sistemas suena problemático. ¿Con qué frecuencia se equivocan? Segundo, ¿cómo va exactamente del tablet al sistema de oficina?"

**Usuario:** "Se equivocan como 30% de las veces. Y tienen que transcribir manualmente... Ah, y a veces el tablet no sincroniza bien, entonces los datos están desactualizados."

**Historia principal refinada:**
1. `El técnico completa la orden en el tablet`
2. `El técnico genera el parte de trabajo`
3. `El técnico sincroniza datos con sistema de oficina`
4. `El administrativo consulta la orden en el sistema`
5. `El administrativo crea la factura`
6. `El administrativo envía la factura al cliente`
7. `El cliente recibe y paga la factura`

**Anotaciones:**
```
[P1] Pain point: Transcripción manual
Contexto: Pasos 3-5 (sincronización y creación)
Frecuencia: 30% error rate
Problema: Copiar datos manualmente entre sistemas
Tiempo perdido: 10-15 minutos por factura
Impacto: Alto - errores de cálculo

[P2] Pain point: Sincronización tablet
Contexto: Paso 3 (sincronización)
Problema: Tablet no sincroniza automáticamente
Workaround: Sincronización manual
Frecuencia: Desconocida

[V1] Variación: Facturas complejas
Contexto: Paso 5 (crear factura)
Descripción: Facturas con múltiples órdenes requieren proceso especial
```

---

## Progressive Disclosure

Para técnicas específicas:
- **Plot Holes**: consulta `references/deteccion-plot-holes.md`
- **Anotaciones**: consulta `references/sistema-anotaciones.md`
- **Pain Points**: consulta `references/identificacion-pain-points.md`
- **Knowledge Crunching**: consulta `references/knowledge-crunching.md`
- **Facilitación**: consulta `references/ejemplos-facilitacion.md`

## Principles of Facilitation

### Escucha Activa
- **Atención completa** al experto del dominio
- **Preguntas abiertas** para profundizar
- **No asumir** - siempre clarificar
- **Validar entendimiento** constantemente

### Knowledge Crunching
- **Extracción de conocimiento tácito** (lo que saben pero no dicen)
- **Identificación de asunciones** (lo que "todos saben")
- **Reglas no documentadas** (políticas no escritas)
- **Excepciones importantes** (lo que rompe la norma)

### Registro Sistemático
- **Anotaciones como respaldo**, no protagonista
- **Clasificación consistente** de notas
- **Referencias cruzadas** a la historia principal
- **Formato estandarizado** para facilitar revisión

## Techniques for Knowledge Crunching

### 1. Técnica del "Por Qué"
**Proceso:** Pregunta "por qué" varias veces hasta llegar a la causa raíz

**Ejemplo:**
- Tú: "¿Por qué copian los datos manualmente?"
- Usuario: "Porque el tablet no se integra con el sistema de facturación"
- Tú: "¿Por qué no se integra?"
- Usuario: "Porque fueron sistemas comprados por separado"
- Tú: "¿Por qué no se integraron en su momento?"
- Usuario: "Porque当时 no había presupuesto para integración"

### 2. Técnica del "Cuéntame más"
**Proceso:** Solicita detalles sobre procesos "automáticos"

**Ejemplo:**
- Usuario: "Y entonces el sistema calcula automáticamente el precio"
- Tú: "Cuéntame más sobre cómo calcula automáticamente"
- Usuario: "Bueno, coge la tarifa base, aplica descuentos, suma impuestos..."
- Tú: "¿Y cómo sabe qué descuentos aplicar?"
- Usuario: "Ah, aquí es donde se complica..."

### 3. Técnica de "Scenario Mining"
**Proceso:** Explora casos extremos para entender límites

**Ejemplo:**
- Tú: "¿Qué pasa si el cliente es de otro país?"
- Usuario: "Ah, entonces no aplica el descuento local"
- Tú: "¿Qué más cambia?"
- Usuario: "También cambian los impuestos y el plazo de pago..."

### 4. Técnica de "Workaround Detection"
**Proceso:** Identifica soluciones temporales que se volvieron permanentes

**Ejemplo:**
- Tú: "¿Y cómo manejan cuando el sistema está caído?"
- Usuario: "Ah, usamos la hoja de cálculo de emergencia"
- Tú: "¿Con qué frecuencia pasa esto?"
- Usuario: "Unas 3 veces al mes..."
- Tú: "¿Y la hoja de cálculo funciona bien?"
- Usuario: "Mejor que el sistema, la verdad..."

## Indicators of Pain Points

### Verbal Indicators
- **"Esto es problemático..."**
- **"Aquí siempre se atasca..."**
- **"Normalmente tardamos mucho..."**
- **"Es muy tedioso..."**
- **"Aquí perdemos mucho tiempo..."**
- **"Esto es un rollo..."**
- **"A veces no funciona..."**
- **"Es frustrante..."**

### Temporal Indicators
- **Pausas largas** al mencionar un paso
- **Cambios de ritmo** - acelera o ralentiza
- **Repetición** del mismo punto
- **Vuelta atrás** en la narrativa

### Emotional Indicators
- **Sighs (suspiros)**
- **Cambios de tono** (más serio, más lento)
- **Lenguaje corporal** (cruzarse de brazos, mirar lejos)
- **Frustración evidente** en la voz

### Behavioral Indicators
- **Workarounds** - "Lo que hacemos es..."
- **Soluciones temporales** - "Por ahora hacemos..."
- **Dependencia de personas específicas** - "Solo X sabe cómo..."
- **Documentación informal** - "Tenemos una hoja de..."

## Common Plot Holes to Detect

### 1. Comunicación Implícita
**Gap:** Un actor se entera de algo sin que se explique cómo

**Ejemplo:**
```
1. "El supervisor aprueba vacaciones"
2. "El empleado disfruta vacaciones" ❌ (falta: ¿cómo se entera?)
```

**Pregunta de detección:**
"¿Cómo se entera [actor] de [evento]?"

### 2. Validaciones Ocultas
**Gap:** Se asume que algo es válido sin verificar

**Ejemplo:**
```
1. "El cliente envía datos"
2. "El sistema procesa datos" ❌ (falta: ¿se validan?)
```

**Pregunta de detección:**
"¿Cómo sabemos que [cosa] es correcta/válida?"

### 3. Transiciones de Estado
**Gap:** Un objeto cambia de estado sin acción

**Ejemplo:**
```
1. "El empleado solicita vacaciones"
2. "El empleado está de vacaciones" ❌ (falta: aprobación)
```

**Pregunta de detección:**
"¿Qué pasa entre [estado A] y [estado B]?"

### 4. Sistemas Intermedios
**Gap:** Se usa un sistema sin explicar la transición

**Ejemplo:**
```
1. "El técnico completa en el tablet"
2. "El administrativo ve los datos" ❌ (falta: sincronización)
```

**Pregunta de detección:**
"¿Cómo viajan los datos de [sistema A] a [sistema B]?"

### 5. Información Faltante
**Gap:** Se actúa con información que no se mencionó

**Ejemplo:**
```
1. "El cliente solicita servicio"
2. "El vendedor prepara presupuesto" ❌ (falta: ¿qué información tiene?)
```

**Pregunta de detección:**
"¿Con qué información cuenta [actor] para hacer [acción]?"

## Best Practices

### Para Facilitación
1. **Mantén neutralidad** - no juzgues el proceso actual
2. **Sé curioso, no crítico** - "Interesante, cuéntame más..."
3. **Deja que el experto hable** - tú preguntas, ellos responden
4. **Valida, no asumas** - "¿Esto significa que...?"
5. **Documenta todo** - mejor sobre-documentar que perder información

### Para Knowledge Crunching
1. **Ve más allá de lo obvio** - pregunta "¿y luego qué?"
2. **Explora excepciones** - "¿Qué pasa cuando NO funciona así?"
3. **Identifica dependencias** - "¿Esto depende de que haya pasado X?"
4. **Encuentra reglas no escritas** - "¿Hay alguna regla que...?"
5. **Entiende el "por qué"** - no solo el "cómo"

### Para Detección de Plot Holes
1. **Escucha gaps** - "¿Y entonces qué pasa?"
2. **Verifica causalidad** - "¿X causa Y?"
3. **Pregunta por transiciones** - "¿Cómo va de A a B?"
4. **Identifica información faltante** - "¿Cómo sabe X que Y?"
5. **No llenes con asunciones** - deja que el experto complete

### Para Pain Points
1. **Escucha quejas** - "Aquí siempre..."
2. **No soluciones aún** - solo documenta
3. **Profundiza en el impacto** - "¿Cuánto tiempo se pierde?"
4. **Identifica workarounds** - "¿Cómo lo resuelven ahora?"
5. **Mide frecuencia** - "¿Con qué frecuencia pasa?"

## Tips for Application

1. **Paciencia es clave** - El knowledge crunching toma tiempo
2. **Preguntas abiertas** - Evitar sí/no, preferir "¿cómo...?"
3. **Silencio es útil** - Deja que el usuario piense
4. **Repite para validar** - "Lo que entiendo es..."
5. **Visualiza las anotaciones** - Usa listas o tablas
6. **Clasifica en tiempo real** - Marca [V], [P], [E] mientras escuchas
7. **No interrumpas el flujo** - Anota preguntas para después
8. **Usa ejemplos concretos** - "Dame un ejemplo específico"

## Common Pitfalls to Avoid

❌ **Saltar a soluciones**
- Usuario: "Aquí siempre se atasca"
- Tú: "¿Han pensado en automatizarlo?" ❌
- Tú: "¿Con qué frecuencia pasa esto?" ✅

❌ **Asumir conocimiento**
- Usuario: "Y entonces lo procesamos normalmente"
- Tú: "¿Qué significa 'normalmente'?" ✅
- Tú: "Ya entiendo" ❌

❌ **Perder las anotaciones**
- Documentar solo la historia principal
- No clasificar las anotaciones
- Mezclar anotaciones con historia principal

❌ **No profundizar**
- Quedarse en la superficie
- No preguntar "¿y luego qué?"
- Aceptar "automáticamente" sin entender cómo

❌ **Juzgar el proceso actual**
- "Eso es ineficiente"
- "Nosotros lo haríamos mejor"
- "Eso no puede ser normal"

❌ **Permitir generalidades**
- "Siempre", "nunca", "normalmente"
- Sin frecuencia específica
- Sin ejemplos concretos

**Recuerda:** Tu rol es facilitar la extracción de conocimiento, no juzgarlo. Captura todo, clasifica sistemáticamente, y mantén la historia principal limpia. Las anotaciones son tu herramienta más poderosa.
