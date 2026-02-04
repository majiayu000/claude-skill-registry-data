---
name: tree-traversal
description: Master tree traversal techniques including DFS (inorder, preorder, postorder) and BFS level-order traversal with production-ready implementations.
sasmp_version: "1.3.0"
bonded_agent: 02-trees-binary
bond_type: PRIMARY_BOND

# Production-Grade Skill Specifications (2025)
atomic_responsibility: tree_traversal_execution
version: "2.0.0"

parameter_validation:
  strict: true
  rules:
    - name: root
      type: TreeNode
      required: true
      nullable: true
    - name: target
      type: integer
      required: false

retry_logic:
  max_attempts: 3
  backoff_ms: [100, 200, 400]
  retryable_errors:
    - recursion_depth
    - timeout

logging_hooks:
  on_start: true
  on_complete: true
  on_error: true
  log_format: "[TRE-SKILL] {timestamp} | {operation} | {status}"

complexity_annotations:
  inorder:
    time: "O(n)"
    space: "O(h) recursive, O(n) iterative worst"
  preorder:
    time: "O(n)"
    space: "O(h)"
  postorder:
    time: "O(n)"
    space: "O(h)"
  level_order:
    time: "O(n)"
    space: "O(w) where w = max width"
---

# Tree Traversal Skill

**Atomic Responsibility**: Execute tree traversal algorithms with correct order and optimal space.

## Tree Node Definition

```python
from typing import Optional, List
from collections import deque

class TreeNode:
    """Standard binary tree node."""
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right
```

## DFS - Inorder (Left, Root, Right)

```python
def inorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """
    Inorder traversal - gives sorted order for BST.

    Time: O(n), Space: O(h) where h = height

    Args:
        root: Root of binary tree

    Returns:
        List of values in inorder sequence
    """
    result = []

    def dfs(node: Optional[TreeNode]) -> None:
        if not node:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)

    dfs(root)
    return result


def inorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    Iterative inorder using explicit stack.

    Time: O(n), Space: O(h)
    Use when: Recursion depth might exceed limit.
    """
    result = []
    stack = []
    current = root

    while current or stack:
        # Go left as far as possible
        while current:
            stack.append(current)
            current = current.left

        # Process current node
        current = stack.pop()
        result.append(current.val)

        # Move to right subtree
        current = current.right

    return result
```

## DFS - Preorder (Root, Left, Right)

```python
def preorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """
    Preorder traversal - useful for tree serialization.

    Time: O(n), Space: O(h)
    """
    if not root:
        return []

    return ([root.val] +
            preorder_recursive(root.left) +
            preorder_recursive(root.right))


def preorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    Iterative preorder using stack.

    Note: Push right first, then left (LIFO).
    """
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)

        # Right first (so left is processed first)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result
```

## DFS - Postorder (Left, Right, Root)

```python
def postorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """
    Postorder traversal - useful for deletion, expression evaluation.

    Time: O(n), Space: O(h)
    """
    if not root:
        return []

    return (postorder_recursive(root.left) +
            postorder_recursive(root.right) +
            [root.val])


def postorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    Iterative postorder using two stacks or modified preorder.

    Trick: Modified preorder (root, right, left) then reverse.
    """
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)

        # Left first (so right is processed first after reverse)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    return result[::-1]  # Reverse to get postorder
```

## BFS - Level Order Traversal

```python
def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Level-by-level traversal using queue.

    Time: O(n), Space: O(w) where w = max width

    Returns:
        List of levels, each level is a list of values
    """
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result


def zigzag_level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Level order with alternating direction.

    Time: O(n), Space: O(w)
    """
    if not root:
        return []

    result = []
    queue = deque([root])
    left_to_right = True

    while queue:
        level_size = len(queue)
        level = deque()

        for _ in range(level_size):
            node = queue.popleft()

            if left_to_right:
                level.append(node.val)
            else:
                level.appendleft(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(list(level))
        left_to_right = not left_to_right

    return result
```

## BST Validation

```python
def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    Validate if tree is a valid Binary Search Tree.

    Time: O(n), Space: O(h)

    Property: All left descendants < node < all right descendants
    """
    def validate(node: Optional[TreeNode],
                 min_val: float,
                 max_val: float) -> bool:
        if not node:
            return True

        if not (min_val < node.val < max_val):
            return False

        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))

    return validate(root, float('-inf'), float('inf'))
```

## Unit Test Template

```python
import pytest

class TestTreeTraversal:
    """Unit tests for tree traversal implementations."""

    @pytest.fixture
    def sample_tree(self):
        """Create sample tree: 1 -> (2, 3) -> ((4, 5), None)"""
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        return root

    def test_inorder(self, sample_tree):
        assert inorder_recursive(sample_tree) == [4, 2, 5, 1, 3]
        assert inorder_iterative(sample_tree) == [4, 2, 5, 1, 3]

    def test_preorder(self, sample_tree):
        assert preorder_recursive(sample_tree) == [1, 2, 4, 5, 3]

    def test_postorder(self, sample_tree):
        assert postorder_recursive(sample_tree) == [4, 5, 2, 3, 1]

    def test_level_order(self, sample_tree):
        assert level_order(sample_tree) == [[1], [2, 3], [4, 5]]

    def test_empty_tree(self):
        assert inorder_recursive(None) == []
        assert level_order(None) == []

    def test_single_node(self):
        root = TreeNode(1)
        assert inorder_recursive(root) == [1]
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| RecursionError | Deep tree | Use iterative version |
| Wrong order | Processing order incorrect | Verify left/right/root sequence |
| Missing nodes | Not checking None | Add `if not node: return` |
| Stack overflow | Very unbalanced tree | Convert to iterative |

### Debug Checklist
```
□ Null root handled?
□ Base case returns correct value?
□ Both children processed?
□ Return value accumulated correctly?
□ Stack/queue order correct?
□ Tested with single node and empty tree?
```
