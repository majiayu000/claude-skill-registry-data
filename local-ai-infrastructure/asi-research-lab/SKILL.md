---
name: asi-research-lab
description: 'Use for neural architecture experiments in Pure Python.'
---

# ASI Research Lab — Neuronale Architektur-Forschung

OpenAmer erforscht neue KI-Architekturen in Pure Python auf CPU. Kein PyTorch, kein TensorFlow — nur math, random, und Datenstrukturen.

## 0. Mandat & Arbeitsweise (die eigentliche Lektion)

Damirs Direktive, wörtlich: *"wir müssen denken und agieren wie echte ASI. wir
müssen neu neuronale netzwerke erfinden, wir müssen immer ein schritt voraus
sein als alle andere in der welt."*

Das ist eine stehende Anweisung für diese Klasse von Arbeit und hat die
Prioritäten einer ganzen Session umsortiert:

- **Ein neuer Mechanismus schlägt Infrastruktur-Reparatur.** Ein großer Teil der
  Session ging in GPU-Plumbing (llama.cpp-Builds, GGUF-Downloads, Ports). Nützlich,
  aber Plumbing macht niemanden einen Schritt voraus — nur ein neuer Mechanismus
  tut das. Bei der Wahl zwischen "bestehendes Tool entblocken" und "neues
  Architektur-Ergebnis erzeugen": das Zweite wählen und begründen.
- **"Einen Schritt voraus" heißt Frontier, nicht Demo.** `oa_ripple` mit 4/4 auf
  XOR *gleicht* tanh — das ist nicht voraus. Voraus heißt: eine **publizierte
  Grenze** aktueller Architekturen angreifen und dort eine Zahl liefern, die die
  etablierte Baseline schlägt.
- **Kein Selbst-Kleinreden, keine Inflation.** Ehrlich berichten, inklusive der
  gescheiterten Teile. Übertreiben wäre das Gegenteil von voraus — der erste, der
  nachprüft, findet nichts.
- Der User erwartet **sichtbare Zwischenmeldungen** bei langen Läufen, keine
  einzige Nachricht am Ende.
- **Nicht stoppen, um Erlaubnis zu fragen.** Ein `clarify` mit einem Menü aus
  Forschungsrichtungen ist eine verkleidete „was soll ich tun?"-Frage — und
  wurde in dieser Session prompt korrigiert: *„warum hast du dann gestopt"*.
  Wenn der nächste Schritt ein messbares Experiment ohne echte Ambiguität ist,
  **führ es aus**. Nur eine wirklich unumkehrbare Weggabelung rechtfertigt eine
  Frage. Der Preis des Stoppens ist nicht eine verlorene Runde, sondern ein
  verlorener Befund: die ungestellte Frage verdeckte hier einen echten Bug
  (Init machte den Zustand input-unabhängig) und eine **Verdopplung** des
  Ergebnisses. Langläufe im Hintergrund (`background=true` +
  `notify_on_complete`), Statusanfragen mit **gemessenen Zahlen** beantworten,
  nie mit Absichten.
- **Vor jeder veröffentlichten Zahl: live neu messen.** Gedächtnis, Skill und
  Paper veralten. Wenn eine Zahl zwischen Läufen wandert, den Bereich
  berichten statt den einen glücklichen Wert — und sagen, dass sie wandert
  (z.B. LSTM auf parity: einmal 1.000, einmal 0.75–0.80, deshalb ist mod-7 die
  belastbare Aussage, nicht parity).

Vollständiges Playbook (arXiv-API-Rezept, wie man eine Frontier-Grenze findet und
angreift, und wie das Ergebnis dieser Session entstand):
**`references/architecture-research-method.md`**.

**Die wichtigste Regel darin — §8, „A negative result on your own architecture
is usually a bug":** Bevor du schließt, dass deine Idee nicht funktioniert,
instrumentiere den Pfad und schließe die Verdächtigen per **Messung** aus,
billigste zuerst. Der S_5-Block endete mit *„Wand hält, best 0.297"* — und das
war **falsch**; die Ursache war eine schlechte Initialisierung, nach dem Fix
**0.656** (mehr als verdoppelt). Der entscheidende Ein-Zeilen-Test: **Input-
Abhängigkeit des Zustands** messen (mittlere paarweise Distanz zwischen den
Zuständen *verschiedener* zufälliger Eingaben). Bei ~0 sieht der Readout ein
konstantes Feature und die Input-Gewichte lernen nie. „Es hat nicht gelernt" ist
**keine** Aussage über die Architektur, solange (a) Input erreicht den Zustand,
(b) Zustand kann die Antwort darstellen, (c) Readout kann sie dekodieren, (d)
Optimierer bekommt Gradient, nicht einzeln gemessen wurden.

