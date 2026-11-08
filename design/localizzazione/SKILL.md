---
description: Controlla o imposta il layout di un progetto perché regga testi tradotti più lunghi, l'orientamento RTL, l'ordine di lettura e lo zoom. Non modifica file. Si lancia solo su richiesta.
argument-hint: [cartella-progetto]
disable-model-invocation: true
---

# Layout e localizzazione

Rispondi in italiano. Una sola domanda per messaggio.

Questa skill verifica o imposta il layout perché tenga con le lingue supportate dal progetto (in `CLAUDE.md`, voce «Lingue supportate»). La localizzazione (chiavi di traduzione, lingua di default) e le date stanno in `frontend.md` §4.2 e §4.3: qui si applica la procedura di layout.

1. Leggi il layout dei componenti principali e le chiavi di traduzione. Se le lingue supportate non sono chiare, chiedi una sola domanda prima di continuare.
2. Raggruppa con lo spazio più che con linee divisorie. Le linee servono solo dove lo spazio non basta a distinguere due gruppi.
3. Tieni distinti i controlli dal contenuto: un controllo ha un contorno o uno sfondo riconoscibile anche senza bordo visibile, e il contorno rispetta il contrasto di `colori-tema` (WCAG 2.2, 1.4.11).
4. Allinea gli elementi a bordi condivisi: stesso margine sinistro (o di inizio, in RTL) per titolo, testo e campi di una stessa colonna.
5. Per gli elementi che si specchiano in RTL usa proprietà logiche (`margin-inline`, `padding-block`, `inset-inline-start`) al posto di quelle fisiche (`left`, `right`). Verifica l'attributo `dir` sul documento e l'attributo `lang` sul contenuto tradotto.
6. Ordine di lettura: il DOM segue l'ordine visivo, anche in RTL e dopo un reflow (WCAG 2.2, 1.3.2). Un ordine visivo ottenuto solo con CSS è una segnalazione.
7. Testo che si espande: ogni etichetta, pulsante e titolo ha spazio per una traduzione più lunga. Il testo che può superare lo spazio va a capo oppure viene troncato con una via d'uscita (tooltip, pagina di dettaglio), mai tagliato senza modo di leggerlo.
8. Reflow: il contenuto si legge a 320 px di larghezza senza scorrimento orizzontale, e a zoom del 200% senza perdita di contenuto (WCAG 2.2, 1.4.10 e 1.4.4).
9. Contenuto nascosto (pannelli, menu, sezioni espandibili): lo stato è dichiarato (aperto o chiuso) e c'è sempre un controllo per aprirlo (WCAG 2.2, 4.1.2).
10. Crescita: nessuna altezza fissa per blocchi di testo; i contenitori crescono con il contenuto (`min-height`, `max-width`, non `height` su testi).
11. Chiudi con l'elenco dei componenti controllati e, per ciascuno, il problema trovato o «ok». Le modifiche al codice non si fanno da questa skill: si propongono, e si applicano con una richiesta separata.

Riferimenti: `frontend.md` §4.2 e §4.3; WCAG 2.2, criteri 1.3.2, 1.4.4, 1.4.10, 1.4.11 e 4.1.2.
