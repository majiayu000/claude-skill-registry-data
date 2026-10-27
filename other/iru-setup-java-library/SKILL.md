---
name: iru-setup-java-library
description: "Invoke as `/iru-setup-java-library`, optionally with `args` (key: value lines). Generates the root `pom.xml` and Maven source folders for a new Java library from the house template; asks Update / Keep / Replace / Stop if a pom exists. Normally called by `iru-setup-java-library-repository`."
model: sonnet
---

# Setup Java Library

Generate `pom.xml` at the repository root for a new Java library, using an explicit example template embedded in
this skill (Step 4) that is genericized from a real repository's `pom.xml` — same test dependencies, same
`sign`/`build-extras` profiles, same build/reporting plugins — with only the project-identity fields (groupId,
artifactId, version, package, license, developer, repository info) filled in per repository. It also scaffolds the
standard Maven source folders for the library's base package.

## Step 0 — Check for pre-supplied parameters

This skill can be invoked stand-alone (`/iru-setup-java-library`) or as a step inside another skill, such as
`iru-setup-java-library-repository`, which resolves these same inputs itself (e.g. after asking the user once, or
applying its own defaults) and passes them through `args` as `key: value` lines, one per line, e.g.:

```
groupId: com.example
artifactId: my-library
package: com.example.mylibrary
java-version: 21
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/jane
license: Apache License 2.0
open-source: yes
visibility: public
ci: yes
publish: yes
sonar: cloud
sonar-organization: example-github
sonar-project-key: example_my-library
sonar-host-url: https://sonarcloud.io
on-existing: ask
```

Parse any such lines from `args` now. Every field found here is resolved — skip asking about it in Step 2. Only
fields genuinely missing from `args` (including `version` and `java-version`, which callers typically leave for
this skill's own defaults) still need a question. If `args` is absent or doesn't look like this format, treat everything as unset
and ask normally.

Recognized keys also include `open-source` (`yes`/`no`), `publish` (`yes`/`no` — whether the generated `pom.xml`
wires up Maven Central publishing), and `sonar` (`cloud`/`self-hosted`/`none`) plus, only when `sonar` is `cloud`
or `self-hosted`, `sonar-organization`/`sonar-project-key`/`sonar-host-url`. When `args` resolves `sonar`, Step 2's
own Sonar question is skipped entirely — it exists only as the fallback for whichever of `open-source`/`publish`/
`sonar` `args` didn't resolve.

Three more optional keys:

- `visibility` (`public`/`private`/`internal`) — the GitHub repository's visibility; only used to pick the
  recommended answer of Step 2's Sonar question (`internal` behaves like `private`). If absent and Step 2 still
  has to ask `sonar`, resolve it there (see Step 2).
- `ci` (`yes`/`no`) — whether the caller is generating GitHub Actions workflows. Only affects the Sonar question
  and report (Step 2/Step 8): with `ci: no`, nothing would send analysis reports automatically. Absent ⇒ treat as
  `yes` (this skill doesn't generate workflows itself, so it never asks this).
- `on-existing` (`ask`/`keep`/`update`/`replace`, default `ask`) — how Step 1 treats an existing `pom.xml` without
  asking. Only for scripted runs.

Ignore any other key (e.g. `mode`, `ci-tests`, `pages`) — they belong to other skills in the same pipeline.

## Step 1 — Check for an existing `pom.xml`

- **No `pom.xml` at the repository root**: tell the user this skill is **creating `pom.xml` from scratch**, then
  skip straight to Step 2.
- **`pom.xml` already exists**: tell the user this skill is **updating an existing setup**, and warn that a prior
  `pom.xml` was found. Read it now: its current `groupId`, `artifactId`, `version`, `description`, license,
  developer, main source package, Java version (`maven.compiler.source`/`maven.compiler.target`/
  `maven.compiler.release`), and whether it already carries `central-publishing-maven-plugin`/a `sign` profile and
  `sonar-maven-plugin`/`sonar.*` properties. Compare those against whatever Step 0 already resolved, and name any
  concrete contradiction in the question (e.g. "your current `pom.xml` has `sonar-maven-plugin` but this run chose
  `sonar: none`", "it has no `central-publishing-maven-plugin` but `publish: yes`").

  If `on-existing` (Step 0) is `keep`, `update`, or `replace`, apply that choice without asking (still print the
  warning). Otherwise ask with `AskUserQuestion` (header e.g. `pom.xml`), explaining each option's consequence:

  - **Update (Recommended)** — "Merge: add what's missing from this skill's template (test dependencies, standard
    build/reporting plugins, `sign`/`build-extras` profiles, `sonar.*`/Central blocks per this run's
    `publish`/`sonar`) and correct outdated parts (plugin versions, blocks that should now be gated on/off); keep
    every dependency, plugin, profile, and property this skill doesn't own. You review a diff; your customizations
    survive, but a customized part this skill owns (e.g. a pinned plugin version) may be rewritten."
  - **Keep as is** — "Leave `pom.xml` untouched (only missing source folders are created). Nothing you customized
    changes, but it may stay out of date or disagree with this run's choices — the report lists each mismatch."
  - **Replace** — "Regenerate the whole file from this skill's example. Result matches the house pattern exactly,
    but every dependency or plugin beyond the four test dependencies and the standard profiles/plugins is lost
    (recoverable only from git history)."
  - **Stop** — "End this skill now without changing anything (no `pom.xml` edit, no source folders)."

  Then:

  - **Stop**: report that `pom.xml` already exists and end here — make no changes.
  - **Keep**: skip Steps 2–6 except for what Step 7 needs: take the library package from Step 0's `package` if
    supplied, otherwise from the existing `pom.xml`'s main source layout (an existing `src/main/java/<path>`
    directory or the `groovy-maven-plugin` build-info path), asking the user only if neither resolves it. Go to
    Step 7, and list in Step 8 every mismatch between the kept file and this run's resolved
    `publish`/`sonar`/Java-version values.
  - **Update** or **Replace**: before asking the questions in Step 2, use the existing file's values read above as
    the *defaults* you offer the user for each question that Step 0 didn't already resolve — a value supplied via
    `args` always wins over a value merely found in the existing file, since it reflects what the caller (or the
    user, just now) explicitly asked for. For **Replace**, tell the user up front that regenerating from the
    template replaces the whole file — any dependencies or plugins beyond the four test dependencies and the
    standard profiles/plugins in Step 4's example will be lost unless the user re-adds them afterward (call this
    out again in Step 8). For **Update**, Step 6 merges instead of overwriting (see there).

