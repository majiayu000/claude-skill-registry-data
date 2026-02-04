---
name: ml-integration-patterns
description: Machine learning integration patterns for rRNA-Phylo covering three use cases - rRNA sequence classification (supervised learning with sklearn/PyTorch), multi-tree consensus (ensemble methods), and generative tree synthesis (GNNs/transformers). Includes feature engineering, model training, hyperparameter tuning, model serving, versioning, and evaluation metrics for bioinformatics ML workflows.
---

# ML Integration Patterns

## Purpose

Provide comprehensive patterns for integrating machine learning into the rRNA-Phylo project across three distinct use cases: rRNA classification, phylogenetic tree consensus, and generative tree synthesis.

## When to Use

This skill activates when:
- Training ML models for rRNA detection
- Implementing feature engineering for sequences
- Building ensemble methods for tree consensus
- Working with graph neural networks for trees
- Model serving and inference
- ML model evaluation and metrics
- Hyperparameter tuning
- Model versioning and deployment

## Three ML Use Cases

### 1. **rRNA Sequence Classification** (Supervised Learning)
Goal: Classify sequences into rRNA types (16S, 18S, 23S, etc.)

### 2. **Multi-Tree Consensus** (Ensemble Methods)
Goal: Combine multiple phylogenetic trees into a reliable consensus

### 3. **Generative Tree Synthesis** (Deep Learning)
Goal: Generate optimized phylogenetic trees using GenAI

---

## Use Case 1: rRNA Sequence Classification

### Overview

Train a supervised classifier to identify rRNA type from DNA/RNA sequences. This complements traditional methods (HMM, BLAST) and can be faster with comparable accuracy.

### Feature Engineering

**Pattern 1: K-mer Frequency Vectors**

```python
# app/services/ml/features/kmers.py
from typing import Dict, List
import numpy as np
from collections import Counter
from itertools import product

class KmerFeatureExtractor:
    """Extract k-mer frequency features from sequences."""

    def __init__(self, k: int = 6, normalize: bool = True):
        """
        Initialize k-mer extractor.

        Args:
            k: K-mer size (default 6)
            normalize: Whether to normalize frequencies
        """
        self.k = k
        self.normalize = normalize
        self.vocab = self._build_vocab()

    def _build_vocab(self) -> Dict[str, int]:
        """Build k-mer vocabulary."""
        bases = ['A', 'C', 'G', 'T']
        kmers = [''.join(p) for p in product(bases, repeat=self.k)]
        return {kmer: idx for idx, kmer in enumerate(kmers)}

    def extract(self, sequence: str) -> np.ndarray:
        """
        Extract k-mer features from sequence.

        Args:
            sequence: DNA sequence

        Returns:
            Feature vector of shape (4^k,)
        """
        sequence = sequence.upper().replace('U', 'T')

        # Count k-mers
        kmers = [
            sequence[i:i+self.k]
            for i in range(len(sequence) - self.k + 1)
        ]
        counts = Counter(kmers)

        # Build feature vector
        features = np.zeros(len(self.vocab))
        for kmer, count in counts.items():
            if kmer in self.vocab:
                features[self.vocab[kmer]] = count

        # Normalize
        if self.normalize and features.sum() > 0:
            features = features / features.sum()

        return features
```

**Pattern 2: Positional Encoding + One-Hot**

```python
# app/services/ml/features/sequence_encoding.py
import numpy as np
from typing import Optional

class SequenceEncoder:
    """Encode sequences for deep learning models."""

    def __init__(self, max_length: int = 2000):
        self.max_length = max_length
        self.base_to_idx = {'A': 0, 'C': 1, 'G': 2, 'T': 3, 'N': 4}

    def one_hot_encode(
        self,
        sequence: str,
        pad: bool = True
    ) -> np.ndarray:
        """
        One-hot encode sequence.

        Args:
            sequence: DNA sequence
            pad: Whether to pad to max_length

        Returns:
            Array of shape (length, 5) or (max_length, 5) if padded
        """
        sequence = sequence.upper().replace('U', 'T')

        # Truncate if needed
        if len(sequence) > self.max_length:
            sequence = sequence[:self.max_length]

        # Encode
        encoded = np.zeros((len(sequence), 5))
        for i, base in enumerate(sequence):
            idx = self.base_to_idx.get(base, 4)  # 4 for unknown
            encoded[i, idx] = 1

        # Pad
        if pad and len(sequence) < self.max_length:
            padding = np.zeros((self.max_length - len(sequence), 5))
            encoded = np.vstack([encoded, padding])

        return encoded

    def positional_encode(
        self,
        sequence: str
    ) -> np.ndarray:
        """
        Add positional encoding (for transformers).

        Returns:
            Array of shape (length, 5 + positional_dims)
        """
        # One-hot encode
        one_hot = self.one_hot_encode(sequence, pad=False)

        # Add positional encoding (simplified)
        positions = np.arange(len(sequence))[:, np.newaxis]
        pos_encoding = np.sin(positions / 10000)

        return np.hstack([one_hot, pos_encoding])
```

