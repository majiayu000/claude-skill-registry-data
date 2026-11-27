---
name: italiano-semplificato
description: >-
  Riscrive o controlla un testo dato con l'Italiano Tecnico Semplificato (ITS, adattamento italiano di
  ASD-STE100, 63 regole): classifica il testo, lo riscrive frase per frase e ne verifica la
  conformità, lasciando intatti codice, comandi e fatti.
when_to_use: >-
  Usa quando l'utente passa un testo e dice "riscrivi in ITS", "togli il burocratese", "rendi
  leggibile", "accorcia le frasi", "controlla che sia conforme", o chiede documentazione,
  runbook, messaggi di errore, note di rilascio, capitolati, istruzioni per agenti. Non per le
  risposte in chat (le regole base stanno nel metodo di Arturo o nel CLAUDE.md), non per marketing o voce di brand, non per impaginare un documento che ha un suo standard grafico.
version: 1.1.0
license: MIT
compatibility: claude-code cursor codex gemini-cli opencode
metadata:
  derivato-da: ASD-STE100 Issue 9 (2025-01-15) via github.com/AminBlg/SimpleEnglish (MIT)
  standard: ITS 1.1
---

# Italiano Semplificato: scrivi come un manuale di manutenzione

## Che cosa deve uscire

Il lettore è stanco, di fretta o non madrelingua: ogni frase regge una lettura sola. Un testo ITS ha queste proprietà. Il percorso per arrivarci lo scegli tu.

- Ogni passaggio è procedurale oppure descrittivo, mai le due cose insieme. La classificazione fissa il limite di parole e la forma verbale (tabella sotto).
- Una parola per concetto in tutto il testo. Prima di scrivere scegli il verbo tra `verifica / controlla / accertati`, il nome tra `configurazione / impostazioni / parametri`, il verbo tra `esegui / avvia / lancia`.
- Una sola forma per le istruzioni: imperativo alla seconda singolare, oppure infinito (Regola 5.3).
- Codice, identificatori, comandi, errori citati e fatti restano esatti (vedi Intoccabili).
- Prima di consegnare, il controllo della sezione "Prima di consegnare".

Se ti chiedono di CONTROLLARE un testo invece di riscriverlo, riporta ogni violazione con: numero di regola (la numerazione è quella di `references/catalogo.md`), testo che la viola, riscrittura conforme.

## Due modalità

| Modalità | Quando | Che cosa applichi |
|---|---|---|
| **Pragmatica** (predefinita) | Documentazione, README, messaggi di errore. L'utente vuole un testo chiaro. | Tutte le regole di struttura. Le parole di dominio restano ("idempotente", "webhook", "capitolato"). |
| **Rigorosa** | L'utente nomina ITS, ASD-STE100 o la conformità. Il testo va tradotto o certificato. | Regole di struttura più glossario di progetto scritto, una sola forma verbale per le istruzioni, nessuna parola fuori glossario. |

In modalità rigorosa dichiara sempre il limite della sezione "Limiti": ITS trasporta la meccanica di ASD-STE100, non la certificazione.

## Classifica il testo

| Tratto | Procedurale (istruzioni) | Descrittivo (spiegazioni) |
|---|---|---|
| Scopo | Dire al lettore che cosa fare | Spiegare che cosa è o che cosa fa una cosa |
| Forma verbale | Imperativo: "Installa la pompa." | Indicativo presente, passato prossimo, futuro semplice |
| Limite di frase | **22 parole** (Regola 5.1) | **28 parole** (Regola 6.3) |
| Unità | Un'istruzione per frase (5.2) | Un tema per paragrafo (6.5), massimo sei frasi (6.6) |

Una sezione "Per iniziare" è procedurale. Una sezione "Architettura" è descrittiva. Una nota dentro una procedura è descrittiva: limite di 28 parole, niente imperativo.

ASD-STE100 fissa 20 e 25 parole. L'italiano dice la stessa cosa con più parole grammaticali ("the configuration file" sono tre parole, "il file di configurazione" quattro): il rapporto misurato in localizzazione sta tra 1,10 e 1,20. ITS applica 1,10 e arrotonda a 22 e 28. Se il dominio ha nomi tecnici lunghi, alza le soglie una volta sola e scrivilo nella guida di stile del progetto.


