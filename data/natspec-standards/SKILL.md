---
name: natspec-standards
description: NatSpec documentation standards and best practices for Solidity contracts. Use when documenting code or reviewing documentation quality.
---

# NatSpec Standards Skill

This skill provides standards and best practices for NatSpec (Ethereum Natural Specification) documentation in Solidity.

## When to Use

Use this skill when:
- Documenting smart contracts
- Reviewing code documentation
- Generating documentation
- Preparing for audits
- Creating public APIs

## NatSpec Overview

NatSpec is Ethereum's standard for documenting smart contracts. It generates human-readable documentation and is displayed in wallets when users interact with contracts.

**Benefits:**
- User-facing descriptions in wallets
- Developer documentation
- Automated doc generation
- Audit trail
- Function parameter explanation

## Basic Tags

### Contract-Level Tags

```solidity
/// @title Brief contract title
/// @author Author name
/// @notice Explanation visible to end users
/// @dev Technical details for developers
/// @custom:security-contact security@example.com
contract MyContract {
    // ...
}
```

### Function Tags

```solidity
/// @notice Transfers tokens to a recipient
/// @dev Uses SafeERC20 for safe transfers
/// @param to The address receiving the tokens
/// @param amount The number of tokens to transfer
/// @return success True if the transfer succeeded
function transfer(address to, uint256 amount) public returns (bool success) {
    // ...
}
```

### Event Tags

```solidity
/// @notice Emitted when tokens are transferred
/// @dev Follows ERC20 standard
/// @param from The sender address
/// @param to The recipient address
/// @param value The amount transferred
event Transfer(address indexed from, address indexed to, uint256 value);
```

### State Variable Tags

```solidity
/// @notice The total supply of tokens
/// @dev Updated on mint and burn
uint256 public totalSupply;

/// @notice Mapping of account balances
mapping(address => uint256) public balances;
```

## Complete Tag Reference

| Tag | Usage | Visibility |
|-----|-------|-----------|
| `@title` | Contract title | External |
| `@author` | Author name | External |
| `@notice` | User explanation | External |
| `@dev` | Developer notes | Developer |
| `@param` | Parameter description | External |
| `@return` | Return value description | External |
| `@inheritdoc` | Inherit documentation | - |
| `@custom:*` | Custom tags | Both |

## Documentation Patterns

### Comprehensive Contract Documentation

```solidity
/**
 * @title ERC20 Token Implementation
 * @author YourName
 * @notice This contract implements a standard ERC20 token with additional features
 * @dev Inherits from OpenZeppelin's ERC20 implementation
 * @custom:security-contact security@example.com
 */
contract MyToken is ERC20, Ownable {
    /// @notice The maximum supply of tokens that can ever exist
    /// @dev Set to 1 million tokens with 18 decimals
    uint256 public constant MAX_SUPPLY = 1_000_000 * 10**18;

    /// @notice Tracks the total amount of tokens that have been minted
    /// @dev Incremented on mint, used to enforce MAX_SUPPLY
    uint256 public totalMinted;

    /**
     * @notice Creates the token contract and mints initial supply
     * @dev Sets the token name and symbol, grants DEFAULT_ADMIN_ROLE to deployer
     * @param initialOwner The address that will own the contract
     */
    constructor(address initialOwner)
        ERC20("MyToken", "MTK")
        Ownable(initialOwner)
    {}

    /**
     * @notice Mints new tokens to a specified address
     * @dev Only callable by owner, enforces MAX_SUPPLY limit
     * @param to The address that will receive the minted tokens
     * @param amount The number of tokens to mint (in wei, e.g., 1e18 = 1 token)
     *
     * Requirements:
     * - Caller must be the owner
     * - Total minted must not exceed MAX_SUPPLY
     * - `to` cannot be the zero address
     *
     * Emits a {Transfer} event from the zero address
     */
    function mint(address to, uint256 amount) public onlyOwner {
        require(totalMinted + amount <= MAX_SUPPLY, "Exceeds max supply");
        _mint(to, amount);
        totalMinted += amount;
    }

    /**
     * @notice Returns the remaining tokens that can be minted
     * @dev Calculates MAX_SUPPLY - totalMinted
     * @return remaining The number of tokens that can still be minted
     */
    function remainingSupply() public view returns (uint256 remaining) {
        return MAX_SUPPLY - totalMinted;
    }
}
```

### Documenting Complex Functions