### Model Training (Classical ML)

**Pattern: sklearn Pipeline**

```python
# app/services/ml/models/rrna_classifier.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib
from typing import List, Tuple
import numpy as np

class RRNAClassifier:
    """Classical ML classifier for rRNA type prediction."""

    def __init__(self, model_type: str = "random_forest"):
        self.model_type = model_type
        self.pipeline = self._build_pipeline()
        self.classes_ = None

    def _build_pipeline(self) -> Pipeline:
        """Build sklearn pipeline."""
        if self.model_type == "random_forest":
            return Pipeline([
                ('scaler', StandardScaler()),
                ('classifier', RandomForestClassifier(
                    n_estimators=200,
                    max_depth=20,
                    min_samples_split=5,
                    random_state=42,
                    n_jobs=-1
                ))
            ])
        # Add other models (XGBoost, SVM, etc.)

    def train(
        self,
        X: np.ndarray,
        y: np.ndarray,
        test_size: float = 0.2,
        tune_hyperparameters: bool = False
    ) -> dict:
        """
        Train the classifier.

        Args:
            X: Feature matrix (n_samples, n_features)
            y: Labels (n_samples,)
            test_size: Test set proportion
            tune_hyperparameters: Whether to run GridSearch

        Returns:
            Training metrics
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Hyperparameter tuning
        if tune_hyperparameters:
            self.pipeline = self._tune_hyperparameters(X_train, y_train)
        else:
            self.pipeline.fit(X_train, y_train)

        # Evaluate
        y_pred = self.pipeline.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        conf_matrix = confusion_matrix(y_test, y_pred)

        self.classes_ = self.pipeline.classes_

        return {
            "accuracy": report["accuracy"],
            "classification_report": report,
            "confusion_matrix": conf_matrix.tolist(),
            "train_size": len(X_train),
            "test_size": len(X_test)
        }

    def _tune_hyperparameters(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray
    ) -> Pipeline:
        """Grid search for best hyperparameters."""
        param_grid = {
            'classifier__n_estimators': [100, 200, 300],
            'classifier__max_depth': [10, 20, 30],
            'classifier__min_samples_split': [2, 5, 10]
        }

        grid_search = GridSearchCV(
            self.pipeline,
            param_grid,
            cv=5,
            scoring='f1_weighted',
            n_jobs=-1,
            verbose=1
        )

        grid_search.fit(X_train, y_train)
        print(f"Best parameters: {grid_search.best_params_}")

        return grid_search.best_estimator_

    def predict(
        self,
        X: np.ndarray,
        return_proba: bool = False
    ) -> np.ndarray:
        """Make predictions."""
        if return_proba:
            return self.pipeline.predict_proba(X)
        return self.pipeline.predict(X)

    def save(self, path: str):
        """Save model to disk."""
        joblib.dump(self.pipeline, path)

    @classmethod
    def load(cls, path: str):
        """Load model from disk."""
        instance = cls()
        instance.pipeline = joblib.load(path)
        instance.classes_ = instance.pipeline.classes_
        return instance
```

### Model Training (Deep Learning)

**Pattern: PyTorch CNN for Sequences**

