---
name: recursive-research
version: 2.2.0
author: Joseph Huayhualla (@Anjos2)
license: MIT
repository: https://github.com/Anjos2/recursive-research
description: Investigación recursiva profunda con loop auto-regulado hasta nivel PhD. Aplicable a cualquier dominio (ciencia, tecnología, negocio, arte, humanidades). Usa WDM + Inversión Munger para decisiones autónomas, tiering de fuentes confiables, y checkpointing a disco para sobrevivir límites de contexto.
---

# Skill: Investigación Recursiva Profunda (v2.0)

Investigación auto-regulada que itera hasta alcanzar **nivel PhD** sobre una semilla de investigación (tema raíz). Funciona en cualquier dominio: ciencias formales, naturales, sociales, humanidades, artes, tecnología, negocio.

## Cuándo usar

- Quieres profundizar en un tema hasta el nivel de un experto
- Necesitas entender un campo nuevo para tomar decisiones informadas
- Preparas un documento técnico, paper, propuesta o estudio
- Quieres identificar estado del arte + gaps de conocimiento

## Principios

1. **Pregunta antes de investigar** — la skill interroga al usuario sobre semilla, modo y fuentes ANTES de arrancar
2. **Fuentes confiables con tiering transparente** — rechaza automáticamente fuentes no fiables
3. **WDM + Inversión Munger** en toda decisión autónoma no trivial
4. **Loop con auto-regulación** — no iteraciones fijas; criterio medible para cerrar
5. **Checkpointing defensivo** — guarda a disco cada ciclo; sobrevive compact / cierre de sesión
6. **Pausa preventiva** — detecta proximidad al límite de contexto y sugiere pausar antes del cierre forzoso

---

## Flujo completo

### Fase 0 — Preguntas iniciales (la skill interroga)

Al invocar `/recursive-research`, la skill pregunta al usuario, en orden:

1. **Semilla de investigación**: "¿Cuál es el tema que quieres investigar?" (texto libre)
2. **Modo**: `web` / `local` / `mixto`
3. **Si incluye local**: "¿Qué rutas locales debo investigar?" (lista de paths separados por comas)
4. **Fuentes priorizadas** (opcional): autores, dominios, publicaciones preferidas
5. **Fuentes excluidas** (opcional)
6. **Tope duro de ciclos** (default: 20; configurable)

La skill presenta un resumen y espera confirmación antes de arrancar.

---

### Fase 1 — Preparación del espacio de trabajo

1. Generar `slug` de la semilla (kebab-case, máx. 40 caracteres)
2. Verificar / crear `memoria/investigaciones/<slug>/` en el directorio de trabajo actual
   - **Si `memoria/` NO existe, crearla** explicando: *"No existe la carpeta `memoria/` en el proyecto. La creo porque la skill necesita consolidar hallazgos en disco cada ciclo — es lo que permite reanudar la investigación en sesiones nuevas."*
3. Crear archivos iniciales:
   - `estado.md` — metadatos, progreso, métricas
   - `hilos.md` — árbol de hilos semilla + sub-hilos
   - `fuentes-tier-1.md`, `fuentes-tier-2.md`, `fuentes-tier-3.md`, `fuentes-rechazadas.md`
   - `hallazgos.md` — consolidación

---

### Fase 2 — Identificar hilos semilla

Generar **3-5 hilos semilla** (ángulos distintos del tema).

**Aplicar WDM a la selección de hilos**:

| Criterio | Peso | Qué evalúa |
|---|---|---|
| Cobertura conceptual | 4 | ¿Cubre una dimensión distinta del tema? |
| Diversidad de perspectivas | 3 | ¿Trae voces / escuelas distintas? |
| Accesibilidad de fuentes | 3 | ¿Existen fuentes Tier 1/2 para este hilo? |
| Relevancia al usuario | 4 | ¿Alinea con el objetivo que motivó la investigación? |

Evaluar 5-8 hilos candidatos, seleccionar top 3-5.

**Inversión Munger sobre los hilos elegidos**:
- ¿Qué hilo importante estoy ignorando?
- ¿Qué perspectiva ausente haría que mi investigación sea parcial?
- ¿Qué escuela / voz disidente no aparece?

