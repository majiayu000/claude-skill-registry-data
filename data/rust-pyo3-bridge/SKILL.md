---
name: rust-pyo3-bridge
description: Bridge Rust and Python using PyO3 with proper GIL handling and async compatibility. Use when integrating Python ML models or libraries.
---

# PyO3 Python Bridge

Integrate Python code with Rust using PyO3 for ML inference and library access.

## Setup

```toml
# Cargo.toml
[dependencies]
pyo3 = { version = "0.20", features = ["auto-initialize"] }
```

## Basic Python Bridge Structure

```rust
use pyo3::prelude::*;
use pyo3::types::{PyList, PyModule};
use std::path::PathBuf;

pub struct PythonBridge {
    module_path: PathBuf,
    initialized: bool,
}

impl PythonBridge {
    pub fn new(module_path: PathBuf) -> Result<Self> {
        Ok(Self {
            module_path,
            initialized: false,
        })
    }

    /// Add module path to Python sys.path
    pub fn initialize(&mut self) -> Result<()> {
        if self.initialized {
            return Ok(());
        }

        Python::with_gil(|py| {
            let sys = PyModule::import(py, "sys")?;
            let path: &PyList = sys.getattr("path")?.downcast()?;

            let path_str = self.module_path.to_str()
                .ok_or_else(|| PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    "Invalid path"
                ))?;

            path.insert(0, path_str)?;
            Ok::<(), PyErr>(())
        })?;

        self.initialized = true;
        Ok(())
    }
}
```

## Path Resolution (Windows-Aware)

```rust
fn find_python_module() -> Result<PathBuf> {
    let candidates = vec![
        PathBuf::from("python"),
        PathBuf::from("../python"),
        // Absolute fallback for Windows
        PathBuf::from("E:/project/python"),
    ];

    for candidate in candidates {
        let init_file = candidate.join("module/__init__.py");
        if init_file.exists() {
            // Canonicalize and handle Windows extended-length paths
            let absolute = candidate.canonicalize()?;
            let path_str = absolute.to_string_lossy();

            // Strip Windows \\?\ prefix if present
            let clean_path = if path_str.starts_with(r"\\?\") {
                PathBuf::from(&path_str[4..])
            } else {
                absolute
            };

            return Ok(clean_path);
        }
    }

    Err(Error::ModuleNotFound)
}
```

## Calling Python Functions

```rust
impl PythonBridge {
    pub fn call_function(&self, func_name: &str, arg: &str) -> Result<String> {
        Python::with_gil(|py| {
            let module = PyModule::import(py, "my_module")?;

            let func = module.getattr(func_name)?;
            let result = func.call1((arg,))?;
            let output: String = result.extract()?;

            Ok(output)
        })
    }

    pub fn transcribe(&self, audio_path: &str) -> Result<String> {
        Python::with_gil(|py| {
            let embedders = PyModule::import(py, "embedders")?;

            let transcribe_fn = embedders.getattr("transcribe")?;
            let result = transcribe_fn.call1((audio_path,))?;
            let text: String = result.extract()?;

            Ok(text)
        })
    }
}
```

## Extracting Complex Types

```rust
pub fn embed_video(&self, video_path: &str) -> Result<Vec<f32>> {
    Python::with_gil(|py| {
        let embedders = PyModule::import(py, "embedders")?;

        let embed_fn = embedders.getattr("embed_video")?;
        let result = embed_fn.call1((video_path,))?;

        // Extract numpy array as Vec<f32>
        let embedding: Vec<f32> = result.extract()?;

        Ok(embedding)
    })
}

pub fn analyze_video(&self, video_path: &str) -> Result<VideoAnalysis> {
    Python::with_gil(|py| {
        let module = PyModule::import(py, "analyzer")?;

        let analyze_fn = module.getattr("analyze")?;
        let result = analyze_fn.call1((video_path,))?;

        // Extract dictionary fields
        let description: String = result
            .get_item("description")?
            .extract()
            .unwrap_or_default();

        let keywords: Vec<String> = result
            .get_item("keywords")
            .ok()
            .and_then(|v| v.extract().ok())
            .unwrap_or_default();

        let is_meme: bool = result
            .get_item("is_meme")
            .ok()
            .and_then(|v| v.extract().ok())
            .unwrap_or(false);

        Ok(VideoAnalysis {
            description,
            keywords,
            is_meme,
        })
    })
}
```