## Step 2 — Collect the required inputs

For any field Step 0 already resolved from `args`, use that value directly and don't ask about it again. For
everything else, ask the user directly (plain conversation, pre-filling defaults found in Step 1 if updating an
existing file):

- **groupId** — e.g. `com.example`.
- **artifactId** — e.g. `my-library`.
- **version** — default `1.0.0-SNAPSHOT` if the user doesn't give one.
- **Java version** — the language level the library targets, written to
  `maven.compiler.source`/`maven.compiler.target` in Step 4's template. Default `21` if the user doesn't give one;
  offer that default explicitly rather than asking open-endedly. Keep it consistent with whatever
  `iru-setup-java-github-workflows` sets up the CI pipeline to build against (same `21` default there), and note the
  chosen value in Step 8's report so the user can spot a mismatch if that skill was already run with a different
  one.
- **Library package** — the base Java package for the library's main source (e.g. `com.example.mylibrary`). This
  need not equal `groupId`; ask for it explicitly. Used in Step 3's `src/main/java/<package>` layout and in the
  `groovy-maven-plugin` step of Step 5.
- **Developer name**, **developer email**, **organizationUrl** — populate the `<developers>` block.

Then, unless Step 0 already resolved a `license` value from `args`, ask about the **license** with
`AskUserQuestion` (small bounded choice, so a proper multiple-choice question fits, unlike the free-text fields
above):

- Apache License 2.0 (recommended) — `The Apache License, Version 2.0` /
  `http://www.apache.org/licenses/LICENSE-2.0.txt`
- MIT License — `The MIT License` / `https://opensource.org/license/mit`
- No license (proprietary / all rights reserved) — omit the `<licenses>` block entirely
- Other — ask for the license's display name and URL directly afterward

If a license is chosen (anything but "No license"), remind the user in Step 7 to also add a matching `LICENSE`
file at the repository root if one doesn't exist yet — the `iru-check-license` skill can verify/backfill file headers
against it once it's there.

