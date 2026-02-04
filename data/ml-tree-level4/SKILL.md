---
name: ml-tree-level4
description: Advanced Maximum Likelihood phylogenetics with model selection (AIC/BIC), tree search algorithms (NNI/SPR/TBR), and performance optimization (Numba/GPU)
type: domain
priority: high
---

# ML Tree Level 4 - Advanced Maximum Likelihood Methods

## Overview

Level 4 enhances Maximum Likelihood tree inference with:
1. **Model Selection**: Automatically test and select best evolutionary model using AIC/BIC
2. **Tree Search Algorithms**: NNI, SPR, TBR for finding optimal tree topologies
3. **Advanced Rate Models**: FreeRate, partition models, branch-specific rates
4. **Performance Optimization**: Numba JIT, GPU acceleration, Cython

## Current Status (Level 3)

Level 3 implementation includes:
- GTR model with empirical base frequencies
- Gamma rate heterogeneity (α parameter)
- Felsenstein's pruning algorithm
- Basic likelihood optimization (bfgs)
- Support for DNA, RNA, and protein sequences

**Files**: `backend/rrna_phylo/models/ml_tree_level3.py`

## Level 4 Feature 1: Model Selection

### Theory

**Information Criteria**:
- **AIC** (Akaike): `AIC = -2*ln(L) + 2*k`
- **BIC** (Bayesian): `BIC = -2*ln(L) + k*ln(n)`
- Lower is better (penalizes complexity)

**Models to Test**:
```python
DNA_MODELS = {
    'JC69': 0 params,      # Equal rates, equal frequencies
    'K80': 1 param,        # Transition/transversion ratio
    'F81': 3 params,       # Empirical frequencies
    'HKY85': 4 params,     # K80 + empirical frequencies
    'GTR': 6 params,       # General time reversible
    'GTR+G': 7 params,     # GTR + gamma rate heterogeneity
}

PROTEIN_MODELS = {
    'JTT': 0 params,       # Jones-Taylor-Thornton matrix
    'WAG': 0 params,       # Whelan and Goldman
    'LG': 0 params,        # Le and Gascuel
    'JTT+G': 1 param,      # JTT + gamma
}
```

### Implementation Pattern

```python
def select_best_model(
    sequences: List[Sequence],
    tree: TreeNode,
    criterion: str = 'BIC',
    models: List[str] = None,
    verbose: bool = False
) -> Tuple[str, float, Dict[str, float]]:
    """
    Test multiple models and select best using AIC/BIC.

    Args:
        sequences: Aligned sequences
        tree: Initial tree topology
        criterion: 'AIC' or 'BIC'
        models: List of model names to test (None = test all)
        verbose: Print comparison table

    Returns:
        (best_model_name, best_score, all_scores)

    Example:
        best, score, all_scores = select_best_model(
            sequences,
            initial_tree,
            criterion='BIC'
        )
        # best = 'GTR+G'
        # all_scores = {'JC69': 5420.3, 'K80': 5315.2, 'GTR+G': 5298.1}
    """
    results = {}
    n_sites = len(sequences[0].sequence)

    for model_name in models:
        # Compute likelihood with this model
        logL, params = compute_likelihood_with_model(
            tree, sequences, model_name
        )

        # Calculate information criterion
        k = len(params)  # Number of free parameters
        if criterion == 'AIC':
            score = -2 * logL + 2 * k
        else:  # BIC
            score = -2 * logL + k * np.log(n_sites)

        results[model_name] = {
            'logL': logL,
            'params': k,
            'score': score
        }

    # Find best model (lowest score)
    best_model = min(results.items(), key=lambda x: x[1]['score'])

    if verbose:
        print("\nModel Selection Results:")
        print(f"Criterion: {criterion}")
        print(f"{'Model':<12} {'LogL':>12} {'Params':>8} {criterion:>12}")
        print("-" * 48)
        for name, res in sorted(results.items(), key=lambda x: x[1]['score']):
            marker = " *" if name == best_model[0] else ""
            print(f"{name:<12} {res['logL']:>12.2f} {res['params']:>8} "
                  f"{res['score']:>12.2f}{marker}")

    return best_model[0], best_model[1]['score'], results
```

