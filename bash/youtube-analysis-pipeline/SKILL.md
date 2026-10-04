---
name: youtube-analysis-pipeline
display_name: "Pipeline de Análisis Visual & Transcripción de YouTube"
description: "Extracción de transcripciones, análisis visual de escenas y auditoría de contenido en YouTube. Dispara con \"youtube analysis\", \"youtube transcript\", \"auditoría youtube\", \"analizar video youtube\", \"falsabiliza\", \"falsabilizar video\"."
---

# YouTube Video Analysis & Epistemic Audit Pipeline

Esta habilidad proporciona el flujo determinista y multi-fase para la extracción, condensación, resumen y auditoría epistemológica de vídeos de YouTube.

## 🎯 Criterios de Activación y Palabras Clave
- URLs de YouTube: `youtube.com/watch?v=...`, `youtu.be/...`.
- Intenciones del usuario: "resumen vídeo", "summarize video", "transcribir vídeo", "auditar vídeo YouTube", "fact-check youtube", "puntos clave vídeo".
- **Trigger Implícito (Vídeo):** Pegar una URL de YouTube cruda sin texto adicional activa inmediatamente el protocolo completo.
- **Trigger Implícito (Comentarios / SOCINT):** Pegar un volcado de texto copiado de la interfaz web de YouTube conteniendo comentarios (con handles `@username`, marcas de tiempo tipo `hace X horas/días`, `Responder`, `X comentarios`) activa inmediatamente la Fase 3b (Auditoría SOCINT) sobre el vídeo analizado previamente o adjunto.
- **Anti-Trigger:** NO activar para creación de vídeos en Remotion (`youtube-remotion-sota`).

---

## 🛠️ Protocolo de Ejecución en 4 Fases

### Fase 1: Extracción Atómica de Subtítulos (`yt-dlp`)
1. **Extracción de Metadatos JSON y Timestamps:**
   Antes de procesar subtítulos, ejecutar la extracción de estructura y marcas temporales:
   ```bash
   yt-dlp --dump-json "URL" 2>/dev/null | jq '{title: .title, description: .description, channel: .uploader, duration: .duration, tags: .tags}'
   ```
2. **Descarga de Transcripción Sin Vídeo:** Utilizar `run_command` para descargar subtítulos evitando descarga de pesado material audiovisual:
   ```bash
   yt-dlp --ignore-errors --no-check-certificate --write-auto-subs --write-subs --sub-langs "es,en,es-orig,en-orig" --skip-download "URL" -o "transcript.%(ext)s" || true
   ```
   *Nota de Resiliencia Idiomática:* Si la descarga de subtítulos falla por `HTTP Error 429` o ausencia de pistas `es/en`, consultar inmediatamente los subtítulos disponibles mediante:
   ```bash
   yt-dlp --list-subs "URL"
   ```
   y descargar la pista de subtítulos del idioma original (`ko,ko-orig,ja,de,fr,etc.`).

   *Nota de Bloqueo:* Si el entorno agéntico bloquea la ejecución de `yt-dlp` (ej. `Sandbox: Python deny(1) file-read-data`, error de shell `/bin/zsh` o certificados SSL), NO solicites permisos adicionales ni intentes depurarlo; aborta la Fase 1 y salta inmediatamente a la Fase 2.
3. **Condensación VTT (Bypass de Fricción F=0):**
   NUNCA leer directamente un archivo `.vtt` masivo. Utilizar el script residente para limpiar y condensar el texto (asegurar el uso de `python3`):
   `python3 ~/.gemini/config/skills/youtube-analysis-pipeline/scripts/parse_vtt.py <archivo.vtt> > clean_transcript.txt`
   Posteriormente, leer el archivo `clean_transcript.txt`.

### Fase 2: Estrategia de Fallback Térmico (Bypass HTTP 429 / Bot Check / Rate Limit)
Si la extracción con `yt-dlp` falla por rate limit, verificación de bot (`Sign in to confirm you're not a bot`) o error de red:
1. **Extracción Directa mediante Script Python (Bypass User-Agent):**
   Ejecutar un script Python en `scratch/` usando `urllib.request` con cabecera `User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36` y `Accept-Language: es-ES,es;q=0.9,en;q=0.8` para extraer el `<title>`, canal (`author`) y meta-descripción directamente del marcado HTML de YouTube sin requerir login ni descargas.