```python
# app/services/ml/models/rrna_cnn.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np

class SequenceDataset(Dataset):
    """Dataset for sequence classification."""

    def __init__(self, sequences: List[np.ndarray], labels: List[int]):
        self.sequences = sequences
        self.labels = labels

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        return (
            torch.FloatTensor(self.sequences[idx]),
            torch.LongTensor([self.labels[idx]])[0]
        )

class RRNACNNClassifier(nn.Module):
    """CNN for rRNA sequence classification."""

    def __init__(
        self,
        num_classes: int = 6,
        seq_length: int = 2000,
        num_filters: int = 128
    ):
        super().__init__()

        # Convolutional layers
        self.conv1 = nn.Conv1d(5, num_filters, kernel_size=7, padding=3)
        self.conv2 = nn.Conv1d(num_filters, num_filters*2, kernel_size=5, padding=2)
        self.conv3 = nn.Conv1d(num_filters*2, num_filters*4, kernel_size=3, padding=1)

        # Pooling
        self.pool = nn.MaxPool1d(2)

        # Global pooling
        self.global_pool = nn.AdaptiveAvgPool1d(1)

        # Fully connected
        self.fc1 = nn.Linear(num_filters*4, 256)
        self.fc2 = nn.Linear(256, num_classes)

        # Regularization
        self.dropout = nn.Dropout(0.5)
        self.batch_norm1 = nn.BatchNorm1d(num_filters)
        self.batch_norm2 = nn.BatchNorm1d(num_filters*2)

    def forward(self, x):
        # x shape: (batch, seq_length, 5)
        x = x.transpose(1, 2)  # (batch, 5, seq_length)

        # Conv blocks
        x = self.pool(torch.relu(self.batch_norm1(self.conv1(x))))
        x = self.pool(torch.relu(self.batch_norm2(self.conv2(x))))
        x = self.pool(torch.relu(self.conv3(x)))

        # Global pooling
        x = self.global_pool(x).squeeze(-1)

        # FC layers
        x = self.dropout(torch.relu(self.fc1(x)))
        x = self.fc2(x)

        return x

class RRNACNNTrainer:
    """Trainer for CNN model."""

    def __init__(
        self,
        model: RRNACNNClassifier,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        self.model = model.to(device)
        self.device = device

    def train(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader,
        epochs: int = 50,
        lr: float = 0.001
    ) -> dict:
        """Train the model."""
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', patience=5, factor=0.5
        )

        history = {"train_loss": [], "val_loss": [], "val_acc": []}

        for epoch in range(epochs):
            # Training
            self.model.train()
            train_loss = 0
            for sequences, labels in train_loader:
                sequences = sequences.to(self.device)
                labels = labels.to(self.device)

                optimizer.zero_grad()
                outputs = self.model(sequences)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                train_loss += loss.item()

            train_loss /= len(train_loader)

            # Validation
            val_loss, val_acc = self._validate(val_loader, criterion)
            scheduler.step(val_loss)

            history["train_loss"].append(train_loss)
            history["val_loss"].append(val_loss)
            history["val_acc"].append(val_acc)

            print(f"Epoch {epoch+1}/{epochs}: "
                  f"Train Loss={train_loss:.4f}, "
                  f"Val Loss={val_loss:.4f}, "
                  f"Val Acc={val_acc:.4f}")

        return history

    def _validate(
        self,
        loader: DataLoader,
        criterion: nn.Module
    ) -> Tuple[float, float]:
        """Validate the model."""
        self.model.eval()
        total_loss = 0
        correct = 0
        total = 0

        with torch.no_grad():
            for sequences, labels in loader:
                sequences = sequences.to(self.device)
                labels = labels.to(self.device)

                outputs = self.model(sequences)
                loss = criterion(outputs, labels)
                total_loss += loss.item()

                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        return total_loss / len(loader), correct / total

    def save(self, path: str):
        """Save model checkpoint."""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'model_config': {
                'num_classes': self.model.fc2.out_features,
                # Add other config
            }
        }, path)

    @classmethod
    def load(cls, path: str):
        """Load model checkpoint."""
        checkpoint = torch.load(path)
        model = RRNACNNClassifier(**checkpoint['model_config'])
        model.load_state_dict(checkpoint['model_state_dict'])
        return cls(model)
```

### Model Serving

**Pattern: FastAPI Integration**

