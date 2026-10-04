---
name: Aerodrome Voter
description: This skill should be used when the user asks about "Voter", "vote", "voting", "gauge creation", "emissions distribution", "bribes", "whitelistToken", or needs to understand Aerodrome's voting mechanics.
version: 0.1.0
---

# Aerodrome Voter

The Voter contract manages votes, emission distribution, and gauge creation in the Aerodrome ecosystem. It's the core coordinator between veNFTs, pools, and gauges.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                       VOTER                                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐   │
│  │   veNFT     │─────►│   Voter     │─────►│   Gauge     │   │
│  │   Holder    │      │             │      │             │   │
│  └─────────────┘      └──────┬──────┘      └─────────────┘   │
│        │                     │                    │          │
│        ▼                     ▼                    ▼          │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐   │
│  │   Vote for  │      │  Distribute │      │   LP        │   │
│  │   Pools     │      │  Emissions  │      │   Stakers   │   │
│  └─────────────┘      └─────────────┘      └─────────────┘   │
│        │                                                     │
│        ▼                                                     │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Earn: Pool Fees + External Bribes                      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Epoch Timing

```solidity
library ProtocolTimeLibrary {
    uint256 internal constant WEEK = 7 days;

    /// @notice Get epoch start (Thursday 00:00 UTC)
    function epochStart(uint256 timestamp) internal pure returns (uint256) {
        return (timestamp / WEEK) * WEEK;
    }

    /// @notice Get next epoch start
    function epochNext(uint256 timestamp) internal pure returns (uint256) {
        return epochStart(timestamp) + WEEK;
    }

    /// @notice Get vote window start (1 hour after epoch start)
    function epochVoteStart(uint256 timestamp) internal pure returns (uint256) {
        return epochStart(timestamp) + 1 hours;
    }

    /// @notice Get vote window end (1 hour before epoch end)
    function epochVoteEnd(uint256 timestamp) internal pure returns (uint256) {
        return epochNext(timestamp) - 1 hours;
    }
}
```

## Voting

### Cast Votes

```solidity
/// @notice Vote for pools with a veNFT
/// @param _tokenId veNFT to vote with
/// @param _poolVote Pools to vote for
/// @param _weights Weight distribution (relative, not percentage)
function vote(
    uint256 _tokenId,
    address[] calldata _poolVote,
    uint256[] calldata _weights
) external onlyNewEpoch(_tokenId) nonReentrant {
    address _sender = _msgSender();
    if (!IVotingEscrow(ve).isApprovedOrOwner(_sender, _tokenId)) revert NotApprovedOrOwner();
    if (_poolVote.length != _weights.length) revert UnequalLengths();
    if (_poolVote.length > maxVotingNum) revert TooManyPools();
    if (IVotingEscrow(ve).deactivated(_tokenId)) revert InactiveManagedNFT();

    uint256 _timestamp = block.timestamp;
    // Only whitelisted NFTs can vote in the last hour
    if ((_timestamp > ProtocolTimeLibrary.epochVoteEnd(_timestamp)) && !isWhitelistedNFT[_tokenId])
        revert NotWhitelistedNFT();

    lastVoted[_tokenId] = _timestamp;
    uint256 _weight = IVotingEscrow(ve).balanceOfNFT(_tokenId);
    _vote(_tokenId, _weight, _poolVote, _weights);
}

function _vote(
    uint256 _tokenId,
    uint256 _weight,
    address[] memory _poolVote,
    uint256[] memory _weights
) internal {
    _reset(_tokenId);  // Clear previous votes

    uint256 _poolCnt = _poolVote.length;
    uint256 _totalVoteWeight = 0;
    uint256 _totalWeight = 0;
    uint256 _usedWeight = 0;

    // Sum all weights for normalization
    for (uint256 i = 0; i < _poolCnt; i++) {
        _totalVoteWeight += _weights[i];
    }

    // Distribute votes
    for (uint256 i = 0; i < _poolCnt; i++) {
        address _pool = _poolVote[i];
        address _gauge = gauges[_pool];
        if (_gauge == address(0)) revert GaugeDoesNotExist(_pool);
        if (!isAlive[_gauge]) revert GaugeNotAlive(_gauge);

        if (isGauge[_gauge]) {
            // Calculate proportional weight
            uint256 _poolWeight = (_weights[i] * _weight) / _totalVoteWeight;
            if (votes[_tokenId][_pool] != 0) revert NonZeroVotes();
            if (_poolWeight == 0) revert ZeroBalance();

            _updateFor(_gauge);

            poolVote[_tokenId].push(_pool);
            weights[_pool] += _poolWeight;
            votes[_tokenId][_pool] += _poolWeight;

            // Deposit voting power in reward contracts
            IReward(gaugeToFees[_gauge])._deposit(_poolWeight, _tokenId);
            IReward(gaugeToBribe[_gauge])._deposit(_poolWeight, _tokenId);

            _usedWeight += _poolWeight;
            _totalWeight += _poolWeight;

            emit Voted(_msgSender(), _pool, _tokenId, _poolWeight, weights[_pool], block.timestamp);
        }
    }

    if (_usedWeight > 0) IVotingEscrow(ve).voting(_tokenId, true);
    totalWeight += _totalWeight;
    usedWeights[_tokenId] = _usedWeight;
}
```