Then resolve `open-source`, `publish`, and `sonar` — skip any of the three Step 0 already resolved from `args`.
When invoked stand-alone with none of them pre-resolved, ask `open-source` *first* (`AskUserQuestion`: yes/no) and
derive the recommended defaults for the other two from that answer, per this catalog's shared convention:

- **open-source** — is this repository open source? Yes / No.
- **publish** (Maven Central) — default **Yes** when open-source is Yes; when not open source, ask with **No**
  recommended, explaining that Maven Central is meant for publishing redistributable artifacts other projects
  depend on, which usually isn't appropriate for closed-source code. `No` omits `central-publishing-maven-plugin`
  and the `sign` profile from Step 4's template entirely (the `build-extras` profile is unrelated to publishing
  and is kept regardless).
- **sonar** — whether to wire up a SonarQube/SonarCloud scan (this house pattern runs it via the
  `sonar-maven-plugin`, invoked as `mvn sonar:sonar` — typically from the CI workflow the
  `iru-setup-java-github-workflows` skill generates, so it's worth setting up here even if that workflow comes
  later). Phrase it as "Configure SonarCloud / SonarQube and send CI analysis and coverage reports to it?".
  Recommend **SonarCloud** (`cloud`) only when open-source is Yes **and** `visibility` is `public`; otherwise state
  that SonarCloud (SonarQube Cloud) is free only for public/open-source projects — a private project needs a paid
  plan, per SonarSource's current pricing (tell the user to double-check) — and recommend **None** (`none`),
  offering **self-hosted SonarQube** as the second option (Community Build is free, but you run the server). If
  `visibility` wasn't supplied in `args`, resolve it just before this question: `gh repo view --json visibility -q
  .visibility` when the repository has a GitHub remote (lowercase the result and tell the user), otherwise ask
  **Public** / **Private** with `AskUserQuestion` (Public recommended when open source, else Private); if
  open-source is Yes but visibility is private/internal, point out the contradiction and ask which is right. If
  `ci: no` was supplied, say plainly that nothing would send reports automatically — analysis would only run when
  someone runs `mvn sonar:sonar` manually with a token — and recommend **None**; if the user still picks
  `cloud`/`self-hosted`, configure the `pom.xml` side below anyway and note in Step 8 that no CI step sends reports:
  - `cloud` — ask for the `sonar.organization` key, offering `<owner>-github` (the owner parsed in Step 3) as the
    suggested default, since that's the key SonarCloud assigns by default when an organization is created by
    importing from GitHub. Default `sonar.projectKey` to `<owner>_<repo>` (also from Step 3) and `sonar.host.url`
    to `https://sonarcloud.io`, confirming both with the user rather than assuming silently.
  - `self-hosted` — ask for `sonar.host.url` directly (no sensible default), plus `sonar.organization` only if
    that server has organizations enabled, and `sonar.projectKey`.
  - `none` — omit the four `sonar.*` properties and the `sonar-maven-plugin` entry from Step 4's template
    entirely.

## Step 3 — Infer repository information

Don't ask for these — derive them from the current repository:

- **Owner/repo and host**: parse `git remote get-url origin` (handles both `git@host:owner/repo.git` and
  `https://host/owner/repo.git` forms). Use the parsed host/owner/repo for:
  - `<url>`: `https://<host>/<owner>/<repo>`
  - `<scm><connection>`/`<developerConnection>`: `scm:git@<host>:<owner>/<repo>.git`
  - `<scm><url>`: `git@<host>:<owner>/<repo>.git`
  If there's no `origin` remote yet, ask the user for the intended repository URL instead of leaving it blank.
- **Description**: if the `gh` CLI is available and authenticated, try `gh repo view --json description -q
  .description`; if that yields nothing (no remote repo yet, `gh` unavailable, or empty description), ask the user
  for a one-line description instead.
- **Inception year**: `git log --reverse --format=%ad --date=format:%Y | head -1` for the first commit's year;
  fall back to the current year if the repository has no commits yet.

## Step 4 — Reference template

