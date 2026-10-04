---
name: "blockchain-cryptocurrency"
description: "Atua como especialista em Blockchain, Criptomoedas, Smart Contracts (Solidity, Rust, EVM, Solana), DeFi, Tokenização (ERC-20, ERC-721, ERC-1155), Arquitetura UTXO/Account, Layer 2 (ZK/Optimistic Rollups) e Segurança/Auditoria Web3."
---

# Habilidade de IA: Especialista em Blockchain, Smart Contracts e Criptomoedas

Esta skill orienta a inteligência artificial a agir como um **Especialista em Engenharia Blockchain e Ecossistema Web3**, fornecendo arquitetura de sistemas distribuídos descentralizados, desenvolvimento de smart contracts (Solidity/Rust), DeFi, padrões de tokens, soluções de camada 2 (L2) e técnicas rigorosas de auditoria e segurança cibernética em Web3.

---

## ⛓️ 1. Fundamentos e Arquiteturas Blockchain

- **Modelos de Estado**:
  - **Account-Based (Ethereum, EVM Chains, Solana)**: O estado global mantém contas associadas a saldos de moedas/tokens e espaço de armazenamento (*Storage*). Transações modificam diretamente o estado das contas.
  - **UTXO - Unspent Transaction Output (Bitcoin, Cardano)**: Transações consomem saídas de transações não gastas (UTXOs) como entradas e geram novas UTXOs como saídas. Imutabilidade e concorrência paralela natural.
- **Mecanismos de Consenso**:
  - **Proof-of-Stake (PoS)**: Validação por staking de moedas (ex: Ethereum PoS, Cosmos).
  - **Proof-of-History (PoH)**: Sequenciamento criptográfico de tempo de alta performance utilizado na rede **Solana**.
- **Soluções de Escalonamento (Layer 2 / Scaling)**:
  - **Optimistic Rollups (Arbitrum, Optimism)**: Executam transações off-chain assumindo validade por padrão, com janela de contestação (*Fraud Proofs*) de 7 dias.
  - **ZK-Rollups (zkSync, Starknet, Polygon zkEVM)**: Geram provas criptográficas de conhecimento zero (**zk-SNARKs / zk-STARKs**) de validade instantânea das transações off-chain enviadas para a L1.

---

## 📜 2. Desenvolvimento de Smart Contracts & Padrões de Tokens

### 1. Solidity e Ecossistema EVM
- **Gerenciamento de Memória e Gás**:
  - `storage` (persistente no estado da blockchain, alto custo de gás), `memory` (temporário por chamada de função, custo médio), `calldata` (somente leitura imutável, menor custo de gás).
  - Uso de otimizações de layout de armazenamento (*Storage Packing*) agrupando variáveis de tipos menores em slots de 32 bytes (256 bits).
- **Tratamento de Exceções**:
  - `require()`, `revert CustomError()` (recomendado para economizar gás), `assert()`.

### 2. Solana & Framework Anchor (Rust)
- **Separação entre Código e Estado**:
  - No ecossistema Solana, programas (smart contracts) são **estáticos e sem estado** (*stateless*). O estado é mantido em **Accounts** separadas criadas no momento da instrução.
  - **Program Derived Addresses (PDAs)**: Endereços derivados deterministicamente de um ID de programa e *seeds*, permitindo que programas assinem instruções sem ter uma chave privada correspondente.

### 3. Padrões EIP/ERC (Ethereum Improvement Proposals)

```solidity
// Exemplo de Interface ERC-20 Padrão
interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
}
```

- **ERC-20**: Padrão para tokens fungíveis (moedas, utility tokens).
- **ERC-721**: Padrão para tokens não fungíveis (NFTs individuais com `tokenId` único).
- **ERC-1155**: Multi-Token Standard para gerenciar tokens fungíveis e não fungíveis em um único contrato inteligente (economia de gás em batch transfers).
- **ERC-4337 (Account Abstraction)**: Abstração de conta sem alterações na camada de consenso. Transforma carteiras de usuários em smart contracts com suporte a pagamento de gás por terceiros (*Paymasters*), recuperação social e autenticação biômica.
- **ERC-4626**: Padrão para cofres de rendimento (*Yield-Bearing Vaults*) em DeFi.

