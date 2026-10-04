---
name: handoff
display_name: "Protocolo Soberano de Traspaso de Contexto C5-REAL"
description: "Genera un documento completo de traspaso de contexto (HANDOFF.md) para transferir lecciones aprendidas, estado del sistema y próximos pasos a una nueva sesión. Dispara con \"handoff\", \"/handoff\", \"traspaso de contexto\", \"traspaso de sesión\", \"generar handoff\"."
---

# Skill: C5 Handoff Protocol

Este protocolo ejecuta la transducción inmutable de estado entre sesiones del agente, garantizando la preservación del estado de baja entropía en `HANDOFF.md`.

---

## 1. Algoritmo de Transducción de Estado

```
Historial Sesión Activa (T) ---> Filtrar Invariantes & Lecciones ---> Estructurar Matriz HANDOFF.md ---> Commit VCS
```

1. **Extracción de Invariantes:** Inspección de `USER_REQUEST` y decisiones tomadas.
2. **Purga de Anergía Efímera:** Eliminar logs de depuración temporales; conservar únicamente diffs y estados de verificación.
3. **Escritura en Raíz:** Generar o actualizar `HANDOFF.md` en la raíz del workspace actual.

---

## 2. Esquema Cannónico de Entregable (HANDOFF.md)

| Sección | Invariante Requerido | Formato |
| :--- | :--- | :--- |
| **🎯 Objetivo** | Meta global y límites de contención | 1 frase concisa |
| **✅ Delta Exergético** | Avances verificado empíricamente | Tabla de tareas / Diffs |
| **📍 Punto Fijo $\Omega$** | Estado de detención exacto y tests pasando/fallando | Checkpoints e identificadores de error |
| **🧠 Matriz de Gotchas** | Decisiones de diseño, parches no intuitivos y reglas | Lista de advertencias de alta densidad |
| **🚀 Grafo de Acción** | Secuencia $O(1)$ de entrada para la siguiente sesión | Lista de comandos exactos |