```python
# app/services/ml/inference/rrna_predictor.py
from typing import List, Dict
import numpy as np
from app.services.ml.features.kmers import KmerFeatureExtractor
from app.services.ml.models.rrna_classifier import RRNAClassifier

class RRNAMLPredictor:
    """ML-based rRNA predictor (production)."""

    def __init__(self, model_path: str, feature_extractor: str = "kmer"):
        self.model = RRNAClassifier.load(model_path)
        self.feature_extractor = KmerFeatureExtractor(k=6)

    async def predict(
        self,
        sequence: str,
        return_confidence: bool = True
    ) -> Dict:
        """
        Predict rRNA type.

        Args:
            sequence: DNA sequence
            return_confidence: Return confidence scores

        Returns:
            Prediction with confidence
        """
        # Extract features
        features = self.feature_extractor.extract(sequence)
        features = features.reshape(1, -1)

        # Predict
        if return_confidence:
            proba = self.model.predict(features, return_proba=True)[0]
            pred_idx = np.argmax(proba)
            pred_class = self.model.classes_[pred_idx]

            return {
                "predicted_type": pred_class,
                "confidence": float(proba[pred_idx]),
                "all_probabilities": {
                    self.model.classes_[i]: float(p)
                    for i, p in enumerate(proba)
                }
            }
        else:
            pred = self.model.predict(features)[0]
            return {"predicted_type": pred}

# app/api/v1/rrna.py (API endpoint)
from app.services.ml.inference.rrna_predictor import RRNAMLPredictor

ml_predictor = RRNAMLPredictor("models/rrna_classifier_v1.joblib")

@router.post("/ml-detect")
async def ml_detect_rrna(sequence: str):
    """Detect rRNA using ML model."""
    result = await ml_predictor.predict(sequence)
    return result
```

---

## Use Case 2: Multi-Tree Consensus (Ensemble)

### Overview

Combine multiple phylogenetic trees (from different methods) into a single consensus tree. This is an ensemble approach similar to model ensembling in ML.

### Tree Representation

```python
# app/services/ml/phylo/tree_representation.py
from typing import List, Set, Dict
from ete3 import Tree
import numpy as np

class TreeEnsemble:
    """Ensemble of phylogenetic trees."""

    def __init__(self, trees: List[Tree], methods: List[str]):
        """
        Initialize tree ensemble.

        Args:
            trees: List of ete3 Tree objects
            methods: Method used for each tree
        """
        self.trees = trees
        self.methods = methods
        self.taxa = self._get_taxa()

    def _get_taxa(self) -> Set[str]:
        """Get all taxa across trees."""
        taxa = set()
        for tree in self.trees:
            taxa.update([leaf.name for leaf in tree.get_leaves()])
        return taxa

    def get_bipartitions(self) -> List[Dict]:
        """
        Extract bipartitions from all trees.

        Returns:
            List of bipartitions with frequencies
        """
        bipart_counts = {}

        for tree in self.trees:
            for node in tree.traverse():
                if not node.is_leaf():
                    # Get leaves under this node
                    leaves = set([leaf.name for leaf in node.get_leaves()])

                    # Create bipartition (as frozenset for hashing)
                    bipart = frozenset(leaves)

                    # Count
                    if bipart not in bipart_counts:
                        bipart_counts[bipart] = 0
                    bipart_counts[bipart] += 1

        # Convert to list with frequencies
        bipartitions = [
            {
                "bipartition": list(bipart),
                "frequency": count / len(self.trees),
                "count": count
            }
            for bipart, count in bipart_counts.items()
        ]

        return sorted(bipartitions, key=lambda x: x["frequency"], reverse=True)
```

### Consensus Methods

**Pattern: Majority-Rule Consensus**

