---
name: gestion-alcance-scope
description: Skill especializada en gestión de alcance (scope) para Domain Storytelling, enfocada en ajustar la granularidad del modelado (coarse-grained "pájaro/cometa" vs fine-grained "mar/peces") y distinguir perspectivas temporales (As-Is proceso actual vs To-Be futuro deseado). Útil para definir el nivel apropiado de detalle según el objetivo del modelado y para gestionar expectativas entre stakeholders.
---

# Gestión de Alcance (Scope)

## Overview

Esta skill te ayuda a determinar y ajustar el nivel de granularidad apropiado para el modelado de historias de dominio, así como a gestionar las perspectivas temporales (proceso actual vs. futuro deseado). Se basa en la metáfora de la granularidad ("pájaro/cometa" vs. "mar/peces") para explicar cómo el nivel de detalle cambia según el propósito del modelado y la audiencia objetivo.

## When to Use

Usa esta skill cuando necesites:

- **Definir el nivel de detalle** apropiado para un modelado
- **Gestionar expectativas** entre stakeholders con diferentes necesidades
- **Cambiar granularidad** según la fase del proyecto
- **Distinguir proceso actual vs. futuro** deseado
- **Adaptar la historia** a diferentes audiencias
- **Evitar over-modeling** (demasiado detalle) o under-modeling (muy poco)
- **Establecer scope claro** para el modelado

## Core Capabilities

Esta skill se centra en **dos dimensiones fundamentales**:

### 1. Ajuste de Granularidad
**¿Qué es?** El nivel de detalle en el modelado, desde visión general hasta detalles específicos
**Metáforas clave:**
- **Pájaro/Cometa** - Vista desde arriba (coarse-grained)
- **Mar/Peces** - Vista bajo el agua (fine-grained)

**Cómo aplicarlo:**
- Determinar qué nivel necesita la audiencia
- Ajustar detalle según propósito del modelado
- Cambiar granularidad dinámicamente si es necesario
- Equilibrar completitud con simplicidad

### 2. Perspectiva Temporal (As-Is vs. To-Be)
**¿Qué es?** Distinguir entre el proceso actual (As-Is) y el proceso futuro deseado (To-Be)
**Cómo aplicarlo:**
- Identificar qué perspectiva quiere el stakeholder
- Clarificar objetivos del modelado (documentar vs. diseñar)
- Manejar transiciones entre perspectivas
- Gestionar expectativas sobre mejoras

## Instructions

Sigue este proceso para aplicar gestión de alcance efectivamente:

### Paso 1: Evaluación de Necesidades
1. **Pregunta por el propósito:** "¿Para qué vamos a usar este modelo?"
2. **Identifica la audiencia:** "¿Quién va a usar esta historia?"
3. **Determina el objetivo:** ¿Documentar proceso actual o diseñar uno nuevo?
4. **Clarifica el scope:** "¿Qué aspectos son más importantes?"

### Paso 2: Definición de Granularidad

#### Para Granularidad Gruesa (Coarse-Grained - Pájaro/Cometa)
**Cuándo usar:**
- Visión general para ejecutivos
- Comunicación con stakeholders no técnicos
- Planificación estratégica
- Understanding inicial del dominio

**Características:**
- Pasos amplios y resumidos
- Actores principales únicamente
- Sin detalles de implementación
- Flujo de alto nivel
- 5-10 pasos máximo

**Ejemplo:**
```
1. `Cliente solicita servicio`
2. `Comercial evalúa solicitud`
3. `Operaciones ejecuta servicio`
4. `Cliente recibe factura`
5. `Cliente paga`
```

#### Para Granularidad Fina (Fine-Grained - Mar/Peces)
**Cuándo usar:**
- Desarrollo de software
- Automatización de procesos
- Documentación técnica
- Análisis detallado de problemas

**Características:**
- Pasos específicos y detallados
- Todos los actores relevantes
- Sistemas y herramientas incluidos
- Validaciones y excepciones
- 15-50+ pasos

**Ejemplo:**
```
1. `Cliente completa formulario web`
2. `Sistema valida formato email`
3. `Sistema verifica email no existe`
4. `Comercial recibe notificación email`
5. `Comercial revisa solicitud en CRM`
6. `Comercial consulta historial cliente`
7. `Comercial evalúa viabilidad técnica`
8. `Comercial consulta disponibilidad recursos`
9. `Comercial decide aprobar/rechazar`
10. `Si aprueba: Sistema crea orden preliminar`
11. `Si aprueba: Sistema envía confirmación al cliente`
12. `Si rechaza: Sistema registra motivo`
13. `Si rechaza: Comercial llama al cliente`
...
```

