# 📚 Study Guide - Exam Preparation

> **For the 6-student team oral exam - 10 minutes total**
> The professor can ask ANY student about ANY part of the code.
> Focus: Threading, Client-Server, Architecture decisions ("Why X and not Y?")

---

## 📖 Recommended Reading Order

To understand the project from scratch, read the documentation in this order:

### Phase 1: The Big Picture (Start Here)

| #   | File                         | Why Read This First                               |
| --- | ---------------------------- | ------------------------------------------------- |
| 1   | [../README.md](../README.md) | Overview, architecture diagram, package structure |

### Phase 2: Server Side - Entry Point & Core Flow

| #   | File                                                             | What You Learn                                         |
| --- | ---------------------------------------------------------------- | ------------------------------------------------------ |
| 2   | [../2-server/ServerApp.md](../2-server/ServerApp.md)             | How the server starts (entry point)                    |
| 3   | [../2-server/StoreServer.md](../2-server/StoreServer.md)         | Socket server, accepting connections, creating threads |
| 4   | [../2-server/ClientHandler.md](../2-server/ClientHandler.md)     | **CRITICAL** - How each client request is handled      |
| 5   | [../2-server/CustomerHandler.md](../2-server/CustomerHandler.md) | Async customer checkout (thread pool)                  |

### Phase 3: Model/Data Layer

| #   | File                                                                 | What You Learn                                           |
| --- | -------------------------------------------------------------------- | -------------------------------------------------------- |
| 6   | [../4-model/Chain.md](../4-model/Chain.md)                           | Store chain container                                    |
| 7   | [../4-model/StoreBranch.md](../4-model/StoreBranch.md)               | **CRITICAL** - Branch logic, customer queue, thread pool |
| 8   | [../4-model/Customer.md](../4-model/Customer.md)                     | Abstract class, polymorphism                             |
| 9   | [../4-model/CustomerSubclasses.md](../4-model/CustomerSubclasses.md) | VIP/Returning/New - getDiscount() override               |
| 10  | [../4-model/Product.md](../4-model/Product.md)                       | Abstract product class                                   |
| 11  | [../4-model/ProductSubclasses.md](../4-model/ProductSubclasses.md)   | Jean, Bra, Sneaker, etc.                                 |
| 12  | [../4-model/Employee.md](../4-model/Employee.md)                     | Employee model                                           |
| 13  | [../4-model/Role.md](../4-model/Role.md)                             | MANAGER vs CASHIER enum                                  |

### Phase 4: Client Side

| #   | File                                                       | What You Learn                    |
| --- | ---------------------------------------------------------- | --------------------------------- |
| 14  | [../3-client/ClientApp.md](../3-client/ClientApp.md)       | Client entry point                |
| 15  | [../3-client/BranchClient.md](../3-client/BranchClient.md) | Network communication with server |
| 16  | [../3-client/BranchMenu.md](../3-client/BranchMenu.md)     | User interface, menu options      |

### Phase 5: Utilities & Cross-Cutting

| #   | File                                                                               | What You Learn                          |
| --- | ---------------------------------------------------------------------------------- | --------------------------------------- |
| 17  | [../5-utils/JsonLoader.md](../5-utils/JsonLoader.md)                               | Configuration management                |
| 18  | [../5-utils/Logger.md](../5-utils/Logger.md)                                       | Logging utility                         |
| 19  | [../5-utils/PasswordValidator.md](../5-utils/PasswordValidator.md)                 | Password validation logic               |
| 20  | [../2-server/ChatAvailabilityObserver.md](../2-server/ChatAvailabilityObserver.md) | Observer pattern for chat notifications |

---

## 🎯 Key Topics for Exam (Grouped by Context)

### Topic 1: Threading & Concurrency ⭐⭐⭐ (MOST LIKELY TO BE ASKED)

**Files to Study:**

- `StoreServer.java` - lines 35-55 (creating threads for each client)
- `StoreBranch.java` - lines 30-47 (ExecutorService thread pool)
- `ClientHandler.java` - `handleSell()` method
- `CustomerHandler.java` - entire file (Runnable, async processing)
- `StoreBranch.java` - `sell()` method with `synchronized` keyword

