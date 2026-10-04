---
name: linkedin-cringe-analytics
description: Analizza i commenti di un post LinkedIn (tipicamente un post cringe generato con la skill linkedin-cringe) e produce un report markdown con le statistiche - quanti ci hanno creduto e quanti hanno colto lo scherzo, top ten per gradimento, toni, categorie di commentatori, cringe-metro dei commenti. Usala quando l'utente chiede di analizzare le reazioni o i commenti a un post LinkedIn.
---

# LinkedIn Cringe Analytics: analisi dei commenti

Data l'URL di un post LinkedIn, scarica tutti i commenti e produce un **report
markdown** con le statistiche. È la skill gemella di `linkedin-cringe`: quella
genera il post, questa misura cosa è successo dopo.

## Flusso

### 1. Acquisizione dei commenti

Due strade, in ordine di preferenza:

**A. Browser automation (Claude in Chrome).** Se i tool `mcp__claude-in-chrome__*`
sono disponibili e un browser è collegato, estrai tutto da solo. La procedura
completa e collaudata è in `references/estrazione.md`: **leggila prima di iniziare**,
la UI di LinkedIn ha classi CSS offuscate, liste virtualizzate e lazy-load che si
innesca solo con eventi rotella, e il playbook risolve tutti e tre i problemi.
Se il browser non risulta collegato, chiedi all'utente di collegarlo e offri
subito la strada B come alternativa.

**B. Fallback manuale.** L'utente apre il post, espande tutti i commenti
("Carica altri commenti" / "Vedi risposte precedenti" / "…altro"), seleziona
tutto, copia e incolla in chat, oppure salva la pagina e passa il percorso del
file. Il parsing a valle è identico.

I dati grezzi (con i nomi veri) vanno **solo nella scratchpad di sessione**,
mai nel repository.

### 2. Parsing

Trasforma il raccolto in una lista di commenti strutturati. Il formato dei
blocchi e le regole (risposte dell'autore, duplicazioni da annidamento, righe
di conteggio) sono in `references/estrazione.md`, sezione *Parsing*.

Escludi dalla classificazione le risposte dell'autore del post (blocco
"Autore"): si contano a parte come "botta e risposta" e non inquinano le
percentuali.

### 3. Analisi

Per ogni commento assegna, con i criteri di `references/classificazione.md`:

- **Esito**: 😇 ci ha creduto · 🎭 ha colto lo scherzo · 🤨 dubbioso · ⬜ non classificabile
- **Tono**: ironico di rimando, serio-motivazionale, correttivo-normativo,
  logico-forense, indignato, aneddotico, altro
- **Categoria autore**: dedotta dalla headline (tech, sales/BD, HR/recruiting,
  motivazionale, altro)
- **Cringe-metro 1-10**: solo per i commenti scritti in buona fede, usando
  `../linkedin-cringe/references/tassonomia.md` e `moduli.md` (riferimento
  incrociato: se la skill gemella non è installata accanto, salta questa parte
  segnalandolo)

Poi gli aggregati: percentuali per esito (sui classificabili), top ten per
reazioni, incrocio categoria x esito, distribuzione dei toni, podio del
cringe involontario, fenomeni ricorrenti (citazioni, tormentoni, refusi del
post notati dai lettori).

**Il bucket "non classificabile" è obbligatorio e va difeso**: applausi, tag
secchi e "Grazie per la condivisione" senza altro non sono decidibili, e
forzarli dentro creduto/colto falserebbe le percentuali. Le percentuali si
calcolano sui soli classificabili, dichiarandolo.

### 4. Report

Scrivi il report in `analisi/YYYY-MM-DD-<slug>/report.md` (lo slug viene dal
tema del post, es. `sedia`). Struttura e regole in `references/report.md`.

Due regole non negoziabili, valide anche in chat:

- **Anonimizzazione totale**: mai nomi o aziende dei commentatori, solo
  categoria di profilo ("un recruiter", "una pagina satirica"). Gli estratti
  di commento si citano brevi e senza attribuzione.
- **Copertura dichiarata**: sempre "letti X commenti su un contatore di Y".
  Il contatore di LinkedIn include commenti cancellati e filtrati, quindi
  X < Y è normale e va spiegato, non nascosto.

Consegna: mostra in chat i 3-4 numeri chiave (percentuale creduloni in testa),
poi invia il file. Se l'utente vuole anche la dashboard HTML autocontenuta
(grafici CSS/JS inline, niente CDN), generala nella stessa cartella come
`dashboard.html`; è opzionale, il markdown è l'output primario.

## Paletti

- **Nessun giudizio sulle persone, solo sui commenti.** "Il commento è livello 8
  di cringe", mai "il commentatore è un cretino".
- I dati grezzi con i nomi restano in scratchpad e non si committano. Nel
  repository entra solo il report anonimizzato.
- Se l'utente chiede di pubblicare il report, ricordagli una volta che i testi
  citati restano di chi li ha scritti, poi fai quello che chiede.
- Le risposte private, i profili e i contatti dei commentatori non si toccano:
  questa skill legge un thread pubblico e si ferma lì.
