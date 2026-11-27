---
name: revisione
description: >-
  Rilegge le sessioni di Claude Code della persona con Arturo e propone cosa migliorare: lavori ripetuti
  senza una skill, attriti che tornano, igiene (memoria, omonimi, todo, audit) e consolidamenti. Ogni
  proposta porta le prove. Le proposte scelte partono verso chi mantiene Arturo solo dopo il sì
  sull'anteprima. Per chi mantiene Arturo rivede prima le segnalazioni ricevute e aggiunge le funzioni nuove.
when_to_use: >-
  Usa con /revisione, o quando la persona chiede "rivedi come uso Arturo", "cosa posso migliorare",
  "cosa non funziona nel mio modo di lavorare con te", "fai una revisione generale". Non per la review del
  codice di un progetto (/code-review), non per controllare la config (/system-audit), non per mandare
  un problema singolo (/segnala).
argument-hint: "[giorni, di default 30]"
---

# /revisione

La persona chiede ad Arturo di guardare come lo ha usato e di proporre cosa migliorare. Lo script estrae e
conta. Il giudizio lo dai tu. Chi ti parla **potrebbe non essere una persona tecnica**: parla semplice.

`A` è il comando di Arturo (`python3 ~/.claude/bin/arturo`; col plugin `python3 "$ARTURO_CODICE/bin/arturo"`).
`S` è una cartella nuova nello scratchpad della sessione (il percorso sta nel prompt di sistema).

## 0. Chi la chiede

```bash
test -f ~/.claude/personale/revisione-sviluppatore.md && echo SVILUPPATORE || echo PERSONA
```

Con `SVILUPPATORE` leggi quel file per intero con Read e seguilo: dice come rivedere prima le segnalazioni
ricevute, come leggere l'uso anche da altre macchine e dove vanno le proposte. Torna a questi passi solo
dove il file te lo dice. Con `PERSONA` vai avanti da qui.

## 1. Estratto, sintesi, igiene, registro

```bash
D="$ARGUMENTS"; D="${D:-30}"
$A revisione estrai --giorni "$D" -o "$S"
$A revisione sintesi "$S"
$A revisione igiene
$A revisione registro
```

Leggi la sintesi, poi ogni `estratto-N.md` per intero con Read. Ogni sessione è `## Sn · data · cartella · id`,
poi gli eventi in ordine:
- i prompt della persona; uno corto porta `⟵ dopo Claude: "…"`, la fine del messaggio a cui rispondeva;
- gli slash con gli argomenti, e `[!]` per un comando che la persona ha lanciato lei col `!`;
- `[interrotto con Esc]` e `[rifiutato]`: attriti della persona, a volte col motivo;
- `[bloccato dal classificatore]` col motivo;
- i due "senza verdetto" non sono un giudizio di rischio. `[senza verdetto, hook dopo la revisione]` è un hook che cambia il comando: un difetto della config;
  `[classificatore giù, …]` è un guasto passeggero del server. Molti nello stesso minuto, in più sessioni o
  su più macchine, sono lo stesso guasto: non diventano una proposta;
- `[mod]`: un prompt scritto da un mod, non dalla persona;
- `comandi falliti`: errori di Claude, non della persona. Non attribuirli a lei.

Il registro dice cosa è già stato proposto: una proposta rifiutata non torna senza un fatto nuovo, e una
correzione accettata che si ripresenta è il segnale più forte.

## 2. Cosa cercare

Quattro famiglie. Una proposta nasce da un fatto ripetuto in almeno due sessioni diverse. Il caso singolo
resta fuori, salvo un errore di Arturo con la causa certa.
- **Ottimizzazione**: lo stesso lavoro chiesto più volte con le stesse spiegazioni, senza una skill che lo
  copra; una skill che non parte da sola e che la persona deve nominare; un passo che la persona fa a mano
  col `!` perché Claude non ci riesce. Per un lavoro ripetuto senza skill proponi `/creaskill`, con
  `chi: tu`: le spiegazioni che la persona ha già dato nelle sessioni sono le risposte alle sue domande.
