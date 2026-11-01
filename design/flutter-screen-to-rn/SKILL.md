---
name: flutter-screen-to-rn
description: Port one Flutter screen or page (lib/presentation/screens/**, sheets/**, or a stateful app widget) to a React Native screen in apps/mobile/src/screens using @vidaxl/ui components, TanStack Query hooks, Zustand stores, AppNav.go and i18n keys. Use it when you're asked to port, rebuild or review a screen/page/tab/sheet (e.g. "port OrdersPage", "convert live_home.dart", "build the cart screen"), or when you need the patterns for loading/error/empty/sign-in states, demo vs live branches, pull-to-refresh, paging, sheets and toasts. Includes a worked mini example.
---

# Porting a Flutter screen

Read the `flutter-to-rn-migration` skill first for the general procedure (matrix row, header, test, update). This skill covers what's
specific to screens. Mapping tables: `.claude/skills/flutter-to-rn-migration/references/` (widget, state, navigation, l10n).

## Steps

1. **Read the whole Dart file** and list its widgets: the public page, private `_Xxx` widgets, sheets it opens, and the scope reads
   (`MemberScope`, `LoyaltyScope`, `CartScope`, `XxxSource.maybeOf`). Note every `AppNav.go(...)`, `showToast`, `showVidaSheet`,
   `refreshXxx()` and every `l10n.key`.
2. **Find the branches.** Most screens render differently in three modes; keep all of them:
   - `demo`: no live loyalty state (`LiveMode.demo`, `XxxSource.maybeOf` returns null) → sample data from `useMemberStore`.
   - `needsSignIn`: live but signed out → `LiveSignIn`.
   - `live` → the query hooks.
3. **Map the data.** Each repository call becomes a hook from `apps/mobile/src/hooks` (names in TRACEABILITY §c: `useXxx` for queries,
   `useXxxMutation` for mutations). If a hook doesn't exist yet, write it next to the others, or ask the App-Architecture owner.
4. **Lay out** with `@vidaxl/ui` (`SubPageScaffold`/`TabBody` from `apps/mobile/src/components`, `PageTitle`, `SectionHead`, `VidaCard`,
   `PrimaryButton`, `EmptyState`, `MenuRow`, …). These components keep the Dart names and props, so the JSX follows the Dart tree.
5. **States**, in the Dart order (usually): loading when there's nothing to show → error with retry when there's nothing to show →
   empty → content (+ inline "more" error / "Load more"). Use `LiveLoading`, `LiveError` (pass `error` when the Dart code does, which enables
   "Check connection"), `LiveSignIn` and `EmptyState`.
6. **Interactions:** `AppNav.go(route)` with the same route strings; sheets through `showVidaSheet` / `useSheet`; toasts with
   `showToast(t('key'))`; mutations with `mutateAsync` when the next step needs the result (reward wheel, navigation to the order).
   Invalidate the same data the Dart code refreshes.
7. **Lists:** `FlatList` for API lists. Copy the Dart paging UX exactly: some screens use a **"Load more" button** (OrdersPage, ActivityPage),
   others load on scroll (`ProductFeed`, `NearEndListener` → `onEndReached`). Pull to refresh only where Dart has a `RefreshIndicator`.
8. **i18n:** `const { t } = useTranslation()`; the same keys as `context.l10n.key`; params by their ARB names. Literal strings stay literal.
9. **Accessibility and test hooks:** `accessibilityLabel`/`Role` from `Semantics`; `testID` where the ported tests find widgets by key
   (`ValueKey('order-…')` → `testID="order-…"`).
10. **Port the screen's widget tests** (skill `flutter-test-to-jest`), including the "fits 360px" / French variants. Then update the row.

## Worked mini example: `OrdersPage` (`lib/presentation/screens/account/orders_page.dart`, 148 lines)

Dart (abridged):

```dart
class OrdersPage extends StatelessWidget {
  Widget build(BuildContext context) {
    final apis = AccountSource.maybeOf(context);
    if (apis != null && liveSignedIn(context)) return _LiveOrders(apis: apis);
    final orders = MemberScope.of(context).orders;                // demo
    return SubPageScaffold(title: l10n.accountOrdersTitle, children: [
      PageTitle(l10n.accountOrdersHeadline, subtitle: l10n.accountOrdersSubtitle),
      if (orders.isEmpty) EmptyState(icon: VidaIcons.box, title: …EmptyTitle, body: …EmptyBody,
          action: PrimaryButton(l10n.rewardsExploreOffers, full: false, onPressed: () => AppNav.go(context, 'offers')))
      else for (final o in orders) OrderCard(o),
    ]);
  }
}
// _LiveOrders: GET /me/orders; loading → LiveLoading(accountOrdersLoading); error → LiveError(liveErrorMessage(e), onRetry: _load);
// empty → EmptyState(…LiveEmptyBody, PrimaryButton(accountOrdersShop → 'products')); list of LiveOrderCard(key: 'order-<id>');
// _moreError as SmallText; "Load more" SecondaryButton while nextCursor != null (label accountOrdersLoadingMore while loading);
// de-duplicates by id when appending.
```

React Native:

```tsx
// Ported from: lib/presentation/screens/account/orders_page.dart
import React from 'react';
import { useTranslation } from 'react-i18next';
import { EmptyState, PageTitle, PrimaryButton, SecondaryButton, SmallText, VidaIcons } from '@vidaxl/ui';

import { SubPageScaffold } from '../../components/SubPageScaffold';
import { OrderCard, LiveOrderCard } from '../../components/OrderCard';
import { LiveError, LiveLoading, liveErrorMessage } from '../../components/LiveStatusViews';
import { useAccountApis, useLiveSignedIn } from '../../hooks/useAccountApis';
import { useMyOrders } from '../../hooks/useOrders';
import { useMemberStore } from '../../state/memberStore';
import { AppNav } from '../../navigation/appNav';

/** Figma "Orders" (`20:619`). Route `orders`: live `GET /me/orders` when signed in, sample orders otherwise. */
export function OrdersPage() {
  const apis = useAccountApis();
  const live = useLiveSignedIn();
  if (apis && live) return <LiveOrders />;
  return <DemoOrders />;
}

function DemoOrders() {
  const { t } = useTranslation();
  const orders = useMemberStore((s) => s.orders);
  return (
    <SubPageScaffold title={t('accountOrdersTitle')}>
      <PageTitle title={t('accountOrdersHeadline')} subtitle={t('accountOrdersSubtitle')} />
      {orders.length === 0 ? (
        <EmptyState
          icon={VidaIcons.box}
          title={t('accountOrdersEmptyTitle')}
          body={t('accountOrdersEmptyBody')}
          action={<PrimaryButton label={t('rewardsExploreOffers')} full={false} onPressed={() => AppNav.go('offers')} />}
        />
      ) : (
        orders.map((o) => <OrderCard key={o.id} order={o} />)
      )}
    </SubPageScaffold>
  );
}

function LiveOrders() {
  const { t } = useTranslation();
  // useInfiniteQuery over OrdersRepository.myOrders({ cursor }); `select` de-duplicates by id like `_more()`.
  const q = useMyOrders();
  const orders = q.data?.orders ?? [];
  return (
    <SubPageScaffold title={t('accountOrdersTitle')}>
      <PageTitle title={t('accountOrdersHeadline')} subtitle={t('accountOrdersLiveSubtitle')} />
      {q.isPending ? (
        <LiveLoading label={t('accountOrdersLoading')} />
      ) : q.isError && orders.length === 0 ? (
        <LiveError message={liveErrorMessage(t, q.error)} onRetry={() => q.refetch()} />
      ) : orders.length === 0 ? (
        <EmptyState
          icon={VidaIcons.box}
          title={t('accountOrdersEmptyTitle')}
          body={t('accountOrdersLiveEmptyBody')}
          action={<PrimaryButton label={t('accountOrdersShop')} full={false} onPressed={() => AppNav.go('products')} />}
        />
      ) : (
        <>
          {orders.map((o) => <LiveOrderCard key={o.id} order={o} testID={`order-${o.id}`} />)}
          {q.isFetchNextPageError ? <SmallText text={liveErrorMessage(t, q.error)} /> : null}
          {q.hasNextPage ? (
            <SecondaryButton
              label={q.isFetchingNextPage ? t('accountOrdersLoadingMore') : t('accountOrdersLoadMore')}
              onPressed={q.isFetchingNextPage ? null : () => q.fetchNextPage()}
            />
          ) : null}
        </>
      )}
    </SubPageScaffold>
  );
}
```

What carried over: both branches; the same keys; `offers` vs `products` targets (different in demo and live!); the "Load more"
**button**, not infinite scroll; the inline "more" error; the `order-<id>` test id. Check the real prop names of `@vidaxl/ui` and the app
components before copying this: the example shows the shape, not a contract.

## Screen checklist

- [ ] All branches (demo / needsSignIn / live) and every conditional section from the Dart `build`.
- [ ] Loading, error (+ retry, + "Check connection" when Dart passes `error`), empty, content; inline errors for secondary loads.
- [ ] Pull to refresh where Dart has `RefreshIndicator`, refreshing the same things (`LiveHome` refreshes `/home`, `/me` and categories).
- [ ] Paging UX identical (button vs scroll), with de-duplication when Dart does it.
- [ ] Sheets/dialogs/toasts identical in content and result handling; reward wheel shown where Dart shows it.
- [ ] Every `AppNav.go` target identical; `PopScope` → `beforeRemove`.
- [ ] Invalidation after mutations matches the Dart `refreshXxx()` calls.
- [ ] Timers cleaned up; countdowns use the server clock skew where Dart does.
- [ ] Hidden-in-design widgets not rendered, with a comment.
- [ ] Renders at width 360 in French without clipping important text.
- [ ] Widget tests ported; matrix row updated.
