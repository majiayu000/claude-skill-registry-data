---
name: fr-cfe
description: "Use this skill whenever asked about the French Cotisation Foncière des Entreprises (CFE) for self-employed individuals. Trigger on phrases like \"CFE France\", \"Cotisation Foncière\", \"cotisation foncière des entreprises\", \"CET France\", \"CFE auto-entrepreneur\", \"taxe professionnelle\", \"CFE micro-entreprise\", or any question about local business tax obligations for a self-employed client in France. Covers the rental value base, municipal rates, first-year exemption, and minimum contribution. ALWAYS read this skill before touching any France CFE work."
license: "AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)"
metadata:
  source: openaccountants
  openaccountants_url: "https://www.openaccountants.com/skills/fr-cfe"
  jurisdiction: "FR"
  tax_year: "2026"
  last_updated: "2026-10-19"
  authored_by: "Michael Cutajar and the OpenAccountants team"
  trust_label: "Built by Michael Cutajar and the OpenAccountants team"
  review_status: "pending_review"
---

# France: the cotisation foncière des entreprises (CFE), with the CVAE and the CET cap

This skill works out whether a business in France owes the cotisation foncière des entreprises (CFE), on what base, by when it is paid, which exemptions and reductions apply, and when the cap on the contribution économique territoriale (CET, which is the CFE plus the CVAE) gives money back. Figures are for tax year 2026. The 2025 figures govern the CVAE for 2025 settled on form 1329-DEF in May 2026 and the CET cap claimed for 2025 by 31 December 2026, while the figures in force during 2026 (the 2026 minimum-base table, the 2026 CVAE rates and relief, and the 2026 cap rate) govern the CFE and the CVAE charged for 2026. The CFE for 2026 is assessed on the premises used and the turnover made in 2024, the year N-2. The rules stated are those in force on 19 October 2026, read on official pages between 19 September and 19 October 2026; each page's own date stamp is given in the Sources section.

## Skill Metadata

**Skill Metadata**

| Field | Value |
| --- | --- |
| Jurisdiction | France |
| Jurisdiction Code | FR |
| Primary Legislation | Code général des impôts (CGI), articles 1447 to 1478 bis (CFE), as listed on the service-public CFE page |
| Supporting Legislation | CGI art. 1647 D (minimum base); art. 1647 B sexies (CET cap); art. 1586 quater (CVAE rate and relief) |
| Tax Authority | DGFiP (Direction générale des finances publiques), through the service des impôts des entreprises (SIE) |
| Official sources used | entreprendre.service-public.gouv.fr, impots.gouv.fr, bofip.impots.gouv.fr (see Sources) |
| Status | Source-cited draft, not yet reviewed by a French expert-comptable |
| Refresh date | 19 October 2026 |

## Confidence Tier Definitions

- **[T1] Tier 1, deterministic**: apply exactly as written.
- **[T2] Tier 2, reviewer judgement required**: flag and present the options.
- **[T3] Tier 3, out of scope**: escalate, do not guess.

## The method, step by step

1. **Is the activity within the CFE at all?** The CFE is due where the activity is carried on in France, habitually, on a professional footing and not as an employee. Letting premises has its own entry tests (table "Who is within the CFE" below). Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547 (CGI art. 1447).
2. **Was the business active on 1 January of the tax year?** The CFE is due each year by any business that carries on its non-salaried activity habitually on 1 January of the year of assessment. A business created during the year owes nothing for that year (step 4). Source: https://www.impots.gouv.fr/sites/default/files/media/3_Documentation/depliants/pro_fiche_cet-ifer_2026.pdf
3. **Does an exemption apply?** Check the automatic exemptions (artisans working only with apprentices, certain taxi drivers, artists, authors and the others in Step 5), the small-turnover exemption for a business on the minimum base, and any exemption the commune has granted. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547
4. **Creation year.** A new business is exempt for the year it starts, up to 31 December of that year. To get the exemption it files form 1447-C-SD (déclaration initiale), on paper, with its SIE before 31 December of the creation year. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547
5. **Find the real base.** Take the rental value (valeur locative) of the property subject to taxe foncière that the business used for its activity in year N-2. Apply any reduction in the reductions table (industrial, artisan with up to three employees, Corsica, the half base in the year after creation). Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547 (CGI art. 1498 to 1498 bis for the rental value).
6. **Compare with the commune's minimum base.** Find the turnover band from the N-2 turnover excluding VAT over 12 months. The commune fixes a minimum base inside the band's range in the minimum-base table. If the real base is lower than that minimum, or the business has no premises, the minimum base is used instead, at the principal establishment. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547 (CGI art. 1647 D).
7. **Apply the commune's rate.** Multiply the base by the rate voted for the place of the establishment. The rates are published on impots.gouv.fr in the service "Connaître les taux d’impositions directes locales par commune" (choose the year, the region, then the department). Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547
8. **Add the chamber tax and the management fee.** The taxe additionnelle for the chambers of commerce is a percentage of the CFE base, and the management fee is a percentage of the CFE plus that tax (table "What is added to the CFE"). A micro-entrepreneur pays the chamber taxes through URSSAF, not on the CFE notice. Sources: https://entreprendre.service-public.gouv.fr/vosdroits/F23547 and the 2026 fiche above.
9. **Pay.** The notice is online only, in the espace professionnel on impots.gouv.fr. The balance is due by 15 December. A business whose CFE for the previous year reached the acompte threshold pays half of that amount in advance in June unless it is on monthly direct debit. Any payment must be by an electronic means (online, monthly debit, or debit at the due date). Source: the 2026 fiche above and https://entreprendre.service-public.gouv.fr/vosdroits/F23547
10. **Report changes on 1447-M-SD.** A request for an exemption, a change in the surface of the premises, a change in the number of employees, crossing the bare-letting threshold, or a cessation goes on form 1447-M-SD, to the SIE, before the 2nd working day after 1 May. For the CFE due in 2027 the date is 5 May 2026. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547
11. **Check the CVAE and the CET cap.** A business with turnover above the CVAE entry threshold files form 1330-CVAE even if no CVAE is payable (Step 6.5). If CFE plus CVAE exceed the cap rate times the value added, claim the relief on form 1327-CET-SD (régime réel) or 1327S-CET-SD (micro), before 31 December of the year after the CFE was put into collection. Sources: https://entreprendre.service-public.gouv.fr/vosdroits/F23548 and https://bofip.impots.gouv.fr/bofip/2594-PGP.html

