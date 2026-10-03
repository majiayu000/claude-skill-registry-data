---
name: notifications-guide
description: Använd INNAN du bygger en notifikation, för att avgöra vilken status (Informational/Success/Warning/Error/E-Com) och komponenttyp (Toast/Inline/Banner/Modal/Notification panel) som passar situationen. Läs sedan skillen för den specifika komponenttypen (toast-system, inline-notification, banner-notification, modal-ecom eller toast-ecom).
---

> Del av designsystemet i swedol-ui-prototype. Se `CLAUDE.md` för teknikstack, mallregler, breakpoints och kvalitetschecklistan som alltid gäller utöver denna spec.

## Notifikationer – Användningsriktlinjer (ECO Design System)

**Figma:** https://www.figma.com/design/42MgqJjV9vfplwQnrUB62r/ECO-Design-System?node-id=6709-216647

---

### Vilken status ska användas?

| Status | Användning | Varaktighet | Färg |
|---|---|---|---|
| **E-Com** | Produkthantering: kundvagn, favoriter, urklipp | Ej obligatorisk — kan auto-stänga eller ligga kvar | Brand (svart/vit) |
| **Informational E-Com** | Kampanjinfo relevant för användaren | — | Info (`#0066ff`) |
| **Informational** | Tilläggsinfo, ej nödvändigtvis kopplad till aktiv uppgift | — | Info (`#0066ff`) |
| **Success** | Bekräftar att uppgift slutförts med förväntat resultat | Löser sig ofta automatiskt | Success (`#248616`) |
| **Warning** | Informerar om att aktuell åtgärd kanske inte är optimal | Kvarstår tills avfärdad eller uppgift genomförd | Warning (`#fac000`) |
| **Error** | Kritiskt fel, kan blockera framsteg tills löst eller avfärdad | Kvarstår tills löst eller avfärdad | Danger (`#d90000`) |

---

### Vilken komponenttyp ska användas?

| Typ | Användning | Varaktighet / Interaktion |
|---|---|---|
| **Inline Default** | Icke-störande feedback/status som är relevant för aktuell uppgift | Kvarstår tills löst |
| **Toast** | Kortlivade, tidsbaserade meddelanden — glider in/ut | Auto-stänger eller stängs av användaren |
| **Inline Actionable** | Interaktiva komponenter i inline- eller toast-stil | Kvarstår eller tas bort automatiskt |
| **Banner** | Globala/systemnotiser, full bredd, överst på sidan | Kan vara kampanjlång eller permanent |
| **Notification panel** | Systemgenererade meddelanden om kontot | Öppnas/stängs av användaren (drawer) |
| **Modal** | Hög störningsgrad — kräver omedelbar uppmärksamhet eller åtgärd | Blockerar UI tills avfärdad |

---

### Notifieringskategorier

ECO Design System skiljer på **task-generated** och **system-generated** notiser:

- **Task-generated**: utlöses av en direkt användaråtgärd (spara, skicka, ta bort). Visas i Toast eller Inline.
- **System-generated**: utlöses av systemhändelser utan direkt användarinteraktion (avisering om nytt meddelande, kontostatus). Visas i Notification panel eller Banner.

---

### Ikonanvändning

Reserverade ikoner per status — använd alltid rätt ikon och variant:

| Status | Material Symbol | Variant |
|---|---|---|
| **Informational** | `info` | Outlined / wght 300 / Filled |
| **Error** | `error` | Outlined / wght 300 / Filled |
| **Success** | `check_circle` | Outlined / wght 300 / Filled |
| **Warning** | `warning_amber` | Outlined / wght 300 / Filled |
| **E-Com Informational** | Valfri från galleri | Outlined / wght 300 |

> Ikonerna är reserverade per status och ska **inte** bytas ut mot andra ikoner för System-notifikationer. E-Com Informational är det enda undantaget.

---

### Avfärdning (Dismiss)

Alla notifikationer som kan stängas av användaren ska stödja minst ett av följande:

| Metod | Används i |
|---|---|
| **× (stäng-knapp)** | Toast, Inline, Banner, Modal |
| **Klick utanför** | Modal (klick på overlay stänger) |
| **ESC-tangent** | Modal |
| **Auto-dismiss** | Toast (Success, E-Com) |

> Modal ska **alltid** ha × i header, stödja ESC och stänga vid klick på overlay — dessa tre dismiss-mekanismer är obligatoriska.

---

### Mobil – höjd och position

- En toast på mobil ska använda `width: 375px` (eller `100%` om viewport är smalare).
- En inline-notifikation kan ha `height: auto` baserat på innehållet.
- En banner upptar alltid `width: 100%` och placeras överst på sidan.
- En modal på mobil kan ha `height: 100%` av skärmen eller anpassa sig efter innehållet och hålla sig fast längs nederkanten.

---
