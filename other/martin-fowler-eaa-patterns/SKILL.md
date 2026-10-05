---
name: martin-fowler-eaa-patterns
type: reference
description: Reference for Martin Fowler's Patterns of Enterprise Application Architecture (PoEAA, 2002). ALWAYS read before structuring business logic, data access, web presentation, distribution, concurrency, or session state for enterprise applications.
---

Enterprise application architecture patterns from Martin Fowler's PoEAA (2002). Enterprise applications display, manipulate, and store large amounts of often complex data and automate business processes with that data.

### Layering (foundational)

- The dominant organizing principle: keep Presentation, Domain (business logic), and Data Source as separate layers. Dependencies point downward (Presentation -> Domain -> Data Source). Do not let lower layers know about higher ones.

### Domain Logic Patterns

- **Transaction Script** — Organizes business logic by procedures where each procedure handles a single request from the presentation. Use when domain logic is simple and procedural; easy to start but degrades as rules multiply.
- **Domain Model** — An object model of the domain that incorporates both behavior and data. Use when business logic is complex (rules, state, relationships); richer but needs a data mapping layer.
- **Table Module** — A single instance that handles the business logic for all rows in a database table or view. Use with a Record Set-centric stack (e.g. .NET DataTables) and tabular UIs.
- **Service Layer** — Defines an application's boundary with a layer of services that establishes a set of available operations and coordinates the application's response in each operation. Use to give several clients/channels a common API and a single place for use-case coordination; usually wraps a Domain Model.

### Data Source Architectural Patterns

- **Table Data Gateway** — An object that acts as a gateway to a database table; one instance handles all the rows. Use for the simplest DB access with Transaction Script or Table Module; returns Record Sets.
- **Row Data Gateway** — An object that acts as a gateway to a single record; one instance per row. Use when you want an object interface to a row without full domain logic; can evolve toward a Domain Model.
- **Active Record** — An object that wraps a row, encapsulates database access, and adds domain logic on that data. Use for simple domain logic with direct table mapping (Rails-style); couples domain objects to persistence.
- **Data Mapper** — A layer of mappers that moves data between objects and a database while keeping them independent of each other and the mapper. Use with a Domain Model so domain objects know nothing of the database; most decoupled, heaviest.

### Object-Relational Behavioral Patterns

- **Unit of Work** — Maintains a list of objects affected by a business transaction and coordinates writing out changes and resolving concurrency. Use for transactional change tracking and consistent multi-object commits.
- **Identity Map** — Ensures each object gets loaded only once by keeping every loaded object in a map. Use to avoid duplicate/inconsistent in-memory objects and redundant DB hits within a transaction.
- **Lazy Load** — An object that doesn't contain all the data you need but knows how to get it. Use to defer loading large object graphs; watch for N+1 queries.

### Object-Relational Structural Patterns

- **Identity Field** — Saves a database ID field in an object to maintain identity between an in-memory object and a database row. Foundational for all O/R mapping of identifiable objects.
- **Inheritance Mappers** — A structure to organize database mappers that handle inheritance hierarchies. Use when domain inheritance is mapped to tables (choose Single/Class/Concrete below).
- **Foreign Key Mapping** — Maps an association between objects to a foreign key reference between tables. Use for one-to-one and one-to-many references.
- **Association Table Mapping** — Saves an association as a table with foreign keys to the tables that are linked. Use for many-to-many associations, or when the link needs extra attributes.
- **Dependent Mapping** — Has one class perform the database mapping for a child class. Use when a child has no life outside its parent (composition); the parent owns persistence.
- **Embedded Value** — Maps an object into several fields of another object's table. Use for small value objects owned by a row (e.g. an address).
- **Serialized LOB** — Saves a graph of objects by serializing them into a single large object stored in a database field. Use for flexible structured blobs you rarely query individually.
- **Single Table Inheritance** — Represents an inheritance hierarchy as a single table with columns for all fields of the various classes. Use for shallow/stable hierarchies; simplest queries but sparse columns.
- **Class Table Inheritance** — Represents an inheritance hierarchy with one table per class. Use for deeper hierarchies wanting OO clarity; no sparse columns but reads need joins.
- **Concrete Table Inheritance** — Represents an inheritance hierarchy with one table per concrete class. Use when you rarely query across the hierarchy; duplicates fields and makes polymorphism hard.

### Object-Relational Metadata Mapping Patterns

- **Metadata Mapping** — Holds details of object-relational mapping in metadata. Use to avoid hand-written mappers and to generate them.
- **Query Object** — An object that represents a database query. Use to decouple query construction from DB syntax and to compose queries safely.
- **Repository** — Mediates between the domain and data mapping layers using a collection-like interface for accessing domain objects. Use to decouple the domain from data mapping and centralize object/query access, especially with a Domain Model.

