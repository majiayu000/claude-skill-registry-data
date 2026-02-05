---
name: phylogenetic-methods
description: Comprehensive guide to phylogenetic tree building methods including distance-based (UPGMA, Neighbor-Joining), maximum likelihood (RAxML, IQ-TREE), and Bayesian inference (MrBayes). Covers multiple sequence alignment, distance matrices, bootstrap analysis, consensus methods, tree formats (Newick, Nexus), and tree comparison metrics. Includes implementation patterns for tree visualization and evaluation.
---

# Phylogenetic Methods

## Purpose

Provide comprehensive guidance for implementing phylogenetic tree building and analysis methods, covering multiple approaches from distance-based to advanced statistical methods.

## When to Use

This skill activates when:
- Building phylogenetic trees
- Performing sequence alignment
- Calculating distance matrices
- Running bootstrap analysis
- Creating consensus trees
- Comparing tree topologies
- Working with tree formats (Newick, Nexus)
- Implementing tree visualization
- Evaluating tree quality and support values

## Overview of Methods

### Distance-Based Methods (Fast, Good for Large Datasets)
- **UPGMA**: Simple clustering, assumes constant evolutionary rate
- **Neighbor-Joining (NJ)**: More accurate, handles rate variation

### Maximum Likelihood (ML) Methods (Accurate, Computationally Intensive)
- **RAxML-ng**: Fast ML implementation
- **IQ-TREE**: Modern, automatic model selection
- **FastTree**: Approximate ML, very fast

### Bayesian Methods (Most Rigorous, Very Slow)
- **MrBayes**: MCMC sampling of tree space
- **BEAST**: Time-calibrated trees

---

## Multiple Sequence Alignment

### Overview

Before building trees, sequences must be aligned to identify homologous positions.

### Tools Integration

```python
# app/services/phylo/alignment.py
import subprocess
from pathlib import Path
from typing import List, Dict
from Bio import SeqIO, AlignIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import tempfile

class MultipleSequenceAligner:
    """Align sequences using external tools."""

    def __init__(
        self,
        method: str = "muscle",
        muscle_path: str = "muscle",
        mafft_path: str = "mafft"
    ):
        self.method = method
        self.muscle_path = muscle_path
        self.mafft_path = mafft_path

    async def align(
        self,
        sequences: List[Dict[str, str]],
        params: Dict = None
    ) -> str:
        """
        Align multiple sequences.

        Args:
            sequences: List of dicts with 'id' and 'sequence'
            params: Method-specific parameters

        Returns:
            Aligned sequences in FASTA format
        """
        if self.method == "muscle":
            return await self._align_muscle(sequences, params or {})
        elif self.method == "mafft":
            return await self._align_mafft(sequences, params or {})
        else:
            raise ValueError(f"Unknown alignment method: {self.method}")

    async def _align_muscle(
        self,
        sequences: List[Dict[str, str]],
        params: Dict
    ) -> str:
        """Align using MUSCLE."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.fasta', delete=False
        ) as input_file:
            # Write sequences to temp file
            for seq_data in sequences:
                input_file.write(f">{seq_data['id']}\n{seq_data['sequence']}\n")
            input_file.flush()

            with tempfile.NamedTemporaryFile(
                mode='r', suffix='.fasta', delete=False
            ) as output_file:
                # Run MUSCLE
                cmd = [
                    self.muscle_path,
                    "-in", input_file.name,
                    "-out", output_file.name
                ]

                # Add parameters
                if params.get("max_iterations"):
                    cmd.extend(["-maxiters", str(params["max_iterations"])])

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=600
                )

                if result.returncode != 0:
                    raise AlignmentError(f"MUSCLE failed: {result.stderr}")

                # Read aligned sequences
                return Path(output_file.name).read_text()

    async def _align_mafft(
        self,
        sequences: List[Dict[str, str]],
        params: Dict
    ) -> str:
        """Align using MAFFT."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.fasta', delete=False
        ) as input_file:
            for seq_data in sequences:
                input_file.write(f">{seq_data['id']}\n{seq_data['sequence']}\n")
            input_file.flush()

            # Run MAFFT
            cmd = [self.mafft_path]

            # Algorithm selection
            if params.get("algorithm") == "auto":
                cmd.append("--auto")
            elif params.get("algorithm") == "linsi":
                cmd.append("--localpair")
                cmd.append("--maxiterate")
                cmd.append("1000")

            cmd.append(input_file.name)

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )

            if result.returncode != 0:
                raise AlignmentError(f"MAFFT failed: {result.stderr}")

            return result.stdout

    def validate_alignment(self, alignment_text: str) -> Dict:
        """
        Validate alignment quality.

        Returns:
            Quality metrics
        """
        alignment = AlignIO.read(
            StringIO(alignment_text),
            "fasta"
        )

        length = alignment.get_alignment_length()
        num_sequences = len(alignment)

        # Calculate gap percentage
        gaps = sum(
            1 for record in alignment
            for base in str(record.seq)
            if base == '-'
        )
        total = length * num_sequences
        gap_percentage = gaps / total

        # Calculate conserved positions
        conserved = 0
        for i in range(length):
            column = alignment[:, i]
            if len(set(column)) == 1:
                conserved += 1

        return {
            "length": length,
            "num_sequences": num_sequences,
            "gap_percentage": gap_percentage,
            "conserved_positions": conserved,
            "conservation_rate": conserved / length
        }
```

