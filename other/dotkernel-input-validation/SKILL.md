---
name: dotkernel-input-validation
description: >
  Use when handling incoming data in a Dotkernel project — writing or changing an
  InputFilter, an Input class, or a laminas-form Form; wiring validators, filters and error
  messages; handling CSRF on a templated project; validating uploads; or deciding where a value
  should be checked. Also use when a write endpoint accepts data it should reject, when
  validation messages are inconsistent, or when a form redisplays without its errors.
---

# Input validation and forms

```text
Applies to
  Projects:  - Dotkernel API
             - Dotkernel Admin
             - Dotkernel Frontend
  Packages:  - none
```

**Never trust input.** Nothing from the request reaches a service, entity or query builder
before it has been through validation.

Which mechanism depends on the variant (`dotkernel-project-variants`):

| Variant | Mechanism |
| --- | --- |
| API | `laminas/laminas-inputfilter` |
| Admin / Frontend | `laminas/laminas-form` — objects for elements, wrapping an InputFilter, plus CSRF |

The stock Light accepts no input and the stock Queue validates no request data; if you add
either to one of them, use an InputFilter.

## InputFilters (every variant)

```text
src/<Module>/src/InputFilter/
├── Input/TitleInput.php                extends Laminas\InputFilter\Input
├── CreateBookInputFilter.php           extends the repo's AbstractInputFilter
└── UpdateBookInputFilter.php
```

An Input class owns one field, and attaches **both** a filter chain and a validator chain:

```php
class TitleInput extends Input
{
    public const TITLE_MAX_LENGTH = 191;

    public function __construct(?string $name = null, bool $isRequired = true)
    {
        parent::__construct($name);
        $this->setRequired($isRequired);

        $this->getFilterChain()
            ->attachByName(StringTrim::class)
            ->attachByName(StripTags::class);

        $this->getValidatorChain()
            ->attachByName(NotEmpty::class, ['message' => Message::VALIDATOR_REQUIRED_FIELD], true)
            ->attachByName(StringLength::class, [
                'max'     => self::TITLE_MAX_LENGTH,
                'message' => Message::validatorLengthMax(self::TITLE_MAX_LENGTH),
            ], true);
    }
}
```

Rules:

- Reuse the shared Input classes in the project's `App` module (API and Admin: email, password, UUID,
  image, identity…) before writing a new one.
- `max` length must match the entity's column length. Drifting these two is a 500 waiting for
  a long input.
- Messages come from the shared message catalogue constant, never inline strings.
- The `true` third argument breaks the chain on failure, so one field yields one message.
- Nested structures use `CollectionInputFilter` / a child InputFilter added under a key.
- Document the validated shape with `@phpstan-type` on the filter so phpstan can narrow it.

## Using an InputFilter (API style)

```php
$this->inputFilter->setData((array) $request->getParsedBody());
if (! $this->inputFilter->isValid()) {
    throw BadRequestException::create(
        detail: Message::VALIDATOR_INVALID_DATA,
        additional: ['errors' => $this->inputFilter->getMessages()]
    );
}
$data = (array) $this->inputFilter->getValues();   // never getRawValues()
```

`getValues()` returns filtered values; `getRawValues()` bypasses the filter chain and defeats
the point.

## Forms (Admin / Frontend)

`laminas-form` gives a thin object layer over elements, an InputFilter per input, and binding
data to and from the form. It integrates with the Laminas security ecosystem —
`laminas-escaper`, `laminas-validator`, `laminas-filter`, `laminas-session` — so validation,
filtering and rendering enforce escaping by design.

- One `Form` class per use case, in `src/<Module>/src/Form/`.
- Attach the InputFilter rather than declaring validators inline, so the same rules are
  reusable from a CLI command or an API.
- **Every form needs a CSRF element**, and the handler must validate it. A form without CSRF is
  a vulnerability, not a simplification.
- On failure, re-render the same template with the form bound so the user sees their input and
  the messages — do not redirect and lose them.
- Escaping is the view layer's job; never build HTML in a handler or service.

## Query parameters are input too

Sort, filter, pagination and search values arrive unvalidated. **Whitelist sortable and
filterable columns against an explicit array** before they reach a query builder, and clamp
`limit` to a maximum. An unwhitelisted `sort` is an injection and enumeration risk, not a style
detail.

## Uploads

Validate MIME type and size with the shared image/file Input, store outside any
web-executable path, and never trust the client-supplied filename or extension.

## Checklist

- [ ] Every write path validates before any business logic runs.
- [ ] Input `max` lengths match the entity column lengths.
- [ ] Messages come from the shared catalogue.
- [ ] `getValues()`, not `getRawValues()`.
- [ ] CSRF element present and validated (templated projects).
- [ ] Failed form re-renders bound, with messages.
- [ ] Sort/filter/limit whitelisted and clamped.
- [ ] Uploads checked for type and size.
- [ ] Validated shape typed for phpstan.
