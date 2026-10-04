---
name: marketplace-test
description: Use when the user asks to "test the marketplace plugins", "run marketplace tests", "check every installed plugin", or "/ar:marketplace-test". Walks the installed marketplace plugins, finds each one's test suite, runs them from the plugin's own directory, and reports per-plugin results.
allowed-tools: Bash(uv *), Bash(git *), Bash(ls *), Bash(find *)
---

# Marketplace Plugin Testing

<purpose>

You are running tests for all installed Claude Code marketplace plugins to ensure they work correctly together.

## Your Task

Run the test suite for all plugins in the autorun marketplace that have tests, and provide a comprehensive report of the results.

</purpose>

<workflow>

## Steps

1. **List all marketplace plugins**
   ```bash
   ls -la ~/.claude/plugins/repos/
   ```

2. **Check which plugins have tests**
   ```bash
   for plugin in ~/.claude/plugins/repos/*; do
     if [ -d "$plugin/tests" ]; then
       echo "✓ $plugin has tests"
     fi
   done
   ```

3. **Run tests for each plugin with tests**
   ```bash
   for plugin_dir in ~/.claude/plugins/repos/*; do
     plugin_name=$(basename "$plugin_dir")

     # Check if plugin has tests
     if [ -d "$plugin_dir/tests" ]; then
       echo ""
       echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
       echo "Testing plugin: $plugin_name"
       echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

       # Change to plugin directory
       cd "$plugin_dir" || continue

       # Check if pytest.ini or pyproject.toml exists
       if [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
         # Run pytest with verbose output
         echo "Running pytest..."
         uv run python -m pytest tests/ -v --tb=short

         # Check exit code
         if [ $? -eq 0 ]; then
           echo "✅ $plugin_name: All tests PASSED"
         else
           echo "❌ $plugin_name: Some tests FAILED"
         fi
       else
         echo "⚠️  $plugin_name: No pytest configuration found"
       fi
     fi
   done
   ```

4. **Generate summary report**
   - Count total plugins tested
   - Count passed/failed
   - List any plugins with test failures
   - Report total test execution time

## Important Notes

- **Run in parallel when possible**: Use `pytest -n auto` for plugins that support it
- **Don't break active sessions**: Tests should use temporary directories only
- **Skip plugins without tests**: Only test plugins that have a `tests/` directory
- **Report test coverage**: If available, include coverage information
- **Check for UV compatibility**: Verify plugins use UV for dependency management

</workflow>

<output_contract>

## Example Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MARKETPLACE PLUGIN TEST REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Plugins tested: 3
Plugins with tests: 3
Plugins passed: 2
Plugins failed: 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ autorun: PASSED (15/15 tests)
✅ plan-export: PASSED (13/13 tests)
❌ pdf-extractor: FAILED (3/10 tests failed)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total execution time: 45.2s

Failed tests details:
- pdf-extractor/test_extraction.py::test_pdf_parse: FAILED
- pdf-extractor/test_extraction.py::test_metadata: FAILED
- pdf-extractor/test_extraction.py::test_unicode: FAILED
```

</output_contract>

<additional_checks>

## Additional Checks

For each plugin tested, also verify:
1. **pyproject.toml exists and has [tool.uv] section**
2. **pytest.ini or pytest configuration in pyproject.toml**
3. **tests/ directory with test_*.py files**
4. **README.md or tests/README.md documenting how to run tests**

</additional_checks>

<error_handling>

## Error Handling

If a plugin's tests fail to run (e.g., import errors, missing dependencies):
- Note the error in the report
- Continue testing other plugins
- Don't let one plugin's test failure stop the entire process

</error_handling>
