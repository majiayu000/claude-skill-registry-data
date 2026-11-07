# -*- coding: utf-8 -*-
"""Dicionario de tarifas bancarias BR (o coracao do produto, SPEC-00 secao 5).

Autoria do Doug a partir de nomes publicos de servico bancario (padronizacao
Bacen) + descritores comuns de extrato. Nenhum dado real de extrato aqui.

Cada categoria e uma lista de (regex, exige_marcador_tarifa). Quando
`exige_marcador_tarifa` e True, o termo sozinho tambem aparece como a propria
OPERACAO (ex.: uma TED de R$50.000 enviada) e so conta como tarifa quando o
historico tambem casa um marcador de tarifa (`TAR`/`TARIFA`) em algum lugar da
descricao (secao 6: honestidade do numero, nunca soma cega).
"""
from __future__ import annotations

import re

# marcador generico de tarifa: usado tanto pro fallback `outra_tarifa` quanto
# pra desambiguar os termos de operacao (TED/DOC) da secao 6.
MARCADOR_TARIFA = re.compile(r"\bTAR\b|\bTARIFA\b")

IMPOSTO = re.compile(r"\bIOF\b")

# ordem da tabela da SPEC-00 secao 5 (preserva ordem de checagem no matcher).
CATEGORIAS: dict[str, list[tuple[re.Pattern, bool]]] = {
    "manutencao": [
        (re.compile(r"\bTAR(?:IFA)? MANUTENCAO"), False),
        (re.compile(r"MANUTENCAO CC"), False),
        (re.compile(r"\bCESTA\b"), False),
        (re.compile(r"PACOTE (DE )?SERVICOS"), False),
        (re.compile(r"MENSALIDADE"), True),
        (re.compile(r"TARIFA MENSAL"), False),
        # nomes reais de pacote/conta de servico BR (nomes de servico, casam sem marcador)
        (re.compile(r"CONTA CERTA"), False),
        (re.compile(r"CONTA MAX"), False),
        (re.compile(r"TARIFA BANCARIA MAX"), False),
        (re.compile(r"\bTAR(?:IFA)? CTA GARANTIDA"), False),
    ],
    "transferencia": [
        # bare: e tambem o nome da OPERACAO (TED/DOC enviado). So conta com marcador junto.
        (re.compile(r"\bTED\b"), True),
        (re.compile(r"\bDOC\b"), True),
        (re.compile(r"\bTAR(?:IFA)? (DE )?TRANSFERENCIA"), False),
    ],
    "pix": [
        # todos os padroes aqui ja carregam o marcador de tarifa embutido (PF e gratis por regra).
        (re.compile(r"\bTAR(?:IFA)? PIX"), False),
        (re.compile(r"PIX (PAG|ENVIO|RECEB)\w*.*TARIF"), False),
        (re.compile(r"\bTARIFA AVULSA ENVIO PIX"), False),
        # "PAGTO PIX" sozinho e a OPERACAO; so conta com marcador de tarifa junto.
        (re.compile(r"PAGTO\.? PIX"), True),
    ],
    "boleto": [
        (re.compile(r"\bTAR(?:IFA)? (DE )?BOLETO"), False),
        # LIQUIDACAO/EMISSAO de boleto sao a OPERACAO; so contam com marcador de tarifa junto.
        (re.compile(r"LIQUIDACAO (DE )?BOLETO"), True),
        (re.compile(r"EMISSAO (DE )?(BLOQUETO|BOLETO)"), True),
        (re.compile(r"TARIFA (DE )?COBRANCA"), False),
        # descritores reais de cobranca BR (custas/cobranca expressa)
        (re.compile(r"CUSTAS? COBRANCA"), False),
        (re.compile(r"COBRANCA EXP"), False),
    ],
    "cambio": [
        # tarifa de operacao de cambio/internacional (negociavel=sim).
        # "TAR OPE"/"TAR CAMB" ja carregam o marcador; "CARTA CIRCULARIZADORA" e nome de servico.
        (re.compile(r"\bTAR(?:IFA)? OPE\b"), False),
        (re.compile(r"\bTAR(?:IFA)? CAMB"), False),
        (re.compile(r"TARIFA ENVIO OPE"), False),
        (re.compile(r"TARIFA AVULSA ENVIO"), False),
        (re.compile(r"CARTA CIRCULARIZADORA"), False),
    ],
    "custodia": [
        (re.compile(r"\bCUSTODIA\b"), False),
        (re.compile(r"\bTAR(?:IFA)? CUSTODIA"), False),
        (re.compile(r"MANUTENCAO (DE )?TITULO"), False),
    ],
    "cartao": [
        (re.compile(r"\bANUIDADE\b"), False),
        (re.compile(r"\bTAR(?:IFA)? CARTAO"), False),
    ],
    "saque_extrato": [
        (re.compile(r"\bTAR(?:IFA)? SAQUE"), False),
        (re.compile(r"SEGUNDA VIA"), False),
        (re.compile(r"\bTAR(?:IFA)? EXTRATO"), False),
        (re.compile(r"\bTAR(?:IFA)? SALDO"), False),
    ],
}

# ordem estavel das categorias tarifa (exclui "imposto", que fica a parte, e
# "outra_tarifa", que e o fallback generico calculado no matcher).
ORDEM_CATEGORIAS = tuple(CATEGORIAS.keys())
