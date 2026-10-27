---
name: gemini-argon
license: GPL-3.0-only
description: Usa Gemini come agente o collaboratore esterno in Codex tramite Antigravity CLI e login Google al proprio piano Google AI, senza API a consumo. Supporta Argon predefinito e altri modelli Gemini selezionabili con --model. Usa per chiedere a Gemini revisioni, secondi pareri, analisi o proposte sul progetto.
---

# Gemini via Antigravity

Copyright © 2026 Cerqua ([elcerqua](https://github.com/elcerqua)).
Licenza [GNU GPL versione 3](LICENSE). Repository ufficiale:
[elcerqua/argon-agent](https://github.com/elcerqua/argon-agent).

Usa `scripts/Gemini_Argon.py`, risolto rispetto a questa skill. Python 3.10+ e
Antigravity CLI ufficiale (`agy`). Backend predefinito `antigravity-cli`,
autenticazione **login Google al piano Google AI**, modello predefinito
`gemini-4-argon`. Usa Gemini come collaboratore esterno coordinato da Codex:
Codex prepara l'incarico, Gemini analizza il dossier e Codex verifica la risposta.
Il percorso predefinito non richiede chiavi API ne fatturazione API a consumo;
restano i costi e le quote del piano. Antigravity puo usare crediti AI extra quota
se l'utente ha abilitato AI Credit Overages: l'opzione Never limita l'uso alla quota
inclusa. Non promettere assenza di costi extra e non cambiare questa preferenza
senza incarico. Vedi [piani e crediti](https://www.antigravity.google/docs/plans/#overages).
Il wrapper risolve
anche l'installazione Windows in `%LOCALAPPDATA%\agy\bin\agy.exe` senza richiedere
un riavvio del PATH. Mantieni il nome d'invocazione `$gemini-argon` anche per gli
altri modelli. Non passare ad altri modelli o all'API a consumo automaticamente.

## Modello come parametro

`prepare --model <slug>` e `probe --model <slug>` selezionano il modello.
Per i modelli diversi da Argon usa lo slug esatto restituito da `agy models`,
per esempio `gemini-3.8-flash-medium` o `gemini-3.1-pro-high`, se disponibili
sull'account. Non esiste una lista fissa nel wrapper: gli slug sono inoltrati
senza riscritture. L'unica abbreviazione e `gemini-4-argon`, espansa con il thinking
per compatibilita. Il parametro del run viene conservato in `request.json` e
`state.json`; `send` usa quel valore e non sceglie un modello nuovo.

Se l'utente specifica un modello, rispettalo. Se indica solo una famiglia e lo
slug non e noto, consulta `agy models` prima di preparare l'invio. La selezione
di un modello non dimostra l'accesso sul piano e non autorizza un fallback.

## Ragionamento

| Richiesta | Parametro |
|---|---|
| basso, leggero, low | `--thinking low` |
| medio, bilanciato, medium | `--thinking medium` |
| alto, approfondito, high | `--thinking high` |

Senza una scelta esplicita, ricava il livello da uno slug Antigravity che termina
in `-low`, `-medium` o `-high`; altrimenti usa `high`. Dichiaralo prima dell'invio.
Uno slug con suffisso e un `--thinking` diverso sono rifiutati gia da `prepare`,
senza rete. Mantieni modello e preferenza espressi per la campagna anche nei
follow-up, salvo nuove indicazioni. Un livello
non supportato, come max/ultra, richiede chiarimento: non convertirlo in silenzio.
Con Antigravity il wrapper usa lo slug scelto (per Argon abbreviato:
`gemini-4-argon-<livello>`) insieme a `--effort <livello>`. Se lo slug non e
disponibile sull'account, segnala l'errore:
non cambiare livello o modello. `--max-output-tokens` e supportato solo dai backend
API/Gemini CLI; Antigravity usa i propri limiti e il timeout, non un cap token
imposto da questo parametro. I metadati della CLI non sono un'attestazione del server.

## OAuth e disponibilita effettiva

```powershell
$argonWrapper = Join-Path $env:USERPROFILE '.codex\skills\gemini-argon\scripts\Gemini_Argon.py'
python $argonWrapper status
python $argonWrapper login
```

`login` richiede un terminale interattivo: completa il browser con l'account
Google associato al piano Pro/Ultra. In alternativa apri
`scripts/Login_Gemini_Argon.ps1` in PowerShell. Non chiedere password o codici in chat.
Antigravity usa la propria sessione Google condivisa fra CLI e altre superfici,
con credenziali gestite dal keyring del sistema. Il wrapper non ne legge o stampa
il contenuto e non copia token dal precedente profilo Gemini CLI.
Non sostituire OAuth con una chiave API o con ADC.

I percorsi degli esempi vanno risolti dalla directory effettiva della skill;
un'installazione in `~/.agents/skills` richiede di adeguare `$argonWrapper`.

`status` e locale: rileva CLI e controlla solo metadati del provider nelle
impostazioni; NON verifica piano, login valido o accesso al modello. Google documenta
Argon su Antigravity CLI per Pro pagante (non trial) e Ultra; l'accesso effettivo
va verificato sull'account. `agy models` elenca i modelli dopo il login. Esegui una sola
prova minima, autorizzata dalla richiesta di verificare l'accesso:

```powershell
python $argonWrapper probe --model gemini-3.8-flash-medium --out 'D:\progetto\review\gemini-access-01'
```

Ometti `--model` per provare Argon predefinito. La prova invia solo
`Reply exactly GEMINI_ACCESS_OK. Do not use tools.` e controlla anche la risposta
esatta. Non allega il progetto. Se la CLI risponde con modello diverso, manca la
prova del modello, il marker e diverso o il server rifiuta il modello, riferisci
l'esito preciso. L'assenza
del nome nella lista locale non dimostra da sola un rifiuto del server.
L'accesso sul piano rimane soggetto alle quote; non dichiararlo illimitato.

## Dossier e consulenza

Gemini non eredita questa chat. Prepara una domanda UTF-8 con obiettivo, incarico,
vincoli ed evidenze e seleziona i file testuali pertinenti. Includi fonti primarie,
risultati negativi ed errata utili, oltre alle sintesi. Chiedi citazioni dei file
e delle righe, distinguendo fatti osservati, ipotesi e prove mancanti.
Non inviare segreti, file di credenziali o archivi dell'intero progetto.
Il controllo automatico dei segreti e parziale e non sostituisce la selezione.

Per revisioni di campagne e proposte di nuovi esperimenti leggi
[references/review-experiments.md](references/review-experiments.md).
Le istruzioni specifiche del progetto si passano nel dossier.

```powershell
python $argonWrapper prepare --root 'D:\progetto' --prompt-file 'D:\progetto\review\question.md' --files-from 'D:\progetto\review\files.json' --thinking high --out 'D:\progetto\review\argon-01'
python $argonWrapper send --run 'D:\progetto\review\argon-01'
```

Per un altro modello aggiungi a `prepare`, per esempio,
`--model gemini-3.8-flash-medium --thinking medium`. Lo slug effettivo deve esistere
sull'account. Per un incarico di scrittura o proposta passa obiettivo e istruzioni
nel prompt; la skill restituisce testo o codice proposto nel dossier di risposta.
Il wrapper resta in modalita di consulenza: Codex verifica e applica gli eventuali
interventi entro l'incarico dell'utente.

`files.json` e un array JSON di file espliciti relativi alla root, per esempio
`["AGENTS.md", "reports/result.md", "src/model.py"]`. Sono ammessi percorsi assoluti
interni alla root. Oppure ripeti `--attach`. Non sono supportati glob o scansioni
ricorsive. Per una domanda breve usa `--prompt`; `--system-file` aggiunge istruzioni.
PDF/immagini/binari richiedono prima estrazione testuale verificata.

`prepare` e offline. Produce domanda completa numerata, manifest SHA256 e stato.
Richiede una directory nuova; limite predefinito 3.000.000 byte del payload,
modificabile con `--max-input-bytes`. Non tronca e non stima i token.
`request.json` conserva il dossier e i parametri in una struttura comune ai backend:
con OAuth non e inviato come richiesta REST, ne sono usati i campi store/background.

`send` passa il dossier su stdin con input/output stream-json, modello fissato,
modalita `plan`, agente di revisione e workspace separato. Non concede
autoapprovazioni. L'agente dichiara `tools: []`, ma nella CLI 1.4.2 il catalogo
degli strumenti rimane esposto nell'evento init: non dichiarare che gli strumenti
siano tecnicamente assenti. Il wrapper invalida una risposta che riporta uso di
tool; questo controllo osserva gli eventi e non e un sandbox preventivo.
Rimuove dal solo processo figlio variabili per chiavi API/Vertex/ADC
e rifiuta impostazioni di provider API o ADC rilevate. Non modifica le preferenze
permanenti dell'utente. Il login resta quello gestito ufficialmente da Antigravity.
Il server puo comunque rifiutare modello, configurazione o quota: nessun recupero
tramite un altro backend e autorizzato implicitamente.

Prima dell'invio comunica modello, thinking, contenuto generale e percorso del run,
poi procedi entro l'autorizzazione esistente. Il comando CLI puo richiedere minuti:
usa sessioni tool riprendibili e dai aggiornamenti. Timeout predefinito 900 secondi,
modificabile con `send --cli-timeout`. Non ripetere automaticamente un invio.

Per una domanda successiva aggiungi a `prepare` `--previous-run '<run precedente>'`
e ripeti `--model` e `--thinking` della campagna. Il cambio di modello o backend
richiede una conversazione nuova.
Con i backend CLI il wrapper incorpora esplicitamente il transcript locale precedente
(domanda e risposta) nel nuovo dossier; NON usa il resume nativo della CLI.
Il nuovo manifest collega i run e il limite di byte si applica all'intero transcript.
`resume --run` su un run CLI legge solo lo stato locale, senza inviare altro.

## Risultati e recupero

- Exit 0: preparazione/stato o risposta completata con testo e modello verificato.
- Exit 3: richiesta ancora in corso, per esempio una sessione tool non terminata.
- Exit 4: login richiesto, modello indisponibile/diverso/non verificato, probe
  con marker errato (`probe_failed`), risposta
  parziale/vuota, fallimento CLI o esito ambiguo. Non presentarlo come successo.
- Exit 2: errore locale, input non valido o errore del backend.

Leggi `state.json`, `response.md`, `response-0001.json` e, se necessario, i log
`cli-stdout.txt`/`cli-stderr.txt`. Non riversare nella chat URL OAuth o token
eventualmente presenti nei log di un'autenticazione fallita. Per Antigravity il
wrapper richiede evento `init` con lo slug fissato, risultato `SUCCESS`, testo e
exit code 0; il contratto headless della CLI esclude fallback silenziosi. Questo
verifica la selezione della CLI, non certifica l'identita interna del server.
Eventuali tool effettivamente usati invalidano il risultato di sola revisione.

Una richiesta di consulenza autorizza l'invio del materiale pertinente e
condivisibile; la sola configurazione non autorizza l'invio del progetto.
La proposta di Gemini non autorizza automaticamente nuovi fit, download o modifiche.
Gemini e un collaboratore esterno, non un modello nativo di `spawn_agent`.
Riporta il suo parere con link alla risposta salvata e verifica le indicazioni
prima di applicarle. Non attribuirgli file che non ha ricevuto o calcoli non eseguiti.

Il backend REST precedente rimane disponibile solo su richiesta esplicita:
vedi [references/api-backend.md](references/api-backend.md). Con OAuth non usarlo.
Il backend `gemini-cli` precedente e mantenuto solo come opzione esplicita;
non usarlo al posto di Antigravity per questa configurazione.

Fonti: [autenticazione](https://www.antigravity.google/docs/install?tab=cli),
[modelli e piani](https://www.antigravity.google/docs/models/),
[headless e ragionamento](https://www.antigravity.google/docs/cli/headless/),
[agenti personalizzati](https://www.antigravity.google/docs/subagents/).
