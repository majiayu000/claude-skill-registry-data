---
name: flashlist-patterns
description: FlashList high-performance list patterns. Use when implementing lists.
---

# FlashList Patterns Skill

This skill covers Shopify's FlashList for high-performance lists.

## When to Use

Use this skill when:
- Implementing any scrollable list
- Replacing FlatList
- Lists have 50+ items
- List performance is critical

## Core Principle

**FLASHLIST ALWAYS** - FlashList is 10x faster than FlatList. Use it for all lists.

## Installation

```bash
npm install @shopify/flash-list
```

## Basic Usage

```typescript
import { FlashList } from '@shopify/flash-list';

interface Item {
  id: string;
  title: string;
}

function ItemList({ items }: { items: Item[] }): React.ReactElement {
  return (
    <FlashList
      data={items}
      renderItem={({ item }) => (
        <View className="p-4 border-b border-gray-200">
          <Text className="text-lg">{item.title}</Text>
        </View>
      )}
      estimatedItemSize={60}  // Required!
      keyExtractor={(item) => item.id}
    />
  );
}
```

## Required Props

### estimatedItemSize

```typescript
// Required for FlashList to calculate recycling
<FlashList
  data={items}
  renderItem={renderItem}
  estimatedItemSize={80}  // Average height of items in pixels
/>
```

## Performance Optimization

### Memoize renderItem

```typescript
import { useCallback, memo } from 'react';

const ItemCard = memo(function ItemCard({ item }: { item: Item }) {
  return (
    <View className="p-4">
      <Text>{item.title}</Text>
    </View>
  );
});

function ItemList({ items }: { items: Item[] }): React.ReactElement {
  const renderItem = useCallback(
    ({ item }: { item: Item }) => <ItemCard item={item} />,
    []
  );

  return (
    <FlashList
      data={items}
      renderItem={renderItem}
      estimatedItemSize={60}
    />
  );
}
```

### Use keyExtractor

```typescript
<FlashList
  data={items}
  renderItem={renderItem}
  estimatedItemSize={60}
  keyExtractor={(item) => item.id}  // Unique stable key
/>
```

## Different Item Types

### getItemType

```typescript
interface ListItem {
  id: string;
  type: 'header' | 'item' | 'separator';
  data: unknown;
}

<FlashList
  data={items}
  renderItem={({ item }) => {
    switch (item.type) {
      case 'header':
        return <HeaderComponent data={item.data} />;
      case 'separator':
        return <SeparatorComponent />;
      default:
        return <ItemComponent data={item.data} />;
    }
  }}
  getItemType={(item) => item.type}  // Enables better recycling
  estimatedItemSize={60}
/>
```

### overrideItemLayout

```typescript
<FlashList
  data={items}
  renderItem={renderItem}
  estimatedItemSize={60}
  overrideItemLayout={(layout, item) => {
    // Set exact size for different item types
    if (item.type === 'header') {
      layout.size = 100;
    } else if (item.type === 'separator') {
      layout.size = 20;
    } else {
      layout.size = 60;
    }
  }}
/>
```

## Horizontal Lists

```typescript
<FlashList
  data={items}
  renderItem={renderItem}
  estimatedItemSize={150}
  horizontal
/>
```

## Grid Layout

```typescript
<FlashList
  data={items}
  renderItem={renderItem}
  estimatedItemSize={180}
  numColumns={2}
/>
```

## Pull to Refresh

```typescript
import { useState } from 'react';
import { RefreshControl } from 'react-native';

function RefreshableList(): React.ReactElement {
  const [refreshing, setRefreshing] = useState(false);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchNewData();
    setRefreshing(false);
  };

  return (
    <FlashList
      data={items}
      renderItem={renderItem}
      estimatedItemSize={60}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    />
  );
}
```

## Infinite Scroll

```typescript
function InfiniteList(): React.ReactElement {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  const loadMore = async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    const newItems = await fetchMoreItems();

    if (newItems.length === 0) {
      setHasMore(false);
    } else {
      setItems((prev) => [...prev, ...newItems]);
    }
    setLoading(false);
  };

  return (
    <FlashList
      data={items}
      renderItem={renderItem}
      estimatedItemSize={60}
      onEndReached={loadMore}
      onEndReachedThreshold={0.5}
      ListFooterComponent={loading ? <ActivityIndicator /> : null}
    />
  );
}
```

## Empty State

```typescript
<FlashList
  data={items}
  renderItem={renderItem}
  estimatedItemSize={60}
  ListEmptyComponent={
    <View className="flex-1 items-center justify-center p-8">
      <Text className="text-gray-500">No items found</Text>
    </View>
  }
/>
```

## Headers and Footers

```typescript
<FlashList
  data={items}
  renderItem={renderItem}
  estimatedItemSize={60}
  ListHeaderComponent={
    <View className="p-4 bg-gray-100">
      <Text className="text-xl font-bold">Items</Text>
    </View>
  }
  ListFooterComponent={
    <View className="p-4">
      <Text className="text-gray-500 text-center">End of list</Text>
    </View>
  }
/>
```

## Sticky Headers

```typescript
interface Section {
  title: string;
  data: Item[];
}

// Use SectionList-like pattern
<FlashList
  data={flattenedData}
  renderItem={({ item }) => {
    if (item.isHeader) {
      return <StickyHeader title={item.title} />;
    }
    return <ItemCard item={item} />;
  }}
  stickyHeaderIndices={headerIndices}
  estimatedItemSize={60}
  getItemType={(item) => (item.isHeader ? 'header' : 'item')}
/>
```

## Scroll to Item

```typescript
import { useRef } from 'react';
import { FlashList } from '@shopify/flash-list';

function ScrollableList(): React.ReactElement {
  const listRef = useRef<FlashList<Item>>(null);

  const scrollToTop = () => {
    listRef.current?.scrollToOffset({ offset: 0, animated: true });
  };

  const scrollToIndex = (index: number) => {
    listRef.current?.scrollToIndex({ index, animated: true });
  };

  return (
    <>
      <FlashList
        ref={listRef}
        data={items}
        renderItem={renderItem}
        estimatedItemSize={60}
      />
      <Button onPress={scrollToTop}>Scroll to Top</Button>
    </>
  );
}
```

## Common Props

```typescript
<FlashList
  data={items}
  renderItem={renderItem}
  estimatedItemSize={60}
  keyExtractor={(item) => item.id}
  getItemType={(item) => item.type}
  numColumns={1}
  horizontal={false}
  inverted={false}
  showsVerticalScrollIndicator={true}
  showsHorizontalScrollIndicator={false}
  onEndReached={loadMore}
  onEndReachedThreshold={0.5}
  refreshControl={<RefreshControl />}
  ListHeaderComponent={<Header />}
  ListFooterComponent={<Footer />}
  ListEmptyComponent={<EmptyState />}
  ItemSeparatorComponent={() => <View className="h-px bg-gray-200" />}
/>
```

## Debug Mode

```typescript
// Enable debug logs in development
<FlashList
  data={items}
  renderItem={renderItem}
  estimatedItemSize={60}
  // Debug overlay shows recycling info
/>
```

## Notes

- `estimatedItemSize` is required
- Use `getItemType` for different item layouts
- Memoize renderItem with useCallback
- Use React.memo for item components
- FlashList recycles views for performance
- Test with large datasets (1000+ items)
