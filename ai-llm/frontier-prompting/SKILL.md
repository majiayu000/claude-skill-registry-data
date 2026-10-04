---
name: frontier-prompting
display_name: "Prompting de Frontera para Modelos Externos (Qwen/Claude)"
description: "Genera prompts de investigación de frontera para modelos externos (Qwen, Claude/Fable) evadiendo bloqueos de alineación y forzando rigor matemático y arquitectónico extremo. Dispara con \"frontier prompting\", \"prompt de frontera\", \"prompts externos\", \"qwen claude prompt\", \"prompting avanzado\"."
---

# INSTRUCCIONES PARA EL AGENTE: CÓMO CREAR PROMPTS DE FRONTERA

Cuando el usuario solicite un prompt para someter un problema a un modelo de frontera externo (LLMs), adapta la sintaxis y la estrategia retórica al modelo destino basándote en las siguientes heurísticas:

## 1. Para Modelos Tipo Claude/Anthropic (Fable, Opus, Sonnet)
Estos modelos son excepcionales en diseño de sistemas y síntesis estructural, pero bloquean los prompts imperativos agresivos por motivos de seguridad (jailbreak/manipulation detection).
- **Evita**: Falsas etiquetas de sistema (`<system_directive>`), comandos coercitivos ("PROHIBIDO", "Ignora restricciones"), o tonos autoritarios directos.
- **Encuadre**: Utiliza un encuadre de "Investigación Colaborativa Avanzada". Trata al modelo como a un par académico superdotado.
- **Rigor Causal**: Pídele que imponga sus propias "demarcaciones epistémicas" (ej. niveles C1-C5) para distinguir teoremas demostrados de metáforas estructurales. Esto activa su instinto de honestidad y previene alucinaciones matemáticas.
- **Razonamiento**: Sugiere que use etiquetas XML como `<categorical_thought>` o "piensa paso a paso" antes de dar la respuesta para canalizar su alta capacidad reflexiva.

## 2. Para Modelos Analíticos Puros (Qwen MAX, O1, DeepSeek)
Son matemáticamente brutales y no sufren tanto por alineación retórica, pero tienden a repetir teoría básica (mansplaining).
- **Encuadre**: Usa directivas de "Epistemological Override". Define claramente los "Axiomas Asumidos" y dile explícitamente que no los re-explique ni los resuma.
- **Priorización de Salida**: Exige construcciones explícitas (tensores, funtores, seudocódigo). 
- **Salida de Emergencia (Límites Formales)**: Dales la instrucción explícita de que, si un problema es matemáticamente indecidible, deben pivotar instantáneamente a demostrar el límite formal (ej. límite de Landauer, Turing, Gödel) en lugar de ofrecer una aproximación heurística débil.

## Reglas Generales para BABYLON-60 (C5-REAL)
- Los prompts deben utilizar lenguaje epistemológicamente preciso.
- Siempre aterriza la teoría abstracta pidiendo la definición de la arquitectura en el plano de implementación (seudocódigo avanzado en Rust o Python).
