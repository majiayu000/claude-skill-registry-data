---
name: rideshare
description: >-
  When the user asks you to get them a ride, call a car, or book an Uber, Lyft,
  Bolt, Grab, or another rideshare for now or for a set time, before you open
  the service or request anything.
---
# Rideshare

You request rides for the user on Uber, Lyft, Bolt, Grab, or whichever service works where they are. A ride is a purchase with a driver on the way, so the user picks the option and the user confirms the request. Your job ends with a message the user can find their car from.

## Entry points

- "Get me an Uber to SFO" names the destination; the pickup is wherever the user is.
- "I need a ride from the office to 500 Howard at 6" names both ends and a time.
- "Can you get me a Lyft?" names the service and nothing else; the destination is the first thing to resolve.
- "Book a car for tomorrow at 7am to the airport" is a scheduled ride, not an immediate one.

## Before you start

- Resolve the pickup. Use the location the user stated, then a home or office address from the Memory section, then ask. Confirm the exact pickup spot in prose before you request, because a wrong pin sends the driver to the wrong door.
- Resolve the destination the same way. Saved places in memory (home, work, the gym) beat retyping an address.
- Decide immediate versus scheduled. "First thing tomorrow" or "at 6" means a scheduled ride. Ask for the time if it is missing, and state the weekday, date, and time in the user's zone from the Time section before you enter it.
- Run SearchPlugins for the service the user named, and for the services they usually use if they did not name one. Use a connector when one is installed. When SearchPlugins finds a matching connector that is not installed, ask in the user's words. Send a question widget whose prompt is "Add the <service> connector?" with Yes / No. Do not say plugin, MCP, or plugin id. The widget ends the turn. On yes, follow the Cursor-managed `add-connector` skill: GetPlugin, then InstallPlugin with the stable plugin id on the next turn. Never paste a connect link. New tools arrive on the following message. If the search finds nothing, open the service's web app in your browser, `m.uber.com` for Uber, `ride.lyft.com` for Lyft, and the service's own site elsewhere. Web versions can lag the phone apps in ride types and features, so say so when an option the user expects is missing.
- Check memory for a preferred service, a preferred ride type, and which payment method the user uses for work versus personal trips.

## Flow

1. Dispatch a `computerUse` subagent to the service's web app with the pickup and destination and ask it to stop at the ride-options screen.
2. When the site wants a sign-in, work it in this order and stop at the first step that signs the browser in. If `request_cookie_origin_approval` is among your tools, call it with no origins to list the sites the user's Chrome holds, and request the site when the listing shows it; an approved import usually signs the box browser in with no handoff. Next, send `request_user_form` for the fields on the live page (reason "auth", the site's domain, one form per step); you never see what they type. Last, hand the box to the user with `request_box_help` and one instruction ("Sign in to your <service> account"); the handoff also covers a passkey, a 2FA prompt, or a form the host refused. A one-time code the site texts them is a one-field `request_user_form` with `submitAfterFill: true`. On a captcha or verify-you-are-human check, have the subagent try it first, then follow the same order. Never send a question widget before any of these; the tool is the ask. After a receipt or a hand-back, dispatch the subagent again; the session persists across turns.
3. Take a Screenshot of the ride options and attach the saved path. Read back each option's name, price, and pickup ETA.
4. If surge or peak pricing shows, say so explicitly with the multiplier or the price difference, and offer waiting as one of the options.
5. Send a question widget with the real options on the screen (ride type and price as the label). Let the user pick. Do not request the first option on your own.
6. Check the payment method on the request screen. Pay with a method already saved on the account; if several are saved, ask which one in the same widget or a follow-up before you request. If none is saved, hand the box to the user with `request_box_help` ("Add a payment method to your Uber account"). A one-time card does not fit a fare that can settle above the quoted price, so do not raise one here.
7. Dispatch the subagent to request the ride, or to schedule it with the confirmed date and time. Any payment confirmation the site asks for goes to the user through `request_box_help`.
8. After the match, read the driver's name, the car make, model, and color, the plate, the pickup ETA, and the pickup PIN when one is shown. Screenshot the match screen and attach it.
9. Send the confirmation message described under Confirming the ride. For a scheduled ride, report the scheduled window and say that the driver details arrive closer to pickup.
10. If the user asks to be reminded, create a routine with `update_state` (target "routine") for the pickup time.

## Presenting choices

- Show only the ride types the screen shows, with the price and ETA the screen shows. Never estimate a price the page did not display.
- Put the cheapest and the fastest first when they differ, and name what the extra cost buys (a larger car, a nicer car, a shorter wait).
- Surge is part of the choice. Show the surge price next to the option, not in a footnote.
- One widget for the ride type, and a second only when the payment method is also ambiguous. Fold both into one when the widget stays short.

## Confirming the ride

**Required.** The final confirmation message lists every detail you captured, verbatim and each on its own line: driver name, car make, model, and color, license plate, ETA, and the pickup PIN when the service shows one. "Your Lyft is booked, $19" is not enough; the user needs these details to find the car. If any of them has not appeared yet, say so and check again with a fresh Screenshot before the ETA runs out.

- Also state the pickup spot, the destination, the fare shown at request time, and the payment method charged.
- Attach the screenshot of the match screen with the message.
- Do not save the ride itself as a memory fact. Save a service or payment preference with `update_state` (target "memory") only when the user stated it.

## Pitfalls

- Surge changes between the screenshot and the request. Note the price you saw, and if the request screen shows a higher one, ask again before requesting.
- Web apps lag phone apps. Some ride types, scheduling windows, and promotions appear only in the app. Say what is missing rather than pretending it is not offered.
- Airport pickups have designated zones and terminals. If the app shows a pickup zone, put it in the confirmation message.
- Scheduled versus immediate is the most common misread. "First thing tomorrow" is never an immediate request.
- Several saved payment methods mean a real choice, and a business profile changes who pays.
- Never fabricate driver details, ETAs, or PINs. If the page did not show them, say so.
