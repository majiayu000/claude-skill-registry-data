---
name: metanova-nova-miner
description: This skill should be used when setting up, optimizing, or managing MetaNova NOVA miners on Bittensor Subnet 68 (SN68). Use it for miner configuration, molecular search strategy development, PSICHIC scoring optimization, GitHub submission management, entropy maximization strategies, or achieving top miner rankings in the decentralized drug discovery network.
---

# MetaNova NOVA Miner - Bittensor SN68

## Overview

NOVA (Subnet 68) is a decentralized drug discovery platform on Bittensor that rewards miners for discovering high-affinity molecules for pharmaceutical targets. Miners search massive chemical databases (1.75 billion synthesizable molecules) using AI and heuristics, submit candidate molecules via GitHub, and earn TAO emissions based on PSICHIC affinity scores validated by the network.

This skill provides comprehensive guidance for:
- Setting up and configuring NOVA miners
- Developing competitive molecular search strategies
- Optimizing for PSICHIC and Boltz2 scoring
- Maximizing entropy bonuses and avoiding penalties
- Managing GitHub submissions and monitoring performance

## When to Use This Skill

Use this skill when:
- Setting up a new NOVA SN68 miner
- Optimizing mining strategies for better rankings
- Debugging miner configuration or submission issues
- Implementing molecular search algorithms
- Understanding PSICHIC scoring and incentive mechanisms
- Deploying miners on Basilica or other GPU infrastructure
- Analyzing competitor strategies from leaderboards
- Troubleshooting GitHub API or validation errors

## Quick Start

### 1. Prerequisites

Before mining, ensure:
- **Bittensor Wallet**: Created and funded for subnet registration
- **GitHub Account**: Personal Access Token with repo permissions
- **Hardware**: CPU (minimum) or CUDA 12.6 GPU (recommended)
- **Python**: 3.12+ installed
- **TAO**: Sufficient balance for subnet 68 registration fee

### 2. Initial Setup

Run the automated setup script:

```bash
# Download and run setup
bash scripts/setup_miner.sh
```

This script:
1. Clones the NOVA repository
2. Creates `.env` configuration template
3. Installs dependencies (CPU or CUDA)
4. Verifies PSICHIC model loading
5. Provides next steps

### 3. Configuration

Edit `.env` file with your credentials:

```bash
# Network Configuration
SUBTENSOR_NETWORK="wss://entrypoint-finney.opentensor.ai:443"
DEVICE_OVERRIDE="cpu"  # or None for GPU

# GitHub Authentication
GITHUB_TOKEN="ghp_xxxxxxxxxxxxx"  # Create at github.com/settings/tokens

# Miner GitHub Repository (for submissions)
GITHUB_REPO_NAME="nova-submissions"
GITHUB_REPO_BRANCH="main"
GITHUB_REPO_OWNER="your-github-username"
GITHUB_REPO_PATH=""  # or "data/results"
```

**GitHub Token Permissions**:
- Repository access: Write (for miners)
- Scopes: `repo` (full control of private repositories)

### 4. Register on Subnet

```bash
btcli subnet register \\
    --netuid 68 \\
    --wallet.name my_wallet \\
    --wallet.hotkey my_hotkey
```

Check registration cost first:
```bash
btcli subnet list
```

### 5. Run Miner

```bash
cd nova
source .venv/bin/activate

python3 neurons/miner.py \\
    --wallet.name my_wallet \\
    --wallet.hotkey my_hotkey \\
    --netuid 68 \\
    --logging.info
```

Monitor logs for:
- ✅ Wallet and metagraph sync
- ✅ PSICHIC model loading
- ✅ Challenge parameters fetched
- ✅ Molecule submission successful

## Core Mining Workflow

### Step 1: Understand Current Challenge

Each epoch (approximately every Tempo + 1 blocks), challenges rotate:

**Key Challenge Parameters**:
- **Target Protein**: Weekly target (e.g., "O15379" - UniProt ID)
- **Antitargets**: 8 proteins to avoid (off-target penalties)
- **Valid Reaction**: May restrict to specific synthesis pathways
- **Entropy Weight**: Increases over time, rewarding chemical diversity

**Query Challenge Info**:
```python
# Miner automatically fetches from blockchain
challenge_params = get_challenge_params_from_blockhash(block_hash)

# Or check config.yaml
with open('config/config.yaml') as f:
    config = yaml.safe_load(f)
    target = config['protein_selection']['weekly_target']
    num_antitargets = config['protein_selection']['num_antitargets']
```

### Step 2: Search Strategy Selection

Choose a search strategy based on resources and expertise:

#### Strategy A: ML-Guided Search (Recommended for GPU miners)
**Best for**: Miners with GPU, ML experience
**Performance**: Excellent
**Time**: 1-2 hours per epoch

1. Sample 50K-100K molecules from SAVI-2020
2. Score with PSICHIC to create training data
3. Train surrogate model (MLP on fingerprints or GCN)
4. Screen full database with surrogate
5. Validate top 1000 with PSICHIC
6. Submit highest scorer

**Advantages**:
- Can search entire 1.75B molecule space
- Adaptive to new targets
- High success rate

**Implementation**: See `references/mining_strategies.md` section "S-Tier: ML-Guided Active Search"

#### Strategy B: Similarity-Based Search (Recommended for CPU miners)
**Best for**: Miners with limited compute
**Performance**: Good
**Time**: 30-60 minutes per epoch

1. Query ChEMBL/PubChem for known binders to target
2. Compute molecular fingerprints (ECFP4)
3. Search SAVI-2020 for similar molecules (Tanimoto > 0.7)
4. Score top 10K candidates with PSICHIC
5. Submit highest scorer

**Advantages**:
- Leverages existing knowledge
- Fast execution
- Reliable for well-studied targets

**Implementation**: See `references/mining_strategies.md` section "B-Tier: Similarity-Based Database Search"

#### Strategy C: Genetic Algorithm (For novel exploration)
**Best for**: Miners wanting to discover new molecules
**Performance**: Good
**Time**: 2-4 hours per epoch

1. Initialize population with known binders
2. Score with PSICHIC
3. Evolve via mutation and crossover
4. Run 50-100 generations
5. Submit best individual

**Advantages**:
- Explores beyond database
- Can discover novel scaffolds
- Good for entropy bonuses

**Implementation**: See `references/mining_strategies.md` section "A-Tier: Genetic Algorithm Optimization"

### Step 3: Molecular Validation

Before scoring with PSICHIC, validate molecular properties:

**Required Checks** (from `config.yaml`):
```python
def validate_molecule(mol):
    # Heavy atom count
    heavy_atoms = get_heavy_atom_count(mol)
    if heavy_atoms < 20:
        return False, "Insufficient heavy atoms"

    # Rotatable bonds
    rot_bonds = count_rotatable_bonds(mol)
    if rot_bonds < 1 or rot_bonds > 10:
        return False, "Rotatable bonds out of range"

    # Lipinski's Rule of Five (optional but recommended)
    if not passes_lipinski(mol):
        return False, "Fails drug-likeness"

    # Reaction validity (if random_valid_reaction: true)
    if not matches_valid_reaction(mol, current_reaction):
        return False, "Invalid synthesis pathway"

    return True, "Valid"
```

### Step 4: PSICHIC Scoring

Score candidates with PSICHIC affinity prediction model:

**Batch Scoring** (Efficient):
```python
from PSICHIC.wrapper import PsichicWrapper

# Initialize model
psichic = PsichicWrapper(device="cuda:0")  # or "cpu"

# Get target sequence
target_sequence = get_sequence_from_protein_code(target_uniprot_id)

# Score batch of molecules
candidates = [mol1, mol2, mol3, ...]  # SMILES strings
scores = psichic.predict_batch(
    molecules=candidates,
    protein_sequence=target_sequence,
    batch_size=128
)

# Handle antitargets
for antitarget in antitargets:
    antitarget_seq = get_sequence_from_protein_code(antitarget)
    antitarget_scores = psichic.predict_batch(candidates, antitarget_seq)

# Calculate composite score
final_scores = []
for i in range(len(candidates)):
    target_score = scores[i]
    max_antitarget = max(antitarget_scores[j][i] for j in range(len(antitargets)))
    antitarget_penalty = max_antitarget * 0.9  # antitarget_weight
    entropy_bonus = compute_maccs_entropy(candidates[i]) * entropy_weight
    final = target_score - antitarget_penalty + entropy_bonus
    final_scores.append(final)

# Select best
best_idx = np.argmax(final_scores)
best_molecule = candidates[best_idx]
```

### Step 5: Entropy Optimization

Entropy weight increases over time, rewarding chemical diversity:

**Calculate Current Entropy Weight**:
```python
from utils.scoring import calculate_dynamic_entropy

current_epoch = get_current_block() // epoch_length
start_epoch = 18703  # From config
starting_weight = 0.3
step_size = 0.007142857

entropy_weight = calculate_dynamic_entropy(
    starting_weight=starting_weight,
    step_size=step_size,
    start_epoch=start_epoch,
    current_epoch=current_epoch
)
```