This is a genericized example — based on a real Java/Maven library's actual `pom.xml` — kept verbatim below except
for the placeholders. Preserve every dependency, profile, plugin, version, and reporting entry exactly as shown;
only substitute `<placeholder>` values using Steps 2–3.

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId><group-id></groupId>
  <artifactId><artifact-id></artifactId>
  <version><version></version>
  <packaging>jar</packaging>

  <name>${project.groupId}:${project.artifactId}</name>
  <description><description></description>
  <url><repository-url></url>
  <inceptionYear><inception-year></inceptionYear>

  <!-- Omit this whole <licenses> block if the user chose "No license" in Step 2 -->
  <licenses>
    <license>
      <name><license-name></name>
      <url><license-url></url>
    </license>
  </licenses>
  <developers>
    <developer>
      <name><developer-name></name>
      <email><developer-email></email>
      <organizationUrl><organization-url></organizationUrl>
    </developer>
  </developers>
  <scm>
    <connection>scm:git@<host>:<owner>/<repo>.git</connection>
    <developerConnection>scm:git@<host>:<owner>/<repo>.git</developerConnection>
    <url>git@<host>:<owner>/<repo>.git</url>
  </scm>

  <dependencies>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>5.13.4</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.junit.platform</groupId>
      <artifactId>junit-platform-launcher</artifactId>
      <version>1.14.3</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.mockito</groupId>
      <artifactId>mockito-core</artifactId>
      <version>5.19.0</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.mockito</groupId>
      <artifactId>mockito-junit-jupiter</artifactId>
      <version>5.19.0</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <!-- <java-version> from Step 2 — `21` unless the user or the calling skill asked for something else -->
    <maven.compiler.source><java-version></maven.compiler.source>
    <maven.compiler.target><java-version></maven.compiler.target>
    <github.global.server>github</github.global.server>
    <github.global.oauth2Token>${env.GITHUB_OAUTH_TOKEN}</github.global.oauth2Token>
    <!-- Omit these four sonar.* properties if the user opted out of SonarCloud/SonarQube in Step 2 -->
    <sonar.organization><sonar-organization></sonar.organization>
    <sonar.projectKey><sonar-project-key></sonar.projectKey>
    <sonar.host.url><sonar-host-url></sonar.host.url>
    <sonar.coverage.jacoco.xmlReportPaths>${project.build.directory}/site/jacoco/jacoco.xml</sonar.coverage.jacoco.xmlReportPaths>
  </properties>

  <profiles>
    <!-- Omit this whole "sign" profile if the user opted out of Maven Central publishing (publish: no) in Step 2 —
         signing is only needed to satisfy Central's artifact-signing requirement -->
    <profile>
      <id>sign</id>
      <build>
        <plugins>
          <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-gpg-plugin</artifactId>
            <version>3.2.8</version>
            <executions>
              <execution>
                <id>sign-artifacts</id>
                <phase>verify</phase>
                <goals>
                  <goal>sign</goal>
                </goals>
              </execution>
            </executions>
          </plugin>
        </plugins>
      </build>
    </profile>
    <profile>
      <id>build-extras</id>
      <activation>
        <activeByDefault>true</activeByDefault>
      </activation>
      <build>
        <plugins>
          <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-source-plugin</artifactId>
            <version>3.3.1</version>
            <executions>
              <execution>
                <id>attach-sources</id>
                <goals>
                  <goal>jar-no-fork</goal>
                </goals>
              </execution>
            </executions>
          </plugin>
          <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-javadoc-plugin</artifactId>
            <version>3.11.3</version>
            <executions>
              <execution>
                <id>attach-javadocs</id>
                <goals>
                  <goal>jar</goal>
                </goals>
              </execution>
            </executions>
          </plugin>
        </plugins>
      </build>
    </profile>
  </profiles>

  <!-- default profile -->
  <build>
    <plugins>
      <!-- unit tests plugins -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.5.4</version>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-failsafe-plugin</artifactId>
        <version>3.5.4</version>
      </plugin>
      <!-- code coverage plugin -->
      <plugin>
        <groupId>org.jacoco</groupId>
        <artifactId>jacoco-maven-plugin</artifactId>
        <version>0.8.13</version>
        <executions>
          <execution>
            <id>jacoco-initialize</id>
            <goals>
              <goal>prepare-agent</goal>
            </goals>
          </execution>
          <execution>
            <id>jacoco-site</id>
            <phase>package</phase>
            <goals>
              <goal>report</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
      <!-- code quality plugins -->
      <plugin>
        <groupId>com.github.spotbugs</groupId>
        <artifactId>spotbugs-maven-plugin</artifactId>
        <version>4.9.6.0</version>
      </plugin>
      <!-- maven site -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-site-plugin</artifactId>
        <version>3.21.0</version>
      </plugin>
      <!-- save build info into generated package -->
      <plugin>
        <groupId>org.codehaus.gmaven</groupId>
        <artifactId>groovy-maven-plugin</artifactId>
        <version>2.1.1</version>
        <executions>
          <execution>
            <phase>validate</phase>
            <goals>
              <goal>execute</goal>
            </goals>
            <configuration>
              <source>
                <![CDATA[
                import java.util.Date
                import java.util.Properties
                import java.text.SimpleDateFormat
                import java.io.File
                import java.io.FileWriter

                println("Saving build info...")
                def dateFormatter = new SimpleDateFormat("yy-MM-dd HH:mm:ss")
                def buildTimestamp = dateFormatter.format(new Date())

                String groupId = "${project.groupId}"
                String artifactId = "${project.artifactId}"
                String version = "${project.version}"

                //JENKINS
                def buildNumber = System.getenv("BUILD_NUMBER")
                def commit = System.getenv("GIT_COMMIT")
                def branch = System.getenv("GIT_BRANCH")

                //TRAVIS CI
                if (buildNumber == null) {
                  buildNumber = System.getenv("TRAVIS_BUILD_NUMBER")
                }
                if (commit == null) {
                  commit = System.getenv("TRAVIS_COMMIT")
                }
                if (branch == null) {
                  branch = System.getenv("TRAVIS_BRANCH")
                }

                //GITLAB
                if (buildNumber == null) {
                  buildNumber = System.getenv("CI_JOB_ID")
                }
                if (commit == null) {
                  commit = System.getenv("CI_COMMIT_SHA")
                }
                if (branch == null) {
                  branch = System.getenv("CI_COMMIT_REF_NAME")
                }

                def props = new Properties()
                props.setProperty("BUILD_TIMESTAMP", buildTimestamp)
                props.setProperty("GROUP_ID", groupId)
                props.setProperty("ARTIFACT_ID", artifactId)
                props.setProperty("VERSION", version)
                if (buildNumber != null) {
                  props.setProperty("BUILD_NUMBER", buildNumber)
                }
                if (commit != null) {
                  props.setProperty("COMMIT", commit)
                }
                if (branch != null) {
                  props.setProperty("BRANCH", branch)
                }

                File dir = new File("src/main/resources/<library-package-path>")
                dir.mkdirs()
                File file = new File(dir, "build-info.properties")
                FileWriter writer = new FileWriter(file)
                props.store(writer, null)
                writer.close()
                println("Build info saved at " + file)
                ]]>
              </source>
            </configuration>
          </execution>
        </executions>
      </plugin>
      <!-- deploys artifact to snapshots repository; omit this whole plugin entry if publish: no in Step 2 -->
      <plugin>
        <groupId>org.sonatype.central</groupId>
        <artifactId>central-publishing-maven-plugin</artifactId>
        <version>0.8.0</version>
        <extensions>true</extensions>
        <configuration>
          <publishingServerId>central</publishingServerId>
          <autoPublish>true</autoPublish>
        </configuration>
      </plugin>
      <!-- SonarCloud analysis; omit this plugin entry if sonar: none in Step 2 -->
      <plugin>
        <groupId>org.sonarsource.scanner.maven</groupId>
        <artifactId>sonar-maven-plugin</artifactId>
        <version><sonar-maven-plugin-version></version>
      </plugin>
    </plugins>
  </build>

  <reporting>
    <plugins>
      <!-- add javadoc report into site -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-javadoc-plugin</artifactId>
        <version>3.11.3</version>
        <configuration>
          <show>private</show>
          <nohelp>true</nohelp>
          <detectJavaApiLink>true</detectJavaApiLink>
        </configuration>
      </plugin>
      <!-- adds unit tests report into site -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-report-plugin</artifactId>
        <version>3.5.4</version>
      </plugin>
      <!-- adds code coverage report into site -->
      <plugin>
        <groupId>org.jacoco</groupId>
        <artifactId>jacoco-maven-plugin</artifactId>
        <version>0.8.13</version>
      </plugin>
      <!-- adds code quality reports into site -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-checkstyle-plugin</artifactId>
        <version>3.6.0</version>
        <configuration>
          <configLocation>checkstyle.xml</configLocation>
        </configuration>
        <reportSets>
          <reportSet>
            <reports>
              <report>checkstyle</report>
            </reports>
          </reportSet>
        </reportSets>
      </plugin>

      <plugin>
        <groupId>com.github.spotbugs</groupId>
        <artifactId>spotbugs-maven-plugin</artifactId>
        <version>4.9.6.0</version>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-pmd-plugin</artifactId>
        <version>3.27.0</version>
      </plugin>
      <!--
      adds cross reference into source for easier navigation of source in
      reports
      -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jxr-plugin</artifactId>
        <version>3.6.0</version>
      </plugin>
    </plugins>
  </reporting>
