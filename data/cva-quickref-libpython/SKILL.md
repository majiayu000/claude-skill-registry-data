---
name: cva-quickref-libpython
description: Quick reference cheatsheet for libpython-clj Python interop. Includes initialization, module imports, function calls, data conversions, NumPy/Pandas/Transformers patterns, and troubleshooting. Use when calling Python from Clojure, using Python libraries, or debugging interop issues.
allowed-tools: Read,Bash,Edit,Write
---

# libpython-clj Quick Reference

> **Purpose:** Fast API reference for Python interop in Clojure
> **Target:** Developers integrating Python libraries with Clojure

## 🎯 Quick Start

```clojure
;; Most common operations - copy-paste ready

;; 1. Initialize Python
(require '[libpython-clj2.python :as py])
(py/initialize!)

;; 2. Import Python module
(require '[libpython-clj2.require :refer [require-python]])
(require-python '[numpy :as np])

;; 3. Call Python function
(np/array [1 2 3])

;; 4. Convert Python → Clojure
(py/->jvm python-obj)

;; 5. Convert Clojure → Python
(py/->py clojure-data)

;; REPL test:
;; (require '[libpython-clj2.python :as py])
;; (py/initialize!)
;; => :ok
```

## 📚 Complete Reference

### Setup & Dependencies

**deps.edn:**
```clojure
{:deps {clj-python/libpython-clj {:mvn/version "2.025"}}}

;; REPL test:
;; (require '[libpython-clj2.python :as py]) => should not error
```

**Namespace Requires:**
```clojure
(require '[libpython-clj2.python :as py])
(require '[libpython-clj2.require :refer [require-python]])

;; REPL test:
;; (resolve 'py/initialize!) => should show function
```

### Initialization

**Auto-detect (recommended):**
```clojure
(py/initialize!)

;; Finds Python automatically
;; Works with system Python, pyenv, conda
;; REPL test:
;; (py/initialize!) => :ok
```

**Manual (specific Python):**
```clojure
(py/initialize!
  :python-executable "/usr/bin/python3"
  :library-path "/usr/lib/libpython3.10.so")

;; Use when auto-detect fails
;; REPL test:
;; Check paths exist first:
;; (.exists (java.io.File. "/usr/bin/python3"))
```

**With Virtual Environment:**
```clojure
(py/initialize!
  :python-executable ".venv/bin/python")

;; Automatically finds venv's Python
;; REPL test:
;; (py/initialize! :python-executable ".venv/bin/python")
;; See also: #troubleshooting-venv
```

### Module Imports

**Clojure Style (recommended):**
```clojure
(require-python '[numpy :as np])
(require-python '[pandas :as pd])
(require-python '[transformers :as hf])

;; Direct usage like Clojure namespaces
(np/array [1 2 3])
(pd/DataFrame {:a [1 2 3]})

;; REPL test:
;; (require-python '[builtins :as python])
;; (python/len [1 2 3]) => 3
```

**Python Style (explicit):**
```clojure
(def np (py/import-module "numpy"))
(def pd (py/import-module "pandas"))

;; Need py/ prefix for calls
(py/call-attr np "array" [1 2 3])

;; REPL test:
;; (def math (py/import-module "math"))
;; (py/call-attr math "sqrt" 16) => 4.0
```

**Submodule Imports:**
```clojure
(require-python '[sklearn.ensemble :as ensemble])
(require-python '[sklearn.model_selection :as ms])

;; Usage:
(ensemble/RandomForestClassifier :n_estimators 100)

;; REPL test:
;; (require-python '[os.path :as path])
;; (path/exists "/tmp") => True
```

### Function Calls

**Direct Call (with require-python):**
```clojure
(np/mean data)
(np/std data)
(pd/read_csv "file.csv")

;; REPL test:
;; (require-python '[builtins :as py])
;; (py/sum [1 2 3]) => 6
```

