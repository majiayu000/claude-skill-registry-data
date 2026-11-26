---
name: ase-code-triage
argument-hint: "[--help|-h] [--why|-w] <cve-id>|<vulnerability-hint>"
description: >
    Triage whether the project of the current repository is affected by a
    vulnerability, given either by its CVE id or by a free-text security
    or vulnerability description, by consulting the published VEX status
    of the project, the CVE record or the Internet/Web, and the project
    artifacts, and emit an AFFECTED, NOT-AFFECTED, or INCONCLUSIVE
    verdict, optionally with a brief reason. Use when the user asks
    whether the project is "affected" by, "vulnerable" to, or "exposed"
    to a CVE or a vulnerability, or calls to "triage" one.
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Agent"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-code-triage">
Triage Vulnerability Exposure
</purpose>

<expand name="getopt"
    arg1="ase-code-triage"
    arg2="--why|-w">
    $ARGUMENTS
</expand>

<objective>
*Triage* whether the project of the current repository is *affected* by
a vulnerability and report the *triage verdict* `AFFECTED`,
`NOT-AFFECTED`, or `INCONCLUSIVE`.
</objective>

<define name="triage-fail">
Only output the following <template/> and then immediately *STOP*
processing the entire current skill:

<template>
⧉ **ASE**: ✪ skill: **ase-code-triage**, ▶ ERROR: <arg1/>, ▶ TRIAGE VERDICT: **INCONCLUSIVE**
</template>
</define>

<define name="triage-report">
Set <verdict><arg1/></verdict>. Under `--why`, set <justification/> to
a single VEX-style justification label of the verdict (like
`component_not_present`, `vulnerable_code_not_present`,
`vulnerable_code_not_in_execute_path`, `vulnerable_code_in_execute_path`,
or `insufficient_evidence`) and <reason/> to 1-2 very brief sentences
citing the decisive evidence (like VEX documents, dependency versions,
or code locations with their project-relative file paths). Then only
output the following <template/> and then immediately *STOP* processing
the entire current skill:

<if condition="<getopt-option-why/> is equal `true`">
<template>
<ase-tpl-boxed title="TRIAGE VERDICT" subtitle="<vuln-id/>">
**VULNERABILITY**: <vuln-title/>

**BASIS**: <basis/>

**VERDICT**: **<verdict/>**

**REASON**: `<justification/>`: <reason/>
</ase-tpl-boxed>
</template>
</if>
<else>
<template>
<ase-tpl-boxed title="TRIAGE VERDICT" subtitle="<vuln-id/>">
**VULNERABILITY**: <vuln-title/>

**BASIS**: <basis/>

**VERDICT**: **<verdict/>**
</ase-tpl-boxed>
</template>
</else>
</define>

Procedure
---------

<flow>

1.  <step id="STEP 1: Check Argument">

    Set <query/> to <getopt-arguments/> with any leading and trailing
    whitespace and any surrounding quotes stripped. Set <cve-id></cve-id>,
    <hint></hint>, <facts></facts>, and <vuln></vuln> (all empty). Do not
    output anything.

    <if condition="<query/> is empty">
    <expand name="triage-fail" arg1="expected a `<cve-id>` or `<vulnerability-hint>` argument"></expand>
    </if>

    <if condition="<query/> matches the case-insensitive regexp `^CVE-\d{4}-\d{4,}$`">
    Set <cve-id/> to <query/> in upper-case.
    </if>
    <else>
    Set <hint/> to <query/>.
    </else>

    </step>

2.  <step id="STEP 2: Match Hint" condition="<hint/> is not empty">

    1.  <if condition="<hint/> contains exactly one distinct match of the case-insensitive regexp `CVE-\d{4}-\d{4,}`">
        Set <cve-id/> to this match in upper-case and *skip* the
        remaining items of this step.
        </if>

    2.  Gather the facts on the vulnerability described by <hint/> through
        the following sub-agent, and store the returned facts in <facts/>:

        `Agent(
            description: "Query Web Search Service",
            subagent_type: "ase:ase-meta-search",
            prompt: "Search the Internet/Web and gather facts about the following security vulnerability: <hint/>. Especially, gather its CVE id(s), its title, its affected products, packages, and versions, its vulnerable functionality (functions, classes, modules, features, or configuration options), its exploitation preconditions, and its fixed versions.",
            run_in_background: false
        )`

    3.  <if condition="<facts/> name exactly *one* CVE id which unambiguously and confidently matches the vulnerability described by <hint/>">
        Set <cve-id/> to this CVE id in upper-case.
        </if>
        <else>
        Keep <cve-id/> empty, so the vulnerability is triaged by the
        free-text <hint/> and its <facts/> only.
        </else>
        Do not output anything.

    </step>

