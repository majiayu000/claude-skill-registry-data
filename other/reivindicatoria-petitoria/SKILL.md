---
name: reivindicatoria-petitoria
description: "Redige acao reivindicatoria — o proprietario nao-possuidor reivindica a coisa de quem injustamente a possui ou detem (CC 1.228), com presuncao de propriedade plena e exclusiva (CC 1.231) e possibilidade de reivindicar de terceiro apos cancelamento do registro inexato (CC 1.247 par. unico), distinguindo a PETITORIA (fundada no dominio/titulo registrado) da POSSESSORIA (fundada na posse), respeitada a vedacao de alegar dominio na pendencia da possessoria (CPC 557). Use quando o operador disser acao reivindicatoria, reaver imovel, sou dono mas estao na posse, petitoria, ou reivindicar propriedade."
---

# REIVINDICATORIA-PETITORIA

> Camada 5 (acoes civeis). Acao petitoria do proprietario sem posse contra o possuidor/detentor injusto — fundada no DOMINIO, nao na posse. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cc-10406-02.md` — arts. 1.228 (faculdade de usar/gozar/dispor + direito de reave-la de quem injustamente possua ou detenha), 1.231 (propriedade presume-se plena e exclusiva ate prova em contrario), 1.247 + par. unico (registro que nao exprime a verdade; reivindicar de terceiro apos cancelamento) — **grep + ler a faixa**.
- `context/cpc-13105-15.md` — art. 557 (vedacao de propor acao de reconhecimento do dominio na pendencia da possessoria, salvo contra terceiro); requisitos da inicial (319) + `context/jurisprudencia-civel.md` (so ✅).

## Objetivo
Inicial reivindicatoria que prova o dominio (titulo registrado), individualiza a coisa e demonstra a posse injusta do reu, sem confundir o juizo petitorio com o possessorio.

## Quando ativar
- Proprietario com titulo registrado, mas sem posse, quer reaver a coisa de quem a possui/detem injustamente.
- Registro inexato cancelado -> reivindicar de terceiro (CC 1.247 par. unico).

## Metodologia
1. **Gestao processual SEMPRE (Camada 2) antes de redigir:** `competencia-e-foro` (situacao do imovel) · `valor-da-causa` · `gratuidade-e-impugnacao` · `tempestividade-civel`.
2. **Provar o dominio:** titulo de propriedade registrado; invocar a presuncao de propriedade plena e exclusiva (CC 1.231). A reivindicatoria exige PROVA DO DOMINIO, nao mera posse.
3. **Individualizar a coisa:** descricao precisa do imovel (matricula, confrontacoes, area) — sem individualizacao, risco de improcedencia.
4. **Demonstrar a posse injusta do reu:** quem possui/detem sem causa juridica que se oponha ao proprietario (CC 1.228 — reaver de quem injustamente possua ou detenha).
5. **Distinguir petitoria x possessoria:** a petitoria funda-se no titulo/dominio; a possessoria, na posse. Respeitar a vedacao do CPC 557 (nao discutir dominio na pendencia da possessoria, salvo contra terceiro).
6. **Pedido:** restituicao da coisa ao proprietario; perdas e danos e frutos conforme a boa/ma-fe do possuidor (via `validador-civel`).

## Entrega obrigatoria final
- Inicial redigida ponta a ponta (dominio/titulo registrado + individualizacao da coisa + posse injusta do reu + distincao petitoria/possessoria + pedido de restituicao + valor + provas) + checklist de documentos + indicacao do foro/vara.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: defesa/recuperacao pela POSSE -> `possessorias`; aquisicao originaria pela posse -> `usucapiao-judicial`; execucao/cumprimento pesado -> `execucao-adv-os`.