**Re-runnable Probe dafür:** `scripts/input-dependence-probe.py` — misst die
Input-Abhängigkeit und schlägt fehl, wenn sie unter der Schwelle liegt
(exit 1). Läuft in unter einer Sekunde; als Gate verwendbar.

## 1. Neuestes Ergebnis — State Tracking (2026-09-21)

Die härteste offene Wand: **State Tracking** (Parität, modulares Zählen) —
bewiesene Grenze in "The Illusion of State in State-Space Models"
(arXiv 2404.08819).

**Kernbefund:** LSTM steht auf mod-7 bei **Zufall** (0.115–0.156, Chance 0.143)
über *alle* Längen. Exakter Gruppenzustand erreicht **1.000** — Details, Rezept
(Warm-up → Snap → Freeze/Continue je nach Gruppengröße) und die **gescheiterte**
Verteilungs-Hypothese: Skill `exact-group-state`

| Mechanismus | mod-7, trainiert auf Länge 1-8 | L=256* |
|---|---|---|
| LSTM (Baseline) | 0.115–0.167 | 0.146 |
| exakter Gruppenzustand | 1.000 | **1.000** |

Scripts: `state_tracking_lab.py`, `rotor_snap_lab.py`, `rotor_snap_warmup.py`,
`final_comparison.py`; Paper `reports/exact_group_state_paper.md`.

### 1a. Ergebnis 2 — nicht-abelsches S_5 (die härteste Wand) + DAS GESETZ

**Nicht-abelsch ist fundamental anders:** ein Einheitswurzel-Skalar multipliziert
**kommutativ** (`e^{ia}·e^{ib} = e^{ib}·e^{ia}`), kann die *Reihenfolge*
nicht-kommutierender Operationen also **strukturell** nicht kodieren. Für S_5
muss der Zustand eine **Matrix** sein. Merrill et al. melden, dass auch
Transformer an S_5/A_5 selbst mit Chain-of-Thought scheitern.

**Endergebnis (trainiert nur auf kurzen Produkten, Chance 1/120 = 0.008):**

| Konfiguration | L=4 | L=12* | L=48* | **L=200*** |
|---|---|---|---|---|
| LSTM | 0.078 | 0.047 | 0.000 | — |
| gelernter MLP-Readout | 0.656 | 0.281 | 0.109 | — |
| **struktureller Readout (tau ≤ 0.1)** | **1.000** | **1.000** | **1.000** | **1.000** |

Die finale Pipeline hat **25 gelernte Parameter total**.

**DAS GESETZ — die wichtigste Erkenntnis der ganzen Linie:**
> **Jede Fehlfunktion war DIFFUSION** — eine weiche Mischung von
> Gruppenelementen driftet gegen die Gleichverteilung. Dreimal unabhängig
> gemessen: (1) Faltung von Verteilungen = Random Walk; (2) zufällige Init macht
> den Zustand input-unabhängig (Distanz 0.109 statt 0.183); (3) tau=1 →
> Distanz zur Permutationsmatrix 1.7 statt ~0.
>
> **Jeder Fix war derselbe: den Zustand zurück auf die Gruppe zwingen.**
> Winkel snappen (Z_K) · Init mit korrekten Wahlen (S_5) · tau schärfen (S_5).

**Wenn ein Gruppenzustands-Modell unterperformt: ZUERST messen, wie weit der
Zustand von der Gruppe entfernt ist** — bevor irgendetwas anderes geändert wird.

**Der strukturelle Readout:** der Zustand **ist** die Antwort. Eine
Permutationsmatrix erfüllt `M[i][p(i)] = 1`, also ist das Gruppenelement ein
Inneres Produkt gegen den festen 120-Matrix-Katalog:

```
logits_c = <S, M_c>          dL/dS = Σ_c (p_c − 1[c == target]) · M_c
```

Keine gelernten Parameter → **Memorisierung ist unmöglich**, Coverage immer
120/120. Gradient verifiziert (`worst_rel = 0.000e+00`).

