---
name: kotlin-expert
description: Kotlin expertise for modern Android development from Google's Android team. Use when writing Kotlin code, using coroutines and Flow for async operations, implementing Kotlin DSLs, working with sealed classes/data classes, integrating Hilt/Dagger for DI, using Room database, or optimizing Kotlin performance. Triggers on Kotlin, coroutines, Flow, Android Kotlin, Hilt, Room, or Kotlin-specific patterns.
---

# Kotlin Expert - Modern Android Development

**Purpose**: Master Kotlin for building robust, concise Android applications

**Agent**: Google Android Lead
**Use When**: Building Android apps, backend services with Kotlin, or migrating from Java

---

## Kotlin Basics

```kotlin
// Variables
val immutable = "Cannot change"  // val = final
var mutable = "Can change"       // var = variable

// Null safety
var nullable: String? = null
var nonNull: String = "Never null"

// Safe call
val length = nullable?.length  // Returns null if nullable is null

// Elvis operator
val len = nullable?.length ?: 0  // Default to 0 if null

// Not-null assertion (!!)
val len2 = nullable!!.length  // Throws NPE if null

// Data classes
data class User(
    val id: Int,
    val name: String,
    val email: String
)

val user = User(1, "John", "john@example.com")
val copy = user.copy(name = "Jane")  // Immutable update

// Extension functions
fun String.isPalindrome(): Boolean {
    return this == this.reversed()
}

"racecar".isPalindrome()  // true

// Lambda expressions
val numbers = listOf(1, 2, 3, 4, 5)
val doubled = numbers.map { it * 2 }
val evens = numbers.filter { it % 2 == 0 }

// When expression (switch on steroids)
when (x) {
    0 -> println("Zero")
    in 1..10 -> println("Between 1 and 10")
    is String -> println("It's a string")
    else -> println("Other")
}
```

---

## Android Development

### Activity/Fragment

```kotlin
class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.button.setOnClickListener {
            val intent = Intent(this, DetailActivity::class.java)
            intent.putExtra("userId", 123)
            startActivity(intent)
        }
    }
}
```

### ViewModel + LiveData

```kotlin
class UserViewModel : ViewModel() {
    private val _users = MutableLiveData<List<User>>()
    val users: LiveData<List<User>> = _users

    private val _loading = MutableLiveData<Boolean>()
    val loading: LiveData<Boolean> = _loading

    fun loadUsers() {
        viewModelScope.launch {
            _loading.value = true
            try {
                val result = repository.getUsers()
                _users.value = result
            } catch (e: Exception) {
                // Handle error
            } finally {
                _loading.value = false
            }
        }
    }
}

// In Activity/Fragment
class UserListFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        viewModel.users.observe(viewLifecycleOwner) { users ->
            adapter.submitList(users)
        }

        viewModel.loading.observe(viewLifecycleOwner) { isLoading ->
            binding.progressBar.isVisible = isLoading
        }

        viewModel.loadUsers()
    }
}
```

### Coroutines

```kotlin
// Launch coroutine
lifecycleScope.launch {
    val user = withContext(Dispatchers.IO) {
        database.getUser(userId)
    }
    binding.nameTextView.text = user.name
}

// Async/await
lifecycleScope.launch {
    val deferred1 = async { api.getUser() }
    val deferred2 = async { api.getPosts() }

    val user = deferred1.await()
    val posts = deferred2.await()
}

// Flow (reactive streams)
class UserRepository {
    fun observeUsers(): Flow<List<User>> = flow {
        while (true) {
            val users = api.getUsers()
            emit(users)
            delay(5000)  // Poll every 5 seconds
        }
    }
}

// Collect flow
lifecycleScope.launch {
    repository.observeUsers().collect { users ->
        adapter.submitList(users)
    }
}
```

### Retrofit (Networking)

```kotlin
interface ApiService {
    @GET("users")
    suspend fun getUsers(): List<User>

    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: Int): User

    @POST("users")
    suspend fun createUser(@Body user: User): User
}

val retrofit = Retrofit.Builder()
    .baseUrl("https://api.example.com/")
    .addConverterFactory(GsonConverterFactory.create())
    .build()

val api = retrofit.create(ApiService::class.java)

// Usage
lifecycleScope.launch {
    try {
        val users = api.getUsers()
        // Update UI
    } catch (e: Exception) {
        // Handle error
    }
}
```

### Room Database

```kotlin
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: Int,
    @ColumnInfo(name = "name") val name: String,
    @ColumnInfo(name = "email") val email: String
)

@Dao
interface UserDao {
    @Query("SELECT * FROM users")
    fun getAllUsers(): Flow<List<UserEntity>>

    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUser(userId: Int): UserEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: UserEntity)

    @Delete
    suspend fun deleteUser(user: UserEntity)
}

@Database(entities = [UserEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
}

// Create database
val db = Room.databaseBuilder(
    context,
    AppDatabase::class.java,
    "app-database"
).build()
```

---

## Best Practices

- Use `val` over `var` (immutability)
- Leverage null safety (`?`, `?:`, `?.`)
- Use data classes for models
- Prefer coroutines over callbacks
- Use Flow for reactive streams
- ViewModels survive configuration changes
- Repository pattern for data layer

---

**Remember**: Kotlin is Java++. Concise, safe, and interoperable.

**Created**: 2026-02-04
**Maintained By**: Google Android Lead