## Ask the client first

- When did the business start, and has it ever changed hands? The creation year is exempt and the next year is on a half base; a transfer during the year leaves the old operator liable for the whole year.
- In which commune is the principal establishment, and are there other premises? The commune sets both the rate and the minimum base.
- Does the business use premises of its own or rented premises, or does it work from home or at clients' sites? Without premises, the minimum base applies.
- What was the turnover excluding VAT in year N-2 (2024 for the CFE due in 2026), restated to 12 months if the year was short? This picks the minimum-base band and the small-turnover exemption.
- What is the activity, and does the client employ anyone other than apprentices? Artisans, taxi drivers, artists, authors and others may be exempt, and an artisan with up to three employees gets a base reduction.
- Was the CFE for last year at or above the acompte threshold, and is the client on monthly direct debit? This decides whether a June acompte is due.

## Step 0: Client Onboarding Questions

Before computing, you MUST know:

1. **Activity type** [T1]: entreprise individuelle, micro-entreprise or auto-entrepreneur, profession libérale, or société. Micro-entrepreneurs are within the CFE, including when they work from home or at their clients'.
2. **Year of creation** [T1]: the creation year is exempt and the following year is on a half base.
3. **Location of the principal establishment and any other premises** [T1]: the commune decides the rate and the minimum base.
4. **Type of premises** [T1]: home-based (domiciliation), rented office, owned premises, or none.
5. **Chiffre d'affaires or recettes of year N-2, excluding VAT** [T1]: picks the minimum-base band and the small-turnover exemption.
6. **Any exemption claimed or granted** [T2]: artisan, taxi, artist, author, a zone (ZAFR, ZAIPME, ZFRR, QPV, ZRD, BER and the others in Step 5), a 3-year commune exemption for a new establishment.

**If the commune is unknown, STOP. Each commune votes its own rate and its own minimum base.**

## Step 1: What is CFE? [T1]

- **CFE definition**: the CFE is a local tax due by any business or person carrying on a non-salaried professional activity, unless exempt. Together with the CVAE it makes up the contribution économique territoriale (CET). Source: https://www.impots.gouv.fr/sites/default/files/media/3_Documentation/depliants/pro_fiche_cet-ifer_2026.pdf
- **Who is liable**: any company, any entity without legal personality, and any individual entrepreneur, micro-entrepreneurs included, even when working from home or at clients' sites. Employees are not concerned.
- **Composition**: amount payable = CFE + taxe additionnelle (chamber tax) + frais de gestion. The service-public page states it in those words: "CFE due + taxe additionnelle + frais de gestion".
- **CFE itself**: base × the rate of the commune (or of the EPCI, the intercommunal body that receives it).

**Who is within the CFE**

| Situation | Value | Note |
| --- | --- | --- |
| Source | all figures below | https://entreprendre.service-public.gouv.fr/vosdroits/F23547 |
| Letting or sub-letting BARE premises: within the CFE once turnover or gross receipts excluding VAT are at least this amount. Letting bare premises for residential use is outside the CFE at any amount | EUR 100,000 | "doivent être au moins égaux à" / "la CFE ne concerne pas la location et sous-location d'immeubles nus à usage d'habitation" |
| Letting or sub-letting FURNISHED premises: within the CFE once turnover or gross receipts excluding VAT are more than this amount. No CFE where the furnished let is part of the owner's main home | EUR 5,000 | "doivent être supérieurs à" / "la CFE n’est pas due lorsque la location meublée porte sur un logement inclus dans la résidence principale du propriétaire" |

The general conditions apply whatever the activity, the tax regime or the nationality: the activity is carried on in France, habitually (repeatedly), professionally (not a non-profit activity and not the mere management of private wealth), and not as an employee. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547

## Step 2: Tax Base (Base Imposable) [T1]

