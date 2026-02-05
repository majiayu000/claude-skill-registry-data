---
name: Ruby Information
description: When you need check documentation about Ruby classes, modules, and methods use this skill to get full details. Avoid check source code or use `ruby -e` for documentation unless absolutely necessary.
allowed-tools: Bash(ri:*), Bash(which ri), Task, Bash(head:*), Bash(wc:*), Bash(grep:*)
---

# Ruby Information

Use the `ri` command to access Ruby documentation which is installed locally on your system.

## Instructions

Use `ri [options] <whatever>` to look up information about Ruby classes, modules, and methods.

- Combine with `head` to fast check documentation before displaying full content.
- Combine with `wc` to count relevant items when searching for multiple entries.
- Combine with `grep` to filter results based on keywords.

Consider to add quote to queries with special characters to avoid shell interpretation issues. e.g. `ri 'String#blank?'`

## Scenarios

### Direct Lookup

Check specific Ruby classes or methods accurately.

```bash
ri Array#push
```

### Search method

Check for methods is implemetned in a class or module and get a count of results.

```bash
ri '.find' | wc -l
```

Use grep to filter results.

```bash
ri '.find' | grep 'Enumerable'
```

> Note: Use `wc` and `grep` to ensure the output is concise and relevant.

### List Names

Get a list of all classes and modules under a specific namespace.

```bash
ri --list 'MyModule::Application'
```

### Preview Documentation

Preview the first few lines of documentation for a method or class.

```bash
ri 'String#upcase' | head -n 10
```

### Explore Options

Explore various options available with the `ri` command.

```bash
ri --help
```

## Documentation

You can get README and other documentation if bundled with gems.

```bash
ri rspec:README.md
```

To list all available documentation files for a gem:

```bash
ri rspec:
```

Append the `:` after the gem name to see all documentation files associated with that gem.

## Building Documentation

You can use `rdoc` to generate and view documentation for your own Ruby projects.

```bash
rdoc --format=ri --output=ri_doc .
```

View the generated documentation using `ri`:

```bash
ri -d ./ri_doc 'MyClass'
```

## References

For more information, refer to the official Ruby documentation: [https://ruby.github.io/rdoc/index.html](https://ruby.github.io/rdoc/index.html)
