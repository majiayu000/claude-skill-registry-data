---
name: Euler Periphery
description: This skill should be used when the user asks about "Perspective", "vault validation", "Lens", "Swapper", "SwapVerifier", "IRM Factory", "Governor", "Snapshot", or needs to understand Euler's peripheral infrastructure.
version: 0.1.0
---

# Euler Periphery Infrastructure

The EVK Periphery provides supporting infrastructure for Euler vaults: Perspectives for vault validation, Lens for read operations, Swaps for debt/collateral swaps, and factory contracts.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                   EVK PERIPHERY                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Perspectives (Vault Validation):                            │
│  ├── EulerDefaultPerspective - Standard safety checks        │
│  ├── EulerClusterPerspective - Cluster vault validation      │
│  └── Custom perspectives for specific use cases              │
│                                                              │
│  Lens Contracts (Read Operations):                           │
│  ├── VaultLens - Vault state queries                         │
│  ├── AccountLens - Account position queries                  │
│  ├── OracleLens - Price queries                              │
│  └── IRMLens - Interest rate queries                         │
│                                                              │
│  Swaps:                                                      │
│  ├── Swapper - Execute swaps via aggregators                 │
│  └── SwapVerifier - Verify swap results                      │
│                                                              │
│  Factory/Registry:                                           │
│  ├── IRMFactory - Deploy interest rate models                │
│  ├── SnapshotRegistry - Track vault snapshots                │
│  └── GenericFactory - Deploy new vaults                      │
│                                                              │
│  Governance:                                                 │
│  ├── GovernorAccessControl - Role-based access               │
│  └── TimelockController - Delayed execution                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Perspectives

Perspectives validate vaults meet specific criteria before use.

```solidity
// evk-periphery/src/Perspectives/EulerPerspective.sol

interface IPerspective {
    /// @notice Check if vault is valid from this perspective
    /// @param vault Vault to verify
    /// @return True if vault meets criteria
    function perspectiveVerify(address vault, bool failEarly) external returns (bool);

    /// @notice Check if vault has been verified
    function isVerified(address vault) external view returns (bool);

    /// @notice Get verification details
    function verifiedVaults(address vault) external view returns (VerifiedVault memory);
}

contract EulerDefaultPerspective is IPerspective {
    // Registry of approved vaults
    mapping(address => VerifiedVault) public verifiedVaults;

    struct VerifiedVault {
        bool verified;
        uint48 verifiedAt;
        address verifiedBy;
    }

    /// @notice Verify vault meets default safety criteria
    function perspectiveVerify(address vault, bool failEarly) external returns (bool) {
        // Check factory - must be deployed by recognized factory
        if (!isRecognizedFactory(IEVault(vault).factory())) {
            if (failEarly) revert UnrecognizedFactory();
            return false;
        }

        // Check oracle - must be configured
        if (IEVault(vault).oracle() == address(0)) {
            if (failEarly) revert NoOracle();
            return false;
        }

        // Check IRM - must be set
        if (IEVault(vault).interestRateModel() == address(0)) {
            if (failEarly) revert NoIRM();
            return false;
        }

        // Check governor - must be valid governance
        if (!isValidGovernor(IEVault(vault).governorAdmin())) {
            if (failEarly) revert InvalidGovernor();
            return false;
        }

        // Check unit of account - must be supported
        address unitOfAccount = IEVault(vault).unitOfAccount();
        if (!isSupportedUnitOfAccount(unitOfAccount)) {
            if (failEarly) revert UnsupportedUnitOfAccount();
            return false;
        }

        // Mark as verified
        verifiedVaults[vault] = VerifiedVault({
            verified: true,
            verifiedAt: uint48(block.timestamp),
            verifiedBy: msg.sender
        });

        emit VaultVerified(vault, msg.sender);
        return true;
    }
}
```

## Cluster Perspective

