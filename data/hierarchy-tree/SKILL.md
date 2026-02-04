---
name: hierarchy-tree
description: Construct ASCII tree visualizations from parent/child work item data. Use when the user asks to "show hierarchy", "show tree", "display parent child", "visualize structure", "show feature tree", or wants to see work item relationships as a tree diagram. This skill teaches how to build trees from flat data WITHOUT code - use LLM reasoning only.
---

# Building ASCII Trees from Parent/Child Data

When you have flat parent/child data, construct the tree visually using LLM reasoning - NO CODE NEEDED.

## Step 1: Get the Data

Query work items with their parent:
```bash
az boards query --wiql "SELECT [System.Id], [System.Title] FROM workitems WHERE [System.WorkItemType] = 'Feature' AND [System.TeamProject] = 'ProjectName'" -o json
```

Then for each item, get its parent via relations (System.LinkTypes.Hierarchy-Reverse).

The result is flat data like:
```
ID     Parent   Title
1517   1509     Feature A
1518   1509     Feature B
1759   1827     Feature C
1827   1509     Feature D
```

## Step 2: Build the Tree (LLM Reasoning)

1. **Find roots** - Items whose Parent is not in the ID list (or is an Epic/external)
2. **Group children** - For each ID, collect all items where Parent = that ID
3. **Recurse** - Build subtrees for each child

From the example above:
- Root: 1509 (not in ID list as a child)
- 1509's children: 1517, 1518, 1827
- 1827's children: 1759

## Step 3: Render ASCII

Use these characters:
```
|   = vertical continuation (more siblings below)
|-- = branch to sibling (more siblings follow)
`-- = last branch (no more siblings)
    = indent (4 spaces under a last branch)
```

Rules:
- Each level indents 4 characters
- Use `|-- ` for all children except the last
- Use `` `-- `` for the last child
- Continue `|   ` vertically when parent has more siblings

## Example Transformation

**Input data:**
```
ID    Parent  Name
100   -       Root
200   100     Child A
300   100     Child B
400   300     Grandchild B1
500   300     Grandchild B2
600   100     Child C
```

**Output tree:**
```
#100 Root
|-- #200 Child A
|-- #300 Child B
|   |-- #400 Grandchild B1
|   `-- #500 Grandchild B2
`-- #600 Child C
```

## Complex Example

**Input:**
```
ID    Parent  Name
1     -       Epic
10    1       Feature A
11    1       Feature B
20    10      Sub A1
21    10      Sub A2
30    11      Sub B1
31    30      Deep B1a
32    30      Deep B1b
```

**Output:**
```
#1 Epic
|-- #10 Feature A
|   |-- #20 Sub A1
|   `-- #21 Sub A2
`-- #11 Feature B
    `-- #30 Sub B1
        |-- #31 Deep B1a
        `-- #32 Deep B1b
```

## Key Points

1. **Don't use code** - The LLM can construct this from data using reasoning
2. **Process top-down** - Start from roots, recurse into children
3. **Track "is last"** - Determines `|--` vs `` `-- ``
4. **Track depth** - Determines indentation and vertical bars
5. **Keep it clean** - Omit IDs if user prefers names only

## When to Use

- User asks for "tree view" or "hierarchy"
- User wants to see parent/child relationships
- Visualizing feature breakdown structures
- Showing Epic → Feature → PBI → Task relationships