3.  <step id="STEP 3: Lookup VEX Status" condition="<cve-id/> is not empty">

    1.  Set <vuln-id><cve-id/></vuln-id> and
        <vuln-title><cve-id/></vuln-title>. Call the `ase_vex(id:
        "<cve-id/>", format: "json")` tool of the `ase` MCP server.
        Deviating from the generic MCP tool error handling, if its
        response `text` starts with `ERROR: <info/>`, expand:

        <expand name="triage-fail" arg1="<info/>"></expand>

    2.  Take the `verdict` of the returned record and its decisive first
        entry of `statements` (if any). Set <basis/> to the text
        "published VEX status <vex-verdict/> in <file/>", where
        <vex-verdict/> is the `verdict` and <file/> is the `file` of the
        decisive statement, both enclosed in a backtick code span. For the reason under `--why`, take the justification
        label from the `detail` of the decisive statement if it carries
        one, or its `status` otherwise.

        -   <if condition="the `verdict` is `AFFECTED`">
            <expand name="triage-report" arg1="AFFECTED"></expand>
            </if>

        -   <if condition="the `verdict` is `NOT-AFFECTED` or `FIXED`">
            <expand name="triage-report" arg1="NOT-AFFECTED"></expand>
            </if>

        -   Otherwise (`UNDER-INVESTIGATION` or `UNKNOWN`), the project
            has published no decision yet: continue with the next step.
            Do not output anything.

    </step>

4.  <step id="STEP 4: Resolve CVE" condition="<cve-id/> is not empty">

    1.  Call the `ase_cve(id: "<cve-id/>", format: "md")` tool of the
        `ase` MCP server. Deviating from the generic MCP tool error
        handling, if its response `text` starts with `ERROR: <info/>`,
        expand:

        <expand name="triage-fail" arg1="<info/>"></expand>

    2.  <if condition="the `State` of the returned record is `REJECTED`">
        <expand name="triage-fail" arg1="vulnerability **<cve-id/>** is `REJECTED`"></expand>
        </if>

    3.  Set <vuln/> to the returned record, merged with any <facts/>
        from STEP 2, and set <vuln-title/> to `<cve-id/>: <title/>`,
        where <title/> is the title of the record (or a very brief
        summary of its description if it has no title). Do not output
        anything.

    </step>

5.  <step id="STEP 5: Ground Hint" condition="<cve-id/> is empty">

    <if condition="<facts/> contains no usable facts about the vulnerability described by <hint/>">
    <expand name="triage-fail" arg1="Web grounding found no usable facts on the vulnerability"></expand>
    </if>

    Set <vuln/> to <facts/>, set <vuln-id>free-text hint</vuln-id>, and
    set <vuln-title/> to a very brief title of the vulnerability derived
    from <facts/>. Do not output anything.

    </step>

6.  <step id="STEP 6: Gather Evidence">

    1.  Determine from <vuln/> the *affected components* <components/>:
        the ecosystems, package names, vulnerable version ranges, and
        fixed versions of all affected packages and products, their
        *vulnerable functionality* (functions, classes, modules,
        features, or configuration options), and their exploitation
        preconditions. Do not output anything.

    2.  Gather the evidence of the project on <components/> through the
        following sub-agent (replaced by the `general-purpose` one if
        `Explore` is not available), and store the returned evidence in
        <evidence/>:

        `Agent(
            description: "Gather Triage Evidence",
            subagent_type: "Explore",
            prompt: "Strictly read-only, gather the evidence whether the project in the current working directory is exposed to the following vulnerability: <components/>. Report (1) every occurrence of an affected component in the manifests, lockfiles, and vendored or bundled code, each with its resolved version and whether it is a runtime, development, or build-time dependency, and (2) every usage of the vulnerable functionality in the source code, configuration, and build scripts, each with whether it is reachable from the entry points of the project. Cite every piece of evidence with its project-relative file path and line, report explicitly what was searched but not found, and give no verdict.",
            run_in_background: false
        )`

    </step>

7.  <step id="STEP 7: Decide Verdict">

    Set <basis>project analysis</basis> and decide the verdict
    *critically* and *solely* from <evidence/>, where runtime,
    development, and build-time dependencies count alike:

    -   <if condition="no affected component could be identified from <vuln/>, or the presence or versions of the affected components could not be determined (like an unresolved version range without any lockfile)">
        <expand name="triage-report" arg1="INCONCLUSIVE"></expand>
        </if>

    -   <if condition="a vulnerable version of an affected component is present *and* its vulnerable functionality is used and reachable">
        <expand name="triage-report" arg1="AFFECTED"></expand>
        </if>

    -   Otherwise, as no affected component is present, only fixed
        versions are present, or no usage of the vulnerable
        functionality was found:

        <expand name="triage-report" arg1="NOT-AFFECTED"></expand>

    </step>

</flow>

