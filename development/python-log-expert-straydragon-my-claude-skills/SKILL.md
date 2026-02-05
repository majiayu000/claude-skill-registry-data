---
name: python-log-expert
description: Expert guidance for Python logging libraries including structlog, standard logging, and log analysis. Use when working with Python logs, troubleshooting logging issues, implementing logging best practices, or analyzing structlog source code implementation. Includes complete structlog source code in source/structlog/ for deep implementation analysis. Requires structlog package.
---

# Python Log Expert

Expert guidance for Python logging libraries including structlog, standard logging, and log analysis.

## Quick Start

### Basic structlog setup

```python
import structlog

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Get a logger
log = structlog.get_logger()
log.info("Hello, world!", user="alice")
```

### Standard logging integration

```python
import logging
import structlog

# Standard logging configuration
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

## Instructions

1. **Analyze logging requirements**: Determine if you need structured logging, standard logging, or both
2. **Configure logging**: Set up appropriate processors and formatters
3. **Implement context**: Add relevant context to your log messages
4. **Handle exceptions**: Use proper exception logging techniques
5. **Performance considerations**: Optimize logging for production use

### Deep Implementation Analysis

When you need to understand specific implementation details or troubleshoot complex issues, examine the actual source code:

- **How processors work**: Look at `source/structlog/src/structlog/processors.py` to understand the JSONRenderer, TimeStamper, and other processors
- **Context binding mechanism**: Examine `source/structlog/src/structlog/contextvars.py` for the actual contextvar implementation
- **Standard library bridge**: Study `source/structlog/src/structlog/stdlib.py` to understand how structlog integrates with Python's logging module
- **Logger factory patterns**: Review `source/structlog/src/structlog/_base.py` for the core BoundLogger implementation
- **Configuration defaults**: Check `source/structlog/src/structlog/_config.py` for default processor chains and settings

For detailed configuration options, see [REFERENCE.md](REFERENCE.md).
For practical examples, see [EXAMPLES.md](EXAMPLES.md).
For log analysis scripts, see [scripts/](scripts/) directory.

For actual implementation details and source code analysis, refer to the structlog source code in [source/structlog/src/structlog/](source/structlog/src/structlog/) - this contains the complete library source including processors, formatters, and core implementations that you can examine for deeper understanding.

## Requirements

The structlog package must be installed in your environment:

```bash
pip install structlog
```

## Best Practices

- Use structured logging with meaningful context
- Configure appropriate log levels for different environments
- Include correlation IDs for request tracking
- Use JSON formatting for machine-readable logs
- Implement proper error handling and exception logging
- Consider performance impact in high-throughput applications

## Source Code Analysis

For deep understanding of structlog internals, examine the source code:

- **Processors**: `source/structlog/src/structlog/processors.py` - Core data transformation logic including JSONRenderer, TimeStamper, etc.
- **Standard Library Integration**: `source/structlog/src/structlog/stdlib.py` - Logger factory and standard library bridging
- **Context Management**: `source/structlog/src/structlog/contextvars.py` - Context binding implementation
- **Core Configuration**: `source/structlog/src/structlog/_config.py` - Configuration management and defaults
- **Base Logger**: `source/structlog/src/structlog/_base.py` - Core logger implementation
- **Output Formatting**: `source/structlog/src/structlog/_output.py` - Output formatting and rendering logic
- **Development Tools**: `source/structlog/src/structlog/dev.py` - Console rendering for development
- **Testing**: `source/structlog/src/structlog/testing.py` - Testing utilities and helpers

## Troubleshooting

Common issues and solutions:

- **Logs not appearing**: Check log level configuration and examine `source/structlog/src/structlog/stdlib.py` for logger factory setup and BoundLogger implementation
- **Missing context**: Ensure proper context binding - see `source/structlog/src/structlog/contextvars.py` for implementation details
- **Performance issues**: Review processor chain in `source/structlog/src/structlog/processors.py` and output formatting - check TimeStamper and JSONRenderer optimizations
- **JSON formatting problems**: Verify context values are JSON-serializable - check `source/structlog/src/structlog/processors.py` for JSONRenderer implementation
- **Configuration issues**: Examine `source/structlog/src/structlog/_config.py` for default values and configuration logic