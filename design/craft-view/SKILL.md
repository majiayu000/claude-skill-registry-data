---
name: craft-view
description: Crafting package views. Blade components, view publishing, and the visual contract with your consumers.
---

# Skill: Craft View

> "Published views assert stability across the major version. Every `vendor:publish` is a promise." -- Dan Harrin

## The Standard

1. **Namespace Everything**: Register views with `loadViewsFrom()` using a namespace. Always `package::view-name`. Never pollute the global view namespace. Collisions with other packages or the app itself are silent and maddening.

   ```php
   $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

   // Consumer usage
   return view('courier::dashboard');
   ```

2. **Published Views Are a Contract**: When consumers publish your views, they expect those views to remain stable within the major version. Changing published view structure in a minor release breaks every consumer who customized them. Treat published views like a public API.

3. **Blade Component Registration**: Three approaches, matched to the need.

   | Approach             | Method                                                          | When                                                   |
   |----------------------|-----------------------------------------------------------------|--------------------------------------------------------|
   | Explicit alias       | `Blade::component('pkg-alert', AlertComponent::class)`          | One-off components, maximum clarity                    |
   | Component namespace  | `Blade::componentNamespace('Vendor\\Views\\Components', 'pkg')` | Many components, auto-discovery via `<x-pkg::alert />` |
   | Anonymous components | Place in `resources/views/components/`                          | Simple markup-only components, no class needed         |

   Spatie's `PackageServiceProvider` handles this: `->hasViewComponents('spatie', Alert::class, Card::class)` registers components with the `<x-spatie-alert />` prefix.

4. **Anonymous Components in Packages**: Place them in the `components/` subdirectory of your views directory. They are auto-discovered once `loadViewsFrom()` is registered. Consumer usage: `<x-courier::alert />`.

5. **CSS Framework Agnosticism**: Never hardcode Tailwind, Bootstrap, or any CSS framework in package views. Either ship unstyled views with CSS classes consumers can target, or use a configurable theme approach. Filament's pattern: a design system of Blade components that abstracts the CSS framework entirely.

6. **View Publishing Groups**: Namespace publish tags as `{package}-views`. Let consumers publish only what they need. Never bundle views with config in a single publish tag.

   ```php
   $this->publishes([
       __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
   ], 'courier-views');
   ```

7. **View Composers for Shared Data**: When views need data that doesn't come from the controller, use view composers. Register them in the service provider. Keep the composer class focused -- single concern, no side effects.

   ```php
   View::composer('courier::*', function ($view) {
       $view->with('courierVersion', Courier::VERSION);
   });
   ```

8. **Livewire Component Registration**: For packages that ship Livewire components, register them explicitly with `Livewire::component()`. Use a consistent naming convention: `package-name::component-name`.

   ```php
   use Livewire\Livewire;

   Livewire::component('courier::tracking-widget', TrackingWidget::class);
   ```

9. **Render Hooks**: For packages that need to inject UI into specific locations (admin panels, dashboards), provide named render hooks. Filament's pattern: `renderHook('panels::body.start')`. Consumers register content at hooks without modifying views.

10. **View Override Priority**: Laravel checks `resources/views/vendor/{package}/` before the package's own views directory. This is automatic once you use `loadViewsFrom()`. Document which views are safe to override and which are internal.

## The Anti-Patterns

| Don't                                             | Do                                                             | Why                                       |
|---------------------------------------------------|----------------------------------------------------------------|-------------------------------------------|
| Skip view namespace                               | Always `loadViewsFrom()` with a namespace                      | Collisions with other packages are silent |
| Change published view structure in minor versions | Treat published views as a major-version contract              | Breaks every consumer who customized them |
| Hardcode CSS frameworks in views                  | Ship framework-agnostic markup or configurable themes          | Forces consumers into your CSS choices    |
| Bundle views and config in one publish tag        | Separate publish groups: `{package}-views`, `{package}-config` | Consumers publish only what they need     |
| Register Livewire components without namespace    | Use `package::component` naming                                | Collisions with app components            |
| Ship complex logic in Blade templates             | Extract to Blade components or view models                     | Blade is for presentation, not logic      |
| Publish every view                                | Only publish views consumers will customize                    | Less surface area to maintain             |
| Forget view override documentation                | Document which views are safe to override                      | Consumers need to know what's stable      |

## Real-World Examples

See [examples.md](examples.md).