Si la inversión revela un hilo crítico faltante, agregarlo y re-ejecutar WDM.

**Ejemplos por dominio** (NO solo código):

| Dominio | Semilla | Hilos típicos |
|---------|---------|---------------|
| Ciencia | Inmunoterapia contra cáncer | Mecanismos moleculares / Ensayos clínicos / Historia y evolución / Controversias y limitaciones / Estado comercial |
| Arte | Minimalismo en música del siglo XX | Compositores clave / Técnicas / Contexto histórico-cultural / Crítica y recepción / Obras emblemáticas |
| Negocio | Modelos de monetización SaaS B2B | Pricing strategies / Métricas financieras / Casos documentados / Marco legal / Psicología de compra B2B |
| Humanidades | Filosofía estoica aplicada moderna | Fuentes primarias (Epicteto, Séneca, Aurelio) / Interpretaciones contemporáneas / Aplicaciones prácticas / Críticas filosóficas / Evidencia empírica psicológica |
| Tecnología | Arquitectura hexagonal en microservicios | Fundamentos teóricos / Implementaciones por lenguaje / Casos reales / Trade-offs y críticas / Herramientas |

---

### Fase 3 — Detectar herramientas disponibles

Antes del primer ciclo, detectar MCPs disponibles y ordenar por preferencia:

**Preferencia (mayor a menor velocidad/efectividad)**:

1. **MCPs de scraping optimizados para IA**: Firecrawl (`firecrawl_scrape`, `firecrawl_crawl`, `firecrawl_search`, `firecrawl_extract`) — texto estructurado, rápido
2. **MCPs de documentación oficial**: Context7 (`query-docs`) — cuando la fuente es una librería/framework
3. **Herramientas nativas**: `WebSearch`, `WebFetch` — fallback universal
4. **MCPs de navegación real (Chrome DevTools)**: DESPRIORIZADOS — solo si el contenido requiere ejecución JS explícita (SPAs sin SSR, contenido tras auth)

Razón: scrapers de IA son 10-50× más rápidos que navegadores reales y dan texto ya estructurado.

---

### Fase 4 — Fuentes semilla sugeridas

La skill presenta al usuario una lista de fuentes semilla **pre-cargadas por dominio** para que **confirme, añada o rechace**:

