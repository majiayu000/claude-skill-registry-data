---
name: sequelize-models
description: Sequelize ORM model definition patterns and best practices for PostgreSQL. Use when defining models, setting up associations, configuring validations, or optimizing Sequelize usage.
---

# Sequelize Model Patterns

## Model Definition

### Basic Model Structure
```javascript
const { DataTypes, Model } = require('sequelize');

class User extends Model {
  // Instance methods
  getFullName() {
    return `${this.firstName} ${this.lastName}`;
  }

  // Class methods
  static async findByEmail(email) {
    return this.findOne({ where: { email: email.toLowerCase() } });
  }
}

User.init({
  id: {
    type: DataTypes.BIGINT,
    primaryKey: true,
    autoIncrement: true,
  },
  email: {
    type: DataTypes.TEXT,
    allowNull: false,
    unique: true,
    validate: {
      isEmail: true,
      notEmpty: true,
    },
    set(value) {
      this.setDataValue('email', value.toLowerCase());
    },
  },
  firstName: {
    type: DataTypes.TEXT,
    allowNull: false,
    field: 'first_name', // Maps to snake_case column
  },
  lastName: {
    type: DataTypes.TEXT,
    allowNull: false,
    field: 'last_name',
  },
  status: {
    type: DataTypes.TEXT,
    allowNull: false,
    defaultValue: 'active',
    validate: {
      isIn: [['active', 'inactive', 'suspended']],
    },
  },
  metadata: {
    type: DataTypes.JSONB,
    allowNull: false,
    defaultValue: {},
  },
}, {
  sequelize,
  modelName: 'User',
  tableName: 'users',
  underscored: true, // Automatically use snake_case for columns
  timestamps: true,  // Adds createdAt, updatedAt
  paranoid: false,   // Set true for soft deletes (adds deletedAt)
  indexes: [
    { fields: ['email'], unique: true },
    { fields: ['status'] },
    { fields: ['created_at'] },
  ],
});

module.exports = User;
```

## Data Type Mappings

### PostgreSQL ↔ Sequelize

| PostgreSQL | Sequelize DataType | Notes |
|------------|-------------------|-------|
| `BIGINT` | `DataTypes.BIGINT` | Use for IDs and large numbers |
| `INTEGER` | `DataTypes.INTEGER` | Standard integers |
| `NUMERIC(p,s)` | `DataTypes.DECIMAL(p,s)` | Money, precise decimals |
| `DOUBLE PRECISION` | `DataTypes.DOUBLE` | Floating point |
| `TEXT` | `DataTypes.TEXT` | Prefer over STRING/VARCHAR |
| `BOOLEAN` | `DataTypes.BOOLEAN` | True/false |
| `TIMESTAMPTZ` | `DataTypes.DATE` | Sequelize handles timezone |
| `DATE` | `DataTypes.DATEONLY` | Date without time |
| `JSONB` | `DataTypes.JSONB` | Structured JSON data |
| `UUID` | `DataTypes.UUID` | Use with UUIDV4 default |
| `TEXT[]` | `DataTypes.ARRAY(DataTypes.TEXT)` | Arrays |
| `INET` | `DataTypes.INET` | IP addresses |
| `CIDR` | `DataTypes.CIDR` | Network ranges |
| `MACADDR` | `DataTypes.MACADDR` | MAC addresses |

### ID Patterns
```javascript
// Auto-increment BIGINT (preferred)
id: {
  type: DataTypes.BIGINT,
  primaryKey: true,
  autoIncrement: true,
}

// UUID (when needed for distribution/opacity)
id: {
  type: DataTypes.UUID,
  primaryKey: true,
  defaultValue: DataTypes.UUIDV4,
}
```

### Avoid These Mappings
```javascript
// BAD: VARCHAR/STRING - use TEXT instead
name: DataTypes.STRING(255)  // Avoid
name: DataTypes.TEXT         // Prefer

// BAD: FLOAT for money
price: DataTypes.FLOAT       // Never
price: DataTypes.DECIMAL(10, 2)  // Always

// BAD: DATE without timezone
createdAt: DataTypes.DATE    // Actually OK - Sequelize uses TIMESTAMPTZ
```

