---
name: Checklist de Validación MAIA
key: validacion-maia-checklist
description: 24 criterios de validación del sistema MAIA. Los usa el Campaign Manager en Cierre como capa de control de calidad transversal.
version: 3.2.0
owner: system
status: active
---

# Checklist de Validación MAIA

Cargada por el Campaign Manager. Define los 24 criterios de validación que el Campaign Manager ejecuta en Cierre (post-Art Director) sobre el paquete completo de la campaña.

Esta skill formaliza la "Validación MAIA": una capa de control transversal que cruza todos los outputs de todos los agentes en un único paso final.

---

## Criterios de validación

### Cierre (post-Art Director, sobre el paquete completo)

El Campaign Manager evalúa el paquete completo (brief + estrategia + estrategia creativa + mockups) contra estos 24 criterios:

| # | Criterio | Que verificar | Fuente |
|---|---|---|---|
| V01 | Coherencia con principios por canal | Cada campaña tiene check_principios. Ningun pasa_global: false sin justificación valida. | channel-playbook-* |
| V02 | Coherencia con CRM | Si hay email/CRM, respeta los principios del canal: idea dominante, CTA único, personalización no invasiva. | channel-playbook-email |
| V03 | Coherencia con tienda | Si hay tienda, respeta los principios: reducir ansiedad, no folleto, soportes con mision única. | channel-playbook-tienda |
| V04 | Coherencia con Movistar+ | Si hay M+, los formatos se usan según su rol (banner =/= preroll =/= First Impression). No como inventario genérico. | channel-playbook-movistarplus |
| V05 | Coherencia con digital | Si hay digital, cada pieza sabe en que fase del funnel esta. No todo es performance. | channel-playbook-digital |
| V06 | Coherencia de funnel y segmentos | La fase de funnel del briefing corresponde con los canales activados y la presión propuesta. La `segmentacion_creativa` de C cubre todos los `segmentos_operativos` de B sin omisiones ni invenciones. | matriz-objetivo-canal, campaign-output-format |
| V07 | Coherencia de marca | Los copies respetan tono y voz. No hay retailización de marca en fases altas del funnel. | brand-voice-movistar, tesis-estratégica-movistar |
| V08 | Nivel de presión y reglas heredadas | La presión comercial por canal es proporcional al valor aportado y al momento mental del cliente. Las `reglas_presion_heredadas` de C son copia literal de las `reglas_presion_comercial` de B. Si C propuso desviaciones, estan documentadas en `desviaciones_propuestas` con justificación. | tesis-estratégica-movistar, campaign-output-format |
| V09 | Frecuencia | Hay frecuencia definida por canal. No hay canales sin limite de impactos. | reglas-planner-movistar (P08) |
| V10 | Riesgo de saturación | No hay acumulación excesiva de canales sobre el mismo cliente en el mismo período. | journey-canales-movistar |
| V11 | Contradicciones entre canales | No hay mensajes contradictivos entre canales ni canibalización evidente. Coherencia con principios transversales de orquestación. | channel-playbook-transversales, Análisis cross-canal |
| V12 | Mandatorios de marca | Restricciones de marca y operativas del brief se respetan en el output final. | brief + brand-visual-guidelines-movistar |
| V13 | Identidad visual | Los mockups (HTML, imagen, otros) usan colores, tipografías y espaciados de brand-visual-guidelines-movistar. | brand-visual-guidelines-movistar |
| V14 | Calidad de pieza | Cada pieza tiene rationale, los placeholders estan documentados, los mockups son editables o tienen dimensiones reales del soporte. | Inspección directa |
| V15 | Calendario integrado | El `calendario_integrado` de C concreta la `secuencia_sugerida` de B. Hay al menos una entrada por semana del período. No hay semanas vacias sin justificación ni acumulación excesiva en una sola semana. | campaign-output-format |
| V16 | Arquitectura del mes | La `arquitectura_mes` de C hereda los movimientos del brief y todos los territorios estan asignados a un movimiento. Ningun territorio queda huerfano y ningun movimiento queda vacio. Si C reasigno algun territorio, hay flag `ajuste_propuesto` con justificacion. | campaign-output-format, golden-briefing-schema |
| V17 | Copy prototype y scoring de comunicacion | Cada campana tiene `copy_prototype` por canal activo con `notas_para_d` no vacias. Cada pieza tiene `scoring_comunicacion` con score calculado correctamente (base_60 + modulacion_40 = score). Scores < 70 tienen flag correspondiente con severidad media. El `tema_a_vigilar` es especifico de la pieza, no generico. Cada `scoring_comunicacion` tiene `principios_decisivos` con 1-3 entradas (principio + justificacion no vacios). | campaign-output-format |
| V18 | Piezas no producidas | El design rationale de D incluye seccion `piezas_no_producidas` con toda pieza de `copy_prototype[]` no seleccionada para produccion. Cada entrada tiene formato, canal, campana y motivo_exclusion no vacio. Si todas las piezas fueron producidas, la seccion lo indica explicitamente. | design_rationale |
| V19 | Procedencia completa | Toda afirmacion con valor informativo (dato, cifra, volumen, fecha, prioridad, restriccion, regla) lleva bloque `procedencia` con `nivel`, `fuente` y `validacion` no vacios. Cero afirmaciones sin procedencia. La `fuente` es concreta y verificable, nunca "el brief" a secas ni "analisis interno". | contexto-sistema-maia seccion 7 |
| V20 | Integridad de la herencia de procedencia | Ningun agente ha subido el nivel de una afirmacion respecto al agente anterior. Una `propuesta` de B sigue siendo `propuesta` en C y en E. Las reglas de presion, prelacion, contact policy y cascada de ofertas llevan `nivel: propuesta` y `validacion: no_confirmado`, y en ningun documento visible se presentan como decididas. Toda discrepancia conocida del original tiene su flag `dato_a_validar` y la cifra afectada esta marcada `a_validar`. | contexto-sistema-maia seccion 7 |
| V21 | Ausencia de claim paraguas transversal | No existe en el paquete una frase, promesa o idea verbal unica presentada como paraguas de todos los territorios. Control operativo: ninguna promesa se repite como idea dominante en mas de un tercio de los territorios del ciclo. Cada territorio tiene su propia `idea_dominante`. | 03-copywriter, golden-briefing-schema |
| V22 | Orientacion de comunicacion y decision de produccion | Cada territorio tiene los siete campos de la ficha de orientacion (objetivo, idea dominante, tension, tono, principio, por donde explorar, que evitar), todos no vacios y de extension breve. Cada territorio tiene su `decision_produccion` REUSE/ADAPT/REFRESH/CREATE con racional, `modo` declarado y `necesita_validacion_inventario`. Las verbalizaciones ilustrativas estan etiquetadas como direccion, nunca como copy final. Ningun soporte con Produccion MAIA = No lleva copy ni pieza. | 03-copywriter, eficiencia-creativa-movistar, matriz-soportes-movistar |
| V23 | Uso correcto del rendimiento | Toda `decision_produccion` en `modo: con_dato` trae `evidencia_rendimiento` completa con una de las seis metricas de RESPUESTA (CTR, leads, CPL, VTR, clics, interaccion) y su semana. **Ninguna decision SOBRE UN ACTIVO se apoya en impactos, impresiones, frecuencia ni ventas** (el Planner si puede usar esas metricas para calibrar presion y mix: la prohibicion es sobre juzgar creatividades, no sobre planificar). Toda decision en `modo: cualitativo` tiene `evidencia_rendimiento: null`, `necesita_validacion_inventario: true` y un racional que no afirma estar basado en datos. Si `cobertura_informes.nivel_confianza` es bajo, ninguna decision esta en modo con_dato. El brief trae `cobertura_informes` y, si hay semanas disponibles, `rendimiento_periodo_anterior` no vacio. | informe-semanal-publicidad, eficiencia-creativa-movistar |
| V24 | Paridad de version JSON-HTML | **[BLOQUEANTE]** Para cada agente upstream (Strategist, Planner, Copywriter), el sufijo de version del JSON coincide con el de su .docx y con el de todos sus .html. Un JSON parcheado cuyo HTML no se regenero no pasa: se devuelve al agente de origen. El Storyteller integra los HTML tal cual y no los reescribe, asi que un HTML desfasado llega intacto al comite. | 01-strategist, 02-planner, 03-copywriter |

