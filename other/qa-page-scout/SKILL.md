---
name: qa-page-scout
section: pipeline
description: "Page fingerprint probe — runs ONE browser_evaluate per cell before skill dispatch. Returns 100 boolean flags (hasForms, hasImages, hasTables, etc.) that qa-cell-worker uses to filter out skills whose requires: [] conditions aren't met on this page. Saves ~77% tokens by skipping irrelevant skills. Runs on every cell, every viewport."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
interactive: false
requires: []
---

# qa-page-scout — Page Fingerprint

Runs as the FIRST probe on every cell. Returns a compact boolean fingerprint the worker uses to
skip skills whose `requires:` flags are all absent from this page.

**Logic:** `requires: [flag1, flag2]` = run skill if `flag1 OR flag2` is true in the fingerprint.
Skills with `requires: []` always run regardless.

## Probe (browser_evaluate)

```js
() => {
  const q = (sel, min) => { try { return document.querySelectorAll(sel).length > (min||0); } catch(e) { return false; } };
  const re = (pattern, slice) => { try { return pattern.test((document.body.innerText||'').slice(0,slice||5000)); } catch(e) { return false; } };
  const mm = q2 => { try { return window.matchMedia(q2).matches; } catch(e) { return false; } };
  const css = slice => { try { return [...document.styleSheets].flatMap(ss => { try { return [...ss.cssRules].map(r => r.cssText); } catch(e) { return []; } }).join('').slice(0,slice||8000); } catch(e) { return ''; } };

  return {
    // ── FORMS ──────────────────────────────────────────
    hasForms:             q('form'),
    hasInputs:            q('input:not([type=hidden]),textarea,select'),
    hasPasswordField:     q('input[type=password]'),
    hasFileUpload:        q('input[type=file]'),
    hasSearchInput:       q('input[type=search],[placeholder*=search i],[class*=search-input]'),
    hasRequiredFields:    q('[required],[aria-required=true]'),
    hasDateTimePicker:    q('input[type=date],input[type=time],input[type=datetime-local],[class*=datepicker],[class*=timepicker]'),
    hasMultiStepForm:     q('[class*=wizard],[class*=stepper],[class*=step-form],[data-step]'),
    hasRichTextEditor:    q('[contenteditable=true],[class*=quill],[class*=tiptap],[class*=ck-editor],[class*=froala]'),
    hasOAuthButtons:      q('[class*=social-login],[class*=oauth],[href*=google],[href*=github]'),
    hasAutoComplete:      q('[list],[class*=autocomplete],[class*=typeahead]'),
    hasFormErrors:        q('[class*=error-msg],[class*=invalid-feedback],[aria-invalid=true]'),

    // ── TABLES / DATA GRID ─────────────────────────────
    hasTables:            q('table,[role=grid],[role=treegrid]'),
    hasSortableColumns:   q('[aria-sort],[class*=sortable],[class*=sort-header]'),
    hasEditableRows:      q('[class*=inline-edit],[data-editable],[class*=row-edit]'),
    hasRowSelection:      q('[class*=row-select],[class*=select-row]'),
    hasFilters:           q('[class*=filter-bar],[class*=filter-panel],input[type=search]'),
    hasPagination:        q('[class*=pagination],[class*=pager],[class*=page-nav]'),
    hasInfiniteScroll:    q('[data-infinite],[class*=infinite-scroll],[class*=load-more]'),
    hasEmptyState:        q('[class*=empty-state],[class*=no-data],[class*=no-results]'),
    hasBulkActions:       q('[class*=bulk-action],[class*=select-all],[class*=mass-action]'),
    hasDataGrid:          q('[class*=ag-grid],[class*=handsontable],[class*=data-grid]'),

    // ── NAVIGATION ─────────────────────────────────────
    hasNavigation:        q('nav,[role=navigation]'),
    hasSidebar:           q('[class*=sidebar],[class*=sidenav],[class*=side-menu],[class*=left-nav]'),
    hasTopNavbar:         q('header nav,[class*=topbar],[class*=navbar],[class*=top-nav]'),
    hasBottomTabBar:      q('[class*=bottom-nav],[class*=tab-bar],[class*=footer-tabs]'),
    hasBreadcrumb:        q('[aria-label*=breadcrumb i],[class*=breadcrumb]'),
    hasTabs:              q('[role=tablist],[role=tab],[class*=tab-nav],[class*=nav-tabs]'),
    hasHamburgerMenu:     q('[class*=hamburger],[class*=menu-toggle],[class*=burger],[aria-label*=menu i]'),
    hasMegaMenu:          q('[class*=mega-menu],[class*=nav-dropdown]'),
    hasBackButton:        q('[class*=btn-back],[aria-label*=go back i],[onclick*=history]'),
    hasStepIndicator:     q('[class*=step-indicator],[class*=progress-steps],[class*=wizard-steps]'),

    // ── MODALS / OVERLAYS / DROPDOWNS ──────────────────
    hasModals:            q('[role=dialog],[class*=modal-dialog],[class*=modal-content]'),
    hasDrawer:            q('[class*=drawer],[class*=offcanvas],[class*=slide-panel]'),
    hasDropdownMenus:     q('[role=listbox],[role=combobox],[class*=dropdown-menu],[class*=select-menu]'),
    hasTooltips:          q('[role=tooltip],[data-tooltip],[data-bs-toggle=tooltip]'),
    hasPopovers:          q('[data-bs-toggle=popover],[class*=popover],[class*=flyout]'),
    hasToastContainer:    q('[class*=toast-container],[class*=snackbar],[class*=notification-stack]'),
    hasAlertBanners:      q('[role=alert],[class*=alert-banner],[class*=inline-message]'),
    hasBottomSheet:       q('[class*=bottom-sheet],[class*=action-sheet]'),
    hasContextMenu:       q('[class*=context-menu],[data-contextmenu]'),
    hasOverlayBackdrop:   q('[class*=backdrop],[class*=overlay-bg]'),

    // ── MEDIA ──────────────────────────────────────────
    hasImages:            q('img,[role=img]'),
    hasLazyImages:        q('img[loading=lazy],[data-src],[data-lazy-src]'),
    hasSrcsetImages:      q('img[srcset],picture source'),
    hasAvatars:           q('[class*=avatar],[class*=profile-img],[class*=user-photo]'),
    hasBrokenImgSrc:      q('img[src=""],[img]:not([src])'),
    hasVideo:             q('video,iframe[src*=youtube],iframe[src*=vimeo],[class*=video-player]'),
    hasAudio:             q('audio,[class*=audio-player]'),
    hasIcons:             q('svg use,i[class*=fa-],i[class*=icon-],[class*=material-icons]', 3),
    hasInlineBgImages:    q('[style*=background-image]'),
    hasThirdPartyIframe:  q('iframe:not([src*=youtube]):not([src*=vimeo])'),

    // ── CHARTS / DATA VIZ ──────────────────────────────
    hasCharts:            q('canvas,[class*=chart],[class*=recharts],[class*=echarts],[class*=apexcharts],[class*=highcharts]'),
    hasProgressBars:      q('[role=progressbar],[class*=progress-bar]'),
    hasGauges:            q('[class*=gauge],[class*=dial],[class*=meter]'),
    hasKPICards:          q('[class*=stat-card],[class*=kpi],[class*=metric-card]'),
    hasMaps:              q('[id*=map],[class*=leaflet],[class*=mapbox],[class*=google-map]'),
    hasSparklines:        q('[class*=sparkline],[class*=mini-chart]'),

    // ── CONTENT BLOCKS / WIDGETS ───────────────────────
    hasCards:             q('[class*=card]:not([class*=card-body]):not([class*=card-header])', 2),
    hasCarousel:          q('[class*=carousel],[class*=swiper],[class*=slick],[class*=splide]'),
    hasAccordion:         q('[class*=accordion],[class*=collapse-item],details,summary'),
    hasTimeline:          q('[class*=timeline],[class*=activity-feed],[class*=audit-log]'),
    hasKanban:            q('[class*=kanban],[class*=task-board],[class*=sprint-board]'),
    hasCalendar:          q('[class*=calendar],[class*=fc-],[class*=fullcalendar]'),
    hasTreeView:          q('[role=tree],[role=treeitem],[class*=treeview],[class*=tree-node]'),
    hasDashboardTiles:    q('[class*=tile-grid],[class*=app-grid],[class*=widget-grid]'),

    // ── INTERACTIVE CONTROLS ───────────────────────────
    hasDragDrop:          q('[draggable=true],[data-dnd],[class*=drag-handle],[class*=sortable-handle]'),
    hasToggleSwitches:    q('[role=switch],[class*=toggle-switch]'),
    hasRangeSlider:       q('input[type=range],[class*=range-slider],[class*=slider-thumb]'),
    hasRatingWidget:      q('[class*=star-rating],[class*=rating-stars]'),
    hasColorPicker:       q('input[type=color],[class*=color-picker]'),
    hasCheckboxGroup:     q('input[type=checkbox]', 2),
    hasRadioGroup:        q('input[type=radio]', 1),
    hasNumberStepper:     q('input[type=number],[class*=qty-input],[class*=stepper-input]'),
    hasHoverElements:     q('[class*=hover-],[data-hover],[class*=hoverable]'),
    hasResizable:         q('[class*=resizable],[data-resize]'),

    // ── LAYOUT PATTERNS ────────────────────────────────
    hasStickyHeader:      (() => { try { const h = document.querySelector('header,nav'); return !!(h && ['sticky','fixed'].includes(getComputedStyle(h).position)); } catch(e){return false;} })(),
    hasStickyElements:    q('[class*=sticky],[class*=affix],[class*=fixed-top]'),
    hasScrollContainers:  q('[class*=scroll-area],[class*=scrollable],[class*=overflow-auto]'),
    hasAnimations:        q('[class*=animate__],[data-aos],[class*=motion-],[class*=animated]'),
    hasTransitions:       q('[class*=fade-in],[class*=slide-in],[class*=transition-]'),
    hasParallax:          q('[data-parallax],[class*=parallax]'),
    hasVirtualScroll:     q('[class*=virtual-scroll],[class*=cdk-virtual]'),
    hasLoadingSpinner:    q('[class*=spinner],[class*=loader],[class*=loading-icon]'),
    hasSkeletonScreen:    q('[class*=skeleton],[class*=shimmer],[class*=placeholder-glow]'),

    // ── CRUD / DATA ACTIONS ────────────────────────────
    hasAddButton:         q('[class*=btn-add],[class*=add-new],[aria-label*=add i],[aria-label*=create i],[title*=add i],[title*=create i],gf-button[title*=add i],gf-button[title*=create i]'),
    hasEditButton:        q('[class*=btn-edit],[class*=edit-action],[aria-label*=edit i],[title*=edit i],[title*=update i],gf-button[title*=edit i],gf-button[title*=update i],[class*=fa-edit],[class*=fa-pencil]'),
    hasDeleteButton:      q('[class*=btn-delete],[class*=delete-action],[aria-label*=delete i],[title*=delete i],[title*=remove i],gf-button[title*=delete i],gf-button[title*=remove i],[class*=fa-trash]'),
    hasExportOption:      re(/export|download csv|export pdf|export report/i),
    hasImportOption:      re(/import|bulk upload|upload file|upload data/i),
    hasPrintOption:       q('[onclick*=print],[class*=btn-print],[aria-label*=print i]'),
    hasCopyButton:        q('[class*=copy-btn],[aria-label*=copy i],[class*=clipboard]'),
    hasBatchOperation:    q('[class*=batch-action],[class*=bulk-edit],[class*=multi-select-action]'),

    // ── AUTH / PERMISSIONS ─────────────────────────────
    hasLoginForm:         !!(document.querySelector('input[type=password]') && document.querySelector('form')),
    hasLogoutOption:      re(/log.?out|sign.?out/i, 3000),
    hasUserMenu:          q('[class*=user-menu],[class*=profile-dropdown],[class*=account-menu]'),
    hasRoleIndicator:     q('[data-role],[class*=role-badge],[class*=permission-tag]'),
    hasRestrictedContent: q('[class*=locked],[class*=restricted],[class*=forbidden]'),
    hasTwoFactor:         re(/two.factor|2fa|otp|verification code/i),

    // ── NOTIFICATIONS / FEEDBACK ───────────────────────
    hasToastMessages:     q('[class*=toast],[class*=snackbar],[class*=notification-toast]'),
    hasInlineAlerts:      q('[role=alert],[class*=alert-success],[class*=alert-error],[class*=alert-warning]'),
    hasProgressIndicator: q('[class*=step-progress],[class*=wizard-progress]'),
    hasNotificationBadge: q('[class*=badge-count],[class*=notification-dot],[class*=unread-badge]'),
    hasConfirmDialog:     q('[class*=confirm-dialog],[class*=confirm-modal]'),

    // ── THEME / I18N / RTL ─────────────────────────────
    hasThemeToggle:       q('[class*=theme-toggle],[aria-label*=dark mode i],[data-theme-switch]'),
    hasDarkModeActive:    document.documentElement.classList.contains('dark') || document.documentElement.getAttribute('data-theme') === 'dark' || document.documentElement.getAttribute('data-bs-theme') === 'dark',
    hasLanguageSwitcher:  q('[class*=lang-switch],[class*=language-select],[aria-label*=language i]'),
    hasRTL:               document.documentElement.dir === 'rtl' || document.body.dir === 'rtl',
    hasI18nAttributes:    q('[data-i18n],[data-translate],[i18n]'),
    hasCurrencySymbols:   re(/[$€£¥₹]/u),

    // ── ACCESSIBILITY SIGNALS ──────────────────────────
    hasSkipLink:          q('[href="#main"],[href="#content"],[class*=skip-nav],[class*=skip-link]'),
    hasARIALandmarks:     q('[role=main],[role=banner],[role=contentinfo]', 1),
    hasLiveRegions:       q('[aria-live],[role=status],[role=log]'),
    hasImgWithoutAlt:     q('img:not([alt]),img[alt=""]'),
    hasMissingLabels:     q('input:not([aria-label]):not([id]):not([title])'),
    hasFocusTrap:         q('[class*=focus-trap],[data-focus-trap]'),

    // ── TOOLBAR / ACTION BAR ───────────────────────────
    hasToolbar:           q('[role=toolbar],[class*=toolbar],[class*=action-bar]'),
    hasActionButtons:     q('[class*=btn-primary],[class*=btn-action],[class*=cta-btn]'),
    hasFloatingAction:    q('[class*=fab],[class*=floating-btn]'),
    hasSplitButton:       q('[class*=split-btn],[class*=button-group],[role=group]'),

    // ── SEARCH ─────────────────────────────────────────
    hasGlobalSearch:      q('[role=search],[class*=global-search],[class*=site-search]'),
    hasSearchResults:     q('[class*=search-results],[class*=search-hits]'),
    hasSearchSuggestions: q('[class*=search-suggest],[class*=autocomplete-list]'),

    // ── WORKFLOW / MULTI-STEP ──────────────────────────
    hasWorkflowProcess:   q('[class*=workflow],[class*=pipeline-step],[class*=approval-flow]'),
    hasWizardFlow:        q('[class*=wizard],[class*=onboarding],[class*=setup-guide]'),
    hasApprovalActions:   re(/approve|reject|submit for review|pending approval/i),
    hasStatusBadges:      q('[class*=status-badge],[class*=state-chip],[class*=tag-status]'),

    // ── CSS / OS-LEVEL SIGNALS ─────────────────────────
    hasCSSVariables:      (getComputedStyle(document.documentElement).getPropertyValue('--primary') !== '' || getComputedStyle(document.documentElement).getPropertyValue('--color-primary') !== ''),
    hasPrefersColorScheme: mm('(prefers-color-scheme: dark)'),
    hasPrefersReducedMotion: mm('(prefers-reduced-motion: reduce)'),
    hasForcedColors:      mm('(forced-colors: active)'),
    hasViewportUnits:     /\b(dvh|dvw|svh|svw|lvh|vw|vh|vmin|vmax)\b/.test(css()),
    hasNotchSafeArea:     /env\(safe-area-inset/i.test(css()),

    // ── PERFORMANCE / DOM COMPLEXITY ───────────────────
    hasLargeDOM:          document.querySelectorAll('*').length > 1500,
    hasManyImages:        document.querySelectorAll('img').length > 20,
    hasManyScripts:       document.querySelectorAll('script[src]').length > 15,
    hasLazyLoading:       q('[loading=lazy],[data-src]'),
    hasThirdPartyEmbeds:  q('iframe[src*=google],iframe[src*=facebook],[class*=embed-widget]'),
    hasManyFonts:         q('link[href*=fonts]', 3),

    // ── META ───────────────────────────────────────────
    pageTitle:    document.title,
    pageUrl:      location.pathname,
    domNodeCount: document.querySelectorAll('*').length,
    viewportWidth:  window.innerWidth,
    viewportHeight: window.innerHeight
  };
}
```
