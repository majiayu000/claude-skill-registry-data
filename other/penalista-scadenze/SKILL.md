---
name: penalista-scadenze
description: "Calcolo preciso dei termini processuali penali italiani con ragionamento esplicito e aggiornamento dello scadenziario. ATTIVARE SEMPRE quando l'avvocato chiede di calcolare un termine, una scadenza, una data limite processuale, o dice: 'entro quando devo depositare', 'quando scade il termine per', 'ho ancora tempo per', 'calcola la prescrizione', 'quando matura la prescrizione', 'scade la custodia cautelare il', 'ho quanto tempo per il riesame', 'termine per l'appello', 'scadenza per la Cassazione', 'termini di fase', 'quando posso chiedere le misure alternative'. Attivare anche per la verifica dell'improcedibilita Cartabia (art. 344-bis c.p.p.) e per aggiornare lo SCADENZIARIO del fascicolo."
---

# Skill — Calcolo Termini Processuali Penali

Calcola i termini processuali penali con ragionamento esplicito, passo per passo. Un errore sul termine può costare l'inammissibilità di un'impugnazione o la libertà di un cliente detenuto.

---

## Prima di calcolare

Identifica quale tipo di termine serve. Se mancano informazioni, chiedi solo quelle strettamente necessarie per quel calcolo specifico.

---

## REGOLE GENERALI DI CALCOLO (art. 172 c.p.p.)

Applicare sempre queste regole prima di qualsiasi calcolo:

1. **Dies a quo non computatur** — il giorno iniziale (evento che fa decorrere il termine) NON si conta
2. **La scadenza** cade alla mezzanotte dell'ultimo giorno
3. **Festività e sabato**: se il termine scade in un giorno festivo o di sabato, è automaticamente prorogato al primo giorno non festivo successivo
4. **Sospensione feriale (L. 742/1969 — 1–31 agosto)**: si applica ai termini di impugnazione penale. Eccezioni: misure cautelari (per la parte cautelare), udienza di convalida, termini per il riesame cautelare, atti urgenti. Quando la sospensione feriale si interseca con un termine, aggiungere i giorni di agosto al conteggio.

**Mostrare sempre il ragionamento completo:** evento → dies a quo → eventuale sospensione → dies ad quem.

---

## TERMINI DI IMPUGNAZIONE

### Appello (art. 585 c.p.p.)

**Input necessario:** data dell'avviso di deposito della sentenza (o data del dispositivo se motivazione contestuale)

**Calcolo:**
```
Scenario A — Motivazione contestuale:
Dies a quo: giorno della lettura del dispositivo
Termine: 15 giorni
Sospensione feriale: applicare se il periodo include agosto
Dies ad quem: dies a quo + 15 giorni (escluso dies a quo) ± sospensione

Scenario B — Motivazione depositata dopo (caso ordinario):
Dies a quo: giorno dell'avviso di deposito della sentenza
Termine: 30 giorni
Sospensione feriale: applicare se il periodo include agosto
Dies ad quem: dies a quo + 30 giorni (escluso dies a quo) ± sospensione
```

**Esempio completo:**
Avviso di deposito notificato il 10 luglio.
- Dies a quo: 10 luglio (non si conta)
- Primo giorno del termine: 11 luglio
- 30° giorno: 9 agosto
- Ma 9 agosto cade in sospensione feriale (1-31 agosto)
- I giorni dal 9 al 31 agosto sono 23 giorni → ripartono il 1° settembre
- 1° settembre + 22 giorni rimanenti = 23 settembre
- **Scadenza: 23 settembre**

### Ricorso per Cassazione (art. 585 c.p.p.)

**Input necessario:** data dell'avviso di deposito della sentenza d'appello

**Calcolo:**
```
Dies a quo: giorno dell'avviso di deposito
Termine: 30 giorni (+ sospensione feriale se applicabile)
Per imputato che ricorre in proprio: 45 giorni
```

### Riesame cautelare (art. 309 co. 1 c.p.p.)

**Input necessario:** data di esecuzione della misura o data di notifica dell'ordinanza

**Calcolo:**
```
Dies a quo: giorno dell'esecuzione/notifica
Termine: 10 giorni PERENTORI
Sospensione feriale: NON si applica (misura cautelare)
Dies ad quem: dies a quo + 10 giorni (escluso dies a quo)
```

**Attenzione:** termine perentorio — la tardività produce inammissibilità. Verificare immediatamente appena ricevuta l'ordinanza.

### Appello cautelare (art. 310 c.p.p.)

```
Dies a quo: giorno dell'ordinanza impugnata
Termine: 15 giorni
Sospensione feriale: NON si applica
```

---

## TERMINI DI FASE DELLA CUSTODIA CAUTELARE (art. 303 c.p.p.)

**Input necessario:** data dell'esecuzione della misura, fase processuale, tipo di reato

**Tabella dei termini massimi:**

| Fase | Reati comuni | Reati art. 407 co. 2 |
|---|---|---|
| Indagini preliminari | 3 mesi | 6 mesi (prorogabile a 1 anno) |
| Udienza preliminare | 3 mesi | 3 mesi |
| Dibattimento primo grado | 6 mesi | 1 anno |
| Appello | 6 mesi | 1 anno |
| **Cassazione** | **45 giorni** | **3 mesi** |

**Calcolo:**
```
Data inizio custodia nella fase: [data esecuzione / trasmissione atti al giudice della fase]
Durata massima nella fase: [dalla tabella]
Scadenza del termine di fase: data inizio + durata massima
```

**Attenzione al cambio di fase:** il termine riparte all'inizio di ogni nuova fase processuale. Monitorare la trasmissione degli atti tra fasi.