**call-attr (explicit):**
```clojure
(py/call-attr np "mean" data)
(py/call-attr pd "read_csv" "file.csv")

;; REPL test:
;; (def np (py/import-module "numpy"))
;; (py/call-attr np "array" [1 2 3])
```

**With Keyword Arguments:**
```clojure
(py/call-attr-kw np "linspace"
                 [0 10]          ; positional args
                 {:num 50        ; keyword args
                  :dtype "float64"})

;; REPL test:
;; (require-python '[builtins :as py])
;; (py/call-attr-kw py "print" ["hello"] {:end " world\n"})
```

**py. Syntax (Java-like):**
```clojure
(py. np mean data)
(py. df describe)

;; REPL test:
;; (require-python '[math])
;; (py. math sqrt 16) => 4.0
```

### Data Conversions

**Automatic Conversions:**

| Python | Clojure | Notes |
|--------|---------|-------|
| `int`, `float` | `Long`, `Double` | Automatic |
| `str` | `String` | Automatic |
| `list` | `vector` | Automatic |
| `tuple` | `vector` | Both become vectors |
| `dict` | `map` | Automatic |
| `True`/`False` | `true`/`false` | Automatic |
| `None` | `nil` | Automatic |

```clojure
;; REPL test:
;; (require-python '[builtins :as py])
;; (py/->jvm (py/dict {:a 1 :b 2})) => {"a" 1 "b" 2}
```

**Manual Conversions:**
```clojure
;; Python → Clojure
(py/->jvm python-obj)                ; Generic conversion
(py/->jvm (np/array [1 2 3]))       ; => [1 2 3]

;; Clojure → Python
(py/->py clojure-data)               ; Generic conversion
(py/->py-dict {:a 1 :b 2})          ; Explicit dict
(py/->py-list [1 2 3])              ; Explicit list

;; REPL test:
;; (py/->py {:a 1}) => Python dict
;; (py/->jvm (py/->py {:a 1})) => {"a" 1}
```

**Nested Structures:**
```clojure
(py/->py {:data [1 2 3]
          :nested {:a 1 :b 2}})

;; REPL test:
;; (def result (py/->py {:x [1 2 3]}))
;; (py/python-type result) => <class 'dict'>
```

### Attribute Access

**Get Attribute:**
```clojure
(py/get-attr obj "attribute")
(py. obj attribute)

;; Example:
(py/get-attr (np/array [1 2 3]) "shape")  ; => (3,)

;; REPL test:
;; (require-python '[sys])
;; (py/get-attr sys "version") => Python version string
```

**Set Attribute:**
```clojure
(py/set-attr! obj "attribute" value)

;; Example:
(py/set-attr! my-object "name" "new-name")

;; REPL test:
;; (def obj (py/import-module "types"))
;; (py/set-attr! obj "custom" 42)
;; (py/get-attr obj "custom") => 42
```

**Check Attribute:**
```clojure
(py/has-attr? obj "attribute")

;; REPL test:
;; (require-python '[sys])
;; (py/has-attr? sys "version") => true
;; (py/has-attr? sys "nonexistent") => false
```

**List Attributes:**
```clojure
(py/dir obj)

;; Returns all attributes/methods
;; REPL test:
;; (require-python '[math])
;; (py/dir math) => ["sin", "cos", "sqrt", ...]
```

### Indexing & Slicing

**Get Item:**
```clojure
(py/get-item arr 0)                  ; First element
(py/get-item dict "key")             ; Dictionary value

;; REPL test:
;; (require-python '[builtins :as py])
;; (py/get-item [1 2 3] 0) => 1
```

**Set Item:**
```clojure
(py/set-item! arr 0 value)
(py/set-item! dict "key" value)

;; REPL test:
;; (def lst (py/->py [1 2 3]))
;; (py/set-item! lst 0 99)
;; (py/get-item lst 0) => 99
```

