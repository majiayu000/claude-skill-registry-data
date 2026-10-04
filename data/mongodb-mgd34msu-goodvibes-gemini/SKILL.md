---
name: mongodb
description: Integrates MongoDB document database with Node.js applications using the official driver or Mongoose ODM. Use when building applications with flexible schemas, document storage, or when user mentions MongoDB, NoSQL, or document databases.
---

# MongoDB

Document database for Node.js applications with flexible schemas and powerful querying.

## Quick Start

```bash
# Install official driver
npm install mongodb

# Or with Mongoose ODM
npm install mongoose
```

## Native Driver

### Connection

```typescript
import { MongoClient, Db, Collection } from 'mongodb';

// Connection URI
const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017';
const client = new MongoClient(uri);

// Singleton pattern
let db: Db;

export async function connectToDatabase(): Promise<Db> {
  if (db) return db;

  try {
    await client.connect();
    db = client.db('myapp');
    console.log('Connected to MongoDB');
    return db;
  } catch (error) {
    console.error('MongoDB connection error:', error);
    throw error;
  }
}

// Get typed collection
export function getCollection<T>(name: string): Collection<T> {
  return db.collection<T>(name);
}

// Graceful shutdown
process.on('SIGINT', async () => {
  await client.close();
  process.exit(0);
});
```

### CRUD Operations

```typescript
import { ObjectId, Filter, UpdateFilter } from 'mongodb';

interface User {
  _id?: ObjectId;
  name: string;
  email: string;
  age: number;
  createdAt: Date;
  tags?: string[];
}

const users = getCollection<User>('users');

// Create
async function createUser(data: Omit<User, '_id'>): Promise<User> {
  const result = await users.insertOne({
    ...data,
    createdAt: new Date(),
  });

  return { _id: result.insertedId, ...data, createdAt: new Date() };
}

// Create many
async function createUsers(data: Omit<User, '_id'>[]): Promise<ObjectId[]> {
  const result = await users.insertMany(
    data.map(d => ({ ...d, createdAt: new Date() }))
  );
  return Object.values(result.insertedIds);
}

// Read one
async function getUserById(id: string): Promise<User | null> {
  return users.findOne({ _id: new ObjectId(id) });
}

// Read with query
async function findUsers(filter: Filter<User>): Promise<User[]> {
  return users.find(filter).toArray();
}

// Read with options
async function searchUsers(
  query: string,
  page: number = 1,
  limit: number = 10
): Promise<{ users: User[]; total: number }> {
  const filter: Filter<User> = {
    $or: [
      { name: { $regex: query, $options: 'i' } },
      { email: { $regex: query, $options: 'i' } },
    ],
  };

  const [users, total] = await Promise.all([
    users
      .find(filter)
      .sort({ createdAt: -1 })
      .skip((page - 1) * limit)
      .limit(limit)
      .toArray(),
    users.countDocuments(filter),
  ]);

  return { users, total };
}

// Update one
async function updateUser(
  id: string,
  update: Partial<User>
): Promise<User | null> {
  const result = await users.findOneAndUpdate(
    { _id: new ObjectId(id) },
    { $set: update },
    { returnDocument: 'after' }
  );
  return result;
}

// Update many
async function activateUsers(ids: string[]): Promise<number> {
  const result = await users.updateMany(
    { _id: { $in: ids.map(id => new ObjectId(id)) } },
    { $set: { active: true } }
  );
  return result.modifiedCount;
}

// Delete
async function deleteUser(id: string): Promise<boolean> {
  const result = await users.deleteOne({ _id: new ObjectId(id) });
  return result.deletedCount === 1;
}

// Upsert
async function upsertUser(
  email: string,
  data: Partial<User>
): Promise<User | null> {
  const result = await users.findOneAndUpdate(
    { email },
    { $set: data, $setOnInsert: { createdAt: new Date() } },
    { upsert: true, returnDocument: 'after' }
  );
  return result;
}
```

### Query Operators

```typescript
// Comparison
const adults = await users.find({ age: { $gte: 18 } }).toArray();
const teens = await users.find({ age: { $gte: 13, $lt: 20 } }).toArray();
const specificAges = await users.find({ age: { $in: [18, 21, 25] } }).toArray();

// Logical
const result = await users.find({
  $and: [
    { age: { $gte: 18 } },
    { email: { $exists: true } }
  ]
}).toArray();

const orResult = await users.find({
  $or: [
    { name: 'Alice' },
    { email: /admin/i }
  ]
}).toArray();

// Element
const withTags = await users.find({ tags: { $exists: true } }).toArray();
const typeCheck = await users.find({ age: { $type: 'number' } }).toArray();

// Array
const hasTag = await users.find({ tags: 'developer' }).toArray();
const allTags = await users.find({ tags: { $all: ['developer', 'admin'] } }).toArray();
const arraySize = await users.find({ tags: { $size: 3 } }).toArray();
const elemMatch = await users.find({
  addresses: { $elemMatch: { city: 'NYC', zip: { $exists: true } } }
}).toArray();

// Text search (requires text index)
const textResults = await users.find({ $text: { $search: 'developer' } }).toArray();

// Regex
const pattern = await users.find({ name: { $regex: /^A/i } }).toArray();
```

