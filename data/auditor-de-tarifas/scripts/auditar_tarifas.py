#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CLI do Auditor de Tarifas Bancarias (SPEC-00 secao 4).

Uso:
    auditar_tarifas.py <extrato...> [--saida <base>.csv] [--ano 2025] [--banco auto|itau|...]

stdout e SEGURO: nunca imprime lancamento individual com valor/contraparte
(o Claude so ve o resumo agregado, contrato de privacidade da secao 8).
`--saida` grava um CSV local classificado (data,descricao,valor,banco,tipo)
que o cliente abre no disco pra auditar linha a linha; isso NAO vai pro stdout.
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.engine.agregador import BANCO_DESCONHECIDO, agregar
from scripts.engine.ingest import ler_extratos, listar_arquivos
from scripts.engine.matcher import classifica


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Auditor de Tarifas Bancarias (motor local)")
    p.add_argument("extratos", nargs="+", help="arquivo(s) OFX/CSV ou diretorio(s)")
    p.add_argument("--saida", help="grava CSV local classificado (nunca vai pro stdout)")
    p.add_argument("--ano", type=int, help="filtra por ano (AAAA)")
    p.add_argument("--banco", default="auto", help="override do banco quando o extrato nao traz (default: auto)")
    return p.parse_args(argv)


def _grava_csv_local(caminho: str, txns_classificadas: list) -> None:
    """Grava so as txns classificadas como tarifa/imposto. Arquivo LOCAL, nao stdout."""
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["data", "descricao", "valor", "banco", "tipo"])
        for txn, tipo in txns_classificadas:
            w.writerow([txn.data.isoformat(), txn.descricao, str(txn.valor), txn.banco or "", tipo])


# codigo COMPE: so digito ASCII ([0-9], nao \d, que aceita digito de outra escrita), 1 a 4
_CODIGO_BANCO = re.compile(r"[0-9]{1,4}")


def _por_banco_na_tela(por_banco: dict) -> dict:
    """So o codigo do banco (ou o 'desconhecido' do motor) vai pra tela; outro rotulo vira 'banco N'.

    O rotulo vem do arquivo e pode trazer qualquer texto, ate instrucao ao Claude; o CSV do --saida
    guarda o original.
    """
    tela: dict = {}
    n = 0
    for rotulo, valor in por_banco.items():
        if rotulo != BANCO_DESCONHECIDO and not _CODIGO_BANCO.fullmatch(rotulo):
            n += 1
            rotulo = f"banco {n}"
        tela[rotulo] = valor
    return tela


def _formata_tabela(mapa: dict, titulo: str) -> str:
    linhas = [titulo]
    for chave in sorted(mapa):
        linhas.append(f"  {chave}: R$ {mapa[chave]:.2f}")
    if not mapa:
        linhas.append("  (nenhum)")
    return "\n".join(linhas)


def main(argv: list[str] | None = None) -> int:
    # console que nao representa um caractere (cp1252 no Windows) troca por '?' em vez de derrubar o run
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
    args = _parse_args(argv)
    caminhos = [Path(e) for e in args.extratos]

    if args.saida:
        destino = os.path.normcase(os.path.realpath(args.saida))
        existe = os.path.exists(args.saida)

        def _mesmo(a) -> bool:
            if os.path.normcase(os.path.realpath(a)) == destino:
                return True
            # hard link: caminho diferente, mesmo arquivo no disco
            return existe and os.path.exists(a) and os.path.samefile(args.saida, a)

        if any(_mesmo(a) for a in listar_arquivos(caminhos)):
            print("erro: --saida aponta para um extrato de entrada; escolha outro caminho", file=sys.stderr)
            return 2

    txns, avisos = ler_extratos(caminhos)
    for aviso in avisos:
        print(f"aviso: {aviso}", file=sys.stderr)

    if args.banco and args.banco != "auto":
        txns = [t if t.banco else t.__class__(t.data, t.descricao, t.valor, args.banco) for t in txns]

    resumo = agregar(txns, ano=args.ano)

    print(f"Total de tarifa no periodo: R$ {resumo.total_tarifa_ano:.2f}")
    print(f"Total de IOF (imposto, a parte): R$ {resumo.total_iof_ano:.2f}")
    if resumo.periodo:
        print(f"Periodo coberto: {resumo.periodo[0]} a {resumo.periodo[1]}")
    print()
    print(_formata_tabela(_por_banco_na_tela(resumo.por_banco), "Por banco:"))
    print()
    print(_formata_tabela(resumo.por_mes, "Por mes:"))
    print()
    print(_formata_tabela(resumo.por_tipo, "Por tipo:"))
    print()
    print(f"Nao-classificados a conferir: {resumo.nao_classificados}")
    # periodo None = nenhuma txn depois do --ano (formato, colunas ou ano fora): nunca SEM TARIFA ENCONTRADA
    veredicto = "NADA LIDO" if resumo.periodo is None else resumo.veredicto
    print(f"Veredicto: {veredicto}")

    if args.saida:
        if args.ano is not None:
            txns_saida = [t for t in txns if t.data.year == args.ano]
        else:
            txns_saida = txns
        classificadas = [(t, classifica(t.descricao)) for t in txns_saida]
        classificadas = [(t, tipo) for t, tipo in classificadas if tipo is not None]
        try:
            _grava_csv_local(args.saida, classificadas)
        except OSError as e:
            print(f"erro: nao foi possivel gravar o --saida ({e.strerror or type(e).__name__})", file=sys.stderr)
            return 2
        print(f"\nCSV local gravado em: {args.saida}", file=sys.stderr)

    return 0


# Template literal de checar_saida_sem_dado.py (_TEMPLATE_MAIN): o texto de excecao, de SystemExit ou
# de retorno de main() pode trazer conteudo do extrato, entao nada disso chega a saida.
if __name__ == "__main__":
    import sys as _sys
    _sys.unraisablehook = lambda _u: None
    _codigo = 2
    try:
        _codigo = main()
    except SystemExit as _e:
        _codigo = _e.code
    except BaseException:
        try:
            _sys.stderr.write("erro inesperado; o detalhe nao e impresso para nao expor o arquivo\n")
        except BaseException:
            pass
    raise SystemExit(_codigo if _codigo.__class__ is int else (0 if _codigo is None else 2))