```solidity
// Validates vaults within a cluster (related vaults)

contract EulerClusterPerspective is IPerspective {
    // Cluster configuration
    mapping(bytes32 clusterId => ClusterConfig) public clusters;

    struct ClusterConfig {
        address[] vaults;
        address governor;
        bool locked;
    }

    /// @notice Verify vault is in valid cluster configuration
    function perspectiveVerify(address vault, bool failEarly) external returns (bool) {
        bytes32 clusterId = getClusterForVault(vault);

        if (clusterId == bytes32(0)) {
            if (failEarly) revert NotInCluster();
            return false;
        }

        ClusterConfig memory config = clusters[clusterId];

        // All vaults in cluster must share same governor
        for (uint i = 0; i < config.vaults.length; i++) {
            if (IEVault(config.vaults[i]).governorAdmin() != config.governor) {
                if (failEarly) revert InconsistentGovernor();
                return false;
            }
        }

        // Cross-check LTV configurations
        // Vaults can only accept each other as collateral with proper LTVs

        return true;
    }
}
```

## Vault Lens

```solidity
// evk-periphery/src/Lens/VaultLens.sol

contract VaultLens {
    /// @notice Get comprehensive vault state
    function getVaultInfo(address vault) external view returns (VaultInfo memory) {
        IEVault v = IEVault(vault);

        return VaultInfo({
            asset: v.asset(),
            name: v.name(),
            symbol: v.symbol(),
            decimals: v.decimals(),
            totalAssets: v.totalAssets(),
            totalSupply: v.totalSupply(),
            totalBorrows: v.totalBorrows(),
            cash: v.cash(),
            supplyCap: v.supplyCap(),
            borrowCap: v.borrowCap(),
            interestRateModel: v.interestRateModel(),
            oracle: v.oracle(),
            unitOfAccount: v.unitOfAccount(),
            borrowAPY: v.borrowAPY(),
            supplyAPY: v.supplyAPY(),
            utilization: calculateUtilization(v),
            governor: v.governorAdmin(),
            feeReceiver: v.feeReceiver(),
            interestFee: v.interestFee()
        });
    }

    /// @notice Get LTV configurations for all collaterals
    function getCollateralLTVs(address vault) external view returns (
        address[] memory collaterals,
        uint16[] memory borrowLTVs,
        uint16[] memory liquidationLTVs
    ) {
        // Query all configured collaterals and their LTVs
    }

    /// @notice Batch query multiple vaults
    function getVaultInfoBatch(address[] calldata vaults)
        external view
        returns (VaultInfo[] memory)
    {
        VaultInfo[] memory infos = new VaultInfo[](vaults.length);
        for (uint i = 0; i < vaults.length; i++) {
            infos[i] = getVaultInfo(vaults[i]);
        }
        return infos;
    }
}
```

## Account Lens

