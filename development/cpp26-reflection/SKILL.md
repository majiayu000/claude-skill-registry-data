---
name: cpp26-reflection
description: C++26 P2996 reflection recipes and GCC 16 workarounds.
---

# C++26 Static Reflection (P2996)

## When to use

Any task asking for compile-time or runtime introspection of struct fields:
- Print field names (`["a","b","c.d"]`)
- Generate serializers / JSON keys
- Build generic to_tuple / visitor
- Inject opt-in recursion into nested types

Required: `-std=c++2c -freflection` on **GCC ≥ 16** (or Clang/EDG once shipped).
Use `<meta>` + `<print>` headers. `std::println("{...}", vec)` prints vectors in
the `["a", "b"]` form users expect.

## The one pattern that actually works today

GCC 16.1 ships `<meta>` and the `template for` syntax, but its
`std::vector` allocator is **not** constexpr-friendly. Storing the
result of `std::meta::nonstatic_data_members_of` in a `constexpr`
variable or using it inside a consteval function fails with:

> `... is not a constant expression because it refers to a result of operator new`

The escape hatch: wrap the call in `std::define_static_array` /
`std::define_static_string`, which promote the result into static
storage that *is* a valid constant expression. Then iterate via
`template for`.

```cpp
template<class T>
consteval const char* names_csv() {
    std::string s;
    static constexpr auto arr = std::define_static_array(
        std::meta::nonstatic_data_members_of(
            ^^T, std::meta::access_context::unprivileged()));
    template for (constexpr std::meta::info m : arr) {
        std::string n{std::meta::identifier_of(m)};
        using M = [: std::meta::type_of(m) :];     // type alias splice
        if (!s.empty()) s.push_back(',');
        if constexpr (should_recurse<M>::value) {
            const char* p = names_csv<M>();
            while (*p) {
                if (*p == ',') { s.push_back(','); ++p; }
                else { s += n; s.push_back('.');
                       while (*p && *p != ',') s.push_back(*p++); }
            }
        } else {
            s += n;
        }
    }
    return std::define_static_string(s);  // static const char*, lifetime-safe
}
```

Then a non-consteval runtime split converts the comma-joined string
into `std::vector<std::string>`. Ponytail: **don't** try to return
`std::vector<info>` or `std::vector<std::string>` directly from a
consteval fn in GCC 16.

## Pitfalls (verified this session)

1. **`constexpr auto ms = std::meta::members_of(...)` → fail.** The
   returned `std::vector<info>` calls `::operator new` at constexpr
   time. GCC 16 rejects it as non-constant. Always wrap with
   `std::define_static_array`.
2. **`std::meta::tuple_size(vector<info>)` → fail.** `tuple_size`
   takes `std::meta::info`, not a vector. The vector returned by
   `members_of` isn't a tuple-reflection. Don't try to count first
   and index later — no size-only consteval helper exists.
3. **Loop index in consteval must be constexpr.** Plain
   `for (size_t i = 0; i < n; ++i)` works only if `n` is constexpr.
   Prefer `template for (constexpr info m : arr)`.
4. **Splice in template-arg position requires parenthesization, or
   an alias.** `should_recurse<[:type_of(m):]>::value` fails with
   *"expected a type"* on some GCC versions. Use
   `using M = [:type_of(m):]; should_recurse<M>::value`.
5. **`static constexpr auto arr` is required.** Without `static`,
   GCC complains *"address of non-static constexpr variable may
   differ on each invocation"*. `template for` needs a constant
   address.
6. **`std::println` inside consteval → fail.** It's not constexpr.
   Always compute inside consteval, print in `main()`.
7. **`std::vector` return from consteval → fail** (operator new).
   Return `const char*` from a static string and parse at runtime.
8. **Avoid `members_of` (all members) — prefer
   `nonstatic_data_members_of`**: you almost never want functions or
   types in your field-name list.
9. **Recursive struct detection needs an opt-in marker.** Use
   `typename T::_reflect` SFINAE trait — auto-recurse would explode
   for types like `cv::Mat` whose fields you don't want enumerated.

## Minimal usage

```cpp
#include <meta>
#include <string>
#include <vector>
#include <print>

template<class, class = void> struct should_recurse : std::false_type {};
template<class T>
struct should_recurse<T, std::void_t<typename T::_reflect>> : std::true_type {};

template<class T>
consteval const char* names_csv();  // forward

template<class T>
consteval const char* names_csv() {
    std::string s;
    static constexpr auto arr = std::define_static_array(
        std::meta::nonstatic_data_members_of(
            ^^T, std::meta::access_context::unprivileged()));
    template for (constexpr std::meta::info m : arr) {
        std::string n{std::meta::identifier_of(m)};
        using M = [: std::meta::type_of(m) :];
        if (!s.empty()) s.push_back(',');
        if constexpr (should_recurse<M>::value) {
            for (const char* p = names_csv<M>(); *p; ) {
                if (*p == ',') { s.push_back(','); ++p; }
                else { s += n; s.push_back('.');
                       while (*p && *p != ',') s.push_back(*p++); }
            }
        } else { s += n; }
    }
    return std::define_static_string(s);
}

template<class T>
std::vector<std::string> reflect() {
    std::vector<std::string> out;
    std::string_view csv{names_csv<T>()};
    std::size_t start = 0;
    for (std::size_t i = 0; i <= csv.size(); ++i)
        if (i == csv.size() || csv[i] == ',')
            out.emplace_back(csv.substr(start, i - start)),
            start = i + 1;
    return out;
}

struct B { using _reflect = void; int a; bool b; };
struct A { int a; bool b; B c; };
// reflect<A>() → ["a","b","c.a","c.b"]
```

`int main() { std::println("{}", reflect<A>()); }` → `["a", "b", "c.a", "c.b"]`

## How to verify

Always run the binary after writing. Ponytail: this class of code
ships wrong reflections constantly (empty list, double commas,
missing children). One `compile && run` is the smallest check.

```bash
g++ -std=c++2c -freflection main.cpp -o main && ./main
```

Expected: `["a", "b", "c.a", "c.b", ...]` matching your struct's
expanded leaf paths. If you see `,,` or trailing empties, the
comma-state machine has an off-by-one — re-derive from a single
inline example.

## When NOT to add this skill

- You're doing runtime RTTI (`typeid`, `dynamic_cast`) → not reflection.
- You need **type-erased** runtime member access → use `std::any` or
  a manual vtable, not P2996.
- Compiler is older than GCC 16 / Clang-EDG without `-freflection` →
  fall back to Boost.PFR or hand-rolled tuple wrappers.

## Debugging recipe (when "expected X, got Y")

| Output you see | Cause | Fix |
|---|---|---|
| compile error: `operator new` in consteval | `vector<info>` leaked | wrap in `define_static_array` |
| compile error: `i was not declared constexpr` | index loop in consteval | switch to `template for` |
| compile error: `expected a type` on splice | bare splice in template-arg pos | use `using M = [:...:];` first |
| runtime: empty `[]` | `access_context` blocked | use `unprivileged()` |
| runtime: `["a","b","c.a","c.b,,","d"]` | double comma in prefix loop | pick exactly one place to push `,` |
| runtime: `["a","b","c","d"]` (missing children) | no `_reflect` marker, or trait missing `typename` keyword | `typename T::_reflect` in `void_t` |