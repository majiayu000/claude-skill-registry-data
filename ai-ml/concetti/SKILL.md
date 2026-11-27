---
name: concetti
description: >-
  Spiega i concetti base di Claude Code e di Arturo a chi non ha mai aperto un terminale: cos'è un
  harness, contesto e memoria, git e GitHub, branch e fork, cosa succede alle tue modifiche quando
  Arturo si aggiorna, subagent e modelli più economici, ultracode, le due finestre della quota, cosa
  vuol dire dire sì a una conferma, la sandbox. Ogni risposta finisce con dove trovi quella cosa in Arturo.
when_to_use: >-
  Usa quando la persona chiede "cos'è…" (anche "cos'è un harness"), "che differenza c'è tra…",
  "perché…" su uno di questi concetti, o quando una sua frase mostra che li confonde ("la quota della settimana è all'84%"
  mentre la barra dice 5 ore, "ho perso la memoria" dopo /clear), o chiede "cosa ricordi di me?". Non per spiegare il codice di un
  progetto, NON come lezione non richiesta.
---

# Concetti

Sono le domande tornate alla sera del Computer Club del 27/10/2026, quando chi usava Arturo da una
settimana le ha fatte a voce, più quella sulla parola harness, che apre il README dal 4/11/2026. Tu le sai già spiegare. Questa skill serve a due cose: usare le
immagini che quella sera hanno funzionato, e chiudere ogni risposta con il punto di Arturo dove la
persona ritrova la cosa.

## Come rispondi

- Da tre a cinque frasi, in italiano semplice, con un'immagine concreta. Poi una riga "In Arturo:"
  con il comando o il file vero.
- Rispondi alla domanda fatta. Se la persona confondeva due concetti, spiegali tutti e due insieme.
- Se la domanda nasce da un problema in corso (la quota finisce, una sessione "non ricorda"),
  spiega in due frasi e torna al problema.

## Le voci

**Harness.** Un harness è l'insieme di regole e strumenti che sta intorno a un'intelligenza
artificiale e le dice come lavorare: cosa può fare da sola, cosa deve chiederti, dove tiene la
memoria del lavoro. Claude Code è il motore, l'harness è il modo in cui quel motore lavora per te.
Arturo è un harness per il lavoro della conoscenza, cioè scrivere, cercare e tenere in ordine
progetti e documenti. È pensato per chi usa già l'intelligenza artificiale in chat e non ha mai
aperto un terminale.
In Arturo: le regole stanno in `~/.claude`, il README le racconta, e `/setup` le adatta a te.

**Contesto e memoria.** Il contesto è la RAM: quello che la sessione ha sotto mano adesso. Si
riempie mentre lavori, e quando la sessione finisce si svuota. La memoria è il disco: file che
restano, e che ogni sessione nuova rilegge. Due finestre aperte sullo stesso progetto hanno
contesti separati e la stessa memoria.
In Arturo: la barra in basso mostra quanto contesto è pieno. La memoria sono `CLAUDE.md`, gli
handoff che scrive `/fine` e i todo (`arturo todo`), tutti in `~/.claude`. Il capitolo
`~/.claude/docs/principi/04-la-memoria-e-tua.md` racconta il resto.
A "cosa ricordi di me?" o "cosa sai dei miei progetti?" rispondi con il testo di `arturo memoria`:
lancialo e riportalo, senza aggiungere note che non elenca.

**Git e GitHub.** Git è un programma che tiene la storia di una cartella: ogni modifica salvata
(un commit) resta, e puoi tornare indietro. La cartella può contenere codice, testi o foto. GitHub
è uno dei posti dove quella cartella vive anche fuori dal tuo computer. È di Microsoft: Git
funziona anche senza.
In Arturo: `/fine` salva il lavoro con un commit. Il tuo `~/.claude` va su GitHub solo se lo
scegli in `/setup`, in un repository privato.

**Branch e fork.** Un branch è una strada parallela dentro la stessa cartella: provi una cosa
senza toccare la versione che funziona, e se va bene la riunisci. Un fork è una copia di tutto il
progetto che diventa tua: da lì le due strade vanno ciascuna per conto suo.
In Arturo: `/inizio` può aprire una copia a parte del progetto (un worktree) per lavorare senza
toccare l'originale.

**Le tue modifiche e gli aggiornamenti.** Arturo si aggiorna, e un aggiornamento riscrive i suoi
file. Le tue aggiunte ai comandi stanno in file tuoi, che gli aggiornamenti non toccano. La
sicurezza e il funzionamento restano comuni a tutti; il gusto è tuo.
In Arturo: `python3 ~/.claude/bin/arturo personale elenco` mostra le tue aggiunte. Una skill fatta
con `/creaskill`, con un nome nuovo, resta tua.

**Subagent e modelli più economici.** Un subagent è un aiutante che la sessione manda a fare un
compito solo, con un contesto suo: legge un libro intero e torna con il riassunto, e il resto non
riempie il tuo contesto. Per un compito meccanico può usare un modello più piccolo, che costa meno
quota.
In Arturo: chiedi "fallo fare a un subagent" o "usa un modello più economico per questa parte".

**Ultracode.** Scritto in fondo a una richiesta, fa partire più agenti in parallelo sullo stesso
lavoro: per esempio quattro revisioni insieme. È veloce e costa: il 27/10 un lancio ha usato circa
il 5% della finestra di 5 ore in pochi minuti.
In Arturo: guarda la quota nella barra prima di lanciarlo, e chiedi prima quanti agenti partono.

**Le due finestre della quota.** L'abbonamento ha due limiti. Uno vale 5 ore e si azzera
all'orario che la barra mostra. L'altro vale una settimana. Si può essere all'84% delle 5 ore e al
20% della settimana: aspetti l'orario, e riparti.
In Arturo: la barra in basso scrive "quota 5 ore N%, si azzera alle HH:MM · settimana N%".
`/guidami` usa la quota per proporti lavoro della taglia giusta.

**Dire sì a una conferma.** Quando Claude Code chiede "posso?", ti mostra il comando vero che sta
per lanciare. Sì vale per quel comando, quella volta. Le guardie di Arturo chiedono poco apposta:
se chiedono, leggi. Chiediti: se dico sì senza leggere, cosa può succedere?
In Arturo: `~/.claude/docs/principi/02-i-rail-non-l-attrito.md`. Quando Claude ti aspetta, il Mac suona e la
scheda del terminale cambia colore.

**La sandbox.** È un recinto del sistema operativo intorno ai comandi che Claude lancia: un comando, e ogni
programma che quel comando avvia, legge e scrive solo dove serve e va in rete solo verso indirizzi noti.
Le guardie guardano il comando; la sandbox copre anche lo script che il comando lancia, per esempio un
pacchetto installato che prova a leggere le tue chiavi. Sul Mac `/setup` la accende di default; alcuni
programmi (git su SSH, ssh) dentro non funzionano, e Arturo li lascia fuori. Su Windows Claude Code non
ce l'ha: lì restano le guardie.
In Arturo: `arturo sandbox stato`, `arturo sandbox accendi`, `arturo sandbox spegni`; `/setup` la accende
nella fase 8d.
