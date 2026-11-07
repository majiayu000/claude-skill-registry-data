# -*- coding: utf-8 -*-
"""Agregador: soma por banco x mes x tipo, IOF a parte, veredicto.

SPEC-00 secao 7 (schema do resumo agregado, o que o Claude ve). So tarifa
(nao IOF) entra em por_banco/por_mes/por_tipo/total_tarifa_ano. Valores
sempre Decimal, 2 casas, nunca float.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

from .ingest import Txn
from .matcher import classifica

ZERO = Decimal("0.00")

BANCO_DESCONHECIDO = "desconhecido"


@dataclass
class Resumo:
    total_tarifa_ano: Decimal
    total_iof_ano: Decimal
    periodo: tuple[str, str] | None       # (mes inicial, mes final) em "AAAA-MM"
    por_banco: dict[str, Decimal] = field(default_factory=dict)
    por_mes: dict[str, Decimal] = field(default_factory=dict)
    por_tipo: dict[str, Decimal] = field(default_factory=dict)
    nao_classificados: int = 0
    veredicto: str = "SEM TARIFA ENCONTRADA"


def _acumula(mapa: dict[str, Decimal], chave: str, valor: Decimal) -> None:
    mapa[chave] = mapa.get(chave, ZERO) + valor


def agregar(txns: list[Txn], ano: int | None = None) -> Resumo:
    """Classifica e soma as txns. Filtra por `ano` antes de tudo, se informado."""
    if ano is not None:
        txns = [t for t in txns if t.data.year == ano]

    total_tarifa = ZERO
    total_iof = ZERO
    por_banco: dict[str, Decimal] = {}
    por_mes: dict[str, Decimal] = {}
    por_tipo: dict[str, Decimal] = {}
    nao_classificados = 0
    tarifas_detectadas = 0
    meses_vistos: set[str] = set()

    for txn in txns:
        # registra o mes de TODA txn lida (mesmo operacao ignorada) antes do
        # classifica/continue, pra "Periodo coberto" refletir o extrato inteiro,
        # nao so os meses que tiveram tarifa.
        mes = f"{txn.data.year:04d}-{txn.data.month:02d}"
        meses_vistos.add(mes)

        tipo = classifica(txn.descricao)
        if tipo is None:
            continue

        # custo liquido: Txn.valor e debito-negativo por contrato, entao o custo
        # e -valor. Um ESTORNO de tarifa e um credito (valor>0) e por isso SUBTRAI
        # do custo, netando a cobranca (nao infla o total como abs() faria).
        custo = -txn.valor

        if tipo == "imposto":
            total_iof += custo
            continue

        total_tarifa += custo
        tarifas_detectadas += 1
        banco = txn.banco or BANCO_DESCONHECIDO
        _acumula(por_banco, banco, custo)
        _acumula(por_mes, mes, custo)
        _acumula(por_tipo, tipo, custo)
        if tipo == "outra_tarifa":
            nao_classificados += 1

    periodo = (min(meses_vistos), max(meses_vistos)) if meses_vistos else None

    if nao_classificados > 0:
        veredicto = "CONFERIR"
    elif tarifas_detectadas == 0:
        veredicto = "SEM TARIFA ENCONTRADA"
    else:
        veredicto = "OK"

    return Resumo(
        total_tarifa_ano=total_tarifa,
        total_iof_ano=total_iof,
        periodo=periodo,
        por_banco=por_banco,
        por_mes=por_mes,
        por_tipo=por_tipo,
        nao_classificados=nao_classificados,
        veredicto=veredicto,
    )