### Update Operators

```typescript
// $set - Set field value
await users.updateOne(
  { _id: new ObjectId(id) },
  { $set: { name: 'New Name', 'address.city': 'NYC' } }
);

// $unset - Remove field
await users.updateOne(
  { _id: new ObjectId(id) },
  { $unset: { temporaryField: '' } }
);

// $inc - Increment
await users.updateOne(
  { _id: new ObjectId(id) },
  { $inc: { loginCount: 1, 'stats.views': 5 } }
);

// $push - Add to array
await users.updateOne(
  { _id: new ObjectId(id) },
  { $push: { tags: 'newTag' } }
);

// $push with modifiers
await users.updateOne(
  { _id: new ObjectId(id) },
  {
    $push: {
      notifications: {
        $each: [{ message: 'Hello' }],
        $position: 0,
        $slice: 10  // Keep only 10 newest
      }
    }
  }
);

// $pull - Remove from array
await users.updateOne(
  { _id: new ObjectId(id) },
  { $pull: { tags: 'oldTag' } }
);

// $addToSet - Add unique to array
await users.updateOne(
  { _id: new ObjectId(id) },
  { $addToSet: { tags: 'uniqueTag' } }
);

// $rename - Rename field
await users.updateOne(
  { _id: new ObjectId(id) },
  { $rename: { oldName: 'newName' } }
);
```

### Aggregation Pipeline

```typescript
// Basic aggregation
const stats = await users.aggregate([
  { $match: { active: true } },
  { $group: {
    _id: '$country',
    count: { $sum: 1 },
    avgAge: { $avg: '$age' },
    names: { $push: '$name' }
  }},
  { $sort: { count: -1 } },
  { $limit: 10 }
]).toArray();

// Lookup (join)
const ordersWithUsers = await db.collection('orders').aggregate([
  { $lookup: {
    from: 'users',
    localField: 'userId',
    foreignField: '_id',
    as: 'user'
  }},
  { $unwind: '$user' },
  { $project: {
    orderId: 1,
    total: 1,
    'user.name': 1,
    'user.email': 1
  }}
]).toArray();

// Faceted search
const faceted = await products.aggregate([
  { $match: { category: 'electronics' } },
  { $facet: {
    byBrand: [
      { $group: { _id: '$brand', count: { $sum: 1 } } },
      { $sort: { count: -1 } }
    ],
    byPriceRange: [
      { $bucket: {
        groupBy: '$price',
        boundaries: [0, 100, 500, 1000, Infinity],
        default: 'Other',
        output: { count: { $sum: 1 } }
      }}
    ],
    results: [
      { $skip: 0 },
      { $limit: 20 }
    ]
  }}
]).toArray();
```

### Indexes

```typescript
// Create indexes
await users.createIndex({ email: 1 }, { unique: true });
await users.createIndex({ name: 'text', bio: 'text' }); // Text index
await users.createIndex({ location: '2dsphere' }); // Geospatial
await users.createIndex({ createdAt: 1 }, { expireAfterSeconds: 86400 }); // TTL
await users.createIndex({ category: 1, price: -1 }); // Compound

// List indexes
const indexes = await users.indexes();

// Drop index
await users.dropIndex('email_1');
```

### Transactions

```typescript
const session = client.startSession();

try {
  await session.withTransaction(async () => {
    // All operations in this block are part of the transaction
    await users.updateOne(
      { _id: fromUserId },
      { $inc: { balance: -amount } },
      { session }
    );

    await users.updateOne(
      { _id: toUserId },
      { $inc: { balance: amount } },
      { session }
    );

    await transactions.insertOne({
      from: fromUserId,
      to: toUserId,
      amount,
      createdAt: new Date()
    }, { session });
  });
} finally {
  await session.endSession();
}
```

## Mongoose ODM

### Schema Definition

