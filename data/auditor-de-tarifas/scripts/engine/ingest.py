# -*- coding: utf-8 -*-
"""Ingest: le OFX/CSV e devolve lista canonica de txns.

SPEC-00 secao 3: `extrato (OFX | CSV | ...) -> lista canonica de txns
{data, descricao, valor, banco?}`. PDF fica pro F2 (reusa o conversor-extrato,
nao reimplementado aqui). Robustez: arquivo invalido/vazio nao derruba o
processo, so devolve lista vazia + um aviso (texto, sem PII).
"""
from __future__ import annotations

import csv
import io
import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

from .normalize import parse_data, parse_valor


@dataclass(frozen=True)
class Txn:
    data: date
    descricao: str
    valor: Decimal          # sinal original do extrato (debito = negativo)
    banco: str | None = None


_STMTTRN = re.compile(r"<STMTTRN>(.*?)</STMTTRN>", re.DOTALL | re.IGNORECASE)
_BANKID = re.compile(r"<BANKID>\s*([^<\r\n]+)", re.IGNORECASE)


def _campo_ofx(bloco: str, tag: str) -> str | None:
    m = re.search(rf"<{tag}>\s*([^<\r\n]+)", bloco, re.IGNORECASE)
    return m.group(1).strip() if m else None


def ler_ofx(texto: str) -> tuple[list[Txn], list[str]]:
    """Parser proprio e leve de OFX (SGML, tolerante a tags sem fechamento)."""
    avisos: list[str] = []
    banco = None
    m_bank = _BANKID.search(texto)
    if m_bank:
        banco = m_bank.group(1).strip()

    if not _STMTTRN.search(texto):
        # espelha o ler_csv: export vazio/sem lancamentos nao pode ser confundido
        # com conta limpa (o CLI concluiria SEM TARIFA ENCONTRADA silenciosamente).
        return [], ["arquivo OFX vazio ou sem lancamentos"]

    txns: list[Txn] = []
    for bloco_match in _STMTTRN.finditer(texto):
        bloco = bloco_match.group(1)
        dtposted = _campo_ofx(bloco, "DTPOSTED")
        trnamt = _campo_ofx(bloco, "TRNAMT")
        descricao = _campo_ofx(bloco, "MEMO") or _campo_ofx(bloco, "NAME")
        if dtposted is None or trnamt is None or descricao is None:
            avisos.append("lancamento OFX incompleto ignorado (faltou data/valor/descricao)")
            continue
        try:
            txns.append(Txn(
                data=parse_data(dtposted),
                descricao=descricao,
                valor=parse_valor(trnamt, origem="ofx"),
                banco=banco,
            ))
        except ValueError as e:
            avisos.append(f"lancamento OFX invalido ignorado: {e}")
    return txns, avisos


_ALIASES_COLUNA = {
    "data": {"data", "date", "dtposted"},
    "descricao": {"descricao", "historico", "memo", "desc", "lancamento"},
    "valor": {"valor", "amount", "vlr"},
    "banco": {"banco", "bank", "instituicao"},
}


def _sem_acento_lower(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).strip().lower()


def _mapeia_colunas(cabecalho: list[str]) -> dict[str, int]:
    mapa: dict[str, int] = {}
    normalizado = [_sem_acento_lower(c) for c in cabecalho]
    for campo, aliases in _ALIASES_COLUNA.items():
        for i, col in enumerate(normalizado):
            if col in aliases:
                mapa[campo] = i
                break
    return mapa


