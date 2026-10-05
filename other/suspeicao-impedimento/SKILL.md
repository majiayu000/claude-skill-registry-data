---
name: suspeicao-impedimento
description: "Argui impedimento (CPC 144, hipoteses objetivas I a IX) ou suspeicao (CPC 145, amizade intima/inimizade, presente/aconselhamento, credor/devedor, interesse no julgamento — I a IV) do juiz, em peticao especifica no prazo de 15 dias do conhecimento do fato (CPC 146), que o juiz reconhece ou remete ao tribunal — efeito suspensivo declarado pelo relator (146 §2), extensiva a MP, auxiliares da justica e demais sujeitos imparciais (CPC 148). Use quando o operador disser suspeicao, impedimento do juiz, juiz parcial, recusar o juiz, excecao de suspeicao, juiz amigo da parte contraria."
---

# SUSPEICAO-IMPEDIMENTO

> Camada 8 (incidentes processuais). Recusa do juiz por quebra de imparcialidade. Distingue impedimento (objetivo) de suspeicao (subjetivo). Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 144 (impedimento, I a IX + §1 a §3), 145 (suspeicao, I a IV + §1 foro intimo / §2 ilegitimidade), 146 (procedimento: 15 dias, peticao especifica, §2 efeitos), 148 (extensao a MP, auxiliares e demais imparciais) — **grep + ler a faixa**.
- `context/jurisprudencia-civel.md` (so ✅/🟡 vistoriados).

## Objetivo
Afastar o juiz parcial com a tese certa: impedimento (nulidade absoluta, arguivel a qualquer tempo, fundamento de rescisoria) ou suspeicao (preclui em 15 dias), em peticao especifica e instruida, com efeito suspensivo quando o risco justificar.

## Quando ativar
- Ha causa objetiva do art. 144 (atuacao previa, parentesco, interesse societario).
- Ha quebra subjetiva do art. 145 (amizade intima/inimizade, presente, aconselhamento, credor/devedor, interesse no julgamento).

## Metodologia
1. **Gestao processual SEMPRE (Camada 2):** `tempestividade-civel` (o prazo de 15 dias e fatal na suspeicao — CPC 146); `memoria-de-caso-civel` (registrar a data do conhecimento do fato).
2. **Enquadrar a hipotese:** impedimento (CPC 144, I a IX — objetivo: juiz que ja decidiu em outro grau, II; parente postulando, III; parte/cliente do escritorio do conjuge, IV/VIII; promover acao contra a parte, IX). Suspeicao (CPC 145, I a IV — amigo intimo/inimigo, I; presente/aconselhamento/custeio, II; credor/devedor, III; interesse no julgamento, IV). O §2 do 144 veda forjar fato superveniente; o §2 do 145 torna ilegitima a suspeicao provocada por quem a alega ou apos manifesta aceitacao.
3. **Distinguir o regime:** impedimento = objetivo, nulidade absoluta, nao precluivel, abre rescisoria. Suspeicao = subjetivo, preclui se nao arguida no prazo.
4. **Prazo e forma (CPC 146):** 15 dias do conhecimento do fato; peticao ESPECIFICA dirigida ao juiz do processo, com o fundamento da recusa, documentos e rol. O juiz pode reconhecer e remeter ao substituto (146 §1); se nao, autua em apartado, apresenta razoes em 15 dias e remete o incidente ao tribunal.
5. **Efeito suspensivo (CPC 146 §2):** pedir ao relator; sem efeito o processo corre, com efeito fica suspenso ate o julgamento. Ate a declaracao do efeito (ou se suspensivo), a tutela de urgencia vai ao substituto (146 §3).
6. **Extensao subjetiva (CPC 148):** as mesmas causas alcancam membro do MP, auxiliares da justica e demais sujeitos imparciais — arguir na primeira oportunidade de falar nos autos (148 §1).

## Entrega obrigatoria final
- Peticao de arguicao redigida ponta a ponta (fato gerador da recusa + enquadramento impedimento x suspeicao + provas e rol + pedido de remessa ao substituto/tribunal + efeito suspensivo) + data do conhecimento do fato e termo final do prazo.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: nulidade de atos do juiz impedido como fundamento autonomo -> `acao-rescisoria`; competencia entre juizos -> `conflito-de-competencia`.
