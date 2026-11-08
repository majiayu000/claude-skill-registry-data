---
description: Revisiona i test di un progetto o di un diff cercando test che danno falsa sicurezza, test fragili e duplicati, e propone come scrivere test xUnit parametrici e leggibili. Non modifica file. Si lancia solo su richiesta.
argument-hint: [cartella-o-file]
disable-model-invocation: true
---

# Qualità dei test

Rispondi in italiano. Una sola domanda per messaggio.

Questa skill revisiona i test e segnala i problemi, con una gravità per ciascuno. Le regole di base (livelli di test, dati indipendenti, nessun `skip`) stanno in `core.md` §4 e `backend-app.md` §4.5: qui si applica la procedura di revisione.

1. **Ambito.** Individua i file di test nella cartella o nel diff indicato. Se l'ambito non è chiaro, chiedi una sola domanda prima di cominciare.
2. **Falsa sicurezza (gravità alta).** Segnala i test che non possono fallire o che verificano meno di quanto dicono:
   - nessuna asserzione, o solo asserzioni che sono sempre vere;
   - asserzioni su valori che il test stesso ha prodotto, senza collegamento con il comportamento;
   - test che ripetono la logica dell'implementazione invece di verificarne il risultato;
   - eccezioni attese con un tipo troppo generico, che accetta errori diversi da quello previsto.
3. **Fragilità (gravità media).** Segnala i test che dipendono da:
   - l'ordine di esecuzione o dai dati lasciati da altri test;
   - l'ora corrente o il fuso orario della macchina (vedi `backend.md` §9: `TimeProvider` per test deterministici);
   - attese arbitrarie: `Task.Delay`, `Thread.Sleep` (già bloccati dal guard, vedi `core.md` §4);
   - risorse condivise tra test, come file, porte o database.
4. **Duplicati e manutenibilità (gravità bassa).** Quando più test differiscono solo per i dati, proponi un test parametrico con `[Theory]` e `[InlineData]`, o `[MemberData]` per dati complessi. Un test per concetto: più asserzioni sono accettabili se verificano lo stesso risultato.
5. **Nomi e asserzioni.** Il nome del test dice il comportamento verificato e la condizione, per esempio `Sconto_applicato_quando_il_totale_supera_la_soglia`. Le asserzioni sono specifiche: uguaglianza su valori attesi, non solo «non è nullo». Dove la libreria lo permette, usa asserzioni con messaggio leggibile.
6. **Isolamento.** Nei test unitari le dipendenze sono sostituite, senza database. Nei test di integrazione i dati sono creati dal test stesso con builder o fixture (`core.md` §4).
7. **Esito.** Chiudi con un elenco per gravità: il file, la riga, il problema e la correzione proposta. Non modificare i file: le correzioni si applicano con una richiesta separata.

Riferimenti: `core.md` §4; `backend-app.md` §4.5; `backend.md` §9 (tempo).