### Model Classes

```python
class SubstitutionModel:
    """Base class for substitution models."""

    def __init__(self, name: str, n_params: int):
        self.name = name
        self.n_params = n_params

    def get_rate_matrix(self, params: np.ndarray, freqs: np.ndarray) -> np.ndarray:
        """Get Q matrix for this model."""
        raise NotImplementedError

class JC69Model(SubstitutionModel):
    """Jukes-Cantor: equal rates, equal frequencies."""

    def __init__(self):
        super().__init__('JC69', n_params=0)

    def get_rate_matrix(self, params=None, freqs=None) -> np.ndarray:
        # All rates equal (normalized to 1)
        freqs = np.array([0.25, 0.25, 0.25, 0.25])
        Q = np.ones((4, 4)) * 0.25
        np.fill_diagonal(Q, 0)
        np.fill_diagonal(Q, -Q.sum(axis=1))
        return Q

class K80Model(SubstitutionModel):
    """Kimura: different transition/transversion rates."""

    def __init__(self):
        super().__init__('K80', n_params=1)

    def get_rate_matrix(self, params: np.ndarray, freqs=None) -> np.ndarray:
        kappa = params[0]  # transition/transversion ratio
        freqs = np.array([0.25, 0.25, 0.25, 0.25])

        # Build Q matrix
        Q = np.array([
            [0, 1, kappa, 1],      # A -> C(transv), G(trans), T(transv)
            [1, 0, 1, kappa],      # C -> A(transv), G(transv), T(trans)
            [kappa, 1, 0, 1],      # G -> A(trans), C(transv), T(transv)
            [1, kappa, 1, 0]       # T -> A(transv), C(trans), G(transv)
        ]) * freqs

        np.fill_diagonal(Q, -Q.sum(axis=1))
        return Q
```

## Level 4 Feature 2: Tree Search Algorithms

### NNI (Nearest Neighbor Interchange)

**Algorithm**:
1. For each internal branch
2. Swap one subtree from each side
3. Calculate new likelihood
4. Accept if better
5. Repeat until no improvement

```python
def nni_search(
    tree: TreeNode,
    sequences: List[Sequence],
    model: str = 'GTR',
    max_iterations: int = 100,
    verbose: bool = False
) -> Tuple[TreeNode, float, int]:
    """
    Improve tree topology using NNI rearrangements.

    Args:
        tree: Starting tree
        sequences: Aligned sequences
        model: Substitution model
        max_iterations: Max NNI rounds
        verbose: Print progress

    Returns:
        (best_tree, best_logL, n_improvements)

    Algorithm:
        1. Calculate initial likelihood
        2. For each internal branch:
           a. Generate 2 NNI neighbors
           b. Calculate likelihoods
           c. Accept best if better
        3. Repeat until convergence
    """
    current_tree = tree.copy()
    current_logL = compute_likelihood(current_tree, sequences, model)

    improvements = 0

    for iteration in range(max_iterations):
        improved = False

        # Get all internal branches
        internal_edges = get_internal_edges(current_tree)

        for edge in internal_edges:
            # Generate NNI neighbors
            neighbor1, neighbor2 = generate_nni_neighbors(current_tree, edge)

            # Calculate likelihoods
            logL1 = compute_likelihood(neighbor1, sequences, model)
            logL2 = compute_likelihood(neighbor2, sequences, model)

            # Accept best if better
            best_logL = max(logL1, logL2, current_logL)

            if best_logL > current_logL:
                if logL1 > logL2:
                    current_tree = neighbor1
                else:
                    current_tree = neighbor2
                current_logL = best_logL
                improved = True
                improvements += 1

                if verbose:
                    print(f"Iteration {iteration}: LogL improved to {current_logL:.2f}")

        if not improved:
            if verbose:
                print(f"NNI converged after {iteration} iterations")
            break

    return current_tree, current_logL, improvements

def generate_nni_neighbors(tree: TreeNode, edge: Tuple[TreeNode, TreeNode]) -> Tuple[TreeNode, TreeNode]:
    """
    Generate two NNI neighbors by swapping subtrees.

    For edge connecting nodes A and B:
         A               A               A
        / \             / \             / \
       L   B    -->    C   B    or     L   B
          / \             / \             / \
         C   R           L   R           R   C

    Args:
        tree: Original tree
        edge: (parent, child) nodes defining internal edge

    Returns:
        (neighbor1, neighbor2): Two NNI rearrangements
    """
    parent, child = edge

    # Copy tree
    tree1 = tree.copy()
    tree2 = tree.copy()

    # Find corresponding nodes in copies
    p1 = find_node(tree1, parent.name)
    c1 = find_node(tree1, child.name)

    p2 = find_node(tree2, parent.name)
    c2 = find_node(tree2, child.name)

    # Swap subtrees (different for each neighbor)
    # Neighbor 1: swap parent.left with child.left
    p1.left, c1.left = c1.left, p1.left

    # Neighbor 2: swap parent.left with child.right
    p2.left, c2.right = c2.right, p2.left

    return tree1, tree2
```

