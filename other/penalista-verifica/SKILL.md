---
name: penalista-verifica
description: "Controllo qualita' pre-deposito di un atto processuale penale. ATTIVARE SEMPRE quando l'avvocato dice: 'verifica l'atto', 'controlla prima del deposito', 'e' pronto per il deposito?', 'ricontrolla le citazioni', 'verifica i termini', 'controllo finale', 'revisiona la memoria', 'check finale', o quando un atto prodotto con penalista-atti sta per essere consegnato/depositato. Attivare anche d'ufficio: proporre la verifica al termine della redazione di qualsiasi atto destinato al deposito (memoria, appello, ricorso, istanza)."
---

# Skill — Verifica pre-deposito

Questa skill è il controllo qualità dello studio: un riesame **indipendente e sistematico** dell'atto prima che esca. Il suo principio: *l'atto si difende da solo solo se ogni affermazione regge alla verifica*.

## Quando attivarla

- Su richiesta esplicita dell'avvocato.
- **D'ufficio:** al termine della redazione di ogni atto destinato al deposito, proporre: *"Vuole che esegua la verifica pre-deposito? Controllo citazioni, termini e coerenza con il fascicolo."*

## Metodo: verifica indipendente

Se l'ambiente consente di lanciare un agente di verifica separato (subagente), **usarlo**: il verificatore non deve essere influenzato dal contesto di chi ha scritto l'atto. Istruirlo a leggere SOLO l'atto, il fascicolo e la Knowledge Base — non la conversazione di redazione. Se il subagente non è disponibile, eseguire la checklist direttamente, dichiarandolo.

## CHECKLIST DI VERIFICA (eseguire tutta, nell'ordine)

### 1. Citazioni giurisprudenziali — la verifica più importante

Per OGNI sentenza citata nell'atto:

| Esito | Criterio | Azione |
|---|---|---|
| ✅ VERIFICATA | Presente nell'indice della KB — registro citazionale di `KNOWLEDGE_BASE/_INDICE/INDICE.md` (o `FASCICOLI/<caso>/_INDICE/`) — con **riscontro testuale** della massima alla pagina indicata (PROTOCOLLO_GROUNDING) | Nessuna |
| ⚠️ NON IN KB | Non presente nell'indice della KB (non riscontrabile nei registri) | La citazione va resa testuale dall'indice oppure dichiarata "non presente in KB"; suggerire verifica su Italgiure / DeJure / Portale del Massimario |
| ❌ SOSPETTA | Estremi incoerenti (sezione/anno/numero non plausibili), massima che non corrisponde alla fonte | Segnalare in rosso: NON depositare senza verifica umana |

**Mai declassare una citazione a "verificata" per somiglianza.** La verifica richiede riscontro testuale della massima, non solo degli estremi.

### 2. Termini e date

- Ricalcolare **da zero** ogni termine menzionato nell'atto (non fidarsi del calcolo fatto in redazione): regole art. 172 c.p.p., sospensione feriale, giorni festivi.
- Confrontare con lo SCADENZIARIO del fascicolo: coincidono? Se no, segnalare la divergenza — è un errore in uno dei due posti.
- Verificare la coerenza interna delle date (notifica, decorrenza, deposito).

### 3. Coerenza atto ↔ fascicolo

- I fatti affermati nell'atto corrispondono a quanto risulta dal fascicolo? Ogni affermazione fattuale ha la sua fonte (atto + pagina)?
- Il capo di imputazione citato è identico a quello del fascicolo (articoli, commi, aggravanti)?
- Nomi, R.G.N.R., autorità procedente, dati anagrafici: corrispondono?
- L'atto contraddice posizioni assunte in atti precedenti dello stesso procedimento? (Se sì: segnalare — può essere voluto, ma l'avvocato deve saperlo.)

### 4. Requisiti formali dell'atto

- Intestazione completa e corretta (dati studio da CLAUDE.md)
- Autorità destinataria corretta per il tipo di atto
- Sottoscrizione, procura/nomina richiamata dove necessario
- Conclusioni: presenti, univoche, coerenti con i motivi

### 5. Normativa citata

- Gli articoli citati esistono e dicono ciò che l'atto afferma? Se il testo normativo è in `penalista-fonti/`, riscontrare sul testo; altrimenti marcare [VERIFICARE su Normattiva].
- Norme toccate da riforme recenti: controllare [[AGGIORNAMENTO_NORMATIVO_2025-2026]] (es. termini cautelari, interrogatorio preventivo, nuove fattispecie L. 80/2025).

## FORMATO DEL REPORT

```
# VERIFICA PRE-DEPOSITO — [nome atto] — [data]

## Esito complessivo: 🟢 PRONTO / 🟡 DEPOSITABILE CON RISERVE / 🔴 NON DEPOSITARE

## 1. Citazioni giurisprudenziali   [n. verificate / n. da verificare / n. sospette]
[elenco per esito, con motivazione]

## 2. Termini e date                [✅ / ⚠️ con dettaglio]
## 3. Coerenza con il fascicolo     [✅ / ⚠️ con dettaglio]
## 4. Requisiti formali             [✅ / ⚠️ con dettaglio]
## 5. Normativa                     [✅ / ⚠️ con dettaglio]

## Azioni richieste prima del deposito
1. [azione concreta, in ordine di gravità]
```

Salvare il report nel fascicolo come `verifica-[atto]-[data].md` e collegarlo al fascicolo.

## Regole finali

- **L'esito 🟢 non sostituisce la revisione del difensore.** Dirlo sempre: ogni atto resta una bozza fino alla revisione personale dell'avvocato (regola n. 7 del kit).
- Se anche una sola citazione è ❌ SOSPETTA, l'esito complessivo non può essere 🟢.
- La verifica è un fatto di metodo, non di sfiducia: proporla sempre, anche per gli atti semplici.
