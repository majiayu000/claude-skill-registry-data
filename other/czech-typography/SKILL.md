---
name: czech-typography
description: Czech typography rules for web development. Use when building web pages in Czech language, writing Czech content, or fixing typography issues in Czech text. Covers punctuation, dashes, quotes, numbers, units, non-breaking spaces, and HTML entities.
---

# Česká typografie pro web

## Interpunkce

| Znak        | Pravidlo                      | Příklad                       |
| ----------- | ----------------------------- | ----------------------------- |
| . , ; : ? ! | Bez mezery před, mezera za    | `Text, další text.`           |
| ( )         | Mezera vně, bez mezery uvnitř | `Text (v závorce) pokračuje.` |
| „ "         | Těsně k textu, tvar 99–66     | `Řekl: „Ahoj."`               |
| ‚ '         | Vnořené uvozovky              | `„Řekl: ‚Ahoj.'"`             |

## Pomlčka vs. spojovník

| Znak          | Použití                       | Příklad                              |
| ------------- | ----------------------------- | ------------------------------------ |
| - (spojovník) | Složená slova, bez mezer      | `česko-anglický`, `modro-bílý`       |
| – (pomlčka)   | Rozsah jednoslovný, bez mezer | `8–16 h`, `Praha–Brno`, `str. 10–15` |
| – (pomlčka)   | Rozsah víceslovný, s mezerami | `Karlovy Vary – Liberec`             |
| – (pomlčka)   | Vsuvka, s mezerami            | `Text – poznámka – pokračuje.`       |

## Lomítko

- Jednoslovné výrazy: **bez mezer** → `a/nebo`, `km/h`, `2024/2025`
- Víceslovné výrazy: **s mezerami** → `černá / bílá / šedá varianta`

## Čísla

- Desetinná čárka bez mezer: `3,14`
- Tisíce s nedělitelnou mezerou: `1 234 567`
- Datum: `1. 1. 2025` nebo `01.01.2025` (formální)
- Čas: `14.30` nebo `14:30`

## Procenta a jednotky

- `10 %` = deset procent (s mezerou)
- `10% sleva` = desetiprocentní sleva (bez mezery, přídavné jméno)
- `100 Kč`, `25 kg`, `18 °C` – vždy mezera před jednotkou

## Nedělitelná mezera

Vkládej `&nbsp;` nebo CSS `white-space: nowrap` za:

- Jednopísmenné předložky: `v`, `s`, `k`, `z`, `u`, `o`
- Jednopísmenné spojky: `a`, `i`
- Tituly: `Ing.`, `Mgr.`, `p.`
- Čísla před jednotkami: `100 Kč`

## Zkratky

- `s. r. o.` (s mezerami, ne `s.r.o.`)
- `a. s.`, `v. o. s.`
- `atd.`, `apod.`, `např.`, `tj.`, `tzn.`
- `viz` – není zkratka, bez tečky

## HTML entity

```
&nbsp;   – nedělitelná mezera
&ndash;  – pomlčka (–)
&mdash;  – dlouhá pomlčka (—)
&bdquo;  – otevírací uvozovka („)
&ldquo;  – zavírací uvozovka (“)
&hellip; – výpustka (…)
```

## Zdroje

- [Internetová jazyková příručka ÚJČ](https://prirucka.ujc.cas.cz/)
- ČSN 01 6910:2014
- Filip Blažek: Typokniha
