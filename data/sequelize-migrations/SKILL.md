---
name: sequelize-migrations
description: Sequelize migration patterns and best practices for PostgreSQL schema changes. Use when creating migrations, modifying tables, managing indexes, or handling data migrations safely.
---

# Sequelize Migration Patterns

## Migration Basics

### File Structure
```
migrations/
├── 20240101000000-create-users.js
├── 20240101000001-create-orders.js
├── 20240102000000-add-status-to-users.js
└── 20240103000000-add-index-to-orders.js
```

### Basic Migration Template
```javascript
'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    // Forward migration
  },

  async down(queryInterface, Sequelize) {
    // Rollback migration
  },
};
```

## Creating Tables

### Basic Table Creation
```javascript
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('users', {
      id: {
        type: Sequelize.BIGINT,
        primaryKey: true,
        autoIncrement: true,
      },
      email: {
        type: Sequelize.TEXT,
        allowNull: false,
        unique: true,
      },
      first_name: {
        type: Sequelize.TEXT,
        allowNull: false,
      },
      last_name: {
        type: Sequelize.TEXT,
        allowNull: false,
      },
      status: {
        type: Sequelize.TEXT,
        allowNull: false,
        defaultValue: 'active',
      },
      metadata: {
        type: Sequelize.JSONB,
        allowNull: false,
        defaultValue: {},
      },
      created_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('NOW()'),
      },
      updated_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('NOW()'),
      },
    });

    // Add indexes after table creation
    await queryInterface.addIndex('users', ['email'], { unique: true });
    await queryInterface.addIndex('users', ['status']);
    await queryInterface.addIndex('users', ['created_at']);
  },

  async down(queryInterface) {
    await queryInterface.dropTable('users');
  },
};
```

### Table with Foreign Keys
```javascript
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('orders', {
      id: {
        type: Sequelize.BIGINT,
        primaryKey: true,
        autoIncrement: true,
      },
      user_id: {
        type: Sequelize.BIGINT,
        allowNull: false,
        references: {
          model: 'users',
          key: 'id',
        },
        onUpdate: 'CASCADE',
        onDelete: 'CASCADE',
      },
      status: {
        type: Sequelize.TEXT,
        allowNull: false,
        defaultValue: 'pending',
      },
      total: {
        type: Sequelize.DECIMAL(10, 2),
        allowNull: false,
      },
      created_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('NOW()'),
      },
      updated_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal('NOW()'),
      },
    });

    // CRITICAL: Index foreign key columns
    await queryInterface.addIndex('orders', ['user_id']);
    await queryInterface.addIndex('orders', ['status']);
    await queryInterface.addIndex('orders', ['created_at']);
  },

  async down(queryInterface) {
    await queryInterface.dropTable('orders');
  },
};
```

## Adding Columns

### Simple Column Addition
```javascript
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.addColumn('users', 'phone', {
      type: Sequelize.TEXT,
      allowNull: true,
    });
  },

  async down(queryInterface) {
    await queryInterface.removeColumn('users', 'phone');
  },
};
```

### Column with Default Value
```javascript
module.exports = {
  async up(queryInterface, Sequelize) {
    // For non-volatile defaults, this is fast (no table rewrite)
    await queryInterface.addColumn('users', 'is_verified', {
      type: Sequelize.BOOLEAN,
      allowNull: false,
      defaultValue: false,
    });
  },

  async down(queryInterface) {
    await queryInterface.removeColumn('users', 'is_verified');
  },
};
```

### NOT NULL Column on Existing Table (Safe Pattern)
```javascript
module.exports = {
  async up(queryInterface, Sequelize) {
    // Step 1: Add column as nullable
    await queryInterface.addColumn('users', 'role', {
      type: Sequelize.TEXT,
      allowNull: true,
    });

    // Step 2: Backfill existing rows
    await queryInterface.sequelize.query(`
      UPDATE users SET role = 'user' WHERE role IS NULL
    `);

    // Step 3: Add NOT NULL constraint
    await queryInterface.changeColumn('users', 'role', {
      type: Sequelize.TEXT,
      allowNull: false,
      defaultValue: 'user',
    });
  },

  async down(queryInterface) {
    await queryInterface.removeColumn('users', 'role');
  },
};
```