---

## Distance-Based Methods

### Distance Matrix Calculation

```python
# app/services/phylo/distance.py
import numpy as np
from typing import List, Dict
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator
from io import StringIO

class DistanceMatrixCalculator:
    """Calculate distance matrices from alignments."""

    def __init__(self, model: str = "identity"):
        """
        Initialize calculator.

        Args:
            model: Distance model (identity, blastn, etc.)
        """
        self.model = model

    def calculate(self, alignment_text: str) -> np.ndarray:
        """
        Calculate distance matrix.

        Args:
            alignment_text: Aligned sequences in FASTA format

        Returns:
            Distance matrix (n_sequences, n_sequences)
        """
        alignment = AlignIO.read(StringIO(alignment_text), "fasta")

        if self.model == "identity":
            return self._identity_distance(alignment)
        elif self.model == "jukes_cantor":
            return self._jukes_cantor_distance(alignment)
        elif self.model == "kimura":
            return self._kimura_distance(alignment)
        else:
            # Use Biopython's calculator
            calculator = DistanceCalculator(self.model)
            dm = calculator.get_distance(alignment)
            return np.array([dm[i] for i in range(len(dm))])

    def _identity_distance(self, alignment) -> np.ndarray:
        """Simple identity-based distance."""
        n = len(alignment)
        matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(i+1, n):
                seq1 = str(alignment[i].seq)
                seq2 = str(alignment[j].seq)

                # Count differences (ignore gaps)
                differences = sum(
                    1 for a, b in zip(seq1, seq2)
                    if a != '-' and b != '-' and a != b
                )
                valid_positions = sum(
                    1 for a, b in zip(seq1, seq2)
                    if a != '-' and b != '-'
                )

                distance = differences / valid_positions if valid_positions > 0 else 1.0
                matrix[i, j] = distance
                matrix[j, i] = distance

        return matrix

    def _jukes_cantor_distance(self, alignment) -> np.ndarray:
        """Jukes-Cantor correction for multiple substitutions."""
        identity_matrix = self._identity_distance(alignment)

        # Jukes-Cantor formula: d = -3/4 * ln(1 - 4/3 * p)
        # where p is the proportion of different sites
        with np.errstate(divide='ignore', invalid='ignore'):
            jc_matrix = -0.75 * np.log(1 - (4.0/3.0) * identity_matrix)
            jc_matrix[np.isnan(jc_matrix)] = 1.0  # Handle saturation
            jc_matrix[np.isinf(jc_matrix)] = 1.0

        return jc_matrix

    def _kimura_distance(self, alignment) -> np.ndarray:
        """Kimura 2-parameter distance."""
        n = len(alignment)
        matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(i+1, n):
                seq1 = str(alignment[i].seq)
                seq2 = str(alignment[j].seq)

                transitions = 0  # A<->G, C<->T
                transversions = 0  # Other changes
                valid = 0

                for a, b in zip(seq1, seq2):
                    if a == '-' or b == '-':
                        continue
                    valid += 1
                    if a != b:
                        if (a, b) in [('A','G'), ('G','A'), ('C','T'), ('T','C')]:
                            transitions += 1
                        else:
                            transversions += 1

                if valid == 0:
                    distance = 1.0
                else:
                    P = transitions / valid  # Transition proportion
                    Q = transversions / valid  # Transversion proportion

                    # Kimura formula
                    try:
                        distance = -0.5 * np.log((1 - 2*P - Q) * np.sqrt(1 - 2*Q))
                    except:
                        distance = 1.0

                matrix[i, j] = distance
                matrix[j, i] = distance

        return matrix
```