### SPR (Subtree Pruning and Regrafting)

**More aggressive than NNI**:
1. Cut a subtree
2. Reattach at a different location
3. Explores more of tree space

```python
def spr_search(
    tree: TreeNode,
    sequences: List[Sequence],
    model: str = 'GTR',
    max_iterations: int = 50,
    verbose: bool = False
) -> Tuple[TreeNode, float, int]:
    """
    Improve tree using SPR rearrangements.

    SPR explores more tree space than NNI but is more expensive.

    Algorithm:
        1. For each branch, prune subtree
        2. For each other branch, regraft
        3. Calculate likelihood
        4. Accept best if better
    """
    # Implementation similar to NNI but with more extensive rearrangements
    pass
```

## Level 4 Feature 3: Advanced Rate Models

### FreeRate Model

Allows rate categories without gamma distribution constraint:

```python
def compute_freerate_categories(
    tree: TreeNode,
    sequences: List[Sequence],
    n_categories: int = 4
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Estimate free rate categories (weights and rates).

    Unlike gamma, rates are free parameters estimated from data.

    Args:
        tree: Tree topology
        sequences: Aligned sequences
        n_categories: Number of rate categories

    Returns:
        (rates, weights): Rate values and category probabilities

    Example:
        rates, weights = compute_freerate_categories(tree, seqs, 4)
        # rates = [0.05, 0.3, 1.2, 2.8]  # Free parameters
        # weights = [0.25, 0.25, 0.25, 0.25]  # Can also be optimized
    """
    # Optimize rates and weights jointly
    def objective(params):
        rates = params[:n_categories]
        weights = softmax(params[n_categories:])  # Ensure sum to 1

        logL = 0
        for site in range(n_sites):
            site_L = 0
            for rate, weight in zip(rates, weights):
                site_L += weight * compute_site_likelihood(tree, site, rate)
            logL += np.log(site_L)

        return -logL

    # Initialize
    initial = np.concatenate([
        np.linspace(0.1, 3.0, n_categories),  # Initial rates
        np.ones(n_categories)                  # Initial log-weights
    ])

    result = minimize(objective, initial, method='L-BFGS-B')

    rates = result.x[:n_categories]
    weights = softmax(result.x[n_categories:])

    return rates, weights
```

### Partition Models

Different models for different regions (e.g., codon positions):

