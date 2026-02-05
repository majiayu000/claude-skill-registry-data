---
name: brazilian-financial-integration
description: Implement Brazilian financial system integrations including Boleto generation, PIX payments, parcelamento (installments), CPF/CNPJ validation, and Banco do Brasil API integration. Use this skill when building fintech applications, payment processing systems, or any system requiring Brazilian banking compliance.
---

# Brazilian Financial Integration Skill

## Overview

This skill provides comprehensive patterns for integrating Brazilian financial systems and payment methods. It covers Boleto bank slip generation, PIX instant payments, installment plans (parcelamento), Brazilian tax ID validation, and banking API integrations.

## When to Use This Skill

- Building fintech or payment processing systems for Brazil
- Implementing Boleto bank slip generation
- Integrating PIX instant payment system
- Creating installment payment plans (parcelamento)
- Validating CPF/CNPJ tax identification numbers
- Integrating with Brazilian banking APIs (Banco do Brasil, Itaú, etc.)
- Handling Brazilian currency and date formats

## Core Concepts

### Brazilian Payment Methods

1. **Boleto Bancário** (Bank Slip)
   - Paper or digital payment slip
   - Barcode for bank processing
   - Payment deadline (vencimento)
   - Widely used for bills and purchases

2. **PIX** (Instant Payment)
   - Real-time payment system
   - QR Code or key-based
   - 24/7 availability
   - Transaction fees typically lower than boleto

3. **Parcelamento** (Installments)
   - Split payments over multiple months
   - Fixed or variable amounts
   - Interest calculations
   - Payment schedules

### Brazilian Tax IDs

- **CPF** (Cadastro de Pessoas Físicas): Individual taxpayer ID (11 digits)
- **CNPJ** (Cadastro Nacional da Pessoa Jurídica): Company taxpayer ID (14 digits)

## Project Structure for Financial Module

```
src/
├── domain/
│   ├── modules/
│   │   ├── boleto/
│   │   │   ├── entity.py              # Boleto domain entity
│   │   │   ├── generator.py           # IBoletoGenerator interface
│   │   │   ├── barcode.py             # Barcode generation logic
│   │   │   └── validator.py           # Boleto validation rules
│   │   ├── pix/
│   │   │   ├── entity.py              # CobrancaPix entity
│   │   │   ├── payment_strategy.py    # IPixPaymentStrategy
│   │   │   └── qrcode_generator.py    # QR code generation
│   │   ├── parcelamento/
│   │   │   ├── entity.py              # Parcelamento entity
│   │   │   ├── calculator.py          # Interest/installment calculator
│   │   │   └── strategy.py            # Payment strategies
│   │   └── shared/
│   │       ├── cpf_cnpj_validator.py  # Tax ID validation
│   │       └── currency.py            # Brazilian currency helpers
│   └── infra/
│       ├── payment/
│       │   ├── bb_api_adapter.py      # Banco do Brasil API
│       │   ├── boleto_pdf_generator.py # PDF generation (reportlab)
│       │   └── pix_api_client.py      # PIX API integration
│       └── database/
│           └── alchemist/
│               └── modules/
│                   ├── boleto/
│                   ├── pix/
│                   └── parcelamento/
```

## Implementation Patterns

### 1. CPF/CNPJ Validation