## Associations

### One-to-Many
```javascript
// User has many Orders
User.hasMany(Order, {
  foreignKey: 'userId',
  as: 'orders',
  onDelete: 'CASCADE',
});

Order.belongsTo(User, {
  foreignKey: 'userId',
  as: 'user',
});

// Usage
const user = await User.findByPk(1, {
  include: [{ model: Order, as: 'orders' }],
});

const order = await Order.findByPk(1, {
  include: [{ model: User, as: 'user' }],
});
```

### Many-to-Many
```javascript
// Products belong to many Categories through ProductCategories
Product.belongsToMany(Category, {
  through: 'ProductCategories',
  foreignKey: 'productId',
  otherKey: 'categoryId',
  as: 'categories',
});

Category.belongsToMany(Product, {
  through: 'ProductCategories',
  foreignKey: 'categoryId',
  otherKey: 'productId',
  as: 'products',
});

// With junction table model (for extra fields)
class ProductCategory extends Model {}
ProductCategory.init({
  productId: {
    type: DataTypes.BIGINT,
    primaryKey: true,
  },
  categoryId: {
    type: DataTypes.BIGINT,
    primaryKey: true,
  },
  sortOrder: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
  },
}, { sequelize, modelName: 'ProductCategory', tableName: 'product_categories' });

Product.belongsToMany(Category, {
  through: ProductCategory,
  foreignKey: 'productId',
  as: 'categories',
});
```

### One-to-One
```javascript
User.hasOne(Profile, {
  foreignKey: 'userId',
  as: 'profile',
  onDelete: 'CASCADE',
});

Profile.belongsTo(User, {
  foreignKey: 'userId',
  as: 'user',
});
```

### Self-Referential
```javascript
// Categories with parent/children
Category.hasMany(Category, {
  foreignKey: 'parentId',
  as: 'children',
});

Category.belongsTo(Category, {
  foreignKey: 'parentId',
  as: 'parent',
});

// Hierarchical query
const category = await Category.findByPk(1, {
  include: [
    { model: Category, as: 'children' },
    { model: Category, as: 'parent' },
  ],
});
```

## Validations

### Built-in Validators
```javascript
email: {
  type: DataTypes.TEXT,
  validate: {
    isEmail: true,
    notEmpty: true,
  },
},
age: {
  type: DataTypes.INTEGER,
  validate: {
    min: 0,
    max: 150,
    isInt: true,
  },
},
website: {
  type: DataTypes.TEXT,
  validate: {
    isUrl: true,
  },
},
status: {
  type: DataTypes.TEXT,
  validate: {
    isIn: [['pending', 'active', 'completed']],
  },
},
username: {
  type: DataTypes.TEXT,
  validate: {
    len: [3, 50],
    isAlphanumeric: true,
  },
},
```

### Custom Validators
```javascript
price: {
  type: DataTypes.DECIMAL(10, 2),
  validate: {
    isPositive(value) {
      if (parseFloat(value) <= 0) {
        throw new Error('Price must be positive');
      }
    },
  },
},
startDate: {
  type: DataTypes.DATE,
  validate: {
    isBeforeEndDate(value) {
      if (this.endDate && value >= this.endDate) {
        throw new Error('Start date must be before end date');
      }
    },
  },
},
```

### Model-Level Validation
```javascript
User.init({
  // ... attributes
}, {
  sequelize,
  modelName: 'User',
  validate: {
    bothNamesOrNone() {
      if ((this.firstName === null) !== (this.lastName === null)) {
        throw new Error('Either both names or neither');
      }
    },
  },
});
```

## Hooks