**Legislation:** CGI art. 1447 to 1478 bis; rental value under CGI art. 1498 to 1498 bis (articles named on https://entreprendre.service-public.gouv.fr/vosdroits/F23547).

### Standard Base

- **Standard base**: the rental value of the property subject to taxe foncière that the business used for its professional activity in year N-2. For the CFE due for 2026, that is the premises used in 2024. The service-public page gives that example in terms: "Pour calculer la CFE due au titre de 2026, il faut prendre en compte le local commercial utilisé en 2024".
- The rental value is an administrative value of the property. It is NOT the rent the business actually pays.
- **Reference period**: in most cases the second calendar year before the year of assessment (N-2). Source: https://www.impots.gouv.fr/sites/default/files/media/3_Documentation/depliants/pro_fiche_cet-ifer_2026.pdf

### For Home-Based Businesses

- **Home-based business rule**: an entrepreneur who has no premises and works from home or at clients' sites still owes the CFE. It is then a rate applied to a minimum base, and both vary with the commune where the business is domiciled. The place of domiciliation can be the entrepreneur's home or another address under a commercial domiciliation contract. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547

### Reduction for New Establishments

- **Year after creation**: in the year following its creation, a new business gets the reduction of its base shown in the reductions table. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547
- **Base for a new establishment**: for the two years after the year of creation, the base is the property subject to taxe foncière that the business had at its disposal on 31 December of its first year of activity. Source: https://www.impots.gouv.fr/sites/default/files/media/3_Documentation/depliants/pro_fiche_cet-ifer_2026.pdf

**Reductions of the base**

| Reduction | Value | Note |
| --- | --- | --- |
| Source | all figures below | https://entreprendre.service-public.gouv.fr/vosdroits/F23547 |
| Industrial establishments: reduction of the rental value | 30% | "pour les établissements industriels" |
| New business, in the year following its creation: reduction of its base | 50% | "L'année suivant leur création, les nouvelles entreprises bénéficient d'une réduction" |
| Artisan not wholly exempt, with 1 employee (apprentices not counted) | 75% | "employant 3 salariés maximum" |
| Artisan not wholly exempt, with 2 employees | 50% | "pour 2 salariés" |
| Artisan not wholly exempt, with 3 employees | 25% | "pour 3 salariés (sans compter les apprentis)" |
| Condition for the artisan reduction: pay for labour (profit, wages paid and social contributions) is more than this share of the artisan's total turnover including VAT | 50% | "représente plus de" ... "du chiffre d'affaires global TTC de l'artisan" |
| Establishment in Corsica | 25% | "en cas d'implantation en Corse" |

Seasonal businesses (restaurants or cafés, for example) have their rental value reduced for the period of inactivity. The page gives no figure for it.

## Step 3: Municipal Rates [T2]

- **Municipal rate**: each commune (or EPCI) votes its CFE rate. At equal turnover, two businesses in two communes do not pay the same CFE. The page names the place as the commune where the business has its principal establishment. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547
- **Where to find it**: the impots.gouv.fr service "Connaître les taux d’impositions directes locales par commune" (choose the accounting year, the region, then the department), linked from the service-public CFE page.

**[T2] The rate is commune-specific. Do not compute without the commune's rate for the year. Earlier versions of this skill gave a typical range of rates; no official page read prints one, and it has been removed.**

## Step 4: Cotisation Minimum (Minimum CFE) [T1]

- **Minimum base rule**: the real base (the rental value of the property used in N-2) may not be lower than a minimum base, which varies with the commune where the business is domiciled. If it is lower, or there are no premises, the CFE is computed on the minimum base. The band depends on the turnover excluding VAT made over 12 months in year N-2. The commune picks a figure inside the band's range: the table gives a range, never a single amount. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547 (CGI art. 1647 D).
- **Several establishments**: the CFE on a minimum base is due at the principal establishment, which is not always the registered office.

### Minimum CFE Brackets (2026)

**Minimum base for the CFE due in 2026, by turnover excluding VAT of year N-2 (the commune sets the figure inside the range)**

| Turnover excluding VAT in N-2 | Minimum base, lowest | Minimum base, highest |
| --- | --- | --- |
| Source | all figures below | https://entreprendre.service-public.gouv.fr/vosdroits/F23547 |
| EUR 10,000 or less | EUR 250 | EUR 597 |
| EUR 10,001 to EUR 32,600 | EUR 250 | EUR 1,194 |
| EUR 32,601 to EUR 100,000 | EUR 250 | EUR 2,509 |
| EUR 100,001 to EUR 250,000 | EUR 250 | EUR 4,183 |
| EUR 250,001 to EUR 500,000 | EUR 250 | EUR 5,974 |
| EUR 500,001 or more | EUR 250 | EUR 7,769 |

The page heads the table "Base minimum de CFE due en 2026 (selon la commune)". The amounts are BASES, to which the commune's rate is then applied. They are not amounts of tax. A commune's minimum base is never one of the band ends unless the commune chose it.

**Small-turnover exemption**

| Rule | Value | Note |
| --- | --- | --- |
| Source | all figures below | https://entreprendre.service-public.gouv.fr/vosdroits/F23547 |
| A business on the minimum base is exempt from the CFE where its turnover excluding VAT of year N-2 did not exceed this amount. A business created in N-1 qualifies if its turnover of that first year (N-1) did not exceed it. The turnover may need restating to 12 months, pro rata to the real period of activity | EUR 5,000 | "n'a pas dépassé" |

The 2026 fiche from impots.gouv.fr describes the same exemption as one "en faveur des entreprises soumises à la base minimum dont le montant de chiffre d'affaires ou de recettes au cours de la période de référence est inférieur ou égal" to that amount (https://www.impots.gouv.fr/sites/default/files/media/3_Documentation/depliants/pro_fiche_cet-ifer_2026.pdf).

### Micro-Entrepreneurs / Auto-Entrepreneurs

- **Micro-entrepreneur CFE liability**: micro-entrepreneurs are within the CFE on the same basis as any individual entrepreneur, including when they work from home or at clients' sites. With no premises, the minimum base applies. The creation-year exemption and the small-turnover exemption apply to them as to anyone else. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547
- **Chamber taxes**: a micro-entrepreneur pays the taxe additionnelle (chamber of commerce tax) through the autoentrepreneur.urssaf.fr account, not with the CFE, and the chamber taxes then do not appear on the CFE notice. Sources: https://entreprendre.service-public.gouv.fr/vosdroits/F23547 and https://www.impots.gouv.fr/sites/default/files/media/3_Documentation/depliants/pro_fiche_cet-ifer_2026.pdf

## Step 5: Exemptions [T1]

- **Two kinds**: automatic exemptions (de plein droit), usually permanent and usually with no declaration; and optional exemptions (facultatives), granted by the commune or EPCI, usually temporary, and requested on form 1447-M-SD (with annex 1447-E if the activity is not listed, and form 1465-SD for some zones such as ZAFR, ZAIPME and ZFRR). Each form is filed on paper with the SIE. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547

### First-Year Exemption (Année de création)

- **First-year exemption**: a business is exempt from the CFE for the year it is created, up to 31 December of the year it starts. It must request the exemption on form 1447-C-SD (déclaration initiale), filed with the SIE before 31 December of that year so that the base can be set for the following year. In the following year its base is reduced as shown in the reductions table. Example: a business created on 15 March 2026 owes no CFE for 2026, files 1447-C-SD before 31 December 2026, and receives its first notice for 2027 on the reduced base. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547
- **New businesses and the CVAE**: new businesses are not liable to the CVAE in the year of their creation, except where an activity is transferred. Source: https://www.impots.gouv.fr/sites/default/files/media/3_Documentation/depliants/pro_fiche_cet-ifer_2026.pdf

### Other Exemptions

**Automatic exemptions most often met by self-employed clients**

| Exemption | Value | Note |
| --- | --- | --- |
| Source | all figures below | https://entreprendre.service-public.gouv.fr/vosdroits/F23547 |
| Artisans and façonniers, with or without a sign or shop, who use only the help of apprentices under contract; the spouse, PACS partner and children may help. Permanent | no figure | "lorsqu'ils utilisent uniquement le concours d'apprenti(s)sous contrat" |
| Taxi or ambulance drivers who own or rent 1 or 2 cars of up to 7 seats (driver not counted), drive or manage them themselves, do not run the 2 cars at the same time and keep to the regulated fares (CGI art. 1453). Permanent | no figure | "à condition que les 2 voitures ne soient pas en service en même temps" |
| Independent home sellers (VDI), for total gross pay below this amount. Permanent | EUR 7,930 | "pour leur rémunération brute totale inférieure à" |
| Painters, sculptors, engravers and draughtsmen regarded as artists who sell only the product of their art; graphic designers if limited to creating graphic works (CGI art. 1460). Permanent | no figure | "ne vendant que le produit de leur art" |
| Author-photographers, for taking pictures and selling their works or rights; authors, composers, choreographers and translators receiving droits d'auteur; lyric and dramatic artists. Permanent | no figure | "percevant des droits d'auteur" |
| Teachers of letters, sciences and arts who teach personally at home, at the pupils' homes, or in premises with no sign and no special fitting. Permanent | no figure | "dans un local dépourvu d'enseigne et ne comportant pas un aménagement spécial" |
| Midwives and garde-malades, unless they come under the nursing profession; sportsmen for the practice of a sport alone. Permanent | no figure | "sauf s'ils relèvent de la profession d'infirmière" |
| Letting part of one's own home occasionally at a reasonable price, or furnished where it is the sub-tenant's main home (CGI art. 1459). Permanent | no figure | "de façon occasionnelle à un prix raisonnable" |
| Classified furnished tourist lets and chambres d'hôtes within the owner's own home, unless the commune decides otherwise. Permanent | no figure | "(sauf délibération contraire de la commune)" |
| Lawyers who completed the CAPA training: limited to 2 years from the start of activity. Temporary | no figure | "l'exonération est limitée à 2 ans à compter du début d'activité" |
| Businesses created in a bassin urbain à dynamiser (BUD) between 1 January 2018 and 31 December 2026, or set up in a zone de développement prioritaire (ZDP) between 1 January 2019 and 31 December 2027, and exempt from income tax or corporation tax: limited to 7 years from creation. Temporary | no figure | "L'exonération est limitée à 7 ans à compter de la création" |

The page lists further automatic exemptions (cooperatives, ports, fishermen, farmers, Scop, private schools under contract, press activities, trade unions, HLM bodies, methanisation, social activities). Check the full list on the page before saying a client is liable.

**Optional exemptions (the commune or EPCI must have decided them)**

- Businesses in the ZAFR, ZAIPME, ZFRR (zones France ruralités revitalisation), ZUS, QPV, ZRD, BER, the ZFA in Guadeloupe, Guyane, Martinique, La Réunion and Mayotte, and businesses in Corsica.
- Doctors and health auxiliaries opening a secondary practice in a medical desert or a small commune, rural vets, JEI, JEC, JEU and JEII, independent record shops, labelled independent bookshops, live-performance businesses, caisses de crédit municipal.
- A 3-year exemption for the creation or extension of an establishment, from the year after the creation (or the 2nd year after the extension), on a commune decision, requested on 1447-M-SD for each establishment before 5 May of the year following the extension.

Source for both lists: https://entreprendre.service-public.gouv.fr/vosdroits/F23547 (the CFE page). The 2026 fiche gives one example of a commune-decided zone exemption for commercial businesses in the quartiers prioritaires with fewer than fifty employees (https://www.impots.gouv.fr/sites/default/files/media/3_Documentation/depliants/pro_fiche_cet-ifer_2026.pdf). Earlier versions of this skill listed a ZFU exemption and a 5-year ZRR exemption; neither appears on the pages read, which now name the ZFRR, and they have been removed.

### CA < EUR 5,000 Exemption

- **Small-turnover exemption**: see the small-turnover table in Step 4. It concerns businesses on the minimum base. The test is turnover excluding VAT of N-2 (or of N-1 for a business created in N-1), restated to 12 months where needed, and the business is exempt if it did not exceed the amount in the table. This is not the same rule as the furnished-letting entry test in Step 1, which uses the same amount with "more than".

## Step 6: Computation Steps [T1]

- **Computation steps overview**: sub-steps 6.1 to 6.5 below, applied in order.

### Step 6.1: Verify liability

- IF the year of assessment is the creation year: EXEMPT (1447-C-SD filed before 31 December).
- IF the business is on the minimum base AND its N-2 turnover (or N-1 turnover for a business created in N-1) did not exceed the small-turnover amount: EXEMPT.
- IF an automatic exemption in Step 5 applies, or the commune granted an optional exemption: EXEMPT for its scope and duration.
- IF the business let bare premises for business use below the bare-letting threshold, or furnished premises at or below the furnished-letting threshold: NOT WITHIN the CFE for that activity.

### Step 6.2: Determine base

- real_base = rental value of the property used in N-2, less any reduction in the reductions table.
- IF the year is the year after creation: apply the new-business reduction from the reductions table.
- minimum_base = the figure the commune chose inside the band for the N-2 turnover (minimum-base table).
- base = the higher of real_base and minimum_base; with no premises, base = minimum_base.

### Step 6.3: Apply municipal rate

- CFE = base × the commune's rate (or the EPCI's) for the year. The minimum is a minimum BASE, so the rate is applied to it as to any other base.

### Step 6.4: Add additional taxes

**What is added to the CFE**

| Addition | Value | Note |
| --- | --- | --- |
| Source | all figures below | https://entreprendre.service-public.gouv.fr/vosdroits/F23547 |
| Taxe additionnelle (for CCI France and the regional chambers of commerce), due by every business that owes the CFE unless exempt from this tax: a percentage of the CFE BASE | 1.12% | "fixée à" ... "du montant de la base d’imposition à la CFE" |
| Frais de gestion de la fiscalité locale: a percentage of the CFE plus the taxe additionnelle | 1% | "équivalent à" ... "du montant de la CFE et de la taxe additionnelle" |

- total = CFE + taxe additionnelle + frais de gestion.
- Exempt from the taxe additionnelle: artisans registered in the RNE as craft businesses and not on the chamber of commerce electoral list, agricultural cooperatives and Sica, fishermen and artisanal fishing companies, furnished-let operators, heads of institutions and boarding masters. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547
- A business that must register in the RNE as a craft business also pays the taxe pour frais de chambre de métiers et de l'artisanat (TCMA). The fiche gives no rate for it. Source: https://www.impots.gouv.fr/sites/default/files/media/3_Documentation/depliants/pro_fiche_cet-ifer_2026.pdf

### Step 6.5: Cap (plafonnement CET)

- **CET cap rule**: on the taxpayer's request, the relief equals CFE + CVAE minus the cap rate times the value added, where the value added is computed under the CVAE rules for the year of assessment (or the last 12-month accounting period closed in that year). The relief cannot bring the CET below the commune's minimum CFE. The chamber taxes, the ZRD tax credit and the relief for cessation are left out of the computation. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23548
- **How to claim**: form 1327-CET-SD (régime réel) or 1327S-CET-SD (micro-BIC or micro-BNC), to the SIE of the principal establishment, before 31 December of the year after the CFE was put into collection. The claim for 2025 is due by 31 December 2026. Half of the relief obtained or expected for N-1 may be deducted from the June acompte of year N, at the taxpayer's own risk. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23548

**CET cap rate, by year of the CET**

| Year of the CET | Value | Note |
| --- | --- | --- |
| Source | all figures below | https://bofip.impots.gouv.fr/bofip/2594-PGP.html |
| CET due for 2025 | 1.438% | "le taux de 1,438 % à la CET due au titre de l’année 2025" |
| CET due for 2026 and 2027 | 1.531% | "le taux de 1,531 % à la CET due au titre des années 2026 et 2027" |
| CET due for 2028 | 1.438% | "à la CET due au titre de l’année 2028" |

Earlier versions of this skill gave a single cap rate that belonged to 2023. The service-public cap page (F23548, Vérifié le 01 janvier 2026) applies the 2026 rate to value added produced in 2025; BOFiP (version in force from 29 April 2026) and the impots.gouv.fr 2026 fiche both give the lower rate in the table above for 2025. Use BOFiP and flag the difference when filing a 2025 claim.

**The CVAE, which makes up the CET with the CFE**

| CVAE rule | Value | Note |
| --- | --- | --- |
| Source | all figures below | https://bofip.impots.gouv.fr/bofip/839-PGP.html |
| Entry threshold: a business is liable to the CVAE when its turnover in the reference period is more than this amount (group consolidation does not apply to this test) | EUR 152,500 | "est supérieur à" ... "ni pour apprécier le seuil d’assujettissement à la CVAE" |
| Turnover excluding VAT below this amount: CVAE rate nil in every year from 2025 to 2029 | EUR 500,000 | "< 500 000 € 0 %" |
| Rate below the first band | 0% | "< 500 000 € 0 %" |
| Top band: turnover excluding VAT above this amount carries the maximum rate | EUR 50,000,000 | "> 50 000 000 €" |
| Maximum rate, top band, CVAE due for 2026 and 2027 | 0.28% | "Le taux maximal de la CVAE due au titre des années 2026 et 2027 est ainsi maintenu à son niveau de 2024" |
| Maximum rate, top band, CVAE due for 2025 | 0.19% | "Le taux maximal de la CVAE due au titre de 2025 est ainsi abaissé" |
| Temporary complementary contribution on the CVAE due for 2025 only (none for 2026): this share of the 2025 CVAE, added to it and settled on the same 1329-DEF | 47.4% | "due uniquement au titre de l’année 2025, dont le taux est fixé à 47,4 % et qui s’ajoute à la CVAE due au titre de l’année 2025" |
| Flat relief (dégrèvement) on the CVAE due for 2026 and 2027, where turnover is below the condition in the row after next | EUR 188 | "Pour la CVAE due au titre des années 2026 et 2027, ce dégrèvement est égal à" |
| Flat relief on the CVAE due for 2025, same condition | EUR 125 | "La CVAE due au titre de l’année 2025 obtenue par application du barème progressif est dégrevée d’un montant de" |
| Turnover condition for the flat relief: below this amount | EUR 2,000,000 | "lorsque le chiffre d’affaires de l’entreprise est inférieur à 2 millions d’euros" |
| Franchise: since 2024, no CVAE is due where the annual amount does not exceed this amount | EUR 63 | "la CVAE n’est pas due lorsque son montant annuel n’excède pas" |

Between the first band and the top band, the rate rises by the formulas in the BOFiP table for each year; use the formula for the year of the charge and round to the nearest hundredth, as BOFiP does. The same page also prints, in an older paragraph on group consolidation, a relief of "63 € pour 2026"; the rule paragraph (§ 170) and the 2025 finance law news item (https://bofip.impots.gouv.fr/bofip/14800-PGP.html/ACTU-2025-00145), which says the relief "est ajusté dans les mêmes proportions" as the rate, give the figure in the table. The amount in the franchise row is a different rule.

The 2025 contribution is settled on the same 1329-DEF as the 2025 CVAE, for 2025 by 5 May 2026 (the 2026 fiche: "liquidation définitive de la contribution complémentaire sur la même déclaration n° 1329-DEF que le millésime 2025 de CVAE, soit au plus tard le 5 mai 2026").

**CVAE filing and payment**

| Obligation | Value | Note |
| --- | --- | --- |
| Source | all figures below | https://www.impots.gouv.fr/sites/default/files/media/3_Documentation/depliants/pro_fiche_cet-ifer_2026.pdf |
| Form 1330-CVAE (value added and employees): filed electronically by businesses with turnover excluding VAT above this amount, by the 2nd working day after 1 May, even where no CVAE is payable | EUR 152,500 | "doit être déposée par les entreprises réalisant un chiffre d’affaires HT supérieur à" |
| Acomptes on 1329-AC by 15 June and 15 September: each this share of the CVAE due for N-1 | 50% | "Les acomptes payés en N représentent chacun" |
| No acomptes where the CVAE for the previous year does not exceed this amount | EUR 1,500 | "L'entreprise est dispensée du versement des acomptes dès lors que la CVAE due au titre de l'année précédant celle de l'imposition n'excède pas" |

The final CVAE return 1329-DEF is filed by the 2nd working day after 1 May of the following year, with any balance; for 2025 the fiche gives 5 May 2026. A small single-establishment business may use the CVAE box of its results return (2033-E, 2035-E, 2059-E or 2072-E) instead of 1330-CVAE if it meets every condition on the fiche, one of which is that it is not under the micro-enterprise regime.

## Step 7: Payment Schedule [T1]

**Payment Schedule (impots.gouv.fr 2026 fiche)**

| Obligation | Value | Note |
| --- | --- | --- |
| Source | all figures below | https://www.impots.gouv.fr/sites/default/files/media/3_Documentation/depliants/pro_fiche_cet-ifer_2026.pdf |
| Acompte: due by 15 June from a business not on monthly direct debit whose CFE for the previous year was at least this amount | EUR 3,000 | "dont le montant de cotisation de l’année précédente est supérieur ou égal à" |
| Amount of the acompte: this share of the previous year's CFE | 50% | "Cet acompte est égal à" ... "de la CFE de l’année précédente" |

- **Balance (solde)**: due by 15 December of the year of assessment. A date falling on a Saturday, Sunday or public holiday moves to the next working day. Source: the fiche above.
- **Monthly direct debit**: ten debits from January to October, with any adjustment in December; sign up by 30 June for the current year, and before 15 June to avoid the acompte. Source: the fiche above.
- **Debit at the due date**: sign up by 31 May for the acompte and by 30 November for the balance. Source: the fiche above.
- **Payment by bank transfer**: only for non-resident taxpayers (and some DGE businesses). Every other business pays by an electronic means. Source: the fiche above.
- **Notices**: CFE notices are no longer sent by post. They are only online, in the espace professionnel on impots.gouv.fr (MES SERVICES > Consulter > Avis C.F.E), which must be created first. Source: the fiche above.

**Payment Schedule (service-public wording)**

| Obligation | Value | Note |
| --- | --- | --- |
| Source | all figures below | https://entreprendre.service-public.gouv.fr/vosdroits/F23547 |
| The page separates businesses whose CFE paid the previous year was at or below, or above, this amount; above it, an acompte of half the previous year's CFE is due, "en général entre le 26 mai et le 16 juin (inclus)" | EUR 3,000 | "CFE supérieure à" |

The two official pages word the acompte boundary differently: the impots.gouv.fr fiche says "supérieur ou égal" and the service-public page says "supérieure". At exactly the threshold, rely on the avis d'acompte in the espace professionnel. Late payment carries a surcharge; no page read prints its rate for the CFE, so check the notice and do not quote a rate.

### First Year After Creation

- **No acompte in the first year a notice is due**: the creation year is exempt, so the previous year's CFE was nil and the acompte condition in the table above is not met. The first notice is the balance due by 15 December of the year after creation.

## Step 8: Tax Deductibility [T1]

**Tax Deductibility**

| Question | Answer |
| --- | --- |
| Is the CFE deductible from taxable profit under a régime réel? | The general rule in BOFiP is that net profit is computed after deducting the taxes borne by the business and put into collection during the accounting year, with listed exclusions (income tax itself and some specific taxes). The CFE is not among the listed exclusions, but the page does not name it. Source: https://bofip.impots.gouv.fr/bofip/2102-PGP.html (CGI art. 39, 1-4°) [T2] |
| For micro-entrepreneurs? | No separate deduction. The taxable base is turnover less a flat allowance meant to cover expenses: "ce ne sont donc pas les charges réelles qui sont déduites". Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23267 |
| When, under a régime réel? | In the accounting year in which the tax is put into collection, under the same BOFiP rule. |

## Step 9: Edge Case Registry

### EC1: Auto-entrepreneur, first year [T1]

**Situation:** Client registered as an auto-entrepreneur in May 2026.
**Resolution:** No CFE for 2026, the creation year. Request the exemption on 1447-C-SD before 31 December 2026. The CFE starts in 2027, on the reduced base for the year after creation (reductions table), and on the minimum base if the client has no premises. If the turnover of 2026, restated to 12 months, did not exceed the small-turnover amount, the client is exempt in 2027 as well.

### EC2: Home-based freelancer, no separate premises [T1]

**Situation:** Software developer working from home, no office rented, N-2 turnover (illustrative) of 25,000 in euro.
**Resolution:** The minimum base applies at the place of domiciliation. Turnover of 25,000 falls in the second band of the minimum-base table, so the commune's minimum base is somewhere in that band's range. CFE = the commune's minimum base × the commune's rate, plus the additions in Step 6.4 (paid through URSSAF for a micro-entrepreneur's chamber tax).

### EC3: Turnover at or below the small-turnover amount [T1]

**Situation:** Part-time freelancer on the minimum base with N-2 turnover (illustrative) of 3,500 in euro.
**Resolution:** Exempt, because the turnover did not exceed the amount in the small-turnover table. The test is "did not exceed", so turnover exactly equal to the amount is also exempt.

### EC4: Artisan exemption [T1]

**Situation:** Client is a self-employed carpenter working alone.
**Resolution:** The automatic exemption covers artisans who use only the help of apprentices under contract; the spouse, PACS partner and children may help. If the client hires one employee, the exemption is lost, and the client gets instead the base reduction for an artisan with 1 employee, provided pay for labour is more than the share of total turnover including VAT shown in the reductions table. Earlier versions of this skill added conditions (manual work, registration with the chambre de métiers) that the official page does not state; they have been removed.

### EC5: Multiple establishments [T2]

**Situation:** Client has a registered office in Paris and a workshop in Lyon.
**Resolution:** Where the CFE is set on a minimum base, it is due only at the principal establishment, which is not always the registered office. Each commune votes its own rate. [T2] How the rental value of each establishment is taxed across communes is not set out on the pages read: confirm with the SIE and check each commune's rate.

### EC6: Closing business mid-year [T1]

**Situation:** Client ceases activity on 30 June 2026.
**Resolution:** On a cessation during the year, the business does not owe the CFE for the months left to run. The CET cap page names this relief as "Dégrèvement pour cessation d'activité"; the pages read do not say how it is obtained, so ask the SIE. Report the cessation on 1447-M-SD. This is different from a change of operator: when a business is sold or transferred during the year, the former operator stays liable for the whole year and the new operator is not taxed that year; the new operator files 1447-C-SD before 1 January of the following year. A classified installation for the environment (ICPE) still owes the CFE during the rehabilitation of the site. Source: https://entreprendre.service-public.gouv.fr/vosdroits/F23547

### EC7: Zone location [T2]

**Situation:** Client is based in a QPV, a ZFRR or another zone.
**Resolution:** Most zone exemptions are optional: they exist only if the commune or EPCI decided them, they carry conditions, and they are requested on 1447-M-SD with form 1465-SD for the ZAFR, ZAIPME and ZFRR. The BUD and ZDP exemptions are automatic within their dates and conditions. [T2] Confirm the zone, the commune's decision and the conditions with the SIE.

### EC8: CFE + CVAE combined cap [T2]

**Situation:** Client's CFE plus CVAE exceed the cap rate times its value added.
**Resolution:** Claim the cap relief on 1327-CET-SD or 1327S-CET-SD (Step 6.5), using the rate for the year of the CET in the cap table. The relief cannot take the CET below the commune's minimum CFE. A business with turnover above the CVAE entry threshold files 1330-CVAE, but pays no CVAE while its turnover is below the first CVAE band in the CVAE table. [T2] The value added follows the CVAE rules: have it computed from the accounts.

## Step 10: Test Suite

All amounts in this section are in euro and are illustrative; commune rates are written as decimals.

### Test 1: Creation year, exempt

**Input:** Auto-entrepreneur registered in June 2026, turnover 20,000.
**Expected output:** CFE for 2026 = 0 (creation year). Must file 1447-C-SD before 31 December 2026.

### Test 2: Year after creation, reduced base

**Input:** Business created in 2025, premises with a rental value of 2,000, commune rate 0.25, N-2 turnover band 3, commune minimum base 900. Assessment year 2026.
**Expected output:** Reduced real base = 2,000 × 0.5 = 1,000 (new-business reduction in the reductions table). 1,000 is above the commune minimum base of 900, so base = 1,000. CFE = 1,000 × 0.25 = 250, before the additions in Step 6.4.

### Test 3: Home-based, minimum base

**Input:** Freelancer at home, no premises, N-2 turnover 25,000, commune minimum base 800 (inside the second band's range), commune rate 0.22.
**Expected output:** CFE = 800 × 0.22 = 176, before the additions in Step 6.4. The minimum is a base, so the rate always applies to it.

### Test 4: Turnover below the small-turnover amount

**Input:** Part-time consultant on the minimum base, N-2 turnover 4,500.
**Expected output:** Exempt. CFE = 0.

### Test 5: Artisan exemption

**Input:** Self-employed plumber, works alone with one apprentice under contract.
**Expected output:** Automatic exemption (Step 5). CFE = 0.

### Test 6: High CFE, advance payment

**Input:** Established business not on monthly direct debit, CFE for the previous year 4,500.
**Expected output:** Acompte due by 15 June = 4,500 × 0.5 = 2,250. Balance due by 15 December = the CFE for the year less 2,250.

### Test 7: CET cap limited by the minimum CFE (the BOFiP example, CET for 2026)

**Input:** Turnover 400,000, value added 15,000, a CFE of 600, a commune minimum CFE of 500, no CVAE.
**Expected output:** Cap = 15,000 × 0.01531 = 229.65. Relief before the limit = 600 minus 229.65 = 370.35. The CET may not fall below the minimum CFE, so the relief is limited to 600 minus 500 = 100. Source: https://bofip.impots.gouv.fr/bofip/2594-PGP.html

## When to refuse or refer

- The commune, its rate or its minimum base for the year is unknown: do not compute an amount; explain the method and the band only.
- Industrial establishments, port, airport and anti-pollution installations, seasonal reductions, and the IFER (network businesses): refer.
- Optional zone exemptions and the 3-year commune exemption: refer to the SIE for the commune's decision and the conditions.
- Several establishments in different communes: refer for the split of the real base.
- Computing value added for the CET cap or the CVAE rate between the first and the top band: refer to the accountant with the accounts.
- Groups (CVAE turnover consolidation), restructurings, transfers of a business during the year, and ICPE sites: refer.
- A dispute over a notice (réclamation) other than the cap claim: refer.
- Income tax on the profit: use `fr-income-tax`. Furnished and bare letting income tax: use `fr-rental-income`. Self-employed social contributions and the URSSAF account: use `fr-social-contributions`. Setting up the business: use `france-formation`. Booking the CFE in the accounts: use `france-bookkeeping`.

## PROHIBITIONS

- NEVER compute a CFE amount without the commune's rate and minimum base for the year.
- NEVER state a single minimum base for a band: the table is a range and the commune chooses.
- NEVER treat the minimum base as an amount of tax: the rate is applied to it.
- NEVER forget the creation-year exemption, which must be requested on 1447-C-SD before 31 December of the creation year.
- NEVER ignore the reduced base in the year after creation.
- NEVER state that micro-entrepreneurs are exempt from the CFE as such: they are within it, subject to the creation-year, small-turnover and activity exemptions.
- NEVER confuse the rental value of the premises with the rent actually paid.
- NEVER forget that CFE notices are online only, in the espace professionnel on impots.gouv.fr.
- NEVER charge a closing business for the months after a cessation, and NEVER apply that relief to a change of operator, where the former operator owes the whole year.
- NEVER say the CVAE keeps falling in 2026: the maximum rate for 2026 and 2027 is higher than for 2025 (CVAE table).
- NEVER confuse the CVAE flat relief with the CVAE franchise; they are different amounts and different rules.
- NEVER advise on a zone exemption without the commune's decision and the conditions.
- NEVER present the CFE as the whole local business tax: the CET is the CFE plus the CVAE.

## Sources

- Cotisation foncière des entreprises (CFE), Entreprendre Service Public, Vérifié le 02 avril 2026: https://entreprendre.service-public.gouv.fr/vosdroits/F23547
- Peut-on plafonner la contribution économique territoriale (CET) ?, Entreprendre Service Public, Vérifié le 01 janvier 2026: https://entreprendre.service-public.gouv.fr/vosdroits/F23548
- La contribution économique territoriale et l'IFER, impots.gouv.fr fiche, March 2026: https://www.impots.gouv.fr/sites/default/files/media/3_Documentation/depliants/pro_fiche_cet-ifer_2026.pdf
- BOI-IF-CFE-40-30-20-30, plafonnement de la CET, version in force from 29/04/2026: https://bofip.impots.gouv.fr/bofip/2594-PGP.html
- BOI-CVAE-LIQ-10, CVAE rate and relief, version in force from 19/11/2025: https://bofip.impots.gouv.fr/bofip/839-PGP.html
- BOFiP news item of 19/11/2025 on the 2025 finance law, art. 62: https://bofip.impots.gouv.fr/bofip/14800-PGP.html/ACTU-2025-00145
- BOI-BIC-CHG-40-30, taxes as business expenses: https://bofip.impots.gouv.fr/bofip/2102-PGP.html
- Régime fiscal de la micro-entreprise, Entreprendre Service Public, Vérifié le 13 mai 2026: https://entreprendre.service-public.gouv.fr/vosdroits/F23267

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as an expert-comptable, a CPA/EA, a tax attorney, or an equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date version of this skill is maintained at openaccountants.com. Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

<!-- openaccountants-cta-block -->

---

## Talk to a verified accountant

This guide is maintained by the OpenAccountants network — accountants who put
their name behind the tax answers AI gives people. The live, always-current
version (and the professional behind it) is at
[openaccountants.com](https://www.openaccountants.com).

- Use it in your AI: https://www.openaccountants.com/connect
- Meet the accountants: https://www.openaccountants.com/network

> **General reference only.** This document does not constitute tax, legal, or
> financial advice. Verify figures against the cited primary sources or with a
> licensed professional before relying on them.

## Today's figures and who stands behind this skill

This file is an AI skill (tax rules your AI follows) from OpenAccountants, copied on 2026-10-19. Rates, thresholds and deadlines change. For the current version of this skill, its official sources and the named accountant (if any) who stands behind it, call `get_skill` with slug `fr-cfe` on the OpenAccountants connector (https://www.openaccountants.com/connect), or read https://www.openaccountants.com/skills/fr-cfe. If neither is available, confirm every figure against the official source pages cited above before relying on it.
