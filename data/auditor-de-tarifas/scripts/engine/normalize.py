# -*- coding: utf-8 -*-
"""Normalizadores compartilhados: valor monetario e data.

Lida com os dois mundos que os motores da Trilha Tesouraria cruzam:
  - BR humano (extrato/razao/contas a pagar-receber CSV/XLS): "1.234,56" / "31/01/2026"
  - OFX (padrao aberto): "1234.56" / "20260131" ou "20260131120000[-3:GMT]"

Decisao de aritmetica: dinheiro nunca em float. parse_valor -> Decimal quantizado
a 0.01; o core de cada motor compara/soma em Decimal.

Canonico em `_shared/engine/normalize.py`; copias byte-iguais guardadas por
`test_vendoring.py`.
"""
from __future__ import annotations

import re
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

CENTAVO = Decimal("0.01")


_MILHAR_BR = re.compile(r"\d{1,3}(\.\d{3})+")  # 1.234 / 12.500 / 1.234.567 (grupo de milhar BR)


def parse_valor(raw, origem: str = "auto") -> Decimal:
    """Converte texto monetario (BR ou OFX) para Decimal com 2 casas.

    `origem`:
      - "ofx": ponto e SEMPRE decimal (extrato OFX traz 2 casas; nunca milhar com ponto).
      - "br"/"auto": ponto pode ser milhar BR. Um valor que casa o padrao de milhar
        (`1.234`, `12.500`, `1.234.567`) e tratado como milhar; corrige o erro 1000x
        de `"1.234"` virar 1,23 na razao digitada por humano (achado da revisao).
    Sinal: aceita '-' a esquerda, '-' a direita (convencao Itau, ex.: "89,90-") ou
    parenteses contabeis "(1.234,56)".
    """
    if raw is None:
        raise ValueError("valor vazio")
    s = str(raw).strip()
    if s == "":
        raise ValueError("valor vazio")

    neg = False
    if s.startswith("(") and s.endswith(")"):  # contabil: (1.234,56) = negativo
        neg, s = True, s[1:-1].strip()
    s = s.replace("R$", "").replace("\xa0", "").replace(" ", "")
    if s.endswith("-"):  # sufixo '-' (convencao Itau): marca negativo
        neg, s = True, s[:-1]
    if s.startswith("-"):
        neg, s = True, s[1:]
    if s.startswith("+"):
        s = s[1:]

    has_dot, has_comma = "." in s, "," in s
    if has_dot and has_comma:
        s = s.replace(".", "").replace(",", ".")           # BR: ponto=milhar, virgula=decimal
    elif has_comma:
        s = s.replace(",", ".")                              # BR: virgula=decimal
    elif has_dot:
        if origem != "ofx" and _MILHAR_BR.fullmatch(s):
            s = s.replace(".", "")                           # milhar BR puro: 1.234 -> 1234
        elif s.count(".") > 1:
            s = s.replace(".", "")                           # 1.234.567 -> milhar (qualquer origem)
        # senao: ponto unico = decimal (OFX "1234.56"; ou BR "1.5" = 1,50)
    # so digitos e ponto agora
    if not re.fullmatch(r"\d+(\.\d+)?", s):
        raise ValueError(f"valor nao-numerico: {raw!r}")
    val = Decimal(s).quantize(CENTAVO, rounding=ROUND_HALF_UP)
    return -val if neg else val


_DATE_PATTERNS = (
    ("%d/%m/%Y", re.compile(r"^\d{2}/\d{2}/\d{4}")),
    ("%d/%m/%y", re.compile(r"^\d{2}/\d{2}/\d{2}$")),
    ("%Y-%m-%d", re.compile(r"^\d{4}-\d{2}-\d{2}")),
    ("%d-%m-%Y", re.compile(r"^\d{2}-\d{2}-\d{4}")),
)


def parse_data(raw) -> date:
    """Converte data BR/ISO/OFX para datetime.date.

    OFX DTPOSTED = YYYYMMDD[HHMMSS][.sss][-3:GMT] -> pega os 8 primeiros digitos.
    """
    if raw is None:
        raise ValueError("data vazia")
    s = str(raw).strip()
    if s == "":
        raise ValueError("data vazia")

    # OFX: comeca com 8 digitos AAAAMMDD (com ou sem hora/timezone colado),
    # desde que NAO seja uma data ISO "AAAA-MM-DD".
    m = re.match(r"^(\d{4})(\d{2})(\d{2})", s)
    if m and not s[4:5] == "-":
        y, mo, d = (int(g) for g in m.groups())
        return date(y, mo, d)

    for fmt, pat in _DATE_PATTERNS:
        if pat.match(s):
            clip = {"%d/%m/%Y": 10, "%d/%m/%y": 8, "%Y-%m-%d": 10, "%d-%m-%Y": 10}[fmt]
            return datetime.strptime(s[:clip], fmt).date()
    raise ValueError(f"data em formato nao reconhecido: {raw!r}")


def norm_doc(raw):
    """Normaliza documento/numero: ultima sequencia de digitos sem zeros a esquerda.
    Devolve None se nao houver digito (campo livre tipo 'PIX RECEBIDO')."""
    if raw is None:
        return None
    digs = re.findall(r"\d+", str(raw))
    if not digs:
        return None
    last = digs[-1].lstrip("0")
    return last if last else "0"


def so_digitos(s):
    if s is None:
        return None
    d = re.sub(r"\D", "", str(s))
    return d or None


def extrai_cpf_cnpj(texto):
    """Acha um CPF (11) ou CNPJ (14) num texto livre (ex.: MEMO de PIX).
    Tolera pontuacao ('12.345.678/0001-90'). Deterministico; None se nao houver."""
    if not texto:
        return None
    s = re.sub(r"[.\-/]", "", str(texto))
    for m in re.finditer(r"(?<!\d)(\d{14}|\d{11})(?!\d)", s):
        return m.group(1)
    return None


def norm_cpf_cnpj(raw):
    """Normaliza um campo de CPF/CNPJ (so digitos); valida tamanho 11 ou 14."""
    d = so_digitos(raw)
    return d if d and len(d) in (11, 14) else None


def _sem_acento(s: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


# alias publico: auditor-tarifas/motor/scripts/engine/matcher.py:16 importa "sem_acento"
# (sem underscore). Mantido para nao remover API publica de nenhuma copia (Gate 1A passe 1).
sem_acento = _sem_acento


# ruido comum em descricao de extrato/razao que nao identifica contraparte
_STOP_NOME = {
    "LTDA", "EIRELI", "EPP", "MEI", "PIX", "TED", "DOC", "TEV", "TBI",
    "PAGTO", "PAGAMENTO", "PAGAMENTOS", "RECEBIDO", "RECEBIDA", "RECEBIMENTO",
    "CRED", "CREDITO", "DEB", "DEBITO", "TRANSFERENCIA", "ENVIADO", "ENVIADA",
    "RSHOP", "COMPRA", "CARTAO", "SAQUE", "TAR", "TARIFA", "CXE", "REND", "APLIC",
}


def tokens_nome(texto):
    """Conjunto de tokens significativos de um nome/descricao p/ desempate por overlap.
    Maiusculas, sem acento, so letras, >=3 chars, sem palavras de ruido bancario."""
    if not texto:
        return set()
    s = _sem_acento(str(texto)).upper()
    toks = re.findall(r"[A-Z]{3,}", s)
    return {t for t in toks if t not in _STOP_NOME}