```python
# src/domain/modules/shared/cpf_cnpj_validator.py
import re
from typing import Literal

class CPFCNPJValidator:
    """Validator for Brazilian CPF and CNPJ tax IDs.

    Implements official validation algorithms with check digits.
    """

    @staticmethod
    def clean(value: str) -> str:
        """Remove non-numeric characters from CPF/CNPJ."""
        return re.sub(r'\D', '', value)

    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """Validate CPF using official algorithm.

        Args:
            cpf: CPF string (can contain formatting)

        Returns:
            True if valid, False otherwise
        """
        cpf = CPFCNPJValidator.clean(cpf)

        # Check length
        if len(cpf) != 11:
            return False

        # Check for invalid patterns (all same digits)
        if cpf == cpf[0] * 11:
            return False

        # Check for known invalid values
        invalid_values = ['00000000000', '11111111111', '22222222222',
                         '33333333333', '44444444444', '55555555555',
                         '66666666666', '77777777777', '88888888888',
                         '99999999999']
        if cpf in invalid_values:
            return False

        # Calculate first check digit
        sum_digits = sum(int(cpf[i]) * (10 - i) for i in range(9))
        first_check = (sum_digits * 10) % 11
        first_check = 0 if first_check == 10 else first_check

        if int(cpf[9]) != first_check:
            return False

        # Calculate second check digit
        sum_digits = sum(int(cpf[i]) * (11 - i) for i in range(10))
        second_check = (sum_digits * 10) % 11
        second_check = 0 if second_check == 10 else second_check

        return int(cpf[10]) == second_check

    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        """Validate CNPJ using official algorithm.

        Args:
            cnpj: CNPJ string (can contain formatting)

        Returns:
            True if valid, False otherwise
        """
        cnpj = CPFCNPJValidator.clean(cnpj)

        # Check length
        if len(cnpj) != 14:
            return False

        # Check for invalid patterns
        if cnpj == cnpj[0] * 14:
            return False

        # Calculate first check digit
        weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_digits = sum(int(cnpj[i]) * weights_1[i] for i in range(12))
        first_check = sum_digits % 11
        first_check = 0 if first_check < 2 else 11 - first_check

        if int(cnpj[12]) != first_check:
            return False

        # Calculate second check digit
        weights_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_digits = sum(int(cnpj[i]) * weights_2[i] for i in range(13))
        second_check = sum_digits % 11
        second_check = 0 if second_check < 2 else 11 - second_check

        return int(cnpj[13]) == second_check

    @staticmethod
    def validate(value: str) -> tuple[bool, Literal["CPF", "CNPJ", None]]:
        """Validate CPF or CNPJ automatically.

        Args:
            value: CPF or CNPJ string

        Returns:
            Tuple of (is_valid, document_type)
        """
        cleaned = CPFCNPJValidator.clean(value)

        if len(cleaned) == 11:
            return CPFCNPJValidator.validate_cpf(cleaned), "CPF"
        elif len(cleaned) == 14:
            return CPFCNPJValidator.validate_cnpj(cleaned), "CNPJ"
        else:
            return False, None

    @staticmethod
    def format_cpf(cpf: str) -> str:
        """Format CPF as XXX.XXX.XXX-XX."""
        cleaned = CPFCNPJValidator.clean(cpf)
        return f"{cleaned[:3]}.{cleaned[3:6]}.{cleaned[6:9]}-{cleaned[9:]}"

    @staticmethod
    def format_cnpj(cnpj: str) -> str:
        """Format CNPJ as XX.XXX.XXX/XXXX-XX."""
        cleaned = CPFCNPJValidator.clean(cnpj)
        return f"{cleaned[:2]}.{cleaned[2:5]}.{cleaned[5:8]}/{cleaned[8:12]}-{cleaned[12:]}"
```

### 2. Boleto Entity and Generation

```python
# src/domain/modules/boleto/entity.py
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

@dataclass
class Boleto:
    """Boleto bancário domain entity.

    Represents a Brazilian bank slip payment.
    """
    id: int | None
    numero_documento: str  # Document number
    valor_principal: Decimal  # Principal amount
    valor_desconto: Decimal  # Discount amount
    valor_multa: Decimal  # Late fee
    valor_juros: Decimal  # Interest
    data_vencimento: date  # Due date
    data_emissao: date  # Issue date
    nosso_numero: str  # Bank's reference number
    codigo_barras: str  # Barcode number
    linha_digitavel: str  # Typeable line
    pagador_cpf_cnpj: str  # Payer tax ID
    pagador_nome: str  # Payer name
    pagador_endereco: str | None  # Payer address
    beneficiario_nome: str  # Beneficiary name
    beneficiario_cpf_cnpj: str  # Beneficiary tax ID
    instrucoes: str | None  # Payment instructions
    created_at: datetime
    status: str = "PENDENTE"  # PENDENTE, PAGO, CANCELADO, VENCIDO

    @property
    def valor_total(self) -> Decimal:
        """Calculate total amount including fees."""
        return (
            self.valor_principal
            + self.valor_multa
            + self.valor_juros
            - self.valor_desconto
        )

    @property
    def esta_vencido(self) -> bool:
        """Check if boleto is past due date."""
        return date.today() > self.data_vencimento

    def aplicar_multa_juros(self, dias_atraso: int) -> None:
        """Apply late fees based on days overdue.

        Business rule: 2% late fee + 0.033% daily interest.
        """
        if dias_atraso > 0:
            # 2% late fee
            self.valor_multa = self.valor_principal * Decimal("0.02")
            # 0.033% daily interest (1% per month / 30 days)
            self.valor_juros = (
                self.valor_principal * Decimal("0.00033") * dias_atraso
            )


# src/domain/modules/boleto/generator.py
from abc import ABC, abstractmethod
from src.domain.modules.boleto.entity import Boleto

class IBoletoGenerator(ABC):
    """Abstract interface for boleto generation."""

    @abstractmethod
    async def generate_barcode(self, boleto: Boleto) -> str:
        """Generate barcode number for boleto."""
        pass

    @abstractmethod
    async def generate_linha_digitavel(self, codigo_barras: str) -> str:
        """Generate typeable line from barcode."""
        pass

    @abstractmethod
    async def generate_pdf(self, boleto: Boleto) -> bytes:
        """Generate PDF file for boleto."""
        pass
```

