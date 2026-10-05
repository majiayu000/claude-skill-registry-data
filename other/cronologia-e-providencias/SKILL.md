---
name: cronologia-e-providencias
description: "Converte intimacoes, decisoes, despachos e atas de audiencia numa linha do tempo do processo e numa agenda de providencias com prazos. Le o ato, extrai deliberacoes, identifica o que precisa ser feito e ate quando, e atualiza a memoria do caso. Use quando o operador colar uma intimacao/decisao/ata, disser monta a cronologia, quais as providencias, o que tenho que fazer, agenda do processo, ou organizar o caso."
---

# CRONOLOGIA-E-PROVIDENCIAS

> Camada 2 (gestao processual). Transforma atos processuais em agenda acionavel. Alimenta o `memoria-de-caso-civel`.

## Anexos obrigatorios (context/)
- `context/metodologia-civel.md` (fluxo processual).

## Objetivo
Que nada do processo passe despercebido: cada ato vira providencia com prazo, na ordem cronologica.

## Quando ativar
- O operador cola intimacao, decisao, despacho ou ata de audiencia.
- Pede a cronologia, a agenda ou as providencias do caso.

## Metodologia
1. **Ler o ato** (intimacao/decisao/ata) e identificar a natureza (determina conduta? abre prazo? designa audiencia? defere/indefere?).
2. **Extrair deliberacoes** e o que cada uma exige da parte.
3. **Calcular prazo** de cada providencia chamando `tempestividade-civel` (dias uteis; marco inicial).
4. **Montar a linha do tempo** (atos ja praticados) + **a agenda** (providencias futuras com data fatal).
5. **Atualizar** o `memoria-de-caso-civel` (historico + prazos + proximo passo).

## Entrega obrigatoria final
- Linha do tempo do processo + tabela de providencias (o que / ate quando / responsavel) + atualizacao da memoria do caso.

## Guard
Prazos sempre via `tempestividade-civel` (dias uteis, regra nova de feriado local). Nao inventar datas sem o marco da intimacao/publicacao.