```solidity
// evk-periphery/src/Lens/AccountLens.sol

contract AccountLens {
    /// @notice Get account position in a vault
    function getAccountInfo(
        address vault,
        address account
    ) external view returns (AccountInfo memory) {
        IEVault v = IEVault(vault);
        IEVC evc = v.EVC();

        return AccountInfo({
            balance: v.balanceOf(account),
            balanceAssets: v.convertToAssets(v.balanceOf(account)),
            debt: v.debtOf(account),
            healthFactor: calculateHealthFactor(v, account),
            collaterals: evc.getCollaterals(account),
            controllers: evc.getControllers(account),
            isController: evc.isControllerEnabled(account, vault),
            isCollateral: evc.isCollateralEnabled(account, vault)
        });
    }

    /// @notice Calculate health factor for account
    function calculateHealthFactor(
        address vault,
        address account
    ) public view returns (uint256) {
        IEVault v = IEVault(vault);

        uint256 debt = v.debtOf(account);
        if (debt == 0) return type(uint256).max;

        uint256 debtValue = getValueInUnitOfAccount(vault, debt, v.asset());

        uint256 collateralValue = 0;
        address[] memory collaterals = v.EVC().getCollaterals(account);

        for (uint i = 0; i < collaterals.length; i++) {
            uint256 balance = IEVault(collaterals[i]).balanceOf(account);
            if (balance == 0) continue;

            uint256 assets = IEVault(collaterals[i]).convertToAssets(balance);
            uint256 value = getValueInUnitOfAccount(vault, assets, IEVault(collaterals[i]).asset());

            // Apply LTV
            (uint16 ltv,) = v.getLTV(collaterals[i]);
            collateralValue += value * ltv / 10000;
        }

        // Health = collateral / debt (scaled by 1e18)
        return collateralValue * 1e18 / debtValue;
    }

    /// @notice Get all positions for an owner (all sub-accounts)
    function getAllPositions(
        address owner,
        address[] calldata vaults
    ) external view returns (AccountInfo[][] memory) {
        AccountInfo[][] memory positions = new AccountInfo[][](256);

        for (uint8 subId = 0; subId < 256; subId++) {
            address account = getSubAccount(owner, subId);
            AccountInfo[] memory subPositions = new AccountInfo[](vaults.length);

            for (uint i = 0; i < vaults.length; i++) {
                subPositions[i] = getAccountInfo(vaults[i], account);
            }

            positions[subId] = subPositions;
        }

        return positions;
    }
}
```

## Swapper

```solidity
// evk-periphery/src/Swaps/Swapper.sol

contract Swapper {
    /// @notice Execute a swap via aggregator
    /// @param tokenIn Token to sell
    /// @param tokenOut Token to buy
    /// @param amountIn Amount to sell
    /// @param amountOutMin Minimum output
    /// @param swapData Encoded swap route (from aggregator API)
    function swap(
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 amountOutMin,
        bytes calldata swapData
    ) external returns (uint256 amountOut) {
        // Pull tokens
        IERC20(tokenIn).safeTransferFrom(msg.sender, address(this), amountIn);

        // Approve aggregator
        (address aggregator,) = abi.decode(swapData, (address, bytes));
        IERC20(tokenIn).approve(aggregator, amountIn);

        // Execute swap
        uint256 balanceBefore = IERC20(tokenOut).balanceOf(address(this));
        (bool success,) = aggregator.call(swapData);
        require(success, "Swap failed");

        amountOut = IERC20(tokenOut).balanceOf(address(this)) - balanceBefore;
        require(amountOut >= amountOutMin, "Slippage");

        // Send to caller
        IERC20(tokenOut).safeTransfer(msg.sender, amountOut);

        emit Swap(msg.sender, tokenIn, tokenOut, amountIn, amountOut);
    }
}
```

## Swap Verifier

```solidity
// evk-periphery/src/Swaps/SwapVerifier.sol

contract SwapVerifier {
    /// @notice Verify swap result matches expected using oracle
    function verifySwap(
        address oracle,
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 amountOut,
        uint256 maxSlippageBps
    ) external view returns (bool valid, uint256 slippageBps) {
        // Get oracle quote
        uint256 expectedOut = IPriceOracle(oracle).getQuote(amountIn, tokenIn, tokenOut);

        if (amountOut >= expectedOut) {
            return (true, 0);  // Better than expected
        }

        // Calculate slippage
        slippageBps = (expectedOut - amountOut) * 10000 / expectedOut;
        valid = slippageBps <= maxSlippageBps;
    }
}
```

## IRM Factory