## Passing Lists to Python

```rust
pub fn embed_images(&self, image_paths: &[String]) -> Result<Vec<f32>> {
    Python::with_gil(|py| {
        let embedders = PyModule::import(py, "embedders")?;

        let embed_fn = embedders.getattr("embed_images")?;

        // Convert Vec<String> to Python list
        let py_list = PyList::new(py, image_paths);

        let result = embed_fn.call1((py_list,))?;
        let embedding: Vec<f32> = result.extract()?;

        Ok(embedding)
    })
}
```

## Async Integration with spawn_blocking

```rust
use tokio::task::spawn_blocking;

impl PythonBridge {
    /// Async-safe Python call
    pub async fn transcribe_async(&self, audio_path: String) -> Result<String> {
        // Clone self or relevant data for the closure
        let module_path = self.module_path.clone();

        spawn_blocking(move || {
            Python::with_gil(|py| {
                // Setup sys.path
                let sys = PyModule::import(py, "sys")?;
                let path: &PyList = sys.getattr("path")?.downcast()?;
                path.insert(0, module_path.to_str().unwrap())?;

                // Call Python
                let embedders = PyModule::import(py, "embedders")?;
                let result = embedders
                    .getattr("transcribe")?
                    .call1((&audio_path,))?;

                result.extract::<String>()
            })
        })
        .await?
        .map_err(|e| Error::Python(e.to_string()))
    }
}
```

## Releasing GIL for Parallelism

```rust
Python::with_gil(|py| {
    // Release GIL while doing non-Python work
    py.allow_threads(|| {
        // This Rust code runs without holding the GIL
        // Other Python threads can execute
        expensive_rust_computation()
    })
});
```

## GPU Memory Monitoring via pynvml

```rust
pub fn get_gpu_memory() -> Result<(u64, u64)> {
    Python::with_gil(|py| {
        let pynvml = PyModule::import(py, "pynvml")?;

        pynvml.call_method0("nvmlInit")?;

        let handle = pynvml.call_method1("nvmlDeviceGetHandleByIndex", (0,))?;
        let info = pynvml.call_method1("nvmlDeviceGetMemoryInfo", (handle,))?;

        let used: u64 = info.getattr("used")?.extract()?;
        let total: u64 = info.getattr("total")?.extract()?;

        Ok((used, total))
    })
}
```

## Model Loading and Unloading

```rust
impl PythonBridge {
    pub fn load_models(&mut self) -> Result<()> {
        Python::with_gil(|py| {
            let embedders = PyModule::import(py, "embedders")?;
            embedders.getattr("load_all_models")?.call0()?;
            Ok::<(), PyErr>(())
        })?;

        Ok(())
    }

    pub fn unload_models(&mut self) -> Result<()> {
        Python::with_gil(|py| {
            let embedders = PyModule::import(py, "embedders")?;
            embedders.getattr("unload_all_models")?.call0()?;
            Ok::<(), PyErr>(())
        })?;

        Ok(())
    }
}
```

## Error Handling

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum PythonError {
    #[error("Python import error: {0}")]
    Import(String),

    #[error("Python execution error: {0}")]
    Execution(String),

    #[error("Type conversion error: {0}")]
    TypeConversion(String),
}

impl From<PyErr> for PythonError {
    fn from(err: PyErr) -> Self {
        Python::with_gil(|py| {
            PythonError::Execution(err.to_string())
        })
    }
}
```

## Guidelines

- Always use `Python::with_gil()` for Python access
- Use `spawn_blocking` for async integration
- Use `py.allow_threads()` for parallel Rust work
- Handle Windows path prefixes (\\?\)
- Add module paths to sys.path before import
- Extract types safely with `.ok()` and `.unwrap_or_default()`
- Unload models to free GPU memory when done

## Examples

See `hercules-local-algo/src/python/mod.rs` for complete implementation.
