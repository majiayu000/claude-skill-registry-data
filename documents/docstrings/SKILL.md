---
name: docstrings
description: Generate comprehensive function, class, and module docstrings following language conventions (JSDoc, PyDoc, JavaDoc, XML docs, godoc, Doxygen). Use when.
---

# Docstring Generation

Generate comprehensive, standards-compliant docstrings for all public interfaces including modules, classes, functions, and methods.

## When to Use This Skill

Use this skill when you need to:

- Document function parameters and return values
- Add class and module documentation
- Generate API reference documentation
- Improve code discoverability
- Create self-documenting code
- Meet documentation requirements

**Trigger phrases**: "add docstrings", "document code", "generate docstrings", "API documentation", "JSDoc", "PyDoc", "JavaDoc", "godoc", "Doxygen"

## What This Skill Does

### Documentation Formats by Language

| Language | Format | Standard |
|----------|--------|----------|
| Python | Google/NumPy/reST | PEP 257 |
| JavaScript | JSDoc | JSDoc 3 |
| TypeScript | TSDoc | TSDoc |
| Java | JavaDoc | Oracle JavaDoc |
| C# | XML Documentation | Microsoft XML Comments |
| Go | godoc | Effective Go |
| C/C++ | Doxygen | Doxygen |

## Instructions

### Python Docstrings (Google Style)

```python
"""Module-level docstring describing the module's purpose.

This module provides utility functions for data processing
and validation. It supports multiple input formats and
includes comprehensive error handling.

Example:
    >>> from mymodule import process_data
    >>> result = process_data({"key": "value"})
    >>> print(result)
    {'key': 'VALUE'}

Attributes:
    DEFAULT_CONFIG (dict): Default configuration settings.
    SUPPORTED_FORMATS (list): List of supported file formats.
"""

def process_data(
    data: dict[str, Any],
    options: dict[str, Any] | None = None,
    *,
    strict: bool = False
) -> dict[str, Any]:
    """Process and transform input data according to rules.

    Validates input data, applies transformations based on
    configuration, and returns the processed result.

    Args:
        data: Input data dictionary to process.
        options: Optional processing options. Defaults to None.
        strict: If True, raise on warnings. Defaults to False.

    Returns:
        Processed data dictionary with transformations applied.

    Raises:
        ValueError: If data is empty or malformed.
        TypeError: If data is not a dictionary.
        ProcessingError: If transformation fails.

    Example:
        >>> result = process_data({"name": "test"})
        >>> print(result)
        {'name': 'TEST'}

    Note:
        This function modifies the input data in place when
        `options['in_place']` is True.
    """
    pass


class DataProcessor:
    """A class for processing and transforming data.

    This class provides methods for validating, transforming,
    and exporting data in various formats.

    Attributes:
        config: Configuration dictionary for processing.
        logger: Logger instance for this processor.

    Example:
        >>> processor = DataProcessor(config={'format': 'json'})
        >>> result = processor.process(data)
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the DataProcessor.

        Args:
            config: Configuration dictionary containing:
                - format (str): Output format ('json', 'csv')
                - validate (bool): Enable validation
                - strict (bool): Strict mode
        """
        pass
```

### JavaScript/TypeScript (JSDoc)

```javascript
/**
 * Module for data processing utilities.
 * @module dataProcessor
 */

/**
 * Process and transform input data.
 *
 * @param {Object} data - Input data to process
 * @param {string} data.name - Name field
 * @param {number} data.value - Value field
 * @param {Object} [options={}] - Processing options
 * @param {boolean} [options.strict=false] - Enable strict mode
 * @returns {Promise<Object>} Processed data object
 * @throws {ValidationError} If data validation fails
 * @throws {ProcessingError} If transformation fails
 *
 * @example
 * const result = await processData({ name: 'test', value: 42 });
 * console.log(result);
 * // { name: 'TEST', value: 42, processed: true }
 */
async function processData(data, options = {}) {
  // Implementation
}

/**
 * Data processor class for handling transformations.
 *
 * @class
 * @classdesc Provides methods for data validation and transformation.
 *
 * @example
 * const processor = new DataProcessor({ format: 'json' });
 * const result = processor.process(data);
 */
class DataProcessor {
  /**
   * Create a new DataProcessor.
   *
   * @param {Object} config - Configuration object
   * @param {string} config.format - Output format
   * @param {boolean} [config.validate=true] - Enable validation
   */
  constructor(config) {
    /** @type {Object} Configuration settings */
    this.config = config;
  }

  /**
   * Process the input data.
   *
   * @param {Object} data - Data to process
   * @returns {Object} Processed data
   * @memberof DataProcessor
   */
  process(data) {
    // Implementation
  }
}
```

### Java (JavaDoc)