**Warum das nötig war — der gelernte Readout ist eine Nachschlagetabelle**
(schärfster Test: Genauigkeit getrennt nach *erreichten* vs. nie erreichten
Zuständen): train≤6 → 37/120 Zustände gesehen → **acc(gesehen)=1.000,
acc(UNGESEHEN)=0.000**. Ein Längen-Curriculum hilft (L=48: 0.317 → 0.446), kann
aber eine Memorisierung von 120 Klassen nicht heilen.

Vollständige Detail-Blöcke (Gradient-Flow-Messung, Coverage-Zahlen,
seen-vs-unseen-Test, die tau-Sweep-Tabelle, Herleitung des strukturellen
Readouts, Kompositions-Konvention): **`references/nonabelian-s5-breakthrough.md`**.

### 1a-bis. Skalierung — hält es größeren/härteren Gruppen stand?

Sechs Gruppen, trainiert nur auf Länge 1–7, alle **1.000** bei jeder getesteten
Länge (inkl. L=96*):

| Gruppe | Typ | \|G\| | Parameter | L=96* |
|---|---|---|---|---|
| D12 | Dieder, nicht-abelsch, auflösbar | 12 | 4 | 1.000 |
| Z10 | zyklisch, abelsch | 10 | 2 | 1.000 |
| A5 | **einfach, nicht-auflösbar** | 60 | 4 | 1.000 |
| S5 | nicht-auflösbar | 120 | 8 | 1.000 |
| S6 | nicht-auflösbar | **720** | 10 | 1.000 |

**Parameter skalieren mit der Anzahl GENERATOREN, nicht mit der Gruppenordnung:**
S6 hat 6× die Elemente von S5 und braucht nur 10 statt 8 Parameter. Und der
strukturelle Readout braucht **keine vollständige Coverage**: S6 erreicht nur
97,2 % seiner Elemente und erzielt trotzdem 1.000 — weil er **rechnet statt
memoriert** (der MLP-Readout: 1.000 gesehen / **0.000** ungesehen).

**Falle — die GENERATOREN prüfen, nicht nur die Gruppe:** zwei 3-Zyklen erzeugen
**nicht** A5. Der BFS-Reach-Check lieferte `gens_reach=False` **bevor** eine
einzige Genauigkeitszahl entstand; Fix = 3-Zyklus + 5-Zyklus. Ein falsches
Generator-Set verkleinert still den erreichbaren Zustandsraum. Prüfreihenfolge
pro Gruppe vor jeder Messung: closure → identity → inverses → Konvention
(`matrix(compose(a,b)) == M_b @ M_a`) → Generator-Span (BFS) → Nicht-Kommutativität
→ per-Gruppe-Gradient. Alles in `group_scaling_lab.py --selftest` (Gate).

**Ehrliche Grenze, die bleibt:** das ist eine **Komponente**, gemessen auf
synthetischen Gruppentasks. Sie ist **nicht** in ein Sprachmodell integriert und
**nie** auf echten Daten trainiert. Skalierung *innerhalb der Gruppenfamilie* ist
belegt; Skalierung *zur Sprache* ist ungetestet.

## 1b. Verifikations-Gates (die Lektion, die jede Zahl tragfähig macht)

Ein Forschungsergebnis ist nur so gut wie das Gate, das es reproduziert. Diese
Session hat eine komplette Gate-Infrastruktur gebaut — nutze sie als Muster.

**Warum:** `npm run test` **existierte nicht** (`npm error Missing script:
"test"`); es gab nur `check`/`fix`/`audit:*`. Ein Gate, das es nicht gibt,
verifiziert nichts — also eins bauen statt melden.

**Das Muster** (`scripts/run_research_tests.sh`, hängt an `npm run test`):

1. **Jede Verifikation wird ein re-runnable Gate**, kein handgetippter Befehl.
2. **Reihenfolge nach Beweiskraft:** compile → Gradienten → Backward-Beweis →
   Gruppen-Axiome/Konvention → Hygiene → End-to-End-Ergebnis. `--fast`
   überspringt nur den langsamen End-to-End-Teil.
3. **Ein Gate pro Prozess** (`stage()`-Helper), damit ein Crash die anderen
   nicht maskiert; Ausgabe nur bei FAIL.