### Paso 3: Identificación de Perspectiva Temporal

#### As-Is (Proceso Actual)
**Cuándo modelar:**
- Documentar cómo funciona actualmente
- Identificar problemas y pain points
- Auditoría de procesos
- Baseline para mejoras

**Enfoque:**
- Reality-based -如实描述
- Incluye workarounds y problemas
- Muestra ineficiencias
- Documenta "cómo es ahora"

**Señales del usuario:**
- "Actualmente hacemos..."
- "En el proceso actual..."
- "Lo que pasa ahora es..."
- "Nuestro proceso real..."

#### To-Be (Proceso Futuro Deseado)
**Cuándo modelar:**
- Diseñar nuevos procesos
- Planificación de mejoras
- Automatización
- Optimización

**Enfoque:**
- Ideal-based - como debería ser
- Sin problemas ni ineficiencias
- Automatizado donde posible
- Best practices

**Señales del usuario:**
- "Idealmente queremos..."
- "En el futuro我们将..."
- "Debería funcionar así..."
- "Lo que buscamos es..."

#### Híbrido (As-Is + To-Be)
**Cuándo usar:**
- Transición de estado actual a futuro
- Mostrar gap y solución
- Justificación de cambios

**Enfoque:**
- Primero As-Is (problema)
- Luego To-Be (solución)
- Comparación clara
- Justificación de cambios

### Paso 4: Comunicación de Scope

#### Al Iniciar la Sesión
**Pregunta inicial:**
"Antes de empezar, ¿queremos modelar el proceso actual (As-Is) o el proceso futuro deseado (To-Be)? ¿Y necesitamos un nivel de detalle alto (visión general) o detallado (paso a paso)?"

#### Durante la Sesión
**Si scope cambia:**
"Interrumpo un momento. Estamos modelando muy detalladamente - ¿queremos mantener este nivel o prefieres una visión más general?"

**Para clarificar perspectiva:**
"Cuando dices 'debería ser' - ¿estamos hablando de cómo funciona ahora o cómo queremos que funcione?"

### Paso 5: Gestión de Expectativas

#### Si Piden Demasiado Detalle
"Para el propósito de [objetivo], una visión general será suficiente. ¿Te parece si mantenemos los pasos a nivel de [X]?"

#### Si Piden Muy Poco Detalle
"Para poder [desarrollar/automatizar/entender], necesitamos más detalle. ¿Podemos profundizar en [área específica]?"

#### Si Mezclan As-Is y To-Be
"Estoy confundido - ¿estamos documentando el proceso actual o diseñando el futuro? ¿Hacemos primero el actual y luego el futuro?"

### Paso 6: Adaptación Dinámica

#### Cambiar Granularidad Durante Sesión
**De coarse a fine:**
"Perfecto, tenemos la visión general. Ahora, para [propósito específico], necesitamos más detalle en [área]. ¿Podemos profundizar en [X]?"

**De fine a coarse:**
"Este nivel de detalle es muy técnico. ¿Le parece si resumimos a los pasos principales para [audiencia]?"

#### Cambiar Perspectiva Temporal
"Antes de continuar con el proceso futuro, ¿podemos documentar primero cómo funciona actualmente para tener el baseline?"

## Bundled Resources

