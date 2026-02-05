---
name: cva-setup-clojure
description: Clojure project setup and configuration for agent development with Google ADK. Includes deps.edn configuration, directory structure, namespace organization, REPL-driven development workflow, and build system integration. Use when starting new agent projects, configuring Clojure dependencies, troubleshooting project setup issues, organizing namespaces and code structure, or need guidance on Clojure best practices for agent development.
allowed-tools: Read,Bash,Edit,Write
---

# Clojure Project Setup for Agent Development

> **Purpose:** Complete guide for setting up Clojure projects for developing agents with Google ADK and Python interop
> **Prerequisites:** Java 17+, Clojure 1.11+

## 🎯 Overview

This skill provides comprehensive guidance for setting up production-ready Clojure projects tailored for agent development. It covers the complete project lifecycle from initial directory creation to REPL-driven workflows, focusing on the unique requirements of building intelligent agents that combine Clojure's functional programming paradigm with Google's Agent Development Kit (ADK) and Python machine learning libraries.

The setup emphasizes separation of concerns, proper dependency management, and development ergonomics through REPL-driven workflows. You'll learn how to structure projects that can seamlessly integrate Java-based Google ADK, Python libraries via libpython-clj, and maintain clean, testable Clojure code.

This configuration supports multiple development workflows including interactive REPL development, automated testing with Kaocha, and production builds with tools.build. The structure is battle-tested for projects requiring multi-language interoperability and complex AI/ML agent orchestration.

## 📋 Recommended Project Structure

```
meu-agente/
├── deps.edn                 # Dependencies and configuration
├── .gitignore              # Files to ignore
├── README.md               # Project documentation
├── python.edn              # libpython-clj config (optional)
├── resources/              # Static resources
│   └── credentials/        # Credentials (DO NOT VERSION!)
├── src/
│   └── lab/
│       ├── agents/         # Agent implementations
│       ├── tools/          # Custom tools
│       ├── interop/        # Java/Python interop
│       ├── utils/          # Utilities
│       └── config/         # Initial configuration
├── test/
│   └── lab/
│       └── agents_test.clj
└── dev/
    └── user.clj            # Development namespace
```

## 🔧 Complete deps.edn Configuration

### Full Configuration with All Dependencies

```clojure
{:paths ["src" "resources"]

 :deps {;; Clojure core
        org.clojure/clojure {:mvn/version "1.11.1"}

        ;; Google ADK Java SDK
        com.google.cloud/google-adk-java {:mvn/version "0.2.0"}

        ;; Python interop
        clj-python/libpython-clj {:mvn/version "2.025"}

        ;; Google Cloud libraries
        com.google.cloud/google-cloud-aiplatform {:mvn/version "3.40.0"}

        ;; Utilities
        org.clojure/data.json {:mvn/version "2.5.0"}
        metosin/malli {:mvn/version "0.13.0"}  ;; Schema validation
        }

 :aliases
 {;; Development
  :dev {:extra-paths ["dev"]
        :extra-deps {nrepl/nrepl {:mvn/version "1.1.0"}
                     cider/cider-nrepl {:mvn/version "0.42.1"}}}

  ;; Testing
  :test {:extra-paths ["test"]
         :extra-deps {lambdaisland/kaocha {:mvn/version "1.87.1366"}}}

  ;; REPL tools
  :repl {:extra-deps {com.bhauman/rebel-readline {:mvn/version "0.1.4"}}
         :main-opts ["-m" "rebel-readline.main"]}

  ;; Build
  :build {:deps {io.github.clojure/tools.build {:git/tag "v0.9.6"
                                                  :git/sha "8e78bcc"}}
          :ns-default build}

  ;; Local Python environment (adjust path)
  :python {:jvm-opts ["-Dpython.executable=/usr/bin/python3"]}}}
```

## 🚀 Step-by-Step Project Creation

### 1. Create Directory Structure

```bash
# Create project directory with full structure
mkdir -p meu-agente/{src/lab/{agents,tools,interop,utils,config},test/lab,dev,resources}

cd meu-agente

# Test: Verify structure created
# Expected output: tree showing all directories
ls -R
```

### 2. Create deps.edn

```bash
# Create dependency file with minimal config
cat > deps.edn << 'EOF'
{:paths ["src" "resources"]
 :deps {org.clojure/clojure {:mvn/version "1.11.1"}
        com.google.cloud/google-adk-java {:mvn/version "0.2.0"}
        clj-python/libpython-clj {:mvn/version "2.025"}}}
EOF

# Test: Verify deps.edn is valid
# Expected: Should see dependency download
clj -P
```