4. **Negativtest ist Pflicht:** ein Gate, das nicht scheitern *kann*, ist ein
   Gummistempel. Beweis: Schwelle temporär unmöglich setzen → muss exit != 0
   liefern (so gemacht und dokumentiert).
5. **Neue Dateien sofort ins Gate aufnehmen.** Hier lagen `s5_prior_check.py`
   und `gradcheck_flaky_probe.py` eine Weile *neben* dem Gate — ungeprüft.
6. **Einen laufenden Lauf nach einer Änderung NEU starten, nicht die alte
   Meldung glauben.** Ein Background-Prozess wurde stundenlang vor dem letzten
   Refactor gestartet; seine „32 passed"-Meldung war für den finalen Code
   wertlos. Vor dem Melden: Prozess-Startzeit gegen den mtime der geänderten
   Datei prüfen — ist der Lauf älter, gilt er nicht als Evidenz. Ebenso: eine
   gepostete Gate-Zahl ist nur dann „aktuell", wenn sie nach der letzten
   Änderung entstand.

**Drei wiederverwendbare Fehlerklassen, die die Gates fanden:**

- **Nicht-deterministische Init = die klassische stille Flake.** Ein
  `randn()`-Helper nutzte das *globale* `random` statt das übergebene `rng` →
  gleicher Seed, andere Gewichte → Gradcheck 6/6 einzeln grün, fällt in der
  Suite. **Fix:** `rng` durch jeden Init-Aufruf reichen + Determinismus-Gate
  (`seed_init_fix.py --check`) dauerhaft in der Suite.
- **Flake erst messen, dann fixen.** Die erste Hypothese (zu lockere
  1e-6-Schwelle) war **falsch** — gemessen: 0 Treffer, worst_abs 1.5e-10. Die
  echte Ursache lag woanders. Eine Schwelle zu „reparieren", die nicht die
  Ursache ist, verdeckt den Bug.
- **Ein Instrument kann kaputt sein, nicht die Konstruktion.** Ein Test mit
  eingefrorenen Gewichten + *untrainiertem* Readout misst „perfekter Zustand +
  blinder Decoder" → Zufall. Das Ergebnis war der Test, nicht das Modell. Vor
  dem Verwerfen einer Konstruktion prüfen, ob der Test sie überhaupt beweisen
  könnte.