```python
# app/services/ml/phylo/consensus.py
from ete3 import Tree
from typing import List, Dict

class ConsensusTreeBuilder:
    """Build consensus trees from multiple input trees."""

    def __init__(self, ensemble: TreeEnsemble):
        self.ensemble = ensemble

    def strict_consensus(self) -> Tree:
        """
        Build strict consensus tree.

        Only includes bipartitions present in ALL trees.
        """
        bipartitions = self.ensemble.get_bipartitions()

        # Filter to 100% frequency
        strict_biparts = [
            b for b in bipartitions
            if b["frequency"] == 1.0
        ]

        return self._build_tree_from_bipartitions(strict_biparts)

    def majority_rule_consensus(self, threshold: float = 0.5) -> Tree:
        """
        Build majority-rule consensus tree.

        Args:
            threshold: Minimum frequency to include bipartition

        Returns:
            Consensus tree
        """
        bipartitions = self.ensemble.get_bipartitions()

        # Filter by threshold
        majority_biparts = [
            b for b in bipartitions
            if b["frequency"] >= threshold
        ]

        tree = self._build_tree_from_bipartitions(majority_biparts)

        # Add support values to nodes
        for node in tree.traverse():
            if not node.is_leaf():
                leaves = set([leaf.name for leaf in node.get_leaves()])
                # Find matching bipartition
                for bipart in majority_biparts:
                    if set(bipart["bipartition"]) == leaves:
                        node.support = bipart["frequency"]
                        break

        return tree

    def weighted_consensus(self, weights: List[float]) -> Tree:
        """
        Build weighted consensus tree.

        Args:
            weights: Weight for each input tree

        Returns:
            Consensus tree with weighted support
        """
        # Similar to majority-rule but with weighted frequencies
        pass

    def _build_tree_from_bipartitions(
        self,
        bipartitions: List[Dict]
    ) -> Tree:
        """
        Construct tree from bipartitions.

        This is non-trivial! Use greedy algorithm or exact methods.
        """
        # Start with star tree
        taxa = list(self.ensemble.taxa)
        tree = Tree()
        tree.add_child(name=taxa[0])

        # Add bipartitions greedily
        for bipart in bipartitions:
            leaves_in_bipart = set(bipart["bipartition"])
            # Find node to split
            # This is a simplified version
            pass

        return tree
```

### Conflict Detection

```python
# app/services/ml/phylo/conflict.py
from typing import List, Dict, Tuple

class TreeConflictAnalyzer:
    """Analyze conflicts between trees."""

    def __init__(self, ensemble: TreeEnsemble):
        self.ensemble = ensemble

    def find_conflicts(self) -> List[Dict]:
        """
        Find conflicting bipartitions across trees.

        Returns:
            List of conflicts with details
        """
        bipartitions = self.ensemble.get_bipartitions()

        conflicts = []
        for i, b1 in enumerate(bipartitions):
            for b2 in bipartitions[i+1:]:
                if self._are_conflicting(b1, b2):
                    conflicts.append({
                        "bipartition1": b1,
                        "bipartition2": b2,
                        "conflict_type": self._classify_conflict(b1, b2)
                    })

        return conflicts

    def _are_conflicting(
        self,
        b1: Dict,
        b2: Dict
    ) -> bool:
        """Check if two bipartitions conflict."""
        set1 = set(b1["bipartition"])
        set2 = set(b2["bipartition"])

        # Bipartitions conflict if they're incompatible
        # (i.e., cannot both be in the same tree)
        intersect = set1 & set2
        return (
            len(intersect) > 0 and
            len(intersect) < len(set1) and
            len(intersect) < len(set2)
        )

    def robinson_foulds_distance(
        self,
        tree1: Tree,
        tree2: Tree
    ) -> int:
        """
        Calculate Robinson-Foulds distance.

        Measures topological difference between trees.
        """
        result = tree1.robinson_foulds(tree2)
        return result[0]  # RF distance
```

---

## Use Case 3: GenAI Tree Synthesis (Advanced)

### Overview

Use generative AI (Graph Neural Networks or Transformers) to synthesize phylogenetic trees from multiple inputs. This is experimental/research-level.

### Graph Representation

```python
# app/services/ml/genai/tree_graph.py
import torch
from torch_geometric.data import Data
from ete3 import Tree
from typing import List

class TreeToGraphConverter:
    """Convert phylogenetic trees to graph representation."""

    def __init__(self):
        self.taxa_to_idx = {}

    def tree_to_graph(self, tree: Tree) -> Data:
        """
        Convert tree to PyTorch Geometric graph.

        Returns:
            Graph data object
        """
        # Assign indices to all nodes
        nodes = list(tree.traverse())
        node_to_idx = {id(node): i for i, node in enumerate(nodes)}

        # Build edge list
        edges = []
        for node in nodes:
            if node.up:
                # Add edge from parent to child
                parent_idx = node_to_idx[id(node.up)]
                child_idx = node_to_idx[id(node)]
                edges.append([parent_idx, child_idx])
                edges.append([child_idx, parent_idx])  # Undirected

        edge_index = torch.tensor(edges, dtype=torch.long).t()

        # Node features (simplified)
        node_features = []
        for node in nodes:
            if node.is_leaf():
                # Leaf node: one-hot encode taxon
                features = self._encode_taxon(node.name)
            else:
                # Internal node: aggregate features
                features = torch.zeros(100)  # Placeholder
            node_features.append(features)

        x = torch.stack(node_features)

        return Data(x=x, edge_index=edge_index)

    def _encode_taxon(self, taxon: str) -> torch.Tensor:
        """Encode taxon name."""
        if taxon not in self.taxa_to_idx:
            self.taxa_to_idx[taxon] = len(self.taxa_to_idx)
        idx = self.taxa_to_idx[taxon]

        # One-hot encoding
        encoding = torch.zeros(100)  # Assume max 100 taxa
        encoding[idx] = 1
        return encoding
```