**references/** - Ejemplos y casos de uso para gestión de alcance
- `granularidad-pajaro-vs-mar.md` - Comparación detallada de niveles de granularidad
- `as-is-vs-to-be.md` - Cómo manejar perspectivas temporales
- `audiencias-y-scope.md` - Adaptar scope según audiencia
- `ejemplos-cambio-granularidad.md` - Casos de cambio dinámico de granularidad
- `gestion-expectativas.md` - Técnicas para manejar expectativas

## Examples

### Ejemplo 1: Cambio de Granularidad

#### Contexto
**Solicitud inicial:** "Queremos modelar el proceso de ventas"

**Tú (definiendo scope):**
"¿Para qué vamos a usar este modelo? ¿Es para una presentación ejecutiva o para desarrollar un sistema?"

**Usuario:** "Para presentar a la dirección"

**Tú (eligiendo coarse-grained):**
"Perfecto. Entonces modelaremos a nivel de visión general, los pasos principales."

#### Modelado Coarse-Grained (Pájaro)
```
Proceso de Ventas - Visión General

1. `Cliente Contacta Empresa`
2. `Comercial Presenta Servicios`
3. `Cliente Solicita Presupuesto`
4. `Comercial Prepara Propuesta`
5. `Cliente Evalúa Propuesta`
6. `Cliente Negocia Términos`
7. `Cliente Aprueba Propuesta`
8. `Se Formaliza Contrato`
9. `Se Ejecuta Servicio`
10. `Se Factura al Cliente`

Duración total: 2-4 semanas
Puntos críticos: Preparación propuesta y negociación
```

**Después de la presentación, nueva solicitud:**
"Excelente. Ahora necesitamos desarrollar el CRM para automatizar esto. ¿Podemos modelar más detalladamente?"

**Tú (cambiando a fine-grained):**
"Claro. Ahora necesitamos detalle técnico para el desarrollo."

#### Modelado Fine-Grained (Mar/Peces)
```
Proceso de Ventas - Detalle Técnico

1. `Cliente completa formulario contacto web`
2. `Sistema envía email automático a comercial`
3. `Comercial recibe notificación en CRM`
4. `Comercial revisa información cliente`
5. `Comercial consulta historial si cliente existente`
6. `Comercial agenda llamada con cliente`
7. `Comercial realiza llamada de discovery`
8. `Comercial identifica necesidades cliente`
9. `Comercial prepara propuesta técnica`
10. `Comercial calcula precios según tarifa`
11. `Comercial envía propuesta por email`
12. `Cliente recibe propuesta`
13. `Cliente revisa propuesta`
14. `Cliente solicita modificaciones si necesario`
15. `Comercial incorpora modificaciones`
16. `Comercial envía propuesta revisada`
17. `Cliente solicita reunión de cierre`
18. `Comercial agenda reunión`
19. `Comercial y cliente negocian términos`
20. `Cliente solicita descuento`
21. `Comercial evalúa solicitud descuento`
22. `Comercial consulta políticas descuento`
23. `Comercial decide aprobación/rechazo`
24. `Si aprobado: Cliente acepta términos`
25. `Si rechazado: Cliente evalúa alternativa`
26. `Cliente firma contrato digital`
27. `Sistema genera orden de trabajo`
28. `Operaciones recibe orden`
29. `Servicio se ejecuta`
30. `Sistema genera factura automáticamente`
31. `Factura se envía a cliente`
...
```

### Ejemplo 2: Perspectiva As-Is vs To-Be

#### Sesión As-Is (Proceso Actual con Problemas)

**Usuario:** "Queremos documentar cómo funciona ahora para identificar problemas"

**Tú (clarificando perspectiva):**
"Perfecto, documentamos el proceso actual, incluyendo problemas y workarounds."

```
Proceso de Solicitud de Vacaciones - AS-IS (Actual)

1. `Empleado quiere vacaciones`
2. `Empleado va a RRHH` (Pain point: lejos, siempre hay cola)
3. `RRHH le da formulario papel`
4. `Empleado completa formulario` (Pain point: formulario confuso, 15 campos)
5. `Empleado devuelve formulario a RRHH`
6. `RRHH verifica días disponibles` (Manual, en Excel)
7. `RRHH pasa formulario a supervisor`
8. `Supervisor revisa solicitud` (Pain point: supervisor siempre ocupado)
9. `Supervisor aprueba/rechaza`
10. `Si aprueba: RRHH actualiza calendario Excel` (Pain point: Excel se corrompe)
11. `Si aprueba: RRHH imprime confirmación`
12. `Empleado recoge confirmación` (Pain point: empleado debe ir otra vez a RRHH)
13. `RRHH archiva formulario papel` (Pain point: se pierden formularios)

Duración: 3-5 días
Problemas identificados: 6 pain points
Eficiencia: 20% tiempo real en valor agregado
```

#### Sesión To-Be (Proceso Futuro Optimizado)

**Usuario:** "Ahora queremos diseñar cómo debería funcionar"

**Tú (cambiando perspectiva):**
"Ahora diseñamos el proceso ideal, automatizado y eficiente."

```
Proceso de Solicitud de Vacaciones - TO-BE (Futuro)

1. `Empleado accede a portal self-service`
2. `Sistema muestra días disponibles automáticamente`
3. `Empleado selecciona fechas en calendario visual`
4. `Sistema valida disponibilidad en tiempo real`
5. `Sistema envía solicitud automáticamente a supervisor`
6. `Supervisor recibe notificación móvil`
7. `Supervisor aprueba con un clic`
8. `Sistema actualiza calendario automáticamente`
9. `Empleado recibe confirmación instantánea`
10. `Sistema envía recordatorios antes de vacaciones`
11. `Datos se sincronizan con nóminas automáticamente`

Duración: 2 horas
Automatización: 90%
Eficiencia: 95% tiempo real en valor agregado
```

### Ejemplo 3: Audiencia Diferente, Scope Diferente

#### Para Desarrolladores (Fine-Grained + To-Be)

**Contexto:** Modelar para desarrollo de sistema de vacaciones

**Scope:** Detallado, técnico, proceso futuro

```
Sistema de Vacaciones - Especificación Técnica

1. `Frontend: Portal empleado carga página solicitud`
2. `API: Consulta días disponibles (endpoint: GET /vacation/available)`
3. `API: Devuelve días disponibles en JSON`
4. `Frontend: Renderiza calendario interactivo`
5. `Usuario: Selecciona fechas (validate: no más 22 días)`
6. `Frontend: Calcula días seleccionados`
7. `Usuario: Hace clic en "Solicitar"`
8. `Frontend: Envía POST /vacation/request`
9. `API: Valida datos (schema validation)`
10. `API: Consulta reglas negocio (discount days, holidays)`
11. `API: Guarda solicitud en DB (table: vacation_requests)`
12. `API: Genera solicitud ID`
13. `API: Envía email a supervisor (queue: notification_queue)`
14. `Queue Worker: Procesa notificaciones`
15. `Email Service: Envía email HTML`
16. `Supervisor: Recibe email con link aprobación`
17. `Supervisor: Hace clic en link`
18. `Frontend: Carga página aprobación`
19. `API: Verifica permisos supervisor`
20. `API: Devuelve solicitud pendiente`
21. `Frontend: Muestra solicitud`
22. `Supervisor: Hace clic "Aprobar"`
23. `Frontend: Envía PUT /vacation/{id}/approve`
24. `API: Actualiza status a "APPROVED"`
25. `API: Calcula impacto en calendario`
26. `API: Actualiza tabla calendar`
27. `API: Sincroniza con sistema nóminas`
28. `API: Envía confirmación empleado`
...
```

#### Para Directivos (Coarse-Grained + As-Is + To-Be)

**Contexto:** Presentación a junta directiva sobre digitalización RRHH

**Scope:** Alto nivel, comparación actual vs. futuro, ROI

```
Digitalización RRHH - Presentación Ejecutiva

AS-IS (Actual):
1. `Empleado solicita vacaciones` → 3-5 días proceso
2. `Múltiples interacciones manuales` → 90% tiempo perdido
3. `Formularios papel` → Se pierden, ineficientes
4. `Verificación manual` → Errores frecuentes
5. `Actualización Excel` → Corrupciones, datos inconsistentes

COSTO ACTUAL:
- Tiempo RRHH: 40h/mes = €2,400/mes
- Tiempo empleados: 60h/mes = €3,600/mes
- Errores: 15% casos = €800/mes
TOTAL: €6,800/mes = €81,600/año

TO-BE (Futuro):
1. `Portal self-service` → 2 horas proceso
2. `Automatización 90%` → 95% eficiencia
3. `Validación automática` → 0% errores
4. `Integración sistemas` → Datos consistentes
5. `Notificaciones móviles` → Instantáneo

AHORRO PROYECTADO:
- Tiempo RRHH: 4h/mes = €240/mes
- Tiempo empleados: 6h/mes = €360/mes
- Errores: 0% = €0
TOTAL: €600/mes = €7,200/año

ROI: 91% reducción costo = €74,400/año ahorrados
PAYBACK: 4 meses
```

### Ejemplo 4: Manejo de Scope Durante Sesión

#### Situación: Usuario Pide Demasiado Detalle

**Usuario:** "Y entonces el empleado hace clic en el botón y... ¿qué pasa exactamente cuando hace clic?"

**Tú (gestionando expectativas):**
"Para entender el proceso general, no necesitamos entrar en tanto detalle técnico. ¿Te parece si mantenemos los pasos a nivel de 'el empleado solicita' y 'el sistema procesa'? Si luego necesitamos desarrollar el sistema, ahí sí profundizaremos."

#### Situación: Usuario Pide Muy Poco Detalle

**Usuario:** "El sistema envía la factura al cliente."

**Tú (pidiendo más detalle):**
"Para poder automatizar esto, necesitamos saber qué datos incluye la factura, cómo se genera, qué validaciones hace... ¿Podemos profundizar un poco en cómo funciona exactamente el envío?"

#### Situación: Mezclan As-Is y To-Be

**Usuario:** "El empleado solicita vacaciones, el sistema valida automáticamente, pero ahora tenemos que ir a RRHH para el papel..."

**Tú (clarificando):**
"Espera, estoy confundido. ¿Estamos hablando de cómo funciona ahora (As-Is) o cómo queremos que funcione (To-Be)? Porque mencionas 'sistema valida automáticamente' (futuro) y 'ir a RRHH' (actual). ¿Hacemos primero el proceso actual completo y luego diseñamos el futuro?"

### Ejemplo 5: Adaptación Dinámica por Audiencia

#### Fase 1: Sesión con Usuarios Finales (Fine-Grained + As-Is)

**Objetivo:** Entender proceso actual en detalle

```
Entrevista: María (Administrativa)
Scope: Detallado, proceso actual

1. `María recibe parte de trabajo del técnico`
2. `María abre sistema facturación`
3. `María busca orden por número`
4. `María verifica que orden está "completada"`
5. `María copia datos cliente a factura`
6. `María introduce horas trabajadas manualmente`
7. `María introduce materiales manualmente`
8. `María calcula descuentos (calculadora)`
9. `María calcula impuestos (tabla)`
10. `María revisa totales`
11. `María genera PDF factura`
12. `María abre Outlook`
13. `María redacta email`
14. `María adjunta PDF`
15. `María envía email`
16. `María marca orden como "facturada"`
17. `María archiva parte papel`

Tiempo promedio: 25 minutos
Puntos de error: Pasos 7, 8, 9 (cálculos manuales)
```

#### Fase 2: Sesión con Desarrolladores (Fine-Grained + To-Be)

**Objetivo:** Diseñar solución técnica

```
Workshop: Equipo Desarrollo
Scope: Detallado, proceso futuro

1. `Técnico completa orden en tablet`
2. `Tablet guarda datos localmente`
3. `Tablet sincroniza cuando hay conexión`
4. `API recibe datos orden completada`
5. `Servicios calculan costes automáticamente`
   5.1. `Consulta tarifa por tipo trabajo`
   5.2. `Suma horas trabajadas`
   5.3. `Calcula materiales + margen`
   5.4. `Aplica descuentos cliente`
   5.5. `Calcula impuestos según ubicación`
6. `Generador PDF crea factura`
7. `Email service envía factura`
8. `Sistema actualiza estado orden`
9. `Notificación a contabilidad`
10. `Sincronización con ERP`

Automatización: 95%
Tiempo estimado: 2 minutos
```

#### Fase 3: Presentación a Gerencia (Coarse-Grained + To-Be)

**Objetivo:** Mostrar beneficios

```
Presentación: Gerencia General
Scope: Visión general, futuro

1. `Técnico completa trabajo`
2. `Sistema calcula automáticamente`
3. `Cliente recibe factura al instante`
4. `Contabilidad actualiza automáticamente`

BENEFICIOS:
- Tiempo: 25 min → 2 min (92% reducción)
- Errores: 15% → 0% (eliminación)
- Satisfacción cliente: +40%
- Productividad: +300%
```

## Progressive Disclosure

Para información específica:
- **Granularidad**: consulta `references/granularidad-pajaro-vs-mar.md`
- **Perspectivas**: consulta `references/as-is-vs-to-be.md`
- **Audiencias**: consulta `references/audiencias-y-scope.md`
- **Cambios**: consulta `references/ejemplos-cambio-granularidad.md`
- **Expectativas**: consulta `references/gestion-expectativas.md`

## Metáforas Clave

### Granularidad

#### Vista de Pájaro/Cometa (Coarse-Grained)
- **Perspectiva:** Desde arriba, vista general
- **Qué ves:** Flujo principal, pasos amplios
- **Qué NO ves:** Detalles, excepciones, sistemas específicos
- **Analogía:** Como ver un río desde un avión - ves el curso general, no las piedras del fondo
- **Uso típico:** Presentaciones, planificación, comunicación ejecutiva

#### Vista de Mar/Peces (Fine-Grained)
- **Perspectiva:** Bajo el agua, detalle granular
- **Qué ves:** Cada paso, cada actor, cada validación
- **Qué NO ves:** Solo lo general, el "por qué"
- **Analogía:** Como nadar en el río - ves cada piedra, corriente, pez
- **Uso típico:** Desarrollo, automatización, documentación técnica

### Perspectiva Temporal

#### As-Is (Proceso Actual)
- **Analogía:** Fotografía del momento actual
- **Enfoque:**如实描述, incluyendo imperfecciones
- **Uso:** Baseline, identificación de problemas

#### To-Be (Proceso Futuro)
- **Analogía:** Boceto de lo que queremos construir
- **Enfoque:** Ideal, optimizado, automatizado
- **Uso:** Diseño, planificación, visión

## Principios de Scope Management

### 1. Propósito Determina Granularidad
- **Desarrollo** → Fine-grained
- **Comunicación** → Coarse-grained
- **Análisis** → Fine-grained (As-Is)
- **Planificación** → Coarse-grained (To-Be)

### 2. Audiencia Determina Perspectiva
- **Usuarios finales** → As-Is detallado
- **Desarrolladores** → To-Be detallado
- **Ejecutivos** → As-Is + To-Be (comparación)
- **Stakeholders** → Según objetivo

### 3. Fase del Proyecto
- **Descubrimiento** → As-Is coarse
- **Análisis** → As-Is fine
- **Diseño** → To-Be coarse
- **Desarrollo** → To-Be fine
- **Implementación** → To-Be fine
- **Validación** → As-Is vs To-Be

### 4. Cambio es Normal
- Scope puede cambiar durante sesión
- Es mejor adaptar que forzar
- Comunicar cambios claramente
- Validar nuevo scope

## Tips for Application

### Para Definir Scope Inicial

1. **Pregunta directa:** "¿Para qué vamos a usar esto?"
2. **Identifica audiencia:** "¿Quién lo va a leer/usar?"
3. **Clarifica nivel:** "¿Visión general o detalle paso a paso?"
4. **Confirma perspectiva:** "¿Proceso actual o futuro deseado?"

### Para Mantener Scope

1. **Señales de over-scope:** Demasiados detalles técnicos, pasos micro
2. **Señales de under-scope:** Pasos muy amplios, preguntas sobre implementación
3. **Ajusta dinámicamente:** "Para [propósito], ¿necesitamos más o menos detalle?"
4. **Documenta decisiones:** "Modelamos a nivel [X] porque [razón]"

### Para Cambiar Scope

1. **Comunica el cambio:** "Cambiamos de visión general a detalle porque..."
2. **Justifica la decisión:** "Para [objetivo], necesitamos [nivel] granularidad"
3. **Valida con usuario:** "¿Te parece bien este nivel de detalle?"
4. **Ofrece alternativas:** "Podemos hacer [opción A] u [opción B]"

## Common Pitfalls to Avoid

❌ **No definir scope al inicio**
- Asumir que "todos saben" el nivel necesario
- No preguntar propósito u audiencia

❌ **Scope creep durante sesión**
- Agregar detalles sin preguntar
- No mantener foco en objetivo

❌ **Mezclar granularidades**
- Algunos pasos muy detallados, otros muy amplios
- Inconsistencia confunde

❌ **Confundir As-Is y To-Be**
- Mezclar proceso actual con deseado
- No clarificar perspectiva

❌ **No adaptar a audiencia**
- Mismo nivel para todos
- No considerar conocimientos técnicos

❌ **Ser inflexible al cambio**
- No adaptar cuando scope cambia
- Forzar scope inapropiado

❌ **Over-engineering**
- Demasiado detalle innecesario
- Modelar lo obvio

❌ **Under-engineering**
- Muy poco detalle para el propósito
- Saltar pasos importantes

**Recuerda:** El scope correcto es el que sirve al propósito. Ni más ni menos. Es mejor tener el nivel apropiado que tener "todo". Pregunta, clarifica, adapta.
