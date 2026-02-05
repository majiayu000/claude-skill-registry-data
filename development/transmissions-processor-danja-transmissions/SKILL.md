---
name: transmissions-processor
description: Guide for creating custom Transmissions processors with factory registration for core and remote development
---

# Transmissions Processor Creation Skill

This skill guides you through creating custom processors to extend Transmissions functionality, helping you choose between core and remote development.

## Quick Start Decision Tree

First check for an existing processor that can be used in `src/processors`. If the name is a reasonable match for the required functionality, check the processor's signature in comments in the code.

**Choose your development path:**

### Core Development (Recommended for reusable processors)
- ✅ Processors available to all apps
- ✅ Registered in framework factory
- ✅ Easy to test and debug
- ✅ Can be contributed to framework
- ❌ Requires framework modification

**Use when:** Building reusable processors, contributing to framework

### Remote Development (For app-specific processors)
- ✅ Keeps app self-contained
- ✅ Independent from framework
- ⚠️ Requires manual import paths
- ⚠️ Factory registration challenges
- ❌ More complex setup

**Use when:** Processor is app-specific, maintaining separation

## Workflow

### 1. Gather Information

Ask the user:
- **Processor name**: What should it be called? (e.g., `MyProcessor`)
- **Group name**: What category? (e.g., `my-group`, or use existing like `util`, `text`, `flow`)
- **Development location**: Core (`src/processors/`) or Remote (app-specific)?
- **Processor purpose**: What transformation does it perform?

### 2. Create Processor Structure

Execute based on chosen path:

#### For Core Development (New Group):

```bash
# Copy example group
cp -r src/processors/example-group src/processors/{GROUP_NAME}

# Rename processor file
mv src/processors/{GROUP_NAME}/Example.js src/processors/{GROUP_NAME}/{PROCESSOR_NAME}.js

# Rename factory
mv src/processors/{GROUP_NAME}/ExampleProcessorsFactory.js src/processors/{GROUP_NAME}/{GROUP_NAME}ProcessorsFactory.js

# List created files
ls -la src/processors/{GROUP_NAME}/
```

#### For Core Development (Existing Group):

```bash
# Just create new processor in existing group
# Example: adding to util/
touch src/processors/util/{PROCESSOR_NAME}.js
```

#### For Remote Development:

```bash
# Create in app's processor directory
mkdir -p ~/hyperdata/trans-apps/apps/{APP_NAME}/processors

# Copy example
cp src/processors/example-group/Example.js ~/hyperdata/trans-apps/apps/{APP_NAME}/processors/{PROCESSOR_NAME}.js

# Copy factory
cp src/processors/example-group/ExampleProcessorsFactory.js ~/hyperdata/trans-apps/apps/{APP_NAME}/processors/{PROCESSOR_NAME}Factory.js
```

### 3. Implement Processor

Edit the processor file:

**Basic structure:**
```javascript
// src/processors/{GROUP}/{ PROCESSOR_NAME}.js

import logger from '../../utils/Logger.js'
import ns from '../../utils/ns.js'
import Processor from '../../model/Processor.js'

/**
 * @class {PROCESSOR_NAME}
 * @extends Processor
 * @classdesc
 * {PROCESSOR_DESCRIPTION}
 *
 * ### Processor Signature
 * #### __*Settings*__
 * * **`ns.trn.settingName`** - Description
 *
 * #### __*Input*__
 * * **`message.field`** - Expected input
 *
 * #### __*Output*__
 * * **`message.result`** - Output field
 */
class {PROCESSOR_NAME} extends Processor {
    constructor(config) {
        super(config)
    }

    async process(message) {
        logger.debug(`{PROCESSOR_NAME}.process`)

        // Skip if spawning completion
        if (message.done) {
            return this.emit('message', message)
        }

        // Get configuration
        const setting = super.getProperty(ns.trn.settingName, 'default')

        // Process message
        // YOUR LOGIC HERE

        // Emit result
        return this.emit('message', message)
    }
}

export default {PROCESSOR_NAME}
```

### 4. Update Factory

Edit factory file to register processor:

**For new group:**
```javascript
// src/processors/{GROUP}/{GROUP}ProcessorsFactory.js

import logger from '../../utils/Logger.js'
import ns from '../../utils/ns.js'
import {PROCESSOR_NAME} from './{PROCESSOR_NAME}.js'

class {GROUP}ProcessorsFactory {
    static createProcessor(type, config) {
        if (type.equals(ns.trn.{PROCESSOR_NAME})) {
            return new {PROCESSOR_NAME}(config)
        }
        // Add more processors here
        return false
    }
}

export default {GROUP}ProcessorsFactory
```

**For existing group:**
Add to existing factory file:
```javascript
import {PROCESSOR_NAME} from './{PROCESSOR_NAME}.js'

// In createProcessor method:
if (type.equals(ns.trn.{PROCESSOR_NAME})) {
    return new {PROCESSOR_NAME}(config)
}
```

### 5. Register in AbstractProcessorFactory

**For core processors only:**

Edit `src/engine/AbstractProcessorFactory.js`:

```javascript
// Add import at top
import {GROUP}ProcessorsFactory from '../processors/{GROUP}/{GROUP}ProcessorsFactory.js'

// Add to createProcessor method
static createProcessor(type, app) {
    // ... existing processors ...

    var processor = {GROUP}ProcessorsFactory.createProcessor(type, app)
    if (processor) return processor

    // ... rest of factories ...
}
```

### 6. Test Processor

Create test app:

```bash
# Create test app
mkdir -p src/apps/test/{PROCESSOR_NAME}-test

# Create transmissions.ttl
cat > src/apps/test/{PROCESSOR_NAME}-test/transmissions.ttl << 'EOF'
@prefix : <http://purl.org/stuff/transmissions/> .

:test a :EntryTransmission ;
    :pipe (:setup :test-processor :verify) .

:setup a :SetField ;
    :settings [
        :field "testInput" ;
        :value "test-value"
    ] .

:test-processor a :{PROCESSOR_NAME} ;
    :settings [
        :settingName "test-setting"
    ] .

:verify a :ShowMessage .
EOF
```

Run test:
```bash
./trans test.{PROCESSOR_NAME}-test -v
```

## Quick Reference

### Common Processor Patterns

See [templates/processor-template.md](templates/processor-template.md) for:
- Simple transformation
- Property manipulation
- Async operations
- Error handling
- State management

### Factory Registration

See [templates/factory-guide.md](templates/factory-guide.md) for:
- Factory structure
- Type checking
- Multiple processors
- Error handling

### Testing Strategies

See [templates/testing.md](templates/testing.md) for:
- Unit testing
- Integration testing
- Test app creation
- Debugging techniques

## Common Issues

**Processor not found:**
- Check factory registration
- Verify import paths
- Check AbstractProcessorFactory.js includes your factory

**Type mismatch:**
- Verify `ns.trn.{PROCESSOR_NAME}` matches transmissions.ttl
- Check factory uses `type.equals()` not `===`

**Import errors:**
- Check relative paths in imports
- For remote: paths may be very long (../../../../../../)

## Next Steps

After basic processor creation:
1. Implement core logic in `process()` method
2. Add comprehensive JSDoc comments
3. Create test apps
4. Add to integration tests
5. Document in processor's about.md
6. Consider contributing to core if reusable

## Reference

- Example processor: `src/processors/example-group/Example.js`
- Processor base class: `src/model/Processor.js`
- Factory pattern: `src/engine/AbstractProcessorFactory.js`
- Manual: `docs/manual/dev/processors.md`