### Reset Votes

```solidity
/// @notice Reset votes for a tokenId
function reset(uint256 _tokenId) external onlyNewEpoch(_tokenId) nonReentrant {
    if (!IVotingEscrow(ve).isApprovedOrOwner(msg.sender, _tokenId)) revert NotApprovedOrOwner();
    _reset(_tokenId);
}

function _reset(uint256 _tokenId) internal {
    address[] storage _poolVote = poolVote[_tokenId];
    uint256 _poolVoteCnt = _poolVote.length;
    uint256 _totalWeight = 0;

    for (uint256 i = 0; i < _poolVoteCnt; i++) {
        address _pool = _poolVote[i];
        uint256 _votes = votes[_tokenId][_pool];

        if (_votes != 0) {
            _updateFor(gauges[_pool]);
            weights[_pool] -= _votes;
            delete votes[_tokenId][_pool];

            // Withdraw from reward contracts
            IReward(gaugeToFees[gauges[_pool]])._withdraw(_votes, _tokenId);
            IReward(gaugeToBribe[gauges[_pool]])._withdraw(_votes, _tokenId);

            _totalWeight += _votes;
            emit Abstained(_msgSender(), _pool, _tokenId, _votes, weights[_pool], block.timestamp);
        }
    }

    IVotingEscrow(ve).voting(_tokenId, false);
    totalWeight -= _totalWeight;
    usedWeights[_tokenId] = 0;
    delete poolVote[_tokenId];
}
```

### Poke (Update Voting Power)

```solidity
/// @notice Update voting power for a tokenId
function poke(uint256 _tokenId) external nonReentrant {
    if (block.timestamp <= ProtocolTimeLibrary.epochVoteStart(block.timestamp))
        revert DistributeWindow();

    uint256 _weight = IVotingEscrow(ve).balanceOfNFT(_tokenId);
    _poke(_tokenId, _weight);
}

function _poke(uint256 _tokenId, uint256 _weight) internal {
    address[] memory _poolVote = poolVote[_tokenId];
    uint256 _poolCnt = _poolVote.length;
    uint256[] memory _weights = new uint256[](_poolCnt);

    for (uint256 i = 0; i < _poolCnt; i++) {
        _weights[i] = votes[_tokenId][_poolVote[i]];
    }
    _vote(_tokenId, _weight, _poolVote, _weights);
}
```

## Gauge Creation

```solidity
/// @notice Create a gauge for a pool
function createGauge(address _poolFactory, address _pool)
    external nonReentrant returns (address)
{
    address sender = _msgSender();
    if (!IFactoryRegistry(factoryRegistry).isPoolFactoryApproved(_poolFactory))
        revert FactoryPathNotApproved();
    if (gauges[_pool] != address(0)) revert GaugeExists();

    (address votingRewardsFactory, address gaugeFactory) =
        IFactoryRegistry(factoryRegistry).factoriesToPoolFactory(_poolFactory);

    address[] memory rewards = new address[](2);
    bool isPool = IPoolFactory(_poolFactory).isPool(_pool);

    if (isPool) {
        address token0 = IPool(_pool).token0();
        address token1 = IPool(_pool).token1();
        rewards[0] = token0;
        rewards[1] = token1;
    }

    // Non-governors can only create gauges for whitelisted token pools
    if (sender != governor) {
        if (!isPool) revert NotAPool();
        if (!isWhitelistedToken[rewards[0]] || !isWhitelistedToken[rewards[1]])
            revert NotWhitelistedToken();
    }

    // Create reward contracts
    (address _feeVotingReward, address _bribeVotingReward) =
        IVotingRewardsFactory(votingRewardsFactory).createRewards(forwarder, rewards);

    // Create gauge
    address _gauge = IGaugeFactory(gaugeFactory).createGauge(
        forwarder,
        _pool,
        _feeVotingReward,
        rewardToken,
        isPool
    );

    // Register gauge
    gaugeToFees[_gauge] = _feeVotingReward;
    gaugeToBribe[_gauge] = _bribeVotingReward;
    gauges[_pool] = _gauge;
    poolForGauge[_gauge] = _pool;
    isGauge[_gauge] = true;
    isAlive[_gauge] = true;
    _updateFor(_gauge);
    pools.push(_pool);

    emit GaugeCreated(
        _poolFactory, votingRewardsFactory, gaugeFactory,
        _pool, _bribeVotingReward, _feeVotingReward, _gauge, sender
    );
    return _gauge;
}
```