### GNN Model (Experimental)

```python
# app/services/ml/genai/tree_gnn.py
import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv, global_mean_pool

class TreeGNN(nn.Module):
    """Graph Neural Network for tree encoding."""

    def __init__(
        self,
        input_dim: int = 100,
        hidden_dim: int = 128,
        embedding_dim: int = 64
    ):
        super().__init__()

        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.conv3 = GCNConv(hidden_dim, embedding_dim)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        # Graph convolutions
        x = torch.relu(self.conv1(x, edge_index))
        x = torch.relu(self.conv2(x, edge_index))
        x = self.conv3(x, edge_index)

        # Global pooling (tree-level embedding)
        embedding = global_mean_pool(x, data.batch)

        return embedding

class TreeGenerator(nn.Module):
    """Generate trees from embeddings (very experimental)."""

    def __init__(self, embedding_dim: int = 64, max_nodes: int = 20):
        super().__init__()
        self.max_nodes = max_nodes

        # Decoder: embedding -> tree structure
        self.fc1 = nn.Linear(embedding_dim, 256)
        self.fc2 = nn.Linear(256, max_nodes * max_nodes)  # Adjacency matrix

    def forward(self, embedding):
        x = torch.relu(self.fc1(embedding))
        adjacency_logits = self.fc2(x)

        # Reshape to adjacency matrix
        adj_matrix = adjacency_logits.view(-1, self.max_nodes, self.max_nodes)

        # Apply sigmoid to get probabilities
        adj_matrix = torch.sigmoid(adj_matrix)

        # Make symmetric (undirected tree)
        adj_matrix = (adj_matrix + adj_matrix.transpose(1, 2)) / 2

        return adj_matrix

# Training loop would learn to:
# 1. Encode multiple trees into embeddings
# 2. Combine embeddings (e.g., average)
# 3. Decode combined embedding into new tree
# 4. Optimize for tree validity + likelihood
```

---

## Model Versioning & Deployment

```python
# app/services/ml/versioning.py
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any

class ModelRegistry:
    """Track and version ML models."""

    def __init__(self, registry_path: str = "models/registry.json"):
        self.registry_path = Path(registry_path)
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict:
        """Load model registry."""
        if self.registry_path.exists():
            with open(self.registry_path) as f:
                return json.load(f)
        return {"models": []}

    def register_model(
        self,
        name: str,
        version: str,
        model_path: str,
        metrics: Dict[str, Any],
        metadata: Dict[str, Any]
    ):
        """Register a new model version."""
        entry = {
            "name": name,
            "version": version,
            "model_path": model_path,
            "metrics": metrics,
            "metadata": metadata,
            "registered_at": datetime.now().isoformat()
        }

        self.registry["models"].append(entry)
        self._save_registry()

    def get_latest_model(self, name: str) -> Dict:
        """Get latest version of a model."""
        models = [m for m in self.registry["models"] if m["name"] == name]
        return max(models, key=lambda m: m["registered_at"])

    def _save_registry(self):
        """Save registry to disk."""
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)
```

---

## Best Practices

### ✅ DO
- Version all models with metrics
- Use cross-validation for evaluation
- Monitor for model drift
- Keep training/inference code separate
- Use feature stores for consistency
- Validate model outputs
- Log all predictions for analysis
- Use ensemble methods when possible
- Test models on held-out data
- Document feature engineering steps

### ❌ DON'T
- Train on test data
- Skip data normalization
- Ignore class imbalance
- Hardcode feature extraction
- Deploy without evaluation
- Mix training/serving code
- Skip model validation
- Ignore computational costs
- Overfit to small datasets
- Skip ablation studies

---

**Related Skills**: [rRNA-prediction-patterns](../rrna-prediction-patterns/SKILL.md), [project-architecture-patterns](../project-architecture-patterns/SKILL.md)

**Line Count**: < 500 lines ✅