**Maximize Entropy**:
```python
from utils import compute_maccs_entropy

# MACCS fingerprints capture structural diversity
entropy_score = compute_maccs_entropy(molecule_smiles)

# Adjusted composite score
composite = target_score - antitarget_penalty + (entropy_weight * entropy_score)
```

**Strategy**:
- **Early epochs** (entropy_weight < 0.5): Focus on pure affinity
- **Mid epochs** (0.5 < entropy_weight < 1.0): Balance affinity and diversity
- **Late epochs** (entropy_weight > 1.0): Prioritize unique chemical scaffolds

### Step 6: Submit to GitHub

Upload molecule to configured GitHub repository:

**Submission Format**:
```csv
SMILES
CCO
```

Single SMILES string in CSV format.

**Upload via Miner**:
```python
from utils import upload_file_to_github

# Create temporary file with SMILES
with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
    f.write("SMILES\\n")
    f.write(f"{best_molecule}\\n")
    temp_path = f.name

# Upload to GitHub
success = upload_file_to_github(
    file_path=temp_path,
    github_path=github_path,  # From .env
    commit_message=f"Submission for epoch {current_epoch}"
)

if success:
    bt.logging.info("✅ Submission successful")
else:
    bt.logging.error("❌ Submission failed")
```

**GitHub Path Format**:
```
{owner}/{repo}/{branch}/{path}
```
Maximum 100 characters total.

### Step 7: Monitor and Iterate

Track performance and adjust strategy:

**Monitor Metrics**:
- **Rank**: Position on subnet leaderboard
- **Emissions**: TAO earned per epoch
- **Validator Weights**: How validators score your submissions
- **Competition**: Top performers' strategies

**Data Sources**:
- **Taostats**: https://taostats.io/subnets/68/
- **Subnet Alpha**: https://subnetalpha.ai/subnet/nova/
- **Miner Logs**: Local validation scores

**Iterate**:
1. Analyze why top miners win (higher affinity? better entropy?)
2. Adjust search strategy (explore new chemical space)
3. Optimize computational efficiency (faster iteration)
4. Experiment with hybrid approaches

## Advanced Optimization

### Boltz2 Dual Optimization

50% of incentive goes to Boltz2 structural validation winner:

**Strategy**:
```python
# Among top PSICHIC candidates, select best for Boltz2
psichic_top_10 = select_top_k(molecules, psichic_scores, k=10)

# Boltz2 scoring (requires separate model)
from boltz.wrapper import BoltzWrapper
boltz = BoltzWrapper()

boltz_scores = []
for mol in psichic_top_10:
    score = boltz.predict(
        molecule=mol,
        protein_sequence=target_sequence,
        metric="affinity_probability_binary"
    )
    boltz_scores.append(score)

# Select molecule that ranks well in both
combined_rank = rank_psichic + rank_boltz
best = psichic_top_10[np.argmin(combined_rank)]
```

### Antitarget Selectivity Filtering

Pre-filter by selectivity ratio before expensive scoring:

```python
def selectivity_ratio(mol, target, antitargets):
    target_score = psichic.predict(mol, target)
    antitarget_scores = [psichic.predict(mol, at) for at in antitargets]
    max_antitarget = max(antitarget_scores)

    # Selectivity: target_affinity / max_antitarget_affinity
    return target_score / (max_antitarget + 1e-8)

# Filter candidates
filtered = [
    mol for mol in candidates
    if selectivity_ratio(mol, target, antitargets) > 2.0
]
```

### Reaction-Aware Search

When `random_valid_reaction: true`, filter by synthesis pathway:

```python
from combinatorial_db.reactions import get_reaction_smarts

# Get current valid reaction for epoch
valid_reaction = get_valid_reaction_for_epoch(current_block)

# Filter molecules
valid_molecules = [
    mol for mol in candidates
    if matches_reaction_pattern(mol, valid_reaction)
]
```

### Computational Efficiency

**GPU Batch Processing**:
```python
# Maximize GPU utilization
batch_size = 128  # PSICHIC default
for batch in batched(candidates, batch_size):
    scores = psichic.predict_batch(batch, target)
```

**Caching**:
```python
# Cache molecular features
feature_cache = {}

def get_features(smiles):
    if smiles not in feature_cache:
        feature_cache[smiles] = compute_fingerprint(smiles)
    return feature_cache[smiles]
```

**Parallel Processing**:
```python
from multiprocessing import Pool

with Pool(processes=8) as pool:
    features = pool.map(featurize_molecule, molecules)
```

## Deployment on Basilica

Scale mining with GPU compute:

### 1. Provision Instance

