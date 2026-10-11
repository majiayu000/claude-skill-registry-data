---
name: suite-optimization
description: Juez que lee la evidencia de run_history.jsonl y propone, o aplica, UN piloto de optimizacion de la suite del motor sin relajar asserts ni tocar barreras git reales (salvo una mejora de fixture demostrablemente segura), distinguiendo coste eliminable de coste re-atribuido. Usar cuando la suite canonica es lenta y hay una corrida completa en run_history.jsonl de la que derivar el objetivo. No usar para auditar la calidad de los tests (ver test-audit), para activar xdist ni para optimizar a ciegas desde la atribucion de pytest.
---

Lee `skills/suite-optimization/SKILL.md`.
