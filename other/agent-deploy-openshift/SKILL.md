---
name: agent-deploy-openshift
description: Deploy a scaffolded agent to OpenShift using a UBI 9 Python S2I build. Run when the user asks to deploy, build, or run an agent on OpenShift.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

You are a deployment assistant. Your job is to deploy a Python agent to
OpenShift using the pattern from
https://agentops.redhatskills.com/basic-agents/hello-world.md.

The deployment uses a UBI 9 Python 3.12 multi-stage Dockerfile with S2I
`assemble` to install dependencies in a builder stage, then copies the
virtual environment into a minimal runtime image. The agent runs as a
one-shot pod.

## Step 1: Check prerequisites

First, check if `KUBECONFIG` is set by running `echo $KUBECONFIG` via Bash.
If it is empty, check whether `~/.kube/config` exists by running
`ls ~/.kube/config 2>/dev/null`.

If neither `KUBECONFIG` is set nor `~/.kube/config` exists, ask the user
(using AskUserQuestion):

**No kubeconfig found.** In some environments (containers, CI, shared
workstations) the default `~/.kube/config` is not writable. Where should
`oc` store its config?

1. **~/.kube/config** — use the default location
2. **/tmp/kubeconfig** — use a writable temp location (recommended for
   containers and restricted environments)

If the user picks `/tmp/kubeconfig` (or another custom path), run
`export KUBECONFIG=/tmp/kubeconfig` via Bash so all subsequent `oc`
commands in this session use that path. Also prepend
`KUBECONFIG=/tmp/kubeconfig` to all `oc` commands in later steps (or
set it once at the top of each Bash call).

Then run `oc whoami` via Bash to verify the user is logged into OpenShift.

- If the command **fails** — tell the user they must log in first
  (`oc login <cluster-url>`) and **stop**. Do not continue.
- If the command **succeeds** — print the logged-in user and cluster,
  then continue to Step 2.

## Step 2: Gather requirements

Parse `$ARGUMENTS` for:
- `--agent-dir <path>`: Directory containing `agent.py` + `requirements.txt`
- `--project <name>`: OpenShift project/namespace to deploy into (default: `basic-agents`)
- `--headless`: Skip clarifying questions and use all defaults

If `--headless` is NOT set, ask the user (using AskUserQuestion) up to 2
questions:

1. **Where is your scaffolded agent?** — the directory that contains
   `agent.py` and `requirements.txt`. Offer these options:
   - Current directory (`.`)
   - A specific path (let the user type it)
   - **I haven't scaffolded one yet**

2. **What OpenShift project should we deploy to?** (default: `basic-agents`)

### If the user has not scaffolded an agent

Ask which framework they want (using AskUserQuestion):

| Option | Skill to run |
|--------|-------------|
| LangGraph | `/langchain-agent:langchain-agent --headless --output-dir <dir>` |
| CrewAI | `/crewai-agent --headless --output-dir <dir>` |
| AutoGen | `/autogen-agent --headless --output-dir <dir>` |
| LlamaIndex | `/llamaindex-agent --headless --output-dir <dir>` |
| Google ADK | `/google-adk-agent --headless --output-dir <dir>` |

First ask the user for a directory to scaffold into (e.g. `./my-agent`).
Tell the user you will scaffold a default agent first. Run the chosen
framework skill using `Skill` with `--headless --output-dir <dir>` so it
writes files to the chosen directory without further questions. Then use
that output directory as the agent directory for the rest of this flow.

## Step 3: Validate agent folder

Check that the agent directory contains both `agent.py` and
`requirements.txt`. Run `ls <agent-dir>/agent.py <agent-dir>/requirements.txt`
via Bash.

If either file is missing, tell the user exactly which file is missing and
stop.

## Step 4: Create build context

Change into the agent directory and run the following via Bash:

```bash
# Create the Dockerfile
cat <<'EOF' > Dockerfile
# build
FROM registry.access.redhat.com/ubi9/python-312:latest as builder
USER 0
ADD app-src /tmp/src
RUN /usr/bin/fix-permissions /tmp/src
USER 1001
RUN /usr/libexec/s2i/assemble
# deploy
FROM registry.access.redhat.com/ubi9/python-312-minimal:latest
COPY --from=builder /opt/app-root /opt/app-root
USER 1001
CMD ["python", "agent.py"]
EOF

# Copy source files into app-src/
mkdir -p app-src
cp agent.py app-src/agent.py
cp requirements.txt app-src/requirements.txt
```

## Step 5: Create OpenShift project and build

Run each command via Bash. Use the project name from Step 2 (default
`basic-agents`). Replace `<project>` below with the actual name.

```bash
# Create the project (ignore error if it already exists)
oc new-project <project> 2>/dev/null || oc project <project>

# Create a binary build config
oc -n <project> new-build --binary --name=agent

# Start the build and follow the logs
oc -n <project> start-build agent --from-dir=. --follow
```

If `new-build` fails because the build config already exists, that is fine
— skip it and proceed to `start-build`.

## Step 6: Set environment variables

Ask the user for their model connection details (using AskUserQuestion):

1. **OPENAI_API_KEY** — required. API key, or any non-empty string for
   local models.
2. **OPENAI_MODEL_NAME** — model name (default: `gpt-4o-mini`).
3. **OPENAI_BASE_URL** — base URL for OpenAI-compatible endpoints. Omit
   for OpenAI.

## Step 7: Run the agent

Run the agent as a one-shot pod via Bash. Replace `<project>` and the env
var values with the user's answers.

```bash
oc -n <project> run agent \
  --restart=Never \
  --image=image-registry.openshift-image-registry.svc:5000/<project>/agent:latest \
  --env OPENAI_API_KEY=<key> \
  --env OPENAI_MODEL_NAME=<model> \
  --env OPENAI_BASE_URL=<url>
```

If `OPENAI_BASE_URL` was not provided (user is using OpenAI directly),
omit that `--env` flag entirely.

## Step 8: Check logs

Wait a few seconds for the pod to run, then check the logs:

```bash
oc -n <project> logs agent
```

If the pod is not yet finished (`ContainerCreating` or `Pending`), wait
and retry.

## Step 9: Confirm

Tell the user:
- The agent ran successfully (or report any errors from the logs)
- How to re-run: delete the pod and run Step 7 again
- How to clean up everything:

```bash
oc -n <project> delete bc,is,pod agent
```

- Link to the full documentation:
  https://agentops.redhatskills.com/basic-agents/hello-world.md

$ARGUMENTS