**Slicing:**
```clojure
(py/get-item arr (py/slice 0 10))           ; [0:10]
(py/get-item arr (py/slice 0 10 2))         ; [0:10:2]
(py/get-item arr (py/slice nil nil -1))     ; [::-1] reverse

;; REPL test:
;; (require-python '[numpy :as np])
;; (def arr (np/arange 0 10))
;; (py/get-item arr (py/slice 0 5)) => [0 1 2 3 4]
```

## 💡 Common Library Patterns

### NumPy

```clojure
(require-python '[numpy :as np])

;; Array creation
(np/array [1 2 3 4 5])
(np/zeros 10)                        ; [0 0 0 ... 0]
(np/ones [3 3])                      ; 3x3 matrix of 1s
(np/arange 0 10 0.5)                 ; [0 0.5 1.0 ... 9.5]
(np/linspace 0 1 100)                ; 100 points from 0 to 1

;; Statistics
(np/mean arr)
(np/std arr)
(np/sum arr)
(np/max arr)
(np/min arr)
(np/median arr)

;; Indexing
(py/get-item arr 0)                  ; Single element
(py/get-item arr (py/slice 0 5))    ; Slice

;; REPL test:
;; (def arr (np/array [1 2 3 4 5]))
;; (np/mean arr) => 3.0
;; See also: #numpy-analysis-example
```

### Pandas

```clojure
(require-python '[pandas :as pd])

;; Create DataFrame
(def df (pd/DataFrame {:a [1 2 3]
                        :b [4 5 6]}))

;; Read CSV
(def df (pd/read_csv "data.csv"))

;; Access columns
(py/get-item df "a")                 ; Get column 'a'
(py. df head)                        ; First 5 rows
(py. df describe)                    ; Statistics

;; Convert to Clojure
(defn df->clj [df]
  (py/->jvm (py. df to_dict "records")))

;; REPL test:
;; (def df (pd/DataFrame {:x [1 2 3]}))
;; (py/get-attr df "shape") => (3, 1)
;; See also: #pandas-dataframe-example
```

### Transformers (HuggingFace)

```clojure
(require-python '[transformers :as hf])

;; Pipeline (easiest)
(def sentiment (hf/pipeline "sentiment-analysis"))
(sentiment "I love Clojure!")

;; Model & Tokenizer (advanced)
(def tokenizer (hf/AutoTokenizer.from_pretrained "bert-base-uncased"))
(def model (hf/AutoModel.from_pretrained "bert-base-uncased"))

;; Tokenize
(def inputs (tokenizer "Hello world"))

;; Inference
(def outputs (model inputs))

;; REPL test:
;; (def classifier (hf/pipeline "zero-shot-classification"))
;; (classifier "This is a test" ["positive" "negative"])
;; See also: cva-patterns-huggingface
```

### Scikit-learn

```clojure
(require-python '[sklearn.ensemble :as ensemble])
(require-python '[sklearn.model_selection :as ms])

;; Create classifier
(def clf (ensemble/RandomForestClassifier :n_estimators 100))

;; Train
(py. clf fit X y)

;; Predict
(py. clf predict X-test)

;; Evaluate
(py. clf score X-test y-test)

;; REPL test:
;; (require-python '[sklearn.datasets :as datasets])
;; (def iris (datasets/load_iris))
;; (py/get-item iris "data")
;; See also: #ml-pipeline-example
```

## 🎨 Advanced Patterns

### Idiomatic Wrapper Functions

```clojure
(defn analyze-sentiment
  "Clojure wrapper for HuggingFace sentiment analysis"
  [text]
  (let [result (first (@sentiment-pipeline text))]
    {:label (py/get-item result "label")
     :score (py/get-item result "score")}))

;; Usage:
(analyze-sentiment "I love this!")
;; => {:label "POSITIVE" :score 0.9998}

;; REPL test:
;; Create pipeline first, then test wrapper
```

### Context Manager (with statement)

```clojure
;; Python: with open(file) as f:
(py/with [f (py/call-attr (py/import-module "builtins")
                          "open" "file.txt" "r")]
  (py/call-attr f "read"))

;; REPL test:
;; (py/with [f (py/call-attr (py/import-module "tempfile")
;;                           "TemporaryFile" "w+")]
;;   (py/call-attr f "write" "test"))
```

