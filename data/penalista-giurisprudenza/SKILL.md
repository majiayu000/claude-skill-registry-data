---
name: penalista-giurisprudenza
description: "Ricerca e organizzazione della giurisprudenza penale italiana per la difesa. ATTIVARE SEMPRE quando l'avvocato cerca sentenze, massime o orientamenti della Cassazione penale, della Corte EDU o di altri organi giurisdizionali, o dice: 'cerca giurisprudenza su', 'ci sono sentenze favorevoli su', 'cosa dice la Cassazione su', 'quale sezione si occupa di', 'c'e un contrasto tra sezioni su', 'cerca massime su', 'trova precedenti su', 'giurisprudenza favorevole su', 'orientamento della Corte EDU su', 'ci sono novita' dalla Cassazione', 'ultime sentenze segnalate', 'questioni pendenti alle Sezioni Unite', 'la Consulta si e' mai pronunciata su', 'questione di legittimita' costituzionale su', 'sentenze della Corte costituzionale su'. Attivare anche per: costruire la sezione giurisprudenziale di una memoria difensiva o di un ricorso, individuare contrasti giurisprudenziali da portare alle Sezioni Unite, creare o aggiornare note di giurisprudenza nel sistema wikilinks, verificare se un principio di diritto e consolidato o controverso."
---

# Skill — Ricerca Giurisprudenziale Penale

Questa skill supporta la ricerca e l'organizzazione della giurisprudenza penale per costruire argomenti difensivi solidi. La giurisprudenza non è un ornamento — è l'ossatura di ogni atto che conta.

---

## Prima di iniziare

Se la richiesta non è già precisa, chiedi in un'unica domanda:

- **L'argomento giuridico specifico** (non "corruzione" ma "elemento soggettivo della corruzione per la funzione" o "distinzione corruzione/istigazione alla corruzione")
- **L'obiettivo** (trovare orientamenti favorevoli alla difesa / verificare un principio / identificare un contrasto tra sezioni / costruire una citazione per un atto)
- **Il livello di certezza richiesto** (orientamento consolidato / massima specifica / contrasto da segnalare)

---

## MODULO 0 — FRESCHEZZA DELLE FONTI (sempre, prima di ogni ricerca)

La KB contiene due binari di giurisprudenza:

1. **Massimari annuali** (stock consolidato, citazioni con numero **Rv**) — sezioni 1 e 2 dell'INDICE.
2. **Pronunce segnalate** dall'Ufficio del Massimario (flusso settimanale, repo
   `giurisprudenza-db`) — **sezione 3 dell'INDICE** ("Registro segnalate").

**Check di freschezza obbligatorio**: leggi la data di generazione in testa a
`KNOWLEDGE_BASE/_INDICE/INDICE.md`. Se più vecchia di **7 giorni** — o se la cartella
`02_GIURISPRUDENZA/SEGNALATE/` manca — proponi all'avvocato l'aggiornamento:
`python3 skills/penalista-archivio/scripts/sincronizza_segnalate.py KNOWLEDGE_BASE`
(repo pubblico, nessun account richiesto; la pipeline centrale aggiorna ogni lunedì).

**Come si cita una segnalata** (quote-then-claim, sempre):
apri la scheda indicata dal registro → incolla la massima testuale → cita così:
`Cass. pen., Sez. III, n. 23006 del 2026 (dep. 22/06/2026) — massima ufficiale segnalata
dall'Ufficio del Massimario (scheda in KB; PDF ufficiale: <url_pdf dalla scheda>)`.
Il link al PDF autentico VA SEMPRE riportato: è la fonte verificabile con un clic.