### 3. Boleto Barcode Generation

```python
# src/domain/modules/boleto/barcode.py
from decimal import Decimal
from datetime import date

class BoletoBarcode:
    """Generate boleto barcode using FEBRABAN standards.

    Reference: FEBRABAN specification for bank slip barcodes.
    """

    # Base date for boleto calculation (October 7, 1997)
    BASE_DATE = date(1997, 10, 7)

    @staticmethod
    def calculate_fator_vencimento(data_vencimento: date) -> str:
        """Calculate fator de vencimento (due date factor).

        Days between base date and due date.
        """
        days = (data_vencimento - BoletoBarcode.BASE_DATE).days
        return str(days).zfill(4)

    @staticmethod
    def format_valor(valor: Decimal) -> str:
        """Format amount for barcode (10 digits, no decimal point)."""
        # Convert to cents and remove decimal
        valor_cents = int(valor * 100)
        return str(valor_cents).zfill(10)

    @staticmethod
    def calculate_dv_modulo11(codigo: str) -> int:
        """Calculate check digit using modulo 11 algorithm."""
        sequence = [2, 3, 4, 5, 6, 7, 8, 9]
        total = 0
        seq_idx = 0

        # Sum from right to left
        for digit in reversed(codigo):
            total += int(digit) * sequence[seq_idx % len(sequence)]
            seq_idx += 1

        remainder = total % 11
        dv = 11 - remainder

        # Special cases
        if dv == 0 or dv == 10 or dv == 11:
            return 1
        return dv

    @classmethod
    def generate(
        cls,
        banco: str,  # 3 digits
        moeda: str,  # 1 digit (9 = Real)
        data_vencimento: date,
        valor: Decimal,
        campo_livre: str,  # 25 digits (bank-specific)
    ) -> str:
        """Generate 44-digit barcode.

        Format: AAABC.CCCCDE.EEEEE.EEEEEE.FFFFF.FFFFFF.G.HHHH.IIIIIIIIII
        - AAA: Bank code (3 digits)
        - B: Currency code (1 digit, always 9 for BRL)
        - G: Check digit (1 digit)
        - HHHH: Due date factor (4 digits)
        - IIIIIIIIII: Amount (10 digits)
        - Campo livre: 25 digits (bank-specific)
        """
        # Build barcode without check digit
        fator_vencimento = cls.calculate_fator_vencimento(data_vencimento)
        valor_formatado = cls.format_valor(valor)

        # Initial code without DV
        codigo_sem_dv = (
            f"{banco}{moeda}{fator_vencimento}{valor_formatado}{campo_livre}"
        )

        # Calculate check digit
        dv = cls.calculate_dv_modulo11(codigo_sem_dv)

        # Final barcode with DV in position 5
        codigo_barras = f"{banco}{moeda}{dv}{fator_vencimento}{valor_formatado}{campo_livre}"

        return codigo_barras

    @staticmethod
    def generate_linha_digitavel(codigo_barras: str) -> str:
        """Generate typeable line from barcode.

        Splits barcode into 5 fields with check digits.
        Format: AAAAA.AAAAA BBBBB.BBBBBB CCCCC.CCCCCC D EEEEEEEEEEEEE
        """
        # Extract parts from barcode
        banco_moeda = codigo_barras[0:4]
        dv_geral = codigo_barras[4]
        campo_livre = codigo_barras[19:44]
        fator_vencimento = codigo_barras[5:9]
        valor = codigo_barras[9:19]

        # Field 1: Bank + Currency + first 5 of campo livre
        campo1 = banco_moeda + campo_livre[0:5]
        dv1 = BoletoBarcode.calculate_dv_modulo10(campo1)
        campo1_formatado = f"{campo1[0:5]}.{campo1[5:]}{dv1}"

        # Field 2: Next 10 digits of campo livre
        campo2 = campo_livre[5:15]
        dv2 = BoletoBarcode.calculate_dv_modulo10(campo2)
        campo2_formatado = f"{campo2[0:5]}.{campo2[5:]}{dv2}"

        # Field 3: Last 10 digits of campo livre
        campo3 = campo_livre[15:25]
        dv3 = BoletoBarcode.calculate_dv_modulo10(campo3)
        campo3_formatado = f"{campo3[0:5]}.{campo3[5:]}{dv3}"

        # Field 4: General check digit
        campo4 = dv_geral

        # Field 5: Due date factor + amount
        campo5 = fator_vencimento + valor

        return f"{campo1_formatado} {campo2_formatado} {campo3_formatado} {campo4} {campo5}"

    @staticmethod
    def calculate_dv_modulo10(codigo: str) -> int:
        """Calculate check digit using modulo 10 algorithm."""
        sequence = [2, 1]
        total = 0
        seq_idx = 0

        for digit in reversed(codigo):
            produto = int(digit) * sequence[seq_idx % 2]
            # If product > 9, sum digits
            total += produto if produto < 10 else sum(int(d) for d in str(produto))
            seq_idx += 1

        remainder = total % 10
        return 0 if remainder == 0 else 10 - remainder
```