```solidity
// evk-periphery/src/IRMFactory/IRMFactory.sol

contract IRMFactory {
    /// @notice Deploy a new kink IRM
    function deployKinkIRM(
        uint256 baseRate,
        uint256 slope1,
        uint256 slope2,
        uint256 kink
    ) external returns (address irm) {
        irm = address(new KinkIRM(baseRate, slope1, slope2, kink));
        emit IRMDeployed(irm, "kink", abi.encode(baseRate, slope1, slope2, kink));
    }

    /// @notice Deploy a linear IRM
    function deployLinearIRM(
        uint256 baseRate,
        uint256 slope
    ) external returns (address irm) {
        irm = address(new LinearIRM(baseRate, slope));
        emit IRMDeployed(irm, "linear", abi.encode(baseRate, slope));
    }

    /// @notice Get recommended IRM for asset type
    function getRecommendedIRM(
        AssetType assetType
    ) external view returns (uint256 baseRate, uint256 slope1, uint256 slope2, uint256 kink) {
        if (assetType == AssetType.Stablecoin) {
            return (0, 4e16, 100e16, 80e16);  // Low base, steep above 80%
        } else if (assetType == AssetType.Volatile) {
            return (2e16, 8e16, 200e16, 70e16);  // Higher base, steeper curve
        }
        // ...
    }
}
```

## Snapshot Registry

```solidity
// evk-periphery/src/SnapshotRegistry/SnapshotRegistry.sol

contract SnapshotRegistry {
    struct Snapshot {
        uint256 totalAssets;
        uint256 totalBorrows;
        uint256 totalSupply;
        uint256 borrowAPY;
        uint256 supplyAPY;
        uint48 timestamp;
    }

    mapping(address vault => Snapshot[]) public snapshots;

    /// @notice Take snapshot of vault state
    function takeSnapshot(address vault) external {
        IEVault v = IEVault(vault);

        snapshots[vault].push(Snapshot({
            totalAssets: v.totalAssets(),
            totalBorrows: v.totalBorrows(),
            totalSupply: v.totalSupply(),
            borrowAPY: v.borrowAPY(),
            supplyAPY: v.supplyAPY(),
            timestamp: uint48(block.timestamp)
        }));

        emit SnapshotTaken(vault, snapshots[vault].length - 1);
    }

    /// @notice Get historical snapshots
    function getSnapshots(
        address vault,
        uint256 startIndex,
        uint256 count
    ) external view returns (Snapshot[] memory) {
        // Return paginated snapshots
    }
}
```

## Governor Access Control

```solidity
// evk-periphery/src/Governor/GovernorAccessControl.sol

contract GovernorAccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN");
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR");
    bytes32 public constant GUARDIAN_ROLE = keccak256("GUARDIAN");

    mapping(bytes32 role => mapping(address => bool)) public hasRole;

    /// @notice Execute governance action with role check
    function execute(
        address target,
        bytes calldata data,
        bytes32 requiredRole
    ) external {
        require(hasRole[requiredRole][msg.sender], "Unauthorized");

        (bool success,) = target.call(data);
        require(success, "Execution failed");

        emit Executed(target, data, msg.sender);
    }

    /// @notice Grant role
    function grantRole(bytes32 role, address account) external {
        require(hasRole[ADMIN_ROLE][msg.sender], "Not admin");
        hasRole[role][account] = true;
        emit RoleGranted(role, account);
    }
}
```

## Events

```solidity
// Perspectives
event VaultVerified(address indexed vault, address indexed verifier);
event VaultRevoked(address indexed vault, address indexed revoker);

// Swapper
event Swap(address indexed sender, address tokenIn, address tokenOut, uint256 amountIn, uint256 amountOut);

// IRM Factory
event IRMDeployed(address indexed irm, string irmType, bytes params);

// Snapshot Registry
event SnapshotTaken(address indexed vault, uint256 indexed index);

// Governor
event Executed(address indexed target, bytes data, address indexed executor);
event RoleGranted(bytes32 indexed role, address indexed account);
```

## Reference Files

- `evk-periphery/src/Perspectives/` - Vault validation
- `evk-periphery/src/Lens/` - Read contracts
- `evk-periphery/src/Swaps/` - Swap infrastructure
- `evk-periphery/src/IRMFactory/` - IRM deployment
- `evk-periphery/src/SnapshotRegistry/` - Historical data
- `evk-periphery/src/Governor/` - Access control
