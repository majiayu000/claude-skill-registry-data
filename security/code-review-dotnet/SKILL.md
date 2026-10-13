---
name: code-review-dotnet
description: >
  Security review of .NET / C# code — dangerous sinks and ASP.NET pitfalls. Load when reviewing a
  C#/.NET codebase/PR, on .cs source in scope, or "review this .NET app". Signals: .csproj/.sln,
  ASP.NET (Core/MVC/WebForms), BinaryFormatter, SqlCommand, Razor Html.Raw, XmlDocument.
domain: code-review
type: reference
stability: learning
modes: [bugbounty, defense, pentest]
severity: info
cwe: [CWE-502, CWE-89, CWE-78, CWE-611, CWE-79]
tools: [semgrep, security-code-scan, codeql, ripgrep]
schema_version: 1
---

# .NET / C# source review

## When it applies
Reviewing C#/.NET source (ASP.NET Core, MVC, or legacy WebForms). The headline risks are unsafe
deserialization, string-built SQL, XXE, and Razor's raw-output escape hatch.

## Why it works
.NET ships powerful-but-dangerous serializers (`BinaryFormatter`, `Json.NET` with
`TypeNameHandling`, `LosFormatter`/ViewState) that instantiate arbitrary types, and several XML APIs
resolve DTDs by default on older frameworks. Reviews find where these meet untrusted input.

## Sinks & patterns (grep, then trace to user input)
- **Deserialization**: `BinaryFormatter`, `LosFormatter`, `SoapFormatter`, `NetDataContractSerializer`,
  `JsonConvert` with `TypeNameHandling != None`, `Js.NET`/`fastJSON` polymorphic types → RCE gadgets.
- **SQLi**: string-concatenated `SqlCommand`/`ExecuteReader`/`FromSqlRaw`(EF Core) vs parameters.
- **Command exec**: `Process.Start` with concatenated arguments / `UseShellExecute`.
- **XXE**: `XmlDocument`/`XmlReader`/`XmlTextReader` without `DtdProcessing=Prohibit` (legacy default
  resolves entities); `XmlSerializer` with a user-controlled type.
- **XSS**: Razor `@Html.Raw(...)`, `MvcHtmlString`, WebForms `<%= %>` with unencoded input;
  `Response.Write`.
- **Other**: path traversal via `Path.Combine(root, input)`, `LdapConnection` filter injection,
  reflection (`Type.GetType`/`Activator.CreateInstance`) on input, insecure ViewState (no MAC).

## Framework specifics
- **ASP.NET Core**: model binding over-posting/mass assignment (bind whole entity), `[AllowAnonymous]`
  on sensitive actions, disabled antiforgery on POST APIs, exposed dev endpoints, open redirect via
  `Redirect(returnUrl)` without `Url.IsLocalUrl`.
- **WebForms**: ViewState deserialization (machineKey), event-validation off.

## Method
1. Run `security-code-scan`/CodeQL; treat as leads.
2. `rg 'BinaryFormatter|TypeNameHandling|FromSqlRaw|Html\.Raw|XmlDocument|Process\.Start'` → trace to input.
3. Check controller `[Authorize]`/antiforgery coverage and model-binding scope.
4. Confirm with `web-deserialization`, `web-sqli`, `web-xxe`, `web-command-injection`.

## Gotchas
- `Json.NET` is safe by default — the bug is an explicit `TypeNameHandling.All/Auto`.
- EF Core parameterises LINQ; `FromSqlRaw`/`ExecuteSqlRaw` with interpolation is where SQLi returns.
- ViewState RCE needs the `machineKey` (leaked/weak) — note the precondition.

## References
OWASP .NET security cheat sheet; ysoserial.net gadget research; Microsoft secure-coding guidance.