### 3. Create .gitignore

```bash
cat > .gitignore << 'EOF'
# Clojure
.cpcache/
.nrepl-port
.lein-repl-history
target/
pom.xml

# Python
__pycache__/
*.pyc
.python-version
venv/

# IDEs
.idea/
.vscode/
*.iml

# OS
.DS_Store
Thumbs.db

# Credentials (IMPORTANT!)
resources/credentials/
*.json
*.pem
.env
EOF
```

### 4. Create Configuration Namespace

```bash
cat > src/lab/config/init.clj << 'EOF'
(ns lab.config.init
  "Initial project configuration"
  (:require [libpython-clj2.python :as py]))

(defn init-python!
  "Initialize Python environment with auto-detection"
  []
  (py/initialize! :python-executable "python3"
                  :library-path nil)  ; Auto-detect
  (println "✅ Python initialized successfully!"))

(defn init-google-cloud!
  "Configure Google Cloud credentials"
  [credentials-path]
  (System/setProperty "GOOGLE_APPLICATION_CREDENTIALS" credentials-path)
  (println "✅ Google Cloud credentials set"))

(defn init-all!
  "Complete environment initialization"
  [config]
  (init-python!)
  (when-let [creds (:google-credentials config)]
    (init-google-cloud! creds))
  (println "✅ Environment initialized successfully!"))

(comment
  ;; Test initialization
  (init-all! {})
  ;; => ✅ Python initialized successfully!
  ;; => ✅ Environment initialized successfully!
  )
EOF
```

### 5. Create Development Namespace

```bash
cat > dev/user.clj << 'EOF'
(ns user
  "Development REPL namespace"
  (:require [lab.config.init :as init]
            [clojure.repl :refer :all]
            [clojure.pprint :refer [pprint]]))

;; Initialize automatically on REPL startup
(init/init-all! {})

(comment
  ;; Examples for REPL usage

  ;; Reload namespace
  (require '[lab.agents.core :as agents] :reload)

  ;; Test agent
  (agents/run-agent {:input "Hello"})
  ;; => {:output "Agent response" :status :success}

  ;; Pretty print data structures
  (pprint {:complex {:nested {:data "here"}}})
  )
EOF
```

## 🧪 Setup Verification

### Test 1: Verify Clojure REPL

```bash
# Start REPL with rebel-readline
clj -M:repl

# Test: Expected output in REPL
# user=> (+ 1 2 3)
# 6
# user=> (println "✅ Clojure working!")
# ✅ Clojure working!
```

### Test 2: Verify libpython-clj

```bash
clj
```

```clojure
user=> (require '[libpython-clj2.python :as py])
;; => nil

user=> (py/initialize!)
;; => :ok

user=> (def sys (py/import-module "sys"))
;; => #'user/sys

user=> (py/get-attr sys "version")
;; => "3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0]"
;; Expected: Shows Python version string
```

### Test 3: Verify Google ADK (Java Interop)

```clojure
user=> (import '[com.google.adk Agent])
;; => com.google.adk.Agent

user=> Agent
;; => com.google.adk.Agent
;; Expected: Shows class object
```

## 📦 Dependencies Explained

### Core Dependencies

```clojure
;; Google ADK - Agent framework
com.google.cloud/google-adk-java {:mvn/version "0.2.0"}
;; Provides: Agent, Tool, LLMClient classes for building agents

;; Python interop - Use Python libraries from Clojure
clj-python/libpython-clj {:mvn/version "2.025"}
;; Provides: py/initialize!, py/import-module, require-python

;; Google Cloud AI Platform - Vertex AI integration
com.google.cloud/google-cloud-aiplatform {:mvn/version "3.40.0"}
;; Provides: PredictionServiceClient, EndpointServiceClient
```

### Recommended Utilities

```clojure
;; JSON parsing and generation
org.clojure/data.json {:mvn/version "2.5.0"}

;; Schema validation (alternative: clojure.spec)
metosin/malli {:mvn/version "0.13.0"}

;; HTTP client for REST APIs
hato/hato {:mvn/version "0.9.0"}

;; Logging
com.taoensso/timbre {:mvn/version "6.3.1"}
```

## 🎯 Best Practices

### Code Organization

```clojure
;; Organize namespaces by functionality
lab.agents.core        ; Main agent implementations
lab.agents.workflow    ; Workflow agents
lab.agents.llm         ; LLM-based agents
lab.tools.custom       ; Custom tool implementations
lab.interop.python     ; Python interop utilities
lab.interop.java       ; Java interop utilities
```

### Separate Configuration from Logic