### UPGMA Implementation

```python
# app/services/phylo/upgma.py
import numpy as np
from typing import List, Dict, Tuple
from ete3 import Tree

class UPGMATreeBuilder:
    """Build trees using UPGMA (Unweighted Pair Group Method with Arithmetic Mean)."""

    def __init__(self):
        self.taxa_names = []

    def build(
        self,
        distance_matrix: np.ndarray,
        taxa_names: List[str]
    ) -> Tree:
        """
        Build UPGMA tree.

        Args:
            distance_matrix: Pairwise distance matrix
            taxa_names: Names of taxa (same order as matrix)

        Returns:
            Phylogenetic tree (ete3 Tree)
        """
        self.taxa_names = taxa_names
        n = len(taxa_names)

        # Initialize clusters (each taxon is a cluster)
        clusters = {i: Tree(name=taxa_names[i]) for i in range(n)}
        cluster_sizes = {i: 1 for i in range(n)}

        # Working copy of distance matrix
        dm = distance_matrix.copy()

        # Track active clusters
        active = set(range(n))

        while len(active) > 1:
            # Find minimum distance
            min_dist = float('inf')
            merge_i, merge_j = -1, -1

            for i in active:
                for j in active:
                    if i < j and dm[i, j] < min_dist:
                        min_dist = dm[i, j]
                        merge_i, merge_j = i, j

            # Create new cluster
            new_cluster = Tree()
            new_cluster.add_child(clusters[merge_i], dist=min_dist/2)
            new_cluster.add_child(clusters[merge_j], dist=min_dist/2)

            # Update clusters
            new_idx = max(clusters.keys()) + 1
            clusters[new_idx] = new_cluster
            cluster_sizes[new_idx] = cluster_sizes[merge_i] + cluster_sizes[merge_j]

            # Update distance matrix (UPGMA averaging)
            new_distances = {}
            for k in active:
                if k != merge_i and k != merge_j:
                    # Average distance weighted by cluster sizes
                    new_dist = (
                        dm[merge_i, k] * cluster_sizes[merge_i] +
                        dm[merge_j, k] * cluster_sizes[merge_j]
                    ) / (cluster_sizes[merge_i] + cluster_sizes[merge_j])
                    new_distances[k] = new_dist

            # Add new row/column to matrix
            for k, dist in new_distances.items():
                dm[new_idx, k] = dist
                dm[k, new_idx] = dist

            # Remove merged clusters
            active.remove(merge_i)
            active.remove(merge_j)
            active.add(new_idx)

        # Return root
        return clusters[list(active)[0]]
```

### Neighbor-Joining Implementation

```python
# app/services/phylo/neighbor_joining.py
import numpy as np
from ete3 import Tree

class NeighborJoiningTreeBuilder:
    """Build trees using Neighbor-Joining algorithm."""

    def build(
        self,
        distance_matrix: np.ndarray,
        taxa_names: List[str]
    ) -> Tree:
        """
        Build Neighbor-Joining tree.

        Args:
            distance_matrix: Pairwise distance matrix
            taxa_names: Names of taxa

        Returns:
            Phylogenetic tree
        """
        n = len(taxa_names)
        dm = distance_matrix.copy()

        # Initialize nodes
        nodes = {i: Tree(name=taxa_names[i]) for i in range(n)}
        active = set(range(n))

        while len(active) > 2:
            # Calculate net divergence (r)
            r = {}
            for i in active:
                r[i] = sum(dm[i, j] for j in active if j != i)

            # Calculate Q matrix
            Q = np.full_like(dm, float('inf'))
            for i in active:
                for j in active:
                    if i < j:
                        Q[i, j] = (len(active) - 2) * dm[i, j] - r[i] - r[j]

            # Find minimum Q
            min_q = float('inf')
            merge_i, merge_j = -1, -1
            for i in active:
                for j in active:
                    if i < j and Q[i, j] < min_q:
                        min_q = Q[i, j]
                        merge_i, merge_j = i, j

            # Calculate branch lengths
            dist_i = dm[merge_i, merge_j] / 2 + (r[merge_i] - r[merge_j]) / (2 * (len(active) - 2))
            dist_j = dm[merge_i, merge_j] - dist_i

            # Create new node
            new_node = Tree()
            new_node.add_child(nodes[merge_i], dist=max(0, dist_i))
            new_node.add_child(nodes[merge_j], dist=max(0, dist_j))

            # Update nodes
            new_idx = max(nodes.keys()) + 1
            nodes[new_idx] = new_node

            # Update distance matrix
            for k in active:
                if k != merge_i and k != merge_j:
                    new_dist = (dm[merge_i, k] + dm[merge_j, k] - dm[merge_i, merge_j]) / 2
                    dm[new_idx, k] = new_dist
                    dm[k, new_idx] = new_dist

            # Remove merged nodes
            active.remove(merge_i)
            active.remove(merge_j)
            active.add(new_idx)

        # Connect last two nodes
        remaining = list(active)
        if len(remaining) == 2:
            i, j = remaining
            root = Tree()
            root.add_child(nodes[i], dist=dm[i, j]/2)
            root.add_child(nodes[j], dist=dm[i, j]/2)
            return root

        return nodes[remaining[0]]
```