### Web Presentation Patterns

- **Model View Controller** — Splits user interface interaction into three distinct roles. Use for rich, testable UIs with multiple views of one model.
- **Page Controller** — An object that handles a request for a specific page or action on a Web site. Use for page-centric navigation; the common default for simple web apps.
- **Front Controller** — A controller that handles all requests for a Web site. Use when you need centralized request handling (routing, security, common pre-processing).
- **Template View** — Renders information into HTML by embedding markers in an HTML page. Use for HTML-centric pages with server-side templates.
- **Transform View** — A view that processes domain data element by element and transforms it into HTML. Use when you prefer a transform pipeline (e.g. XSLT-style) over templates.
- **Two Step View** — Turns domain data into HTML in two steps: form a logical page, then render it to HTML. Use to keep a consistent look across many views or target multiple output formats.
- **Application Controller** — A centralized point for handling screen navigation and the flow of an application. Use when navigation/flow is complex or shared across controllers.

### Distribution Patterns

- **Remote Facade** — Provides a coarse-grained facade on fine-grained objects to improve efficiency over a network. Use to minimize remote calls across a process/network boundary.
- **Data Transfer Object** — An object that carries data between processes in order to reduce the number of method calls. Use to batch data into one round-trip with a Remote Facade; do not use within a single process.

### Offline Concurrency Patterns

- **Optimistic Offline Lock** — Prevents conflicts by detecting a conflict and rolling back the transaction. Use when conflicts are rare and you want no locking overhead.
- **Pessimistic Offline Lock** — Prevents conflicts by allowing only one business transaction at a time to access data. Use when conflicts are likely and you can tolerate the lock/session cost.
- **Coarse-Grained Lock** — Locks a set of related objects with a single lock. Use to lock an aggregate/cluster together.
- **Implicit Lock** — Allows framework or layer supertype code to acquire offline locks. Use to keep lock management out of domain code.

### Session State Patterns

- **Client Session State** — Stores session state on the client. Use for small state to keep the server stateless; mind size and security limits.
- **Server Session State** — Keeps the session state on a server system in a serialized form. Use for moderate session data with a session store or server affinity.
- **Database Session State** — Stores session data as committed data in the database. Use for long-lived transactions needing durability without server affinity.

### Base Patterns

- **Gateway** — An object that encapsulates access to an external system or resource. Use to isolate external APIs behind a cleaner interface.
- **Service Stub** — Removes dependence upon problematic services during testing. Use to test without the real (remote/flaky) dependency.
- **Record Set** — An in-memory representation of tabular data. Use when UIs and data sources naturally exchange tabular data.
- **Mapper** — An object that sets up communication between two independent objects. Foundational decoupling device (e.g. Data Mapper builds on it).
- **Layer Supertype** — A type that acts as the supertype for all types in its layer. Use to share cross-cutting layer behavior.
- **Separated Interface** — Defines an interface in a separate package from its implementation. Use to break compile-time dependencies / invert dependencies.
- **Registry** — A well-known object that other objects can use to find common objects and services. Use for service location, sparingly (it can hide dependencies).
- **Value Object** — A small simple object, like money or a date range, whose equality isn't based on identity. Use for concepts that compare by value and should be immutable.
- **Money** — Represents a monetary value. Use for money to avoid floating-point error and currency mistakes.
- **Special Case** — A subclass that provides special behavior for particular cases. Use instead of repeated null/empty checks (a.k.a. Null Object).
- **Plugin** — Links classes during configuration rather than compilation. Use to select implementations without recompiling and to support pluggable services.

### Key Choices

- **Domain logic**: Transaction Script (simple) vs Table Module (record-set stack) vs Domain Model (complex rules). Add a Service Layer when multiple clients share the same use cases.
- **Data access vs Domain Model**: Active Record couples domain to persistence and suits simple logic; Data Mapper keeps a Domain Model persistence-ignorant and suits complex logic.
- **Inheritance to tables**: Single Table (simplest, sparse columns) vs Class Table (clear, needs joins) vs Concrete Table (no cross-hierarchy joins, duplicated fields).
- **Web controller**: Page Controller (per-page, simple) vs Front Controller (centralized) vs Application Controller (complex shared flow).
- **Concurrency**: Optimistic (rare conflicts, low overhead) vs Pessimistic (likely conflicts, willing to pay lock cost).
- **Distribution**: reach for Remote Facade + DTO only across a real process/network boundary; finer-grained local calls need neither.
