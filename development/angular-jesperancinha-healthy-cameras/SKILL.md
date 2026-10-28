---
name: angular
description: Conventions for Angular applications 
---

## 1. In all setup files, the target should be esnext

### Example in `tsconfig.json`:

Replace:

```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["es5", "dom"],
    "types": ["cypress", "node"]
  },
  "include": ["**/*.ts"]
}
```

with

```json
{
  "compilerOptions": {
    "target": "esnext",
    "lib": ["esnext", "dom"],
    "types": ["cypress", "node"]
  },
  "include": ["**/*.ts"]
}
```

## 2. Make sure that the code strictly follows all angular standards

Please find the list of alle angular standards on the following page: https://angular.dev/style-guide.
It is of the utmost importance that all configuration, HTML, TypeScript, JavaScript, and everything that consists of an angular project, to follow these standards.
Changes should be made accordingly.
Modernize the build tooling too

## 3. Make sure that Angular projects are completely reactive with the usage of signals.

With the inception of signals, reactive programming for the front-end has been made easy. Make sure that, whenever possible, that the code uses signals instead of the typical subscriber model.
Find information on how to do this with good practices over at: https://angular.dev/guide/signals
Refactor subscribe() to resource()/rxResource()

## 4. Make sure to use new methods for deprecated classes

The `RouterTestingModule` and the `HttpClientTestingModule` have been deprecated. Can you make sure to replace the TypeScript declarations accordingly?


From `RouterTestingModule`.

```text
Use provideRouter or RouterModule/RouterModule.forRoot instead. This module was previously used to provide a helpful collection of test fakes, most notably those for Location and LocationStrategy. These are generally not required anymore, as MockPlatformLocation is provided in TestBed by default. However, you can use them directly with provideLocationMocks.
```

From `HttpClientTestingModule`.

```text
Add provideHttpClientTesting() to your providers instead.
```

Use both definitions to make the changes wherever possible.

## 6. Update the build system, if necessary

Follow the documentation on https://angular.dev/tools/cli/build-system-migration to  make a successful build migration

## 7. Use scss/css standards for scss files

In old projects, very little attention was given to scss standards.
Here we want to make sure that all scss is being applied according to the scss documents over at:

1. https://sass-lang.com/documentation/syntax/
2. https://sass-lang.com/documentation/

When possible, make sure to optimize the use of scss for grids.
Documentation can be found here:

1. https://css-tricks.com/complete-guide-css-grid-layout/

## 8. Checklist

[] All targets in `tsconfig.json` files should be set to `esnext`
[] No target should remain with old target compiler option versions