</project>
```

Note on `<library-package-path>`: this is the library package from Step 2 with dots turned into slashes (e.g.
`com.example.mylibrary` → `com/example/mylibrary`) — it must match wherever the library's own code will later read
`build-info.properties` as a classpath resource, the same way this repository's `BuildInfo` class reads it from
`com/irurueta/hermes`.

## Step 5 — Fill the template

Substitute every placeholder using Steps 2–3:

- `<group-id>`, `<artifact-id>`, `<version>`, `<description>`, `<developer-name>`, `<developer-email>`,
  `<organization-url>` — straight from Step 2's answers.
- `<repository-url>`, `<host>`, `<owner>`, `<repo>`, `<inception-year>` — straight from Step 3's inference.
- `<license-name>` / `<license-url>` — from Step 2's license choice; if "No license" was chosen, remove the entire
  `<licenses>...</licenses>` block rather than leaving empty placeholder tags.
- `<library-package-path>` — the library package from Step 2, with `.` replaced by `/`.
- `<java-version>` — the Java version from Step 2 (`21` unless overridden), substituted into both
  `maven.compiler.source` and `maven.compiler.target`. Drop the explanatory comment above them from the written
  file — it's guidance for filling the template, not part of the generated `pom.xml`.
- `<sonar-organization>` / `<sonar-project-key>` / `<sonar-host-url>` — from Step 2's `sonar` answer; if `sonar:
  none`, remove the four `sonar.*` properties and the `sonar-maven-plugin` plugin entry entirely rather than
  leaving empty placeholder tags.
- `<sonar-maven-plugin-version>` — only needed if `sonar: cloud` or `sonar: self-hosted`: look up the current
  latest `org.sonarsource.scanner.maven:sonar-maven-plugin` version (e.g. via Maven Central's search API) rather
  than hardcoding a version here, since this plugin releases fairly often.
- **`publish: no`** — remove the entire `central-publishing-maven-plugin` `<plugin>` entry under
  `<build><plugins>` *and* the entire `sign` `<profile>` under `<profiles>` (keep the `build-extras` profile — it
  attaches sources/javadoc jars and is unrelated to publishing). `publish: yes` (the default when open source)
  keeps both as shown in Step 4's template, with no placeholders of their own to fill.

Every other line (dependencies, properties, the `build-extras` profile, all build/reporting plugins and their
versions) is copied verbatim from Step 4 — this skill does not add, remove, or re-version any dependency or plugin
beyond what the template already shows, other than the `publish`/`sonar`-gated blocks above.

## Step 6 — Write `pom.xml`

Skip this step entirely if Step 1 resolved **Keep**.

- **New file** or **Replace**: write the filled-in template to `pom.xml` at the repository root (creating it
  fresh, or replacing it entirely).
- **Update**: use the filled-in template as the reference and edit the existing `pom.xml` in place — add every
  dependency, property, profile, and build/reporting plugin from the template that's missing; bring the ones this
  skill owns in line with the template (plugin versions, identity fields the user just confirmed, the
  `publish`/`sonar`-gated blocks added or removed per this run's answers); leave every other dependency, plugin,
  profile, property, and module untouched, in its existing order. Write the result to a temp path, show the user
  `git diff --no-index pom.xml <draft>`, and only write it to `pom.xml` once they accept (free-text corrections
  revise the draft first).

## Step 7 — Scaffold the source folders

Using the same library package from Step 2 (with `.` replaced by `/`, the same `<library-package-path>` computed
in Step 5), create the standard Maven layout if not already present:

```
src/main/java/<library-package-path>/
src/main/resources/<library-package-path>/
src/test/java/<library-package-path>/
```

- Create each directory only if it doesn't already exist — don't touch a directory (or any files already inside
  it) that's already there, whether from a prior run of this skill or from existing library code. This step is
  inherently additive, so it never asks Update/Keep/Replace: tell the user which folders already existed (an
  existing source layout is reported as **kept as is**) and which it is creating from scratch.
- Git doesn't track empty directories, so these three will disappear from `git status`/a commit until a file
  exists inside them. Don't create placeholder files (e.g. `.gitkeep`) unless the user asks for that — note this
  in Step 8 instead, since the first source/test/resource file the user adds will make the directory stick.
- `src/main/resources/<library-package-path>` is exactly where the `groovy-maven-plugin` step in Step 4's template
  writes `build-info.properties` at build time — this folder existing ahead of time isn't required for that (the
  script calls `mkdir()`), but creating it now keeps the layout visibly complete from the start.

## Step 8 — Report and warn

Summarize what was generated, starting with whether this run created from scratch or updated an existing setup and
the action taken on `pom.xml` — **created**, **updated**, **replaced**, **kept as is**, or **stopped** (and whether
that came from the user's answer or from `on-existing`): the resolved groupId/artifactId/version, the Java version written to
`maven.compiler.source`/`maven.compiler.target` (flagging it explicitly if it isn't `21`, so a mismatch with the CI
pipeline `iru-setup-java-github-workflows` generates is easy to spot), the license chosen (or "none"), and the
repository info inferred in Step 3.

State explicitly what was included versus omitted, and why:

- **`open-source`**: yes/no, as resolved in Step 2.
- **`publish`**: yes/no — if `yes`, `central-publishing-maven-plugin` and the `sign` profile were included; if
  `no`, both were omitted (the `build-extras` profile was kept regardless, since it's unrelated to publishing).
- **`sonar`**: `cloud`/`self-hosted`/`none` — if `cloud` or `self-hosted`, the four `sonar.*` properties and the
  `sonar-maven-plugin` entry were included with the resolved `sonar.organization`/`sonar.projectKey`/
  `sonar.host.url`; if `none`, note that this is expected when the project isn't open source (SonarCloud is free
  only for public/open-source projects) unless the user explicitly chose it. If `ci: no` was supplied and Sonar was
  configured anyway, say that no CI step will send analysis/coverage reports — they only reach Sonar when someone
  runs `mvn sonar:sonar` manually with a token.
- If `pom.xml` was **kept as is**, list each mismatch between the kept file and this run's resolved values (e.g.
  `sonar-maven-plugin` present after `sonar: none`, no Central plugin despite `publish: yes`, a Java version other
  than the resolved one), so the user can fix it by hand or re-run with Update.

Then report which of the three source folders from Step 7 were created versus already present. Remind the user
that empty directories won't show up in `git status` until they contain a file. If Step 1's existing file was
replaced (or updated), explicitly list what could have been lost — any dependency or plugin that isn't one of the four test
dependencies or the standard profiles/plugins in Step 4's template — and tell the user to check `git diff pom.xml`
for anything they need to re-add.

Finish with an explicit warning: **the user must review the generated `pom.xml` before building or committing.**
Confirm the license choice matches an actual `LICENSE` file (or that none is intended), that the inferred
repository URL/SCM values are correct, and that `mvn validate` (or `mvn compile`) succeeds before relying on this
file. If a license was chosen and no `LICENSE` file exists yet, suggest the `iru-check-license` skill to generate one
and backfill source headers. If `sonar: cloud` or `sonar: self-hosted` was chosen, note that a `SONAR_TOKEN`
repository secret and an actual SonarCloud/SonarQube project matching `sonar.projectKey` still need to exist before
`mvn sonar:sonar` (typically run from the `iru-setup-java-github-workflows` skill's generated CI) will succeed. If
`publish: yes` was chosen, note that Maven Central publishing credentials/signing secrets still need to exist
before `mvn deploy` (via that same generated CI) will succeed.
