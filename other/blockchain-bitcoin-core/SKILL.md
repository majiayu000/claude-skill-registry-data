---
name: blockchain-bitcoin-core
description: Bitcoin Core development, RPC integration, UTXO management, and regtest workflows for fintech applications
version: "1.0.0"
domain: blockchain
tags: [bitcoin, bitcoin-core, rpc, utxo, regtest, testnet, fintech, blockchain]
contributed_by: trinance-engineering
---

# SKILL: Blockchain Engineer — Bitcoin Core

## Domain: Bitcoin Core Integration for Fintech Applications

**Activation triggers:** Bitcoin Core RPC, Bitcoin address generation, UTXO management, transaction construction, fee estimation, mempool analysis, block parsing, regtest setup, Bitcoin wallet integration, Bitcoin confirmation tracking.

---

## Critical Rules for Bitcoin Financial Integration

```
NEVER:
  - Use float for Bitcoin amounts (use Decimal or integer satoshis)
  - Credit user balances on 0-confirmation transactions (minimum 1, typically 3-6)
  - Expose Bitcoin Core RPC directly to frontend
  - Store private keys in application database
  - Hardcode Bitcoin addresses in code
  - Ignore blockchain reorganizations in financial accounting
  - Confuse the application ledger with Bitcoin Core's wallet balance

ALWAYS:
  - Use Decimal or integer satoshis for amounts
  - Verify confirmation count before crediting
  - Handle RPC timeouts without assuming failure or success
  - Reconcile application ledger against blockchain state
  - Support regtest / testnet / mainnet via configuration
  - Abstract Bitcoin Core behind a gateway interface
```

## Architecture Pattern

```
Frontend (NEVER accesses Bitcoin directly)
    ↓
Trinance API
    ↓
Bitcoin Application Service
    ↓
BitcoinGateway (interface)
    ↓
Bitcoin Core Adapter (implementation)
    ↓
Bitcoin Core RPC (JSON-RPC 2.0)
```

## Amount Handling

```python
# CORRECT: Use Decimal
from decimal import Decimal
amount_btc = Decimal("0.001")        # 1 mBTC
amount_sats = 100_000                 # 100,000 satoshis = 1 mBTC

# CORRECT: Convert BTC ↔ satoshis
SATS_PER_BTC = Decimal("100000000")  # 10^8
sats = int(amount_btc * SATS_PER_BTC)

# WRONG: Never do this
amount = 0.001  # float — causes rounding errors
```

## RPC Configuration

```python
# regtest (local dev via Polar)
BITCOIN_RPC_URL = "http://localhost:18443"
BITCOIN_NETWORK = "regtest"

# testnet
BITCOIN_RPC_URL = "http://localhost:18332"
BITCOIN_NETWORK = "testnet"

# mainnet
BITCOIN_RPC_URL = "http://localhost:8332"
BITCOIN_NETWORK = "mainnet"
```

## Gateway Interface Template

```python
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Optional

class BitcoinGateway(ABC):
    @abstractmethod
    async def get_blockchain_info(self) -> dict[str, Any]: ...

    @abstractmethod
    async def get_new_address(self, wallet: str, label: str = "", address_type: str = "bech32m") -> str: ...

    @abstractmethod
    async def get_transaction(self, txid: str) -> dict[str, Any]: ...

    @abstractmethod
    async def estimate_smart_fee(self, conf_target: int, mode: str = "conservative") -> Decimal: ...

    @abstractmethod
    async def get_balance(self, wallet: str) -> Decimal:
        """
        Returns node wallet balance (Decimal BTC).
        NOTE: This is for reconciliation only.
        Application ledger is the canonical user balance.
        """
```

## Confirmation Handling

```python
CONFIRMATION_THRESHOLDS = {
    "zero_conf": 0,     # NEVER credit for financial purposes
    "fast": 1,          # Low-value, low-risk only
    "standard": 3,      # Standard transactions
    "high_value": 6,    # High-value transactions
    "very_high": 12,    # Very high value
}

async def on_transaction_detected(txid: str, confirmations: int, amount: Decimal):
    if confirmations < CONFIRMATION_THRESHOLDS["standard"]:
        # Update payment status to CONFIRMING — do not credit ledger yet
        await payment_service.transition(payment_id, PaymentStatus.CONFIRMING)
    elif confirmations >= CONFIRMATION_THRESHOLDS["standard"]:
        # Now safe to credit ledger
        await payment_service.transition(payment_id, PaymentStatus.SUCCEEDED)
        await ledger_service.create_journal_entry(...)
```

## Reorg Handling

```python
# If a transaction loses confirmations (reorg):
# 1. Detect via monitoring: confirmations drops or tx disappears
# 2. Reverse the ledger entry if already credited
# 3. Set payment to RECONCILIATION_REQUIRED
# 4. Alert operations team
# 5. Never silently correct financial records

async def handle_reorg(txid: str):
    payment = await payment_service.get_by_provider_reference(txid)
    if payment and payment.status == PaymentStatus.SUCCEEDED:
        await payment_service.transition(
            payment.id, PaymentStatus.RECONCILIATION_REQUIRED,
            reason="Blockchain reorganization detected"
        )
        await alert_operations("Bitcoin reorg detected", txid=txid)
```

## Polar Regtest Workflow

```bash
# Start Bitcoin regtest via Polar
# Mine initial blocks (coinbase maturity = 100 blocks)
# Fund LND / CLN channels

# Via Polar MCP or direct RPC:
curl -u user:pass http://localhost:18443 \
  -d '{"method":"generatetoaddress","params":[101,"bcrt1q..."]}'

# Get new address for deposit testing:
curl -u user:pass http://localhost:18443 \
  -d '{"method":"getnewaddress","params":["test-deposit","bech32m"]}'
```

## Fee Estimation

```python
async def estimate_withdrawal_fee(conf_target: int = 3) -> Decimal:
    """
    Estimate fee for withdrawal in sat/vByte.
    Returns Decimal — never float.
    """
    fee_rate = await bitcoin_gateway.estimate_smart_fee(conf_target, "conservative")
    # fee_rate is BTC/kB from Core — convert to sat/vByte
    sat_per_vbyte = int(fee_rate * Decimal("100000"))  # BTC/kB → sat/vByte
    return Decimal(sat_per_vbyte)
```

## Security Checklist

```
□ Bitcoin Core RPC is NOT exposed to the internet (bind to localhost)
□ RPC authentication enabled (rpcauth or rpcuser/rpcpassword)
□ Wallet encryption enabled for production
□ Separate wallets per purpose (hot, cold, fee)
□ Minimum confirmations enforced before credit
□ Reorg detection implemented
□ Reconciliation scheduled regularly
□ Private keys never in application code or database
□ Hardware signing for large transactions (future)
□ Multi-sig for custody wallets (future)
```
