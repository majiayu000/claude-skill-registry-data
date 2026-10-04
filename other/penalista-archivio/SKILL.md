---
name: penalista-archivio
description: >
  Conversione di documenti (PDF, sentenze, atti, dottrina) in Markdown indicizzato
  per la Knowledge Base, e governo dell'INDICE della giurisprudenza. ATTIVARE quando
  l'avvocato dice: 'converti questo PDF', 'metti questa sentenza in memoria',
  'aggiungi alla knowledge base', 'indicizza i massimari', 'trasforma in markdown',
  'carica il documento nella KB', 'aggiorna l'indice della giurisprudenza',
  'prepara il documento per la consultazione', 'converti la rassegna', 'aggiorna la banca dati', 'scarica le pronunce segnalate', 'sincronizza le segnalate', 'ci sono nuove sentenze della Cassazione?'. Attivare anche
  quando un documento PDF va consultato ripetutamente e conviene convertirlo una volta
  per risparmiare token. È la skill che alimenta il protocollo quote-then-claim:
  produce il materiale ancorabile su cui si fonda ogni citazione verificata.
---

# penalista-archivio — Conversione e indicizzazione della Knowledge Base

## Cosa fa

Trasforma documenti (in primis PDF a testo nativo: rassegne del Massimario, sentenze,
atti, dottrina) in **Markdown pulito con marcatori di pagina** e genera un **indice a
due livelli** che rende la KB interrogabile a basso costo di token e — soprattutto —
**ancorabile**: ogni citazione potrà essere ricondotta a un file e a una pagina reali.

Due ragioni per cui esiste:

1. **Economia di contesto.** Un PDF viene letto come immagine, costoso a ogni
   interrogazione. Il Markdown è testo: leggibile, *grep*-abile, riusabile a costo minimo.
2. **Guardrail anti-allucinazione.** L'indice è il presupposto del protocollo
   *quote-then-claim*: non si cita ciò che non è nell'indice.

## I due livelli dell'indice

- **Strutturale** (concetto → fonte : pagina): PARTE / SEZIONE / CAPITOLO con il loro
  titolo-concetto e la pagina di inizio nel corpo. Serve a **navigare per argomento**.
- **Citazionale** (Rv → fonte : pagina → massima): ogni sentenza realmente presente,
  con numero Rv, pagina e citazione testuale. È il **backbone del grounding**.

L'indice master vive in
`KNOWLEDGE_BASE/02_GIURISPRUDENZA/_MD_INDICIZZATO/INDICE_GIURISPRUDENZA_PENALE.md`.
I Markdown convertiti stanno nella stessa cartella.

## Come si converte un documento

```bash
# 1) Converti un PDF (testo nativo) in MD + indice JSON
python3 skills/penalista-archivio/scripts/converti_indicizza.py \
    <input.pdf> KNOWLEDGE_BASE/02_GIURISPRUDENZA/_MD_INDICIZZATO/ \
    --titolo "Etichetta leggibile della fonte"

# 2) Rigenera l'indice master unendo tutti gli *.index.json presenti
python3 skills/penalista-archivio/scripts/genera_indice_master.py \
    KNOWLEDGE_BASE/02_GIURISPRUDENZA/_MD_INDICIZZATO/ \
    KNOWLEDGE_BASE/02_GIURISPRUDENZA/_MD_INDICIZZATO/INDICE_GIURISPRUDENZA_PENALE.md
```

Dipendenza: `pdfplumber` (`pip install pdfplumber`).

## Limiti — leggere con attenzione

- **NON fa OCR.** Se il PDF è una scansione (poco testo estraibile) lo script si ferma
  e lo segnala: va prima passato per un OCR. Non convertire mai una scansione "alla cieca".
- L'estrazione strutturale è tarata sulle Rassegne del Massimario (PARTE/SEZIONE/CAPITOLO).
  Su documenti con struttura diversa l'indice strutturale può essere parziale: in quel caso
  la ricerca per concetto si fa con `grep` direttamente sul `.md`.