**Ciencia general / papers**:
- arXiv (https://arxiv.org) — preprints en física, matemáticas, CS, biología, economía
- Semantic Scholar (https://www.semanticscholar.org) — red de citaciones
- Google Scholar (https://scholar.google.com)
- Connected Papers (https://www.connectedpapers.com) — mapas visuales de citaciones
- OpenReview (https://openreview.net) — revisiones abiertas en ML

**Medicina / biología**:
- PubMed (https://pubmed.ncbi.nlm.nih.gov)
- Cochrane Library (https://www.cochranelibrary.com) — meta-análisis
- WHO (https://www.who.int)
- ClinicalTrials.gov

**Humanidades / ciencias sociales**:
- JSTOR (https://www.jstor.org)
- SSRN (https://www.ssrn.com)
- Project MUSE (https://muse.jhu.edu)

**Código / tecnología**:
- GitHub (búsqueda, topics, starred lists de expertos)
- Context7 para docs oficiales (si MCP disponible)
- RFCs (https://www.rfc-editor.org)
- W3C specs (https://www.w3.org/TR/)

**Datos / estadística**:
- Banco Mundial (https://data.worldbank.org)
- OECD Data (https://data.oecd.org)
- Our World in Data (https://ourworldindata.org)
- Pew Research (https://www.pewresearch.org)
- Eurostat, INE, y equivalentes nacionales

**Arte / cultura / humanidades**:
- Europeana (https://www.europeana.eu)
- Google Arts & Culture (https://artsandculture.google.com)
- Internet Archive (https://archive.org)
- Project Gutenberg (https://www.gutenberg.org)

**Generales**:
- Wikipedia — como PUNTO DE PARTIDA. Saltar siempre a la sección de **referencias** para llegar a Tier 1/2
- Wikidata — datos estructurados

**Fuentes locales** (si el usuario proporcionó rutas):
- Listar estructura de carpeta
- Priorizar `.md`, `.pdf`, `.txt`, `.doc/.docx`, `.html`, `.epub`
- Usar herramientas de lectura del agente (Read, Grep, Glob)

---

### Fase 5 — Ciclo de investigación (LOOP auto-regulado)

Cada ciclo ejecuta los siguientes sub-pasos.

#### 5.1. Elegir el hilo con menor cobertura

Calcular cobertura actual de cada hilo (`hallazgos_registrados / hallazgos_esperados_proxy`). Elegir el de menor %.

#### 5.2. WDM + Munger sobre fuentes a usar en ESTE ciclo

**WDM por fuente candidata**:

| Criterio | Peso | Escala |
|----------|------|--------|
| Autoridad (Tier) | 5 | Tier 1 = 5 · Tier 2 = 3 · Tier 3 = 2 · Rechazo = 0 |
| Relevancia al hilo actual | 5 | 1-5 por match semántico |
| Accesibilidad | 3 | 5 = full text abierto · 3 = abstract + paywall · 1 = bloqueado |
| Recencia apropiada al campo | 2 | Código: reciente > viejo · Filosofía clásica: viejo = relevante |
| Ausencia de conflicto de interés | 3 | 5 = independiente · 1 = financiada por parte interesada |

Seleccionar top 3-5.

**Inversión Munger sobre las fuentes seleccionadas**:
- ¿Qué fuente NO estoy usando que debería? (disidentes, escuelas críticas, voces silenciadas)
- ¿Qué sesgo comparten todas las seleccionadas? (solo anglosajonas, solo de una época, solo de una escuela)
- ¿Qué opinión contraria existe documentada? → Añadir al menos 1 fuente contradictoria si existe

#### 5.3. Ejecutar búsquedas / lecturas

- Usar MCPs en orden de preferencia detectado en Fase 3
- Extraer: hechos concretos, datos numéricos, citas textuales con atribución, nombres de personas/obras/conceptos nuevos
- Registrar en notas de trabajo del ciclo

#### 5.4. Aplicar tiering a cada fuente consultada

**Tier 1 — Máxima confianza**:
- Papers peer-reviewed en revistas indexadas (Scopus, Web of Science, PubMed, ACM, IEEE)
- Libros de editoriales académicas (MIT Press, Oxford UP, Cambridge UP, Springer)
- Documentación oficial de estándares (W3C, IETF/RFC, ISO, IEEE, WHO, FDA, BIS)
- Archivos primarios verificables (museos nacionales, bibliotecas universitarias, archivos estatales)
- Datos crudos de instituciones estadísticas oficiales

**Tier 2 — Alta confianza**:
- Repositorios oficiales de proyectos activos y reconocidos
- Blogs/publicaciones de autores citables (investigadores, profesionales con trayectoria verificable)
- Charlas en conferencias reconocidas (con video y paper)
- Wikipedia *CON* referencias a Tier 1/2 (tratar como agregador de referencias)
- Reportes de think tanks / consultoras con metodología publicada (Pew, Gartner, McKinsey Institute)

**Tier 3 — Útil con cautela**:
- Blogs con citaciones internas a Tier 1/2
- Stack Overflow / foros con voto alto + citaciones
- Entrevistas grabadas con expertos identificables
- Publicaciones de industria con autoría clara

**Rechazo automático**:
- Sin autor identificable
- Marketing sin datos empíricos
- Agregadores spam / SEO
- Tutoriales sin citar fuentes
- Social media sin contexto verificable
- Contenido generado por IA sin supervisión humana documentada

Cada fuente consultada se registra en el archivo tier correspondiente con: título, URL, autor, fecha, tier asignado, justificación.

#### 5.5. Consolidar en checkpoint

Guardar al final del ciclo: `memoria/investigaciones/<slug>/ciclo-N.md` con:
- Hilo trabajado
- Fuentes consultadas (con tier)
- Hallazgos nuevos
- Conexiones con hilos previos
- Preguntas abiertas para próximos ciclos

#### 5.6. Actualizar `estado.md`

- Incrementar contador de ciclos
- Recalcular cobertura por hilo
- Registrar métrica de saturación: `saturacion = hallazgos_nuevos_ciclo / hallazgos_totales_acumulados`
- Actualizar estimación de tool calls y tokens de output consumidos

#### 5.7. Evaluar criterios de cierre — Función de fitness "nivel PhD"

Los 5 criterios DEBEN cumplirse todos:

1. **Cobertura ≥80%** en todos los hilos semilla
2. **≥3 fuentes Tier-1 por hilo** (o Tier 1+2 combinadas si el campo tiene pocas Tier 1)
3. **Saturación ≤5%** durante 3 ciclos consecutivos
4. **Inversión Munger aplicada al estado del conocimiento**: documentado qué NO sé, qué contradicen las fuentes, qué sesgos detecté
5. **Síntesis cruzada entre hilos**: ≥3 conexiones explícitas entre hilos diferentes registradas

**Decisión**:
- Todos cumplidos → Fase 6 (cierre natural)
- Tope de ciclos alcanzado → Fase 6 (cierre forzado con aviso)
- Caso contrario → continuar al paso 5.8

#### 5.8. Pausa preventiva (check de contexto)

Umbrales:
- `tool_calls_en_sesion ≥ 150`
- **O** `tokens_output_aprox ≥ 80000`

Si se cruza cualquiera:

1. Escribir checkpoint completo (5.5 + 5.6)
2. Emitir mensaje:

```
[PAUSA PREVENTIVA RECOMENDADA]

Estado actual:
- Ciclos completados: N
- Tool calls en sesión: X (cerca del límite)
- Tokens de output aprox: Y

Razón: me aproximo al límite de contexto. Si continúo, podría perder coherencia
al compactarse la sesión.

La investigación está guardada en:
  memoria/investigaciones/<slug>/

Para reanudar en nueva sesión:
  /recursive-research --resume <slug>

¿Pausar aquí, o continuar 1-2 ciclos más? (continuar / pausar)
```

3. Esperar respuesta. Si `continuar`, seguir. Si `pausar`, saltar a Fase 6 (cierre parcial documentado).

Si no se cruza el umbral → volver a 5.1 para próximo ciclo.

---

### Fase 6 — Cierre

Sea cierre natural (5 criterios cumplidos), forzado (tope de ciclos), o parcial (pausa manual):

1. **`sintesis.md`** — síntesis ejecutiva:
   - Resumen en lenguaje simple (3-5 párrafos)
   - Hallazgos por hilo con referencias cruzadas
   - Controversias y contradicciones detectadas
   - Gaps de conocimiento (qué NO se investigó / qué sigue abierto)
   - Mapa de hilos seguidos (árbol)

2. **`acciones.md`** — checklist de acciones aplicables, priorizadas por impacto

3. **Inversión Munger FINAL al estado del conocimiento** (registrar en `gaps.md`):
   - ¿Qué sigo sin saber?
   - ¿Qué fuentes contradijeron entre sí y no resolví?
   - ¿Qué sesgo tiene mi conjunto de fuentes?
   - ¿Qué pregunta debería hacerme un revisor crítico que no sepa responder?

4. **Preguntar al usuario**:

```
[INVESTIGACIÓN COMPLETADA — estado: natural / forzado / pausado]

Semilla: <tema>
Ciclos ejecutados: N / <tope>
Fuentes consultadas: X total (T1: A · T2: B · T3: C · Rechazadas: D)
Estado PhD: alcanzado / NO alcanzado (razones: ...)

Gaps identificados:
  1. ...
  2. ...
  3. ...

Opciones:
  1. Cerrar aquí
  2. Profundizar un gap específico (indica cuál)
  3. Añadir nuevo hilo y continuar
  4. Cambiar de modo (web → mixto, etc.)

¿Qué prefieres?
```

**La investigación puede ser infinita** — solo se cierra por decisión del usuario.

---

## Modo `--resume`

Invocación: `/recursive-research --resume <slug>`

1. Buscar `memoria/investigaciones/<slug>/`
2. Si no existe → error claro, sugerir `/recursive-research` normal
3. Si existe:
   - Leer `estado.md` → reconstruir métricas
   - Leer último `ciclo-N.md` → contexto reciente
   - Leer `hilos.md` → árbol actual
   - Presentar: "Retomo desde ciclo N. Próximo paso: [hilo X]. ¿Continúo?"
4. Continuar el loop desde Fase 5

---

## Modo `--list`

Invocación: `/recursive-research --list`

Listar todas las investigaciones guardadas en `memoria/investigaciones/` del proyecto actual:
- Slug · Semilla · Ciclos completados · Estado (abierta / cerrada) · Última modificación

---

## Anti-patterns a rechazar activamente

1. **Búsqueda plana** — repetir queries con sinónimos sin profundizar en resultados reales
2. **Ignorar Munger** — seleccionar fuentes solo por confort; la inversión es obligatoria
3. **Checkpoint ausente** — avanzar 5 ciclos sin dumpear a disco
4. **Tier 3 sin referencias** — aceptar un blog sin que cite Tier 1/2 explícitamente
5. **Autoconfirmación del PhD** — declarar PhD sin los 5 criterios medidos; si uno falta, NO cerrar
6. **Ignorar gaps** — cerrar sin documentar qué no se sabe; los gaps son parte del entregable
7. **Condescendencia intelectual** — ocultar controversias o contradicciones "para no ensuciar la síntesis"; la honestidad intelectual ES el resultado
8. **Confiar ciegamente en el knowledge interno** — el conocimiento del agente puede estar desactualizado; siempre verificar contra fuente

---

## Estructura final de archivos generados

```
memoria/investigaciones/<slug>/
├── estado.md              ← progreso, métricas, metadata
├── hilos.md               ← árbol de hilos y sub-hilos con estado
├── fuentes-tier-1.md      ← fuentes más confiables consultadas
├── fuentes-tier-2.md      ← fuentes de alta confianza
├── fuentes-tier-3.md      ← fuentes con cautela
├── fuentes-rechazadas.md  ← fuentes evaluadas y descartadas (con razón)
├── hallazgos.md           ← consolidación de descubrimientos
├── ciclo-01.md            ← checkpoint del ciclo 1
├── ciclo-02.md
├── ciclo-N.md
├── sintesis.md            ← síntesis ejecutiva (Fase 6)
├── acciones.md            ← checklist de acciones aplicables
└── gaps.md                ← lo que NO se sabe, controversias, sesgos
```

---

## Ejemplo de invocación

```
Usuario: /recursive-research

Skill: ¿Cuál es el tema que quieres investigar?
Usuario: Mecanismos de la memoria episódica en humanos

Skill: ¿Modo? (web / local / mixto)
Usuario: mixto

Skill: ¿Rutas locales?
Usuario: C:/Dropbox/papers-neurociencia

Skill: ¿Fuentes / autores priorizados? (opcional)
Usuario: Endel Tulving, Eleanor Maguire

Skill: ¿Fuentes excluidas? (opcional)
Usuario: -

Skill: ¿Tope de ciclos? (default 20)
Usuario: 25

Skill: Confirmado.
       Semilla: "memoria episódica en humanos"
       Modo: mixto · Local: [C:/Dropbox/papers-neurociencia]
       Priorizar: [Tulving, Maguire] · Tope: 25 ciclos

       Aplicando WDM + Munger para identificar hilos semilla...
       [muestra tabla]

       Hilos seleccionados:
       1. Bases neuroanatómicas (hipocampo, PFC)
       2. Fenomenología y taxonomía (Tulving et al.)
       3. Trastornos y disociaciones (amnesia, Alzheimer)
       4. Modelos computacionales
       5. Neurociencia cognitiva contemporánea

       La carpeta `memoria/` no existe. La creo — es necesaria para
       consolidar cada ciclo en disco.

       Ruta: memoria/investigaciones/memoria-episodica-humanos/

       Arrancando ciclo 1 (hilo con menor cobertura: 1)...
```

---

## Autoría y licencia

- **Autor:** Joseph Huayhualla ([@Anjos2](https://github.com/Anjos2))
- **Licencia:** MIT — ver archivo `LICENSE` del repositorio
- **Repositorio:** https://github.com/Anjos2/recursive-research

Contribuciones bienvenidas. Si detectas un anti-pattern no cubierto, una heurística mejor, o un criterio de PhD más robusto, abre un PR.
