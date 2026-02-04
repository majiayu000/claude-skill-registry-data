---
name: windev-to-golang
description: Convert Windev (WLanguage) systems to Go, including procedures, functions, web services, and file operations. Handles initialization code, service endpoints, and database operations. Uses Gin for APIs and Zap for logging. Maintains descriptive comments while ignoring commented code.
---

# Windev to Golang Conversion

Convert Windev (WLanguage) code to idiomatic Go, maintaining functionality while adapting to Go best practices.

## Core Conversion Principles

### 1. Comment Handling
- **IGNORE**: Code commented out in Windev (lines starting with `//` at the beginning)
- **PRESERVE**: Descriptive comments explaining functionality, actions, and observations
- **TRANSLATE**: Convert Windev comment style to Go comment style
- Add Go documentation comments (starting with function name) for exported functions

### 2. Code Structure
- Convert Windev procedures to Go functions
- Convert Windev web services to Gin handlers
- Transform initialization code to `main()` or `init()` functions
- Adapt cleanup/finalization code to use `defer` statements

### 3. Mandatory Packages
- **Logging**: Use `go.uber.org/zap` for all logging operations
- **APIs**: Use `github.com/gin-gonic/gin` for web services and REST APIs
- **Database**: Use `database/sql` with appropriate drivers

### 4. Function Discovery
When encountering Windev functions without known Go equivalents:
- Check references/wlanguage-mapping.md first
- If not found, ASK the user: "I need a Go implementation for the Windev function `[FunctionName]`. Can you provide the equivalent or describe what it does?"
- Wait for clarification before proceeding
- Document new mappings for future reference

## Conversion Workflow

### Step 1: Analyze Source Code

Read the Windev code and identify:
- Procedures and functions
- Web service endpoints
- Database operations (HyperFileSQL or SQL)
- File operations
- Initialization/cleanup sections
- Global variables and constants
- External dependencies

### Step 2: Load Reference Materials

Always read these references before conversion:
```bash
view references/wlanguage-mapping.md  # Function mappings
view references/windev-patterns.md    # Common patterns
```

### Step 3: Plan Go Structure

Determine:
- Package organization
- Required imports
- Global variables (minimize these)
- Configuration approach
- Error handling strategy

### Step 4: Convert Code

Follow these priorities:
1. Convert structures and types first
2. Convert utility functions
3. Convert business logic procedures
4. Convert API handlers last
5. Add proper error handling throughout
6. Add logging at key points

### Step 5: Add Infrastructure

- Create `main.go` with initialization
- Setup database connection with pooling
- Configure Zap logger (development or production mode)
- Setup Gin router with middleware
- Add health check endpoint

## Conversion Guidelines

### Procedures to Functions

**Windev:**
```wlanguage
PROCEDURE CalculateTotal(nQuantity is int, rPrice is real)
// Calculate the total with tax
rTotal is real
rTotal = nQuantity * rPrice * 1.15
RESULT rTotal
```

**Go:**
```go
// CalculateTotal calculates the total price with tax
// quantity: number of items
// price: price per item
// Returns: total price including 15% tax
func CalculateTotal(quantity int, price float64) float64 {
    // Calculate the total with tax
    total := float64(quantity) * price * 1.15
    return total
}
```

### Web Services to Gin Handlers

**Windev:**
```wlanguage
PROCEDURE ws_GetProduct(nProductID is int)
stProduct is ST_Product

HReadSeek(Product, ProductID, nProductID)
IF HFound() THEN
    stProduct.Name = Product.Name
    stProduct.Price = Product.Price
    WebserviceWriteHTTPCode(200)
    RESULT VariantToJSON(stProduct)
ELSE
    WebserviceWriteHTTPCode(404)
    RESULT "Product not found"
END
```

**Go:**
```go
// GetProduct retrieves a product by ID
// Converted from Windev: ws_GetProduct
func GetProduct(c *gin.Context) {
    productID, err := strconv.Atoi(c.Param("id"))
    if err != nil {
        logger.Error("invalid product ID", zap.Error(err))
        c.JSON(400, gin.H{"error": "Invalid product ID"})
        return
    }
    
    var product Product
    query := "SELECT id, name, price FROM products WHERE id = $1"
    err = db.QueryRow(query, productID).Scan(&product.ID, &product.Name, &product.Price)
    
    if err == sql.ErrNoRows {
        logger.Warn("product not found", zap.Int("productID", productID))
        c.JSON(404, gin.H{"error": "Product not found"})
        return
    }
    
    if err != nil {
        logger.Error("database error", zap.Error(err))
        c.JSON(500, gin.H{"error": "Internal server error"})
        return
    }
    
    logger.Info("product retrieved", zap.Int("productID", productID))
    c.JSON(200, product)
}
```

### Database Operations

Convert HyperFileSQL operations to SQL queries:

**Windev:**
```wlanguage
FOR EACH Product WHERE Category = sCategory
    stProduct.Name = Product.Name
    ArrayAdd(arrProducts, stProduct)
END
```

**Go:**
```go
query := "SELECT id, name, price FROM products WHERE category = $1"
rows, err := db.Query(query, category)
if err != nil {
    logger.Error("query failed", zap.Error(err))
    return nil, fmt.Errorf("failed to query products: %w", err)
}
defer rows.Close()

var products []Product
for rows.Next() {
    var product Product
    if err := rows.Scan(&product.ID, &product.Name, &product.Price); err != nil {
        logger.Error("scan failed", zap.Error(err))
        return nil, fmt.Errorf("failed to scan product: %w", err)
    }
    products = append(products, product)
}

if err = rows.Err(); err != nil {
    logger.Error("rows error", zap.Error(err))
    return nil, fmt.Errorf("error iterating products: %w", err)
}
```