## Modifying Columns

### Change Column Type
```javascript
module.exports = {
  async up(queryInterface, Sequelize) {
    // Note: May require USING clause for incompatible types
    await queryInterface.changeColumn('products', 'price', {
      type: Sequelize.DECIMAL(12, 2), // Expanding precision
      allowNull: false,
    });
  },

  async down(queryInterface, Sequelize) {
    await queryInterface.changeColumn('products', 'price', {
      type: Sequelize.DECIMAL(10, 2),
      allowNull: false,
    });
  },
};
```

### Change Column Type with USING
```javascript
module.exports = {
  async up(queryInterface) {
    // When types aren't directly compatible
    await queryInterface.sequelize.query(`
      ALTER TABLE products
      ALTER COLUMN status TYPE INTEGER
      USING CASE
        WHEN status = 'active' THEN 1
        WHEN status = 'inactive' THEN 0
        ELSE -1
      END
    `);
  },

  async down(queryInterface) {
    await queryInterface.sequelize.query(`
      ALTER TABLE products
      ALTER COLUMN status TYPE TEXT
      USING CASE
        WHEN status = 1 THEN 'active'
        WHEN status = 0 THEN 'inactive'
        ELSE 'unknown'
      END
    `);
  },
};
```

## Renaming

### Rename Column
```javascript
module.exports = {
  async up(queryInterface) {
    await queryInterface.renameColumn('users', 'name', 'full_name');
  },

  async down(queryInterface) {
    await queryInterface.renameColumn('users', 'full_name', 'name');
  },
};
```

### Rename Table
```javascript
module.exports = {
  async up(queryInterface) {
    await queryInterface.renameTable('users', 'accounts');
  },

  async down(queryInterface) {
    await queryInterface.renameTable('accounts', 'users');
  },
};
```

## Index Management

### Add Index
```javascript
module.exports = {
  async up(queryInterface) {
    // Simple index
    await queryInterface.addIndex('orders', ['customer_id']);

    // Named index
    await queryInterface.addIndex('orders', ['status'], {
      name: 'orders_status_idx',
    });

    // Unique index
    await queryInterface.addIndex('users', ['email'], {
      unique: true,
      name: 'users_email_unique',
    });

    // Composite index
    await queryInterface.addIndex('orders', ['customer_id', 'created_at']);

    // Partial index
    await queryInterface.addIndex('orders', ['customer_id'], {
      where: { status: 'active' },
      name: 'orders_active_customer_idx',
    });
  },

  async down(queryInterface) {
    await queryInterface.removeIndex('orders', 'orders_status_idx');
    await queryInterface.removeIndex('users', 'users_email_unique');
    await queryInterface.removeIndex('orders', ['customer_id', 'created_at']);
    await queryInterface.removeIndex('orders', 'orders_active_customer_idx');
  },
};
```

### Concurrent Index Creation (No Lock)
```javascript
module.exports = {
  async up(queryInterface) {
    // CONCURRENTLY avoids locking the table during index creation
    // CRITICAL: Cannot run in a transaction
    await queryInterface.sequelize.query(`
      CREATE INDEX CONCURRENTLY IF NOT EXISTS orders_customer_id_idx
      ON orders (customer_id)
    `);
  },

  async down(queryInterface) {
    await queryInterface.sequelize.query(`
      DROP INDEX CONCURRENTLY IF EXISTS orders_customer_id_idx
    `);
  },
};
```

### GIN Index for JSONB
```javascript
module.exports = {
  async up(queryInterface) {
    await queryInterface.sequelize.query(`
      CREATE INDEX users_metadata_gin ON users USING GIN (metadata)
    `);
  },

  async down(queryInterface) {
    await queryInterface.sequelize.query(`
      DROP INDEX IF EXISTS users_metadata_gin
    `);
  },
};
```