```java
/**
 * Data processing utility class.
 *
 * <p>This class provides methods for validating, transforming,
 * and exporting data in various formats.</p>
 *
 * <p>Example usage:</p>
 * <pre>{@code
 * DataProcessor processor = new DataProcessor(config);
 * Result result = processor.process(data);
 * }</pre>
 *
 * @author Your Name
 * @version 1.0
 * @since 1.0
 * @see DataValidator
 * @see TransformationEngine
 */
public class DataProcessor {

    /**
     * Process and transform input data.
     *
     * <p>Validates the input, applies configured transformations,
     * and returns the processed result.</p>
     *
     * @param data the input data map to process
     * @param options optional processing configuration
     * @return processed data as a new map
     * @throws IllegalArgumentException if data is null or empty
     * @throws ProcessingException if transformation fails
     *
     * @see #validate(Map)
     * @since 1.0
     */
    public Map<String, Object> processData(
            Map<String, Object> data,
            ProcessingOptions options) throws ProcessingException {
        // Implementation
    }
}
```

### C# (XML Documentation)

```csharp
/// <summary>
/// Provides data processing and transformation capabilities.
/// </summary>
/// <remarks>
/// This class handles validation, transformation, and export
/// of data in various formats.
/// </remarks>
/// <example>
/// <code>
/// var processor = new DataProcessor(config);
/// var result = processor.Process(data);
/// </code>
/// </example>
public class DataProcessor
{
    /// <summary>
    /// Processes and transforms the input data.
    /// </summary>
    /// <param name="data">The input data dictionary to process.</param>
    /// <param name="options">Optional processing configuration.</param>
    /// <returns>
    /// A dictionary containing the processed data.
    /// </returns>
    /// <exception cref="ArgumentNullException">
    /// Thrown when <paramref name="data"/> is null.
    /// </exception>
    /// <exception cref="ProcessingException">
    /// Thrown when transformation fails.
    /// </exception>
    /// <seealso cref="Validate"/>
    public Dictionary<string, object> Process(
        Dictionary<string, object> data,
        ProcessingOptions options = null)
    {
        // Implementation
    }
}
```

### Go (godoc)

```go
// Package processor provides data processing utilities.
//
// This package contains functions and types for validating,
// transforming, and exporting data in various formats.
//
// Example:
//
//	processor := NewProcessor(config)
//	result, err := processor.Process(data)
//	if err != nil {
//	    log.Fatal(err)
//	}
package processor

// Processor handles data transformation operations.
type Processor struct {
    config Config
    logger *log.Logger
}

// NewProcessor creates a new Processor with the given configuration.
//
// The config parameter specifies processing options including
// output format, validation settings, and transformation rules.
func NewProcessor(config Config) *Processor {
    return &Processor{config: config}
}

// Process transforms the input data according to configuration.
//
// It validates the input, applies transformations, and returns
// the processed result. If validation or transformation fails,
// an error is returned.
//
// Example:
//
//	result, err := processor.Process(map[string]interface{}{
//	    "name": "test",
//	    "value": 42,
//	})
func (p *Processor) Process(data map[string]interface{}) (map[string]interface{}, error) {
    // Implementation
}
```

### C/C++ (Doxygen)

```cpp
/**
 * @file processor.h
 * @brief Data processing utilities
 * @author Your Name
 * @date 2025-12-08
 *
 * This module provides functions for data validation,
 * transformation, and export in various formats.
 */

/**
 * @brief Data processor class for handling transformations.
 *
 * This class provides methods for validating, transforming,
 * and exporting data. It supports multiple output formats
 * and includes comprehensive error handling.
 *
 * @code
 * Processor proc(config);
 * auto result = proc.process(data);
 * @endcode
 */
class Processor {
public:
    /**
     * @brief Process and transform input data.
     *
     * Validates the input data, applies configured transformations,
     * and returns the processed result.
     *
     * @param[in] data Input data to process
     * @param[in] options Processing options (optional)
     * @param[out] result Pointer to store the result
     * @return Status code (0 for success)
     * @retval 0 Success
     * @retval -1 Validation error
     * @retval -2 Transformation error
     *
     * @throws std::invalid_argument if data is null
     * @throws ProcessingException if transformation fails
     *
     * @pre data must not be null
     * @post result contains transformed data on success
     *
     * @see validate()
     * @since 1.0
     */
    int process(const Data* data, const Options* options, Result* result);
};
```

## Quality Checklist

- [ ] All public modules/packages documented
- [ ] All public classes documented
- [ ] All public functions/methods documented
- [ ] Parameters clearly described
- [ ] Return values documented
- [ ] Exceptions/errors documented
- [ ] Examples provided for complex APIs
- [ ] Type information included
- [ ] Consistent style throughout
- [ ] Documentation builds without errors

## Common Issues and Solutions

### Issue: Missing type information
**Solution**: Include type hints in function signatures and docstrings:
```python
def process(data: dict[str, Any]) -> Result:
    """Process data.

    Args:
        data: Input dictionary with string keys.

    Returns:
        Result object containing processed data.
    """
```

### Issue: Docstring doesn't match signature
**Solution**: Keep docstrings synchronized with code changes and use tools to validate.

### Issue: Examples don't work
**Solution**: Use doctest to verify examples:
```bash
python -m doctest module.py
```

## Related Skills

- `strategic-comments` - High-value code comments
- `api-documentation` - API reference documentation
- `user-documentation` - User guides and tutorials

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates documentation_generation/docstrings/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
