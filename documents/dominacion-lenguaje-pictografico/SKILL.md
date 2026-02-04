---
name: dominacion-lenguaje-pictografico
description: Skill especializada en análisis de lenguaje pictográfico para identificar actores (personas/sistemas activos), objetos de trabajo (documentos/información/cosas físicas), actividades (verbos) y estructurar información usando el formato Sujeto -> Predicado -> Objeto. Útil para análisis de procesos empresariales, documentación de workflows, extracción de conocimiento estructurado de textos y modelado de procesos de negocio.
---

# Dominio del Lenguaje Pictográfico

## Overview

Esta skill te ayuda a analizar y estructurar información textual aplicando principios del lenguaje pictográfico para identificar elementos clave en procesos empresariales y workflows. Permite extraer conocimiento estructurado de descripciones de procesos, documentos o requerimientos.

## When to Use

Usa esta skill cuando necesites:

- **Análisis de Procesos**: Convertir descripciones de procesos empresariales en estructura formal
- **Documentación de Workflows**: Crear documentación clara de flujos de trabajo
- **Extracción de Conocimiento**: Identificar actores, objetos y actividades en documentos
- **Modelado de Procesos**: Transformar texto descriptivo en elementos estructurados
- **Análisis de Requerimientos**: Desglosar requerimientos en componentes fundamentales
- **Auditoría de Procesos**: Revisar y estructurar procesos existentes

## Core Capabilities

Esta skill se centra en **cuatro componentes fundamentales**:

### 1. Identificación de Actores
**¿Qué son?** Personas, roles, departamentos o sistemas que ejecutan acciones
**Cómo identificarlos:**
- Buscar sustantivos que representan entidades activas
- Identificar quien "hace", "ejecuta", "gestiona", "procesa"
- Considerar: empleados, roles (vendedor, analista), sistemas (ERP, CRM), departamentos

### 2. Identificación de Objetos de Trabajo
**¿Qué son?** Documentos, información, datos o cosas físicas sobre las que se trabaja
**Cómo identificarlos:**
- Buscar sustantivos que reciben acción
- Identificar qué se "procesa", "crea", "modifica", "almacena"
- Considerar: órdenes, facturas, empleados, productos, datos, informes

### 3. Definición de Actividades
**¿Qué son?** Los verbos que conectan actores con objetos de trabajo
**Cómo identificarlos:**
- Buscar verbos de acción entre actores y objetos
- Identificar el "qué se hace" con el objeto
- Considerar: crear, procesar, validar, aprobar, enviar, almacenar

### 4. Estructura Gramatical
**Formato estándar:** `Sujeto (Actor) → Predicado (Actividad) → Objeto (Objeto de Trabajo)`

### 5. Visualización con Iconos (Opcional)
**¿Qué son?** Iconos SVG para representar visualmente actores y objetos de trabajo
**Cómo usarlos:**
- Aplica iconos a actores para mayor claridad visual
- Usa iconos en objetos de trabajo para identificación rápida
- Mantén consistencia en el uso a lo largo de toda la presentación

**Archivos SVG Disponibles:**

Los iconos están disponibles como archivos SVG en el directorio `assets/`:
- **Actores:** `assets/actores/person.svg`, `assets/actores/group.svg`, `assets/actores/system.svg`
- **Objetos:** `assets/objetos/document.svg`, `assets/objetos/folder.svg`, `assets/objetos/call.svg`, `assets/objetos/email.svg`, `assets/objetos/form.svg`, `assets/objetos/database.svg`, `assets/objetos/report.svg`, `assets/objetos/money.svg`, `assets/objetos/cart.svg`, `assets/objetos/calendar.svg`

**Iconos de Actores:**
- **Person** 👤 - Persona individual (empleado, cliente, técnico)
- **Group** 👥 - Grupo o equipo (departamento, comité)
- **System** 💻 - Sistema automatizado (ERP, CRM, software)

**Iconos de Objetos de Trabajo:**
- **Document** 📄 - Documentos (facturas, contratos, informes)
- **Folder** 📁 - Archivos/carpetas (expedientes, carpetas de proyecto)
- **Call** 📞 - Comunicaciones (llamadas, emails, mensajes)
- **Email** ✉️ - Emails y notificaciones
- **Form** 📝 - Formularios y solicitudes
- **Database** 🗄️ - Bases de datos y registros
- **Report** 📊 - Reportes y análisis
- **Money** 💰 - Transacciones financieras
- **Cart** 🛒 - Pedidos y compras
- **Calendar** 📅 - Eventos y programación

**Ejemplo con iconos:**
```html
<!-- Con archivos SVG -->
<img src="assets/actores/person.svg" width="20"> Empleado → ✅ Valida → 📄 Documento
<img src="assets/actores/system.svg" width="20"> Sistema → 🔄 Procesa → 📝 Formulario

<!-- O solo con emojis (equivalentes visuales) -->
👤 Empleado → ✅ Valida → 📄 Documento
💻 Sistema → 🔄 Procesa → 📝 Formulario
```

📖 **Documentación completa:** Ver `referencias/iconos-visualizacion.md` y `assets/README.md` para guías detalladas.

Sigue este proceso paso a paso para aplicar el análisis de lenguaje pictográfico:

### Paso 1: Análisis Inicial
1. Lee el texto o documento completo
2. Identifica el contexto general del proceso
3. Subraya o marca elementos relevantes

### Paso 2: Identificación de Actores
1. Busca todas las personas, roles, departamentos o sistemas mencionados
2. Lista cada actor identificado
3. Verifica que sean entidades "activas" (que hacen algo)
4. **Ejemplo:** "El departamento de RRHH", "El sistema ERP", "El supervisor"

