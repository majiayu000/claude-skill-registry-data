---
description: Aggiorna README.md e CHANGELOG.md del progetto, crea il README se manca, e scrive la voce di rilascio nel CHANGELOG quando l'utente lo chiede. Se il progetto ha un sito di documentazione esterno, aggiorna anche quello, e ricorda per ogni progetto se il sito esiste e dove si trova. Si lancia solo su richiesta.
argument-hint: [cartella-progetto]
disable-model-invocation: true
---

# Aggiornamento della documentazione

Rispondi in italiano. Una sola domanda per messaggio.

1. Individua la radice del repository del progetto (`git rev-parse --show-toplevel`). Il progetto si identifica con questo percorso, con `/` al posto di `\`.
2. Leggi in `~/.claude/kit-progetti.json` la voce del progetto. Se la voce `sito` manca, chiedi una sola domanda: il progetto ha un sito di documentazione esterno (sì/no)? Se sì, chiedi il percorso della cartella del sito. Salva la risposta nella voce del progetto: crea il file se non esiste, e aggiorna solo quella voce.
3. Aggiorna `CHANGELOG.md` del progetto, se esiste, con una voce per il lavoro di questa sessione nel formato del progetto (per il template: giorno, poi una sottosezione per intervento con **Perché**, **Cosa / Dove**, **Verifica**, **Note**). Se l'utente chiede un rilascio e indica la versione `X.Y.Z`, aggiungi in cima la sezione `### Rilascio X.Y.Z` con i punti salienti del ciclo, raggruppati per le categorie definite in `git.md` (sezione «Rilascio»). Non modificare il file di versione e non creare commit: il commit di bump resta separato e si fa solo su richiesta esplicita.
4. Se `README.md` non esiste, crealo con queste sezioni, in quest'ordine: titolo con una frase di scopo; requisiti; avvio rapido; configurazione (variabili d'ambiente, con rimando a `.env.example` e senza valori reali); comandi; struttura del repository; licenza. Se esiste, aggiornalo solo dove il lavoro cambia ciò che il README dice (comandi, installazione, configurazione, struttura). Non riscrivere il resto, nemmeno se è datato.
5. Se il progetto ha un sito (voce `sito` con `esiste: true`), aggiorna le pagine del sito che descrivono ciò che è cambiato, nella cartella indicata. Se non è chiaro quali pagine, chiedi una sola domanda prima di modificare.
6. Non creare commit e non toccare altri file. Chiudi con l'elenco dei file modificati e di ciò che resta da verificare (build, test del sito).