### 4. PIX Payment Integration

```python
# src/domain/modules/pix/entity.py
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class CobrancaPix:
    """PIX charge entity.

    Represents a PIX instant payment charge.
    """
    id: int | None
    txid: str  # Transaction ID (26-35 characters)
    chave_pix: str  # PIX key (CPF, CNPJ, email, phone, or random)
    valor: Decimal
    descricao: str | None
    qrcode_texto: str  # QR code text (EMV format)
    qrcode_imagem: str | None  # Base64 encoded image
    expiracao: int  # Expiration in seconds
    pagador_cpf_cnpj: str | None
    status: str  # ATIVA, CONCLUIDA, REMOVIDA_PELO_USUARIO_RECEBEDOR
    created_at: datetime
    paid_at: datetime | None = None

    @property
    def is_expired(self) -> bool:
        """Check if PIX charge has expired."""
        if self.status != "ATIVA":
            return False
        elapsed = (datetime.now() - self.created_at).total_seconds()
        return elapsed > self.expiracao


# src/domain/modules/pix/payment_strategy.py
from abc import ABC, abstractmethod
from src.domain.modules.pix.entity import CobrancaPix

class IPixPaymentStrategy(ABC):
    """Abstract interface for PIX payment processing."""

    @abstractmethod
    async def create_charge(
        self,
        valor: Decimal,
        chave_pix: str,
        descricao: str | None = None,
        expiracao: int = 3600,
    ) -> CobrancaPix:
        """Create PIX charge with QR code."""
        pass

    @abstractmethod
    async def check_payment_status(self, txid: str) -> str:
        """Check payment status by transaction ID."""
        pass

    @abstractmethod
    async def cancel_charge(self, txid: str) -> bool:
        """Cancel active PIX charge."""
        pass
```

### 5. Banco do Brasil PIX API Adapter

