---
name: vyper
description: Vyper compiler internals - AST nodes, type system, compilation pipeline, IR generation for debugging codegen bugs
compatibility: opencode
metadata:
  domain: ethereum
  language: vyper
---

# Vyper Compiler Skill

## Overview
Vyper is a Pythonic smart contract language for the EVM. The Vyper compiler transforms source code into EVM bytecode. In Ivy's differential fuzzing, we compare the compiled bytecode execution (via Boa) against Ivy's direct AST interpretation to find compiler bugs.

## Installation
Vyper is already installed in the project's `venv/`. Always activate before use:
```bash
source venv/bin/activate
```

## Reading Vyper Source Code
The Vyper compiler source is installed in the venv. To inspect it:
```bash
# Find vyper installation path
python -c "import vyper; print(vyper.__file__)"

# Typically at: venv/lib/python3.x/site-packages/vyper/
```

Key modules to understand:
- `vyper/ast/` - AST node definitions and parsing
- `vyper/semantics/` - Type system and semantic analysis
- `vyper/codegen/` - IR and bytecode generation
- `vyper/compiler/` - Compilation pipeline

## AST Structure
Vyper AST nodes are in `vyper.ast.nodes`. Key nodes:
```python
from vyper.ast import nodes as ast

# Statement nodes
ast.Assign, ast.AnnAssign, ast.If, ast.For, ast.Return
ast.Assert, ast.Raise, ast.Pass, ast.Break, ast.Continue

# Expression nodes  
ast.BinOp, ast.Compare, ast.BoolOp, ast.UnaryOp
ast.Call, ast.Subscript, ast.Attribute
ast.Name, ast.Int, ast.Str, ast.Bytes
```

## Type System
```python
from vyper.semantics.types import (
    IntegerT,      # int128, int256, uint8, uint256, etc.
    BoolT,         # bool
    AddressT,      # address
    BytesT,        # Bytes[N]
    StringT,       # String[N]
    DArrayT,       # DynArray[T, N]
    SArrayT,       # T[N] (static array)
    HashMapT,      # HashMap[K, V]
    StructT,       # struct definitions
    TupleT,        # tuples
)
```

## Compilation Pipeline
```python
from vyper.compiler import compile_code
from vyper.compiler.phases import CompilerData

# Get compiler data (AST, types, etc.)
compiler_data = CompilerData(source_code)

# Access annotated AST
annotated_ast = compiler_data.vyper_module

# Compile to bytecode
output = compile_code(source_code, output_formats=["bytecode", "abi"])
```

## Debugging Tips
- When a divergence occurs, check if it's a compiler codegen bug:
  - Compare the annotated AST against expected semantics
  - Check if the IR generation is correct
  - Verify bytecode matches IR intent
- Use `vyper.compile_code(src, output_formats=["ir"])` to inspect IR
- The `venom` pipeline (experimental) may have different bugs than legacy