```solidity
/**
 * @notice Swaps exact tokens for tokens through multiple pairs
 * @dev Supports multi-hop swaps through the Uniswap V2 router
 *
 * This function swaps an exact amount of input tokens for as many output
 * tokens as possible, following the path of token pairs defined in `path`.
 * The swap will revert if the output amount is less than `amountOutMin`.
 *
 * @param amountIn The exact amount of input tokens to swap
 * @param amountOutMin The minimum amount of output tokens to receive
 * @param path An array of token addresses defining the swap path
 * @param to The address that will receive the output tokens
 * @param deadline Unix timestamp after which the transaction will revert
 *
 * @return amounts An array of amounts for each step in the swap path
 *
 * Requirements:
 * - `path.length` must be >= 2
 * - `deadline` must be in the future
 * - Contract must have approval to spend `amountIn` of `path[0]` tokens
 * - Resulting amount must be >= `amountOutMin`
 *
 * Emits:
 * - {Swap} event for each pair in the path
 * - {Transfer} events for token movements
 *
 * Example:
 * ```
 * // Swap 1 ETH for at least 2000 USDC
 * uint256 amountIn = 1 ether;
 * uint256 amountOutMin = 2000 * 10**6;
 * address[] memory path = new address[](2);
 * path[0] = WETH;
 * path[1] = USDC;
 * swapExactTokensForTokens(amountIn, amountOutMin, path, msg.sender, block.timestamp + 300);
 * ```
 */
function swapExactTokensForTokens(
    uint256 amountIn,
    uint256 amountOutMin,
    address[] calldata path,
    address to,
    uint256 deadline
) external returns (uint256[] memory amounts) {
    // Implementation
}
```

### Documenting Errors

```solidity
/**
 * @notice Thrown when a user has insufficient balance for an operation
 * @dev Used instead of require() for gas efficiency
 * @param account The address with insufficient balance
 * @param balance The actual balance of the account
 * @param needed The amount needed for the operation
 */
error InsufficientBalance(address account, uint256 balance, uint256 needed);

/**
 * @notice Thrown when an unauthorized address attempts a restricted action
 * @param caller The address that attempted the action
 * @param required The role or address required
 */
error Unauthorized(address caller, address required);
```

### Documenting Modifiers

```solidity
/**
 * @notice Ensures the function can only be called when the contract is not paused
 * @dev Reverts with "Pausable: paused" if contract is paused
 */
modifier whenNotPaused() {
    require(!paused(), "Pausable: paused");
    _;
}

/**
 * @notice Prevents reentrant calls to a function
 * @dev Uses the ReentrancyGuard pattern from OpenZeppelin
 */
modifier nonReentrant() {
    require(_status != _ENTERED, "ReentrancyGuard: reentrant call");
    _status = _ENTERED;
    _;
    _status = _NOT_ENTERED;
}
```

### Documenting Structs and Enums

```solidity
/**
 * @notice Represents a user's position in the vault
 * @dev Stored in the `positions` mapping
 * @param amount The amount of tokens deposited
 * @param shares The number of vault shares owned
 * @param lastUpdate The timestamp of the last position update
 * @param locked Whether the position is locked for withdrawals
 */
struct Position {
    uint256 amount;
    uint256 shares;
    uint256 lastUpdate;
    bool locked;
}

/**
 * @notice Possible states for a proposal
 * @dev Used in the governance system
 */
enum ProposalState {
    Pending,    /// @notice Proposal has been created but voting hasn't started
    Active,     /// @notice Voting is currently open
    Canceled,   /// @notice Proposal was canceled by the proposer
    Defeated,   /// @notice Proposal failed to reach quorum or majority
    Succeeded,  /// @notice Proposal passed and can be executed
    Executed    /// @notice Proposal has been executed
}
```

## Documentation Best Practices

### 1. Always Document Public/External Functions

```solidity
// ❌ Bad: No documentation
function transfer(address to, uint256 amount) public returns (bool) {}

// ✅ Good: Clear documentation
/**
 * @notice Transfers tokens to a recipient
 * @param to The recipient address
 * @param amount The amount to transfer
 * @return success True if transfer succeeded
 */
function transfer(address to, uint256 amount) public returns (bool success) {}
```

### 2. Explain Complex Logic

```solidity
/**
 * @notice Calculates compound interest using the formula: A = P(1 + r)^t
 * @dev Uses fixed-point arithmetic with 18 decimals
 *
 * The calculation is broken into steps to avoid overflow:
 * 1. Calculate (1 + rate) with 18 decimal precision
 * 2. Raise to the power of time periods
 * 3. Multiply by principal and adjust for decimals
 *
 * @param principal The initial amount (with 18 decimals)
 * @param rate The interest rate per period (with 18 decimals, e.g., 0.05e18 = 5%)
 * @param periods The number of compounding periods
 * @return The final amount after compound interest
 */
function calculateCompoundInterest(
    uint256 principal,
    uint256 rate,
    uint256 periods
) public pure returns (uint256) {
    // Implementation
}
```

### 3. Document Requirements and Effects

