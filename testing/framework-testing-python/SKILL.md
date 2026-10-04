---
name: framework-testing-python
description: "Atua como Especialista em Testes Automatizados e Engenharia de QA em Python, cobrindo o ecossistema Pytest e o framework nativo Unittest. Domina Fixtures modulares, conftest.py, parametrização formal (BVA/Partições de Equivalência), subTests, Property-Based Testing (Hypothesis), Mocks (unittest.mock, @patch, MagicMock, pytest-mock), Testes de Mutação (mutmut), testes assíncronos (pytest-asyncio) e análise de cobertura (pytest-cov)."
---

# Testes Automatizados em Python: Pytest & Unittest

Esta skill estabelece os padrões e metodologias de engenharia para desenvolvimento e automação de suítes de testes em Python, integrando o ecossistema avançado do **Pytest** e a biblioteca padrão orientada a objetos **Unittest**.

---

## 🧭 1. Comparativo e Diretrizes de Seleção de Framework

| Aspecto | Pytest | Unittest (Standard Library) |
| :--- | :--- | :--- |
| **Estilo / Paradigma** | Funcional com fixtures e asserts nativos | Orientado a Objetos derivando de `unittest.TestCase` |
| **Asserts** | `assert expressao` (com AST rewriting rico) | `self.assertEqual()`, `self.assertRaises()`, etc. |
| **Injeção / Setup** | Fixtures modulares escopadas (`function`, `module`, `session`) | Ciclo de vida estático `setUp()`, `tearDown()`, `setUpClass()` |
| **Parametrização** | `@pytest.mark.parametrize` (formal e declarativo) | `self.subTest()` dentro de laços |
| **Dependências** | Requer `pytest` (`pip install pytest`) | Zero dependências externas (embutido no Python) |
| **Casos de Uso** | Aplicações modernas, microserviços, ML, APIs, mutação | Scripts leves, bibliotecas puras sem dependências externas |

---

## ⚡ 2. Pytest: Padrões Avançados de Engenharia

### 2.1 Parametrização Formal de BVA e Tabelas de Decisão
```python
import pytest
from my_app.services import validate_withdrawal

# Domínio válido de saque: [10.0, 5000.0]
@pytest.mark.parametrize("amount, balance, is_blocked, expected_status, raises_exc", [
    # BVA: Limites da variável amount
    (9.99, 1000.0, False, None, True),          # min- (Inválido robusto)
    (10.0, 1000.0, False, "APPROVED", False),    # min
    (10.01, 1000.0, False, "APPROVED", False),   # min+
    (500.0, 1000.0, False, "APPROVED", False),   # nom
    (4999.99, 6000.0, False, "APPROVED", False), # max-
    (5000.0, 6000.0, False, "APPROVED", False),  # max
    (5000.01, 6000.0, False, None, True),        # max+ (Inválido robusto)
    # Tabela de Decisão: Condições de Saldo e Bloqueio
    (100.0, 50.0, False, "INSUFFICIENT_FUNDS", False),
    (100.0, 1000.0, True, "CARD_BLOCKED", False),
])
def test_withdrawal_bva_and_decision_rules(amount, balance, is_blocked, expected_status, raises_exc):
    if raises_exc:
        with pytest.raises(ValueError):
            validate_withdrawal(amount=amount, balance=balance, is_blocked=is_blocked)
    else:
        status = validate_withdrawal(amount=amount, balance=balance, is_blocked=is_blocked)
        assert status == expected_status
```

### 2.2 Property-Based Testing com `hypothesis`
```python
from hypothesis import given, strategies as st
from my_app.algorithms import sort_items, compress, decompress

@given(st.lists(st.integers()))
def test_sort_invariants(lst):
    result = sort_items(lst)
    assert len(result) == len(lst)
    assert all(result[i] <= result[i+1] for i in range(len(result)-1))

@given(st.binary())
def test_compress_roundtrip(data):
    assert decompress(compress(data)) == data
```

---

## 🏛️ 3. Unittest: Padrões Orientados a Objetos e Sem Dependências

### 3.1 Estrutura de TestCase e SubTests
```python
import unittest
from my_app.services import UserRegistry, validate_discount

class TestUserRegistry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared_resource = {"environment": "test"}

    def setUp(self):
        self.registry = UserRegistry()
        self.registry.clear()

    def tearDown(self):
        self.registry.clear()

    def test_register_user(self):
        user = self.registry.register("alice@example.com", "Alice")
        self.assertEqual(user.email, "alice@example.com")
        self.assertTrue(self.registry.exists("alice@example.com"))

    def test_discount_scenarios_subtest(self):
        test_cases = [
            ("VIP", 100.0, 80.0),
            ("REGULAR", 100.0, 95.0),
            ("ANONYMOUS", 100.0, 100.0),
        ]
        for role, price, expected in test_cases:
            with self.subTest(role=role, price=price):
                result = validate_discount(role, price)
                self.assertAlmostEqual(result, expected, places=2)
```

---

## 🎭 4. Mocks, Spies e Isolamento de Efeitos Colaterais

### 4.1 Uso de `unittest.mock` (`@patch` e `MagicMock`)
```python
from unittest.mock import patch, MagicMock
import pytest
from my_app.gateways import PaymentProcessor

def test_payment_with_patch(mocker):
    # Usando pytest-mock ou unittest.mock nativo
    with patch("my_app.gateways.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "PAID", "tx_id": "tx-123"}
        
        processor = PaymentProcessor()
        tx = processor.charge(amount=150.0, token="card_tok_abc")
        
        mock_post.assert_called_once()
        assert tx.status == "PAID"
        assert tx.id == "tx-123"
```

---

## 🧬 5. Testes de Mutação (mutmut) e Cobertura (pytest-cov)

- **Medição de Escore de Mutação**:
  $$MS = \frac{\text{Mutantes Mortos (Killed)}}{\text{Total de Mutantes Gerados}} \times 100\%$$
- **Comandos de Execução**:
  ```bash
  # Cobertura com branch coverage
  pytest --cov=my_app --cov-branch --cov-report=html --cov-fail-under=90

  # Teste de mutação
  mutmut run --paths-to-mutate my_app/
  mutmut results
  ```