### Expression Index
```javascript
module.exports = {
  async up(queryInterface) {
    await queryInterface.sequelize.query(`
      CREATE UNIQUE INDEX users_lower_email_idx ON users (LOWER(email))
    `);
  },

  async down(queryInterface) {
    await queryInterface.sequelize.query(`
      DROP INDEX IF EXISTS users_lower_email_idx
    `);
  },
};
```

## Constraints

### Add Foreign Key
```javascript
module.exports = {
  async up(queryInterface) {
    await queryInterface.addConstraint('orders', {
      fields: ['customer_id'],
      type: 'foreign key',
      name: 'orders_customer_id_fkey',
      references: {
        table: 'customers',
        field: 'id',
      },
      onDelete: 'CASCADE',
      onUpdate: 'CASCADE',
    });

    // Don't forget to index the FK column!
    await queryInterface.addIndex('orders', ['customer_id']);
  },

  async down(queryInterface) {
    await queryInterface.removeConstraint('orders', 'orders_customer_id_fkey');
    await queryInterface.removeIndex('orders', ['customer_id']);
  },
};
```

### Add Check Constraint
```javascript
module.exports = {
  async up(queryInterface) {
    await queryInterface.addConstraint('products', {
      fields: ['price'],
      type: 'check',
      name: 'products_price_positive',
      where: {
        price: { [Sequelize.Op.gt]: 0 },
      },
    });

    // Or with raw SQL for complex constraints
    await queryInterface.sequelize.query(`
      ALTER TABLE orders
      ADD CONSTRAINT orders_status_valid
      CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled'))
    `);
  },

  async down(queryInterface) {
    await queryInterface.removeConstraint('products', 'products_price_positive');
    await queryInterface.removeConstraint('orders', 'orders_status_valid');
  },
};
```

### Add Unique Constraint
```javascript
module.exports = {
  async up(queryInterface) {
    await queryInterface.addConstraint('order_items', {
      fields: ['order_id', 'product_id'],
      type: 'unique',
      name: 'order_items_order_product_unique',
    });
  },

  async down(queryInterface) {
    await queryInterface.removeConstraint('order_items', 'order_items_order_product_unique');
  },
};
```

## Data Migrations

### Backfill Data
```javascript
module.exports = {
  async up(queryInterface) {
    // Batch update to avoid locking
    const batchSize = 1000;
    let affected = batchSize;

    while (affected === batchSize) {
      const [, result] = await queryInterface.sequelize.query(`
        UPDATE users
        SET normalized_email = LOWER(email)
        WHERE id IN (
          SELECT id FROM users
          WHERE normalized_email IS NULL
          LIMIT ${batchSize}
        )
      `);
      affected = result.rowCount || 0;
    }
  },

  async down(queryInterface) {
    await queryInterface.sequelize.query(`
      UPDATE users SET normalized_email = NULL
    `);
  },
};
```

### Copy Data Between Tables
```javascript
module.exports = {
  async up(queryInterface) {
    await queryInterface.sequelize.query(`
      INSERT INTO user_profiles (user_id, bio, avatar_url, created_at)
      SELECT id, bio, avatar_url, NOW()
      FROM users
      WHERE bio IS NOT NULL OR avatar_url IS NOT NULL
    `);
  },

  async down(queryInterface) {
    await queryInterface.sequelize.query(`
      DELETE FROM user_profiles
    `);
  },
};
```

## Enum Types

### Create Enum Type
```javascript
module.exports = {
  async up(queryInterface) {
    await queryInterface.sequelize.query(`
      CREATE TYPE order_status AS ENUM (
        'pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled'
      )
    `);

    await queryInterface.addColumn('orders', 'status_enum', {
      type: 'order_status',
      allowNull: false,
      defaultValue: 'pending',
    });
  },

  async down(queryInterface) {
    await queryInterface.removeColumn('orders', 'status_enum');
    await queryInterface.sequelize.query(`
      DROP TYPE IF EXISTS order_status
    `);
  },
};
```