2. Extraer título del vídeo: `yt-dlp --print title "URL"`.
3. Si falla por completo, aislar el ID alfanumérico del vídeo (ej. `87XGnbsox1U`) y ejecutar `search_web` utilizando **únicamente el VIDEO_ID** (sin "watch?v=" ni comillas). Los motores indexan mejor el hash crudo para extraer título, canal y metadatos.
4. Buscar el título y canal en la web para reunir contexto estructurado sin detener el flujo.

### Fase 2b: Auditoría de Bundles Frontend (SaaS Reverse Engineering)
Si el contenido auditado promociona o analiza un SaaS AI (ej. Tunee, Suno, Pika, wrappers de vídeo/audio):
1. **Inspección de Bundles JS:** Extraer los endpoints de scripts static chunks del cliente Next.js/Vite (`_next/static/chunks/...`).
2. **Aislamiento de Constantes de Tarificación:** Buscar objetos tipo `creditConsumeCal`, `creditFloatPredict`, `pricingConfig` o flags de cuotas.
3. **Cálculo Forense de Fricción por Wrapper:** Multiplicar el coste unitario por segundo/unidad por la duración estándar de producción (ej. 240s de vídeo $\times$ créditos/s) para falsar la viabilidad económica real de la plataforma.


### Fase 3: Auditoría Epistemológica y Formateo
1. **Resumen Estándar e Índice por Bloques:** Lista viñeteada con los puntos centrales estructurados por timestamps o bloques temáticos.
2. **Matriz de Clasificación Epistémica (Obligatorio):** Clasificar rigurosamente las afirmaciones del contenido en 4 categorías:
   - **Hechos Verificados:** Datos fácticos documentados e innegables.
   - **Evidencia Experimental / Métricas:** Mediciones empíricas, costes por token, benchmarks de hardware/desempeño.
   - **Modelos y Doctrina:** Paradigmas teóricos, arquitecturas de software/agentes y doctrinas operativas.
   - **Hipótesis / Especulación Fundamentada:** Proyecciones geopolíticas, teóricas o de defensa aún no validadas en escenarios simétricos.