```python
# src/infra/payment/bb_pix_adapter.py
import base64
import httpx
from decimal import Decimal
from datetime import datetime

from src.domain.modules.pix.entity import CobrancaPix
from src.domain.modules.pix.payment_strategy import IPixPaymentStrategy

class BancoDoBrasilPixAdapter(IPixPaymentStrategy):
    """Banco do Brasil PIX API integration.

    Implements PIX payment processing using BB's API.
    Reference: https://developers.bb.com.br/
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        developer_key: str,
        gw_dev_app_key: str,
        base_url: str = "https://api.bb.com.br/pix/v2",
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.developer_key = developer_key
        self.gw_dev_app_key = gw_dev_app_key
        self.base_url = base_url
        self._token: str | None = None
        self._token_expires_at: datetime | None = None

    async def _get_access_token(self) -> str:
        """Obtain OAuth2 access token from BB."""
        if self._token and self._token_expires_at > datetime.now():
            return self._token

        auth_url = "https://oauth.bb.com.br/oauth/token"
        headers = {
            "Authorization": f"Basic {self._encode_credentials()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "client_credentials", "scope": "cob.read cob.write"}

        async with httpx.AsyncClient() as client:
            response = await client.post(auth_url, headers=headers, data=data)
            response.raise_for_status()
            token_data = response.json()

        self._token = token_data["access_token"]
        expires_in = token_data["expires_in"]
        self._token_expires_at = datetime.now() + timedelta(seconds=expires_in)

        return self._token

    def _encode_credentials(self) -> str:
        """Encode client credentials for Basic Auth."""
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode()).decode()

    async def create_charge(
        self,
        valor: Decimal,
        chave_pix: str,
        descricao: str | None = None,
        expiracao: int = 3600,
    ) -> CobrancaPix:
        """Create PIX charge using BB API.

        Returns CobrancaPix with QR code data.
        """
        token = await self._get_access_token()
        txid = self._generate_txid()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Developer-Application-Key": self.developer_key,
            "gw-dev-app-key": self.gw_dev_app_key,
        }

        payload = {
            "calendario": {"expiracao": expiracao},
            "devedor": {},  # Optional payer info
            "valor": {"original": f"{valor:.2f}"},
            "chave": chave_pix,
            "solicitacaoPagador": descricao or "Pagamento via PIX",
        }

        url = f"{self.base_url}/cob/{txid}"

        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        # Get QR code
        qrcode_url = f"{self.base_url}/cob/{txid}/qrcode"
        async with httpx.AsyncClient() as client:
            qr_response = await client.get(qrcode_url, headers=headers)
            qr_response.raise_for_status()
            qr_data = qr_response.json()

        return CobrancaPix(
            id=None,
            txid=txid,
            chave_pix=chave_pix,
            valor=valor,
            descricao=descricao,
            qrcode_texto=qr_data["qrcode"],
            qrcode_imagem=qr_data.get("imagemQrcode"),
            expiracao=expiracao,
            pagador_cpf_cnpj=None,
            status=data["status"],
            created_at=datetime.now(),
        )

    async def check_payment_status(self, txid: str) -> str:
        """Check PIX charge status."""
        token = await self._get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Developer-Application-Key": self.developer_key,
            "gw-dev-app-key": self.gw_dev_app_key,
        }

        url = f"{self.base_url}/cob/{txid}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        return data["status"]

    async def cancel_charge(self, txid: str) -> bool:
        """Cancel PIX charge (not supported by BB, returns False)."""
        # BB API doesn't support cancellation, charge expires automatically
        return False

    @staticmethod
    def _generate_txid() -> str:
        """Generate unique transaction ID (26-35 characters alphanumeric)."""
        import uuid
        return str(uuid.uuid4()).replace("-", "")[:35]
```

### 6. Parcelamento (Installment) Calculation

```python
# src/domain/modules/parcelamento/calculator.py
from decimal import Decimal, ROUND_HALF_UP
from datetime import date
from dateutil.relativedelta import relativedelta

class ParcelamentoCalculator:
    """Calculate installment payments with interest.

    Implements Brazilian installment payment calculations.
    """

    @staticmethod
    def calculate_parcelas(
        valor_total: Decimal,
        numero_parcelas: int,
        taxa_juros_mensal: Decimal = Decimal("0"),
        data_primeira_parcela: date | None = None,
    ) -> list[dict]:
        """Calculate installment schedule.

        Args:
            valor_total: Total amount to be split
            numero_parcelas: Number of installments
            taxa_juros_mensal: Monthly interest rate (0.05 = 5%)
            data_primeira_parcela: First installment due date

        Returns:
            List of installment dictionaries with valor and vencimento
        """
        if data_primeira_parcela is None:
            data_primeira_parcela = date.today() + relativedelta(months=1)

        parcelas = []

        if taxa_juros_mensal == 0:
            # Simple division without interest
            valor_parcela = (valor_total / numero_parcelas).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            resto = valor_total - (valor_parcela * numero_parcelas)

            for i in range(numero_parcelas):
                vencimento = data_primeira_parcela + relativedelta(months=i)
                valor = valor_parcela
                # Add remaining cents to last installment
                if i == numero_parcelas - 1:
                    valor += resto

                parcelas.append({
                    "numero": i + 1,
                    "valor": valor,
                    "vencimento": vencimento,
                })
        else:
            # Price table calculation (tabela price)
            taxa = taxa_juros_mensal
            fator = ((1 + taxa) ** numero_parcelas * taxa) / (
                (1 + taxa) ** numero_parcelas - 1
            )
            valor_parcela = (valor_total * fator).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

            saldo_devedor = valor_total

            for i in range(numero_parcelas):
                vencimento = data_primeira_parcela + relativedelta(months=i)
                juros = (saldo_devedor * taxa).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
                amortizacao = valor_parcela - juros

                # Last installment adjustment
                if i == numero_parcelas - 1:
                    amortizacao = saldo_devedor
                    valor_parcela = amortizacao + juros

                parcelas.append({
                    "numero": i + 1,
                    "valor": valor_parcela,
                    "valor_amortizacao": amortizacao,
                    "valor_juros": juros,
                    "saldo_devedor": saldo_devedor,
                    "vencimento": vencimento,
                })

                saldo_devedor -= amortizacao

        return parcelas

    @staticmethod
    def calculate_discount_for_pix(
        valor_total: Decimal,
        percentual_desconto: Decimal = Decimal("0.025"),  # 2.5%
    ) -> tuple[Decimal, Decimal]:
        """Calculate PIX discount.

        Args:
            valor_total: Total amount
            percentual_desconto: Discount percentage (default 2.5%)

        Returns:
            Tuple of (discounted_amount, discount_value)
        """
        desconto = (valor_total * percentual_desconto).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        valor_com_desconto = valor_total - desconto
        return valor_com_desconto, desconto
```

