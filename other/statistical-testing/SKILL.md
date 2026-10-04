---
name: statistical-testing
description: >
  Tests de hipótesis con SciPy — elige el test correcto según los datos,
  interpretá p-values con cuidado, y evitá falsos positivos.
  Trigger: Cuando necesitás hacer tests de hipótesis, validar significancia estadística, o comparar grupos.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T3-balanced
---

# Skill: statistical-testing

Tests de hipótesis. No tires p-values sin entender qué significan.

## Trigger

- Querés saber si dos grupos son diferentes
- Necesitás validar si un cambio fue significativo
- Te pidieron "significancia estadística" en un análisis
- Comparás métricas antes/después de un cambio

## Workflow LEND

```
1. ANALIZAR
   ├── Tipo de comparación: dos grupos, múltiples grupos, antes/después
   ├── Tipo de dato: numérico (continuo) o categórico (conteo)
   ├── Supuestos: ¿normalidad? (Shapiro-Wilk) ¿varianzas iguales? (Levene)
   └── Tamaño de muestra: ¿n suficiente para detectar el efecto?

2. OFRECER (Menú del Senior)
   ├── A) Test paramétrico — t-test o ANOVA si los datos son normales
   ├── B) Test no paramétrico — Mann-Whitney o Kruskal-Wallis si no hay normalidad
   └── C) Bootstrap — distribución empírica sin supuestos, ideal para muestras chicas

3. ELEGIR → confirmación

4. HACER
   ├── Elegir test según esta tabla:
   │   2 grupos, independientes, normales → t-test independiente
   │   2 grupos, independientes, NO normales → Mann-Whitney U
   │   2 grupos, pareados, normales → t-test pareado
   │   2 grupos, pareados, NO normales → Wilcoxon
   │   3+ grupos, normales → ANOVA
   │   3+ grupos, NO normales → Kruskal-Wallis
   │   Categórico → Chi-cuadrado
   ├── Calcular: estadístico, p-value, tamaño del efecto (Cohen's d)
   ├── Interpretar: p-value < 0.05 = significativo, pero NO "verdadero"
   ├── Múltiples comparaciones: ajustar con Bonferroni o Benjamini-Hochberg
   └── Documentar: supuestos verificados, test usado, tamaño del efecto

5. VERIFICAR
   ├── Se verificaron los supuestos del test
   ├── p-value no es el único criterio — tamaño del efecto importa
   └── Si hay comparaciones múltiples, se ajustaron
```

## Patrones

- **p-value no es verdad**: p < 0.05 significa "improbable bajo la hipótesis nula", no "esto es cierto"
- **Tamaño del efecto**: un p-value chico con efecto chico no es interesante
- **Verificar supuestos siempre**: cada test asume algo (normalidad, homogeneidad de varianzas)
- **Múltiples comparaciones**: si hacés 20 tests, 1 va a ser significativo por azar. Ajustá.
- **Bootstrap**: cuando los supuestos no se cumplen y n es chico, bootstrap es tu amigo

## Anti-patrones

- ❌ p-hacking: hacer tests hasta que uno dé significativo
- ❌ No verificar supuestos: t-test con datos no normales y n chico
- ❌ p-value sin tamaño del efecto: "es significativo" no dice si importa
- ❌ Comparaciones múltiples sin ajuste: 20 tests → 1 falso positivo esperado
- ❌ "No significativo" ≠ "no hay efecto": puede ser que n sea muy chico