### Add Value to Existing Enum
```javascript
module.exports = {
  async up(queryInterface) {
    // Add new value to enum (cannot be rolled back in PostgreSQL)
    await queryInterface.sequelize.query(`
      ALTER TYPE order_status ADD VALUE IF NOT EXISTS 'refunded'
    `);
  },

  async down() {
    // Cannot remove enum values in PostgreSQL
    // Would need to recreate the type entirely
    console.log('Warning: Cannot remove enum value. Manual intervention required.');
  },
};
```

## Transactions in Migrations

### Automatic Transaction (Default)
Most Sequelize CLI migrations run in a transaction automatically.

### Disable Transaction for CONCURRENTLY
```javascript
module.exports = {
  async up(queryInterface) {
    // CREATE INDEX CONCURRENTLY cannot run in a transaction
    await queryInterface.sequelize.query(
      'CREATE INDEX CONCURRENTLY idx_users_email ON users (email)',
      { transaction: null } // Disable transaction
    );
  },

  async down(queryInterface) {
    await queryInterface.sequelize.query(
      'DROP INDEX CONCURRENTLY IF EXISTS idx_users_email',
      { transaction: null }
    );
  },
};
```

## Safe Migration Patterns

### Zero-Downtime Column Removal
```javascript
// Step 1: Stop writing to the column (application change)
// Step 2: Migration to remove column

module.exports = {
  async up(queryInterface) {
    // First, drop any constraints
    await queryInterface.removeConstraint('users', 'users_legacy_id_fkey').catch(() => {});

    // Then drop the column
    await queryInterface.removeColumn('users', 'legacy_id');
  },

  async down(queryInterface, Sequelize) {
    await queryInterface.addColumn('users', 'legacy_id', {
      type: Sequelize.INTEGER,
      allowNull: true,
    });
  },
};
```

### Add Column with Default (PostgreSQL 11+)
```javascript
// PostgreSQL 11+ handles default values without table rewrite
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.addColumn('users', 'account_type', {
      type: Sequelize.TEXT,
      allowNull: false,
      defaultValue: 'standard',
    });
  },

  async down(queryInterface) {
    await queryInterface.removeColumn('users', 'account_type');
  },
};
```

### Rename Column Safely (Two-Phase)
```javascript
// Phase 1: Add new column, copy data
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.addColumn('users', 'full_name', {
      type: Sequelize.TEXT,
      allowNull: true,
    });

    await queryInterface.sequelize.query(`
      UPDATE users SET full_name = name WHERE full_name IS NULL
    `);
  },

  async down(queryInterface) {
    await queryInterface.removeColumn('users', 'full_name');
  },
};

// Phase 2: (After application updated) Remove old column
module.exports = {
  async up(queryInterface) {
    await queryInterface.removeColumn('users', 'name');
  },

  async down(queryInterface, Sequelize) {
    await queryInterface.addColumn('users', 'name', {
      type: Sequelize.TEXT,
      allowNull: true,
    });
    await queryInterface.sequelize.query(`
      UPDATE users SET name = full_name
    `);
  },
};
```

## Sequelize CLI Commands

```bash
# Generate migration
npx sequelize-cli migration:generate --name add-phone-to-users

# Run pending migrations
npx sequelize-cli db:migrate

# Undo last migration
npx sequelize-cli db:migrate:undo

# Undo all migrations
npx sequelize-cli db:migrate:undo:all

# Undo to specific migration
npx sequelize-cli db:migrate:undo:all --to 20240101000000-create-users.js

# Check migration status
npx sequelize-cli db:migrate:status
```

## Best Practices

1. **Always write both up and down** - Enable rollback capability
2. **Test migrations both ways** - Run up, then down, then up again
3. **Use transactions** - Sequelize does this by default
4. **Batch large data updates** - Avoid locking tables for extended periods
5. **Index FK columns** - PostgreSQL doesn't auto-create these
6. **Use CONCURRENTLY for production indexes** - Avoid blocking writes
7. **Keep migrations small** - One logical change per migration
8. **Don't modify old migrations** - Create new ones instead
9. **Use raw SQL when needed** - Sequelize's API doesn't cover everything
10. **Name constraints explicitly** - Makes them easier to remove later
