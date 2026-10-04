---
name: cortex-skill-auditor
display_name: "Auditor Exergético de Skills CORTEX Engine"
description: "Diagnóstico y auditoría exergética de las habilidades y skills del ecosistema CORTEX. Dispara con \"auditar skills\", \"auditoría de habilidades\", \"exergía skills\", \"solapamiento de triggers\", \"cortex skill auditor\"."
---

# Skill: Cortex Skill Auditor (Meta-Auditoría de Skills)

Este protocolo audita de manera automatizada y determinista la salud, redundancia y densidad de exergía del ecosistema completo de habilidades en `~/.gemini/config/skills/`.

---

## 1. Algoritmo de Auditoría

```python
def audit_skill_ecosystem(skills_dir):
    """
    Escanear y auditar todos los SKILL.md en el ecosistema.
     Mide solapamiento de triggers, compresión Kolmogorov y nivel de exergía.
    """
    # 1. Cargar metadatos de todos los skills
    skills = parse_all_skill_headers(skills_dir)
    
    # 2. Calcular matriz de solapamiento de triggers (Intersección de keywords)
    overlap_matrix = compute_trigger_overlap(skills)
    
    # 3. Medir uso histórico cruzando con transcript.jsonl
    telemetry = parse_historical_telemetry()
    
    # 4. Calcular ratio de compresión de Kolmogorov por skill
    compression_scores = {s.name: kolmogorov_ratio(s.body) for s in skills}
    
    # 5. Generar recomendaciones (MERGE, SPLIT, OPTIMIZE_TRIGGERS, DEPRECATE)
    recommendations = generate_actionable_recommendations(overlap_matrix, telemetry, compression_scores)
    
    return recommendations
```

---

## 2. Métricas de Evaluación Exergética

### 2.1. Ratio de Solapamiento de Triggers ($O_{i,j}$)
Intersección de palabras clave activadoras entre dos habilidades $S_i$ y $S_j$:

$$O_{i,j} = \frac{|\text{Triggers}(S_i) \cap \text{Triggers}(S_j)|}{\min(|\text{Triggers}(S_i)|, |\text{Triggers}(S_j)|)}$$

- Si $O_{i,j} > 0.6$: Alerta de alta colisión. Recomendar **FUSIÓN (Merge)** o refinamiento unívoco de disparadores.

### 2.2. Índice de Frecuencia de Uso ($U(S_i)$)
Conteo de activaciones históricas registradas en los logs `transcript.jsonl`.
- Si $U(S_i) == 0$ tras > 30 jornadas: Marcar como **Candidato a Depuración/Archivado**.

### 2.3. Densidad Exergética ($E(S_i)$)
Escala de 1 a 23.000 definida en [KERNEL.md](file:///Users/borjafernandezangulo/.gemini/config/skills/KERNEL.md#k6-taxonomía-exergética-escala-1--23000).

---

## 3. Formato Determinista de Reporte

Al ejecutar `cortex-skill-auditor`, la salida DEBE generar una tabla de diagnóstico estructurada:

| Skill | Nivel Exergético | Solapamiento Detectado | Frecuencia Telemetría | Acción Recomendada |
| :--- | :---: | :--- | :---: | :--- |
| `[nombre-skill]` | `[1-23.000]` | `[None / High (Skill_B)]` | `[Alta / Media / Nula]` | `[Mantener / Refinar / Merge]` |