```clojure
;; ❌ Avoid hardcoded configuration
(def agent (create-agent {:api-key "hardcoded-key"}))

;; ✅ Prefer loaded configuration
(def agent (create-agent (load-config)))

;; ✅ Or use environment variables
(def agent (create-agent {:api-key (System/getenv "API_KEY")}))
```

### Use Docstrings and Comments

```clojure
(defn create-agent
  "Creates an agent with specified configuration.

  Args:
    config - Map with :name, :tools, :model keys
             :name   (string)  Agent identifier
             :tools  (vector)  Vector of tool functions
             :model  (keyword) LLM model to use

  Returns:
    Agent instance configured and ready to use

  Example:
    (create-agent {:name \"MyAgent\"
                   :tools [search-tool calc-tool]
                   :model :gemini-pro})
    ;; => #Agent{:name \"MyAgent\" :status :ready}"
  [config]
  (let [{:keys [name tools model]} config]
    ;; Implementation
    ))
```

### REPL-Driven Development

```clojure
;; Always use (comment ...) for experimental code
(comment
  ;; Quick test - doesn't execute on file load
  (def test-agent (create-agent {:name "Test"}))
  ;; => #Agent{:name "Test"}

  ;; View result
  (pprint test-agent)
  ;; => {:name "Test"
  ;;     :tools []
  ;;     :model :gemini-pro}

  ;; Test agent execution
  (run-agent test-agent "Hello")
  ;; => {:response "Hello! How can I help?" :status :success}
  )
```

### State Management

```clojure
;; Use atoms for mutable state when necessary
(defonce app-state
  (atom {:agents {}
         :sessions {}
         :config {}}))

;; Pure functions for transformations
(defn add-agent
  "Pure function to add agent to state"
  [state agent-id agent]
  (assoc-in state [:agents agent-id] agent))

;; Controlled mutation
(swap! app-state add-agent :agent-1 my-agent)

;; Query state immutably
(get-in @app-state [:agents :agent-1])
```

## 🔍 Troubleshooting

### Problem: "Could not locate libpython"

**Solution:**
```clojure
;; Specify path manually in init.clj
(py/initialize! :python-executable "/usr/bin/python3"
                :library-path "/usr/lib/x86_64-linux-gnu/libpython3.10.so")

;; Or find correct path
;; Bash: find /usr/lib -name "libpython*.so*"
```

### Problem: "Class not found: com.google.adk.Agent"

**Solution:**
```bash
# Clear cache and reinstall dependencies
rm -rf .cpcache
clj -P  # Pre-fetch all dependencies
clj -M:dev  # Start REPL again
```

### Problem: REPL slow startup

**Solution:**
```clojure
;; Add to deps.edn :jvm-opts for faster startup
:jvm-opts ["-XX:+TieredCompilation"
           "-XX:TieredStopAtLevel=1"
           "-Xverify:none"]
```

### Problem: Permission denied on credentials

**Solution:**
```bash
# Set correct permissions
chmod 600 resources/credentials/*.json

# Verify .gitignore excludes them
grep -q "resources/credentials" .gitignore && echo "✅ Protected"
```

## 🔗 Related Skills

- [`cva-setup-interop`](../cva-setup-interop/SKILL.md) - Python interop configuration with libpython-clj
- [`cva-setup-vertex`](../cva-setup-vertex/SKILL.md) - Google Cloud and Vertex AI authentication setup
- [`cva-concepts-agent-types`](../cva-concepts-agent-types/SKILL.md) - Understanding different agent architectures
- [`cva-testing-repl`](../cva-testing-repl/SKILL.md) - REPL-driven testing strategies (if exists)
- [`cva-build-deploy`](../cva-build-deploy/SKILL.md) - Production build and deployment (if exists)

## 📘 Additional Documentation

### Performance Optimization

For production deployments, consider:
- AOT compilation for startup time
- GraalVM native-image for zero-startup
- JVM tuning for memory and GC
- Connection pooling for Google Cloud APIs

### IDE Integration

- **VS Code + Calva**: Full Clojure REPL integration
- **IntelliJ + Cursive**: Commercial Clojure IDE
- **Emacs + CIDER**: Traditional Lisp development
- **Vim + vim-fireplace**: Lightweight REPL integration

### References

- [Clojure CLI Tools](https://clojure.org/guides/deps_and_cli)
- [deps.edn Guide](https://clojure.org/reference/deps_and_cli)
- [Project Structure Best Practices](https://practical.li/clojure/clojure-cli/projects/)
- [REPL-Driven Development](https://practical.li/clojure/introduction/repl-workflow/)