### 7. Brazilian Currency and Date Helpers

```python
# src/domain/modules/shared/currency.py
from decimal import Decimal
from datetime import date

class BrazilianCurrency:
    """Brazilian Real (BRL) formatting helpers."""

    @staticmethod
    def format(valor: Decimal) -> str:
        """Format amount as Brazilian Real.

        Example: Decimal("1234.56") -> "R$ 1.234,56"
        """
        valor_str = f"{valor:,.2f}"
        # Swap , and . for Brazilian format
        valor_br = valor_str.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {valor_br}"

    @staticmethod
    def parse(valor_str: str) -> Decimal:
        """Parse Brazilian Real string to Decimal.

        Example: "R$ 1.234,56" -> Decimal("1234.56")
        """
        # Remove currency symbol and spaces
        cleaned = valor_str.replace("R$", "").replace(" ", "")
        # Convert to standard format
        standard = cleaned.replace(".", "").replace(",", ".")
        return Decimal(standard)


class BrazilianDate:
    """Brazilian date formatting helpers."""

    @staticmethod
    def format(data: date) -> str:
        """Format date as DD/MM/YYYY."""
        return data.strftime("%d/%m/%Y")

    @staticmethod
    def parse(data_str: str) -> date:
        """Parse DD/MM/YYYY string to date."""
        return datetime.strptime(data_str, "%d/%m/%Y").date()

    @staticmethod
    def extenso(data: date) -> str:
        """Format date in Brazilian Portuguese long form.

        Example: date(2024, 1, 15) -> "15 de janeiro de 2024"
        """
        meses = [
            "janeiro", "fevereiro", "março", "abril", "maio", "junho",
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
        ]
        dia = data.day
        mes = meses[data.month - 1]
        ano = data.year
        return f"{dia} de {mes} de {ano}"
```

## Database Schema Patterns

### Boleto Table (ptBR naming)

```sql
CREATE TABLE boleto (
    id SERIAL PRIMARY KEY,
    numero_documento VARCHAR(20) NOT NULL UNIQUE,
    valor_principal DECIMAL(10, 2) NOT NULL,
    valor_desconto DECIMAL(10, 2) DEFAULT 0,
    valor_multa DECIMAL(10, 2) DEFAULT 0,
    valor_juros DECIMAL(10, 2) DEFAULT 0,
    data_vencimento DATE NOT NULL,
    data_emissao DATE NOT NULL DEFAULT CURRENT_DATE,
    nosso_numero VARCHAR(20) NOT NULL UNIQUE,
    codigo_barras VARCHAR(44) NOT NULL,
    linha_digitavel VARCHAR(54) NOT NULL,
    pagador_cpf_cnpj VARCHAR(14) NOT NULL,
    pagador_nome VARCHAR(100) NOT NULL,
    pagador_endereco TEXT,
    beneficiario_nome VARCHAR(100) NOT NULL,
    beneficiario_cpf_cnpj VARCHAR(14) NOT NULL,
    instrucoes TEXT,
    status VARCHAR(20) DEFAULT 'PENDENTE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_status CHECK (status IN ('PENDENTE', 'PAGO', 'CANCELADO', 'VENCIDO'))
);

CREATE INDEX idx_boleto_cpf_cnpj ON boleto(pagador_cpf_cnpj);
CREATE INDEX idx_boleto_vencimento ON boleto(data_vencimento);
CREATE INDEX idx_boleto_status ON boleto(status);
```

