---
name: rithum
description: Rithum B2B patterns and distribution API
---

# Rithum Best Practices

## Leverage Data Model Guarantees

Trust guaranteed non-null fields:

```java
// DO: Trust the data model guarantees
order.setTotalPrice(PriceUtils.centsToDollars(transactableBag.getTotal()));

// DON'T: Add unnecessary null checks
if (Objects.nonNull(transactableBag.getTotal())) {
  order.setTotalPrice(PriceUtils.centsToDollars(transactableBag.getTotal()));
}
```

## Clean Separation of Concerns

- Keep main composer methods focused on orchestration
- Extract complex logic into focused helper methods
- Use static utility classes for reusable functionality

## Common Compilation Issues

### OfferData.Shipping.Price Structure
```java
// CORRECT
OfferData.Shipping.Price price = new OfferData.Shipping.Price();

// WRONG
OfferData.Shipping.Method.Price price = new OfferData.Shipping.Method.Price();
```

### MerchantConfiguration Method Names
```java
// CORRECT
config.setRithumConfig(rithumConfig);

// WRONG
config.setRithum(rithumConfig);
```

### Type Consistency
```java
// CORRECT - merchantId is Integer
assertEquals(Integer.valueOf(12345), result.getMerchantId());

// WRONG
assertEquals(Long.valueOf(12345L), result.getMerchantId());
```

## Testing Patterns

### Static Method Mocking

```java
@Test
public void testOrderSyncWithFallbackShipping() {
  try (MockedStatic<RithumMerchantConfig> mockedRithumConfig = Mockito.mockStatic(RithumMerchantConfig.class)) {
    mockedRithumConfig.when(() -> RithumMerchantConfig.shouldUseFallbackShippingMethods(config)).thenReturn(true);

    List<OfferData.Shipping> result = rithumOrderSyncService.getShippingEstimates(request);

    assertNotNull(result);
    assertTrue(CollectionUtils.isNotEmpty(result));
  }
}
```

### Test Data Creation

```java
private DecryptedMerchantCredentials createDecryptedMerchantCredentials() {
  DecryptedMerchantCredentials dmc = new DecryptedMerchantCredentials();
  dmc.setMerchantId(12345);  // Use Integer, not Long
  dmc.setPlatform(Merchant.Platform.RITHUM);
  return dmc;
}
```

## Comprehensive Testing Strategy

- Test successful composition with complete data
- Test edge cases: null addresses, empty collections
- Test status mapping for all enum values
- Test fallback shipping configuration
- Verify property mapping accuracy
- Use realistic test data
