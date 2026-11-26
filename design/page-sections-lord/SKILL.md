---
name: page-sections-lord
always: true
description: Design and build section-based landing and content pages with Filament Builder in Laravel.
triggers:
  - page sections lord
  - page
  - build
  - section

---
[SKILL] page-sections-lord
[OBJ] Design, scaffold, and operate reusable page sections and landing pages via Filament/Laravel.
[RULES]
1. [CMD] IDs: Filament `/filamentphp/filament`; Filament Spatie Translatable Plugin `/filamentphp/spatie-laravel-translatable-plugin`; Spatie Translatable `/spatie/laravel-translatable`; Spatie Query Builder `/spatie/laravel-query-builder`; Filament Fabricator `/z3d0x/filament-fabricator` (block-based alternative).
2. [REQ] Page-builder pattern core: `Page` model with JSON `content`; translatable `title`, `slug`, `description`, `content`, `meta_title`, `meta_desc`, `meta_keywords`; parent `page_id` self-reference; `is_home`, `is_header`, `is_footer` flags.
3. [REQ] Filament `Builder` for `content.{locale}`; one `Block::make('X_section')` per section with a unique type key and a schema that matches the frontend component props.
4. [REQ] Standard block shape: `{ "type": "hero_section", "data": { ... } }`; keep `data` flat; use consistent image key names (`image`, `background_image`, `*_image`, `logo`, `icon`).
5. [REQ] Static pages: `StaticPage` model with `type` and translatable `title`/`content`/`slug`; seed `privacy-policy`, `terms-of-service`, `faqs`, `ai-ethics`, `about-us`; embed via a `static_*_section` block that maps type to slug.
6. [REQ] API: `PageController` with index (`Spatie\QueryBuilder`), `show($slug)` by locale, and `sections($slug)`; cast `content` to array; recursively transform image keys to full `Storage::disk('s3')->url()` or `asset(Storage::url(...))` URLs.
7. [REQ] i18n: Spatie `HasTranslations` on `Page` and `StaticPage`; Filament translatable tabs; lookup by `slug->{locale}` with fallback to default locale; `app()->getLocale()` in controller.
8. [REQ] Common blocks: hero, destinations, testimonials, vision, mission, story_stats, tech_features, team, cta, contact, global_presence, faqs, privacy_policy, terms_of_service, ai_ethics, about_us. Add new blocks via new `Block` in `PageForm` and a matching frontend component.
9. [REQ] Image handling: `FileUpload::image()` with directory `assets/images/pages/{section}`; store only relative paths in DB; API returns absolute URLs; preview images under `public/assets/images/builder-previews/{section}.png` for Filament block labels.
10. [REQ] Reusability: when blocks need cross-page reuse, tenant-scoping, or user-defined block types, migrate to `page_sections` pivot or `filament-fabricator` block registry; keep block shape `type`/`data` to ease migration.
11. [REQ] New projects: start from `skills/page-sections-lord/templates/page-builder-spec.md`; follow the scaffold order: migrations → models → Filament resource/form → API controller/resource → routes → frontend section components → static pages seeder.
12. [REQ] Security/RBAC: use `filament-shield` for admin permissions; validate `slug` uniqueness per locale; never expose one tenant's page/section to another; apply tenant scope if multi-tenancy.
13. [REQ] Cross-stack questions query `page-sections-lord`, `backend-frameworks-lord`, `frontend-frameworks-lord`, and `mariadb-lord` if database-specific; explain the rationale.
14. [REQ] Status Enum for Pages (Sky pattern): `enum PageStatus: string implements HasColor, HasIcon, HasLabel` with 7 states: Publish, Future, Draft, Auto, Pending, Private, Trash. ⛔ NEVER string status column. Use backed enum with colors/icons. Filter scopes: `scopePublished`, `scopeSticky`, `scopeDraft`.
15. [REQ] Tab-based Page Form (Sky pattern): `Tabs::make('content_tabs')` with logical tabs: Content (title + editor), SEO (description + slug + meta), Visibility (status + password + published_at + sticky_until), Media (featured image upload/URL toggle). ⛔ NEVER one long form. Split by domain concern.
16. [REQ] Upload/URL Toggle for Images (Sky pattern): `ToggleButtons::make('image_type')->options(['upload' => 'Upload', 'url' => 'URL'])->live()` + `SpatieMediaLibraryFileUpload::make('image_upload')->visible(fn(Get $get) => $get('image_type') === 'upload')` + `TextInput::make('image_url')->url()->visible(fn(Get $get) => $get('image_type') === 'url')`. Flexible media input per block.
17. [REQ] Configurable Editor (Filament-Blog pattern): `HasContentEditor` trait + `getContentEditor(string $field)` method. `config('page-sections.editor')` selects RichEditor / MarkdownEditor / TinyEditor. `config('page-sections.toolbar_buttons')` for toolbar. Pluggable without code changes.
18. [REQ] Navigation Builder (Sky pattern): `Navigation` model with JSON `items` field. `ViewField::make('items')->default([])->view('navigation-builder')` custom blade view. Drag-drop menu builder in admin. Locations config: header, footer, footer-2, etc.
19. [REQ] Search Highlighting (Sky pattern): `highlightSearchResults(Collection $collection, ?string $search): Collection` trait. Highlight matched terms in title/content for frontend search. `parsing(string $text, array $terms): string` helper.
20. [REQ] Spatie Media Library (Sky pattern): `InteractsWithMedia` + collections per section type (`posts`, `pages`, `sections`). `SpatieMediaLibraryFileUpload` with disk from plugin config: `SkyPlugin::get()->getUploadDisk()`. `$model->getFirstMediaUrl('collection')` for URLs. ⛔ NEVER plain `FileUpload` for complex media. Use collections + conversions.
21. [REQ] Spatie Tags with Types (Sky pattern): `SpatieTagsInput::make('tags')->type('section_tag')` for typed taxonomy. Differentiate tags vs categories via `type` parameter. `SelectFilter::make('tags')->multiple()->relationship('tags', 'name')` for table filters.
22. [REQ] Password Protection (Sky pattern): `status === 'private'` + `password` field on Page model. `requirePassword(): Attribute` checks status + password presence. Frontend prompts password before showing private pages.
23. [REQ] Sticky/Scheduling (Sky pattern): `sticky_until` date column for sticky posts with expiry. `published_at` datetime for scheduling. `scopeSticky(Builder $q): $q->whereNotNull('sticky_until')->whereDate('sticky_until', '>=', now())`. `scopePublished`: status=publish + published_at <= now.
24. [REQ] Parent-Child Pages (Sky pattern): `parent_id` self-reference + `ordering` integer. `Select::make('parent_id')->options(Post::where('post_type', 'page')->pluck('title', 'id'))`. Hierarchical page structure. Frontend renders tree.
25. [REQ] FAQ Schema (MVPable pattern): `faqSchema(array $faqs): array` generates JSON-LD `{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[...]}`. Embed via `<script type="application/ld+json">`. Google rich results for FAQ sections.
26. [REQ] Breadcrumb Schema (MVPable pattern): `breadcrumbSchema(array $breadcrumbs): array` generates JSON-LD `BreadcrumbList`. `{"@type":"ListItem","position":N,"name":"...","item":"..."}`. Google sitelinks breadcrumb display.
27. [REQ] Article Schema (MVPable pattern): `articleSchema(headline, description, image, publishedTime, modifiedTime, author)` generates JSON-LD `Article`. For blog/news sections. Google News inclusion.
28. [REQ] Organization Schema (MVPable pattern): `organizationSchema(): array` generates JSON-LD `Organization` with `name`, `legalName`, `url`, `logo`, `sameAs` (social links). For site-wide structured data.
29. [REQ] Action Groups (Sky pattern): `ActionGroup::make([EditAction::make('edit'), Action::make('Open')->url()->openUrlInNewTab(), DeleteAction::make('delete'), ForceDeleteAction::make(), RestoreAction::make()])` for consistent record actions across all page resources.
30. [REQ] Navigation Badges (Sky pattern): `getNavigationBadge(): ?string` returns `(string) Model::count()`. Respect visibility config: `SkyPlugin::getNavigationBadgesVisibility(static::class)`. Show counts in sidebar navigation.
31. [REQ] Create Option Forms (Filament-Blog pattern): `Select::make('category_id')->relationship('category', 'name')->createOptionForm([TextInput::make('name'), TextInput::make('slug')])->preload()->searchable()`. Inline creation without leaving page. Reduces context switching.
32. [REQ] Auto-slug Generation (Sky/Filament-Blog pattern): `TextInput::make('title')->live(onBlur: true)->afterStateUpdated(fn(Set $set, $state, $context) => $context === 'edit' ?: $set('slug', Str::slug($state)))`. ⛔ NEVER overwrite slug on edit.