- **Problema**: lo stesso attrito che torna (Esc, rifiuti, correzioni sulla stessa cosa, un blocco del
  classificatore su un lavoro legittimo), oppure un comando di Arturo che fallisce in più sessioni.
- **Igiene**: le righe di `igiene` (note doppie o con link rotti, note "scrivi come X", omonimi, todo fermi
  o scaduti, avvisi del system-audit, un CLAUDE.md troppo lungo). La riga `skill tue` conta le skill
  della persona senza "Finito quando": `/creaskill <nome>` aggiunge la lista con una domanda sola.
- **Consolidamento**: due skill, due note o due regole che fanno la stessa cosa; una regola del CLAUDE.md
  che ripete il metodo di Arturo.

Un blocco su un'azione rischiosa (segreti, invii, cancellazioni) è la guardia che funziona: non si propone
di toglierla.

## 3. Il report

Nel terminale. In testa una riga coi numeri della sintesi. Poi al massimo 7 proposte numerate, la più utile
prima. Ognuna ha:
- cosa fare, in una frase all'infinito;
- le prove: due o tre sessioni con la data e le parole della persona fra virgolette dritte, corte;
- chi agisce: **tu** (una riga nella tua Orsa, una nota da togliere) oppure **chi mantiene Arturo**
  (un difetto o una funzione di Arturo);
- il costo, se ce n'è uno.

Sotto, fuori conteggio, al massimo tre righe di igiene reversibile della persona: le applichi tu, e lo dici.
Ultima riga: **sì 1 3**, **tutte** oppure **nessuna**.

Scrivi le proposte anche in `$S/proposte.json`:
`{"proposte": [{"cosa": "...", "perche": "...", "prove": ["..."], "chi": "tu|arturo"}]}`.

## 4. Le scelte e la consegna

1. Le proposte scelte con `chi: tu` le applichi tu, una per volta, col sì della persona sul testo. Una
   modifica al CLAUDE.md la chiede la guardia, come sempre.
2. Le proposte scelte con `chi: arturo` vanno a chi mantiene Arturo, in una segnalazione sola:
   ```bash
   $A revisione bozza --da "$S/proposte.json" --scelte "<numeri>" -o "$S/bozza.md"
   $A segnala prepara --tipo proposta --titolo "Revisione: <il tema principale>" --file "$S/bozza.md" --origine revisione
   ```
   Mostra l'anteprima così com'è: la redazione ha già tolto email, percorsi e segreti. Chiedi **mando** o
   **no**. Solo con **mando** lancia `$A segnala invia --canale arturo --file <il file della riga PRONTA>`.
   Se `prepara` chiede il contatto, fai la domanda come la scrive lui, una volta sola.
   Mai `segnala manda`: partirebbe senza il sì.
3. Scrivi il registro con l'esito di ogni proposta:
   ```bash
   $A revisione salva --da "$S/proposte.json" --scelte "<numeri>" --esito "2=rifiutata: <parole della persona>"
   ```

Il registro resta su questo computer, fuori da ogni repository. L'estratto sta nello scratchpad e non parte
mai. Cosa resta e cosa parte: `~/.claude/docs/privacy.md`, sezione "La revisione".

## Finito quando

Prima di chiudere controlla ogni riga. Se una dice no, sistemala o dillo alla persona.

- Ogni proposta nasce da almeno due sessioni diverse, salvo un errore di Arturo con causa certa?
- Le proposte sono al massimo 7, ognuna con le prove (data e parole fra virgolette dritte) e chi agisce?
- `proposte.json` è scritto nello schema?
- Niente è partito con `segnala manda`, e l'invio è venuto solo dopo **mando**?
- `revisione salva` è stato lanciato con l'esito di ogni proposta?