**Key Concepts:**

1. **One thread per client** - `StoreServer.start()` creates a new `Thread(handler)` for each connection
2. **Fixed thread pool for cashiers** - `Executors.newFixedThreadPool(MAX_CASHIERS)`
3. **Synchronized methods** - `sell()` is synchronized to prevent race conditions
4. **Runnable interface** - `ClientHandler` and `CustomerHandler` implement `Runnable`

**Potential Questions:**
| Question | Where to Find Answer |
|----------|----------------------|
| "Why do we use `synchronized` on the `sell()` method?" | `StoreBranch.java:251` - Prevents two threads from modifying inventory simultaneously |
| "What happens if 10 clients connect but MAX_CASHIERS is 3?" | Thread pool queues excess tasks - they wait until a cashier is free |
| "Why not use a single thread for all clients?" | Would block - each client needs its own thread for real-time communication |
| "What's the difference between `synchronized(chain)` and `synchronized(branch)`?" | Scope of lock - chain locks all branches, branch locks only that branch |
| "Why do we use ExecutorService instead of creating threads directly?" | Thread pooling, reuse, resource management |
| "What happens if two employees sell at the same time in the same branch?" | `sell()` is synchronized - one waits for the other to finish |
| "Why is `customerQueue.poll()` inside `synchronized(branch)`?" | Queue is not thread-safe by default (LinkedList) |

---

### Topic 2: Client-Server Architecture ⭐⭐⭐

**Files to Study:**

- `StoreServer.java` - `ServerSocket`, `accept()` loop
- `BranchClient.java` - `Socket`, `DataInputStream`, `PrintStream`
- `ClientHandler.java` - Protocol parsing (`run()` method lines 60-82)

**Key Concepts:**

1. **Protocol format**: `ACTION|branchId|key1:value1|key2:value2`
2. **Request-Response model**: Client sends request → Server processes → Server sends response
3. **Push notifications**: Server can push messages (e.g., `CHAT_REQUEST|...`)

**Potential Questions:**
| Question | Where to Find Answer |
|----------|----------------------|
| "Explain the communication protocol between client and server" | `ClientHandler.run()` - splits by `\|`, then by `:` for key-value |
| "Why use DataInputStream and PrintStream, not BufferedReader?" | DataInputStream allows reading various primitives, PrintStream for simple output |
| "What happens when a client disconnects unexpectedly?" | `IOException` caught, `cleanup()` called, client removed from list |
| "How does the server know which branch the client belongs to?" | Client sends branchId in every message (field index [1]) |
| "Why don't we use HTTP/REST instead of sockets?" | Real-time bidirectional communication (chat, notifications) |
| "How is the session maintained?" | `currentEmployee` field in `ClientHandler` - set on login, cleared on logout |

---

### Topic 3: OOP - Inheritance & Polymorphism ⭐⭐

**Files to Study:**

- `Customer.java` - abstract class, `abstract double getDiscount()`
- `VIPCustomer.java`, `NewCustomer.java`, `ReturningCustomer.java` - concrete implementations
- `Product.java` - abstract class
- Jean, Bra, Sneaker, etc. - concrete products

**Key Concepts:**

1. **Abstract classes**: `Customer` and `Product` cannot be instantiated directly
2. **Polymorphism**: `customer.getDiscount()` returns different values based on actual type
3. **Method overriding**: Each customer subclass overrides `getDiscount()`

**Potential Questions:**
| Question | Where to Find Answer |
|----------|----------------------|
| "Why is `Customer` abstract and not an interface?" | Has fields (fullName, id, phoneNum), shared constructor logic, `generateShoppingList()` |
| "Where is polymorphism used in the sell process?" | `StoreBranch.sell()` line 279: `customer.getDiscount()` - returns different discount per type |
| "Why not use a single Customer class with a 'type' field?" | Violates Open/Closed principle - adding new type would require modifying Customer class |
| "How are discounts configured?" | From `config.json` via `JsonLoader.getDouble("customers.VIPCustomer")` |
| "Why do Products override `equals()` and `hashCode()`?" | To use as keys in `HashMap<Product, Integer>` for inventory/sellRecord |