**Questioni SU pendenti**: non sono precedenti. Si usano SOLO come segnalazione del
contrasto rimesso alle Sezioni Unite (con data d'udienza) — preziose per istanze di
rinvio, motivi in subordine, strategia. Mai citarle come autorità.

**Corte costituzionale (sezione 4 dell'INDICE)**: la KB contiene di default le pronunce
della Consulta degli **ultimi 10 anni** — dispositivo integrale e massime ufficiali con
parametri normativi (fonte: open data ufficiale); l'archivio completo dal 1956 si scarica
con `--tutto`. Se una pronuncia storica citata non è in KB, dillo ("anteriore alla finestra
sincronizzata") e proponi il sync completo o il link alla scheda ufficiale della Corte —
mai citarla a memoria. Le pronunce scelte dalla Corte per il proprio **Annuario** (rassegna
annuale, dal 2021) portano in frontmatter `annuario:` e `tema_annuario:` e il marcatore
`★ Annuario` nel registro dedicato: utilissime come selezione autorevole per tema
(`grep -rl 'tema_annuario' ...` o grep sul tema). Come si cerca:
- per **numero/anno**: la scheda è `02_GIURISPRUDENZA/CONSULTA/<anno>/{S|O}_<numero>_<anno>.md`;
- per **norma**: `grep -rl "131-bis" KNOWLEDGE_BASE/02_GIURISPRUDENZA/CONSULTA/` (i dispositivi
  e le massime citano le norme testualmente); restringere per anno se servono le recenti.
Come si cita (quote-then-claim): apri la scheda → incolla la massima ufficiale testuale →
`Corte cost., sent. n. 44 del 2026 — massima ufficiale (scheda in KB; testo integrale:
<url_scheda> sul sito della Corte)`. Le declaratorie di illegittimità pesano al **Livello 1**
della gerarchia e travolgono la norma colpita: verificarle SEMPRE quando si lavora su una
fattispecie. Nelle schede non ci sono epigrafe né testo integrale (dati delle parti):
per il testo pieno si segue il link.

**Raccordo Rv**: quando una segnalata compare nel massimario annuale con numero Rv
(campo `rv` valorizzato nella scheda), la citazione con Rv è quella preferita.

---

## MODULO 1 — MAPPA DELLE SEZIONI PENALI DELLA CASSAZIONE

Prima di qualsiasi ricerca, identifica la sezione competente. Ogni sezione ha proprie tendenze interpretative.

| Sezione | Materia principale | Note |
|---|---|---|
| **Prima** | Reati contro lo Stato, criminalità organizzata (art. 416-bis), misure di prevenzione, sequestri di persona | Orientamenti spesso garantisti sulle misure cautelari in ambito mafioso |
| **Seconda** | Furto, rapina, estorsione, ricettazione, riciclaggio, autoriciclaggio, reati contro la fede pubblica | |
| **Terza** | Reati sessuali, reati ambientali, urbanistica, reati in materia di stupefacenti (parte), alcune fattispecie fiscali | Spesso rigorosa sui reati sessuali; più garantista su ambiente |
| **Quarta** | Omicidio colposo, lesioni colpose, sicurezza sul lavoro, responsabilità medica, colpa grave | Terreno della L. Gelli-Bianco e SS.UU. Mariotti 2018 |
| **Quinta** | Reati contro la persona (violenza, stalking), bancarotta e reati fallimentari, reati informatici, diffamazione | |
| **Sesta** | Reati contro la PA (corruzione, concussione, peculato, abuso d'ufficio), associazione per delinquere semplice, reati tributari in parte | Sezione con giurisprudenza più elaborata su corruzione e PA |
| **Sezioni Unite** | Contrasti tra sezioni, questioni di massima importanza (art. 618 c.p.p.) | Vincola tutte le sezioni fino a nuovo contrasto |

**Quando coinvolgere le Sezioni Unite:**
Un contrasto tra sezioni è un argomento difensivo potente in Cassazione. Se esiste un orientamento favorevole di una sezione e uno sfavorevole di un'altra, va segnalato esplicitamente nel ricorso per Cassazione come ragione per investire le SS.UU.

---

## MODULO 2 — COSTRUZIONE DELLA RICERCA GIURISPRUDENZIALE

### Step 1 — Definire la questione giuridica precisa

La ricerca giurisprudenziale fallisce quando la questione è troppo vasta. Scomporla in domande giuridiche specifiche.

**Esempio di cattiva domanda:** "Giurisprudenza sulla corruzione"
**Esempio di buona domanda:** "Orientamenti della Sesta Sezione sul dolo specifico nell'istigazione alla corruzione quando manca risposta del pubblico ufficiale"

### Step 2 — Identificare i principi di diritto rilevanti

Per ogni questione, indicare:
- Il principio di diritto che la difesa vuole affermare
- Il principio di diritto che l'accusa probabilmente citerà
- Se esiste un contrasto tra sezioni su questo punto

### Step 3 — Struttura della citazione giurisprudenziale

**Formato completo (per atti processuali):**
```
Cass. pen., Sez. [numero o Unite], [data udienza/deposito], n. [numero], 
Rv. [numero massimario], imp. [cognome imputato se noto]
```

**Formato minimo accettabile:**
```
Cass. pen., Sez. [numero], n. [numero]/[anno]
```

**Regola fondamentale — ancora o astieniti (PROTOCOLLO_GROUNDING, `KNOWLEDGE_BASE/00_META/PROTOCOLLO_GROUNDING.md`).** Prima di citare una massima cercala nell'indice della KB (`KNOWLEDGE_BASE/_INDICE/INDICE.md` e — sul caso — `FASCICOLI/<caso>/_INDICE/`): se c'è, apri il `.md` alla pagina indicata e incolla la massima testuale con `(fonte, p. N)`; se non c'è, descrivi il principio dichiarando "non presente in KB" e avvisa l'avvocato di verificare su DeJure, OneLeagal o il Massimario prima del deposito. Non inventare mai numeri di sentenza.

---

## MODULO 3 — ORIENTAMENTI PER AREA TEMATICA

Carica il file `references/orientamenti-penale.md` per i principali orientamenti giurisprudenziali per categoria di reato. Usarlo come punto di partenza, non come testo definitivo — la giurisprudenza evolve e va sempre verificata.

---

## MODULO 4 — GIURISPRUDENZA CEDU IN MATERIA PENALE

La Corte EDU non è un quarto grado ma il suo impatto sulla prassi penalistica è crescente. Orientamenti rilevanti:

**Art. 3 CEDU — Trattamento inumano/degradante**
- *Torreggiani e altri c. Italia* (GC, 2013): sovraffollamento carcerario = violazione strutturale. Standard 3 mq per detenuto. Base per reclami sulle condizioni detentive ex artt. 35-ter e 69 Ord. Penit.
- Strumento per chiedere il trasferimento o misure alternative per detenuti in condizioni incompatibili

**Art. 5 CEDU — Libertà personale**
- *Labita c. Italia* (2000): l'onere di giustificazione della custodia cautelare aumenta col passare del tempo
- La durata eccessiva della custodia cautelare può essere denunciata in sede interna (Legge Pinto) e poi a Strasburgo

**Art. 6 CEDU — Equo processo**
- Presunzione di innocenza: qualsiasi dichiarazione pubblica di colpevolezza prima della condanna viola l'art. 6 § 2
- Equità complessiva del processo: la mancanza di contraddittorio nella formazione della prova è un punto sensibile
- Durata ragionevole: rimedio interno prima necessario (Legge Pinto, L. 89/2001)

**Art. 7 CEDU — Legalità penale**
- *Scoppola c. Italia* (GC, 2009): retroattività della lex mitior — l'imputato ha diritto alla pena più favorevole sopravvenuta. Principio applicato dalla Cassazione anche in sede esecutiva
- *Contrada c. Italia* (2015): il reato deve essere prevedibile al momento della condotta. Rilevante per il concorso esterno in associazione mafiosa e per reati nuovi costruiti per via interpretativa

**Art. 8 CEDU — Vita privata e familiare**
- Rilevante per l'esecuzione penale: restrizioni alla vita familiare del detenuto devono essere proporzionate

**Ricorso alla Corte EDU:** termine di 4 mesi dalla decisione interna definitiva (Protocollo 15). Rimedio interno post-condanna CEDU: art. 628-bis c.p.p. (revoca sentenza + riapertura processo).

---

## MODULO 5 — PRINCIPALI CONTRASTI GIURISPRUDENZIALI ATTIVI

Aree dove esistono orientamenti divergenti tra sezioni — da usare come argomenti difensivi o come base per rimessione alle SS.UU.:

**Corruzione:** confine tra corruzione per la funzione (art. 318) e corruzione propria (art. 319) — la distinzione sulla necessità di un atto determinato è stata oggetto di oscillazioni

**Bancarotta fraudolenta:** il nesso causale tra condotta e dissesto — alcune sezioni richiedono causalità stretta (Quinta), altre ammettono una causalità agevolativa

**Stalking:** la soglia dello "stato di ansia" come evento del reato — quanto deve essere provato oggettivamente rispetto alla sola testimonianza della vittima

**Autoriciclaggio:** il confine dell'esclusione per "ordinaria amministrazione del patrimonio personale" — la quinta sezione ha oscillato sulla definizione

**Misure di prevenzione:** standard probatorio per l'accertamento della pericolosità dopo le sentenze CEDU — De Tommaso c. Italia (GC, 2017) ha aperto una breccia sulla determinatezza

Quando individuato un contrasto, segnalarlo esplicitamente nel ricorso per Cassazione come questione da rimettere alle Sezioni Unite (art. 618 c.p.p.) — questo aumenta le probabilità di accettazione del ricorso.

---

## MODULO 6 — INTEGRAZIONE CON IL SISTEMA DI MEMORIA

Quando si trova giurisprudenza rilevante per un fascicolo:

1. Creare un file in `penalista-giurisprudenza/` con naming: `cass-sezX-argomento-anno.md` o `cedu-articolo-anno.md`
2. Usare il formato standard:
```markdown
# [Autorità], [Sezione], [data], n. [numero]
**Argomento:** [tema specifico]
**Massima/Principio:** [testo essenziale]
**Rilevanza per lo studio:** → [[fascicolo-collegato]]
**Note critiche:** [punti di attenzione o limiti del precedente]
```
3. Collegare il file al fascicolo con un wikilink nella sezione "Giurisprudenza di riferimento"
4. Se il precedente è riutilizzabile per più fascicoli, non duplicarlo — linkarlo da ogni fascicolo

---

## Tono e avvertenze

- Distingui sempre tra orientamento consolidato (SS.UU. o indirizzo uniforme di più anni) e orientamento minoritario/isolato
- Segnala quando una massima è stata superata da pronunce successive
- Non citare mai sentenze di cui non sei certo degli estremi — è preferibile descrivere il principio e indicare dove verificarlo
- La giurisprudenza favorevole alla difesa vale tanto quanto quella sfavorevole che l'accusa citerà — mostrare entrambe rafforza la credibilità dell'analisi