### Lazy Module Loading

```clojure
(defonce numpy
  (delay
    (require-python '[numpy :as np])
    np))

(defn use-numpy []
  (@numpy/array [1 2 3]))

;; Only loads when first used
;; REPL test:
;; (realized? numpy) => false
;; (use-numpy)
;; (realized? numpy) => true
```

### Error Handling

```clojure
(defn safe-python-call
  "Call Python function with error handling"
  [f & args]
  (try
    (apply f args)
    (catch Exception e
      (println "Python error:" (.getMessage e))
      nil)))

;; REPL test:
;; (safe-python-call np/array "not-a-valid-input")
;; => Python error: ...
;; => nil
```

## 🔧 Special Types

```clojure
;; Slice
(py/slice start stop)                ; [start:stop]
(py/slice start stop step)           ; [start:stop:step]

;; None
py/None                              ; Python's None

;; Ellipsis
py/...                               ; Python's ...

;; *args expansion
(py/call-attr-kw func [] {:*args args-list})

;; **kwargs expansion
(py/call-attr-kw func [] {:**kwargs kwargs-map})

;; REPL test:
;; (= py/None nil) => false (different types!)
;; (py/python-type py/None) => <class 'NoneType'>
```

## 🐛 Debug & Introspection

```clojure
;; Python type
(py/python-type obj)                 ; => <class 'numpy.ndarray'>

;; List attributes/methods
(py/dir obj)                         ; => ["mean", "std", ...]

;; Python help
(py/call-attr (py/import-module "builtins") "help" obj)

;; Type checking
(py/isinstance obj type-obj)         ; => true/false

;; Is callable?
(py/callable? obj)                   ; => true/false

;; REPL test:
;; (require-python '[numpy :as np])
;; (py/dir (np/array [1 2 3]))
```

## ⚡ Performance

```clojure
;; Make function faster (cache)
(def fast-func (py/make-fastcallable python-func))

;; GIL context (thread safety)
(py/with-gil-stack-rc-context
  (numpy-operation))

;; Disable auto-conversion (faster)
(binding [py/*manual-gil* true]
  (python-operation))

;; REPL test:
;; Compare timing:
;; (time (dotimes [_ 1000] (np/mean data)))
;; (def fast-mean (py/make-fastcallable np/mean))
;; (time (dotimes [_ 1000] (fast-mean data)))
```

## 📝 Best Practices

```clojure
;; ✅ Good: Idiomatic Clojure wrapper
(defn process-data
  "Process data using Python library"
  [data]
  (-> data
      (py/->py-list)                 ; Convert to Python
      (python-function)              ; Process
      (py/->jvm)))                   ; Convert back

;; ❌ Avoid: Exposing interop details
(defn process-data [data]
  (py/call-attr python-lib "process" data))

;; ✅ Good: Type hints in docstring
(defn analyze
  "Analyze data array.
   Args: data (vector of numbers)
   Returns: map with :mean, :std"
  [data]
  ...)

;; REPL test:
;; Test conversions work correctly
```

## 🔍 Complete Examples

### NumPy Statistical Analysis

```clojure
(require-python '[numpy :as np])

(defn analyze-array
  "Comprehensive statistical analysis"
  [data]
  (let [arr (np/array data)]
    {:mean (np/mean arr)
     :std (np/std arr)
     :min (np/min arr)
     :max (np/max arr)
     :median (np/median arr)
     :quartiles [(np/percentile arr 25)
                 (np/percentile arr 50)
                 (np/percentile arr 75)]}))

;; REPL test:
;; (analyze-array [1 2 3 4 5 10 100])
;; => {:mean 17.857..., :std 34.48..., ...}
```

### Pandas DataFrame Processing

