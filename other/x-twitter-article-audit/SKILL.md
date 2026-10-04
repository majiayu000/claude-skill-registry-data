---
name: x-twitter-article-audit
display_name: "Auditoría Epistemológica de Hilos y Artículos de X/Twitter"
description: "Extracción y auditoría epistemológica C5-REAL de hilos, artículos y posts de X/Twitter. Dispara con URLs de X/Twitter ('x.com/*/status/*', 'twitter.com/*/status/*'), 'auditar tweet', 'analizar hilo X'."
---

# X/Twitter Article & Thread Epistemic Audit Pipeline

Esta habilidad proporciona el flujo determinista para la extracción, estructuración, análisis cuantitativo y auditoría epistemológica de artículos e hilos en X (Twitter).

## 🎯 Criterios de Activación
- URLs crudas de X/Twitter: `x.com/*/status/*`, `twitter.com/*/status/*`.
- Intenciones del usuario: "analizar hilo de X", "auditar tweet", "resumir artículo de Twitter", "fact-check twitter".
- **Trigger Implícito:** Pegar una URL de X/Twitter cruda activa automáticamente este protocolo.

---

## 🛠️ Protocolo de Ejecución en 3 Pasos

### Paso 1: Extracción Atómica de Contenido (`read_url_content`)
1. Ejecutar `read_url_content` pasando la URL directa del post/artículo de X.
2. Leer el archivo HTML/markdown resultante generado en `.system_generated/steps/.../content.md`.
3. Aislar los metadatos clave: Autor (@handle), Titular/Encabezado, Fecha de Publicación, Texto del Artículo/Hilo y Métricas sociales (Likes, Retweets, Impresiones).

### Paso 2: Modelado y Taxonomía Cuantitativa (`scratch/`)
1. Generar un script Python en `scratch/` que extraiga y tabule la estructura formal del contenido (leyes, principios, teoremas o métricas):
   ```bash
   python3 -c 'import json; ...' > scratch/twitter_article_metrics.json
   ```
2. Ejecutar la simulación/guardado y verificar la coherencia de los indicadores empíricos.

### Paso 3: Auditoría Epistemológica C5-REAL
1. **Resumen Estructurado y Desglose por Principios:** Presentar cada ley o punto clave con su mecanismo cognitivo subyacente.
2. **Matriz de Clasificación Epistémica (4 Categorías):**
   - **Hechos Verificados:** Datos fácticos e interacciones reales.
   - **Evidencia Experimental / Métricas:** Multiplicadores empíricos, A/B tests, diferencias de reproducciones.
   - **Modelos y Doctrina:** Paradigmas teóricos, economía conductual, saliencia visual.
   - **Hipótesis / Especulación Fundamentada:** Atribuciones causales no aisladas de variables de confusión.
3. **Traducción a Arquitectura Local / UI/UX / Código Soberano:**
   - Mapear las leyes del empaquetado/contenido hacia principios de diseño de interfaces, documentación agéntica y reducción de anergía.
4. **Tabla de Auditoría de Afirmaciones & Calibración Global:**
   - Tabla: Minuto/Sección | Ley / Afirmación | Veredicto | Motivo Técnico | Evidencia.
   - Calcular la puntuación global de credibilidad (0-10) y desacoplamiento epistémico si procede.

---

## 🔒 Contrato de Autonomía
- **ZERO PAUSE INVARIANT:** El agente ejecutará la extracción y auditoría sin requerir interacción intermedia.
