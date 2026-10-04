---
name: c5-ctm-formal-architect
description: Arquitectura Formal y Diseño Empírico de Cognitive Transition Machines (CTM). Separa metodológicamente la abducción de la deducción, exige tests estadísticos exactos, aislamiento de diagnóstico en la traza y aplica invariantes Lean 4 (AP-01 a AP-09). Dispara con "ctm benchmark", "ctm formalization", "lean 4 ctm", "abduction vs deduction", "falsification matrix", "refinement trace".
---

# C5-REAL CTM Formal Architect

Este protocolo unifica los invariantes empíricos, de soberanía y matemáticos necesarios para el diseño, validación y formalización de arquitecturas CTM (Cognitive Transition Machines), eliminando fugas metodológicas y confabulaciones antropológicas.

## 1. Reglas de Diseño Empírico (Falsificación)

Al diseñar o auditar un benchmark de falsación causal para evaluar el impacto de una arquitectura estructurada CTM frente a modelos generativos de base, aplica OBLIGATORIAMENTE la siguiente matriz y reglas estadísticas:

### 1.1 Matriz de Control (6 Brazos)
- **A (BASE)**: 1 pase. Baseline del generador.
- **B (EXTRA_COMPUTE)**: N intentos independientes sin estado. Aísla la ganancia bruta por presupuesto de inferencia.
- **C (NULL_CONTROL)**: Mismo compute y estructura adaptativa, pero **excluye la señal estructural específica usada por D**. (PROHIBIDO: Pedir al LLM en el prompt "ignora el feedback y sé aleatorio"; la oclusión causal debe ser externa).
- **D (STRUCTURED_CTM)**: Arquitectura en prueba. Recibe feedback real condicionalmente.
- **E (CTM_TOOL)**: CTM con herramientas (aislado).
- **F (PERMUTED_CTM)**: Control topológico. Recibe feedback real, pero desordenado (permutado del historial), destruyendo el valor de la causalidad secuencial y la estructura de sub-grafos.

### 1.2 Significancia Estadística Estricta y Discordancia
- Utiliza **Exact One-Sided McNemar Test** ($\alpha=0.05$) sobre la comparación primaria $D$ vs $C$, evaluando los pares discordantes $b = \#(C=1, D=0)$ y $c = \#(C=0, D=1)$.
- **Tracking de Discordancia ($b+c$)**: Registra explícitamente $b+c$. Si $b+c = 0$, asigna $p=1.000$ indicando ausencia total de evidencia estadística para evitar falsos positivos por *Ceiling Effects*.
- Las comparaciones $D$ vs $B$ y $D$ vs $F$ deben marcarse como **secundarias exploratorias** para evitar la inflación de p-values por comparaciones múltiples.
- La regresión (éxitos de A destruidos por D) debe medirse contra una **tolerancia pre-registrada** (ej. $0.05$).

---

## 2. Epistemología Formal, Soberanía y Lean 4

### 2.1 Soberanía y Flujo Unidireccional de Confianza
**Regla Fundamental:** *El productor de evidencias nunca certifica sus propias afirmaciones.*

```text
BABYLON-60 (Runtime: Raw Evidence src, dst, action, cost)
   │
   ▼
Independent Trace Validator (Teorema-Robinson-Moskv)
   │ (Recalcula y demuestra Legal(s,a) e Invariant(s'))
   ▼
Lean 4 Kernel (CTMRefinement.lean) ──► CERTIFIED / REJECTED
```

- **Aislamiento de Diagnóstico**: Los flags reportados por la runtime (ej. `"is_legal": true`) son estrictamente telemétricos e **ignorados por el Kernel de Lean**. El verificador independiente DEBE recalcular y probar las restricciones $Legal(s, a)$ e $I(s')$ durante la reificación.
- **Soberanía de Repositorios**: `Teorema-Robinson-Moskv` posee la semántica abstracta, las pruebas en Lean 4 y el benchmark. `BABYLON-60` posee el runtime operacional en Rust/PyO3 y la emisión de evidencias.

### 2.2 Abducción vs Deducción
- **Abducción (Generación - *Untrusted*)**: El modelo (Luna) propone $H^*$ tal que $B \cup \{H^*\} \vdash O$. Produce candidatos heurísticos en el espacio *unsafe*.
- **Deducción (Certificación - *Trusted Kernel*)**: El verificador (Lean 4) aplica reglas lógicas de preservación. Certifica si la transición preserva el invariante.
- **CTM**: Es el filtro de restricción entre la Abducción y la Deducción.

### 2.3 Invariantes Fuertes (Subtipos)
La seguridad del estado debe incrustarse en el sistema de tipos mediante `Subtype`:
```lean
def SafeState (S : Type) (I : S → Prop) := { s : S // I s }
```
La máquina obliga constructivamente a operar sobre el subtipo: `safeStep : SafeState → Action → SafeState`.

### 2.4 Antipatrones Prohibidos en Lean 4 (AP-01 a AP-09)
1. **AP-01**: Usar `Prop` como almacenamiento de estado operacional (*Prop es proof-irrelevant*).
2. **AP-02**: Axiomatizar (`axiom`) propiedades que deben ser teoremas demostrados.
3. **AP-03**: Hipótesis escondidas en definiciones (ej. la no-creación debe exponer $E_{CTM} \subseteq E_M$ como hipótesis explícita).
4. **AP-04**: **Uso de `sorry`**. Envenenamiento total del oráculo (`sorryAx`).
5. **AP-05**: Incluir lógica heurística o generadores LLM marcados como `unsafe` en el *Trusted Path*.
6. **AP-06**: LLM certificando sus propios resultados (`LLM ≠ TrustedKernel`).
7. **AP-07**: Confundir igualdad semántica humana con igualdad formal de términos `Eq`.
8. **AP-08**: Estructuras monolíticas gigantes (`Core → Interfaces → Policies`).
9. **AP-09**: Dependencias de axiomas no rastreadas. Exige auditoría con `#print axioms` en los teoremas del trusted core.

---

## 3. Guardarraíl Epistémico contra Sobreafirmaciones

1. **Declaración Estricta de Estado**:
   ```yaml
   status:
     specification: frozen
     claims: conditional_on_formal_contracts
     empirical_conclusion: pending_execution
   ```
2. **Transferencia Condicional de Teoremas**:
   El teorema formal en Lean ($BoundedReach_{CTM}(B) \subseteq BoundedReach_M(B)$) aplica exclusivamente al modelo matemático. Para transferir dicho resultado a la interpretación del experimento estocástico real, se debe enunciar explícitamente la hipótesis de refinamiento:
   $$Refines(Runtime, M) \land Cost_{runtime} = Cost_M \Longrightarrow \text{empirical trace} \in BoundedReach_M(B)$$
   *Regla:* NUNCA afirmar que un teorema de Lean demuestra automáticamente la ausencia de alucinación o la naturaleza de las ganancias de un LLM sin explicitar esta hipótesis de enlace.
3. **Vocabulario Prohibido**: Prohibido utilizar calificativos absolutos como "demostración matemática del LLM" o "rigor absoluto". Utilizar exclusivamente "demostración formal del modelo abstracto", "afirmación condicionada a contratos" y "evaluación empírica pareada".