```bash
# GPU instance for PSICHIC inference
basilica up \\
    --gpu-count 1 \\
    --name nova-miner \\
    --image nvidia/cuda:12.6.0-runtime-ubuntu24.04 \\
    --memory-mb 16384 \\
    -d
```

### 2. Transfer Code

```bash
# Copy repository and config
basilica cp -r nova/ nova-miner:/workspace/
basilica cp .env nova-miner:/workspace/nova/
```

### 3. Install Dependencies

```bash
basilica exec nova-miner "cd /workspace/nova && ./install_deps_cu126.sh"
```

### 4. Run Miner

```bash
basilica exec nova-miner "cd /workspace/nova && source .venv/bin/activate && python3 neurons/miner.py --wallet.name my_wallet --wallet.hotkey my_hotkey --logging.info"
```

### 5. Monitor

```bash
# GPU utilization
basilica exec nova-miner "nvidia-smi"

# Miner logs
basilica exec nova-miner "tail -f /workspace/nova/logs/miner.log"
```

## Troubleshooting

### GitHub Submission Fails

**Symptoms**: "Failed to upload to GitHub" error

**Solutions**:
1. Verify GitHub token has `repo` permissions
2. Check repository exists and is accessible
3. Ensure `GITHUB_PATH` < 100 characters
4. Test token: `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user`

### PSICHIC Model Not Loading

**Symptoms**: "Failed to load model weights" error

**Solutions**:
1. Check CUDA version matches (12.6 required)
2. Verify `PSICHIC/trained_weights/TREAT2/` exists
3. Ensure sufficient VRAM (8GB+ recommended)
4. Try `DEVICE_OVERRIDE="cpu"` in `.env`

### Low Miner Rank

**Symptoms**: Consistently ranked below top 50

**Solutions**:
1. Check if affinity scores competitive (compare with top miners)
2. Verify antitarget filtering working (no off-target binding)
3. Increase entropy weight consideration (diversify submissions)
4. Optimize search strategy (switch to ML-guided if using naive)
5. Monitor reaction validity (ensure synthesizable molecules)

### Out of Memory Errors

**Symptoms**: "CUDA out of memory" or system RAM exhausted

**Solutions**:
1. Reduce PSICHIC batch size: edit `PSICHIC/runtime_config.py`
2. Use CPU mode: `DEVICE_OVERRIDE="cpu"`
3. Implement streaming for large databases
4. Clear feature cache periodically

### Submission Rejected

**Symptoms**: Molecule submitted but not scored by validators

**Solutions**:
1. Check molecular property constraints (heavy atoms, rotatable bonds)
2. Verify reaction validity if filtering enabled
3. Ensure SMILES format valid (no parsing errors)
4. Check submission within allowed blocks (not during `no_submission_blocks`)

## Resources

### scripts/
- **setup_miner.sh**: Automated setup script for NOVA miner deployment

### references/
- **nova_architecture.md**: Complete technical architecture, scoring mechanisms, challenge system, API reference
- **mining_strategies.md**: Detailed strategy guides (ML-guided search, genetic algorithms, similarity search), optimization techniques, performance benchmarks

### External Resources
- **GitHub Repository**: https://github.com/metanova-labs/nova
- **Subnet Dashboard**: https://subnetalpha.ai/subnet/nova/
- **Taostats**: https://taostats.io/subnets/68/
- **Bittensor Docs**: https://docs.learnbittensor.org/
- **MetaNova Twitter**: https://x.com/metanova_labs

## Key Constraints

- **Target Changes**: Weekly rotation of protein targets
- **Antitarget Penalty**: 0.9x weight on off-target binding
- **Entropy Bonus**: Increases ~0.007 per epoch
- **Submission Window**: Must submit before (epoch_end - 10 blocks)
- **Molecular Properties**: 20+ heavy atoms, 1-10 rotatable bonds
- **GitHub Path**: Max 100 characters
- **Scoring**: Deterministic PSICHIC model (all validators agree)
- **Boltz2 Weight**: 50% of incentive for structural validation

## Success Metrics

Track these KPIs:
- **Emissions per Epoch**: TAO earned per challenge
- **Average Rank**: Position over 7-day window
- **Win Rate**: Percentage of epochs placing top 10
- **Affinity Scores**: Average target binding affinity
- **Selectivity Ratio**: Target / antitarget affinity
- **Entropy Scores**: Chemical diversity of submissions
- **Submission Success**: % of epochs with valid submissions

Target benchmarks for competitive mining:
- Rank: Top 30 (out of ~192 miners)
- Target Affinity: > 0.7
- Selectivity: > 3.0x
- Submission Success: > 95%