**Se il termine di fase è già scaduto o prossimo:** segnalare come **PRIORITÀ ASSOLUTA** e preparare immediatamente istanza di scarcerazione per decorrenza termini.

---

## PRESCRIZIONE

**Input necessario:** reato contestato, data del fatto, regime applicabile (ante/post 1° gennaio 2020), eventuali interruzioni e sospensioni

### Step 1 — Identificare il regime

- **Fatto commesso dal 1° gennaio 2020 in poi → Regime Bonafede (L. 3/2019)**
  La prescrizione si sospende definitivamente dopo la sentenza di primo grado.
  Calcolare solo il periodo fino alla sentenza di primo grado.

- **Fatto commesso prima del 1° gennaio 2020 → Regime pre-Bonafede**
  La prescrizione continua a decorrere durante i gradi di impugnazione.
  Calcolare l'intero percorso.

### Step 2 — Calcolare il termine base

```
Termine base = massimo della pena edittale (per il delitto nel suo tipo base)
Minimo: 6 anni per delitti, 3 anni per contravvenzioni
Reati ostativi (art. 51 co. 3-bis c.p.p.): termine raddoppiato
Recidiva reiterata: aumento di 1/4
```

**Come trovare il massimo edittale:** dalla norma incriminatrice. Esempio: corruzione propria art. 319 c.p. → pena da 6 a 10 anni → termine base = 10 anni.

### Step 3 — Identificare interruzioni e sospensioni

**Cause di interruzione (art. 160 c.p.):** ogni atto del procedimento che comporta interruzione (sentenza di condanna, decreto penale di condanna, interrogatorio dell'imputato, richiesta di rinvio a giudizio, ecc.). Dopo ogni interruzione, il termine ricomincia da capo, ma non può superare il termine base aumentato di 1/4.

**Cause di sospensione (art. 159 c.p.):** tassative — autorizzazione a procedere, rogatoria internazionale, sospensione del procedimento per legittimo impedimento, ecc. Durante la sospensione il termine non decorre.

### Step 4 — Calcolo finale

```
Data del fatto: [X]
Termine base: [Y anni]
Prima interruzione: [data e tipo atto]
→ Nuovo dies a quo per il termine: [data interruzione]
Termine massimo post-interruzione: termine base + 1/4
[Ripetere per ogni interruzione]
[Sottrarre le sospensioni]
Data di maturazione: [X + Y anni + sospensioni - interruzioni]
```

**Presentare sempre il risultato in questo formato:**
- Regime applicabile: [Bonafede / pre-Bonafede]
- Termine base: [X anni]
- Data di maturazione (in assenza di ulteriori interruzioni): [data]
- **Se già maturata: SEGNALARE COME PRIORITÀ ASSOLUTA**
- Se prossima (< 6 mesi): segnalare e pianificare l'eccezione

---

## IMPROCEDIBILITÀ CARTABIA (art. 344-bis c.p.p.)

*Applicabile ai procedimenti in cui la sentenza di primo grado è pronunciata dal 1° gennaio 2020*

**Input necessario:** data della sentenza di primo grado, fase attuale (appello / Cassazione)

**Calcolo:**
```
Appello:
Dies a quo: data della sentenza di primo grado
Termine: 2 anni
Proroga possibile: + 1 anno per reati gravi (art. 51 co. 3-bis/3-quater, ergastolo, processi complessi)
Scadenza: data sentenza I grado + 2 anni (+ 1 anno se proroga)

Cassazione:
Dies a quo: data della sentenza d'appello
Termine: 1 anno
Proroga possibile: + 6 mesi
Scadenza: data sentenza appello + 1 anno (+ 6 mesi se proroga)
```

**Come usarlo in chiave difensiva:**
- Monitorare proattivamente i termini
- Se il termine si avvicina e il procedimento non è concluso, sollevare la questione davanti al giudice
- La dichiarazione di improcedibilità estingue l'azione penale — equivale all'assoluzione per effetti pratici sulla libertà del cliente

---

## TERMINI DELL'UDIENZA DI CONVALIDA (art. 391 c.p.p.)

```
Arresto / fermo avvenuto: [data e ora]
Comunicazione al PM: entro 24 ore dall'arresto
Comunicazione al GIP e richiesta di convalida: entro 24 ore dalla comunicazione al PM
Udienza di convalida: il GIP la fissa entro 48 ore dalla comunicazione
Termine totale massimo: 96 ore dall'arresto

Scadenza delle 96 ore: [data e ora dell'arresto] + 96 ore
```

Se le 96 ore scadono senza udienza di convalida: **la misura precautelare perde efficacia automaticamente** — istanza immediata di scarcerazione.

---

## TERMINI DELLE INVESTIGAZIONI DIFENSIVE

```
Deposito di atti di investigazione difensiva durante le indagini:
→ Fino alla chiusura delle indagini (termine di durata delle indagini)
→ In UP: fino all'udienza
→ In dibattimento: prima della dichiarazione di apertura (art. 493 c.p.p.) per l'inserimento nel fascicolo del dibattimento
```

---

## Output dell'analisi

Al termine del calcolo, presentare sempre:

```
TIPO DI TERMINE: [descrizione]
NORMA APPLICATA: [articolo e comma]
EVENTO DI DECORRENZA: [fatto e data]
DIES A QUO: [data — non computato]
CALCOLO: [step by step]
SOSPENSIONI APPLICATE: [sì/no — quali]
DIES AD QUEM: [data]
LIVELLO DI URGENZA: [CRITICO / ALTA / NORMALE]
AZIONE RICHIESTA: [cosa fare e entro quando]
```

Aggiornare [[SCADENZIARIO]] con il termine calcolato, indicando fascicolo, tipo termine e dies ad quem.