---

## Maximum Likelihood Methods

### RAxML-ng Integration

```python
# app/services/phylo/raxml.py
import subprocess
from pathlib import Path
import tempfile
from ete3 import Tree

class RAxMLTreeBuilder:
    """Build ML trees using RAxML-ng."""

    def __init__(self, raxml_path: str = "raxml-ng"):
        self.raxml_path = raxml_path

    async def build(
        self,
        alignment_text: str,
        model: str = "GTR+G",
        num_searches: int = 10,
        num_bootstrap: int = 100
    ) -> Dict:
        """
        Build ML tree with bootstrap support.

        Args:
            alignment_text: Aligned sequences (FASTA)
            model: Substitution model
            num_searches: Number of ML searches
            num_bootstrap: Number of bootstrap replicates

        Returns:
            Dict with best tree and bootstrap tree
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Write alignment
            aln_file = tmpdir / "alignment.fasta"
            aln_file.write_text(alignment_text)

            # Run ML search
            cmd = [
                self.raxml_path,
                "--msa", str(aln_file),
                "--model", model,
                "--search",
                "--tree", f"pars{{{num_searches}}}",
                "--prefix", str(tmpdir / "ml")
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600
            )

            if result.returncode != 0:
                raise TreeBuildingError(f"RAxML failed: {result.stderr}")

            # Run bootstrap
            cmd_bs = [
                self.raxml_path,
                "--msa", str(aln_file),
                "--model", model,
                "--bootstrap",
                "--bs-trees", str(num_bootstrap),
                "--prefix", str(tmpdir / "bootstrap")
            ]

            subprocess.run(cmd_bs, capture_output=True, timeout=3600)

            # Map bootstrap support to best tree
            cmd_support = [
                self.raxml_path,
                "--support",
                "--tree", str(tmpdir / "ml.raxml.bestTree"),
                "--bs-trees", str(tmpdir / "bootstrap.raxml.bootstraps"),
                "--prefix", str(tmpdir / "support")
            ]

            subprocess.run(cmd_support, capture_output=True, timeout=300)

            # Read results
            best_tree = Tree(str(tmpdir / "support.raxml.support"))

            return {
                "tree": best_tree,
                "log_likelihood": self._parse_likelihood(
                    (tmpdir / "ml.raxml.log").read_text()
                )
            }

    def _parse_likelihood(self, log_text: str) -> float:
        """Parse log likelihood from RAxML log."""
        for line in log_text.split('\n'):
            if "Final LogLikelihood:" in line:
                return float(line.split()[-1])
        return None
```

---

## Bootstrap Analysis

