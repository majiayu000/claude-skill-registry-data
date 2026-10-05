---
name: debugging-sistematico
description: Risolvi un bug, errore o comportamento inatteso trovando la causa radice prima di proporre fix. Da usare quando l'utente segnala un errore, un test che fallisce, un comportamento sbagliato, una regressione, o quando ci sono già stati 2+ tentativi di fix che non hanno funzionato. NON da usare per nuove feature o refactoring.
---

# Debugging sistematico

**Principio**: la causa radice prima del fix. I fix sui sintomi falliscono.

## Quando si attiva questa skill

- L'utente segnala un errore, eccezione, stack trace, test fallito, comportamento inatteso
- Una funzione "non funziona", "non parte", "dà errore"
- Sono già stati tentati 2+ fix senza successo → STOP e riparti dalla fase 1
- Una regressione (prima funzionava, ora no)

## Le 4 fasi

### 1. Investigazione causa radice

Prima di proporre QUALSIASI fix:

- Leggi l'errore per intero (stack trace completo, non solo la prima riga)
- Riproduci il bug in modo consistente — se non lo riproduci, non lo hai capito
- Controlla i commit recenti (`git log --oneline -20`, `git diff HEAD~5`) per identificare la regressione
- Traccia il flusso dei dati **a ritroso** dall'errore fino alla sorgente
- Attraversa i confini di sistema: frontend → API → DB, app → servizio → log

### 2. Analisi del pattern

- Cerca un esempio funzionante simile nel codebase (`grep` per pattern simili)
- Confronta riga per riga le differenze
- Identifica le dipendenze (versioni pacchetti, env vars, config files, ordine di inizializzazione)

### 3. Ipotesi e test

- Formula UNA ipotesi specifica e falsificabile ("se cambio X, il bug sparisce perché Y")
- Testa cambiando UNA sola variabile alla volta
- Verifica il risultato prima di procedere

### 4. Implementazione

- Se possibile, scrivi prima un test che fallisce
- Applica UN fix che indirizzi la causa radice
- Verifica che il fix risolva il problema E che non rompa altro

## Red flag che richiedono restart dalla fase 1

Se ti senti pensare:
- "Fix veloce per ora, indagine dopo"
- "Provo a cambiare X e vediamo"
- "Aggiungo un try/catch per nascondere l'errore"
- "Il problema sembra essere..." (senza prove)

→ Torna alla fase 1.

## Stop rule

**Se 3 fix consecutivi falliscono**, ferma i tentativi e metti in discussione l'architettura o le tue assunzioni di base. È un sintomo di problema strutturale, non di bug isolato.

## Anti-pattern da evitare

- Cambiare codice "per vedere se funziona"
- Commentare codice che dà fastidio invece di capire perché
- Aggiornare dipendenze sperando che il bug sparisca
- Suggerire all'utente "prova a riavviare" senza diagnosi
- Dichiarare risolto senza eseguire il caso di riproduzione