```solidity
/**
 * @notice Stakes tokens in the contract
 * @dev Transfers tokens from user and mints staking shares
 *
 * @param amount The amount of tokens to stake
 *
 * Requirements:
 * - `amount` must be greater than 0
 * - User must have approved this contract to spend `amount`
 * - User must have sufficient token balance
 * - Contract must not be paused
 *
 * Effects:
 * - Transfers `amount` tokens from user to contract
 * - Mints proportional shares to user
 * - Updates user's stake timestamp
 * - Increases total staked amount
 *
 * Emits:
 * - {Staked} event with user address and amount
 * - {Transfer} events from token transfers
 */
function stake(uint256 amount) external nonReentrant whenNotPaused {
    // Implementation
}
```

### 4. Document Security Considerations

```solidity
/**
 * @notice Withdraws all staked tokens and rewards
 * @dev Uses pull-over-push pattern to avoid reentrancy
 *
 * Security Considerations:
 * - Protected by `nonReentrant` modifier
 * - Updates state before external calls (CEI pattern)
 * - Will revert if contract has insufficient balance
 *
 * @return stakedAmount The amount of staked tokens returned
 * @return rewardAmount The amount of reward tokens claimed
 */
function withdraw() external nonReentrant returns (uint256 stakedAmount, uint256 rewardAmount) {
    // Implementation
}
```

### 5. Use Custom Tags for Additional Info

```solidity
/**
 * @title Vault Contract
 * @author YourName
 * @notice Deposit tokens to earn yield
 * @dev Implements ERC4626 tokenized vault standard
 *
 * @custom:security-contact security@example.com
 * @custom:audit Audited by Company X on 2024-01-15
 * @custom:version 1.0.0
 * @custom:license MIT
 */
contract Vault is ERC4626 {
    // ...
}
```

## Documentation Generation

### Foundry

```bash
# Generate documentation
forge doc

# Generate and serve
forge doc --serve --port 3000

# Generate for specific contract
forge doc --contract MyContract
```

### Hardhat

```bash
# Install hardhat-dodoc
npm install --save-dev @primitivefi/hardhat-dodoc

# Generate documentation
npx hardhat dodoc

# Documentation generated in docs/
```

## Inheritance Documentation

```solidity
/**
 * @title Enhanced ERC20
 * @notice ERC20 with additional features
 * @inheritdoc ERC20
 */
contract EnhancedERC20 is ERC20 {
    /**
     * @notice Mints new tokens with additional validation
     * @inheritdoc ERC20
     * @dev Adds max supply check before minting
     */
    function _mint(address account, uint256 amount) internal override {
        require(totalSupply() + amount <= MAX_SUPPLY, "Exceeds max supply");
        super._mint(account, amount);
    }
}
```

## Common Documentation Mistakes

### ❌ 1. Vague Descriptions

```solidity
/// @notice Does stuff
/// @param x some value
function doSomething(uint256 x) public {}
```

### ✅ Better:

```solidity
/**
 * @notice Updates the withdrawal fee percentage
 * @param newFee The new fee in basis points (e.g., 100 = 1%)
 */
function setFee(uint256 newFee) public {}
```

### ❌ 2. Outdated Documentation

```solidity
/// @notice Transfers tokens (function has been modified but docs haven't)
function transfer(address to, uint256 amount, bool fast) public {}
```

### ❌ 3. Missing Parameter Descriptions

```solidity
/// @notice Swaps tokens
function swap(uint256 a, uint256 b, address[] memory p) public {}
```

### ✅ Better:

```solidity
/**
 * @notice Swaps tokens through specified path
 * @param amountIn The input amount
 * @param amountOutMin The minimum acceptable output
 * @param path The swap path (array of token addresses)
 */
function swap(uint256 amountIn, uint256 amountOutMin, address[] memory path) public {}
```

## Documentation Checklist

- [ ] Every public/external function documented
- [ ] All parameters explained
- [ ] Return values described
- [ ] Requirements listed
- [ ] Effects documented
- [ ] Events documented
- [ ] Errors documented with parameters
- [ ] Complex logic explained
- [ ] Security considerations noted
- [ ] Examples provided for complex functions
- [ ] Custom tags used where appropriate
- [ ] Documentation matches implementation

## Quick Reference

### Minimal Documentation

```solidity
/// @notice Brief user-facing description
/// @param param1 Description
/// @return Description
function myFunction(uint256 param1) external returns (uint256) {}
```

### Complete Documentation

```solidity
/**
 * @notice User-facing description
 * @dev Technical details
 * @param param1 Description
 * @param param2 Description
 * @return returnValue Description
 *
 * Requirements:
 * - List requirements
 *
 * Emits:
 * - {EventName}
 */
function myFunction(uint256 param1, address param2)
    external
    returns (uint256 returnValue)
{}
```

---

**Remember:** Good documentation is essential for security audits, user trust, and long-term maintainability. Document as you code, not as an afterthought.