```python
class PartitionModel:
    """Apply different models to different sequence regions."""

    def __init__(self, partitions: List[Dict]):
        """
        Args:
            partitions: List of partition definitions

        Example:
            partitions = [
                {'start': 0, 'end': 300, 'model': 'GTR+G', 'alpha': 0.5},
                {'start': 300, 'end': 600, 'model': 'GTR', 'alpha': None},
            ]
        """
        self.partitions = partitions

    def compute_likelihood(self, tree: TreeNode, sequences: List[Sequence]) -> float:
        """Sum log-likelihoods across partitions."""
        total_logL = 0

        for partition in self.partitions:
            # Extract sites for this partition
            part_seqs = [
                Sequence(s.id, s.description,
                        s.sequence[partition['start']:partition['end']])
                for s in sequences
            ]

            # Compute likelihood with partition-specific model
            logL = compute_likelihood(
                tree, part_seqs,
                model=partition['model'],
                alpha=partition['alpha']
            )

            total_logL += logL

        return total_logL
```

## Level 4 Feature 4: Performance Optimization

### Numba JIT Compilation

```python
import numba as nb

@nb.jit(nopython=True, cache=True)
def compute_likelihood_fast(
    P_matrices: np.ndarray,  # [n_edges, n_states, n_states]
    site_patterns: np.ndarray,  # [n_sites, n_taxa]
    frequencies: np.ndarray,  # [n_states]
    tree_structure: np.ndarray  # [n_nodes, 3] (parent, left, right indices)
) -> float:
    """
    Numba-optimized likelihood calculation.

    All tree traversal and matrix operations compiled to native code.
    Can give 10-100x speedup for large datasets.
    """
    n_sites = site_patterns.shape[0]
    n_nodes = tree_structure.shape[0]
    n_states = P_matrices.shape[1]

    # Allocate likelihood arrays
    L = np.zeros((n_nodes, n_sites, n_states))

    # Initialize leaves
    for leaf_idx in range(n_taxa):
        for site in range(n_sites):
            state = site_patterns[site, leaf_idx]
            L[leaf_idx, site, state] = 1.0

    # Traverse internal nodes (post-order)
    for node_idx in range(n_taxa, n_nodes):
        parent, left, right = tree_structure[node_idx]

        for site in range(n_sites):
            for i in range(n_states):
                # Compute partial likelihood
                left_sum = 0.0
                right_sum = 0.0

                for j in range(n_states):
                    left_sum += P_matrices[left, i, j] * L[left, site, j]
                    right_sum += P_matrices[right, i, j] * L[right, site, j]

                L[node_idx, site, i] = left_sum * right_sum

    # Sum over root states with frequencies
    root = n_nodes - 1
    logL = 0.0
    for site in range(n_sites):
        site_L = 0.0
        for i in range(n_states):
            site_L += frequencies[i] * L[root, site, i]
        logL += np.log(site_L)

    return logL
```

### GPU Acceleration (CuPy)

```python
try:
    import cupy as cp
    HAS_GPU = True
except ImportError:
    HAS_GPU = False

def compute_likelihood_gpu(
    tree: TreeNode,
    sequences: List[Sequence],
    model: str = 'GTR',
    alpha: float = None
) -> float:
    """
    GPU-accelerated likelihood calculation using CuPy.

    Useful for large alignments (>1000 sites).
    """
    if not HAS_GPU:
        return compute_likelihood(tree, sequences, model, alpha)

    # Move data to GPU
    P_matrices_gpu = cp.array(P_matrices)
    site_patterns_gpu = cp.array(site_patterns)
    frequencies_gpu = cp.array(frequencies)

    # Compute on GPU
    logL_gpu = _likelihood_kernel_gpu(
        P_matrices_gpu,
        site_patterns_gpu,
        frequencies_gpu
    )

    # Move result back to CPU
    return float(logL_gpu.get())
```

## Integration with Existing Code

### Update builder.py