---

### Topic 4: Design Patterns ⭐⭐

**Files to Study:**

- `ChatAvailabilityObserver.java` - Observer pattern
- `CustomerHandler.java` - Runnable (Command-like pattern)
- `StoreBranch.java` - Factory-like method `createProduct()`

**Key Concepts:**

1. **Observer Pattern**: `ChatAvailabilityObserver` - employees subscribe to notifications
2. **Factory Pattern**: `createProduct()` creates different product types based on string
3. **Thread Pool Pattern**: `ExecutorService` manages worker threads

**Potential Questions:**
| Question | Where to Find Answer |
|----------|----------------------|
| "Explain the Observer pattern in the chat system" | `ChatAvailabilityObserver` - employees subscribe, get notified when target is free |
| "Why not use Java's built-in Observer interface?" | It's deprecated; also, our use case is simpler (static methods, no Observable needed) |
| "What pattern is `createProduct()` using?" | Factory Method - creates objects without specifying exact class |
| "Why is `ChatAvailabilityObserver` using static methods?" | Shared across all `ClientHandler` instances - singleton-like behavior |

---

### Topic 5: Data Structures ⭐⭐

**Files to Study:**

- `StoreBranch.java` - `Queue<Customer>`, `Map<Product, Integer>`, `LinkedList<Employee>`
- `Customer.java` - `HashMap<Product, Integer>` for shopping list
- `ClientHandler.java` - `HashMap<String, String>` for request parsing

**Key Concepts:**

1. **Queue**: FIFO for customer line - `LinkedList` implements `Queue`
2. **Map**: Inventory tracking (Product → quantity), sell records
3. **LinkedList**: Employees (preserves insertion order, efficient add/remove)

**Potential Questions:**
| Question | Where to Find Answer |
|----------|----------------------|
| "Why use Queue for customers?" | FIFO - first customer in line gets served first |
| "Why LinkedList and not ArrayDeque for the queue?" | Both work; LinkedList chosen for simplicity |
| "Why Map<Product, Integer> instead of List<Product>?" | Need to track quantity per product, O(1) lookup vs O(n) |
| "What happens when customerQueue.poll() is called on empty queue?" | Returns null (not exception) - handled in `handleSell()` |

---

### Topic 6: Synchronization Details ⭐⭐⭐

**Files to Study:**

- `StoreBranch.java` - `synchronized sell()`, `synchronized(branch)` in `handleSell()`
- `ChatAvailabilityObserver.java` - `synchronized` static methods
- `ClientHandler.java` - various `synchronized(chain)` blocks

**Key Concepts:**

1. **Method-level sync**: `synchronized double sell()` - locks on `this` (the branch)
2. **Block-level sync**: `synchronized(chain)` - locks specific object
3. **Static sync**: `synchronized static` methods lock on the Class object

**Potential Questions:**
| Question | Where to Find Answer |
|----------|----------------------|
| "What object is locked when we call `synchronized sell()`?" | The `StoreBranch` instance (`this`) |
| "Why `synchronized(chain)` instead of `synchronized(branch)` in reports?" | Reports iterate all branches - need to lock the entire chain |
| "Is `cashierBusyStatus` map thread-safe?" | No - but only accessed from synchronized contexts |
| "What's the risk if we remove `synchronized` from `sell()`?" | Race condition: two threads could sell same product, causing negative inventory |

---

### Topic 7: Configuration & Utilities ⭐

**Files to Study:**

- `JsonLoader.java` - Configuration loading and saving
- `config.json` - Understanding the structure
- `Logger.java` - File logging

**Potential Questions:**
| Question | Where to Find Answer |
|----------|----------------------|
| "How does the system load configuration?" | `JsonLoader.load()` reads `config.json` at startup |
| "How are changes persisted (e.g., inventory updates)?" | `JsonLoader.set()` + `JsonLoader.save()` writes to config.json |
| "Why use a custom JsonLoader instead of libraries?" | Learning exercise, fine-grained control |

---

## 🔥 "Why X and Not Y?" Questions (Professor's Favorites)

