---
name: "source-command-handoff-figma"
description: "Handoff su FIGMA per Gravity MVP. Raccoglie user story, lingua e ruoli, esplora il prototipo HTML, identifica le schermate del flusso, costruisce ogni schermata su Figma usando componenti della libreria o template atomici custom. (Per l'handoff HTML interattivo con barra dev + tour + note usa invece handoff.)"
---

# source-command-handoff-figma

Use this skill when the user asks to run the migrated source command `handoff-figma`.

## Command Template

# Handoff Gravity — Costruisci Flusso

Segui questo flusso nell'ordine esatto. Non saltare nessun passo.

---

## FASE 1 — Raccolta informazioni

Prima di toccare Figma, chiedi all'utente tutte le informazioni necessarie in un'unica risposta strutturata:

**Domanda 1 — File di destinazione**
In quale file Figma devo lavorare? Fornisci l'URL del file (e la pagina specifica, se ce n'è una).

**Domanda 2 — User Story**
Elenca le user story da disegnare. Per ognuna fornisci:
- Numero (es. US#01)
- Titolo breve
- Descrizione narrativa del flusso: chi fa cosa, in quale contesto, step per step
- Ruolo/i coinvolti (vedi lista sotto)

**Domanda 3 — Lingua**
In che lingua vanno scritti tutti i testi del canvas? (italiano / inglese / altra)

**Domanda 4 — Prototipo HTML** *(opzionale ma molto utile)*
Hai un prototipo HTML che implementa questo flusso? Se sì, fornisci il percorso del file (es. `prototype/03-inventory/index.html`) oppure aprilo nel browser e condividi l'URL locale. Lo userò per individuare le schermate reali del flusso prima di costruire su Figma.

**Domanda 5 — Diagramma di flusso** *(opzionale)*
Hai un diagramma di flusso (Figma, FigJam, immagine, o testo strutturato) che descrive la logica del flusso con branch, condizioni e percorsi alternativi? Se sì, condividi l'URL o il percorso.

**Ruoli supportati da Gravity:**
| Ruolo | Colore label |
|-------|-------------|
| Tenant Admin | blu `#1677FF` |
| Inventory Manager | cyan `#13C2C2` |
| Sales | arancione `#FF4A1C` |
| Operation Manager | verde `#52C41A` |
| Planner | viola `#722ED1` |

Aspetta le risposte prima di procedere.

---

## FASE 2 — Individuazione schermate del flusso

Carica obbligatoriamente la skill `figma:figma-use` prima di qualsiasi chiamata `use_figma`.

### 2a. Esplora il prototipo HTML (se fornito)
- Leggi il file con `Read` per capire la struttura dei componenti e gli stati UI implementati
- Naviga il prototipo via Playwright (`mcp__playwright__browser_navigate` + `browser_snapshot`) percorrendo l'happy path e i percorsi alternativi click by click
- Prendi screenshot di ogni stato distinto

### 2b. Inventario schermate
Produce un elenco numerato di tutte le schermate del flusso:
- Schermate principali (ogni vista che occupa tutto lo schermo)
- Layer in sovrapposizione: modali, drawer, tooltip, popover, notifiche
- Stati alternativi della stessa schermata (es. lista vuota vs lista popolata, form vuoto vs form in errore)

Per ogni schermata annota:
- Nome descrittivo (es. "Lista spazi — popolata")
- Tipo di layer: `schermata` / `modale` / `drawer` / `overlay`
- Schermate su cui appare (per modali e drawer)

**Non procedere finché l'inventario non è completo.**

---

## FASE 3 — Classificazione layout e assegnazione template

Per ogni schermata principale (non overlay), classifica il layout e assegna il template di riferimento.

**File template:** `WqdTtaemaAOLk8eOfhEV1I` (Shaker UI — Components)
**Container:** node `2529:56483` (frame "Template Screen")

| Tipo | Node Figma | Caratteristiche | Struttura |
|------|-----------|----------------|-----------|
| **Lista** | `2529:56461` | Tabella o lista di item, filtri, paginazione, azioni bulk | Navbar → Header (titolo + azioni CTA) → Tabella/Lista |
| **Dettaglio** | `2529:68281` | Vista singolo record, sezioni informative, azioni contestuali | Navbar → Header (back + titolo soggetto + CTA) → 4 System Cards → Tabs + slot contenuto |
| **Ibrida** | `2529:56484` | Lista principale + sidebar contestuale | Navbar → Header (back + titolo + CTA) → Sidebar sinistra 320px (System Cards + Calendar) + area destra flessibile |
| **Dashboard** | — | KPI, grafici, widget multipli | Template in arrivo — costruire atomicamente fino ad allora |

### Struttura dettagliata dei template

**Type=Detail (`2529:68281`)**
- `Navbar` — menu orizzontale + avatar + bell
- `HeaderDetailScreen` — sx: link "Back to list" + titolo "Detail Screen | Subject Name"; dx: Button primary
- Row di 4 `System Cards` affiancate (1/4 larghezza ciascuna) — KPI con icona, label, valore
- `*Tabs* / Container` — barra tab (type=card) + slot "Slot component" espandibile

**Type=Hybrid (`2529:56484`)**
- `Navbar` — identica al Detail
- `HeaderDetailScreen` — identica al Detail
- Layout 2 colonne:
  - Sinistra `Sidebar/Planning` (320px fissi): System Cards verticali + `Calendar` (Exposure Period con range date evidenziato)
  - Destra `Table Card Wrapper` (flex-1): area bianca per tabella o contenuto principale

**Type=List (`2529:56461`)**
- Usa `get_design_context` su questo nodo per ispezionare la struttura prima di usarlo

Riporta la classificazione all'utente prima di procedere.

---

## FASE 4 — Loop per schermata (ripeti per ogni schermata nell'ordine dell'inventario)

Per ogni schermata, esegui questi step in sequenza:

### Step 1 — Mappatura componenti → libreria Figma

Analizza la schermata (da HTML/screenshot) e produce una lista di tutti i componenti presenti con il loro corrispondente Figma dalla libreria **Ant Design System for Gravity** (`uR6CBOh0Y7dUQvH30SyD0P`).

Formato:
```
- [ComponenteReact] → *NomeFigma* (varianti: Prop=Valore, ...)
  es. <Button type="primary"> → *Button* (Type=Primary, Size=Default, State=Default)
```

Per componenti non presenti in libreria: annota "custom — costruire atomicamente" e specifica da quali particelle (Avatar, Button, Text, ecc.).

Usa la mappa React→Figma in AGENTS.md come riferimento principale.

### Step 2 — Disegno su Figma

Costruisci la schermata nel file Figma usando `use_figma`:
- **Prima scelta:** duplica il template corrispondente (vedi FASE 3) dal file `WqdTtaemaAOLk8eOfhEV1I` e adattalo per la schermata corrente
- **Se nessun template corrisponde:** costruisci un frame custom usando i componenti atomici del design system (Button, Text, Avatar, Icon, ecc.) — mai valori hard-coded, sempre token Gravity
- Rispetta la struttura di layout classificata al FASE 3 (colonne, spacing, gerarchia)
- Usa lo spacing del design system: `8px` base unit, multipli di 4/8/16/24/32/48px
- Dimensioni schermata standard: **1728 × 1117px**, sfondo `#F5F5F5`

### Step 3 — Iterazioni manuali

Dopo aver piazzato la struttura principale, elenca le rifiniture necessarie e applica quelle realizzabili via `use_figma`. Per quelle che richiedono intervento manuale (es. allineamenti complessi, auto layout annidati profondi), segnalale esplicitamente all'utente con descrizione precisa di cosa aggiustare.

### Step 4 — Compilazione con dati mock

Popola tutti i testi e i campi della schermata con dati realistici coerenti con il dominio OOH/DOOH di Gravity:
- Nomi spazi: "Billboard Palermo Centro", "Schermo LED Via Roma 12", "Pensilina Bus Politeama"
- Campagne: "Campagna Primavera 2026 — TIM", "Awareness Q2 — Vodafone"
- Date nel formato `DD/MM/YYYY`
- Budget in euro (es. `€ 12.400`, `€ 8.750`)
- Indirizzi siciliani/palermitani quando contestuali

Non lasciare placeholder "Lorem ipsum" o "Label" generici.

### Step 5 — Traduzione

Traduci **tutti** i testi dell'interfaccia nella lingua scelta in FASE 1 (se inglese: label, titoli, voci di menu, placeholder, messaggi di stato). I dati mock (nomi propri, indirizzi) possono rimanere contestuali.

Dopo la traduzione, fai uno screenshot di verifica della schermata completata.

---

## FASE 5 — Costruzione overlay (modali e drawer)

Dopo aver completato tutte le schermate principali, disegna i layer in sovrapposizione seguendo gli stessi step 1–5 del FASE 4.

Per ogni overlay:
- Piazzalo sopra la schermata su cui appare nel flusso reale
- Usa `*Modal*`, `*Drawer*` dalla libreria con le varianti corrette
- Se il contenuto dell'overlay è un form o una lista, mappa i suoi componenti separatamente

---

## FASE 6 — Struttura canvas e annotazioni

Dopo aver completato tutte le schermate e gli overlay:

### 6a. Disposizione del flusso
- Disponi le schermate **in sequenza orizzontale** nell'ordine del flusso, con gap 80px
- Aggiungi frecce `→` tra le schermate con etichetta dell'azione che le collega (es. "Clic su Crea campagna")
- Posiziona gli overlay sovrapposti (o affianati con freccia tratteggiata) rispetto alla schermata che li attiva

### 6b. Annotazioni
Aggiungi Post-it gialli (`#FFF7CD`) sopra ogni schermata per:
- Regole di business ("Solo se ruolo = Sales", "Richiede almeno 1 spazio selezionato")
- Condizioni di branching
- Vincoli tecnici da comunicare al developer

### 6c. Panel US + User (facoltativo se richiesto dall'utente)
Se il file di destinazione usa la struttura handoff con Section e pannello sinistro, aggiungi:
- Label verticale colorata con il colore del ruolo
- Nome ruolo + avatar
- Numero e titolo US
- Descrizione narrativa

**Mappatura ruolo → colore:**
```
Tenant Admin      → #1677FF
Inventory Manager → #13C2C2
Sales             → #FF4A1C
Operation Manager → #52C41A
Planner           → #722ED1
```

---

## FASE 7 — Validazione finale

1. Screenshot panoramico del flusso completo
2. Verifica:
   - Tutte le schermate dell'inventario sono presenti
   - Tutti i testi sono nella lingua corretta
   - Nessun placeholder generico
   - I dati mock sono coerenti tra le schermate (stessi nomi, stesse date)
3. Riporta all'utente:
   - Elenco schermate costruite (con node ID e URL diretto)
   - Componenti custom creati (non da libreria)
   - Rifiniture manuali ancora necessarie (lista precisa)

---

## Note operative

- **Token sempre, valori hard-coded mai**: usa sempre i token Gravity (`#3E00FB`, `rgba(0,0,0,0.88)`, ecc.) — non colori arbitrari.
- **Lingua coerente**: tutti i testi nella lingua scelta — non mescolare.
- **Dati mock realistici**: OOH/DOOH siciliano, non Lorem ipsum.
- **Ordine fisso**: completa una schermata per volta (mapping → draw → iterazioni → mock → translate) prima di passare alla successiva.
- **Overlay dopo le schermate**: disegna modali e drawer solo dopo aver completato tutte le schermate principali.
