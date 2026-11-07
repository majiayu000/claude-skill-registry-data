# -*- coding: utf-8 -*-
"""Matcher: classifica uma descricao de lancamento em tarifa/imposto/ignora.

SPEC-00 secao 6 (3 baldes, honestidade do numero):
  1. tarifa (negociavel)   -> um dos tipos de CATEGORIAS
  2. imposto (IOF)         -> 'imposto', somado a parte
  3. ignora                -> None (operacao real, receita, despesa, juros)

Conservador por desenho: na duvida vira 'outra_tarifa' (a conferir), nunca
soma cega. Opera so sobre o campo `descricao` (texto do historico), que e
igual em qualquer formato de origem (OFX ou CSV).
"""
from __future__ import annotations

from .dicionario import CATEGORIAS, IMPOSTO, MARCADOR_TARIFA, ORDEM_CATEGORIAS
from .normalize import sem_acento

TipoTarifa = str  # 'manutencao' | 'transferencia' | 'pix' | 'boleto' | 'custodia'
# | 'cartao' | 'saque_extrato' | 'outra_tarifa' | 'imposto' | None


def _normaliza(descricao: str) -> str:
    """Maiusculas + sem acento, pra casar regex de forma tolerante."""
    return sem_acento(str(descricao or "")).upper()


def classifica(descricao: str) -> TipoTarifa | None:
    """Classifica uma descricao de lancamento. Retorna o tipo ou None (ignora)."""
    desc = _normaliza(descricao)

    if IMPOSTO.search(desc):
        return "imposto"

    tem_marcador = bool(MARCADOR_TARIFA.search(desc))

    for categoria in ORDEM_CATEGORIAS:
        for padrao, exige_marcador in CATEGORIAS[categoria]:
            if not padrao.search(desc):
                continue
            if exige_marcador and not tem_marcador:
                continue  # e o termo da OPERACAO (ex.: TED grande), nao tarifa
            return categoria

    if tem_marcador:
        # marcador de tarifa presente mas nenhuma categoria especifica casou:
        # fallback generico (secao 5), sempre "a conferir".
        return "outra_tarifa"

    return None