## Prima di consegnare

Il benchmark del 20/8/2026 (54 generazioni, 3 modelli Claude) dice dove sta il lavoro. Condizionale, nominalizzazioni, "qualora", "si consiglia" e accenti sbagliati non compaiono quasi mai nel testo generato. Le violazioni vere sono quattro: frasi oltre il limite, gerundio, rotazione di sinonimi, lineetta lunga. Controlla prima quelle quattro. Poi ogni "se" e ogni "quando" di un comando: deve stare all'inizio della sua frase.

Per un testo scritto da persone, e per la modalità controllo, usa `references/checklist.md`.

Poi una seconda passata sul ritmo e sulla struttura con gli schemi della skill `humanizer` (`skills/humanizer/SKILL.md`, gruppi A, B ed E): contrasti inventati, terne automatiche, chiuse a sentenza, resti della chat. Conta l'accumulo, non la singola occorrenza. Per la prosa in uscita (post, email, proposte) usa direttamente `humanizer`, che segue la voce della persona nella sua Orsa (`~/.claude/personale/humanizer.md`): chi decide cosa lo dice il diagramma "Tre modi di scrivere" in `skills/humanizer/SKILL.md`.

## Intoccabili

Questi elementi sono nomi tecnici (Regole 1.5 e 8.6). Lasciali esatti, anche quando violano le regole di lessico:

- Blocchi di codice, codice in linea, identificatori, comandi, flag, percorsi di file
- Messaggi di errore e righe di log citati
- Nomi di prodotto, nomi di endpoint API, chiavi di configurazione
- Citazioni testuali di norme, bandi e contratti
- Numeri con unità: ognuno conta come una parola nel limite di frase

Anche i fatti sono intoccabili. Riscrivi lo stile, non il contenuto. Quando la fonte non dà un numero, una causa o un termine esatto, tieni l'affermazione generica. Non inventare dettagli per sembrare concreto.

## Limiti

ITS serve per fatti tecnici e istruzioni. Non applicarlo a testi di marketing, a un pezzo con una voce d'autore o alla scrittura di brand: toglie la persuasione per costruzione, e toglie anche il ritmo. Quando l'utente chiede ITS su un testo promozionale, dillo e offri ITS per la documentazione collegata.

Se il documento ha uno standard di casa (titoli, voce), quello standard detta la voce e ITS governa la frase.

### ITS non è ASD-STE100 e non lo sostituisce

ASD-STE100 è la lingua controllata dei manuali di manutenzione aeronautici, una norma per la sola lingua inglese, con un dizionario ufficiale protetto da copyright, scaricabile gratis su asd-ste100.org (ASD-STE100 è un marchio registrato di ASD). ITS ne trasporta la meccanica in italiano. La numerazione delle regole è nostra e non coincide con ASD-STE100: nel controllo cita solo i numeri di questo file. Nessuna conformità ASD-STE100 discende dall'uso di questa skill e nessuno strumento può garantire la conformità a una lingua controllata. L'ultima parola resta a chi scrive.

## Il catalogo delle regole

Le 63 regole, in dieci sezioni (parole, nomi composti, verbi, frasi, testo procedurale e descrittivo,
avvertenze, punteggiatura, pratiche di scrittura, ortografia), stanno in `references/catalogo.md` coi loro
numeri. In una riscrittura leggilo una volta prima di cominciare; in un controllo cita la regola col suo
numero. Le violazioni che contano di più sono le quattro di "Prima di consegnare", qui sopra.

## Una parola, un concetto

ASD-STE100 ha un dizionario ufficiale di circa 900 parole. Per l'italiano non esiste, ma la meccanica funziona lo stesso: una parola, un significato, una parte del discorso. Il dizionario lo costruisci tu in un glossario di progetto di dieci righe, prima di scrivere. L'italiano tecnico ruota i sinonimi per eleganza, e ITS lo vieta (Regole 1.11 e 9.4). Per ogni riga scegli una colonna e tieni quella.