## Emission Distribution

### Notify Rewards from Minter

```solidity
/// @notice Receive emission from Minter
function notifyRewardAmount(uint256 _amount) external {
    address sender = _msgSender();
    if (sender != minter) revert NotMinter();

    IERC20(rewardToken).safeTransferFrom(sender, address(this), _amount);

    // Calculate share per vote weight
    uint256 _ratio = (_amount * 1e18) / Math.max(totalWeight, 1);
    if (_ratio > 0) {
        index += _ratio;
    }

    emit NotifyReward(sender, rewardToken, _amount);
}
```

### Distribute to Gauges

```solidity
/// @notice Distribute emissions to gauges
function distribute(address[] memory _gauges) external nonReentrant {
    IMinter(minter).updatePeriod();
    uint256 _length = _gauges.length;
    for (uint256 x = 0; x < _length; x++) {
        _distribute(_gauges[x]);
    }
}

function _distribute(address _gauge) internal {
    _updateFor(_gauge);

    uint256 _claimable = claimable[_gauge];
    if (_claimable > IGauge(_gauge).left() && _claimable > DURATION) {
        claimable[_gauge] = 0;
        IERC20(rewardToken).safeApprove(_gauge, _claimable);
        IGauge(_gauge).notifyRewardAmount(_claimable);
        IERC20(rewardToken).safeApprove(_gauge, 0);

        emit DistributeReward(_msgSender(), _gauge, _claimable);
    }
}

function _updateFor(address _gauge) internal {
    address _pool = poolForGauge[_gauge];
    uint256 _supplied = weights[_pool];

    if (_supplied > 0) {
        uint256 _supplyIndex = supplyIndex[_gauge];
        uint256 _index = index;
        supplyIndex[_gauge] = _index;
        uint256 _delta = _index - _supplyIndex;

        if (_delta > 0) {
            uint256 _share = (_supplied * _delta) / 1e18;
            if (isAlive[_gauge]) {
                claimable[_gauge] += _share;
            } else {
                // Return rewards to Minter if gauge is killed
                IERC20(rewardToken).safeTransfer(minter, _share);
            }
        }
    } else {
        supplyIndex[_gauge] = index;
    }
}
```

## Claiming Rewards

```solidity
/// @notice Claim AERO rewards from gauges
function claimRewards(address[] memory _gauges) external {
    uint256 _length = _gauges.length;
    for (uint256 i = 0; i < _length; i++) {
        IGauge(_gauges[i]).getReward(_msgSender());
    }
}

/// @notice Claim bribe rewards
function claimBribes(address[] memory _bribes, address[][] memory _tokens, uint256 _tokenId) external {
    if (!IVotingEscrow(ve).isApprovedOrOwner(_msgSender(), _tokenId)) revert NotApprovedOrOwner();
    uint256 _length = _bribes.length;
    for (uint256 i = 0; i < _length; i++) {
        IReward(_bribes[i]).getReward(_tokenId, _tokens[i]);
    }
}

/// @notice Claim fee rewards
function claimFees(address[] memory _fees, address[][] memory _tokens, uint256 _tokenId) external {
    if (!IVotingEscrow(ve).isApprovedOrOwner(_msgSender(), _tokenId)) revert NotApprovedOrOwner();
    uint256 _length = _fees.length;
    for (uint256 i = 0; i < _length; i++) {
        IReward(_fees[i]).getReward(_tokenId, _tokens[i]);
    }
}
```

## Managed NFT Support