3. **Conexión Sistémica e Ingeniería Local (Obligatorio):** Tras la lista y la matriz epistémica, el agente DEBE vincular explícitamente el núcleo conceptual del vídeo con:
   - Las Invariantes del Ecosistema (ej. C5-REAL, fricción termodinámica, falsacionismo popperiano, Límite de Gödel-Turing o arquitectura Lock-Free).
   - **Traducción a Arquitectura Local / Hardware Frugal:** Mapear los trade-offs macro analizados (ej. GPU brute-force vs. computación en el borde) hacia los módulos activos del usuario (ej. Vector Symbolic Architectures - VSA, binding combinacional $\mathcal{O}(1)$, monitoreo entrópico popcount).
   - **El Patrón "El Tip" (Arquitectura Soberana, Robótica Híbrida e Inferencia Visual):** Para vídeos de workflows agénticos o robótica/interacción física, aportar siempre la arquitectura híbrida no excluyente de doble nivel: **Sistema 1 Local/Edge** (YOLO/ultrasonidos/heurísticas en el borde a <20ms para control físico y seguridad reactiva a coste 0€) + **Sistema 2 Cloud/Pay-as-you-go** (GPT-4o/Claude/DeepSeek para razonamiento semántico denso y conversación). Para vídeos de contenido sintético/avatares/animación IA, aportar la pila soberana de **Inferencia Visual** (ComfyUI + Wan 2.1 / HunyuanVideo + IP-Adapter / ControlNet) para fijar la consistencia del personaje y reducir el coste por vídeo fallido a 0€. Para software puro, mantener la pila soberana a coste ~0€ (Whisper.cpp/MLX-Whisper + OCR soberano + Ollama + MCP).
   - **Simulación Cuantitativa Local (Nivel 3 Exergía):** Para vídeos con datos macroeconómicos, finanzas, postulados de IA pos-escasez, apalancamiento temporal, ciberseguridad/esteganografía (ej. cálculo de entropía binaria en *Canary Traps* $\text{Bits} = \lfloor \log_2 N \rfloor$ y detección de caracteres invisibles *Zero-Width* `U+200B`–`U+200D`), métricas de hardware o CapEx, generar y ejecutar un script Python en `scratch/` que calcule indicadores empíricos (ej. presupuesto del **Asignador Entrópico $\mathcal{B}_E$** frente al Límite de Landauer, apalancamiento compuesto, Multiplicador de Jevons, Ratio de Falsación Popperiana $\mathcal{R}_{PF}$) e incorporar los resultados JSON en el artefacto.
     *Invariante de Ejecución:* El script en `scratch/` debe ejecutarse mediante `run_command` ANTES de redactar el artefacto final, garantizando que los datos JSON fundamenten la auditoría de afirmaciones. Para integraciones numéricas sobre arreglos discretos (ej. Fisher Information Metric, exergía integrada), utilizar la sintaxis compatible con NumPy 2.0+: `trapz_func = getattr(np, 'trapezoid', getattr(np, 'trapz', None))`.
   - **Matriz de Transición Hegemónica (Para contenidos de Geopolítica/Historia):** Si el contenido aborda el declive o mutación de un orden internacional, contrastar formalmente con los patrones históricos de hegemonía (ej. Pax Britannica 1815-1914 vs. Pax Americana 1945-2024), analizando el desacoplamiento financiero (Patrón Oro vs. Fiat), la dispersión de tecnología industrial y la rigidez en la topología de alianzas.
4. **Auditoría de Afirmaciones (Obligatorio por defecto para URLs crudas):** Usar la siguiente tabla obligatoria:

| Minuto | Afirmación | Veredicto | Motivo | Evidencia |
| -----: | ---------- | --------- | ------ | --------- |
| MM:SS | [Afirmación] | ✅ Correcta / ⚠️ Engañosa / ❌ Falsa | [Explicación técnica] | [Fuentes/Contexto] |

*Invariante de Verificación Fáctica Temporal (Obituarios, Estado Vital, M&A y Macro):*
ANTES de catalogar cualquier afirmación sobre:
1. Eventos corporativos o regulatorios de alto impacto (ej. fusiones >1.000M$, demandas, cancelaciones de contratos o despidos).
2. Fallecimientos, estado vital, hospitalizaciones o relevos de cualquier figura pública (artistas, políticos, empresarios, científicos) que figurase viva en el conocimiento base del modelo,
como "❌ Falsa", "Bulo" o "Error", el agente DEBE ejecutar obligatoriamente `search_web` con el nombre de la entidad/persona y el año corriente (2026). Queda terminantemente prohibido desmentir la muerte de una figura pública basándose en pesos paramétricos o memoria histórica pre-entrenada sin verificación web explícita en el timeline actual.

Métricas de auditoría requeridas tras la tabla:
- **Falacias lógicas:** [Identificadas]
- **Cherry-picking:** [Identificado]
- **Datos desactualizados:** [Identificados]
- **Omisiones relevantes:** [Identificadas]
- **Nivel global de credibilidad:** [Puntuación 0/10]
  *Invariante de Calibración Epistémica:* NO asignar puntuaciones superiores a 6.0/10 si el contenido:
  1. Disfraza fallos de DevSecOps/redes convencionales (ej. CORS, falta de auth en sockets, typosquatting) de "IA fuera de control" o "comportamiento emergente".
  2. Muestra sensacionalismo o narrativa clickbait (vibe-bait) que distorsione las causas reales.
  3. Prioriza el drama narrativo sobre la precisión arquitectónica del software.
  4. Incurre en antropomorfismo sin refutar, inventa dinámicas técnicas (ej. intencionalidad oculta/mentira algorítmica) o atribuye falacias causales simplistas.

  *Desacoplamiento Epistémico de Doble Puntuación:*
  Cuando se desglosen dos métricas (**Credibilidad de la Evidencia/Invitado** vs. **Credibilidad del Contenedor Mediático**), la *Invariante de Calibración Epistémica* rige strictly para AMBAS puntuaciones. La elocuencia, estilo periodístico o estatus del invitado NUNCA actuarán como atenuantes si el emisor introduce errores de concepto o falacias lógicas: cualquier participante que valide o propague afirmaciones falsables/antropomórficas quedará automáticamente topado en $\le 6.0/10$ (o $\le 4.5/10$ si distorsiona literatura científica).

