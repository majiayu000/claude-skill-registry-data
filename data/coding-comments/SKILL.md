---
name: coding-comments
description: My personal best practices for writing clear and effective code comments.
---

# Coding Comments

## Gotchas

- When creating source code file top-level descriptions, do not use `//ABOUTME: <etc>` format. Instead, use Taylor Otwells commenting style (adapted to typescript comments, instead of php).

<EXAMPLE>

```
/*
|------------------------------------------------------------------------------
| Heading: How to write your code comments like Taylor
|------------------------------------------------------------------------------
|
| In Laravel, there are 598 three-line code comments. The first line of each
| is ~74 characters long. Each subsequent line has three characters fewer
| than the one above it. Whether trailing periods count is your choice. 
| 
| Descriptions proceeding the first very-specifically-formatted line can be
| any length you want, and can have multiple paragraphs.
|  - Also, optional dot points
|
*/
```

</EXAMPLE>