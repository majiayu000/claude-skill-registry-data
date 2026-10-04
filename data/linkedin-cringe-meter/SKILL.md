---
name: linkedin-cringe-meter
description: Il Cringiometro. Dato l'URL (o il testo) di un post LinkedIn, ne misura il livello di cringe da 1 a 10 con la scala e il catalogo dei 51 moduli della skill linkedin-cringe, dice quali ganci ha preso, il registro, il sapore-AI e la lead-gen, e produce un report markdown più un'immagine 1080x1080 anonima, pronta da usare come risposta sotto al post. Usala quando l'utente chiede "quanto è cringe questo post", "misura / valuta / cringiometro", o vuole un'immagine di risposta stile blastometro.
---

# Cringiometro: quanto è cringe questo post

Terza skill della famiglia: `linkedin-cringe` scrive il post, `linkedin-cringe-analytics`
misura i commenti, il Cringiometro misura il post di qualcun altro (o il proprio) con
lo stesso metro. L'ispirazione è il blastometro, spostato sul cringe: un voto, i
ganci presi, una frase secca, e un'immagine da lasciare nei commenti.

**Si giudica il post, mai la persona.** Nessun nome, azienda, headline o foto
dell'autore compare nel report o nell'immagine. Questo non è negoziabile.

## Flusso

### 1. Acquisizione del post

Serve solo il testo del post (espanso, con l'"…altro" cliccato), più un'indicazione
se c'è un'immagine allegata e cosa mostra. Niente commenti: quelli sono della skill
analytics.

**A. URL + Claude in Chrome.** Se i tool `mcp__claude-in-chrome__*` sono disponibili,
segui il *Setup* di `../linkedin-cringe-analytics/references/estrazione.md` (caricamento
tool, `list_connected_browsers`, scelta browser, `tabs_context_mcp`, `navigate`). Gli
short link `lnkd.in` si risolvono da soli con la navigazione. Poi:

- clicca l'"…altro" del post se il testo è troncato;
- prendi il testo del post con `get_page_text` o `read_page` limitato al contenitore
  del post (l'elemento con `componentkey` che inizia per `urn:li:activity:` o il primo
  `[data-urn]`), senza i commenti;
- annota se c'è un'immagine, un video, un carosello o un sondaggio, e in una riga cosa
  si vede (senza persone riconoscibili).

Se la pagina chiede il login o il browser non è collegato, passa a B senza insistere.

**B. Testo incollato.** L'utente incolla il post in chat, o passa uno screenshot: la
skill legge quello. Dallo screenshot ignora nome, foto e headline dell'autore anche
se visibili. Il resto del flusso è identico.

I dati grezzi (URL, testo integrale, JSON di lavoro) stanno nella scratchpad di
sessione. Nel repository entra solo il report anonimizzato, l'immagine e il JSON
con i soli campi che compaiono nell'immagine.

### 2. Valutazione

Leggi `references/valutazione.md` e, attraverso i suoi rimandi, `tassonomia.md` e
`moduli.md` della skill gemella (`../linkedin-cringe/references/`). Se la skill
gemella non c'è, fermati e dillo: senza catalogo non c'è metro.

Produci, nell'ordine: livello 1-10 con la parola della scala, registro (credibile /
parodico / surreale deadpan / cringe dichiarato), lo scarto in una riga, i moduli rilevati con una
citazione breve ciascuno (massimo 8, in ordine di peso), l'eventuale gancio reale,
sapore-AI, lead-gen, il verdetto in una frase, e i moduli che mancano per salire di
un livello.

Prima di dare il voto, controlla la sezione *Cosa non si valuta* della rubrica: lutti,
malattie e licenziamenti veri fermano la valutazione.

### 3. Report e immagine

Scrivi `analisi/YYYY-MM-DD-<slug>/cringiometro.md` seguendo `references/report.md`
(slug dal tema del post, mai dal nome dell'autore).

Poi genera l'immagine:

1. scrivi `cringiometro.json` nella stessa cartella con `score`, `register`,
   `modules` (codice + nome corto, max 8), `verdict` (la frase, max ~90 caratteri:
   sull'immagine deve stare in due righe), `quote` (una citazione del post di max
   ~90 caratteri, senza nomi) e `lang`;
   **L'immagine parla la lingua del post**: `lang` è il codice della lingua del
   post (`it`, `en`, `de`, `fr`, `es`; altre lingue: `en` più `labels` per i testi
   fissi), e nomi dei moduli, verdetto e citazione vanno scritti in quella lingua.
   Il report e la chat restano nella lingua dell'utente;
2. lancia `python scripts/cringiometro.py analisi/YYYY-MM-DD-<slug>/cringiometro.json
   analisi/YYYY-MM-DD-<slug>/` (percorso dello script relativo a questa skill):
   produce `cringiometro.svg` e, se Pillow è installato, `cringiometro.png` 1080×1080;
3. apri il PNG e guardalo prima di consegnarlo: testo che sborda, pillole tagliate,
   verdetto su tre righe sono da correggere accorciando i testi nel JSON e rilanciando.

Se Pillow manca, consegna l'SVG e di' come installarlo (`pip install pillow`).

### 4. Consegna

In chat: livello e parola, i moduli in una riga, il verdetto. Poi il PNG con
`SendUserFile` e il percorso del report. La prima volta, una riga: l'immagine non
porta nomi, e lasciarla come risposta sotto al post di un estraneo è una scelta sua.

Chiudi offrendo il giro successivo: rigenerare l'immagine con un verdetto diverso,
o passare il post a `linkedin-cringe` per la versione "come sarebbe a 10".

## Paletti

- **Nessun giudizio sulla persona.** Il soggetto delle frasi è il post. Vietati
  aggettivi sull'autore e riferimenti a età, genere, provenienza, aspetto, ruolo.
- **Anonimato totale** in report, immagine e chat: niente nome, azienda, headline,
  foto, link al profilo. L'URL del post resta in scratchpad.
- **Lutti, malattie, licenziamenti veri**: non si valutano. Si dice e ci si ferma.
- **Post privati di persone non pubbliche** (figli, matrimoni, salute): si valutano
  al massimo gli elementi formali, dichiarandolo.
- Se l'utente vuole valutare un proprio post generato con `linkedin-cringe`, il
  registro è "cringe dichiarato" e il voto vale lo stesso: è il collaudo del
  generatore.
- Se l'utente chiede di pubblicare l'immagine come risposta, ricordaglielo una volta
  e poi fai quello che chiede. Non pubblica la skill: consegna il file.
