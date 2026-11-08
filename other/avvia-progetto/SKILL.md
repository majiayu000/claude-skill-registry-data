---
description: Avvia un progetto nuovo. Fa in sequenza le domande di avvio del template, una per messaggio, e compila il CLAUDE.md del progetto con le risposte. Si lancia solo su richiesta, in una cartella di progetto vuota o appena creata.
argument-hint: [nome-progetto]
disable-model-invocation: true
---

# Avvio progetto

Rispondi in italiano. Una sola domanda per messaggio, mai elenchi di domande.

1. Leggi il file di avvio del template: `avvio-progetto.md`, nella cartella del template indicata dalla variabile d'ambiente `KIT_CONFIG_TEMPLATE_DIR` (in `_template/avvio-progetto.md`). Se la variabile non è impostata o il file manca, dillo e fermati.
2. Segui le domande di quel file nell'ordine indicato. Per ogni risposta registra il valore; non assumere nulla che l'utente non ha detto.
3. Quando hai tutte le risposte, mostra il riepilogo e chiedi conferma prima di scrivere.
4. Dopo l'ok, compila `CLAUDE.md` nella radice del progetto con le risposte, nei campi del modello. Non scrivere valori reali di segreti: solo segnaposto.
5. Segnala i moduli di regole da copiare: non copiarli qui, usa `/kit:copia-regole`.
6. Non creare commit e non modificare altri file.
