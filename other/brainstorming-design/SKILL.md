---
name: brainstorming-design
description: Allinea con l'utente sul design prima di scrivere codice, per task non banali. Da usare quando l'utente chiede una nuova feature, un nuovo progetto, una nuova presentazione didattica, un refactoring architetturale, o quando il task ha più strade plausibili. NON da usare per fix puntuali, edit minimi, o task con istruzioni già esplicite.
---

# Brainstorming e design approval

**Principio**: per task non banali, allineati sul design prima di scrivere codice. Una domanda chiara ora evita un refactor domani.

## Quando si attiva

✅ Sì:
- Nuova feature di rilievo (es. "aggiungi sistema notifiche push", "implementa OAuth")
- Nuovo progetto / nuova app
- Nuova presentazione didattica (struttura, target, livello dettaglio)
- Refactoring architetturale che tocca più moduli
- Task con 2+ strade plausibili e trade-off reali
- Modifiche che impattano API pubbliche o schema DB

❌ No:
- Bug fix puntuale
- Edit minimo già specificato dall'utente
- Aggiunta di una singola slide a una presentazione esistente
- Task con istruzioni già operative ("rinomina X in Y", "aggiungi questa funzione qui")

## Processo

### 1. Esplora contesto (silenzioso)
Prima di chiedere, leggi:
- File rilevanti del progetto
- `project-memories/<progetto>.md` se esiste
- Commit recenti (`git log --oneline -10`)
- Pattern simili già usati nel codebase

Questo evita di chiedere all'utente cose già visibili nel codice.

### 2. Domande di chiarimento (mirate, non a raffica)

Chiedi UNA cosa alla volta, preferibilmente con AskUserQuestion + opzioni concrete:
- Scopo: cosa risolve, per chi
- Vincoli: tempo, budget complessità, dipendenze già presenti
- Criterio di successo: come riconosciamo "fatto bene"

❌ Non fare interrogatori da 8 domande in un colpo.
✅ 2-3 domande chiave bastano per il 90% dei casi.

### 3. Proponi 2-3 approcci con trade-off

Per ogni approccio:
- Cosa cambia
- Pro / contro
- Effort stimato (S/M/L)
- Quale raccomandi e perché

Non proporre 5 alternative — l'utente non ha tempo di valutarle tutte. 2-3 è il giusto compromesso.

### 4. Presenta il design scelto

Suddiviso in sezioni leggibili. Per progetti grandi, chiedi approvazione sezione per sezione invece che presentare un wall of text.

### 5. Persisti il design se serve

Per progetti che durano più sessioni, salva la decisione in:
- `project-memories/<progetto>.md` (sezione "Design decisions")
- Un commit `docs:` con il razionale

### 6. Passa all'implementazione

Solo dopo approvazione esplicita.

## Anti-pattern

- Iniziare a scrivere codice prima di aver capito il "perché"
- Fare 10 domande prima di leggere il codice esistente
- Proporre design troppo dettagliato (livello di nome variabili) prima dell'approvazione architetturale
- Ignorare i pattern già consolidati nel KB / project-memory
- Inventare requisiti non chiesti ("metterò anche un sistema di logging", "aggiungo i18n")

## Caso speciale: presentazioni didattiche

Per nuove presentazioni della didattica ITIS, allineati prima su:
- Target (anno, livello, prerequisiti)
- Tecnologia (CDN-only, Vite+TS, Marp)
- Durata stimata (numero slide / minuti lezione)
- Tono (formale, interattivo, esempi pratici)

Esiste già il pattern `educational-presentation-skill` — applicalo invece di reinventare.
