---
name: deploy-coston2
description: Deployer les contrats sur Flare Coston2
user-invocable: true
---

Deploie les smart contracts SENTINEL sur Flare Coston2 testnet :

1. forge build — compile tous les contrats
2. Deploie dans l'ordre : Registry -> Scoring -> Payment -> Proof
3. Verifie chaque contrat sur coston2-explorer.flare.network
4. Met a jour la config avec les nouvelles adresses
5. Lance les smoke tests post-deploiement

IMPORTANT: JAMAIS deployer sur mainnet. Coston2 testnet UNIQUEMENT.

$ARGUMENTS