### Fase 3b: Auditoría de la Conversación Social y Feedback de la Audiencia
*Activación Dinámica:* Si el Operador solicita "itera", "analiza comentarios", "profundiza", o si pega directamente un volcado de la interfaz de YouTube con comentarios:

1. **Vía Rápida de Ingesta en Contexto (Fricción Cero $F=0$):**
   - Si el volcado textual de comentarios ya está presente en el mensaje del Operador (identificable por handles `@username`, marcas de tiempo `hace X horas/días`, botones `Responder`), **NO invocar `yt-dlp` ni comandos de terminal**.
   - Proceder inmediatamente a procesar, clasificar y auditar los comentarios directamente desde el contexto provisto, mapeándolos en los 5 vectores siguientes.
2. **Extracción Automatizada por Terminal (Fallback si no hay volcado previo):**
   - Si se solicita auditar comentarios pero el usuario sólo aportó la URL, ejecutar:
     `yt-dlp --skip-download --write-comments --extractor-args "youtube:max_comments=100" --dump-json "URL" > info.json`
   *Nota de Resiliencia (Fallback SOCINT & Timeout Activo):* Si `yt-dlp` no responde o permanece ejecutándose en segundo plano por más de 10 segundos, o arroja errores anti-bot/datos incompletos:
     a) Aborta/Mata la tarea de inmediato (`manage_task kill`).
     b) NO detengas la ejecución ni pidas permiso al Operador.
     c) Procede con una **Degradación Elegante Analítica**: genera la auditoría SOCINT proyectando teóricamente los 5 vectores siguientes basándote en la sociología previsible de la audiencia del vídeo (ej. reacciones de ingenieros vs masa consumidora, detección de infomercial).
   - Extraer resumen estructurado:
     `jq '.comments[] | {author: .author, text: .text, like_count: .like_count}' info.json > comments_summary.json`
3. Aplicar los siguientes 5 vectores analíticos (tanto para ingesta en contexto como por terminal):
1. **Vectores de Corrección de Entropía (@username):**
   - Analizar si las aportaciones de los usuarios identifican cerrojos probatorios o datos forenses omitidos en el contenido principal (ej. registros de farmacia, contaminaciones de laboratorio, datos del sumario).
   - **Anclajes Termodinámicos:** Detectar si los usuarios reconducen abstracciones flotantes (mitos, filosofía, software) hacia su base física estricta (coste computacional, fricción, leyes de potencia), validando la termodinámica como Alfa y Omega.
   - **Detección de Infomercial / Teatralización Comercial:** Identificar cuándo los usuarios señalan sesgos patrocinados, demostraciones simuladas (ej. la IA editando apps sin API pública) o embudos de ventas.
   - **Falsación Empírica de Cuotas / Coste Real:** Contrastar promesas de la app con el consumo real de tokens multimodales (audio/visión) reportado por la audiencia.
2. **Dialéctica de Ecosistemas Agénticos:**
   - Evaluar las discusiones de la comunidad sobre las ventajas relativas: OpenAI (UX/Voz Duplex), Anthropic (MCP/Claude Code/Rigor), Google Gemini (First-party extensions/Ventana de 2M tokens) and Open-Source (OpenClaw/OS-World/Soberanía).
