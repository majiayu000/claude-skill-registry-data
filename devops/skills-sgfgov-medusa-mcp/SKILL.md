---
name: medusa-mcp
description: Dynamic access to medusa-mcp MCP server (299 tools)
version: 1.0.0
---

# medusa-mcp Skill

This skill provides dynamic access to the medusa-mcp MCP server without loading all tool definitions into context.

## Context Efficiency

Traditional MCP approach:
- All 299 tools loaded at startup
- Estimated context: 149500 tokens

This skill approach:
- Metadata only: ~100 tokens
- Full instructions (when used): ~5k tokens
- Tool execution: 0 tokens (runs externally)

## How This Works

Instead of loading all MCP tool definitions upfront, this skill:
1. Tells you what tools are available (just names and brief descriptions)
2. You decide which tool to call based on the user's request
3. Generate a JSON command to invoke the tool
4. The executor handles the actual MCP communication

## Available Tools

- `PostActor_typeAuth_provider`: Authenticate a customer and receive the JWT token to be used in the header of subsequent requests.

When used with a third-party provider, such as Google, the request returns a `location` property. You redirect to the specified URL in your storefront to continue authentication with the third-party service.

- `PostActor_typeAuth_providerCallback`: This API route is used by your storefront or frontend application when a third-party provider redirects to it after authentication. It validates the authentication with the third-party provider and, if successful, returns an authentication token. All query parameters received from the third-party provider, such as `code`, `state`, and `error`, must be passed as query parameters to this route.
You can decode the JWT token using libraries like [react-jwt](https://www.npmjs.com/package/react-jwt) in the storefront. If the decoded data doesn't  have an `actor_id` property, then you must register the customer using the Create Customer API route passing the token in the request's Authorization header.

- `PostActor_typeAuth_provider_register`: This API route retrieves a registration JWT token of a customer that hasn't been registered yet. The token is used in the header of requests that create a customer.
- `PostActor_typeAuth_providerResetPassword`: Generate a reset password token for a customer. This API route doesn't reset the customer password or send them the reset instructions in a notification.

Instead, This API route emits the `auth.password_reset` event, passing it the token as a payload. You can listen to that event in a subscriber as explained in [this guide](https://docs.medusajs.com/resources/commerce-modules/auth/reset-password), then send the customer a notification. The notification is sent using a [Notification Module Provider](https://docs.medusajs.com/resources/infrastructure-modules/notification), and it should have a URL that accepts a `token` query parameter, allowing the customer to reset their password from the storefront.


 Use the generated token to update the customer's password using the [Reset Password API route](https://docs.medusajs.com/api/store#auth_postactor_typeauth_providerupdate).

- `PostActor_typeAuth_providerUpdate`: Reset a customer's password using a reset-password token generated with the [Generate Reset Password Token API route](https://docs.medusajs.com/api/store#auth_postactor_typeauth_providerresetpassword). You pass the token as a bearer token in the request's Authorization header.
- `PostSession`: Set the cookie session ID of a customer. The customer must be previously authenticated with the `/auth/customer/{provider}` API route first, as the JWT token is required in the header of the request.
- `PostAdminAuthTokenRefresh`: Refresh the authentication token of a customer. This is useful after authenticating a customer with a third-party service to ensure the token holds the new user's details, or when you don't want customers to re-login every day.
- `PostCarts`: Create a cart.
- `GetCartsId`: Retrieve a cart by its ID. You can expand the cart's relations or select the fields that should be returned.
- `PostCartsIdComplete`: Complete a cart and place an order.
- `PostCartsIdCustomer`: Change the cart's customer to the currently logged-in customer. This is useful when you create the cart for a guest customer, then they log in with their account.
- `PostCartsIdGiftCards`: Add a Gift Card to a cart
- `PostCartsIdLineItems`: Add a product variant as a line item in the cart.
- `PostCartsIdLineItemsLine_id`: Update a line item's details in the cart.
- `PostCartsIdPromotions`: Add a list of promotions to a cart.
- `PostCartsIdShippingMethods`: Add a shipping method to a cart. Use this API route when the customer chooses their preferred shipping option.
- `PostCartsIdStoreCredits`: Add a Store Credit to a cart
- `PostCartsIdTaxes`: Calculate the cart's tax lines and amounts.
- `GetCollections`: Retrieve a list of collections. The collections can be filtered by fields such as `handle`. The collections can also be sorted or paginated.
- `GetCollectionsId`: Retrieve a collection by its ID. You can expand the collection's relations or select the fields that should be returned.
- `GetCurrencies`: Retrieve a list of currencies. The currencies can be filtered by fields such as `code`. The currencies can also be sorted or paginated.
- `GetCurrenciesCode`: Retrieve a currency by its code. You can expand the currency's relations or select the fields that should be returned.
- `PostCustomers`: Register a customer. Use the `/auth/customer/emailpass/register` API route first to retrieve the registration token and pass it in the header of the request.
- `GetCustomersMe`: Retrieve the logged-in customer. You can expand the customer's relations or select the fields that should be returned.
- `GetCustomersMeAddresses`: Retrieve the addresses of the logged-in customer. The addresses can be filtered by fields such as `country_code`. The addresses can also be sorted or paginated.
- `GetCustomersMeAddressesAddress_id`: Retrieve an address of the logged-in customer. You can expand the address's relations or select the fields that should be returned.
- `GetGiftCardsIdorcode`: Retrieve a gift card by its ID or code. You can expand the gift card's relations or select the fields that should be returned.
- `GetLocales`: Retrieve the list of supported locales. You can use this list to allow customers to select their preferred locale in your storefront.
- `GetOrders`: Retrieve the orders of the logged-in customer. The orders can be filtered by fields such as `id`. The orders can also be sorted or paginated.
- `GetOrdersId`: Retrieve an order by its ID. You can expand the order's relations or select the fields that should be returned.
- `PostOrdersIdTransferAccept`: Accept an order to be transfered to a customer's account, which was specified when the transfer request was created. The transfer is requested previously either by the customer using the [Request Order Transfer Store API route](https://docs.medusajs.com/api/store#orders_postordersidtransferrequest), or by the admin using the [Request Order Transfer Admin API route](https://docs.medusajs.com/api/admin#orders_postordersidtransferrequest).
- `PostOrdersIdTransferCancel`: Cancel an order transfer that the logged-in customer previously requested using the [Request Order Transfer](https://docs.medusajs.com/api/store#orders_postordersidtransferrequest) API route.
- `PostOrdersIdTransferDecline`: Decline an order transfer previously requested, typically by the admin user using the [Request Order Transfer Admin API route](https://docs.medusajs.com/api/admin#orders_postordersidtransferrequest).
- `PostOrdersIdTransferRequest`: Request an order to be transfered to the logged-in customer's account. The transfer is confirmed using the [Accept Order Transfer](https://docs.medusajs.com/api/store#orders_postordersidtransferaccept) API route.
- `PostPaymentCollections`: Create a payment collection for a cart. This is used during checkout, where the payment collection holds the cart's payment sessions.
- `PostPaymentCollectionsIdPaymentSessions`: Initialize and add a payment session to a payment collection. This is used during checkout, where you create a payment collection for the cart, then initialize a payment session for the payment provider that the customer chooses.
It's highly recommended to have an amount greater than `0` in the payment collection, as some payment providers, such as Stripe, require a non-zero amount to create a payment session. Otherwise, an error will be thrown on the payment provider's side.
In cases where you want to create a payment session for a payment collection with an amount of `0`, you can use the Manual System Payment Provider instead of third-party payment providers. The Manual System Payment Provider is built into Medusa and allows you to create payment sessions without interacting with an external payment provider.
Make sure to configure the Manual System Payment Provider in your store's region. Learn more in the [Manage Region](https://docs.medusajs.com/user-guide/settings/regions#edit-region-details) user guide.

- `GetPaymentProviders`: Retrieve a list of payment providers. You must provide the `region_id` query parameter to retrieve the payment providers enabled in that region.
- `GetProductCategories`: Retrieve a list of product categories. The product categories can be filtered by fields such as `id`. The product categories can also be sorted or paginated.
- `GetProductCategoriesId`: Retrieve a product category by its ID. You can expand the product category's relations or select the fields that should be returned.
- `GetProductTags`: Retrieve a list of product tags. The product tags can be filtered by fields such as `id`. The product tags can also be sorted or paginated.
- `GetProductTagsId`: Retrieve a product tag by its ID. You can expand the product tag's relations or select the fields that should be returned.
- `GetProductTypes`: Retrieve a list of product types. The product types can be filtered by fields such as `id`. The product types can also be sorted or paginated.
- `GetProductTypesId`: Retrieve a product type by its ID. You can expand the product type's relations or select the fields that should be returned.
- `GetProducts`: Retrieve a list of products. The products can be filtered by fields such as `id`. The products can also be sorted or paginated.

You can retrieve the content of the products translated to a specific locale either by passing the `locale` query parameter or by setting the `x-medusa-locale` header to the desired locale code in BCP 47 format. If you don't pass a locale, and your store has a default locale, the default locale will be used.

With localization, the products' content like title and description will be in the specified locale if a translation is available,  and fallback to the original content otherwise. Learn more in the [Localization](#localization) section.

- `GetProductsId`: Retrieve a product by its ID. You can expand the product's relations or select the fields that should be returned.

You can retrieve the content of the product translated to a specific locale either by passing the `locale` query parameter or by setting the `x-medusa-locale` header to the desired locale code in BCP 47 format. If you don't pass a locale, and your store has a default locale, the default locale will be used.

With localization, the product's content like title and description will be in the specified locale if a translation is available,  and fallback to the original content otherwise. Learn more in the [Localization](#localization) section.

- `GetRegions`: Retrieve a list of regions. The regions can be filtered by fields such as `id`. The regions can also be sorted or paginated.
- `GetRegionsId`: Retrieve a region by its ID. You can expand the region's relations or select the fields that should be returned.
- `GetReturnReasons`: Retrieve a list of return reasons. The return reasons can be sorted or paginated.
- `GetReturnReasonsId`: Retrieve a return reason by its ID. You can expand the return reason's relations or select the fields that should be returned.
- `PostReturns`: Create a return for an order's items. The admin receives the return and process it from their side.
- `GetShippingOptions`: Retrieve a list of shipping options for a cart. The cart's ID is set in the required `cart_id` query parameter.

The shipping options also be sorted or paginated.

- `PostShippingOptionsIdCalculate`: Calculate the price of a shipping option in a cart.
- `GetStoreCreditAccounts`: Retrieve the logged-in customer's store credit accounts. The store credit accounts can be filtered by fields such as `id`. The store credit accounts can also be sorted or paginated.
- `GetStoreCreditAccountsId`: Retrieve logged-in customer's store credit account by its ID. You can expand the store credit account's relations or select the fields that should be returned.
- `AdminGetApiKeys`: This tool helps store administors. Retrieve a list of API keys. The API keys can be filtered by fields such as `id`. The API keys can also be sorted or paginated.
- `AdminGetApiKeysId`: This tool helps store administors. Retrieve an API key by its ID. You can expand the API key's relations or select the fields that should be returned using the query parameters.
- `AdminPostApiKeysIdRevoke`: This tool helps store administors. Revokes an API key. If the API key is a secret, it can't be used for authentication anymore. If it's publishable, it can't be used by client applications.

- `AdminPostApiKeysIdSalesChannels`: This tool helps store administors. Manage the sales channels of a publishable API key, either to associate them or remove them from the API key.
- `AdminGetCampaigns`: This tool helps store administors. Retrieve a list of campaigns. The campaigns can be filtered by fields such as `id`. The campaigns can also be sorted or paginated.
- `AdminGetCampaignsId`: This tool helps store administors. Retrieve a campaign by its ID. You can expand the campaign's relations or select the fields that should be returned using the query parameters.
- `AdminPostCampaignsIdPromotions`: This tool helps store administors. Manage the promotions of a campaign, either by adding them or removing them from the campaign.
- `AdminGetClaims`: This tool helps store administors. Retrieve a list of claims. The claims can be filtered by fields such as `id`. The claims can also be sorted or paginated.
- `AdminGetClaimsId`: This tool helps store administors. Retrieve a claim by its ID. You can expand the claim's relations or select the fields that should be returned using the query parameters.
- `AdminPostClaimsIdCancel`: This tool helps store administors. Cancel a claim and its associated return.
- `AdminPostClaimsIdClaimItems`: This tool helps store administors. Add order items to a claim as claim items. These claim items will have the action `WRITE_OFF_ITEM`.
- `AdminPostClaimsIdClaimItemsAction_id`: This tool helps store administors. Update an order item in a claim by the ID of the item's `WRITE_OFF_ITEM` action.

Every item has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminPostClaimsIdInboundItems`: This tool helps store administors. Add inbound (or return) items to a claim. These inbound items will have a `RETURN_ITEM` action.

- `AdminPostClaimsIdInboundItemsAction_id`: This tool helps store administors. Update an inbound (or return) item of a claim using the `ID` of the item's `RETURN_ITEM` action.

Every item has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminPostClaimsIdInboundShippingMethod`: This tool helps store administors. Add an inbound (or return) shipping method to a claim. The inbound shipping method will have a `SHIPPING_ADD` action.

- `AdminPostClaimsIdInboundShippingMethodAction_id`: This tool helps store administors. Update the shipping method for returning items in the claim using the `ID` of the method's `SHIPPING_ADD` action.

Every shipping method has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminPostClaimsIdOutboundItems`: This tool helps store administors. Add outbound (or new) items to a claim. These outbound items will have an `ITEM_ADD` action.

- `AdminPostClaimsIdOutboundItemsAction_id`: This tool helps store administors. Update an outbound (or new) item of a claim using the `ID` of the item's `ITEM_ADD` action.

Every item has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminPostClaimsIdOutboundShippingMethod`: This tool helps store administors. Add an outbound shipping method to a claim. The outbound shipping method will have a `SHIPPING_ADD` action.

- `AdminPostClaimsIdOutboundShippingMethodAction_id`: This tool helps store administors. Update the shipping method for delivering outbound items in a claim using the `ID` of the method's `SHIPPING_ADD` action.

Every shipping method has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminPostClaimsIdRequest`: This tool helps store administors. Confirm a claim request, applying its changes on the associated order.
- `AdminGetCollections`: This tool helps store administors. Retrieve a list of collections. The collections can be filtered by fields such as `id`. The collections can also be sorted or paginated.
- `AdminGetCollectionsId`: This tool helps store administors. Retrieve a collection by its ID. You can expand the collection's relations or select the fields that should be returned using the query parameters.
- `AdminPostCollectionsIdProducts`: This tool helps store administors. Manage the products of a collection by adding or removing them from the collection.
- `AdminGetCurrencies`: This tool helps store administors. Retrieve a list of currencies. The currencies can be filtered by fields such as `id`. The currencies can also be sorted or paginated.
- `AdminGetCurrenciesCode`: This tool helps store administors. Retrieve a currency by its code. You can expand the currency's relations or select the fields that should be returned using the query parameters.
- `AdminGetCustomerGroups`: This tool helps store administors. Retrieve a list of customer groups. The customer groups can be filtered by fields such as `id`. The customer groups can also be sorted or paginated.
- `AdminGetCustomerGroupsId`: This tool helps store administors. Retrieve a customer group by its ID. You can expand the customer group's relations or select the fields that should be returned.
- `AdminPostCustomerGroupsIdCustomers`: This tool helps store administors. Manage the customers of a group to add or remove them from the group.
- `AdminGetCustomers`: This tool helps store administors. Retrieve a list of customers. The customers can be filtered by fields such as `id`. The customers can also be sorted or paginated.
- `AdminGetCustomersId`: This tool helps store administors. Retrieve a customer by its ID. You can expand the customer's relations or select the fields that should be returned.
- `AdminGetCustomersIdAddresses`: This tool helps store administors. Retrieve a list of addresses in a customer. The addresses can be filtered by fields like `query`. The addresses can also be paginated.
- `AdminGetCustomersIdAddressesAddress_id`: This tool helps store administors. Retrieve a list of a customer's addresses. The addresses can be filtered by fields like `company`. The addresses can also be paginated.
- `AdminPostCustomersIdCustomerGroups`: This tool helps store administors. Manage the customer groups of a customer, adding or removing the customer from those groups.
- `AdminGetDraftOrders`: This tool helps store administors. Retrieve a list of draft orders. The draft orders can be filtered by fields such as `id`. The draft orders can also be sorted or paginated.
- `AdminGetDraftOrdersId`: This tool helps store administors. Retrieve a draft order by its ID. You can expand the draft order's relations or select the fields that should be returned using the query parameters.
- `AdminPostDraftOrdersIdConvertToOrder`: This tool helps store administors. Convert a draft order to an order. This will finalize the draft order and create a new order with the same details.
- `AdminPostDraftOrdersIdEdit`: This tool helps store administors. Create an edit on a draft order. This will allow you to make changes to the draft order's items, shipping methods, or promotions. Once you've made the necessar changes, you can later either request the edit (which requires a confirmation from the customer), or force-confirm the edit.
- `AdminPostDraftOrdersIdEditConfirm`: This tool helps store administors. Confirm an edit on a draft order. This will apply the changes made to the draft order.
- `AdminPostDraftOrdersIdEditItems`: This tool helps store administors. Add an item to a draft order edit.
- `AdminPostDraftOrdersIdEditItemsItemItem_id`: This tool helps store administors. Update an existing item in a draft order edit.
- `AdminPostDraftOrdersIdEditItemsAction_id`: This tool helps store administors. Update a new item that was added to a draft order edit by the ID of the item's `ITEM_ADD` action.

Every item has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminPostDraftOrdersIdEditPromotions`: This tool helps store administors. Add promotions to a draft order edit.
- `AdminPostDraftOrdersIdEditRequest`: This tool helps store administors. Change the status of a draft order's edit to be requested. Later, the edit can be confirmed or canceled.
- `AdminPostDraftOrdersIdEditShippingMethods`: This tool helps store administors. Add a shipping method to a draft order edit.
- `AdminPostDraftOrdersIdEditShippingMethodsMethodMethod_id`: This tool helps store administors. Update an existing shipping method in a draft order edit.
- `AdminPostDraftOrdersIdEditShippingMethodsAction_id`: This tool helps store administors. Update a new shipping method that was added to a draft order edit using the `ID` of the method's `SHIPPING_ADD` action.

Every shipping method has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminGetExchanges`: This tool helps store administors. Retrieve a list of exchanges. The exchanges can be filtered by fields such as `id`. The exchanges can also be sorted or paginated.
- `AdminGetExchangesId`: This tool helps store administors. Retrieve an exchange by its ID. You can expand the exchange's relations or select the fields that should be returned using query parameters.
- `AdminPostExchangesIdCancel`: This tool helps store administors. Cancel an exchange and its associated return.
- `AdminPostExchangesIdInboundItems`: This tool helps store administors. Add inbound (or return) items to an exchange. These inbound items will have the action `RETURN_ITEM`.
- `AdminPostExchangesIdInboundItemsAction_id`: This tool helps store administors. Update an inbound (or return) item from an exchange using the `ID` of the item's `RETURN_ITEM` action.

Every item has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminPostExchangesIdInboundShippingMethod`: This tool helps store administors. Add an inbound (or return) shipping method to an exchange. The inbound shipping method will have a `SHIPPING_ADD` action.
- `AdminPostExchangesIdInboundShippingMethodAction_id`: This tool helps store administors. Update the shipping method for returning items in the exchange using the `ID` of the method's `SHIPPING_ADD` action.

Every shipping method has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminPostExchangesIdOutboundItems`: This tool helps store administors. Add outbound (or new) items to an exchange. These outbound items will have the action `ITEM_ADD`.
- `AdminPostExchangesIdOutboundItemsAction_id`: This tool helps store administors. Update an outbound (or new) item from an exchange using the `ID` of the item's `ITEM_ADD` action.

Every item has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminPostExchangesIdOutboundShippingMethod`: This tool helps store administors. Add an outbound shipping method to an exchange. The outbound shipping method will have a `SHIPPING_ADD` action.
- `AdminPostExchangesIdOutboundShippingMethodAction_id`: This tool helps store administors. Update the shipping method for delivering outbound items in the exchange using the `ID` of the method's `SHIPPING_ADD` action.

Every shipping method has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminPostExchangesIdRequest`: This tool helps store administors. Confirm an exchange request, applying its changes on the associated order.
- `AdminGetFeatureFlags`: This tool helps store administors. Retrieve a list of feature flags. The feature flags can be filtered by fields such as `id`. The feature flags can also be sorted or paginated.
- `AdminGetFulfillmentProviders`: This tool helps store administors. Retrieve a list of fulfillment providers. The fulfillment providers can be filtered by fields such as `id`. The fulfillment providers can also be sorted or paginated.
- `AdminGetFulfillmentProvidersIdOptions`: This tool helps store administors. Retrieve the list of fulfillment options of a fulfillment provider. These options may be retrieved from an integrated third-party service.
- `AdminDeleteFulfillmentSetsId`: This tool helps store administors. Delete a fulfillment set.
- `AdminPostFulfillmentSetsIdServiceZones`: This tool helps store administors. Add a service zone to a fulfillment set.
- `AdminGetFulfillmentSetsIdServiceZonesZone_id`: This tool helps store administors. Retrieve a service zone that belongs to a fulfillment set. be paginated.
- `AdminPostFulfillments`: This tool helps store administors. Create a fulfillment for an order, return, exchange, and more.
- `AdminPostFulfillmentsIdCancel`: This tool helps store administors. Cancel a fulfillment. The fulfillment can't be shipped or delivered.

To cancel the fulfillment, the `cancelFulfillment` method of the associated fulfillment provider is used.

- `AdminPostFulfillmentsIdShipment`: This tool helps store administors. Create a shipment for a fulfillment. The fulfillment must not be shipped or canceled.
- `AdminGetGiftCards`: This tool helps store administors. Retrieve a list of gift cards. The gift cards can be filtered by fields such as `id`. The gift cards can also be sorted or paginated.
- `AdminGetGiftCardsId`: This tool helps store administors. Retrieve a gift card by its ID. You can expand the gift card's relations or select the fields that should be returned.
- `AdminGetGiftCardsIdOrders`: This tool helps store administors. Retrieve the list of orders that a gift card was used in.
- `AdminGetIndexDetails`: This tool helps store administors. Retrieve index metadata, including entity type, status, last synced key, and last updated timestamp.
- `AdminPostIndexSync`: This tool helps store administors. Trigger reindexing or re-ingestion of the Index Module.
- `AdminGetInventoryItems`: This tool helps store administors. Retrieve a list of inventory items. The inventory items can be filtered by fields such as `id`. The inventory items can also be sorted or paginated.
- `AdminPostInventoryItemsLocationLevelsBatch`: This tool helps store administors. Manage inventory levels to create, update, or delete them.
- `AdminGetInventoryItemsId`: This tool helps store administors. Retrieve a inventory item by its ID. You can expand the inventory item's relations or select the fields that should be returned.
- `AdminGetInventoryItemsIdLocationLevels`: This tool helps store administors. Retrieve a list of inventory levels associated with an inventory item. The inventory levels can be filtered by fields like `location_id`. The inventory levels can also be paginated.
- `AdminPostInventoryItemsIdLocationLevelsBatch`: This tool helps store administors. Manage the inventory levels of an inventory item to create or delete them.
- `AdminPostInventoryItemsIdLocationLevelsLocation_id`: This tool helps store administors. Updates the details of an inventory item's inventory level using its associated location ID.
- `AdminGetInvites`: This tool helps store administors. Retrieve a list of invites. The invites can be filtered by fields such as `id`. The invites can also be sorted or paginated.
- `AdminPostInvitesAccept`: This tool helps store administors. Accept an invite and create a new user.
Since the user isn't created yet, the JWT token used in the authorization header is retrieved from the `/auth/user/emailpass/register` API route (or a provider other than `emailpass`). The user can then authenticate using the `/auth/user/emailpass` API route.

- `AdminGetInvitesId`: This tool helps store administors. Retrieve an invite by its ID. You can expand the invite's relations or select the fields that should be returned.
- `AdminPostInvitesIdResend`: This tool helps store administors. Refresh the token of an invite.
- `AdminGetLocales`: This tool helps store administors. Retrieve a list of locales. The locales can be filtered by fields such as `code`. The locales can also be sorted or paginated.
- `AdminGetLocalesCode`: This tool helps store administors. Retrieve a locale by its code. You can expand the locale's relations or select the fields that should be returned.
- `AdminGetNotifications`: This tool helps store administors. Retrieve a list of notifications. The notifications can be filtered by fields such as `id`. The notifications can also be sorted or paginated.
- `AdminGetNotificationsId`: This tool helps store administors. Retrieve a notification by its ID. You can expand the notification's relations or select the fields that should be returned.
- `AdminPostOrderChangesId`: This tool helps store administors. Update an order change's details. An order change can be an exchange, claim, or edit. For example, you can edit whether an exchange carries over the parent order's promotion.
- `AdminPostOrderEdits`: This tool helps store administors. Create an order edit.
- `AdminDeleteOrderEditsId`: This tool helps store administors. Cancel a requested order edit.
- `AdminPostOrderEditsIdConfirm`: This tool helps store administors. Confirm an order edit request and apply the changes on the order.
- `AdminPostOrderEditsIdItems`: This tool helps store administors. Add new items to an order edit. These items will have the action `ITEM_ADD`.
- `AdminPostOrderEditsIdItemsItemItem_id`: This tool helps store administors. Update an existing order item's quantity of an order edit.
You can also use this API route to remove an item from an order by setting its quantity to `0`.

- `AdminPostOrderEditsIdItemsAction_id`: This tool helps store administors. Update an added item in the order edit by the ID of the item's `ITEM_ADD` action.

Every item has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminPostOrderEditsIdRequest`: This tool helps store administors. Change the status of an active order edit to requested.
- `AdminPostOrderEditsIdShippingMethod`: This tool helps store administors. Add a shipping method to an exchange. The shipping method will have a `SHIPPING_ADD` action.
- `AdminPostOrderEditsIdShippingMethodAction_id`: This tool helps store administors. Update a shipping method in the order edit by the ID of the method's `SHIPPING_ADD` action.

Every shipping method has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminGetOrders`: This tool helps store administors. Retrieve a list of orders. The orders can be filtered by fields such as `id`. The orders can also be sorted or paginated.
- `AdminPostOrdersExport`: This tool helps store administors. Start an order export process to retrieve a CSV of exported orders.

You'll receive in the response the transaction ID of the workflow generating the CSV file. To check the status of the execution, send a GET request to `/admin/workflows-executions/export-orders/:transaction-id`.

Once the execution finishes successfully, a notification is created for the export. You can retrieve the notifications using the `/admin/notification` API route to retrieve the file's download URL.

- `AdminGetOrdersId`: This tool helps store administors. Retrieve an order by its ID. You can expand the order's relations or select the fields that should be returned.
- `AdminPostOrdersIdArchive`: This tool helps store administors. Change the status of an order to archived.
- `AdminPostOrdersIdCancel`: This tool helps store administors. Cancel an order. The cancelation fails if:
- The order has captured payments.


- The order has refund payments.


- The order has fulfillments that aren't canceled.

- `AdminGetOrdersIdChanges`: This tool helps store administors. Retrieve a list of changes made on an order, including returns, exchanges, etc...

The changes can be filtered by fields like `created_at`. The changes can also be paginated.

- `AdminPostOrdersIdComplete`: This tool helps store administors. Mark an order as completed.
- `AdminPostOrdersIdCreditLines`: This tool helps store administors. Create a credit line for an order.
- `AdminPostOrdersIdFulfillments`: This tool helps store administors. Create a fulfillment for an order. The creation fails if the order is canceled.
- `AdminPostOrdersIdFulfillmentsFulfillment_idCancel`: This tool helps store administors. Cancel an order's fulfillment. The fulfillment can't be canceled if it's shipped.
- `AdminPostOrdersIdFulfillmentsFulfillment_idMarkAsDelivered`: This tool helps store administors. Mark an order's fulfillment as delivered.
- `AdminPostOrdersIdFulfillmentsFulfillment_idShipments`: This tool helps store administors. Create a shipment for an order's fulfillment.
- `AdminGetOrdersIdLineItems`: This tool helps store administors. Retrieve a list of line items in a order. The line items can be filtered by fields like FILTER FIELDS. The line items can also be paginated.
- `AdminGetOrdersIdPreview`: This tool helps store administors. Retrieve a preview of an order using its associated change, such as an edit.
- `AdminGetOrdersIdShippingOptions`: This tool helps store administors. Retrieve a list of shipping options that can be used for outbound shipping in an order. This is especially useful when adding outbound shipping to order exchanges or claims.
- `AdminPostOrdersIdTransfer`: This tool helps store administors. Request an order to be transfered to another customer. The transfer is confirmed by sending a request to the [Accept Order Transfer](https://docs.medusajs.com/api/store#orders_postordersidtransferaccept) Store API route.
- `AdminPostOrdersIdTransferCancel`: This tool helps store administors. Cancel a request to transfer an order to another customer.
- `AdminPostPaymentCollections`: This tool helps store administors. Create a payment collection.
- `AdminDeletePaymentCollectionsId`: This tool helps store administors. Delete a payment collection.
- `AdminPostPaymentCollectionsIdMarkAsPaid`: This tool helps store administors. Mark a payment collection as paid. This creates and authorizes a payment session, then capture its payment, using the manual payment provider.
- `AdminGetPayments`: This tool helps store administors. Retrieve a list of payments. The payments can be filtered by fields such as `id`. The payments can also be sorted or paginated.
- `AdminGetPaymentsPaymentProviders`: This tool helps store administors. Retrieve a list of payment providers. The payment providers can be filtered by fields such as `id`. The payment providers can also be sorted or paginated.
- `AdminGetPaymentsId`: This tool helps store administors. Retrieve a payment by its ID. You can expand the payment's relations or select the fields that should be returned.
- `AdminPostPaymentsIdCapture`: This tool helps store administors. Capture an amount of a payment. This uses the `capturePayment` method of the payment provider associated with the payment's collection.
- `AdminPostPaymentsIdRefund`: This tool helps store administors. Refund an amount of a payment. This uses the `refundPayment` method of the payment provider associated with the payment's collection.
- `AdminGetPlugins`: This tool helps store administors. Retrieve the list of plugins installed in the Medusa application.
- `AdminGetPriceLists`: This tool helps store administors. Retrieve a list of price lists. The price lists can be filtered by fields such as `id`. The price lists can also be sorted or paginated.
- `AdminGetPriceListsId`: This tool helps store administors. Retrieve a price list by its ID. You can expand the price list's relations or select the fields that should be returned.
- `AdminGetPriceListsIdPrices`: This tool helps store administors. Retrieve a list of prices in a price list. The prices can also be paginated.
- `AdminPostPriceListsIdPricesBatch`: This tool helps store administors. Manage the prices of a price list to create, update, or delete them.
- `AdminPostPriceListsIdProducts`: This tool helps store administors. Remove products from a price list.
- `AdminGetPricePreferences`: This tool helps store administors. Retrieve a list of price preferences. The price preferences can be filtered by fields such as `id`. The price preferences can also be sorted or paginated.
- `AdminGetPricePreferencesId`: This tool helps store administors. Retrieve a price preference by its ID. You can expand the price preference's relations or select the fields that should be returned.
- `AdminGetProductCategories`: This tool helps store administors. Retrieve a list of product categories. The product categories can be filtered by fields such as `id`. The product categories can also be sorted or paginated.
- `AdminGetProductCategoriesId`: This tool helps store administors. Retrieve a product category by its ID. You can expand the product category's relations or select the fields that should be returned.
- `AdminPostProductCategoriesIdProducts`: This tool helps store administors. Manage products of a category to add or remove them.
- `AdminGetProductTags`: This tool helps store administors. Retrieve a list of product tags. The product tags can be filtered by fields such as `id`. The product tags can also be sorted or paginated.
- `AdminGetProductTagsId`: This tool helps store administors. Retrieve a product tag by its ID. You can expand the product tag's relations or select the fields that should be returned.
- `AdminGetProductTypes`: This tool helps store administors. Retrieve a list of product types. The product types can be filtered by fields such as `id`. The product types can also be sorted or paginated.
- `AdminGetProductTypesId`: This tool helps store administors. Retrieve a product type by its ID. You can expand the product type's relations or select the fields that should be returned.
- `AdminGetProductVariants`: This tool helps store administors. Retrieve a list of product variants. The product variants can be filtered by fields such as `id`. The product variants can also be sorted or paginated.
- `AdminGetProducts`: This tool helps store administors. Retrieve a list of products. The products can be filtered by fields such as `id`. The products can also be sorted or paginated.
- `AdminPostProductsBatch`: This tool helps store administors. Manage products to create, update, or delete them.
- `AdminPostProductsExport`: This tool helps store administors. Start a product export process to retrieve a CSV of exported products.

You'll receive in the response the transaction ID of the workflow generating the CSV file. To check the status of the execution, send a GET request to `/admin/workflows-executions/export-products/:transaction-id`.
Once the execution finishes successfully, a notification is created for the export. You can retrieve the notifications using the `/admin/notification` API route to retrieve the file's download URL.

- `AdminPostProductsImport`: This tool helps store administors. Create a new product import process. The products aren't imported until the import is confirmed with the `/admin/products/:transaction-id/import` API route.
- `AdminPostProductsImportTransaction_idConfirm`: This tool helps store administors. Confirm that a created product import should start importing the products into Medusa.
- `AdminPostProductsImports`: This tool helps store administors. Create a new product import process. The products aren't imported until the import is confirmed with the `/admin/products/:transaction-id/imports` API route.
- `AdminPostProductsImportsTransaction_idConfirm`: This tool helps store administors. Confirm that a created product import should start importing the products into Medusa.
- `AdminGetProductsId`: This tool helps store administors. Retrieve a product by its ID. You can expand the product's relations or select the fields that should be returned.
- `AdminPostProductsIdImagesImage_idVariantsBatch`: This tool helps store administors. Manage the association between product variants and a product image. You can add or remove associations between variants and the image.
- `AdminGetProductsIdOptions`: This tool helps store administors. Retrieve a list of options of a product. The options can be filtered by fields like `id`. The options can also be paginated.
- `AdminGetProductsIdOptionsOption_id`: This tool helps store administors. Retrieve a product's option by its ID.
- `AdminGetProductsIdVariants`: This tool helps store administors. Retrieve a list of variants in a product. The variants can be filtered by fields like FILTER FIELDS. The variants can also be paginated.
- `AdminPostProductsIdVariantsBatch`: This tool helps store administors. Manage variants in a product to create, update, or delete them.
- `AdminPostProductsIdVariantsInventoryItemsBatch`: This tool helps store administors. Manage a product's variant's inventoris to associate them with inventory items, update their inventory items, or delete their association with inventory items.
- `AdminGetProductsIdVariantsVariant_id`: This tool helps store administors. Retrieve a product's variant by its ID.
- `AdminPostProductsIdVariantsVariant_idImagesBatch`: This tool helps store administors. Manage the association between product images and a product variant. You can add or remove associations between images and the variant.
- `AdminPostProductsIdVariantsVariant_idInventoryItems`: This tool helps store administors. Associate with a product variant an inventory item that manages its inventory details.
- `AdminPostProductsIdVariantsVariant_idInventoryItemsInventory_item_id`: This tool helps store administors. Update the inventory item that manages the inventory details of a product variant.
- `AdminGetPromotions`: This tool helps store administors. Retrieve a list of promotions. The promotions can be filtered by fields such as `id`. The promotions can also be sorted or paginated.
- `AdminGetPromotionsRuleAttributeOptionsRule_type`: This tool helps store administors. Retrieve a list of potential rule attributes for the promotion and application method types specified in the query parameters.
Only the attributes of the rule type specified in the path parameter are retrieved:
- If `rule_type` is `rules`, the attributes of the promotion's type are retrieved.

- If `rule_type` is `target-rules`, the target rules' attributes of the application method's type are retrieved.

- If `rule_type` is `buy-rules`, the buy rules' attributes of the application method's type are retrieved.

- `AdminGetPromotionsRuleValueOptionsRule_typeRule_attribute_id`: This tool helps store administors. Retrieve all potential values for promotion rules and target and buy rules based on the specified rule attribute and type.
For example, if you provide the ID of the `currency_code` rule attribute, and set `rule_type` to `rules`, a list of currencies are retrieved in label-value pairs.

- `AdminGetPromotionsId`: This tool helps store administors. Retrieve a promotion by its ID. You can expand the promotion's relations or select the fields that should be returned.
- `AdminPostPromotionsIdBuyRulesBatch`: This tool helps store administors. Manage the buy rules of a `buyget` promotion to create, update, or delete them.
- `AdminPostPromotionsIdRulesBatch`: This tool helps store administors. Manage the rules of a promotion to create, update, or delete them.
- `AdminPostPromotionsIdTargetRulesBatch`: This tool helps store administors. Manage the target rules of a promotion to create, update, or delete them.
- `AdminGetPromotionsIdRule_type`: This tool helps store administors. Retrieve a list of rules in a promotion. The type of rules retrieved depend on the value of the `rule_type` path parameter:
- If `rule_type` is `rules`, the promotion's rules are retrivied. - If `rule_type` is `target-rules`, the target rules of the promotion's application method are retrieved.

- If `rule_type` is `buy-rules`, the buy rules of the promotion's application method are retrieved.

- `AdminGetRefundReasons`: This tool helps store administors. Retrieve a list of refund reasons. The refund reasons can be filtered by fields such as `id`. The refund reasons can also be sorted or paginated.
- `AdminGetRefundReasonsId`: This tool helps store administors. Retrieve a refund reason by its ID. You can expand the refund reason's relations or select the fields that should be returned.
- `AdminGetRegions`: This tool helps store administors. Retrieve a list of regions. The regions can be filtered by fields such as `id`. The regions can also be sorted or paginated.
- `AdminGetRegionsId`: This tool helps store administors. Retrieve a region by its ID. You can expand the region's relations or select the fields that should be returned.
- `AdminGetReservations`: This tool helps store administors. Retrieve a list of reservations. The reservations can be filtered by fields such as `id`. The reservations can also be sorted or paginated.
- `AdminGetReservationsId`: This tool helps store administors. Retrieve a reservation by its ID. You can expand the reservation's relations or select the fields that should be returned.
- `AdminGetReturnReasons`: This tool helps store administors. Retrieve a list of return reasons. The return reasons can be filtered by fields such as `id`. The return reasons can also be sorted or paginated.
- `AdminGetReturnReasonsId`: This tool helps store administors. Retrieve a return reason by its ID. You can expand the return reason's relations or select the fields that should be returned.
- `AdminGetReturns`: This tool helps store administors. Retrieve a list of returns. The returns can be filtered by fields such as `id`. The returns can also be sorted or paginated.
- `AdminGetReturnsId`: This tool helps store administors. Retrieve a return by its ID. You can expand the return's relations or select the fields that should be returned.
- `AdminPostReturnsIdCancel`: This tool helps store administors. Cancel a return.
- `AdminPostReturnsIdDismissItems`: This tool helps store administors. Add damaged items, whose quantity is to be dismissed, to a return. These items will have the action `RECEIVE_DAMAGED_RETURN_ITEM`.
- `AdminPostReturnsIdDismissItemsAction_id`: This tool helps store administors. Update a damaged item, whose quantity is to be dismissed, in the return by the ID of the  item's `RECEIVE_DAMAGED_RETURN_ITEM` action.

Every item has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property. return.

- `AdminPostReturnsIdReceive`: This tool helps store administors. Start a return receival process to be later confirmed using the `/admin/returns/:id/receive/confirm` API route.
- `AdminPostReturnsIdReceiveItems`: This tool helps store administors. Add received items in a return. These items will have the action `RECEIVE_RETURN_ITEM`.
- `AdminPostReturnsIdReceiveItemsAction_id`: This tool helps store administors. Update a received item in the return by the ID of the  item's `RECEIVE_RETURN_ITEM` action.

Every item has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property. return.

- `AdminPostReturnsIdReceiveConfirm`: This tool helps store administors. Confirm that a return has been received. This updates the quantity of the items received, if not damaged, and  reflects the changes on the order.

- `AdminPostReturnsIdRequest`: This tool helps store administors. Confirm a requested return. The changes are applied on the inventory quantity and the order only after the return has been confirmed as received using the `/admin/returns/:id/received/confirm`.

- `AdminPostReturnsIdRequestItems`: This tool helps store administors. Add items that are requested to be returned. These items will have the action `RETURN_ITEM`.
- `AdminPostReturnsIdRequestItemsAction_id`: This tool helps store administors. Update a requested item to be returned by the ID of the  item's `RETURN_ITEM` action.

Every item has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property. return.

- `AdminPostReturnsIdShippingMethod`: This tool helps store administors. Add a shipping method to a return. The shipping method will have a `SHIPPING_ADD` action.
- `AdminPostReturnsIdShippingMethodAction_id`: This tool helps store administors. Update a shipping method of the return by the ID of the item's `SHIPPING_ADD` action.

Every item has an `actions` property, whose value is an array of actions. You can check the action's name using its `action` property, and use the value of the `id` property.

- `AdminGetSalesChannels`: This tool helps store administors. Retrieve a list of sales channels. The sales channels can be filtered by fields such as `id`. The sales channels can also be sorted or paginated.
- `AdminGetSalesChannelsId`: This tool helps store administors. Retrieve a sales channel by its ID. You can expand the sales channel's relations or select the fields that should be returned.
- `AdminPostSalesChannelsIdProducts`: This tool helps store administors. Manage products in a sales channel to add or remove them from the channel.
- `AdminGetShippingOptionTypes`: This tool helps store administors. Retrieve a list of shipping option types. The shipping option types can be filtered by fields such as `id`. The shipping option types can also be sorted or paginated.
- `AdminGetShippingOptionTypesId`: This tool helps store administors. Retrieve a shipping option type by its ID. You can expand the shipping option type's relations or select the fields that should be returned.
- `AdminGetShippingOptions`: This tool helps store administors. Retrieve a list of shipping options. The shipping options can be filtered by fields such as `id`. The shipping options can also be sorted or paginated.
- `AdminGetShippingOptionsId`: This tool helps store administors. Retrieve a shipping option by its ID. You can expand the shipping option's relations or select the fields that should be returned.
- `AdminPostShippingOptionsIdRulesBatch`: This tool helps store administors. Manage the rules of a shipping option to create, update, or delete them.
- `AdminGetShippingProfiles`: This tool helps store administors. Retrieve a list of shipping profiles. The shipping profiles can be filtered by fields such as `id`. The shipping profiles can also be sorted or paginated.
- `AdminGetShippingProfilesId`: This tool helps store administors. Retrieve a shipping profile by its ID. You can expand the shipping profile's relations or select the fields that should be returned.
- `AdminGetStockLocations`: This tool helps store administors. Retrieve a list of stock locations. The stock locations can be filtered by fields such as `id`. The stock locations can also be sorted or paginated.
- `AdminGetStockLocationsId`: This tool helps store administors. Retrieve a stock location by its ID. You can expand the stock location's relations or select the fields that should be returned.
- `AdminPostStockLocationsIdFulfillmentProviders`: This tool helps store administors. Manage the fulfillment providers to add or remove them from a stock location.
- `AdminPostStockLocationsIdFulfillmentSets`: This tool helps store administors. Create and add a fulfillment set to a stock location.
- `AdminPostStockLocationsIdSalesChannels`: This tool helps store administors. Manage the sales channels in a stock location by adding or removing them.
- `AdminGetStoreCreditAccounts`: This tool helps store administors. Retrieve a list of store credit accounts. The store credit accounts can be filtered by fields such as `id`. The store credit accounts can also be sorted or paginated.
- `AdminGetStoreCreditAccountsId`: This tool helps store administors. Retrieve a store credit account by its ID. You can expand the store credit account's relations or select the fields that should be returned.
- `AdminGetStoreCreditAccountsIdTransactions`: This tool helps store administors. Retrieve a list of transactions in a store credit account. The transactions can be filtered by fields like FILTER FIELDS. The transactions can also be paginated.
- `AdminGetStores`: This tool helps store administors. Retrieve a list of stores. The stores can be filtered by fields such as `id`. The stores can also be sorted or paginated.
- `AdminGetStoresId`: This tool helps store administors. Retrieve a store by its ID. You can expand the store's relations or select the fields that should be returned.
- `AdminGetTaxProviders`: This tool helps store administors. Retrieve a list of tax providers installed in the Medusa application through Tax Module Providers. The tax providers can be filtered by fields such as `id`. The tax providers can also be sorted or paginated.
- `AdminGetTaxRates`: This tool helps store administors. Retrieve a list of tax rates. The tax rates can be filtered by fields such as `id`. The tax rates can also be sorted or paginated.
- `AdminGetTaxRatesId`: This tool helps store administors. Retrieve a tax rate by its ID. You can expand the tax rate's relations or select the fields that should be returned.
- `AdminPostTaxRatesIdRules`: This tool helps store administors. Create a tax rule for a rate.
- `AdminDeleteTaxRatesIdRulesRule_id`: This tool helps store administors. Remove a tax rate's rule.
- `AdminGetTaxRegions`: This tool helps store administors. Retrieve a list of tax regions. The tax regions can be filtered by fields such as `id`. The tax regions can also be sorted or paginated.
- `AdminGetTaxRegionsId`: This tool helps store administors. Retrieve a tax region by its ID. You can expand the tax region's relations or select the fields that should be returned.
- `AdminGetTranslations`: This tool helps store administors. Retrieve a list of translations. The translations can be filtered by fields such as `reference_id` (For example, the ID of a product). The translations can also be sorted or paginated.
- `AdminPostTranslationsBatch`: This tool helps store administors. Manage translations in bulk by creating, updating, or deleting multiple translations in a single request. You can manage translations for various resources such as products, product variants, categories, and more.
- `AdminGetTranslationsEntities`: This tool helps store administors. Retrieve a list of translatable entities. The entities can be filtered by fields such as `id`. The entities can also be sorted or paginated.
- `AdminGetTranslationsSettings`: This tool helps store administors. Retrieve the list of translatable fields for all entities, such as products and collections. You can also filter the results by entity type or active entities.
- `AdminPostTranslationsSettingsBatch`: This tool helps store administors. Create, update, or delete multiple translation settings.
- `AdminGetTranslationsStatistics`: This tool helps store administors. Get statistics on translations for specified locales and entity types. This includes overall translation progress for each entity type, and statistics for each locale within those entity types.
- `AdminPostUploads`: This tool helps store administors. Upload files to the configured File Module Provider.
- `AdminPostUploadsPresignedUrls`: This tool helps store administors. Get a presigned URL for uploading a file to the configured File Module Provider. The presigned URL can be used to upload files directly to the third-party provider. This only works if your configured provider supports presigned URLs, such as the S3 provider.
- `AdminGetUploadsId`: This tool helps store administors. Retrieve an uploaded file by its ID. You can expand the file's relations or select the fields that should be returned.
- `AdminGetUsers`: This tool helps store administors. Retrieve a list of users. The users can be filtered by fields such as `id`. The users can also be sorted or paginated.
- `AdminGetUsersMe`: This tool helps store administors. Retrieve the logged-in user's details.
- `AdminGetUsersId`: This tool helps store administors. Retrieve a user by its ID. You can expand the user's relations or select the fields that should be returned.
- `AdminDeleteUsersIdRolesRole_id`: This tool helps store administors. Remove a Role from a user.
- `AdminGetViewsEntityColumns`: This tool helps store administors. Retrieve a list of columns in a view for an entity. The columns are retrieved for the authenticated admin user.
- `AdminGetViewsEntityConfigurations`: This tool helps store administors. Retrieve a list of view configurations of an entity. The configurations can be filtered by fields like `id`. The configurations can also be paginated. An admin user can only retrieve their own configurations.
- `AdminGetViewsEntityConfigurationsActive`: This tool helps store administors. Get the active view configurations for an entity. If no active view is set, `null` is returned. An admin user can only retrieve their own active configuration.
- `AdminGetViewsEntityConfigurationsId`: This tool helps store administors. Retrieve a view configuration for an entity. An admin user can only retrieve their own configurations.
- `AdminGetWorkflowsExecutions`: This tool helps store administors. Retrieve a list of workflows executions. The workflows executions can be filtered by fields such as `id`. The workflows executions can also be sorted or paginated.
- `AdminGetWorkflowsExecutionsId`: This tool helps store administors. Retrieve a workflows execution by its ID. You can expand the workflows execution's relations or select the fields that should be returned.
- `AdminPostWorkflowsExecutionsWorkflow_idRun`: This tool helps store administors. Execute a workflow by its ID.
- `AdminPostWorkflowsExecutionsWorkflow_idStepsFailure`: This tool helps store administors. Set the status of a step in a workflow's execution as failed. This is useful for long-running workflows.
- `AdminPostWorkflowsExecutionsWorkflow_idStepsSuccess`: This tool helps store administors. Set the status of a step in a workflow's execution as successful. This is useful for long-running workflows.
- `AdminGetWorkflowsExecutionsWorkflow_idSubscribe`: This tool helps store administors. Subscribe to a workflow's execution to receive real-time information about its steps, status, and data.
This route returns an event stream that you can consume using the [EventSource API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource).

- `AdminGetWorkflowsExecutionsWorkflow_idTransaction_id`: This tool helps store administors. Get the details of the workflow's execution.
- `AdminGetWorkflowsExecutionsWorkflow_idTransaction_idStep_idSubscribe`: This tool helps store administors. Subscribe to a step in a workflow's execution to receive real-time information about its status and data.
This route returns an event stream that you can consume using the [EventSource API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource).

- `AdminPostSession`: This tool helps store administors. Set the cookie session ID of an admin user. The admin must be previously authenticated with the `/auth/user/{provider}` API route first, as the JWT token is required in the header of the request.
- `AdminPostAdminAuthTokenRefresh`: This tool helps store administors. Refresh the authentication token of a user. This is useful after authenticating a user with a third-party service to ensure the token holds the new user's details, or when you don't want users to re-login every day.
- `AdminPostActor_typeAuth_provider`: This tool helps store administors. Authenticate a user and receive the JWT token to be used in the header of subsequent requests.

When used with a third-party provider, such as Google, the request returns a `location` property. You redirect to the specified URL in your frontend to continue authentication with the third-party service.

- `AdminPostActor_typeAuth_providerCallback`: This tool helps store administors. This API route is used by your dashboard or frontend application when a third-party provider redirects to it after authentication. It validates the authentication with the third-party provider and, if successful, returns an authentication token. All query parameters received from the third-party provider, such as `code`, `state`, and `error`, must be passed as query parameters to this route.

You can decode the JWT token using libraries like [react-jwt](https://www.npmjs.com/package/react-jwt) in the frontend. If the decoded data doesn't  have an `actor_id` property, then you must create a user, typically using the Accept Invite route passing the token in the request's Authorization header.

- `AdminPostActor_typeAuth_provider_register`: This tool helps store administors. This API route retrieves a registration JWT token of a user that hasn't been registered yet. The token is used in the header of requests that create a user, such as the Accept Invite API route.
- `AdminPostActor_typeAuth_providerResetPassword`: This tool helps store administors. Generate a reset password token for an admin user. This API route doesn't reset the admin's password or send them the reset instructions in a notification.

Instead, This API route emits the `auth.password_reset` event, passing it the token as a payload. You can listen to that event in a subscriber as explained in [this guide](https://docs.medusajs.com/resources/commerce-modules/auth/reset-password), then send the user a notification. The notification is sent using a [Notification Module Provider](https://docs.medusajs.com/resources/infrastructure-modules/notification), and it should have the URL to reset the password in the Medusa Admin dashboard, such as `http://localhost:9000/app/reset-password?token=123`.


 Use the generated token to update the user's password using the [Reset Password API route](https://docs.medusajs.com/api/admin#auth_postactor_typeauth_providerupdate).

- `AdminPostActor_typeAuth_providerUpdate`: This tool helps store administors. Reset an admin user's password using a reset-password token generated with the [Generate Reset Password Token API route](https://docs.medusajs.com/api/admin#auth_postactor_typeauth_providerresetpassword). You pass the token as a bearer token in the request's Authorization header.

## Usage Pattern

When the user's request matches this skill's capabilities:

**Step 1: Identify the right tool** from the list above

**Step 2: Generate a tool call** in this JSON format:

```json
{
  "tool": "tool_name",
  "arguments": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

**Step 3: Execute via bash:**

```bash
cd $SKILL_DIR
python executor.py --call 'YOUR_JSON_HERE'
```

IMPORTANT: Replace $SKILL_DIR with the actual discovered path of this skill directory.

## Getting Tool Details

If you need detailed information about a specific tool's parameters:

```bash
cd $SKILL_DIR
python executor.py --describe tool_name
```

This loads ONLY that tool's schema, not all tools.

## Examples

### Example 1: Simple tool call

User: "Use medusa-mcp to do X"

Your workflow:
1. Identify tool: `example_tool`
2. Generate call JSON
3. Execute:

```bash
cd $SKILL_DIR
python executor.py --call '{"tool": "example_tool", "arguments": {"param1": "value"}}'
```

### Example 2: Get tool details first

```bash
cd $SKILL_DIR
python executor.py --describe example_tool
```

Returns the full schema, then you can generate the appropriate call.

## Error Handling

If the executor returns an error:
- Check the tool name is correct
- Verify required arguments are provided
- Ensure the MCP server is accessible

## Performance Notes

Context usage comparison for this skill:

| Scenario | MCP (preload) | Skill (dynamic) |
|----------|---------------|-----------------|
| Idle | 149500 tokens | 100 tokens |
| Active | 149500 tokens | 5k tokens |
| Executing | 149500 tokens | 0 tokens |

Savings: ~96% reduction in typical usage

---

*This skill was auto-generated from an MCP server configuration.*
*Generator: mcp_to_skill.py*
