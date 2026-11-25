---
name: balance
description: Show the looot balance (available and reserved credit) and, when the person asks to add credit, open a Stripe top-up link for them to pay. Use for "how much looot credit do I have" or "top up looot".
argument-hint: "[top-up amount in USD]"
disable-model-invocation: true
---

# looot balance and top-up

Amount asked for, if any: $ARGUMENTS

1. Call `balance` with `{}` (free, opens no payment). Report `available` and `reserved` in dollars,
   and any `holds`.
2. If no amount was given and the balance is above $0, stop here. Mention that top-ups start at
   `topUpLink.minimumUsd` dollars.
3. If an amount was given, or the balance is $0 and the person wants to continue, call `top_up` with
   `{"amountUsd": <amount>}` (omit `amountUsd` to use the suggested amount). An amount below the
   minimum is refused: say the minimum and ask again.
4. Give the person `checkoutUrl` to pay on Stripe. If it is null, give `dashboardUrl` and the
   `reason`. Never enter card details yourself.
5. When they say they paid, call `balance` again and report the new `available`.
