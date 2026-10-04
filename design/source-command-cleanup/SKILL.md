---
name: "source-command-cleanup"
description: "Pulisce il codice di un prototipo HTML prima dell'handoff su Figma. Rimuove logica morta, stati orfani e riferimenti a feature rimosse, poi genera un brief testuale da passare a Codex Design."
---

# source-command-cleanup

Use this skill when the user asks to run the migrated source command `cleanup`.

## Command Template

# Cleanup Prototype — Preparazione Handoff Figma

Segui questo flusso nell'ordine esatto. Non saltare nessun passo.

---

## FASE 1 — Identificazione del file

Se l'utente non ha specificato il file, chiedi:
> "Su quale prototipo devo fare il cleanup? Fornisci il percorso (es. `prototype/planning/index.html`) oppure dimmi il nome del prototipo."

Leggi il file con `Read` prima di procedere.

---

## FASE 2 — Audit del codice morto

Analizza il file e costruisci una lista di tutto il codice che non corrisponde a nulla di visibile o raggiungibile nel browser. Cerca in modo sistematico:

**Stati React inutilizzati**
- `useState` dichiarati ma non letti in nessuna espressione JSX né in nessuna funzione chiamata dal render

**Funzioni e componenti inutilizzati**
- Funzioni definite ma mai chiamate
- Componenti React definiti ma mai renderizzati
- Handler di eventi collegati a elementi non più presenti nel render

**Props orfane**
- Props passate a un componente che non le dichiara nei parametri
- Props dichiarate nei parametri di un componente ma non usate nel suo body

**Condizioni impossibili**
- Condizioni su valori di stato che non possono più essere veri (es. `step === 3` se `step` va da 1 a 2, `mode === 'old-mode'` se quel valore non viene mai impostato)
- Rami `if/else` o ternari il cui branch non è mai raggiungibile

**Dati mock con strutture orfane**
- Campi in oggetti dati (es. array di impianti) che non compaiono in nessuna colonna, nessun render, nessuna funzione attiva

**Commenti con riferimenti a feature rimosse**
- Commenti che nominano schermate, step, flussi o componenti non più presenti

**Costanti e variabili inutilizzate**
- `const` o `let` definiti a livello di modulo ma non referenziati altrove

---

Presenta la lista all'utente in questo formato prima di toccare qualsiasi cosa:

```
Ho trovato [N] elementi da rimuovere:

STATI
- [nome stato] — motivo (es. "non compare in nessun render")

FUNZIONI / COMPONENTI
- [nome] — motivo

PROPS ORFANE
- [ComponenteName]: prop `[nomeProp]` — motivo

CONDIZIONI IMPOSSIBILI
- riga [N]: `[condizione]` — motivo

DATI MOCK
- campo `[nomeCampo]` in [nomeArray] — motivo

COMMENTI
- riga [N]: "[testo commento]" — motivo

COSTANTI / VARIABILI
- [nome] — motivo
```

Se non trova nulla: "Nessun codice morto rilevato. Il file è già pulito."

Chiedi conferma:
> "Procedo con il cleanup?"

Aspetta risposta prima di modificare qualsiasi file.

---

## FASE 3 — Pulizia

Rimuovi gli elementi confermati nell'ordine seguente:

1. Componenti React interi non più usati
2. Funzioni non più chiamate
3. Props orfane (dalla firma del componente e dai punti in cui vengono passate)
4. `useState` inutilizzati
5. Condizioni impossibili (semplifica il ramo sopravvissuto)
6. Campi orfani negli oggetti dati mock
7. Commenti con riferimenti a feature rimosse
8. Costanti e variabili inutilizzate

**Regola:** non modificare nulla che sia visibile nel browser. Il cleanup non deve cambiare l'output visivo di nessuna schermata.

---

## FASE 4 — Verifica browser

Dopo aver salvato le modifiche, chiedi conferma esplicita all'utente:

> "Ho completato il cleanup. Apri il prototipo nel browser e verifica che l'interfaccia sia identica a prima. Dimmi quando hai controllato."

Aspetta la conferma prima di procedere. Se l'utente segnala differenze, analizza cosa è cambiato e correggi prima di andare avanti.

---

## FASE 5 — Brief per Figma

Analizza il file pulito e genera un testo da copiare, strutturato così:

```
## Prototipo: [nome cartella]

### Viste disponibili
[Elenca ogni vista/schermata con il suo nome e una riga descrittiva di cosa mostra]

### Flusso
[Descrivi la sequenza di interazioni: da dove parte l'utente, cosa può fare, come si muove tra le viste]

### Componenti e interazioni principali
[Elenca i componenti chiave e le interazioni presenti: drawer, modal, filtri, tabelle, mappe, ecc.]

### Dati mostrati
[Elenca i campi/colonne visibili e la struttura dei dati mock]

### Note per il trasferimento su Figma
[Eventuali dettagli rilevanti: colori usati per gli stati, icone custom, logica dei filtri, ecc.]

### Cosa NON è presente (rimosso in sessioni precedenti)
[Elenca esplicitamente le feature/schermate rimosse, così Codex Design non le reinferisce dal codice]
```

Presenta il brief con un'intestazione chiara:
> "Ecco il brief da incollare come primo messaggio a Codex Design:"

---

## FASE 6 — Commit

Mostra un riepilogo delle modifiche effettuate:

```
Modifiche apportate:
- Rimossi [N] stati inutilizzati
- Rimossi [N] componenti/funzioni
- Rimosse [N] props orfane
- Semplificate [N] condizioni impossibili
- Rimossi [N] campi dati orfani
- Rimossi [N] commenti obsoleti
```

Poi di':
> "Quando sei pronta, dimmi 'committa' e creo il commit di cleanup."

Aspetta il via esplicito. Il messaggio di commit da usare:
```
chore: cleanup codice morto prima dell'handoff Figma
```
