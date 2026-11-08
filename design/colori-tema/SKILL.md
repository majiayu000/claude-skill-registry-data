---
description: Costruisce o verifica la palette di un progetto con token semantici per i temi chiaro e scuro, e controlla il contrasto sui valori resi. Non modifica file. Si lancia solo su richiesta.
argument-hint: [cartella-progetto]
disable-model-invocation: true
---

# Colori del tema

Rispondi in italiano. Una sola domanda per messaggio.

Questa skill costruisce o verifica la palette del progetto. Il vincolo obbligatorio (niente colori fissi nei componenti, token CSS, multi-tema) sta in `frontend.md` §3 e §4.1: qui si applica la procedura.

1. Leggi i token esistenti: le variabili CSS in `:root` e nel tema scuro, e i colori usati nei componenti. Se non ci sono token, chiedi una sola domanda: colore primario e sfondo di partenza.
2. Assegna a ogni colore un ruolo: sfondo, superficie, bordo, testo, testo secondario, azione primaria, azione secondaria, stato (errore, avviso, successo), focus. I token si nominano per ruolo (per esempio `--color-text-muted`), mai per tinta (per esempio `--blue-500`) nei componenti.
3. Costruisci per ogni tinta una scala di passi. Ogni passo ha una funzione, e non si aggiungono passi per sfumature che nessun ruolo usa. Il tema chiaro e il tema scuro usano la stessa tinta, con passi scelti per la stessa funzione.
4. Un colore, un significato: se due ruoli usano lo stesso valore, verifica che il significato sia lo stesso; altrimenti separa i token.
5. Misura il contrasto sui valori resi, in ogni coppia del tema chiaro e del tema scuro, dopo overlay e trasparenze:
   - testo normale: almeno 4,5:1 (WCAG 2.2, 1.4.3);
   - testo grande (almeno 24 px, oppure 18,66 px in grassetto): almeno 3:1 (WCAG 2.2, 1.4.3);
   - bordi di componenti, icone funzionali, indicatori di stato e contorno di focus: almeno 3:1 contro lo sfondo adiacente (WCAG 2.2, 1.4.11).
6. Il colore non è l'unico segnale: ogni stato (errore, avviso, successo) ha anche un testo o un'icona (WCAG 2.2, 1.4.1).
7. Gradienti: dichiara lo spazio di interpolazione (per esempio `in oklch`). Verifica il contrasto nei punti del gradiente su cui sta del testo.
8. Chiudi con una tabella delle coppie: ruolo, tema, colore di primo piano, colore di sfondo, rapporto, soglia, esito. Le coppie che non passano restano segnalate, con il valore più vicino che passa la soglia, da confermare con l'utente prima di cambiarlo.

Riferimenti: `frontend.md` §3 e §4.1; WCAG 2.2, criteri 1.4.1, 1.4.3 e 1.4.11.