### Paso 3: Identificación de Objetos de Trabajo
1. Busca todos los sustantivos que representan documentos, información o cosas
2. Lista cada objeto de trabajo
3. Verifica que sean elementos sobre los que se "trabaja"
4. **Ejemplo:** "órdenes de trabajo", "facturas", "datos de empleados", "informes"

### Paso 4: Definición de Actividades
1. Identifica los verbos que conectan actores con objetos
2. Para cada actor-objeto, determina qué actividad los une
3. Usa verbos específicos y claros
4. **Ejemplo:** "validar", "aprobar", "procesar", "generar", "enviar"

### Paso 5: Estructuración Final
1. Aplica el formato: `Actor → Actividad → Objeto`
2. Verifica que cada tripletas tenga sentido completo
3. Revisa la coherencia del conjunto
4. Elimina redundancias

### Paso 6: Validación
1. ¿Cada actor puede realizar la actividad?
2. ¿Cada actividad es apropiada para el objeto?
3. ¿La estructura cubre todo el proceso descrito?
4. ¿Hay elementos faltantes o adicionales?

## Bundled Resources

**references/** - Ejemplos y casos de uso para análisis pictográfico
- `ejemplos-procesos-empresariales.md` - Casos reales de análisis de procesos
- `plantillas-tripletas.md` - Plantillas para estructurar información
- `casos-uso-rrhh.md` - Ejemplos específicos del dominio RRHH
- `casos-uso-ordenes.md` - Ejemplos específicos de órdenes de trabajo

## Examples

### Ejemplo 1: Proceso Simple
**Texto original:**
"El empleado completa la orden de trabajo y la envía al supervisor para validación. El supervisor revisa la orden y la aprueba si está correcta."

**Análisis:**
- **Actores:** empleado, supervisor
- **Objetos de trabajo:** orden de trabajo
- **Actividades:** completar, enviar, validar, revisar, aprobar

**Estructura:**
1. `empleado → completa → orden de trabajo`
2. `empleado → envía → orden de trabajo`
3. `supervisor ← recibe ← orden de trabajo` (implícito)
4. `supervisor → revisa → orden de trabajo`
5. `supervisor → aprueba → orden de trabajo`

### Ejemplo 2: Proceso Empresarial Complejo
**Texto:**
"El departamento de compras genera una orden de pedido basada en la solicitud del departamento de producción. El sistema ERP valida la disponibilidad de stock. El responsable de compras revisa y aprueba la orden. El proveedor recibe la orden y prepara el envío."

**Análisis:**
- **Actores:** departamento de compras, departamento de producción, sistema ERP, responsable de compras, proveedor
- **Objetos de trabajo:** orden de pedido, solicitud, stock, envío
- **Actividades:** generar, basar, validar, revisar, aprobar, recibir, preparar

**Estructura:**
1. `departamento de producción → genera → solicitud`
2. `departamento de compras ← recibe ← solicitud`
3. `departamento de compras → genera → orden de pedido`
4. `sistema ERP → valida → stock`
5. `responsable de compras → revisa → orden de pedido`
6. `responsable de compras → aprueba → orden de pedido`
7. `proveedor ← recibe ← orden de pedido`
8. `proveedor → prepara → envío`

### Ejemplo 3: Sistema Automatizado
**Texto:**
"El sistema CRM registra automáticamente los datos del cliente cuando se completa el formulario web. El sistema envía un email de bienvenida al cliente. El agente de ventas revisa el lead y programa una cita."

**Análisis:**
- **Actores:** sistema CRM, sistema, agente de ventas, cliente
- **Objetos de trabajo:** datos del cliente, formulario web, email de bienvenida, lead, cita
- **Actividades:** registrar, completar, enviar, revisar, programar

**Estructura:**
1. `cliente → completa → formulario web`
2. `sistema CRM → registra → datos del cliente`
3. `sistema → envía → email de bienvenida`
4. `sistema → envía → email de bienvenida a cliente` (derivado)
5. `agente de ventas → revisa → lead`
6. `agente de ventas → programa → cita`

## Progressive Disclosure

Para información detallada sobre ejemplos específicos por dominio:
- **RRHH**: consulta `references/casos-uso-rrhh.md`
- **Órdenes de Trabajo**: consulta `references/casos-uso-ordenes.md`
- **Plantillas**: consulta `references/plantillas-tripletas.md`
- **Procesos Empresariales**: consulta `references/ejemplos-procesos-empresariales.md`

## Tips para el Análisis

1. **Sé específico:** Usa nombres precisos para actores y objetos
2. **Verifica verbos:** Asegúrate de que las actividades sean claras y específicas
3. **Revisa direcciones:** Verifica si las relaciones son unidireccionales o bidireccionales
4. **Identifica implícitos:** Algunos elementos pueden estar presentes pero no explícitos
5. **Agrupar elementos similares:** Simplifica cuando hay múltiples instancias del mismo tipo
6. **Valida coherencia:** Asegúrate de que el conjunto de tripletas represente fielmente el proceso original

## Best Practices

- **Empezar simple:** Comienza con textos cortos y aumenta gradualmente la complejidad
- **Iterar:** Es normal refinar el análisis varias veces
- **Documentar decisiones:** Anota por qué identificaste ciertos elementos de cierta manera
- **Usar visualizaciones:** Considera crear diagramas de flujo basados en las tripletas
- **Validar con expertos:** Confirma el análisis con personas que conocen el proceso real