```clojure
(require-python '[pandas :as pd])

(defn load-and-analyze
  "Load CSV and perform analysis"
  [csv-path]
  (let [df (pd/read_csv csv-path)]
    {:shape (vec (py/get-attr df "shape"))
     :columns (vec (py/get-attr df "columns"))
     :summary (py/->jvm (py. df describe))
     :head (py/->jvm (py. df head))
     :dtypes (py/->jvm (py/get-attr df "dtypes"))}))

;; REPL test:
;; (load-and-analyze "test.csv")
;; => {:shape [100 5], :columns ["a" "b" ...], ...}
```

### Machine Learning Pipeline

```clojure
(require-python '[sklearn.model_selection :as ms]
                '[sklearn.ensemble :as ensemble])

(defn train-classifier
  "Train random forest classifier"
  [X y]
  (let [[X-train X-test y-train y-test]
        (ms/train_test_split X y :test_size 0.2 :random_state 42)

        clf (ensemble/RandomForestClassifier
              :n_estimators 100
              :random_state 42)]

    (py. clf fit X-train y-train)

    {:model clf
     :train-score (py. clf score X-train y-train)
     :test-score (py. clf score X-test y-test)
     :feature-importance (vec (py/get-attr clf "feature_importances_"))}))

;; REPL test:
;; (require-python '[sklearn.datasets :as datasets])
;; (def iris (datasets/load_iris))
;; (train-classifier (py/get-item iris "data")
;;                   (py/get-item iris "target"))
```

## 🚨 Troubleshooting

### "Unable to find library python3"

```clojure
;; Solution: Specify library path explicitly
(py/initialize!
  :library-path "/usr/lib/x86_64-linux-gnu/libpython3.10.so")

;; Find library:
;; $ find /usr -name "libpython*.so" 2>/dev/null

;; REPL test:
;; (py/initialize! :library-path "/path/to/libpython3.10.so")
```

### "Module not found"

```bash
# Install Python package first
pip install numpy pandas transformers

# Or in venv:
source .venv/bin/activate
pip install numpy
```

```clojure
;; Then initialize with venv Python
(py/initialize! :python-executable ".venv/bin/python")
```

### "GIL-related error"

```clojure
;; Use GIL context
(py/with-gil-stack-rc-context
  (python-operation))

;; REPL test:
;; Wrap problematic operations in context
```

### "Type conversion error"

```clojure
;; Manual conversion
(py/->py-list [1 2 3])               ; Explicit list
(py/->py-dict {:a 1})                ; Explicit dict

;; Check types
(py/python-type obj)                 ; What Python sees

;; REPL test:
;; (py/python-type (py/->py [1 2 3])) => <class 'list'>
```

## 🧪 REPL Testing Workflow

```clojure
(comment
  ;; 1. Test initialization
  (py/initialize!)

  ;; 2. Test import
  (require-python '[numpy :as np])

  ;; 3. Test basic call
  (np/array [1 2 3])

  ;; 4. Test conversion
  (py/->jvm (np/array [1 2 3]))      ; => [1 2 3]

  ;; 5. Test attributes
  (py/dir (py/import-module "sys"))

  ;; 6. Test error handling
  (try
    (np/array "invalid")
    (catch Exception e
      (.getMessage e)))

  ;; 7. Cleanup (if needed)
  ;; Python stays initialized for REPL session
  )
```

## 🔗 Related Skills

- [`cva-overview`](../cva-overview/SKILL.md) - Overall architecture
- [`cva-quickref-adk`](../cva-quickref-adk/SKILL.md) - ADK API reference
- [`cva-setup-vertex`](../cva-setup-vertex/SKILL.md) - Environment setup

## 📘 Official Documentation

- **GitHub:** https://github.com/clj-python/libpython-clj
- **Documentation:** https://clj-python.github.io/libpython-clj/
- **Examples:** https://github.com/clj-python/libpython-clj-examples
- **NumPy Docs:** https://numpy.org/doc/
- **Pandas Docs:** https://pandas.pydata.org/docs/
- **HuggingFace Docs:** https://huggingface.co/docs/transformers/
