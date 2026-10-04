---
name: linkedin-cringe
description: Genera post LinkedIn cringe (italiano di default, ma funziona in qualunque lingua), calibrati su livello di cringe (1-10), registro (credibile / parodico / surreale deadpan alla Lynch) e moduli cringe scelti da un catalogo di 51, con la possibilità di partire da un fatto reale (una notizia data dall'utente o cercata dalla skill). Usala quando l'utente chiede un post LinkedIn cringe, motivazionale, da fuffaguru, da founder, da HR o da boomer, un post "ispirato all'attualità", un post surreale o onirico "alla David Lynch", oppure vuole parodiare lo stile LinkedIn.
---

# LinkedIn Cringe: generatore di post

Genera post LinkedIn in italiano che riproducono il cringe autentico di LinkedIn Italia.

## Principio guida

Il cringe non è "scritto male". Il cringe è **imbarazzo vicario**: nasce quando chi
scrive ci crede davvero, rivendica una profondità che il testo non ha, e sta vendendo
qualcosa fingendo di non vendere nulla.

**Regola non negoziabile: la voce non strizza mai l'occhio.** Nessuna ironia, nessuna
autoconsapevolezza, nessun ammicco al lettore. Appena il testo ammicca, smette di essere
cringe e diventa barzelletta.

Leggi `references/tassonomia.md` prima di scrivere: contiene la definizione operativa,
la legge dello scarto e la scala 1-10.

## Flusso

### 1. Raccogli i parametri

Se l'utente ha già indicato tema, livello o moduli nella richiesta, **non fare domande**:
usa quello che ha detto e riempi i buchi con i default (livello 7, credibile).

Altrimenti mostra prima il **menu dei moduli**: elenco compatto, codice + nome, preso da
`references/moduli.md`, e poi chiedi i parametri con **AskUserQuestion**, quattro domande:

**D1. Livello di cringe** (`header: "Livello"`)
- `4` Lieve: passa inosservato, lascia solo un leggero fastidio
- `7` Imbarazzante (consigliato): il punto dolce, chi legge fa una faccia
- `9` Insostenibile: screenshottabile, il tipo di post che gira nelle chat
- `10` Leggendario: tutti i tic insieme, oltre il limite del sopportabile

**D2. Registro** (`header: "Registro"`)
- `Credibile (consigliato)`: deve poter passare per un post vero, pescato dal feed.
  Nessuna esagerazione che tradisca la finzione.
- `Parodico`: esagerazione dichiarata, si capisce che è una presa in giro
- `Surreale deadpan`: il mondo raccontato è impossibile e la voce non se ne accorge.
  Né credibile né parodico, nessuna battuta. Vive dal livello 7 in su, il punto dolce
  è il 9
- `AI-SLOP`: il post non ha un autore, è stato generato e incollato senza rileggerlo.
  Ribalta la regola anti-AI di questa skill. Non viene mai scelto dalla skill: solo
  dall'utente, qui o per nome. Vive dal livello 5 in su, il punto dolce è l'8

**D3. Voce** (`header: "Voce"`)
- `Fuffaguru mindset`: coach/consulente che vende crescita personale
- `Founder / CEO`: imprenditore che flexa mascherando da lezione
- `HR / recruiter`: chi dà lezioni di vita ai candidati
- `Boomer con consiglio`: over 50 che spiega la vita ai giovani

**D4. Moduli cringe da inserire** (`header: "Ingredienti"`, `multiSelect: true`)
Quattro combo pronte; l'utente può usare "Other" per scrivere i codici del catalogo
(es. `C01, C13, C19`):
- `Parabola + colpo di scena` (C01 + C02 + C19)
- `Vulnerabilità + numeri` (C03 + C13 + C11)
- `Hustle + boomerata` (C06 + C14 + C07)
- `Pacchetto completo`: scegli tu i moduli coerenti col livello

Se manca il tema, chiedilo a parte in chat con una riga, non con AskUserQuestion.

**Registro surreale (opzionale).** Si attiva da solo quando l'utente scrive "alla David
Lynch", "surreale", "onirico", "tipo sogno", "assurdo ma serio", o descrive una scena
che non può essere successa: in quel caso non chiedere il registro, dallo per scelto e
porta il livello di default a 9. Prima di scrivere leggi `references/surreale.md`:
contiene le otto regole, il repertorio, cosa cambia nei moduli, le frasi che uccidono
il registro e la diagnosi degli errori. È il registro dove la voce sincera conta più
che altrove, e dove il fatto reale (se c'è) resta l'unico punto fermo del post.

**Gancio reale (opzionale).** Il tema può venire dalla cronaca invece che dalla
fantasia: è quello che fa una buona fetta del cringe vero. Si attiva quando l'utente
scrive "ispirati a…", "prendi spunto da…", "dall'attualità", "dalla cronaca", oppure
incolla una notizia, un dato o un link. Due rami:

- **fatto dato dall'utente** → si usa quello; se è un link, `WebFetch` per ricavare
  data, cifre e luoghi esatti;
- **solo "attualità"** → cerchi tu le notizie degli ultimi 7-10 giorni (`WebSearch`,
  con i feed RSS come fallback) e proponi 3-4 ganci con `AskUserQuestion`; l'utente
  sceglie o scrive il suo. Questa domanda sostituisce quella sul tema.

Prima di procedere leggi `references/attualita.md`: spiega i cinque usi del fatto
reale, le regole di credibilità (il fatto resta vero ed esatto, la morale resta
sganciata) e i paletti specifici, in particolare che **le tragedie si usano solo in
registro parodico**.

**Lingua.** Default: italiano. Non è una quinta domanda, si deduce dalla richiesta
("un post in inglese", "per il mercato tedesco", oppure il fatto che l'utente scriva in
un'altra lingua). Se richiesta una lingua diversa dall'italiano, leggi la sezione
*Adattamento ad altre lingue* in `references/lessico.md` prima di scrivere.
**Non tradurre mai un post italiano: rigeneralo dai moduli nella lingua target.**

### 2. Scegli i moduli

Consulta `references/moduli.md`. Numero di moduli in base al livello:

| Livello | Moduli narrativi | Tic formali |
|---------|------------------|-------------|
| 1-3     | 1                | broetry leggera, 2-3 hashtag |
| 4-6     | 2                | broetry, CTA, 4-6 hashtag |
| 7-8     | 3-4              | + emoji-bullet, numeri finti, P.S. |
| 9-10    | 5+               | tutto: muro di hashtag, MAIUSCOLO, foto scollegata |

I moduli scelti dall'utente hanno la precedenza; aggiungine altri per arrivare al conto.

In registro surreale `C37` (onirico deadpan) è sempre incluso e non conta nel totale:
è il registro fatto modulo. Sotto il livello 7 il registro surreale non si usa, non c'è
abbastanza post intorno al sogno perché il contrasto si veda.

### 3. Scrivi il post

Struttura canonica (modulo C21):

```
HOOK shock                    <- 1 riga, spesso una domanda o un'affermazione brutale
[riga vuota]
micro-narrazione              <- una frase per riga, mai un paragrafo
[riga vuota]
COLPO DI SCENA                <- la battuta che "cambia tutto"
[riga vuota]
morale universale             <- slegata dai fatti, più grande dell'aneddoto
[riga vuota]
CTA + emoji                   <- "E tu? 👇"
muro di hashtag
[riga vuota]
riga di disclaimer            <- vedi sezione dedicata, sempre presente
```

Usa `references/lessico.md` per itanglese aziendale, formule d'attacco, formule di
svolta, chiusure, nomi di fantasia, pool di hashtag ed emoji.

**Leva principale del cringe: la distanza fra l'evento e la morale.** Più l'evento è
banale e la morale è cosmica, più alto il cringe. Non alzare il livello aggiungendo
emoji: alza lo scarto.

Consulta `references/esempi.md` per sentire come suonano i livelli 4, 7, 9 e 10, la
versione parodica e quella surreale.

In registro surreale la leva è la stessa, applicata più in là: l'evento non è banale,
è impossibile, e la morale aziendale ci viene incollata sopra con lo stesso tono di
sempre. Il formato del post non si deforma mai (`references/surreale.md`, regola 2) e
nessuna riga viene costruita per far ridere (regola 7).

Se il post ha un gancio reale, le cifre e le date del fatto restano quelle della fonte
(niente C13 sul fatto: i numeri finti-precisi vanno sulle misurazioni dell'autore), il
fatto occupa al massimo tre righe e non viene mai linkato nel corpo del post.

### 4. Consegna

Mostra il post in un blocco di codice, così si copia-incolla senza che il markdown
mangi la formattazione, poi in due righe elenca i moduli usati con i loro codici.

Dopo i moduli, proponi il **prompt per l'immagine del post**, in un suo blocco di
codice, costruito con le regole della sezione *Immagini* qui sotto. Se per quel
post l'immagine è una cattiva idea (capita: sotto il livello 5 spesso il post vero
non ne ha), dillo e proponi di pubblicare senza.

Chiudi sempre offrendo un giro successivo: alzare o abbassare il livello, cambiare voce,
rigenerare con altri moduli.

## Non deve sembrare scritto da un'AI

Un post che profuma di modello linguistico non è credibile come cringe umano, e il cringe
umano è tutto il punto. Questa regola vale sempre, a qualunque livello e in qualunque lingua.

**Vietato in output:**

- **Il trattino lungo.** Mai. Al suo posto: punto, virgola, due punti, parentesi.
- Frasi tutte della stessa lunghezza, paragrafi tutti della stessa misura.
- Le triadi perfette ("non solo X, ma anche Y, e soprattutto Z").
- I connettivi levigati: "inoltre", "tuttavia", "pertanto", "in conclusione".
- Le formule da assistente: "è importante notare", "vale la pena sottolineare".
- Il paragrafo finale che riassume quello che si è appena detto.
- Elenchi in cui ogni voce ha la stessa struttura sintattica.
- Lessico uniformemente medio-alto, senza una sola ripetizione.

**Obbligatorio, per suonare umani:**

- Ripetere una parola invece di cercare il sinonimo.
- Alternare frasi lunghissime e frasi di due parole.
- Almeno un dettaglio concreto e inutile: un orario, un oggetto, un nome, una cifra sciatta.
- Una piccola sbavatura: una virgola di troppo, un anglicismo storpiato, una ripetizione.
- Chiudere di colpo, senza tirare le somme.

Ci sono due eccezioni, entrambe opt-in, e nessuna delle due si attiva da sola:

- il modulo `C12` (sapore-AI), che ritrae *l'umano che copia-incolla dall'AI senza
  accorgersene*: i cliché vanno inseriti dentro un testo che per il resto suona umano,
  mai al posto suo;
- il registro **AI-SLOP**, in cui la lista qui sopra si legge al contrario e i divieti
  diventano obblighi. Si attiva solo su richiesta esplicita dell'utente: regole,
  repertorio e condizioni di attivazione in `references/slop.md`.

Perché la regola conta più di prima: da agosto 2026 LinkedIn ha un tasto per segnalare
i contenuti che sembrano generati ("sembra contenuto IA scadente"), e rilevazioni di
giugno 2026 stimano il 41% dei post lunghi e il 30% dei commenti come scritti da un
modello. Un post che profuma di modello non è più solo poco credibile: ha una voce di
segnalazione dedicata sotto.

## Immagini

Collaudato sul campo con la skill gemella `linkedin-cringe-analytics`:
**la foto è il punto dove la finzione crolla per prima.** Un testo di livello 7
regge il registro credibile, ma un'immagine generata viene smontata nei commenti
in poche ore: scritte storpiate sui cartelli, abbigliamento fuori stagione, luce
incoerente con l'orario dichiarato nel post.

Se il post prevede un'immagine, in registro credibile:

- meglio nessuna immagine, o una foto vera e banale (una scrivania, una tazza);
- se l'immagine è generata: **niente testo leggibile in scena** (i lettori fanno
  zoom sui cartelli), e coerenza con i fatti del post: stagione, ora e luce,
  abbigliamento, oggetti citati nel testo;
- prima di consegnare, riguarda l'immagine come un commentatore logico-forense:
  è il filone di commenti più rapido a nascere.

In registro parodico o ai livelli 9-10 vale l'inverso: l'incongruenza fotografica
intenzionale è un'esca eccellente (C24), e i commenti che la smontano fanno parte
dello spettacolo.

In registro surreale la regola è ancora diversa, ed è controintuitiva: **l'impossibile
sta nel soggetto, lo stile resta noioso.** Una sola anomalia visiva, la stessa del
testo, fotografata malissimo come si fotografa una cosa qualunque. Mai chiedere al
generatore "surreal, dreamlike, ethereal, cinematic, David Lynch style": la foto che
sembra arte tradisce quanto la foto patinata. Dettagli in `references/surreale.md`.

In registro AI-SLOP la regola si ribalta del tutto e va dichiarato all'utente: testo
impresso, insegne storpiate, luce da render e sorrisi da stock sono il costume di scena,
non un difetto. Dettagli in `references/slop.md`.

### Il prompt d'immagine

In consegna la skill propone sempre un prompt pronto per un generatore di immagini.
Regole di costruzione:

- **In inglese** (i generatori rendono meglio), con una riga in italiano che dice
  cosa raffigura e perché è coerente col post.
- **Estetica da foto vera, non da foto bella**: chiedi "smartphone photo, slightly
  tilted framing, harsh office lighting, mundane, candid". Mai "professional
  photography, cinematic, 8k": la foto patinata tradisce quanto il cartello storpiato.
- **Vietato il testo in scena**: niente insegne, cartelli, badge leggibili, schermi
  con scritte. Metti l'esclusione nel prompt stesso ("no text, no signs, no logos,
  no readable writing anywhere"). Trucco utile: l'oggetto con testo si mostra girato
  o fuori fuoco.
- **Coerenza con i fatti del post**: stagione, ora e luce, abbigliamento, meteo,
  oggetti citati. Se il post dice "le 5:41", la luce è quella delle 5:41 in quella
  stagione. I commentatori controllano davvero.
- **Soggetto**: il dettaglio banale o l'oggetto-esca, mai la scena madre. La sedia
  vuota, non il colloquio; la tazza, non la riunione. Niente persone riconoscibili:
  se serve una figura, di spalle o mani soltanto.
- Ai livelli 9-10 o in registro parodico, ribalta: un'incongruenza visiva piantata
  (C24 o C32 fotografico) è legittima e va dichiarata all'utente.
- In registro surreale l'anomalia è obbligatoria, ma una sola, e va dichiarata:
  l'oggetto-esca impossibile ripreso come si riprende una tazza.
- Chiudi il prompt con l'aspect ratio (4:5 o 1:1, i formati del feed).

## Distribuzione

Vale quando l'utente pubblica davvero e vuole che il post giri. Se il post serve come
esercizio o come collaudo, questa sezione si ignora: non tutti i post buoni sono post
diffusi, e i due obiettivi si contraddicono piu' spesso di quanto sembri.

**La metrica e' la diffusione, non la reazione.** Su quattro post pubblicati ad agosto
2026, i due che facevano piu' commenti in proporzione alle impressioni sono anche quelli
che hanno girato meno. Quello che ha fatto tre volte le impressioni degli altri e' quello
ridiffuso 26 volte contro 2 e 4. Commentare vuol dire "non sono d'accordo" e resta dentro
al thread; ridiffondere vuol dire "guardate qui" e porta il post in una rete nuova.

**La coppia che produce diffusioni e' C33 piu' C32.**

- `C33` il nervo scoperto da' a una categoria professionale un motivo per intervenire.
  Presente in tutti e tre i post sopra le 48mila impressioni, assente nell'unico piatto.
- `C32` l'errore piantato da' a chi legge attentamente qualcosa da mostrare agli altri,
  ma solo se sta nella frase portante del testo e non nell'immagine.

Senza almeno C33, un post di livello 7 ben costruito puo' non uscire dal primo campione.

**Le prime due righe devono essere una tesi completa e citabile.** Stanno sopra
l'"...altro" e sono l'unica parte che si puo' ridiffondere da sola. Un gancio che
annuncia qualcosa senza dirla ("ieri ho letto un numero e ho spento il telefono") spreca
l'unico spazio che conta: il numero, o l'affermazione, vanno nella prima riga.

**Il tema deve stare nella nicchia del profilo.** La prima ondata va a chi ha gia'
interagito con quell'autore. Un tema fuori nicchia parte in salita anche se il post e'
scritto meglio.

**Cosa invece non e' risultato vero**, e va detto perche' il folklore dice il contrario:
il link nel corpo del post non affossa la portata. Il post piu' diffuso del campione ha
un link accorciato dentro al testo e ha fatto 152mila impressioni.

**L'orario:** il campione e' troppo piccolo per una regola. I tre post che hanno girato
sono usciti alle 18:07, alle 05:45 e alle 06:00, quello piatto alle 11:24. Si puo' dire
che la meta' mattina non e' risultata una buona finestra, non molto di piu'.

## Riga finale di disclaimer

**Dopo gli hashtag, sempre**, separata da una riga vuota, aggiungi una riga che riveli lo
scherzo. Serve a chi legge e serve all'utente, che poi decide se tenerla o toglierla.

Base: "Hai letto fino a qui e volevi uccidermi? Non farlo, è semplicemente ironia."

**Varia sempre la formulazione.** Non ripetere due volte di fila la stessa riga: pesca o
improvvisa dal repertorio in `references/lessico.md`, e quando puoi rendila specifica sul
contenuto del post (è più divertente di una formula generica).

Questa riga è l'unico punto in cui la voce può ammiccare. Il corpo del post sopra di essa
resta rigorosamente serio: se l'ironia risale dentro il testo, il cringe si spegne.

**Dati di collaudo:** il muro di hashtag seppellisce il disclaimer davvero: su un
post virale, un commentatore su tre ci ha creduto nonostante la riga finale. Una
formulazione specifica sul contenuto, con un link, viene invece letta, citata e
persino usata dai lettori nei thread. Entrambi gli esiti sono legittimi: scegli
quanto in profondità seppellirla in base a quanto vuoi che lo scherzo si sveli.

Quando consegni, di' all'utente in mezza riga che quella è la riga rimovibile.

Con un gancio reale la riga deve separare il vero dal finto ("La notizia è vera. La
lezione no."): altrimenti chi scopre lo scherzo butta via anche il dato. Se l'utente
vuole citare la fonte, il link va qui, non nel corpo.

In registro surreale la riga separa il vero dal sogno ("La notizia è vera. Il cervo
no.") ma **non spiega il sogno**: può dire che è satira, non può fare da didascalia.
Spiegare cosa volesse dire la figura enigmatica è l'unica forma di ammicco che quel
registro non sopporta.


## Paletti

Valgono anche quando il registro è "credibile", anzi, soprattutto lì:

- **Nessuna persona reale.** Nomi di fantasia. Mai mettere in bocca a una persona
  esistente un post che non ha scritto.
- **Nessuna azienda reale** come autrice o bersaglio. I marchi si citano solo di
  sfuggita come oggetti ("ho aperto Excel").
- **Niente lutti, malattie o licenziamenti reali** dell'utente o di terzi. Il modulo C17
  (trauma mining) si usa solo con eventi palesemente inventati, e va segnalato.
- **Notizie tragiche come gancio reale solo in registro parodico.** In credibile si
  scartano o si attenuano al dato aggregato. Dettagli in `references/attualita.md`.
- **Il registro surreale non sblocca le tragedie**, anzi: la voce sincera rende un
  post onirico su un lutto reale più sgradevole di uno parodico, perché nel testo non
  c'è nessuna dichiarazione di finzione a cui aggrapparsi. E nessuna persona reale
  entra nella scena onirica: chi compare nella notizia resta nella notizia.
- Se l'utente vuole pubblicarlo davvero, ricordagli una volta che è un post finto,
  poi fai quello che chiede.
