---
name: financekit
description: "Access Apple Card, Apple Cash, and Wallet financial data using FinanceKit. Use when querying transaction history, reading account balances, accessing Wallet orders, requesting financial data authorization, or building personal finance features that integrate with Apple's financial services."
---

# FinanceKit

Access financial data from Apple Wallet including Apple Card, Apple Cash, and Apple Card Savings. FinanceKit provides on-device, offline access to accounts, balances, and transactions with user-controlled authorization. Targets Swift 6.3 / iOS 26+. Query APIs are available from iOS 17.4; background delivery requires iOS 26.

## Contents

- [Setup and Entitlements](#setup-and-entitlements)
- [Data Availability](#data-availability)
- [Authorization](#authorization)
- [Querying Accounts](#querying-accounts)
- [Account Balances](#account-balances)
- [Querying Transactions](#querying-transactions)
- [Long-Running Queries and History](#long-running-queries-and-history)
- [Transaction Picker](#transaction-picker)
- [Wallet Orders](#wallet-orders)
- [Background Delivery](#background-delivery)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup and Entitlements

### Requirements

1. **Managed entitlement** -- request `com.apple.developer.financekit` from Apple via the [FinanceKit entitlement request form](https://developer.apple.com/contact/request/financekit/). This is a managed capability; Apple reviews each application.
2. **Organization-level Apple Developer account** (individual accounts are not eligible).
3. **Account Holder role** required to request the entitlement.

### Project Configuration

1. Add the FinanceKit entitlement through Xcode managed capabilities after Apple approves the request.
2. Add `NSFinancialDataUsageDescription` to Info.plist -- this string is shown to the user during the authorization prompt.

```xml
<key>NSFinancialDataUsageDescription</key>
<string>This app uses your financial data to track spending and provide budgeting insights.</string>
```

## Data Availability

Check whether the device supports FinanceKit before making any API calls. This value is constant across launches and iOS versions.

```swift
import FinanceKit

guard FinanceStore.isDataAvailable(.financialData) else {
    // FinanceKit not available -- do not call any other financial data APIs.
    // The framework terminates the app if called when unavailable.
    return
}
```

For Wallet orders:

```swift
guard FinanceStore.isDataAvailable(.orders) else { return }
```

Data availability returning `true` does not guarantee data exists on the device. Data access can also become temporarily restricted (e.g., Wallet unavailable, MDM restrictions). Restricted access throws `FinanceError.dataRestricted` rather than terminating.

## Authorization

Request authorization to access user-selected financial accounts. The system presents an account picker where the user chooses which accounts to share and the earliest transaction date to expose.

```swift
let store = FinanceStore.shared

let status = try await store.requestAuthorization()
switch status {
case .authorized:    break  // Proceed with queries
case .denied:        break  // User declined
case .notDetermined: break  // No meaningful choice made
@unknown default:    break
}
```

### Checking Current Status

Query current authorization without prompting:

```swift
let currentStatus = try await store.authorizationStatus()
```

Once the user grants or denies access, `requestAuthorization()` returns the cached decision without showing the prompt again. Users can change access in Settings > Privacy & Security > Financial Data.

## Querying Accounts

Accounts are modeled as an enum with two cases: `.asset` (e.g., Apple Cash, Savings) and `.liability` (e.g., Apple Card credit). Both share common properties (`id`, `displayName`, `institutionName`, `currencyCode`) while liability accounts add credit-specific fields.

```swift
func fetchAccounts() async throws -> [Account] {
    let query = AccountQuery(
        sortDescriptors: [SortDescriptor(\Account.displayName)],
        predicate: nil,
        limit: nil,
        offset: nil
    )

    return try await store.accounts(query: query)
}
```

### Working with Account Types

```swift
switch account {
case .asset(let asset):
    print("Asset account, currency: \(asset.currencyCode)")
case .liability(let liability):
    if let limit = liability.creditInformation.creditLimit {
        print("Credit limit: \(limit.amount) \(limit.currencyCode)")
    }
}
```

## Account Balances

Balances represent the amount in an account at a point in time. A `CurrentBalance` is one of three cases: `.available` (includes pending), `.booked` (posted only), or `.availableAndBooked`.

```swift
func fetchBalances(for accountID: UUID) async throws -> [AccountBalance] {
    let predicate = #Predicate<AccountBalance> { balance in
        balance.accountID == accountID
    }

    let query = AccountBalanceQuery(
        sortDescriptors: [SortDescriptor(\AccountBalance.id)],
        predicate: predicate,
        limit: nil,
        offset: nil
    )

    return try await store.accountBalances(query: query)
}
```

### Reading Balance Amounts

Amounts are always positive decimals. Use `creditDebitIndicator` to determine the sign:

```swift
func formatBalance(_ balance: Balance) -> String {
    let sign = balance.creditDebitIndicator == .debit ? "-" : ""
    return "\(sign)\(balance.amount.amount) \(balance.amount.currencyCode)"
}

// Extract from CurrentBalance enum:
switch balance.currentBalance {
case .available(let bal):       formatBalance(bal)
case .booked(let bal):          formatBalance(bal)
case .availableAndBooked(let available, _): formatBalance(available)
@unknown default: "Unknown"
}
```

## Querying Transactions

Use `TransactionQuery` with Swift predicates, sort descriptors, limit, and offset.

```swift
let predicate = #Predicate<Transaction> { $0.accountID == accountID }

let query = TransactionQuery(
    sortDescriptors: [SortDescriptor(\Transaction.transactionDate, order: .reverse)],
    predicate: predicate,
    limit: 50,
    offset: nil
)

let transactions = try await store.transactions(query: query)
```

### Reading Transaction Data

```swift
let amount = transaction.transactionAmount
let direction = transaction.creditDebitIndicator == .debit ? "spent" : "received"
print("\(transaction.transactionDescription): \(direction) \(amount.amount) \(amount.currencyCode)")
// merchantName, merchantCategoryCode, foreignCurrencyAmount are optional
```

### Built-In Predicate Helpers

FinanceKit provides factory methods for common filters:

```swift
// Filter by transaction status
let bookedOnly = TransactionQuery.predicate(forStatuses: [.booked])

// Filter by transaction type
let purchases = TransactionQuery.predicate(forTransactionTypes: [.pointOfSale, .directDebit])

// Filter by merchant category
let groceries = TransactionQuery.predicate(forMerchantCategoryCodes: [
    MerchantCategoryCode(rawValue: 5411)  // Grocery stores
])
```

### Transaction Properties Reference

| Property | Type | Notes |
|---|---|---|
| `id` | `UUID` | Unique per device |
| `accountID` | `UUID` | Links to parent account |
| `transactionDate` | `Date` | When the transaction occurred |
| `postedDate` | `Date?` | When booked; nil if pending |
| `transactionAmount` | `CurrencyAmount` | Always positive |
| `creditDebitIndicator` | `CreditDebitIndicator` | `.debit` or `.credit` |
| `transactionDescription` | `String` | Display-friendly description |
| `originalTransactionDescription` | `String` | Raw institution description |
| `merchantName` | `String?` | Merchant name if available |
| `merchantCategoryCode` | `MerchantCategoryCode?` | ISO 18245 code |
| `transactionType` | `TransactionType` | `.pointOfSale`, `.transfer`, etc. |
| `status` | `TransactionStatus` | `.authorized`, `.pending`, `.booked`, `.memo`, `.rejected` |
| `foreignCurrencyAmount` | `CurrencyAmount?` | Foreign currency if applicable |
| `foreignCurrencyExchangeRate` | `Decimal?` | Exchange rate if applicable |

## Long-Running Queries and History

Use `AsyncSequence`-based history APIs for live updates or resumable sync. These return `FinanceStore.Changes` (inserted, updated, deleted items) plus a `HistoryToken` for resumption.

```swift
func monitorTransactions(for accountID: UUID) async throws {
    let history = store.transactionHistory(
        forAccountID: accountID,
        since: loadSavedToken(),
        isMonitoring: true  // true = keep streaming; false = terminate after catch-up
    )

    for try await changes in history {
        // changes.inserted, changes.updated, changes.deleted
        saveToken(changes.newToken)
    }
}
```

### History Token Persistence

`HistoryToken` conforms to `Codable`. Persist it to resume queries without reprocessing data:

```swift
func saveToken(_ token: FinanceStore.HistoryToken) {
    if let data = try? JSONEncoder().encode(token) {
        UserDefaults.standard.set(data, forKey: "financeHistoryToken")
    }
}

func loadSavedToken() -> FinanceStore.HistoryToken? {
    guard let data = UserDefaults.standard.data(forKey: "financeHistoryToken") else { return nil }
    return try? JSONDecoder().decode(FinanceStore.HistoryToken.self, from: data)
}
```

If a saved token points to compacted history, the framework throws `FinanceError.historyTokenInvalid`. Discard the token and start fresh.

### Account and Balance History

```swift
let accountChanges = store.accountHistory(since: nil, isMonitoring: true)
let balanceChanges = store.accountBalanceHistory(forAccountID: accountID, since: nil, isMonitoring: true)
```

## Transaction Picker

For apps that need selective, ephemeral access without full authorization, use `TransactionPicker` from FinanceKitUI. Access is not persisted -- transactions are passed directly for immediate use.

```swift
import FinanceKitUI

struct ExpenseImportView: View {
    @State private var selectedTransactions: [Transaction] = []

    var body: some View {
        if FinanceStore.isDataAvailable(.financialData) {
            TransactionPicker(selection: $selectedTransactions) {
                Label("Import Transactions", systemImage: "creditcard")
            }
        }
    }
}
```

## Wallet Orders

FinanceKit supports saving and querying Wallet orders (e.g., purchase receipts, shipping tracking).

### Saving an Order

```swift
let result = try await store.saveOrder(signedArchive: archiveData)
switch result {
case .added:        break  // Saved
case .cancelled:    break  // User cancelled
case .newerExisting: break // Newer version already in Wallet
@unknown default:   break
}
```

### Checking for an Existing Order

```swift
let orderID = FullyQualifiedOrderIdentifier(
    orderTypeIdentifier: "com.merchant.order",
    orderIdentifier: "ORDER-123"
)
let result = try await store.containsOrder(matching: orderID, updatedDate: lastKnownDate)
// result: .exists, .newerExists, .olderExists, or .notFound
```

### Add Order to Wallet Button (FinanceKitUI)

```swift
import FinanceKitUI

AddOrderToWalletButton(signedArchive: orderData) { result in
    // result: .success(SaveOrderResult) or .failure(Error)
}
```

## Background Delivery

iOS 26+ supports background delivery extensions that notify your app of financial data changes outside its lifecycle. Requires App Groups to share data between the app and extension.

### Enabling Background Delivery

```swift
try await store.enableBackgroundDelivery(
    for: [.transactions, .accountBalances],
    frequency: .daily
)
```

Available frequencies: `.hourly`, `.daily`, `.weekly`.

Disable selectively or entirely:

```swift
try await store.disableBackgroundDelivery(for: [.transactions])
try await store.disableAllBackgroundDelivery()
```

### Background Delivery Extension

Create a background delivery extension target in Xcode (Background Delivery Extension template). Both the app and extension must belong to the same App Group.

```swift
import FinanceKit

struct MyFinanceExtension: BackgroundDeliveryExtension {
    var body: some BackgroundDeliveryExtensionProviding { FinanceDataHandler() }
}

struct FinanceDataHandler: BackgroundDeliveryExtensionProviding {
    func didReceiveData(for dataTypes: [FinanceStore.BackgroundDataType]) async {
        for dataType in dataTypes {
            switch dataType {
            case .transactions:    await processNewTransactions()
            case .accountBalances: await updateBalanceCache()
            case .accounts:        await refreshAccountList()
            @unknown default:      break
            }
        }
    }

    func willTerminate() async { /* Clean up */ }
}
```

## Common Mistakes

### 1. Calling APIs when data is unavailable

DON'T -- skip availability check:
```swift
let store = FinanceStore.shared
let status = try await store.requestAuthorization() // Terminates if unavailable
```

DO -- guard availability first:
```swift
guard FinanceStore.isDataAvailable(.financialData) else {
    showUnavailableMessage()
    return
}
let status = try await FinanceStore.shared.requestAuthorization()
```

### 2. Ignoring the credit/debit indicator

DON'T -- treat amounts as signed values:
```swift
let spent = transaction.transactionAmount.amount // Always positive
```

DO -- apply the indicator:
```swift
let amount = transaction.transactionAmount.amount
let signed = transaction.creditDebitIndicator == .debit ? -amount : amount
```

### 3. Not handling data restriction errors

DON'T -- assume authorized access persists:
```swift
let transactions = try await store.transactions(query: query) // Fails if Wallet restricted
```

DO -- catch `FinanceError`:
```swift
do {
    let transactions = try await store.transactions(query: query)
} catch let error as FinanceError {
    if case .dataRestricted = error { showDataRestrictedMessage() }
}
```

### 4. Requesting full snapshots instead of resumable queries

DON'T -- fetch everything on every launch:
```swift
let allTransactions = try await store.transactions(query: TransactionQuery(
    sortDescriptors: [SortDescriptor(\Transaction.transactionDate)],
    predicate: nil, limit: nil, offset: nil
))
```

DO -- use history tokens for incremental sync:
```swift
let history = store.transactionHistory(
    forAccountID: accountID,
    since: loadSavedToken(),
    isMonitoring: false
)
for try await changes in history {
    processChanges(changes)
    saveToken(changes.newToken)
}
```

### 5. Not persisting history tokens

DON'T -- discard the token:
```swift
for try await changes in history {
    processChanges(changes)
    // Token lost -- next launch reprocesses everything
}
```

DO -- save every token:
```swift
for try await changes in history {
    processChanges(changes)
    saveToken(changes.newToken)
}
```

### 6. Misinterpreting credit/debit on liability accounts

Both asset and liability accounts use `.debit` for outgoing money. But `.credit` means different things: on an asset account it means money received; on a liability account it means a payment or refund that increases available credit. See [references/financekit-patterns.md](references/financekit-patterns.md) for a full interpretation table.

## Review Checklist

- [ ] `FinanceStore.isDataAvailable(.financialData)` checked before any API call
- [ ] `com.apple.developer.financekit` entitlement requested and approved by Apple
- [ ] `NSFinancialDataUsageDescription` set in Info.plist with a clear, specific message
- [ ] Organization-level Apple Developer account used
- [ ] Authorization status handled for all cases (`.authorized`, `.denied`, `.notDetermined`)
- [ ] `FinanceError.dataRestricted` caught and handled gracefully
- [ ] `CreditDebitIndicator` applied correctly to amounts (not treated as signed)
- [ ] History tokens persisted for resumable queries
- [ ] `FinanceError.historyTokenInvalid` handled by discarding token and restarting
- [ ] Long-running queries use `isMonitoring: false` when live updates are not needed
- [ ] Transaction picker used when full authorization is unnecessary
- [ ] Only data the app genuinely needs is queried
- [ ] Deleted data from history changes is removed from local storage
- [ ] Background delivery extension in same App Group as the main app (iOS 26+)
- [ ] Financial data deleted when user revokes access

## References

- Extended patterns (predicates, sorting, pagination, currency formatting, background updates): [references/financekit-patterns.md](references/financekit-patterns.md)
- [FinanceKit framework](https://sosumi.ai/documentation/financekit)
- [FinanceKitUI framework](https://sosumi.ai/documentation/financekitui)
- [FinanceStore](https://sosumi.ai/documentation/financekit/financestore)
- [Transaction](https://sosumi.ai/documentation/financekit/transaction)
- [Account](https://sosumi.ai/documentation/financekit/account)
- [AccountBalance](https://sosumi.ai/documentation/financekit/accountbalance)
- [FinanceKit entitlement](https://sosumi.ai/documentation/bundleresources/entitlements/com.apple.developer.financekit)
- [Implementing a background delivery extension](https://sosumi.ai/documentation/financekit/implementing-a-background-delivery-extension)
- [Meet FinanceKit (WWDC24)](https://sosumi.ai/videos/play/wwdc2024/2023/)
