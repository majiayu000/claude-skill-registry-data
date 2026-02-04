---
name: generating-subtasks
description: Converts approved design documents into agent-executable XML subtasks. Use after a design doc is approved and ready for implementation.
---

<subtask_schema>
Agent-executable subtasks go in `design-docs/agents/<design-doc-name>.xml`.

**This file is generated ONLY after the user approves the human-readable subtasks in the main design doc.**
**IMPORTANT: If you have the user do not have subtask written in the markdown design doc, do NOT generate this file. You must generate the subtasks in the markdown file first, then wait for user instructions before continuing with building the XML file.**
The XML file wraps all tasks in a root element and follows this schema:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<design-doc-tasks>
  <metadata>
    <design-doc>YYYYMMDD-slug.md</design-doc>
    <created>YYYY-MM-DD</created>
    <approved-by>user</approved-by>
  </metadata>

  <task id="T1-slug" owner="unassigned" status="planned">
  <summary>One sentence objective.</summary>

  <scope>
    <in>Concrete inclusions.</in>
    <out>Concrete exclusions.</out>
  </scope>

  <reuse_check>
    <search_terms>
      <term>...</term>
    </search_terms>
    <existing_utilities>
      <candidate>path::symbol</candidate>
    </existing_utilities>
    <decision>reuse|extend|new</decision>
    <justification>Required if decision != reuse.</justification>
  </reuse_check>

  <interfaces>
    <exports>
      <function name="...">
        <signature>...</signature>
        <types>
          <param name="...">...</param>
          <returns>...</returns>
        </types>
        <invariants>
          <invariant>...</invariant>
        </invariants>
        <optionals>
          <allowed>false|true</allowed>
          <justification>Required if Optional/None exists.</justification>
        </optionals>
      </function>
    </exports>
  </interfaces>

  <implementation_plan>
    <step>...</step>
  </implementation_plan>

  <test_data>
    <required>true|false</required>
    <source>http|websocket|file|db|synthetic</source>
    <gap_analysis>What is missing vs required.</gap_analysis>
    <plan>Record/replay, generator, or harness.</plan>
    <fixture_paths>
      <path>tests/fixtures/...</path>
    </fixture_paths>
    <validation>
      <check>schema validation</check>
      <check>golden aggregates</check>
    </validation>
  </test_data>

  <tests>
    <add>
      <test_file>tests/.../test_*.py</test_file>
      <assertion>What this test proves.</assertion>
    </add>
    <update>
      <test_file>...</test_file>
      <change>...</change>
    </update>
  </tests>

  <commands>
    <cmd>...</cmd>
  </commands>

  <acceptance>
    <criterion>Binary "passes when ...".</criterion>
  </acceptance>
  <!-- IMPORTANT!!!: YOU MUST CHANGE task_completed_status TO TRUE WHEN THE TASK IS COMPLETE -->
  <task_completed_status>
  false
  </task_completed_status>
  <safety>
    <destructive_actions>false</destructive_actions>
    <notes>Any risk or confirmation requirements.</notes>
  </safety>
</task>

  <!-- Additional tasks follow the same structure -->
  <task id="T2-slug" owner="unassigned" status="planned">
    ...
  </task>

</design-doc-tasks>
```
</subtask_schema>
