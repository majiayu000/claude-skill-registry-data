---
name: add-mcp-tool
description: Add an MCP tool to the Lodestone editor, so AI agents can use a new editor feature - the tool's schema and handler, the command it runs, and its in-process tests. Use whenever an editor-facing feature lands (every editor action needs an MCP tool), or when an agent needs something the tools can't do.
---

# Add an MCP Tool

Everything a person can do in the editor, an agent must be able to do through MCP (see `docs/AIControl.md` and `docs/Decisions/0016-mcp-server.md`). Components don't need tools: the generic component tools cover every registered component. Tools are for features that aren't components - play mode, screenshots, export, multiplayer, and so on.

## 1. Put the behaviour in the editor context or a command
- Anything that changes a document is a `Command` (`Source/Editor/Lodestone/Editor/Commands`), run through `EditorContext::Execute()`, so it can be undone and the UI can use it too. It must change nothing when it fails, and give the same result - UUIDs included - when redone
- Anything else that the UI also does (opening documents, play mode) is a method on `EditorContext`, so the UI and MCP share it. Tools stay thin

## 2. Register the tool
In `Source/Editor/Lodestone/Editor/Mcp/EditorTools.cpp`, in the `Add...Tools()` function for its area:
```cpp
server.AddTool({.Name = "light_bake",
	.Title = "Bake lighting",
	.Description = "Bakes the open scene's lighting. Returns how long it took",
	.InputSchema = Schema(R"({"type": "object", "properties": {
		"quality": {"type": "string", "enum": ["draft", "final"], "description": "draft by default"}}})"),
	.Handler = [&context](const Json::Value& json)
	{
		const auto quality = Arguments(json).OptionalString("quality");
		if (!quality)
			return Fail(quality.error());
		...
		return McpToolResult::Structured({{"seconds", seconds}});
	}});
```
- Names are `snake_case`, `<area>_<verb>`. The schema is a JSON Schema object with a description for anything that isn't obvious; required arguments are listed in `required`
- Read arguments with `Arguments`, which reports which argument is wrong. Return `Fail(error)` or `McpToolResult::Failure()` for anything the agent can fix - never throw, and never assert on agent input
- Set `ReadOnly` for tools that only read, and `Destructive` for tools that delete or discard. Tools that replace the open document check `CheckUnsaved()` and take `discardChanges`
- Return structured content for data (`McpToolResult::Structured`), `Run()` for commands (it reports what was done), and `McpToolResult::Image` for images
- Paths go through `EditorContext::ResolveAssetPath()`, which keeps them inside the project's `Assets` directory
- Work on the main thread only - tool handlers already run there

## 3. Test it
In `Tests/Editor/EditorToolsTests.cpp`:
- Add the name to `ToolNames` (the inventory test fails until you do, and the bad-arguments test then calls the tool with junk)
- A test case per tool: success, the result's content, the effect on the editor, undo where it's a command, and every failure an agent can cause
- If the feature changes what an agent's whole workflow looks like, extend `Tests/Editor/McpAgentSmokeTest.py`

## 4. Document it
Add it to the tool table in `docs/AIControl.md#tools`.