### File Operations

**Windev:**
```wlanguage
nFileID is int = fOpen(sFilePath, foRead)
WHILE NOT fEndOfFile(nFileID)
    sLine = fReadLine(nFileID)
    // Process line
END
fClose(nFileID)
```

**Go:**
```go
file, err := os.Open(filePath)
if err != nil {
    logger.Error("cannot open file", zap.String("path", filePath), zap.Error(err))
    return fmt.Errorf("cannot open file: %w", err)
}
defer file.Close()

scanner := bufio.NewScanner(file)
for scanner.Scan() {
    line := scanner.Text()
    // Process line
}

if err := scanner.Err(); err != nil {
    logger.Error("scanner error", zap.Error(err))
    return fmt.Errorf("error reading file: %w", err)
}
```

### Error Handling

Always use explicit error handling:

**Windev:**
```wlanguage
WHEN EXCEPTION
    Error("Operation failed: " + ExceptionInfo())
END
bResult = DangerousOperation()
```

**Go:**
```go
result, err := DangerousOperation()
if err != nil {
    logger.Error("operation failed", zap.Error(err))
    return fmt.Errorf("operation failed: %w", err)
}
```

## Logging Standards

Use Zap logger consistently:

```go
// Initialization
logger, _ := zap.NewProduction()
defer logger.Sync()

// Debug (detailed diagnostic info)
logger.Debug("processing item", zap.Int("itemID", id))

// Info (general informational messages)
logger.Info("user created", zap.String("username", username))

// Warn (warning conditions)
logger.Warn("item not found", zap.Int("itemID", id))

// Error (error conditions)
logger.Error("database connection failed", zap.Error(err))

// Fatal (application terminating errors)
logger.Fatal("cannot start server", zap.Error(err))
```

## Project Structure

Organize converted code:

```
project/
├── main.go              # Application entry point
├── handlers.go          # Gin HTTP handlers (converted web services)
├── models.go            # Data structures
├── database.go          # Database operations
├── config.go            # Configuration management
├── utils.go             # Utility functions (converted procedures)
├── go.mod               # Go module definition
├── go.sum               # Dependencies checksums
└── .env.example         # Environment variables template
```

## Templates

Use templates from `assets/go-templates/`:
- `main.go`: Application initialization and server setup
- `handlers.go`: Example API handlers with CRUD operations
- `go.mod`: Module definition with required dependencies
- `.env.example`: Environment configuration template

Copy templates to workspace and adapt to specific needs.

## Common Conversions

### Variable Declarations

| Windev | Go |
|--------|-----|
| `nValue is int` | `var value int` or `value := 0` |
| `rPrice is real` | `var price float64` or `price := 0.0` |
| `sName is string` | `var name string` or `name := ""` |
| `bFlag is boolean` | `var flag bool` or `flag := false` |
| `dDate is date` | `var date time.Time` |
| `arrItems is array of X` | `var items []X` or `items := make([]X, 0)` |

### Control Structures

| Windev | Go |
|--------|-----|
| `IF ... END` | `if { }` |
| `SWITCH ... END` | `switch { }` |
| `FOR ... END` | `for { }` |
| `WHILE ... END` | `for condition { }` |
| `FOR EACH ... END` | `for _, item := range items { }` |

### Constants

| Windev | Go |
|--------|-----|
| `CONSTANT X = 10` | `const X = 10` |
| `True / False` | `true / false` |
| `Null` | `nil` |
| `CRLF` | `"\n"` |

## Conversion Checklist

For each Windev file:
- [ ] Read and understand the code purpose
- [ ] Identify all procedures and functions
- [ ] Check for unknown Windev functions (ask user if needed)
- [ ] Remove commented code (lines starting with `//`)
- [ ] Preserve descriptive comments
- [ ] Convert variable declarations
- [ ] Convert control structures
- [ ] Convert database operations to SQL
- [ ] Convert file operations to Go standard library
- [ ] Add error handling
- [ ] Add Zap logging
- [ ] Convert web services to Gin handlers
- [ ] Test converted code logic
- [ ] Add function documentation
- [ ] Organize into appropriate package structure

## Best Practices

1. **Error Handling**: Never ignore errors. Always check and handle appropriately.
2. **Context Usage**: Use `context.Context` for API handlers and database operations.
3. **Database Connections**: Use connection pooling, set reasonable limits.
4. **Logging**: Log at appropriate levels (Debug, Info, Warn, Error, Fatal).
5. **Configuration**: Use environment variables for configuration.
6. **Testing**: Write tests for converted business logic.
7. **Documentation**: Document exported functions with Go doc comments.
8. **Code Style**: Follow Go conventions (gofmt, golint).

## Common Pitfalls

- **Not checking errors**: Go requires explicit error handling
- **Ignoring context**: Always use context for cancellation and timeouts
- **SQL injection**: Use parameterized queries, never string concatenation
- **Not closing resources**: Use `defer` for cleanup (files, connections, etc.)
- **Global state**: Minimize use of global variables
- **Panic usage**: Prefer returning errors over `panic()`

## Example Conversion Session

User provides Windev code → Load references → Identify unknown functions → Ask user if needed → Convert procedures → Convert web services → Add infrastructure → Test → Deliver complete Go project

## Additional Resources

When converting complex Windev systems:
- Consult `references/wlanguage-mapping.md` for function mappings
- Review `references/windev-patterns.md` for common patterns
- Use templates from `assets/go-templates/` as starting point
- Ask user for clarification on business logic when needed
- Document any custom Windev functions for future reference