def ler_csv(texto: str) -> tuple[list[Txn], list[str]]:
    """Parser de CSV tolerante: detecta delimitador e colunas por cabecalho."""
    avisos: list[str] = []
    texto = texto.strip("﻿\n\r ")
    if not texto:
        return [], ["arquivo CSV vazio"]

    primeira_linha = texto.splitlines()[0]
    try:
        dialeto = csv.Sniffer().sniff(primeira_linha, delimiters=";,\t|")
        delimitador = dialeto.delimiter
    except csv.Error:
        delimitador = ";" if primeira_linha.count(";") >= primeira_linha.count(",") else ","

    leitor = csv.reader(io.StringIO(texto), delimiter=delimitador)
    linhas = list(leitor)
    if not linhas:
        return [], ["arquivo CSV vazio"]

    mapa = _mapeia_colunas(linhas[0])
    if "data" not in mapa or "descricao" not in mapa or "valor" not in mapa:
        return [], ["CSV sem colunas reconheciveis (esperado data/descricao/valor)"]

    txns: list[Txn] = []
    for linha in linhas[1:]:
        if not linha or all(not c.strip() for c in linha):
            continue
        try:
            idx_data, idx_desc, idx_valor = mapa["data"], mapa["descricao"], mapa["valor"]
            banco = linha[mapa["banco"]].strip() if "banco" in mapa and mapa["banco"] < len(linha) else None
            txns.append(Txn(
                data=parse_data(linha[idx_data]),
                descricao=linha[idx_desc],
                valor=parse_valor(linha[idx_valor], origem="br"),
                banco=banco or None,
            ))
        except (ValueError, IndexError) as e:
            avisos.append(f"linha CSV invalida ignorada: {e}")
    return txns, avisos


# Extrato de banco BR vem em UTF-8 (padrao moderno) ou CP1252/Latin-1 (legado).
# Tenta em ordem, aceitando a primeira que decodifica sem erro; so cai no
# errors='replace' como ultimo recurso (nunca corrompe acento antes do matcher).
_ENCODINGS_BR = ("utf-8-sig", "cp1252", "latin-1")


def _decodifica(bruto: bytes) -> str:
    for enc in _ENCODINGS_BR:
        try:
            return bruto.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return bruto.decode("utf-8", errors="replace")


def ler_arquivo(caminho: Path) -> tuple[list[Txn], list[str]]:
    """Le um unico arquivo (OFX ou CSV, por extensao). Nunca lanca excecao."""
    caminho = Path(caminho)
    try:
        texto = _decodifica(caminho.read_bytes())
    except OSError as e:
        return [], [f"nao foi possivel ler {caminho.name}: {e}"]

    sufixo = caminho.suffix.lower()
    if sufixo == ".ofx":
        return ler_ofx(texto)
    if sufixo == ".csv":
        return ler_csv(texto)
    return [], [f"formato nao suportado nesta fase (F1 = OFX/CSV): {caminho.name}"]


# cabecalho exato do CSV de saida do proprio auditor (--saida). Detectar por
# cabecalho e robusto a nome de arquivo.
_HEADER_SAIDA = {"data", "descricao", "valor", "banco", "tipo"}


def _eh_saida_classificada(caminho: Path) -> bool:
    """True se o .csv e o output classificado do proprio auditor.

    Evita que um scan de diretorio re-injira o CSV do --saida como se fosse mais
    um extrato (duplicaria as tarifas, inflando o total). Detecta pelo cabecalho.
    """
    try:
        bruto = caminho.read_bytes()
    except OSError:
        return False
    texto = _decodifica(bruto).strip("﻿\n\r ")
    if not texto:
        return False
    primeira = texto.splitlines()[0]
    cols = {_sem_acento_lower(c) for c in re.split(r"[;,\t|]", primeira)}
    return cols == _HEADER_SAIDA


def listar_arquivos(caminhos: list[Path]) -> list[Path]:
    """Expande arquivos e/ou diretorios na lista de extratos que serao lidos."""
    arquivos: list[Path] = []
    for c in caminhos:
        p = Path(c)
        if p.is_dir():
            for f in sorted(p.iterdir()):
                if f.suffix.lower() not in (".ofx", ".csv"):
                    continue
                if f.suffix.lower() == ".csv" and _eh_saida_classificada(f):
                    continue  # pula o proprio output classificado (anti-duplicacao)
                arquivos.append(f)
        else:
            arquivos.append(p)
    return arquivos


def ler_extratos(caminhos: list[Path]) -> tuple[list[Txn], list[str]]:
    """Le uma lista de arquivos e/ou diretorios, agregando todas as txns."""
    arquivos = listar_arquivos(caminhos)
    todas_txns: list[Txn] = []
    todos_avisos: list[str] = []
    if not arquivos:
        return [], ["nenhum extrato encontrado"]
    for arquivo in arquivos:
        txns, avisos = ler_arquivo(arquivo)
        todas_txns.extend(txns)
        todos_avisos.extend(avisos)
    return todas_txns, todos_avisos