- L'indice citazionale riconosce il formato Cassazione `Sez. X, n. … del gg/mm/aaaa, Nome, Rv. …`.
  Citazioni con formattazione anomala possono sfuggire: vanno aggiunte a mano se rilevanti.
- **Tutto il prodotto è materiale di lavoro**: la conversione non sostituisce la lettura
  della fonte ufficiale da parte del difensore.

## Banca dati pronunce segnalate — sincronizzazione settimanale

Il kit ha una banca dati centralizzata delle **pronunce penali segnalate dall'Ufficio del
Massimario** (sentenze e ordinanze di rilievo nomofilattico, Sezioni Unite, questioni SU
pendenti e decise), aggiornata **ogni lunedì** da una pipeline automatica nel repo pubblico
`Synthos-Logic/giurisprudenza-db`. Ogni scheda contiene la massima ufficiale, "l'esito
in sintesi" e il **link al PDF autentico** sul sito della Corte: fonti verificabili con un clic.

Per scaricarla o aggiornarla (repo pubblico: **non serve alcun account GitHub**):

```bash
python3 skills/penalista-archivio/scripts/sincronizza_segnalate.py KNOWLEDGE_BASE
```

Lo script mantiene una cache git locale (primo scaricamento una tantum, poi solo
differenze), aggiorna `02_GIURISPRUDENZA/SEGNALATE/` (pronunce segnalate + Radar del merito)
e `02_GIURISPRUDENZA/CONSULTA/` (**Corte costituzionale: di default gli ultimi 10 anni**,
~2.700 pronunce e poche decine di MB — il taglio giusto per il lavoro quotidiano; con
`--tutto` l'archivio completo dal 1956, 22.000+ pronunce, ~160 MB; con `--da-anno N` una
soglia personalizzata) e reindicizza la zona: segnalate nel
REGISTRO_FONTI (riga per anno, tipo `massimario-segnalate`) e sezione 3 dell'INDICE;
Consulta come fonte unica (tipo `corte-costituzionale`) con **registro dedicato**
(`CONSULTA/INDICE_CONSULTA.md`, sezione 4 dell'INDICE). Con `--solo-segnalate` si evita
la copia dell'archivio costituzionale.

Avvertenze:
- la cartella `SEGNALATE/` è di proprietà della pipeline: **le modifiche locali vengono
  sovrascritte** alla sincronizzazione successiva. Le note personali vanno altrove in KB.
- le segnalate **non hanno ancora numero Rv** (arriva col massimario annuale): si citano
  per numero/anno con riferimento alla scheda e al PDF ufficiale. Quando la stessa pronuncia
  comparirà nel massimario annuale con Rv, si preferisce la citazione con Rv.
- se il clone fallisce (rete assente), si può scaricare lo ZIP del repo dal browser e
  copiare a mano la cartella `SEGNALATE/`.

## PROTOCOLLO quote-then-claim (grounding obbligatorio)

Quando si cita giurisprudenza che dovrebbe essere nella KB, l'ordine è vincolante:

1. **Cerca prima nell'indice.** Per concetto → indice strutturale o `grep` sul `.md`.
   Per una sentenza → `grep` del numero Rv o della parte nel registro citazionale.
2. **Vai alla pagina e leggi.** Apri il `.md` al marcatore `<!-- pag. N -->` indicato.
3. **Incolla la massima testuale**, con l'indicazione `(fonte, p. N)`. Si afferma solo
   ciò che si è letto.
4. **Se non è nell'indice → si dichiara "non presente in KB".** NON si cita a memoria,
   NON si "ricostruisce" il numero. L'astensione è il comportamento corretto: meglio
   un buco dichiarato che una citazione inventata.

> Regola d'oro: **ciò che non è nell'indice non esiste**, ai fini della citazione.
> Il difensore verifica comunque sulla banca dati ufficiale prima del deposito.