---

## Como aplicar

1. El Campaign Manager recorre la tabla en orden. Para cada criterio, marca: OK, FLAG (con descripción), o NO_APLICA.
2. Los flags se incluyen en el resumen ejecutivo de cierre en el bloque correspondiente ([B1]-[B6]).
3. Si un criterio requiere cargar una skill que el Campaign Manager no tiene en ese momento, la carga antes de evaluar.
4. Un flag en V01-V07 puede ser bloqueante si contradice un principio sin justificación. V08-V11 son generalmente flags de riesgo (no bloqueantes por si solos).
5. **V19, V20 y V21 son bloqueantes sin excepción.** Un paquete con afirmaciones sin procedencia, con procedencia degradada o con un claim paraguas transversal no pasa a presentación. Son los tres criterios que protegen la credibilidad del documento ante el cliente, y su incumplimiento no se compensa con la calidad del resto.
6. V19 y V20 se verifican por conteo, no por lectura: recorrer los JSONs contando afirmaciones con valor informativo frente a bloques `procedencia` presentes, y comparar el `nivel` de cada afirmación heredada con el que traía del agente anterior. Un check que no se puede contar no se ha hecho.

---

## Relación con el self-check del Campaign Manager

Esta checklist complementa el self-check que el Campaign Manager ejecuta antes de publicar el resumen ejecutivo. El self-check verifica que el resumen refleja correctamente los datos; esta checklist verifica que los datos son correctos contra los principios del sistema.