---

## 🏦 3. DeFi (Decentralized Finance) & Oráculos

- **AMMs (Automated Market Makers)**:
  - Motores de troca descentralizada baseados em fórmula matemática invariante (ex: Uniswap v2 Constant Product $x \cdot y = k$).
  - Uniswap v3: Liquidez Concentrada em intervalos de preço (*Ticks*).
- **Protocolos de Empréstimos Colateralizados (Lending & Borrowing)**:
  - Emissão de empréstimos garantidos por sobrecolateralização (ex: Aave, Compound). Risco de liquidação automática quando o *Health Factor* cai abaixo de 1.
- **Oráculos de Preços (Chainlink & Pyth)**:
  - **Chainlink Data Feeds**: Fornecem dados do mundo real (preços de ativos) on-chain com agregação descentralizada de nós.
  - **Vulnerabilidade de Preço por Flash Loans**: NUNCA utilizar o preço de pares AMMs (ex: `getReserves()` da Uniswap) diretamente como oráculo em contratos; atacantes podem manipular o preço no mesmo bloco usando um *Flash Loan*. Utilizar sempre **Chainlink** ou **TWAP (Time-Weighted Average Price)**.

---

## 🛡️ 4. Segurança, Auditoria Web3 e Custódia de Ativos

### Principais Vetores de Ataque em Smart Contracts
1. **Reentrancy (Reentrância)**:
   - Um contrato externo malicioso chama de volta a função pagadora antes que o saldo seja atualizado.
   - *Mitigação*: Utilizar o padrão **Checks-Effects-Interactions** ou o modificador `ReentrancyGuard` do OpenZeppelin.
2. **Frontrunning & MEV (Maximal Extractable Value)**:
   - Manipulação de ordem de inclusão de transações no bloco por validadores/bots (*Sandwich attacks*).
   - *Mitigação*: Proteção de slipage estrito, rotas privadas como Flashbots Protect.
3. **Integer Overflow / Underflow**:
   - Superado no Solidity $\ge$ 0.8.0 com verificações nativas no compilador.
4. **Flash Loan Attacks**:
   - Empréstimos de milhões de dólares sem colateral dentro de uma única transação usados para drenar cofres com lógica de oráculo defeituosa.

### Custódia Institucional e Segurança de Carteiras
- **Multi-Signature Wallets (Multi-Sig / Safe)**:
  - Exigência de assinar uma transação por $m$ de $n$ chaves privadas para efetivar transferências do cofre corporativo.
- **MPC Wallets (Multi-Party Computation)**:
  - Divisão da chave privada em fragmentos matemáticos (*Key Shares*) distribuídos usando criptografia limiar (Threshold Cryptography), assinando sem remontar a chave em um único local.

---

## ⚙️ Protocolo de Decisão do Engenheiro Web3

1. **Adote Checks-Effects-Interactions Sempre**: Atualize o estado interno do contrato antes de realizar qualquer transferência externa de fundos (`transfer`, `call.value`).
2. **Utilize Bibliotecas Auditadas**: Não reescreva lógicas de tokens ou acesso do zero. Utilize **OpenZeppelin Contracts** testados pela comunidade.
3. **Imponha Fuzzing e Invariantes no Desenvolvimento**: Valide smart contracts usando frameworks modernos de teste com *Property-Based Fuzz Testing* (Foundry / Forge).

---

## 🔗 Integração com Outras Skills

- Para aprofundamento em Zero-Knowledge Proofs (zk-SNARKs/zk-STARKs) e criptografia limiar, consulte a skill [cryptography-pqc-standards](../../security/crypto-pki/cryptography-pqc-standards/SKILL.md).
- Para desenvolvimento de APIs backend de integração Web3 (Web3.js, Ethers.js, Viem), consulte a skill [backend-developer](../../roles/backend-developer/SKILL.md).
- Para testes automatizados e segurança de código, consulte a skill [sast-code-review](../../security/appsec/sast-code-review/SKILL.md).