```typescript
import mongoose, { Schema, Document, Model } from 'mongoose';

// Interface
interface IUser extends Document {
  name: string;
  email: string;
  password: string;
  age?: number;
  role: 'user' | 'admin';
  createdAt: Date;
  updatedAt: Date;

  // Methods
  comparePassword(candidate: string): Promise<boolean>;
}

// Schema
const userSchema = new Schema<IUser>(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
      minlength: 2,
      maxlength: 50,
    },
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
      match: [/^\S+@\S+\.\S+$/, 'Invalid email'],
    },
    password: {
      type: String,
      required: true,
      minlength: 8,
      select: false, // Don't return by default
    },
    age: {
      type: Number,
      min: 0,
      max: 150,
    },
    role: {
      type: String,
      enum: ['user', 'admin'],
      default: 'user',
    },
  },
  {
    timestamps: true,
    toJSON: {
      transform: (doc, ret) => {
        ret.id = ret._id;
        delete ret._id;
        delete ret.__v;
        delete ret.password;
        return ret;
      },
    },
  }
);

// Index
userSchema.index({ email: 1 });
userSchema.index({ name: 'text' });

// Pre-save hook
userSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

// Instance method
userSchema.methods.comparePassword = async function (
  candidate: string
): Promise<boolean> {
  return bcrypt.compare(candidate, this.password);
};

// Static method
userSchema.statics.findByEmail = function (email: string) {
  return this.findOne({ email });
};

// Virtual
userSchema.virtual('posts', {
  ref: 'Post',
  localField: '_id',
  foreignField: 'author',
});

// Model
const User: Model<IUser> = mongoose.model('User', userSchema);
export default User;
```

### Connection

```typescript
import mongoose from 'mongoose';

const MONGODB_URI = process.env.MONGODB_URI!;

// Connection options
const options = {
  maxPoolSize: 10,
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
};

// Connect
async function connect() {
  try {
    await mongoose.connect(MONGODB_URI, options);
    console.log('MongoDB connected');
  } catch (error) {
    console.error('MongoDB connection error:', error);
    process.exit(1);
  }
}

// Event handlers
mongoose.connection.on('disconnected', () => {
  console.log('MongoDB disconnected');
});

mongoose.connection.on('error', (err) => {
  console.error('MongoDB error:', err);
});

// Graceful shutdown
process.on('SIGINT', async () => {
  await mongoose.connection.close();
  process.exit(0);
});

export default connect;
```

### CRUD with Mongoose

```typescript
import User from './models/User';

// Create
const user = await User.create({
  name: 'Alice',
  email: 'alice@example.com',
  password: 'securepassword',
});

// Or
const user = new User({ name: 'Alice', email: 'alice@example.com' });
await user.save();

// Read
const user = await User.findById(id);
const user = await User.findOne({ email });
const users = await User.find({ role: 'admin' });

// With query builder
const users = await User.find()
  .where('age').gte(18)
  .where('role').equals('user')
  .select('name email')
  .sort('-createdAt')
  .skip(0)
  .limit(10)
  .lean(); // Returns plain objects (faster)

// Populate references
const posts = await Post.find()
  .populate('author', 'name email')
  .populate({
    path: 'comments',
    populate: { path: 'user', select: 'name' }
  });

// Update
const user = await User.findByIdAndUpdate(
  id,
  { name: 'New Name' },
  { new: true, runValidators: true }
);

// Or
await User.updateOne({ _id: id }, { $set: { name: 'New Name' } });
await User.updateMany({ role: 'guest' }, { $set: { role: 'user' } });

// Delete
await User.findByIdAndDelete(id);
await User.deleteOne({ _id: id });
await User.deleteMany({ inactive: true });
```

### Validation

```typescript
const productSchema = new Schema({
  name: {
    type: String,
    required: [true, 'Product name is required'],
    validate: {
      validator: (v: string) => v.length >= 3,
      message: 'Name must be at least 3 characters',
    },
  },
  price: {
    type: Number,
    required: true,
    min: [0, 'Price cannot be negative'],
    validate: {
      validator: Number.isFinite,
      message: '{VALUE} is not a valid price',
    },
  },
  sku: {
    type: String,
    validate: {
      validator: async function (v: string) {
        const count = await mongoose.models.Product.countDocuments({ sku: v });
        return count === 0;
      },
      message: 'SKU must be unique',
    },
  },
});

// Custom error handling
try {
  await product.save();
} catch (error) {
  if (error instanceof mongoose.Error.ValidationError) {
    const messages = Object.values(error.errors).map((e) => e.message);
    console.log('Validation errors:', messages);
  }
}
```

## Reference Files

- [aggregation.md](references/aggregation.md) - Advanced aggregation pipelines
- [performance.md](references/performance.md) - Optimization and indexing strategies