| Question                                                         | Good Answer                                                                             |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| "Why sockets instead of HTTP/REST?"                              | Real-time bidirectional communication (push notifications, chat), persistent connection |
| "Why one thread per client instead of async/NIO?"                | Simpler to understand and implement; acceptable for small number of clients             |
| "Why `synchronized` keyword instead of `ReentrantLock`?"         | Simpler syntax for our use case; `ReentrantLock` would be overkill                      |
| "Why `LinkedList` for Queue instead of `ConcurrentLinkedQueue`?" | We already synchronize externally; plus, we need to iterate for `VIEW_CUSTOMERS`        |
| "Why abstract class `Customer` not interface?"                   | Need to share implementation (fields, constructor, `generateShoppingList()`)            |
| "Why `ExecutorService` instead of manual thread creation?"       | Thread pooling, reuse, controlled parallelism, clean shutdown                           |
| "Why store discounts in config.json not in code?"                | Configuration over code - can change without recompilation                              |
| "Why split `ClientHandler` and `CustomerHandler`?"               | Separation of concerns - request handling vs. business logic                            |
| "Why is `handleSell()` not synchronized but `sell()` is?"        | `handleSell()` does minimal work before delegating; `sell()` modifies shared state      |

---

## 🧠 Quick Code Walkthrough - Key Methods to Memorize

### 1. Server Startup Flow

```
ServerApp.main()
  → JsonLoader.load()          // Load config
  → generateChain()            // Create Chain with branches
  → new StoreServer().start()  // Start socket server
```

### 2. Client Connection Flow

```
StoreServer.start()
  → serverSocket.accept()      // Wait for connection
  → new ClientHandler(socket)  // Create handler
  → new Thread(handler).start() // Run in separate thread
```

### 3. Sell Flow (CRITICAL)

```
ClientHandler.handleSell()
  → branch.getNextCustomer()        // Dequeue customer (synchronized)
  → branch.setCashierBusy(true)     // Mark cashier busy
  → new CustomerHandler()           // Create checkout task
  → branch.submitCustomerForCheckout() // Submit to thread pool
    ↓
CustomerHandler.run() [in thread pool]
  → Thread.sleep(2-5s)              // Simulate checkout
  → branch.sell(customer, cashierId) // Actual sale (synchronized)
  → finally: setCashierBusy(false)  // Mark free
  → notifyWaitingEmployees()        // Observer notification
```

### 4. Customer Discount Polymorphism

```java
// In StoreBranch.sell():
double finalPrice = sum * customer.getDiscount();
// customer.getDiscount() calls:
//   - VIPCustomer.getDiscount()     → returns 0.5 (50% discount)
//   - ReturningCustomer.getDiscount() → returns 0.8 (20% discount)
//   - NewCustomer.getDiscount()     → returns 1.0 (no discount)
```

---

## 📝 Critical Line Numbers to Know

| File                   | Lines   | What's There                               |
| ---------------------- | ------- | ------------------------------------------ |
| `StoreServer.java`     | 35-55   | Accept loop, thread creation               |
| `StoreBranch.java`     | 30-47   | Thread pool initialization, customer queue |
| `StoreBranch.java`     | 251-288 | `sell()` method - the core business logic  |
| `ClientHandler.java`   | 52-89   | `run()` - protocol parsing                 |
| `ClientHandler.java`   | 370-401 | `handleSell()` - sell request handling     |
| `CustomerHandler.java` | 21-40   | `run()` - async checkout                   |
| `Customer.java`        | 15      | `abstract double getDiscount()`            |
| `VIPCustomer.java`     | 11-14   | `getDiscount()` override                   |

---

## ✅ Pre-Exam Checklist

Every team member should be able to:

- [ ] Draw the architecture diagram from memory
- [ ] Explain the communication protocol format
- [ ] Trace a SELL request from client to server and back
- [ ] Explain why `sell()` is synchronized
- [ ] Explain the thread pool purpose and configuration
- [ ] Explain Customer polymorphism and where it's used
- [ ] Answer at least 3 "Why X and not Y?" questions
- [ ] Point to specific line numbers for key functionality

---

_Last updated: 2026-01-16_
