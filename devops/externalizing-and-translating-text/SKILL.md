---
name: Externalizing and Translating Text
description: Externalizes user-facing text to a resource bundle where they can be easily translated. Use to externalize static strings that are shown to the end user.
---

## Workflow

Copy this checklist and track your progress:

```
Externalizing and translating strings:
- [ ] Step 1: Create String Bundle
- [ ] Step 2: Transfer Strings
- [ ] Step 3: Translate Strings for Requested Languages
- [ ] Step 4: Update References in Go Files
- [ ] Step 5: Update References in Templates
- [ ] Step 6: Versioning
```

#### Step 1: Create String Bundle

Create a `text.yaml` file under the `resources` directory of the microservice, if one does not already exist.

#### Step 2: Transfer Strings

Locate static strings in the microservice that are ultimately shown to the end user. These are likely to be in `service.go` or in HTML or text templates in the `resources` directory.

For each string, create an entry in `text.yaml` that maps a unique key to its localized value on a per language basis. Use PascalCase for the string key (e.g. `MyString`) and ISO 639 language codes for each language (e.g. `en-US`).

```yaml
HelloWorld:
  en: Hello World
```

#### Step 3: Translate Strings for Requested Languages

Update `text.yaml` and add a localized value for each explicitly requested language.
Use the ISO 639 language code under the key of each localization.

```yaml
HelloWorld:
  en: Hello World
  en-AU: G'day World
  fr: Bonjour le Monde
  es: Hola Mundo
```

The `en` or `en-US` localizations are used by default when no other language matches the request's context.
If neither localization is included, a `default` value should be provided instead.

```yaml
HolaMundo:
  fr: Bonjour le Monde
  es: Hola Mundo
  default: Hola Mundo
```

#### Step 4: Update References in Go Files

Use `svc.MustLoadResString` to load strings in Go files such as `service.go`.

Before:

```go
func (svc *Service) HelloWorld(w http.ResponseWriter, r *http.Request) (err error) {
	w.Write([]byte("Hello World"))
	return err
}
```

After:

```go
func (svc *Service) HelloWorld(w http.ResponseWriter, r *http.Request) (err error) {
	ctx := r.Context()
	textHelloWorld := svc.MustLoadResString(ctx, "HelloWorld")
	w.Write([]byte(textHelloWorld))
	return err
}
```

#### Step 5: Update References in Templates

To use localized strings in HTML templates, load all strings with `svc.MustLoadResStrings` into a map, pass the map as part of the data to the template, and use the map in the template to obtain the string by key, instead of the static string.

Before:

```go
func (svc *Service) HelloWorld(w http.ResponseWriter, r *http.Request) (err error) {
	data := struct{
		OtherData int
	}{
		OtherData: 5,
	}
	content, err := svc.ExecuteResTemplate("mytemplate.html", data)
	if err != nil {
		return errors.Trace(err)
	}
	w.Write(content)
	return nil
}
```

```html
<b>Hello World</b>
```

After:

```go
func (svc *Service) HelloWorld(w http.ResponseWriter, r *http.Request) (err error) {
	ctx := r.Context()
	data := struct{
		OtherData int
		Text map[string]string
	}{
		OtherData: 5,
		Text: svc.MustLoadResStrings(ctx),
	}
	content, err := svc.ExecuteResTemplate("mytemplate.html", data)
	if err != nil {
		return errors.Trace(err)
	}
	w.Write(content)
	return nil
}
```

```html
<b>{{ .Text.HelloWorld }}</b>
```

#### Step 6: Document the Microservice

Update the microservice's local `AGENTS.md` file to indicate that user-facing text must be externalized and translated to the requested languages.

#### Step 7: Versioning

Run `go generate` to version the code.