### PIX Table

```sql
CREATE TABLE cobranca_pix (
    id SERIAL PRIMARY KEY,
    txid VARCHAR(35) NOT NULL UNIQUE,
    chave_pix VARCHAR(100) NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    descricao TEXT,
    qrcode_texto TEXT NOT NULL,
    qrcode_imagem TEXT,
    expiracao INTEGER NOT NULL DEFAULT 3600,
    pagador_cpf_cnpj VARCHAR(14),
    status VARCHAR(50) DEFAULT 'ATIVA',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP,

    CONSTRAINT chk_pix_status CHECK (status IN ('ATIVA', 'CONCLUIDA', 'REMOVIDA_PELO_USUARIO_RECEBEDOR'))
);

CREATE INDEX idx_pix_txid ON cobranca_pix(txid);
CREATE INDEX idx_pix_status ON cobranca_pix(status);
```

### Parcelamento Table

```sql
CREATE TABLE parcelamento (
    id SERIAL PRIMARY KEY,
    tipo_cobranca_id INTEGER NOT NULL,
    numero_parcelas INTEGER NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    taxa_juros_mensal DECIMAL(5, 4) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (tipo_cobranca_id) REFERENCES tipo_cobranca(id)
);

CREATE TABLE parcela (
    id SERIAL PRIMARY KEY,
    parcelamento_id INTEGER,
    boleto_id INTEGER,
    pix_id INTEGER,
    numero INTEGER NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    valor_amortizacao DECIMAL(10, 2),
    valor_juros DECIMAL(10, 2),
    data_vencimento DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDENTE',

    FOREIGN KEY (parcelamento_id) REFERENCES parcelamento(id),
    FOREIGN KEY (boleto_id) REFERENCES boleto(id),
    FOREIGN KEY (pix_id) REFERENCES cobranca_pix(id),

    -- Constraint: parcela must have either boleto_id OR pix_id, not both
    CONSTRAINT chk_payment_method CHECK (
        (boleto_id IS NOT NULL AND pix_id IS NULL) OR
        (boleto_id IS NULL AND pix_id IS NOT NULL)
    )
);
```

## API Endpoint Examples

### Boleto Endpoints

```python
# src/api/path/boleto.py
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from src.api.schemas.boleto import BoletoCreateRequest, BoletoResponse
from src.domain.modules.boleto.service import IBoletoService
from src.config.dependency import Container

router = APIRouter(prefix="/v1/boletos", tags=["boletos"])

@router.post("/", response_model=BoletoResponse, status_code=status.HTTP_201_CREATED)
@inject
async def create_boleto(
    request: BoletoCreateRequest,
    service: IBoletoService = Depends(Provide[Container.boleto_service]),
):
    """Create new boleto bank slip."""
    boleto = await service.create_boleto(
        valor_principal=request.valor_principal,
        data_vencimento=request.data_vencimento,
        pagador_cpf_cnpj=request.pagador_cpf_cnpj,
        pagador_nome=request.pagador_nome,
    )
    return BoletoResponse.from_entity(boleto)

@router.get("/{boleto_id}/pdf")
@inject
async def download_boleto_pdf(
    boleto_id: int,
    service: IBoletoService = Depends(Provide[Container.boleto_service]),
):
    """Download boleto PDF file."""
    pdf_bytes = await service.generate_pdf(boleto_id)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=boleto_{boleto_id}.pdf"},
    )
```

### PIX Endpoints

```python
# src/api/path/pix.py
@router.post("/cobrancas", response_model=PixCobrancaResponse)
@inject
async def create_pix_charge(
    request: PixCobrancaRequest,
    service: IPixService = Depends(Provide[Container.pix_service]),
):
    """Create PIX charge with QR code."""
    cobranca = await service.create_charge(
        valor=request.valor,
        chave_pix=request.chave_pix,
        descricao=request.descricao,
        expiracao=request.expiracao or 3600,
    )
    return PixCobrancaResponse.from_entity(cobranca)

@router.get("/cobrancas/{txid}/status")
@inject
async def check_pix_status(
    txid: str,
    service: IPixService = Depends(Provide[Container.pix_service]),
):
    """Check PIX payment status."""
    status = await service.check_payment_status(txid)
    return {"txid": txid, "status": status}
```