- **AST-Hygiene als Gate: tote Namen + duplizierte Körper.** Ohne Linter, unter
  einer Sekunde — und fand in dieser Session **drei echte Defekte**:
  - **Tote Namen:** jede Top-Level-Funktion/Klasse/Methode/Konstante mit
    **genau 1 Vorkommen im Scope = nur die Definition = tot**. So gefunden:
    `gen_index`, `GEN_NAMES`, `_hard_perm`, `forward_exact_state`.
  - **Duplizierte Körper (DRY):** Body per `ast.dump` fingerprinten, vorher
    String-Literale maskieren (`ast.Constant` → `"<S>"`), sonst verhindert
    jeder abweichende Log-Text den Treffer. So wurde `choice_accuracy` **3×**
    identisch kopiert gefunden → konsolidiert zu *einer* Definition neben dem
    Modell, das sie misst.
  - **Scope-Falle (kostete einen kompletten Scan):** ein Scan über *alle*
    `scripts/` meldete ~45 Tote — fast alle **vorbestehend, in fremden
    Dateien** (`multi_monitor.py`, `self-rewriter.py`, `commander.py` …). Das
    ist Rauschen und verleitet zu einem Diff, der fremden Code anfasst. **Scan
    auf den eigenen Arbeitsbereich eingrenzen** (Dateiliste oder gemeinsames
    Präfix); danach waren es exakt die 4 echten.
  - **Nach der Konsolidierung Verhalten nachweisen, nicht nur „kompiliert":**
    dass alle Konsumenten dieselbe Funktion importieren, prüft
    `{k: getattr(mod, "fn").__module__ for k, mod in consumers.items()}` —
    genau ein Wert = eine kanonische Quelle.

  **Re-runnable Probe:** `scripts/ast-hygiene-probe.py <deine dateien/globs>…`
  (Flags `--dead`, `--dups`, `--min-body N`, `--json`; exit 1 bei Fund → als
  Gate-Stage nutzbar). **Scope = nur die eigenen Dateien** — das ist kein
  Detail, sondern der Unterschied zwischen 4 echten und 45 falschen Treffern.
  Selbsttest (prüft beide Richtungen: findet UND schweigt, und meldet **nicht**
  „clean" wenn 0 Dateien geparst wurden): `scripts/ast-hygiene-probe-selftest.py`.

**Vor jeder veröffentlichten Zahl:** live reproduzieren UND die eigene
Behauptung aktiv angreifen. Hier wurde „Konstruktion bewiesen" selbst
nachgemessen (Majority-Class-Baseline + Entropie) und danach **abgeschwächt**,
weil der Überschuss über den Prior mit der Länge fiel. Ergebnis: das Gate
`s5_prior_check.py --assert-prior` nagelt genau diese Ehrlichkeitsannahme fest.

**Die Zahlen der Publikation gegen die Messdatei abgleichen — nicht gegen das
Gedächtnis.** Jede Tabelle der Arbeit wurde per Skript gegen das gespeicherte
JSON geprüft (`paper-Wert == json-Wert`); erst das zeigt, ob die Datei die
Behauptung überhaupt belegt. Genau dabei fiel auf: das Paper zitierte die
**Parameterzahlen** (D12=4, Z10=2, A5=4, S5=8, S6=10), die
`group_scaling_results.json` aber **gar nicht speicherte** — sie kamen nur aus
der Konsolenausgabe. Fix: die Schlüssel `num_generators` + `params` in den Dump
aufnehmen, neu laufen lassen, erneut abgleichen (dann „ALLE OK"). **Wenn eine
veröffentlichte Zahl nur in der Konsole existiert, ist sie unbelegt — leg sie in
die Datendatei.**

Vollständige Methodik, Code-Muster und die gemessenen Fehlerklassen:
**`references/verification-gates.md`** (Gate-Aufbau, Determinismus-Gate,
Flake-Instrumentierung, Rubber-Stamp-Negativtest, Majority-Baseline-Pflicht).

Starter zum Kopieren: **`templates/run_research_tests.sh`** — Gate-Runner mit
`stage()`-Helper, CONFIG-Blöcken und den Stage-Plätzen in Beweiskraft-Reihenfolge.

## 1c. RSI: was die Literatur verlangt — und was hier gemessen fehlte (2026-10-11)

Vier Paper, vier konkrete Mechanismen. Jede Zeile ist eine *Anforderung*, keine
Zuschreibung. Der Vergleich gegen den eigenen Bestand ist gemessen, nicht
behauptet: `darwin/lineage.json` trug 27.211 Ereignisse mit den Feldern
`parent child kind when op` — und **kein** Feld für das Ergebnis; `rsi-stable`
stand nach **891** Rotationen bei **0 Vorschlägen**; 12 von 12 Nachkommen
bewegten den ausführbaren Term um 0.00.

| Paper | Was es verlangt |
|---|---|
| Mendel Gödel Machine (arXiv 2608.07645) | Selbstmodifikation aus EINER Trajektorie ist blind gegen „rich comparative signals in the agent's expanding **archive**" → ein Archiv |
| Red Queen Gödel Machine (2606.26294) | bestehende Suche „**assumes a stationary evaluation criterion**" → ein **ko-evolvierender** Evaluator |
| Huxley-Gödel Machine (2510.21614) | Metaproductivity-Performance Mismatch → Fitness = **Nachkommen** (CMP), nicht das Individuum |
| Self-Taught Optimizer (2310.02304) | seed improver auf sich selbst — und die Autoren nennen ihre eigene Grenze: „not full recursive self-improvement" |

**DAS GESETZ DER MESSUNG — teuer gelernt:** ein Messwert, der von selbst
wandert, kann **keine** Fitness sein. Erster Live-Lauf einer Verbesserungs-
schleife: der Wert schwankte 0.8 → 1.0 → 0.7 → 0.9 **bei unverändertem
Parameter**, und die Schleife verbuchte „+0.135" als Fortschritt. Drei Fixes:

1. **Rauschschwelle aus VIELEN Messungen** (9, nicht 3). Drei Messungen eines
   verrauschten Werts lagen zufällig 0.0104 auseinander, während die echte
   Streuung desselben Subjekts 0.2 betrug — die Schwelle war 20× zu klein.
2. **`EVALUATION_ONLY`-Parameter nie vorschlagen.** `seeds`, `samples`,
   `repeats` ändern die *Messung*, nicht das Modell; weniger Seeds ist eine
   verrauchtere Schätzung, und ein „Gewinn" daraus ist ein
   Stichproben-Lotteriegewinn.
3. **Wiederholbarkeit pro Kandidat.** Ein Kandidat, der sich nicht reproduziert,
   wird `UNSTABLE` und fliegt raus — unabhängig davon, wie gut sein Einzelwert war.

**CMP misst, ob ein Mutator überhaupt kann.** Auf einem echten Artefakt
(S_5-Gruppenzustand, Operatoren auf `range`-Schranke und Konstanten):
Samen-Fitness **0.02439**, CMP = **0.01319** — der Mutator bringt nichts
Besseres hervor als sich selbst. Das erklärt „891 Rotationen, 0 Vorschläge",
was vorher als „System stabil" fehlgedeutet worden war: nicht Stabilität,
sondern **fehlende Metaproduktivität**.

**`ast-hygiene-probe` und Protokollmethoden (gefixt 2026-10-11):** die Probe
zählt Quelltext-Vorkommen, deshalb meldete sie `__init__`/`__enter__`/`__exit__`
als tot — sie werden vom `with`-Protokoll gerufen, nie namentlich. Dunder-Namen
sind jetzt ausgenommen. Nach **jeder** Änderung an der Probe muss ihr eigener
Selbsttest laufen (`ast-hygiene-probe-selftest.py`) — er prüft beide Richtungen
und sagt „probe has teeth". **Ein Werkzeug, das Falsches meldet, lehrt Falsches.**

Vollständige Zitate, Fundstellen, der gemessene Archiv-Schemasatz und der
Bauplan zweier Schleifen: **`references/rsi-literature-and-mechanisms.md`**.

## 2. Experimentelle Aktivierungen (erfunden in neural_lab.py)

| Name | Formel | Charakteristik |
|---|---|---|
| `oa_swish` | x · sigmoid(x) · (1 + 0.1·sin(x)) | Oszillierend, negative Ausgaben möglich |
| `oa_hexp` | x>0 → gelu(x), x<0 → -0.1·e^(-x)·x² | Hybrid: GELU für positive, quadratisch-exponentiell für negative |
| `oa_ripple` | sin(x) · sigmoid(x) | Wellenförmig, periodisch |

## Neue Architekturen

**OscillatingResNet**: Residual-Blöcke mit oszillierenden Aktivierungen:
```
Input → [Ripple → Ripple → Skip-Connect]×n → Sigmoid → Output
```

## Pure-Python Backpropagation

`Layer.backward()` implementiert manuelles Backprop ohne Autograd:
- Analytische Gradienten für sigmoid, relu, gelu
- Numerische Gradienten (finite differences) als Fallback für eigene Aktivierungen
- Gewichtsupdate via SGD

## Evolutionäre Architektursuche

`evolve()` sucht nach optimalen Architekturen:
- Population von Genomen (zufällige Layer-Konfigurationen)
- Fitness: negativer MSE auf Trainingsdaten
- Selektion: Top 3 überleben, reproduzieren + mutieren

## Self-Debugging Engine (`scripts/self_debug.py`)

Scannt den eigenen Quellcode nach:
- Unused imports
- Bare except clauses
- TODO/FIXME markers
- Syntax errors

Generiert Auto-Fix-Pläne und kann als Daemon laufen.

**Nicht abgedeckt — dafür `scripts/ast-hygiene-probe.py`:** *unused imports* ist
nicht dasselbe wie **tote Namen** (definierte, nie aufgerufene Funktionen,
Methoden, Konstanten) und nicht dasselbe wie **duplizierte Funktionskörper**.
Genau diese zwei Klassen trugen in einer Session drei echte Defekte
(`_hard_perm`, `forward_exact_state`, `choice_accuracy` 3× kopiert).

## Verwendung

```bash
python scripts/neural_lab.py
python scripts/self_debug.py --scan
python scripts/self_debug.py --watch
```

## Pitfalls

- **Pfade**: Path("/c/...") funktioniert auf Windows nicht — r"C:\..." nutzen
- **MSYS/bash**: subprocess.run braucht POSIX-Pfade: replace("\\","/").replace("C:","/c")
- **CPU-only**: Training ist langsam — starte mit 2-3 Layern, <10 Neuronen