```solidity
/// @notice Deposit a normal NFT into a managed NFT
function depositManaged(uint256 _tokenId, uint256 _mTokenId)
    external nonReentrant onlyNewEpoch(_tokenId)
{
    address _sender = _msgSender();
    if (!IVotingEscrow(ve).isApprovedOrOwner(_sender, _tokenId)) revert NotApprovedOrOwner();
    if (IVotingEscrow(ve).deactivated(_mTokenId)) revert InactiveManagedNFT();

    uint256 _timestamp = block.timestamp;
    if (_timestamp > ProtocolTimeLibrary.epochVoteEnd(_timestamp)) revert SpecialVotingWindow();

    lastVoted[_tokenId] = _timestamp;
    IVotingEscrow(ve).depositManaged(_tokenId, _mTokenId);

    // Update managed NFT votes
    uint256 _weight = IVotingEscrow(ve).balanceOfNFTAt(_mTokenId, block.timestamp);
    _poke(_mTokenId, _weight);
}

/// @notice Withdraw from a managed NFT
function withdrawManaged(uint256 _tokenId) external nonReentrant onlyNewEpoch(_tokenId) {
    if (!IVotingEscrow(ve).isApprovedOrOwner(_msgSender(), _tokenId)) revert NotApprovedOrOwner();

    uint256 _mTokenId = IVotingEscrow(ve).idToManaged(_tokenId);
    IVotingEscrow(ve).withdrawManaged(_tokenId);

    // Update or reset managed NFT votes
    uint256 _weight = IVotingEscrow(ve).balanceOfNFTAt(_mTokenId, block.timestamp);
    if (_weight == 0) {
        _reset(_mTokenId);
        delete lastVoted[_mTokenId];
    } else {
        _poke(_mTokenId, _weight);
    }
}
```

## Gauge Management

```solidity
/// @notice Kill a gauge (stop emissions)
function killGauge(address _gauge) external {
    if (_msgSender() != emergencyCouncil) revert NotEmergencyCouncil();
    if (!isAlive[_gauge]) revert GaugeAlreadyKilled();

    // Return pending emissions to Minter
    uint256 _claimable = claimable[_gauge];
    if (_claimable > 0) {
        IERC20(rewardToken).safeTransfer(minter, _claimable);
        delete claimable[_gauge];
    }

    isAlive[_gauge] = false;
    emit GaugeKilled(_gauge);
}

/// @notice Revive a killed gauge
function reviveGauge(address _gauge) external {
    if (_msgSender() != emergencyCouncil) revert NotEmergencyCouncil();
    if (isAlive[_gauge]) revert GaugeAlreadyRevived();

    isAlive[_gauge] = true;
    emit GaugeRevived(_gauge);
}
```

## Whitelisting

```solidity
/// @notice Whitelist a token for gauge creation
function whitelistToken(address _token, bool _bool) external {
    if (_msgSender() != governor) revert NotGovernor();
    isWhitelistedToken[_token] = _bool;
    emit WhitelistToken(_msgSender(), _token, _bool);
}

/// @notice Whitelist an NFT for special voting window
function whitelistNFT(uint256 _tokenId, bool _bool) external {
    if (_msgSender() != governor) revert NotGovernor();
    isWhitelistedNFT[_tokenId] = _bool;
    emit WhitelistNFT(_msgSender(), _tokenId, _bool);
}
```

## Key State Variables

```solidity
mapping(address => address) public gauges;         // pool => gauge
mapping(address => address) public poolForGauge;   // gauge => pool
mapping(address => address) public gaugeToFees;    // gauge => FeesVotingReward
mapping(address => address) public gaugeToBribe;   // gauge => BribeVotingReward
mapping(address => uint256) public weights;        // pool => total vote weight
mapping(uint256 => mapping(address => uint256)) public votes;  // tokenId => pool => votes
mapping(uint256 => uint256) public usedWeights;    // tokenId => used weight
mapping(uint256 => uint256) public lastVoted;      // tokenId => last vote timestamp
mapping(address => bool) public isGauge;           // is registered gauge
mapping(address => bool) public isAlive;           // is gauge active
mapping(address => uint256) public claimable;      // gauge => pending emissions
```

## Reference Files

- `contracts/Voter.sol` - Main voter implementation
- `contracts/interfaces/IVoter.sol` - Voter interface
- `contracts/libraries/ProtocolTimeLibrary.sol` - Epoch timing
