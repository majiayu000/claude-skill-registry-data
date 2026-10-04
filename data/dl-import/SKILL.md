---
name: dl-import
description: Commandes import et cross-ref (DVF, AccesLibre, Qualiopi, CNIL, DPE, EPCI, KALI)
disable-model-invocation: true
---

# Import & Cross-ref Commands

```bash
# Data imports
pnpm import-dvf                 # DVF valeurs foncieres -> dl_dvf_transactions
pnpm import-acceslibre          # AccesLibre ERP -> dl_erp_accessibilite
pnpm import-emploi              # FLORES+URSSAF -> dl_emploi_territorial
pnpm import-culture             # Culture conventions -> dl_subventions_versees
pnpm import-transparence-sante  # Transparence sante -> dl_transparence_sante
pnpm import-qualiopi            # Qualiopi -> dl_organismes_formation
pnpm import-cnil-controles      # CNIL controles -> dl_cnil_controles
pnpm import-dpe-tertiaire       # DPE tertiaire -> dl_dpe_tertiaire
pnpm import-epci                # BANATIC EPCI -> dl_epci + cross-ref entities
pnpm import-kali                # KALI IDCC conventions -> dl_kali_conventions
pnpm import-territory-signals   # Culture + INJEP sport + URSSAF TI -> territory

# Cross-ref
pnpm crossref-new               # Cross-ref SIREN toutes nouvelles tables
pnpm crossref-deep              # Cross-ref profond (ERP, DVF, DPE, Qualiopi, CNIL)
pnpm crossref-batch             # Cross-ref dept-par-dept (DVF, DPE, CNIL -> entities)
pnpm crossref-acceslibre-name   # Cross-ref AccesLibre par nom normalise + code postal

# Quality
pnpm weekly-digest              # Submit weekly digest job (or --local for SQL-only)
pnpm territory-cards -- --department 31
pnpm territory-cards -- --all
pnpm golden-dataset -- --eval
pnpm golden-dataset -- --ci-gate
pnpm graph-explore -- --siren 123456789
pnpm graph-explore -- --community 31
```