### Available Hooks
```javascript
User.init({
  // ... attributes
}, {
  sequelize,
  modelName: 'User',
  hooks: {
    // Before/After validation
    beforeValidate: (user, options) => {},
    afterValidate: (user, options) => {},

    // Before/After create
    beforeCreate: (user, options) => {},
    afterCreate: (user, options) => {},

    // Before/After update
    beforeUpdate: (user, options) => {},
    afterUpdate: (user, options) => {},

    // Before/After save (create or update)
    beforeSave: (user, options) => {},
    afterSave: (user, options) => {},

    // Before/After destroy
    beforeDestroy: (user, options) => {},
    afterDestroy: (user, options) => {},

    // Bulk operations
    beforeBulkCreate: (users, options) => {},
    afterBulkCreate: (users, options) => {},
    beforeBulkUpdate: (options) => {},
    afterBulkUpdate: (options) => {},
    beforeBulkDestroy: (options) => {},
    afterBulkDestroy: (options) => {},
  },
});
```

### Common Hook Patterns
```javascript
// Auto-hash password
beforeCreate: async (user) => {
  if (user.password) {
    user.password = await bcrypt.hash(user.password, 10);
  }
},
beforeUpdate: async (user) => {
  if (user.changed('password')) {
    user.password = await bcrypt.hash(user.password, 10);
  }
},

// Auto-update timestamps
beforeUpdate: (instance) => {
  instance.updatedAt = new Date();
},

// Normalize email
beforeValidate: (user) => {
  if (user.email) {
    user.email = user.email.toLowerCase().trim();
  }
},

// Audit logging
afterCreate: async (instance, options) => {
  await AuditLog.create({
    action: 'CREATE',
    modelName: instance.constructor.name,
    recordId: instance.id,
    newValues: instance.toJSON(),
  }, { transaction: options.transaction });
},
```

## Scopes

### Defining Scopes
```javascript
User.init({
  // ... attributes
}, {
  sequelize,
  modelName: 'User',
  defaultScope: {
    attributes: { exclude: ['password'] },
  },
  scopes: {
    active: {
      where: { status: 'active' },
    },
    withPassword: {
      attributes: { include: ['password'] },
    },
    withOrders: {
      include: [{ model: Order, as: 'orders' }],
    },
    recent: {
      order: [['createdAt', 'DESC']],
      limit: 10,
    },
    byStatus(status) {
      return {
        where: { status },
      };
    },
  },
});
```

### Using Scopes
```javascript
// Apply named scope
const activeUsers = await User.scope('active').findAll();

// Chain multiple scopes
const recentActive = await User.scope(['active', 'recent']).findAll();

// Scope with parameter
const pendingUsers = await User.scope({ method: ['byStatus', 'pending'] }).findAll();

// Override default scope
const userWithPassword = await User.scope('withPassword').findByPk(1);

// Remove default scope
const allFields = await User.unscoped().findByPk(1);
```

## Indexes in Sequelize

### Model-Level Indexes
```javascript
User.init({
  // ... attributes
}, {
  sequelize,
  modelName: 'User',
  indexes: [
    // Simple index
    { fields: ['status'] },

    // Unique index
    { fields: ['email'], unique: true },

    // Composite index
    { fields: ['status', 'createdAt'] },

    // Partial index
    {
      fields: ['email'],
      where: { status: 'active' },
      name: 'active_users_email_idx',
    },

    // Expression index (requires raw SQL in migration)
    // Use migrations for LOWER(email) indexes

    // GIN index for JSONB
    {
      fields: ['metadata'],
      using: 'GIN',
    },

    // Full-text search index
    {
      fields: ['searchVector'],
      using: 'GIN',
    },
  ],
});
```

## Transactions

### Managed Transactions
```javascript
// Sequelize manages commit/rollback
const result = await sequelize.transaction(async (t) => {
  const user = await User.create({ email: 'test@example.com' }, { transaction: t });
  const order = await Order.create({ userId: user.id, total: 100 }, { transaction: t });
  return { user, order };
});
// Auto-committed if no error, auto-rolled back on error
```