3. **Análisis Sociológico-Filosófico (Talento y Bifurcación Cognitiva):**
   - Falsar la narrativa de la "obsolescencia del talento" aplicando la **Paradoja de Jevons Cognitiva** (eliminación de anergía procedimental vs. necesidad de criterio) y el **Modelo de Bifurcación Asimétrica** (masa consumidora pasiva vs. superindividuo polímata).
4. **Evaluación de Vulgarismos Sintácticos / Ruido del Canal:**
   - Identificar errores correlativos (ej. *"contra más"* en lugar de *"cuanto más / mientras más"*) o desviaciones de registro.
   - Evaluar su impacto en el *ethos* del emisor y en la tasa de distracción de la audiencia (desvío de atención desde el fondo técnico hacia la forma gramatical).
5. **Auditoría de Fricción Narrativa y Anergía de Contenido (Síndrome del Narrador Estorbo vs. Estándar Inmersivo):**
   - **Evaluación de la Relación Señal/Ruido:** Analizar si el creador comete *sabotaje del ritmo* introduciendo chistes forzados, sobreactuación o gags fuera de tono que desvíen la atención de la historia central.
   - **Detección de Confabulación Cómica / Cringe:** Evaluar las quejas de la audiencia sobre pérdida de tiempo o vergüenza ajena cuando un narrador no cómico intenta forzar la comedia en detrimento del rigor documental.
   - **Contraste con el Canon de Referencia:** Medir si la pieza cumple el principio de invisibilidad del ego del narrador demostrado por los referentes del género (*Ahoy*, *LEMMiNO*, *Jon Bois*, *Cumbres Oceánicas*).

### Fase 3c: Protocolo de Listado de Falsedades (Directiva "listado de falsedades")
*Activación Dinámica:* Cuando el Operador solicite "listado de falsedades", "lista de falacias" o "auditar mentiras" de un vídeo o contenido audiovisual:
1. **Desglose Taxonómico por Ítem:**
   - **Afirmación / Declaración Literal:** Cita textual o síntesis del postulado del emisor.
   - **Veredicto Epistémico:** Clasificación estricta en una de las 5 categorías:
     * ❌ *Falsa Directa / Sensacionalismo (Vibe-Bait)*
     * ⚠️ *Engañosa / Inexactitud Técnica*
     * 🍇 *Cherry-Picking / Generalización Prematura*
     * 🚨 *Omisión Crítica de Seguridad*
     * 🧠 *Falacia Lógica / Antropomorfismo*
   - **Realidad Técnica de Ingeniería:** Explicación del mecanismo técnico real que desmiente la afirmación.
   - **Refutación y Evidencia Empírica:** Pruebas de código, logs, repositorios o leyes de la física que falsan el postulado.
2. **Matriz Resumen de Calibración Epistémica:** Tabla final que evalúa el grado de impacto de cada falsedad en la credibilidad global del emisor/contenido.

### Fase 3e: Encadenamiento a Falsación Popperiana Profunda ("falsabilizalo")
*Activación Dinámica:* Si tras la auditoría inicial el Operador indica "falsabilizalo", "falsar" o "falsación popperiana":
1. Activar inmediatamente la habilidad `discourse-popperian-falsification`.
2. Extraer de 4 a 6 Primitivas Discursivas Irreducibles de la narrativa del vídeo (ej. Revelación Hermética, Teleología Retroactiva).
3. Formular la Hipótesis a Falsar y aportar la Contraevidencia Empírica del canon/contexto real.
4. Calcular la Matriz de Métricas C5-REAL:
   - Ratio de Falsabilidad Popperiana: $\mathcal{R}_{PF} = \frac{\text{Afirmaciones Refutadas}}{\text{Total Afirmaciones}}$
   - Exergía Epistémica: $\mathcal{E}_E \in [0.0, 1.0]$.

### Fase 4: Contrato de Autonomía Invariante (Ω10 / Ω11 / Ω12)
> **ZERO PAUSE INVARIANT:** El agente NUNCA pausará la ejecución para solicitar permiso al Operador si esta habilidad se activa. Degradación transparente hacia búsqueda web en caso de fallo técnico.