| Concetto | Le parole che ruotano | Scelta consigliata |
|---|---|---|
| accertare uno stato | verificare, controllare, accertarsi, assicurarsi, validare | `verifica che` |
| avviare un programma | eseguire, avviare, lanciare, far partire, runnare | `esegui` |
| togliere un dato | cancellare, eliminare, rimuovere, distruggere | `cancella` per i dati, `rimuovi` per gli oggetti fisici |
| mostrare a schermo | visualizzare, mostrare, riportare, restituire, renderizzare | `mostra` |
| impostazioni | configurazione, impostazioni, parametri, opzioni, settaggi | `configurazione` |
| cosa che non funziona | errore, problema, anomalia, criticità, problematica, issue | `errore` per la condizione tecnica, `problema` per il resto |
| mandare dati | inviare, mandare, spedire, trasmettere | `invia` |
| creare una risorsa | creare, generare, istanziare, produrre | `crea` |

Se il dominio usa un'altra parola, cambiala una volta e scrivila nel glossario. Le tabelle di sostituzione per slop AI e burocratese (da "al fine di" a "per", da "consente di" a "puoi") stanno in `references/sostituzioni.md`. Aprile quando riscrivi un testo scritto da persone o preesistente.


## Altri bersagli

Stesse regole, adattamenti diversi, in `references/casi-uso.md`: messaggi di errore (che cosa è successo, causa, soluzione all'imperativo), runbook, report di incidente (solo passato prossimo, niente attenuazioni), commit e pull request, note di rilascio, istruzioni per agenti AI, documenti di gara e capitolati (riferimenti normativi intoccabili), macro di assistenza, testo di interfaccia, preparazione alla traduzione.


## Esempio completo

**Prima (testo reale non modificato, generato da un LLM):**

> **Timeout di connessione.** Qualora sqlpipe risultasse bloccato o fallisse con `dial tcp: i/o timeout`, è importante verificare che l'host su cui gira sqlpipe possa raggiungere la porta Postgres (solitamente la 5432) — si tratta spesso di una regola di firewall o di un security group che sta bloccando la connessione. Nel caso in cui ci si stia connettendo a un database gestito (RDS, Cloud SQL, ecc.), occorre altresì accertarsi che l'istanza consenta le connessioni provenienti dall'IP di sqlpipe. Si potrebbe inoltre provare ad andare ad aumentare `source.connect_timeout_seconds` nella config, dal momento che una rete lenta potrebbe far scattare il timeout di default anche quando la connessione andrebbe comunque a buon fine.

**Dopo (classificato procedurale, verbo scelto "verifica", condizioni prima, un'istruzione per frase):**

> **Timeout di connessione.** sqlpipe si ferma con `dial tcp: i/o timeout` quando non raggiunge la porta Postgres (5432 nella configurazione predefinita).
>
> 1. Verifica che l'host su cui gira sqlpipe raggiunga la porta Postgres. Di solito la blocca un firewall o un security group.
> 2. Se il database è gestito (RDS, Cloud SQL), verifica che l'istanza accetti le connessioni dall'IP di sqlpipe.
> 3. Se la rete è lenta, aumenta `source.connect_timeout_seconds` nella configurazione.

Che cosa è cambiato: frasi da 50 parole spezzate sotto le 22, tolti tre condizionali e due congiuntivi, `verificare / accertarsi` uniti in `verifica`. Via il gerundio, "andare ad aumentare", "altresì", "ecc." e la lineetta lunga. Ogni condizione sta prima del comando. Codice e stringhe di errore sono intatti.


## Riferimenti

- `references/checklist.md` — controllo completo con schemi cercabili, per la modalità controllo e per il testo scritto da persone
- `references/sostituzioni.md` — tabelle slop AI e burocratese, con la parola corta da scrivere al posto
- `references/casi-uso.md` — adattamenti per messaggi di errore, runbook, report di incidente, commit, note di rilascio, agenti, gare, interfaccia, traduzione
