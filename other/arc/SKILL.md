---
name: arc
description: Personal arc guidelines. Use when working with arc (automation tool, arc.lua files).
---

When working with `arc` (automation tool, `arc.lua` files), fetch and read the README from https://github.com/myfavshrimp/arc before making any changes.

When writing `arc.lua` automation, follow the idiomatic patterns:

- Use `important = true` tasks for detection/checks that return results.
- Use `when` guards on dependent tasks to read prior task results (e.g., `when = function() return tasks["detect_os"].result == "linux" end`).
- Avoid parsing `system:run_command` stdout for control flow. Either use shell substitution inline (e.g., `$(brew --prefix openssl@3)`) or model the check as a check task that returns a value.
- Use `arc.project_root_path` to locate paths relative to the `arc.lua` location.

**Example:**

```lua
tasks["check_postgres_running"] = {
    important = true,
    handler = function(system)
        return system:run_command("pg_isready").exit_code == 0
    end,
}

tasks["start_postgres"] = {
    requires = {"check_postgres_running"},
    when = function() return tasks["check_postgres_running"].result == false end,
    handler = function(system)
        system:run_command("systemctl start postgresql")
    end,
}
```

In `arc.lua`, when an operation naturally fans out across a collection (multiple Docker images, multiple services, multiple files to render), prefer **one task that iterates internally** over generating N tasks via a `for ... do tasks[...] = {...} end` block.

**Yes:**

```lua
tasks["build_images"] = {
    handler = function()
        for _, image in ipairs(config.images) do
            host:run_command("docker build -t " .. image.name .. " ...")
        end
    end,
    tags = {"build"},
}
```

**No:**

```lua
for _, image in ipairs(config.images) do
    tasks["build_" .. image.name] = {
        handler = function() ... end,
        tags = {"build"},
    }
end
```

The single-task form keeps the task list short, makes run order obvious, and reduces dependency-edge clutter. Only split into per-item tasks if the items legitimately need independent run/skip/`requires` logic.