## Best Practices

### CPF/CNPJ Handling
- ✅ Always validate before storing
- ✅ Store in cleaned format (numbers only)
- ✅ Format for display using helper functions
- ✅ Index CPF/CNPJ columns for performance
- ✅ Handle null values properly (not all entities require tax ID)

### Boleto Generation
- ✅ Use FEBRABAN standards for barcode
- ✅ Validate all required fields before generation
- ✅ Store nosso_numero (bank reference) for tracking
- ✅ Generate PDF asynchronously for better performance
- ✅ Implement proper late fee calculations

### PIX Integration
- ✅ Cache OAuth tokens to reduce API calls
- ✅ Handle token expiration gracefully
- ✅ Implement webhook for payment notifications
- ✅ Set reasonable expiration times (default 1 hour)
- ✅ Log all API interactions for debugging

### Parcelamento
- ✅ Use Decimal for all monetary calculations
- ✅ Round using ROUND_HALF_UP for consistency
- ✅ Adjust last installment for rounding differences
- ✅ Support both simple and compound interest
- ✅ Validate minimum installment amounts

### Database
- ✅ Use ptBR naming for Brazilian-specific fields
- ✅ Add check constraints for status fields
- ✅ Index frequently queried columns (CPF, status, dates)
- ✅ Use DECIMAL(10,2) for currency values
- ✅ Store dates without timezone for due dates

## Testing Strategy

```python
# tests/domain/modules/shared/test_cpf_cnpj_validator.py
def test_validate_valid_cpf():
    """Test valid CPF validation."""
    assert CPFCNPJValidator.validate_cpf("12345678909") is True
    assert CPFCNPJValidator.validate_cpf("123.456.789-09") is True

def test_validate_invalid_cpf():
    """Test invalid CPF validation."""
    assert CPFCNPJValidator.validate_cpf("11111111111") is False
    assert CPFCNPJValidator.validate_cpf("12345678900") is False

def test_validate_valid_cnpj():
    """Test valid CNPJ validation."""
    assert CPFCNPJValidator.validate_cnpj("11222333000181") is True

# tests/domain/modules/boleto/test_barcode.py
def test_generate_barcode():
    """Test boleto barcode generation."""
    codigo = BoletoBarcode.generate(
        banco="001",
        moeda="9",
        data_vencimento=date(2024, 12, 31),
        valor=Decimal("100.00"),
        campo_livre="1234567890123456789012345",
    )
    assert len(codigo) == 44
    assert codigo[0:3] == "001"  # Bank code
    assert codigo[3] == "9"  # Currency

# tests/domain/modules/parcelamento/test_calculator.py
def test_calculate_parcelas_without_interest():
    """Test simple installment calculation."""
    parcelas = ParcelamentoCalculator.calculate_parcelas(
        valor_total=Decimal("1000.00"),
        numero_parcelas=10,
        taxa_juros_mensal=Decimal("0"),
    )
    assert len(parcelas) == 10
    assert all(p["valor"] == Decimal("100.00") for p in parcelas)
```

## Common Pitfalls

1. **Floating Point for Currency**
   - ❌ Never use `float` for money
   - ✅ Always use `Decimal` type

2. **CPF/CNPJ Formatting in Database**
   - ❌ Don't store formatted values (with dots/dashes)
   - ✅ Store cleaned numeric values, format on display

3. **Timezone Issues**
   - ❌ Don't use timezone-aware dates for vencimento
   - ✅ Use plain `date` type for due dates

4. **Rounding Errors**
   - ❌ Don't ignore cents in installment calculations
   - ✅ Adjust last installment for rounding differences

5. **API Token Management**
   - ❌ Don't request new token for every API call
   - ✅ Cache tokens and refresh before expiration

## References

- [FEBRABAN Barcode Standard](https://portal.febraban.org.br/)
- [Banco do Brasil PIX API](https://developers.bb.com.br/)
- [CPF Validation Algorithm](http://www.receita.fazenda.gov.br/)
- [CNPJ Validation Algorithm](http://www.receita.fazenda.gov.br/)
- [Brazilian Central Bank - PIX](https://www.bcb.gov.br/estabilidadefinanceira/pix)

## Production Examples

Based on patterns from:
- **GEFIN Backend**: Boleto, PIX, and parcelamento implementations
- **Brazilian Banking Standards**: FEBRABAN compliance
- **Banco do Brasil API**: Production-tested PIX integration