```python
def build_ml_tree_level4(
    sequences: List[Sequence],
    method: str = 'ml',
    model: str = 'auto',  # NEW: Auto-select with BIC
    alpha: float = None,
    tree_search: str = 'nni',  # NEW: NNI, SPR, or None
    optimize_branches: bool = True,
    verbose: bool = False
) -> Tuple[TreeNode, float, Dict]:
    """
    Build ML tree with Level 4 enhancements.

    Args:
        model: 'auto' for model selection, or specific model name
        tree_search: 'nni', 'spr', or None

    Returns:
        (tree, logL, metadata)
        metadata includes: selected_model, n_improvements, time_taken
    """
    # Step 1: Get initial tree
    initial_tree = build_bionj_tree(sequences)

    # Step 2: Model selection
    if model == 'auto':
        best_model, score, all_scores = select_best_model(
            sequences, initial_tree, criterion='BIC', verbose=verbose
        )
    else:
        best_model = model

    # Step 3: Tree search
    if tree_search == 'nni':
        final_tree, logL, n_improvements = nni_search(
            initial_tree, sequences, model=best_model, verbose=verbose
        )
    elif tree_search == 'spr':
        final_tree, logL, n_improvements = spr_search(
            initial_tree, sequences, model=best_model, verbose=verbose
        )
    else:
        final_tree = initial_tree
        logL = compute_likelihood(final_tree, sequences, best_model)
        n_improvements = 0

    # Step 4: Optimize branch lengths
    if optimize_branches:
        final_tree, logL = optimize_branch_lengths(
            final_tree, sequences, best_model
        )

    metadata = {
        'model': best_model,
        'tree_search': tree_search,
        'n_improvements': n_improvements,
    }

    return final_tree, logL, metadata
```

## Testing Strategy

### Test Model Selection

```python
def test_model_selection():
    """Verify model selection works correctly."""
    # Use sequences where GTR should clearly win
    sequences = load_test_sequences('mammals.fasta')
    tree = build_bionj_tree(sequences)

    best_model, score, all_scores = select_best_model(
        sequences, tree, criterion='BIC'
    )

    # GTR+G should be selected for real data
    assert best_model in ['GTR', 'GTR+G', 'HKY85']

    # Check that scores are ordered
    assert all_scores['GTR+G'] < all_scores['JC69']
```

### Test NNI Search

```python
def test_nni_improves_likelihood():
    """Verify NNI finds better trees."""
    sequences = load_test_sequences('primates.fasta')

    # Start with UPGMA (often suboptimal)
    initial_tree = build_upgma_tree(sequences)
    initial_logL = compute_likelihood(initial_tree, sequences, 'GTR')

    # Run NNI
    final_tree, final_logL, n_improvements = nni_search(
        initial_tree, sequences, model='GTR', max_iterations=10
    )

    # Should improve
    assert final_logL >= initial_logL
    assert n_improvements > 0
```

### Performance Benchmarks

```python
def benchmark_optimizations():
    """Compare performance of different implementations."""
    sequences = generate_test_sequences(n_seqs=50, length=1000)
    tree = build_bionj_tree(sequences)

    # Baseline Python
    start = time.time()
    logL_python = compute_likelihood_python(tree, sequences)
    time_python = time.time() - start

    # Numba
    start = time.time()
    logL_numba = compute_likelihood_numba(tree, sequences)
    time_numba = time.time() - start

    # GPU (if available)
    if HAS_GPU:
        start = time.time()
        logL_gpu = compute_likelihood_gpu(tree, sequences)
        time_gpu = time.time() - start

        print(f"GPU speedup: {time_python/time_gpu:.1f}x")

    print(f"Numba speedup: {time_python/time_numba:.1f}x")

    # Verify all give same result
    assert abs(logL_python - logL_numba) < 0.01
```

## Common Pitfalls

1. **Model Selection Overfitting**: More parameters always improve likelihood, use BIC not just likelihood
2. **Local Optima**: NNI can get stuck, try multiple starting trees
3. **Numerical Precision**: Use log-space for all likelihood calculations
4. **Performance**: Don't optimize prematurely, profile first
5. **GPU Memory**: Large trees may not fit in GPU memory

## References

- Model Selection: Posada & Crandall (1998) "MODELTEST"
- NNI: Swofford et al. (1996) "Phylogenetic inference"
- SPR: Hordijk & Gascuel (2005) "Improving NNI"
- FreeRate: Soubrier et al. (2012) "FreeRate models"
- Performance: Kosakovsky Pond et al. (2005) "HyPhy"
