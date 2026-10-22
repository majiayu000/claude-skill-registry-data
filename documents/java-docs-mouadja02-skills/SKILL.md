---
name: java-docs
description: >-
  Documents Java types with Javadoc following best practices: summary sentences, @param, @return,
  @throws, and documenting non-public members when complex. Use when Java APIs lack Javadoc or
  existing comments need improving.
license: MIT
source: "https://github.com/github/awesome-copilot"
attribution: "github/awesome-copilot by GitHub Community"
---

> **Attribution:** Sourced from [github/awesome-copilot](https://github.com/github/awesome-copilot) by [GitHub Community](https://github.com/github), licensed MIT. Modified for this collection.

# Java Documentation (Javadoc) Best Practices

- Public and protected members should be documented with Javadoc comments.
- It is encouraged to document package-private and private members as well, especially if they are complex or not self-explanatory.
- The first sentence of the Javadoc comment is the summary description. It should be a concise overview of what the method does and end with a period.
- Use `@param` for method parameters. The description starts with a lowercase letter and does not end with a period.
- Use `@return` for method return values.
- Use `@throws` or `@exception` to document exceptions thrown by methods.
- Use `@see` for references to other types or members.
- Use `{@inheritDoc}` to inherit documentation from base classes or interfaces.
  - Unless there is major behavior change, in which case you should document the differences.
- Use `@param <T>` for type parameters in generic types or methods.
- Use `{@code}` for inline code snippets.
- Use `<pre>{@code ... }</pre>` for code blocks.
- Use `@since` to indicate when the feature was introduced (e.g., version number).
- Use `@version` to specify the version of the member.
- Use `@author` to specify the author of the code.
- Use `@deprecated` to mark a member as deprecated and provide an alternative.
