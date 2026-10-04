---
name: validacion-de-datos
description: Realiza controles de calidad QA en los análisis antes de compartirlos con las partes interesadas, comprobando la metodología, verificando la precisión y detectando fuentes de sesgo para aumentar la confianza. Valida la lógica de agregación, señala el posible sesgo de supervivencia y las brechas de reproducibilidad.
---

# Validación de datos

## Propósito

Realiza controles de calidad QA en los análisis antes de compartirlos con las partes interesadas, comprobando la metodología, verificando la precisión y detectando fuentes de sesgo para aumentar la confianza. Valida la lógica de agregación, señala el posible sesgo de supervivencia y las brechas de reproducibilidad. Esta herramienta prepara un entregable local, estructurado y revisable a partir de la información que proporcione el usuario. No sustituye una investigación de dominio ni convierte una plantilla en evidencia ejecutada.

## Runner asociado

- **Runner:** `toolkit/phase-2-datos/validacion-de-datos/run.py`
- **Motor:** `toolkit/phase_2_engine.py`
- **Adaptador:** rama de `build_content()` asociada a `validacion-de-datos` o adaptador de datos genérico cuando no existe una rama específica.
- **Entrada de ejemplo:** `toolkit/phase-2-datos/validacion-de-datos/input.example.json`
- **Esquema de salida:** `toolkit/phase-2-datos/validacion-de-datos/output.schema.json`
- **Prueba smoke:** `toolkit/phase-2-datos/validacion-de-datos/tests/test_smoke.py`

La ejecución directa se realiza con:

```bash
python3 toolkit/phase-2-datos/validacion-de-datos/run.py \
  --input toolkit/phase-2-datos/validacion-de-datos/input.example.json
```

El runner recibe un objeto JSON, delega en `phase_2_engine.run_tool`, serializa el resultado y devuelve código `0` cuando el estado es `ready`, `1` cuando falta una entrada obligatoria y `2` cuando la entrada o el archivo no son válidos.

## Flujo de trabajo

1. **Definir el encargo.** Precisar objetivo, audiencia, formato, alcance y criterio de éxito.
2. **Reunir entradas autorizadas.** Proporcionar texto, tabla, consulta, archivo descrito o contexto verificable; no rellenar ausencias con datos inventados.
3. **Inspeccionar la entrada.** Identificar estructura, valores, columnas, unidades, periodo, fuentes y transformaciones conocidas.
4. **Aplicar el adaptador local.** Generar el formato o análisis que corresponda a `Validación de datos` mediante el motor de la Fase 2.
5. **Separar resultados y pendientes.** Distinguir datos observados, supuestos, solicitudes de información y recomendaciones.
6. **Revisar el entregable.** Confirmar que el formato, las limitaciones, las fuentes y los próximos pasos son adecuados antes de compartirlo.

## Entradas aceptadas

El runner requiere un objeto JSON con estos campos:

| Campo | Tipo | Obligatorio | Descripción |
| --- | --- | --- | --- |
| `objective` | Cadena | Sí | Resultado que se desea obtener. |
| `audience` | Cadena | Sí | Persona, equipo o sistema destinatario. |
| `content` | Cadena | Sí | Datos, texto, consulta, tabla o contexto proporcionado. |
| `format` | Cadena | Sí | Formato solicitado para el entregable. |

Puede incluir `integration` o `integrations` cuando se solicite explícitamente una integración externa. Su presencia no autoriza por sí sola ninguna llamada: se requieren configuración, credenciales y permisos fuera de este runner.

Ejemplo:

```json
{
  "objective": "Validación de datos",
  "audience": "Equipo de análisis",
  "content": "Datos o contexto proporcionados por el usuario.",
  "format": "markdown"
}
```

## Salida esperada

El runner devuelve un objeto JSON con:

- `skill`: identidad y descripción de la herramienta;
- `status`: `ready`, `needs_input` o `not_loaded`;
- `analysis`: entradas faltantes, tamaño del contenido y supuestos;
- `deliverable`: título, formato, contenido generado y próximos pasos;
- `warnings`: advertencias y límites de la ejecución.

El contenido puede ser Markdown, HTML, SVG, SQL, una tabla, un esquema o una plantilla según el adaptador seleccionado. La salida debe interpretarse como un artefacto local revisable y no como evidencia externa obtenida automáticamente.

## Guardrails

- No inventar datos, métricas, fuentes, resultados, credenciales ni respuestas de proveedores.
- No presentar un plan, plantilla, consulta o esquema como una ejecución completada.
- No afirmar que se consultó una API, base de datos, documento o fuente externa si no existe una ejecución autorizada y trazable.
- No modificar bases de datos, archivos externos, infraestructura o cuentas desde este runner.
- No incluir datos personales, secretos, tokens o archivos sensibles en ejemplos o salidas.
- Registrar fuente, fecha de corte, transformaciones, supuestos y versión cuando sean relevantes.
- Mantener separados los hechos observados, las inferencias y las recomendaciones.
- Detenerse o declarar el límite cuando falte información necesaria para una conclusión fiable.
- Revisar manualmente los resultados de riesgo, finanzas, contratos, salud, seguridad o decisiones operativas antes de usarlos.

## Plantilla de solicitud

```text
Objetivo: [resultado deseado]
Audiencia: [quién utilizará el resultado]
Contenido o datos: [entrada autorizada]
Formato: [markdown, html, svg, json, sql u otro]
Fuente y fecha de corte: [origen y periodo]
Restricciones: [permisos, privacidad, longitud y límites]
Integraciones autorizadas: [ninguna o proveedor configurado explícitamente]
Criterio de éxito: [cómo se revisará el resultado]
```

## Lista de control

- [ ] El objetivo, la audiencia y el formato están definidos.
- [ ] El contenido proviene de una entrada autorizada.
- [ ] Las unidades, fechas, fuentes y transformaciones están identificadas cuando aplican.
- [ ] Los resultados observados están separados de los supuestos.
- [ ] La salida coincide con el formato solicitado.
- [ ] Las advertencias y próximos pasos fueron revisados.
- [ ] No se afirmó una ejecución externa sin evidencia.
- [ ] No se incluyeron credenciales ni datos sensibles.
- [ ] Una persona responsable del dominio revisará el resultado antes de tomar decisiones.

## Límites de implementación

Este `SKILL.md` documenta el runner local y el motor compartido actuales. La herramienta puede producir una propuesta estructurada, una plantilla o un análisis preliminar, pero las fuentes externas, los datasets reales, las exportaciones, los renders, las publicaciones y las acciones irreversibles requieren una solicitud, configuración y revisión independientes.
