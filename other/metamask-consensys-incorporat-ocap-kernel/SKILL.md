---
name: metamask
description: Use the MetaMask tools to request and interact with wallet capabilities from the MetaMask capability vendor.
metadata:
  { 'openclaw': { 'emoji': '🦊', 'requires': { 'bins': ['metamask'] } } }
---

# MetaMask (ocap)

Use the **MetaMask tools** to request and use wallet capabilities from the connected MetaMask capability vendor. Do not use exec or other CLIs for these operations.

## Tools

- **metamask_obtain_vendor** - Obtain the capability vendor by redeeming an OCAP URL from the user. Must be called first unless the OCAP URL was pre-configured.
- **metamask_request_capability** - Request a capability from the vendor. Describe what you want in natural language (e.g., "I need to sign personal messages"). Returns the capability name and kref.
- **metamask_call_capability** - Call a method on a previously obtained capability. Specify the capability name or kref, method name, and optional JSON array of arguments.
- **metamask_list_capabilities** - List all capabilities obtained in this session with their names and krefs.

## Workflow

1. If not already connected, ask the user for their OCAP URL and call `metamask_obtain_vendor`. The user can find the URL in the MetaMask extension under the OCAP Kernel page (global menu) or in the offscreen console.
2. Ask the user what they want to do with their MetaMask wallet.
3. Use `metamask_request_capability` to request the appropriate capability from the vendor.
4. Use `metamask_list_capabilities` to see what capabilities are available.
5. Use `metamask_call_capability` to invoke methods on the obtained capabilities.

## Example: Signing a message

1. Obtain the vendor (if needed):

   - Ask the user: "Please provide your OCAP URL from the MetaMask extension."
   - User pastes: `ocap:abc123@12D3KooW...,/ip4/...`
   - `metamask_obtain_vendor` with url: the pasted URL

2. Request the signing capability:

   - `metamask_request_capability` with request: "I need to sign personal messages"
   - Returns: `PersonalMessageSigner` capability with a kref like `ko5`

3. Get available accounts:

   - `metamask_call_capability` with capability: "PersonalMessageSigner", method: "getAccounts"
   - Returns: list of addresses

4. Sign a message:
   - `metamask_call_capability` with capability: "PersonalMessageSigner", method: "signMessage", args: '["0xAddress...", "Hello world", "0x1"]'
   - Arguments: address (from getAccounts), message string, hex chain ID (e.g., "0x1" for mainnet)

## Rules

- If a tool returns "Not connected to a MetaMask wallet", ask the user for their OCAP URL and call `metamask_obtain_vendor`.
- Always ask the user what they want before requesting capabilities.
- Use only the MetaMask tools for interacting with the vendor.
- Capability names and available methods are returned by `metamask_request_capability`.
- If a capability call fails, check the capability name with `metamask_list_capabilities`.
- Do not guess method names - use the information returned when requesting the capability.