### Unmanaged Transactions
```javascript
const t = await sequelize.transaction();
try {
  const user = await User.create({ email: 'test@example.com' }, { transaction: t });
  await Order.create({ userId: user.id, total: 100 }, { transaction: t });
  await t.commit();
} catch (error) {
  await t.rollback();
  throw error;
}
```

### Transaction Isolation Levels
```javascript
const { Transaction } = require('sequelize');

await sequelize.transaction({
  isolationLevel: Transaction.ISOLATION_LEVELS.SERIALIZABLE,
}, async (t) => {
  // Operations here
});
```

## Query Optimization

### Eager Loading vs Lazy Loading
```javascript
// Eager loading (preferred - avoids N+1)
const users = await User.findAll({
  include: [{ model: Order, as: 'orders' }],
});

// Lazy loading (causes N+1 problem)
const users = await User.findAll();
for (const user of users) {
  const orders = await user.getOrders(); // N additional queries!
}
```

### Select Specific Attributes
```javascript
// Only fetch needed columns
const users = await User.findAll({
  attributes: ['id', 'email', 'firstName'],
});

// Exclude sensitive columns
const users = await User.findAll({
  attributes: { exclude: ['password', 'ssn'] },
});

// Computed columns
const users = await User.findAll({
  attributes: [
    'id',
    [sequelize.fn('COUNT', sequelize.col('orders.id')), 'orderCount'],
  ],
  include: [{ model: Order, as: 'orders', attributes: [] }],
  group: ['User.id'],
});
```

### Raw Queries for Complex Operations
```javascript
// When ORM abstraction is limiting
const [results] = await sequelize.query(`
  SELECT u.*, COUNT(o.id) as order_count
  FROM users u
  LEFT JOIN orders o ON u.id = o.user_id
  WHERE u.status = :status
  GROUP BY u.id
  HAVING COUNT(o.id) > :minOrders
`, {
  replacements: { status: 'active', minOrders: 5 },
  type: QueryTypes.SELECT,
});
```

### Batch Operations
```javascript
// Bulk create (single INSERT)
await User.bulkCreate([
  { email: 'user1@example.com', firstName: 'User', lastName: 'One' },
  { email: 'user2@example.com', firstName: 'User', lastName: 'Two' },
], {
  validate: true, // Run validations
  individualHooks: true, // Run hooks per instance (slower)
});

// Bulk update
await User.update(
  { status: 'inactive' },
  { where: { lastLoginAt: { [Op.lt]: oneYearAgo } } }
);

// Bulk destroy
await User.destroy({
  where: { status: 'deleted' },
});
```

## Timestamps and Paranoid Mode

### Standard Timestamps
```javascript
User.init({
  // ... attributes
}, {
  sequelize,
  timestamps: true,      // Adds createdAt, updatedAt
  createdAt: 'created_at', // Custom column name
  updatedAt: 'updated_at',
});
```

### Soft Deletes (Paranoid Mode)
```javascript
User.init({
  // ... attributes
}, {
  sequelize,
  paranoid: true,        // Adds deletedAt, filters soft-deleted by default
  deletedAt: 'deleted_at',
});

// Soft delete
await user.destroy(); // Sets deletedAt, doesn't remove row

// Hard delete
await user.destroy({ force: true });

// Include soft-deleted in queries
await User.findAll({ paranoid: false });

// Restore soft-deleted
await user.restore();
```

## Best Practices

1. **Always use transactions** for multi-model operations
2. **Define associations in both directions** for full bidirectional navigation
3. **Use scopes** to DRY up common query patterns
4. **Eager load** associations to avoid N+1 queries
5. **Use `underscored: true`** for PostgreSQL naming conventions
6. **Prefer TEXT over STRING** to match PostgreSQL best practices
7. **Add indexes** for frequently queried columns and foreign keys
8. **Use hooks** for cross-cutting concerns (audit, normalization)
9. **Keep models focused** - business logic in services, not models
10. **Use raw queries** for complex analytics rather than forcing ORM patterns