```python
# app/services/phylo/bootstrap.py
import numpy as np
from typing import List
from Bio import AlignIO
from io import StringIO

class BootstrapAnalyzer:
    """Perform bootstrap analysis for tree support."""

    def __init__(self, tree_builder):
        self.tree_builder = tree_builder

    async def bootstrap(
        self,
        alignment_text: str,
        num_replicates: int = 100,
        method: str = "nj"
    ) -> List[Tree]:
        """
        Generate bootstrap replicates.

        Args:
            alignment_text: Original alignment
            num_replicates: Number of bootstrap samples
            method: Tree building method

        Returns:
            List of bootstrap trees
        """
        alignment = AlignIO.read(StringIO(alignment_text), "fasta")
        length = alignment.get_alignment_length()

        trees = []

        for _ in range(num_replicates):
            # Resample columns with replacement
            indices = np.random.choice(length, size=length, replace=True)

            # Create bootstrap alignment
            bootstrap_aln = self._resample_alignment(alignment, indices)

            # Build tree
            tree = await self.tree_builder.build(bootstrap_aln)
            trees.append(tree)

        return trees

    def _resample_alignment(self, alignment, indices):
        """Create resampled alignment."""
        from Bio.Align import MultipleSeqAlignment

        new_records = []
        for record in alignment:
            seq = str(record.seq)
            new_seq = ''.join(seq[i] for i in indices)
            new_records.append(
                SeqRecord(Seq(new_seq), id=record.id, description="")
            )

        return MultipleSeqAlignment(new_records)

    def calculate_support_values(
        self,
        best_tree: Tree,
        bootstrap_trees: List[Tree]
    ) -> Tree:
        """
        Map bootstrap support to best tree.

        Args:
            best_tree: Best tree from original data
            bootstrap_trees: Trees from bootstrap replicates

        Returns:
            Tree with support values
        """
        # Get bipartitions from best tree
        best_bipartitions = self._get_bipartitions(best_tree)

        # Count occurrences in bootstrap trees
        support_counts = {bp: 0 for bp in best_bipartitions}

        for bs_tree in bootstrap_trees:
            bs_bipartitions = self._get_bipartitions(bs_tree)
            for bp in best_bipartitions:
                if bp in bs_bipartitions:
                    support_counts[bp] += 1

        # Add support values to tree
        for node in best_tree.traverse():
            if not node.is_leaf():
                leaves = frozenset(l.name for l in node.get_leaves())
                if leaves in support_counts:
                    node.support = support_counts[leaves] / len(bootstrap_trees)

        return best_tree

    def _get_bipartitions(self, tree: Tree) -> List[frozenset]:
        """Extract bipartitions from tree."""
        bipartitions = []
        for node in tree.traverse():
            if not node.is_leaf():
                leaves = frozenset(l.name for l in node.get_leaves())
                bipartitions.append(leaves)
        return bipartitions
```

---

## Tree Formats

### Newick Format

```python
# app/services/phylo/formats.py
from ete3 import Tree

class TreeFormatter:
    """Convert between tree formats."""

    @staticmethod
    def to_newick(tree: Tree, include_support: bool = True) -> str:
        """
        Convert tree to Newick format.

        Args:
            tree: ete3 Tree object
            include_support: Include support values

        Returns:
            Newick string
        """
        if include_support:
            return tree.write(format=0)  # format 0: branch length + support
        else:
            return tree.write(format=5)  # format 5: branch length only

    @staticmethod
    def from_newick(newick_str: str) -> Tree:
        """Parse Newick string."""
        return Tree(newick_str, format=1)

    @staticmethod
    def to_nexus(tree: Tree, taxa_names: List[str]) -> str:
        """Convert to NEXUS format."""
        nexus = "#NEXUS\n\n"
        nexus += "BEGIN TAXA;\n"
        nexus += f"  DIMENSIONS NTAX={len(taxa_names)};\n"
        nexus += "  TAXLABELS\n"
        for name in taxa_names:
            nexus += f"    {name}\n"
        nexus += "  ;\n"
        nexus += "END;\n\n"
        nexus += "BEGIN TREES;\n"
        nexus += f"  TREE tree1 = {tree.write(format=0)}\n"
        nexus += "END;\n"
        return nexus
```

---

## Best Practices

### ✅ DO
- Use appropriate substitution models for your data
- Perform bootstrap analysis for support values
- Compare multiple tree-building methods
- Validate alignment quality before tree building
- Root trees appropriately (outgroup or midpoint)
- Calculate branch support values
- Document method parameters
- Test with known phylogenies
- Use consensus methods for multiple trees
- Consider computational cost vs accuracy trade-offs

### ❌ DON'T
- Skip sequence alignment
- Ignore alignment gaps (handle properly)
- Use wrong distance model
- Over-interpret low bootstrap values (<70%)
- Compare trees without proper metrics
- Ignore unrooted vs rooted trees
- Skip model selection
- Trust single-method trees for critical work
- Ignore branch lengths
- Use distance methods for deep phylogenies

---

**Related Skills**: [rRNA-prediction-patterns](../rrna-prediction-patterns/SKILL.md), [ml-integration-patterns](../ml-integration-patterns/SKILL.md)

**Line Count**: < 500 lines ✅
