---
name: forge-signing
description: Sign messages with Foundry cheatcodes for testing signature verification. Use when testing EIP-712 signatures, Permit2, or any signed data verification.
---

# Foundry Signing Cheatcodes

Sign messages for testing signature verification in Solidity contracts.

## Import

```solidity
import {Vm} from "forge-std/Vm.sol";
Vm constant vm = Vm(VM_ADDRESS);
```

## sign(uint256 privateKey, bytes32 digest)

Sign a digest with a private key:

```solidity
(uint8 v, bytes32 r, bytes32 s) = vm.sign(privateKey, digest);
```

**Returns:**
- `v` - Recovery id
- `r` - First 32 bytes of signature
- `s` - Second 32 bytes of signature

## sign(Wallet memory wallet, bytes32 digest)

Using a Wallet struct:

```solidity
Wallet memory wallet = vm.createWallet("alice");
(uint8 v, bytes32 r, bytes32 s) = vm.sign(wallet, digest);
```

## Basic Example: Sign and Recover

```solidity uint256 alicePk
(address alice,) = makeAddrAndKey("alice");
bytes32 hash = keccak256("Signed by Alice");

(uint8 v, bytes32 r, bytes32 s) = vm.sign(alicePk, hash);
address signer = ecrecover(hash, v, r, s);

assertEq(alice, signer); // PASS
```

## Testing EIP-712 Signatures

```solidity
function testEIP712Signature() public {
    (address alice, uint256 alicePk) = makeAddrAndKey("alice");
    
    // Build EIP-712 domain separator
    bytes32 domainSeparator = keccak256(abi.encode(
        keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
        keccak256("MyContract"),
        keccak256("1"),
        block.chainid,
        address(this)
    ));
    
    // Build typed data hash
    bytes32 structHash = keccak256(abi.encode(
        keccak256("Message(address sender,uint256 amount)"),
        alice,
        100e18
    ));
    
    bytes32 digest = keccak256(abi.encodePacked(
        "\x19\x01",
        domainSeparator,
        structHash
    ));
    
    // Sign
    (uint8 v, bytes32 r, bytes32 s) = vm.sign(alicePk, digest);
    bytes memory signature = abi.encodePacked(r, s, v);
    
    // Verify in contract
    assertTrue(verifySignature(alice, digest, signature));
}
```

## Testing Permit2 Signatures

```solidity
function testPermit2Signature() public {
    (address alice, uint256 alicePk) = makeAddrAndKey("alice");
    
    // Build permit data (matching Permit2's expected format)
    bytes32 digest = // ... build according to Permit2 spec
    
    (uint8 v, bytes32 r, bytes32 s) = vm.sign(alicePk, digest);
    bytes memory signature = abi.encodePacked(r, s, v);
    
    // Call contract that verifies Permit2 signature
    router.swapSingleTokenExactInWithPermit(..., signature);
}
```

## Gotcha: Signature Byte Order

When encoding for OpenZeppelin's ECDSA library:

```solidity
// WRONG:
bytes memory signature = abi.encodePacked(v, r, s);

// CORRECT:
bytes memory signature = abi.encodePacked(r, s, v);
```

OpenZeppelin expects `(r, s, v)` order, not `(v, r, s)`.

## Related Cheatcodes

| Cheatcode | Purpose |
|-----------|---------|
| `vm.addr(uint256)` | Get address from private key |
| `vm.createWallet(string)` | Create Wallet struct |
| `vm.createWallet(string, uint256)` | Create wallet with specific key |
| `vm.sign(Wallet, bytes32)` | Sign with Wallet struct |
