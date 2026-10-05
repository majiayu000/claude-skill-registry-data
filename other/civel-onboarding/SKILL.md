---
name: civel-onboarding
description: "Wizard de configuracao do plugin civel ao perfil do escritorio. Cria a pasta civel/ com identidade (nome, OAB, escritorio, cidade), areas de atuacao civel, tribunais-alvo (para IRDR/jurisprudencia local), tom e modo de fluxo. Use quando o operador disser configurar civel, instalar civel, primeira vez, /start-civel, onboarding civel."
---

> **🖱️ Escolhas = botoes:** em campos de **lista fechada** (areas de atuacao, modo de fluxo, atualizar/recriar, sim/nao) use a ferramenta **AskUserQuestion** para mostrar **botoes clicaveis** (max. 4 por pergunta; se houver mais, divida em 2). **Texto livre** (nome, OAB, cidade, e-mail, tribunais) segue como pergunta digitada normal.

# CIVEL ONBOARDING

> Tier 0. Wizard de configuracao inicial. Linguagem acolhedora. Configura o plugin ao perfil do escritorio.

## Anexos obrigatorios (context/)
- `context/metodologia-civel.md` (para explicar o que o plugin faz).

## 0. Acionamento
`/start-civel` ou "configurar civel", "primeira vez", "onboarding civel". Cria/atualiza `civel/perfil.md` no diretorio de trabalho.

## 1. Regras do wizard
Uma pergunta por vez, acolhedor, sem jargao. Listas fechadas = AskUserQuestion (botoes). Texto livre = pergunta digitada. Ao fim, gravar e confirmar.

## 2. Blocos de pergunta
1. **Identidade (texto livre):** nome, OAB (nº/UF), escritorio, cidade, e-mail.
2. **Areas de atuacao civel (botoes, multi):** Responsabilidade civil/indenizatorias · Contratos/obrigacoes · Direitos reais/posse · Recursos · Tudo.
3. **Polo predominante (botoes):** Autor · Reu · Ambos.
4. **Tribunais-alvo (texto livre):** TJ(s)/TRF(s) onde atua — usado para pesquisar IRDR e jurisprudencia local (os IRDRs sao estaduais).
5. **Modo de fluxo (botoes):** Checkpoint (confirma a cada etapa) · Continuo.

## 3. Gravacao
Criar `civel/perfil.md`. Se ja existir, perguntar (botoes) Atualizar ou Recriar.

## Entrega obrigatoria final
- `civel/perfil.md` + resumo + sugestao do primeiro comando (`/triagem-civel` ou `/civel-master`).

## Guard
Nao inventar dados do operador. Tribunais-alvo sao do escritorio.
