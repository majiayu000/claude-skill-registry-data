---
name: "Rails Localization (i18n) - English & Arabic"
description: "Comprehensive internationalization skill for Ruby on Rails applications with proper English and Arabic translations, RTL support, pluralization rules, date/time formatting, and culturally appropriate content adaptation."
---

# Rails Localization Skill (English & Arabic)

This skill provides comprehensive guidance for implementing internationalization (i18n) in Ruby on Rails applications with proper support for English and Arabic languages.

## Core Principles

### Arabic Localization is NOT Just Translation

Arabic localization requires cultural and linguistic adaptation, not direct translation:

1. **Right-to-Left (RTL) Layout**: Arabic reads right-to-left
2. **Pluralization**: Arabic has 6 plural forms (zero, one, two, few, many, other)
3. **Gender Agreement**: Arabic nouns and adjectives have grammatical gender
4. **Number Formatting**: Arabic uses Eastern Arabic numerals (٠١٢٣٤٥٦٧٨٩) or Western (0123456789)
5. **Date Formatting**: Hijri calendar support may be needed
6. **Cultural Context**: Greetings, formality levels, and idioms differ significantly

## Project Setup

### 1. Configure Available Locales

```ruby
# config/application.rb
module MyApp
  class Application < Rails::Application
    # Available locales
    config.i18n.available_locales = [:en, :ar]
    
    # Default locale
    config.i18n.default_locale = :en
    
    # Fallback chain
    config.i18n.fallbacks = {
      ar: [:ar, :en],
      en: [:en]
    }
    
    # Load all locale files including nested directories
    config.i18n.load_path += Dir[Rails.root.join('config', 'locales', '**', '*.{rb,yml}')]
  end
end
```

### 2. Locale File Structure

```
config/
└── locales/
    ├── en/
    │   ├── activerecord.en.yml
    │   ├── controllers.en.yml
    │   ├── mailers.en.yml
    │   ├── models.en.yml
    │   └── views.en.yml
    ├── ar/
    │   ├── activerecord.ar.yml
    │   ├── controllers.ar.yml
    │   ├── mailers.ar.yml
    │   ├── models.ar.yml
    │   └── views.ar.yml
    ├── defaults/
    │   ├── en.yml      # Rails defaults, pagination, etc.
    │   └── ar.yml
    └── shared/
        ├── errors.en.yml
        ├── errors.ar.yml
        ├── flash.en.yml
        └── flash.ar.yml
```

### 3. Application Controller Setup

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  around_action :switch_locale

  private

  def switch_locale(&action)
    locale = extract_locale || I18n.default_locale
    I18n.with_locale(locale, &action)
  end

  def extract_locale
    # Priority: URL param > User preference > Cookie > Accept-Language header
    extract_locale_from_param ||
      extract_locale_from_user ||
      extract_locale_from_cookie ||
      extract_locale_from_header
  end

  def extract_locale_from_param
    parsed_locale = params[:locale]
    I18n.available_locales.map(&:to_s).include?(parsed_locale) ? parsed_locale : nil
  end

  def extract_locale_from_user
    current_user&.preferred_locale if user_signed_in?
  end

  def extract_locale_from_cookie
    cookies[:locale] if I18n.available_locales.map(&:to_s).include?(cookies[:locale])
  end

  def extract_locale_from_header
    request.env['HTTP_ACCEPT_LANGUAGE']&.scan(/^[a-z]{2}/)&.first&.then do |locale|
      I18n.available_locales.map(&:to_s).include?(locale) ? locale : nil
    end
  end

  def default_url_options
    { locale: I18n.locale }
  end
end
```

### 4. Route Configuration

```ruby
# config/routes.rb
Rails.application.routes.draw do
  # Locale-scoped routes
  scope "(:locale)", locale: /en|ar/ do
    resources :users
    resources :transactions
    resources :accounts
    
    root "home#index"
  end
  
  # API routes (typically not localized in URL)
  namespace :api do
    namespace :v1 do
      resources :users
    end
  end
  
  # Locale switcher
  get "locale/:locale", to: "locales#switch", as: :switch_locale
end
```

```ruby
# app/controllers/locales_controller.rb
class LocalesController < ApplicationController
  def switch
    locale = params[:locale]
    
    if I18n.available_locales.map(&:to_s).include?(locale)
      cookies[:locale] = { value: locale, expires: 1.year.from_now }
      current_user&.update(preferred_locale: locale) if user_signed_in?
    end
    
    redirect_back(fallback_location: root_path(locale: locale))
  end
end
```

## Locale Files

### Base English Locale

```yaml
# config/locales/defaults/en.yml
en:
  # Direction and language metadata
  direction: ltr
  language_name: "English"
  language_name_native: "English"
  
  # Date and time formats
  date:
    formats:
      default: "%Y-%m-%d"
      short: "%b %d"
      long: "%B %d, %Y"
      month_year: "%B %Y"
      day_month: "%d %B"
    day_names:
      - Sunday
      - Monday
      - Tuesday
      - Wednesday
      - Thursday
      - Friday
      - Saturday
    abbr_day_names:
      - Sun
      - Mon
      - Tue
      - Wed
      - Thu
      - Fri
      - Sat
    month_names:
      - ~
      - January
      - February
      - March
      - April
      - May
      - June
      - July
      - August
      - September
      - October
      - November
      - December
    abbr_month_names:
      - ~
      - Jan
      - Feb
      - Mar
      - Apr
      - May
      - Jun
      - Jul
      - Aug
      - Sep
      - Oct
      - Nov
      - Dec
    order:
      - :year
      - :month
      - :day

  time:
    formats:
      default: "%a, %d %b %Y %H:%M:%S %z"
      short: "%d %b %H:%M"
      long: "%B %d, %Y %H:%M"
      time_only: "%H:%M"
      time_with_zone: "%H:%M %Z"
    am: "AM"
    pm: "PM"

  # Number formats
  number:
    format:
      separator: "."
      delimiter: ","
      precision: 2
      significant: false
      strip_insignificant_zeros: false
    currency:
      format:
        format: "%u%n"
        unit: "$"
        separator: "."
        delimiter: ","
        precision: 2
        significant: false
        strip_insignificant_zeros: false
    percentage:
      format:
        delimiter: ""
        format: "%n%"
    precision:
      format:
        delimiter: ""
    human:
      format:
        delimiter: ""
        precision: 3
        significant: true
        strip_insignificant_zeros: true
      storage_units:
        format: "%n %u"
        units:
          byte:
            one: "Byte"
            other: "Bytes"
          kb: "KB"
          mb: "MB"
          gb: "GB"
          tb: "TB"
          pb: "PB"
      decimal_units:
        format: "%n %u"
        units:
          unit: ""
          thousand: "Thousand"
          million: "Million"
          billion: "Billion"
          trillion: "Trillion"
          quadrillion: "Quadrillion"

  # Distance of time in words
  datetime:
    distance_in_words:
      half_a_minute: "half a minute"
      less_than_x_seconds:
        one: "less than 1 second"
        other: "less than %{count} seconds"
      x_seconds:
        one: "1 second"
        other: "%{count} seconds"
      less_than_x_minutes:
        one: "less than a minute"
        other: "less than %{count} minutes"
      x_minutes:
        one: "1 minute"
        other: "%{count} minutes"
      about_x_hours:
        one: "about 1 hour"
        other: "about %{count} hours"
      x_days:
        one: "1 day"
        other: "%{count} days"
      about_x_months:
        one: "about 1 month"
        other: "about %{count} months"
      x_months:
        one: "1 month"
        other: "%{count} months"
      about_x_years:
        one: "about 1 year"
        other: "about %{count} years"
      over_x_years:
        one: "over 1 year"
        other: "over %{count} years"
      almost_x_years:
        one: "almost 1 year"
        other: "almost %{count} years"
    prompts:
      year: "Year"
      month: "Month"
      day: "Day"
      hour: "Hour"
      minute: "Minute"
      second: "Second"

  # Support
  support:
    array:
      words_connector: ", "
      two_words_connector: " and "
      last_word_connector: ", and "

  # Common UI elements
  common:
    actions:
      save: "Save"
      cancel: "Cancel"
      delete: "Delete"
      edit: "Edit"
      create: "Create"
      update: "Update"
      back: "Back"
      next: "Next"
      previous: "Previous"
      submit: "Submit"
      confirm: "Confirm"
      close: "Close"
      search: "Search"
      filter: "Filter"
      clear: "Clear"
      reset: "Reset"
      download: "Download"
      upload: "Upload"
      export: "Export"
      import: "Import"
      print: "Print"
      refresh: "Refresh"
      view: "View"
      view_all: "View All"
      show_more: "Show More"
      show_less: "Show Less"
      loading: "Loading..."
      processing: "Processing..."
    
    confirmations:
      delete: "Are you sure you want to delete this?"
      unsaved_changes: "You have unsaved changes. Are you sure you want to leave?"
      action_irreversible: "This action cannot be undone."
    
    status:
      active: "Active"
      inactive: "Inactive"
      pending: "Pending"
      approved: "Approved"
      rejected: "Rejected"
      completed: "Completed"
      cancelled: "Cancelled"
      draft: "Draft"
      published: "Published"
      archived: "Archived"
    
    labels:
      yes: "Yes"
      no: "No"
      all: "All"
      none: "None"
      select: "Select"
      select_option: "Select an option"
      optional: "Optional"
      required: "Required"
      not_available: "N/A"
      unknown: "Unknown"
      other: "Other"
    
    messages:
      no_results: "No results found"
      no_data: "No data available"
      error_occurred: "An error occurred"
      try_again: "Please try again"
      success: "Success"
      saved_successfully: "Saved successfully"
      deleted_successfully: "Deleted successfully"
      updated_successfully: "Updated successfully"
      created_successfully: "Created successfully"
    
    pagination:
      first: "First"
      last: "Last"
      previous: "Previous"
      next: "Next"
      showing: "Showing %{from} to %{to} of %{total} entries"
      per_page: "per page"

  # Greetings (time-based)
  greetings:
    morning: "Good morning"
    afternoon: "Good afternoon"
    evening: "Good evening"
    welcome: "Welcome"
    welcome_back: "Welcome back"
    hello: "Hello"
    goodbye: "Goodbye"
    thank_you: "Thank you"
```

### Base Arabic Locale

```yaml
# config/locales/defaults/ar.yml
ar:
  # Direction and language metadata
  direction: rtl
  language_name: "Arabic"
  language_name_native: "العربية"
  
  # Date and time formats
  date:
    formats:
      default: "%Y-%m-%d"
      short: "%d %b"
      long: "%d %B، %Y"
      month_year: "%B %Y"
      day_month: "%d %B"
    day_names:
      - الأحد
      - الاثنين
      - الثلاثاء
      - الأربعاء
      - الخميس
      - الجمعة
      - السبت
    abbr_day_names:
      - أحد
      - اثنين
      - ثلاثاء
      - أربعاء
      - خميس
      - جمعة
      - سبت
    month_names:
      - ~
      - يناير
      - فبراير
      - مارس
      - أبريل
      - مايو
      - يونيو
      - يوليو
      - أغسطس
      - سبتمبر
      - أكتوبر
      - نوفمبر
      - ديسمبر
    abbr_month_names:
      - ~
      - يناير
      - فبراير
      - مارس
      - أبريل
      - مايو
      - يونيو
      - يوليو
      - أغسطس
      - سبتمبر
      - أكتوبر
      - نوفمبر
      - ديسمبر
    order:
      - :day
      - :month
      - :year

  time:
    formats:
      default: "%a، %d %b %Y %H:%M:%S %z"
      short: "%d %b %H:%M"
      long: "%d %B، %Y %H:%M"
      time_only: "%H:%M"
      time_with_zone: "%H:%M %Z"
    am: "ص"
    pm: "م"

  # Number formats (using Western Arabic numerals - common in business)
  # For Eastern Arabic numerals, see the helper section
  number:
    format:
      separator: "٫"
      delimiter: "٬"
      precision: 2
      significant: false
      strip_insignificant_zeros: false
    currency:
      format:
        format: "%n %u"
        unit: "ر.س"
        separator: "٫"
        delimiter: "٬"
        precision: 2
        significant: false
        strip_insignificant_zeros: false
    percentage:
      format:
        delimiter: ""
        format: "%%n"
    precision:
      format:
        delimiter: ""
    human:
      format:
        delimiter: ""
        precision: 3
        significant: true
        strip_insignificant_zeros: true
      storage_units:
        format: "%n %u"
        units:
          byte:
            zero: "بايت"
            one: "بايت"
            two: "بايت"
            few: "بايت"
            many: "بايت"
            other: "بايت"
          kb: "ك.ب"
          mb: "م.ب"
          gb: "ج.ب"
          tb: "ت.ب"
          pb: "ب.ب"
      decimal_units:
        format: "%n %u"
        units:
          unit: ""
          thousand: "ألف"
          million: "مليون"
          billion: "مليار"
          trillion: "تريليون"
          quadrillion: "كوادريليون"

  # Distance of time in words (with Arabic pluralization)
  datetime:
    distance_in_words:
      half_a_minute: "نصف دقيقة"
      less_than_x_seconds:
        zero: "أقل من ثانية"
        one: "أقل من ثانية واحدة"
        two: "أقل من ثانيتين"
        few: "أقل من %{count} ثوانٍ"
        many: "أقل من %{count} ثانية"
        other: "أقل من %{count} ثانية"
      x_seconds:
        zero: "صفر ثوانٍ"
        one: "ثانية واحدة"
        two: "ثانيتان"
        few: "%{count} ثوانٍ"
        many: "%{count} ثانية"
        other: "%{count} ثانية"
      less_than_x_minutes:
        zero: "أقل من دقيقة"
        one: "أقل من دقيقة واحدة"
        two: "أقل من دقيقتين"
        few: "أقل من %{count} دقائق"
        many: "أقل من %{count} دقيقة"
        other: "أقل من %{count} دقيقة"
      x_minutes:
        zero: "صفر دقائق"
        one: "دقيقة واحدة"
        two: "دقيقتان"
        few: "%{count} دقائق"
        many: "%{count} دقيقة"
        other: "%{count} دقيقة"
      about_x_hours:
        zero: "أقل من ساعة"
        one: "حوالي ساعة واحدة"
        two: "حوالي ساعتين"
        few: "حوالي %{count} ساعات"
        many: "حوالي %{count} ساعة"
        other: "حوالي %{count} ساعة"
      x_days:
        zero: "صفر أيام"
        one: "يوم واحد"
        two: "يومان"
        few: "%{count} أيام"
        many: "%{count} يومًا"
        other: "%{count} يوم"
      about_x_months:
        zero: "أقل من شهر"
        one: "حوالي شهر واحد"
        two: "حوالي شهرين"
        few: "حوالي %{count} أشهر"
        many: "حوالي %{count} شهرًا"
        other: "حوالي %{count} شهر"
      x_months:
        zero: "صفر أشهر"
        one: "شهر واحد"
        two: "شهران"
        few: "%{count} أشهر"
        many: "%{count} شهرًا"
        other: "%{count} شهر"
      about_x_years:
        zero: "أقل من سنة"
        one: "حوالي سنة واحدة"
        two: "حوالي سنتين"
        few: "حوالي %{count} سنوات"
        many: "حوالي %{count} سنة"
        other: "حوالي %{count} سنة"
      over_x_years:
        zero: "أقل من سنة"
        one: "أكثر من سنة واحدة"
        two: "أكثر من سنتين"
        few: "أكثر من %{count} سنوات"
        many: "أكثر من %{count} سنة"
        other: "أكثر من %{count} سنة"
      almost_x_years:
        zero: "أقل من سنة"
        one: "ما يقارب سنة واحدة"
        two: "ما يقارب سنتين"
        few: "ما يقارب %{count} سنوات"
        many: "ما يقارب %{count} سنة"
        other: "ما يقارب %{count} سنة"
    prompts:
      year: "السنة"
      month: "الشهر"
      day: "اليوم"
      hour: "الساعة"
      minute: "الدقيقة"
      second: "الثانية"

  # Support
  support:
    array:
      words_connector: "، "
      two_words_connector: " و"
      last_word_connector: "، و"

  # Common UI elements
  common:
    actions:
      save: "حفظ"
      cancel: "إلغاء"
      delete: "حذف"
      edit: "تعديل"
      create: "إنشاء"
      update: "تحديث"
      back: "رجوع"
      next: "التالي"
      previous: "السابق"
      submit: "إرسال"
      confirm: "تأكيد"
      close: "إغلاق"
      search: "بحث"
      filter: "تصفية"
      clear: "مسح"
      reset: "إعادة تعيين"
      download: "تحميل"
      upload: "رفع"
      export: "تصدير"
      import: "استيراد"
      print: "طباعة"
      refresh: "تحديث"
      view: "عرض"
      view_all: "عرض الكل"
      show_more: "عرض المزيد"
      show_less: "عرض أقل"
      loading: "جارٍ التحميل..."
      processing: "جارٍ المعالجة..."
    
    confirmations:
      delete: "هل أنت متأكد من الحذف؟"
      unsaved_changes: "لديك تغييرات غير محفوظة. هل تريد المغادرة؟"
      action_irreversible: "لا يمكن التراجع عن هذا الإجراء."
    
    status:
      active: "نشط"
      inactive: "غير نشط"
      pending: "قيد الانتظار"
      approved: "معتمد"
      rejected: "مرفوض"
      completed: "مكتمل"
      cancelled: "ملغي"
      draft: "مسودة"
      published: "منشور"
      archived: "مؤرشف"
    
    labels:
      yes: "نعم"
      no: "لا"
      all: "الكل"
      none: "لا شيء"
      select: "اختر"
      select_option: "اختر خيارًا"
      optional: "اختياري"
      required: "مطلوب"
      not_available: "غير متوفر"
      unknown: "غير معروف"
      other: "أخرى"
    
    messages:
      no_results: "لا توجد نتائج"
      no_data: "لا توجد بيانات"
      error_occurred: "حدث خطأ"
      try_again: "يرجى المحاولة مرة أخرى"
      success: "نجاح"
      saved_successfully: "تم الحفظ بنجاح"
      deleted_successfully: "تم الحذف بنجاح"
      updated_successfully: "تم التحديث بنجاح"
      created_successfully: "تم الإنشاء بنجاح"
    
    pagination:
      first: "الأولى"
      last: "الأخيرة"
      previous: "السابق"
      next: "التالي"
      showing: "عرض %{from} إلى %{to} من %{total} سجل"
      per_page: "لكل صفحة"

  # Greetings (time-based) - Culturally appropriate Arabic
  greetings:
    morning: "صباح الخير"
    afternoon: "مساء الخير"
    evening: "مساء الخير"
    welcome: "أهلاً وسهلاً"
    welcome_back: "أهلاً بعودتك"
    hello: "مرحبًا"
    goodbye: "مع السلامة"
    thank_you: "شكرًا لك"
```

### ActiveRecord Translations

```yaml
# config/locales/en/activerecord.en.yml
en:
  activerecord:
    models:
      user:
        one: "User"
        other: "Users"
      transaction:
        one: "Transaction"
        other: "Transactions"
      account:
        one: "Account"
        other: "Accounts"
    
    attributes:
      user:
        email: "Email"
        password: "Password"
        password_confirmation: "Password confirmation"
        first_name: "First name"
        last_name: "Last name"
        full_name: "Full name"
        phone_number: "Phone number"
        created_at: "Created at"
        updated_at: "Updated at"
      transaction:
        amount: "Amount"
        description: "Description"
        category: "Category"
        date: "Date"
        status: "Status"
      account:
        name: "Name"
        balance: "Balance"
        currency: "Currency"
        account_number: "Account number"
    
    errors:
      models:
        user:
          attributes:
            email:
              taken: "is already registered"
              invalid: "is not a valid email address"
            password:
              too_short: "must be at least %{count} characters"
      messages:
        record_invalid: "Validation failed: %{errors}"
        restrict_dependent_destroy:
          has_one: "Cannot delete record because dependent %{record} exists"
          has_many: "Cannot delete record because dependent %{record} exist"
        required: "must exist"
        taken: "has already been taken"
        blank: "can't be blank"
        present: "must be blank"
        too_long:
          one: "is too long (maximum is 1 character)"
          other: "is too long (maximum is %{count} characters)"
        too_short:
          one: "is too short (minimum is 1 character)"
          other: "is too short (minimum is %{count} characters)"
        wrong_length:
          one: "is the wrong length (should be 1 character)"
          other: "is the wrong length (should be %{count} characters)"
        not_a_number: "is not a number"
        not_an_integer: "must be an integer"
        greater_than: "must be greater than %{count}"
        greater_than_or_equal_to: "must be greater than or equal to %{count}"
        equal_to: "must be equal to %{count}"
        less_than: "must be less than %{count}"
        less_than_or_equal_to: "must be less than or equal to %{count}"
        other_than: "must be other than %{count}"
        odd: "must be odd"
        even: "must be even"
        invalid: "is invalid"
        confirmation: "doesn't match %{attribute}"
        accepted: "must be accepted"
        empty: "can't be empty"
        inclusion: "is not included in the list"
        exclusion: "is reserved"
        not_saved:
          one: "1 error prohibited this %{resource} from being saved:"
          other: "%{count} errors prohibited this %{resource} from being saved:"
```

```yaml
# config/locales/ar/activerecord.ar.yml
ar:
  activerecord:
    models:
      user:
        zero: "مستخدمين"
        one: "مستخدم"
        two: "مستخدمان"
        few: "مستخدمين"
        many: "مستخدمًا"
        other: "مستخدم"
      transaction:
        zero: "معاملات"
        one: "معاملة"
        two: "معاملتان"
        few: "معاملات"
        many: "معاملة"
        other: "معاملة"
      account:
        zero: "حسابات"
        one: "حساب"
        two: "حسابان"
        few: "حسابات"
        many: "حسابًا"
        other: "حساب"
    
    attributes:
      user:
        email: "البريد الإلكتروني"
        password: "كلمة المرور"
        password_confirmation: "تأكيد كلمة المرور"
        first_name: "الاسم الأول"
        last_name: "اسم العائلة"
        full_name: "الاسم الكامل"
        phone_number: "رقم الهاتف"
        created_at: "تاريخ الإنشاء"
        updated_at: "تاريخ التحديث"
      transaction:
        amount: "المبلغ"
        description: "الوصف"
        category: "الفئة"
        date: "التاريخ"
        status: "الحالة"
      account:
        name: "الاسم"
        balance: "الرصيد"
        currency: "العملة"
        account_number: "رقم الحساب"
    
    errors:
      models:
        user:
          attributes:
            email:
              taken: "مسجّل مسبقًا"
              invalid: "غير صالح"
            password:
              too_short: "يجب أن تكون %{count} أحرف على الأقل"
      messages:
        record_invalid: "فشل التحقق: %{errors}"
        restrict_dependent_destroy:
          has_one: "لا يمكن حذف السجل لوجود %{record} مرتبط"
          has_many: "لا يمكن حذف السجل لوجود %{record} مرتبطة"
        required: "مطلوب"
        taken: "محجوز مسبقًا"
        blank: "لا يمكن أن يكون فارغًا"
        present: "يجب أن يكون فارغًا"
        too_long:
          zero: "طويل جدًا (الحد الأقصى صفر أحرف)"
          one: "طويل جدًا (الحد الأقصى حرف واحد)"
          two: "طويل جدًا (الحد الأقصى حرفان)"
          few: "طويل جدًا (الحد الأقصى %{count} أحرف)"
          many: "طويل جدًا (الحد الأقصى %{count} حرفًا)"
          other: "طويل جدًا (الحد الأقصى %{count} حرف)"
        too_short:
          zero: "قصير جدًا (الحد الأدنى صفر أحرف)"
          one: "قصير جدًا (الحد الأدنى حرف واحد)"
          two: "قصير جدًا (الحد الأدنى حرفان)"
          few: "قصير جدًا (الحد الأدنى %{count} أحرف)"
          many: "قصير جدًا (الحد الأدنى %{count} حرفًا)"
          other: "قصير جدًا (الحد الأدنى %{count} حرف)"
        wrong_length:
          zero: "الطول غير صحيح (يجب أن يكون صفر أحرف)"
          one: "الطول غير صحيح (يجب أن يكون حرفًا واحدًا)"
          two: "الطول غير صحيح (يجب أن يكون حرفين)"
          few: "الطول غير صحيح (يجب أن يكون %{count} أحرف)"
          many: "الطول غير صحيح (يجب أن يكون %{count} حرفًا)"
          other: "الطول غير صحيح (يجب أن يكون %{count} حرف)"
        not_a_number: "ليس رقمًا"
        not_an_integer: "يجب أن يكون عددًا صحيحًا"
        greater_than: "يجب أن يكون أكبر من %{count}"
        greater_than_or_equal_to: "يجب أن يكون أكبر من أو يساوي %{count}"
        equal_to: "يجب أن يساوي %{count}"
        less_than: "يجب أن يكون أقل من %{count}"
        less_than_or_equal_to: "يجب أن يكون أقل من أو يساوي %{count}"
        other_than: "يجب أن يكون مختلفًا عن %{count}"
        odd: "يجب أن يكون فرديًا"
        even: "يجب أن يكون زوجيًا"
        invalid: "غير صالح"
        confirmation: "غير مطابق لـ %{attribute}"
        accepted: "يجب قبوله"
        empty: "لا يمكن أن يكون فارغًا"
        inclusion: "غير مدرج في القائمة"
        exclusion: "محجوز"
        not_saved:
          zero: "لم يتم الحفظ:"
          one: "خطأ واحد منع حفظ %{resource}:"
          two: "خطآن منعا حفظ %{resource}:"
          few: "%{count} أخطاء منعت حفظ %{resource}:"
          many: "%{count} خطأً منع حفظ %{resource}:"
          other: "%{count} خطأ منع حفظ %{resource}:"
```

## Helper Methods

### Localization Helper

```ruby
# app/helpers/localization_helper.rb
module LocalizationHelper
  # Direction helper for RTL/LTR
  def text_direction
    I18n.t('direction', default: 'ltr')
  end

  def rtl?
    text_direction == 'rtl'
  end

  def ltr?
    text_direction == 'ltr'
  end

  # CSS class for direction
  def direction_class
    rtl? ? 'rtl' : 'ltr'
  end

  # Opposite direction (for certain UI elements)
  def opposite_direction
    rtl? ? 'ltr' : 'rtl'
  end

  # Locale-aware text alignment
  def start_align
    rtl? ? 'right' : 'left'
  end

  def end_align
    rtl? ? 'left' : 'right'
  end

  # Eastern Arabic numerals conversion
  EASTERN_ARABIC_NUMERALS = {
    '0' => '٠', '1' => '١', '2' => '٢', '3' => '٣', '4' => '٤',
    '5' => '٥', '6' => '٦', '7' => '٧', '8' => '٨', '9' => '٩'
  }.freeze

  def to_eastern_arabic(number)
    number.to_s.gsub(/[0-9]/, EASTERN_ARABIC_NUMERALS)
  end

  def to_western_arabic(number)
    number.to_s.gsub(/[٠-٩]/, EASTERN_ARABIC_NUMERALS.invert)
  end

  # Locale-aware number display
  def localized_number(number, eastern_arabic: false)
    formatted = number_with_delimiter(number)
    eastern_arabic && I18n.locale == :ar ? to_eastern_arabic(formatted) : formatted
  end

  # Time-based greeting
  def greeting
    hour = Time.current.hour
    key = case hour
          when 5..11 then 'greetings.morning'
          when 12..16 then 'greetings.afternoon'
          else 'greetings.evening'
          end
    I18n.t(key)
  end

  # Personalized greeting with name
  def greeting_with_name(name)
    "#{greeting}، #{name}" if I18n.locale == :ar
    "#{greeting}, #{name}"
  end

  # Language switcher links
  def locale_switch_links
    I18n.available_locales.map do |locale|
      next if locale == I18n.locale
      
      link_to(
        I18n.t('language_name_native', locale: locale),
        switch_locale_path(locale: locale),
        class: 'locale-switch',
        data: { locale: locale }
      )
    end.compact.join(' | ').html_safe
  end

  # Format currency with locale awareness
  def localized_currency(amount, currency: nil)
    currency ||= current_currency
    
    options = {
      unit: currency_unit(currency),
      format: I18n.t('number.currency.format.format'),
      separator: I18n.t('number.currency.format.separator'),
      delimiter: I18n.t('number.currency.format.delimiter')
    }
    
    number_to_currency(amount, options)
  end

  # Saudi Riyal specific formatting
  def format_sar(amount, show_halalas: true)
    precision = show_halalas ? 2 : 0
    formatted = number_with_precision(amount, precision: precision)
    
    if I18n.locale == :ar
      "#{formatted} ر.س"
    else
      "SAR #{formatted}"
    end
  end

  # Currency units mapping
  def currency_unit(currency)
    {
      'SAR' => I18n.locale == :ar ? 'ر.س' : 'SAR',
      'USD' => I18n.locale == :ar ? '$' : '$',
      'EUR' => I18n.locale == :ar ? '€' : '€',
      'GBP' => I18n.locale == :ar ? '£' : '£',
      'AED' => I18n.locale == :ar ? 'د.إ' : 'AED'
    }[currency.to_s.upcase] || currency
  end

  private

  def current_currency
    # Override this based on your app's logic
    'SAR'
  end
end
```

### Arabic-Specific Helper

```ruby
# app/helpers/arabic_helper.rb
module ArabicHelper
  # Arabic pluralization helper for custom cases
  # Arabic has: zero, one, two, few (3-10), many (11-99), other (100+)
  def arabic_pluralize(count, singular, dual, plural_few, plural_many, plural_other = nil)
    return I18n.locale == :ar ? singular : singular unless count

    plural_other ||= plural_many

    case count
    when 0
      singular
    when 1
      singular
    when 2
      dual
    when 3..10
      "#{count} #{plural_few}"
    when 11..99
      "#{count} #{plural_many}"
    else
      "#{count} #{plural_other}"
    end
  end

  # Common Arabic plural forms
  def items_count(count)
    arabic_pluralize(
      count,
      I18n.t('common.items.zero'),
      I18n.t('common.items.one'),
      I18n.t('common.items.two'),
      I18n.t('common.items.few'),
      I18n.t('common.items.many')
    )
  end

  # Gender-aware translation
  # Usage: gender_t('welcome_message', gender: user.gender)
  def gender_t(key, gender:, **options)
    gendered_key = "#{key}.#{gender == 'female' ? 'female' : 'male'}"
    
    if I18n.exists?(gendered_key)
      I18n.t(gendered_key, **options)
    else
      I18n.t(key, **options)
    end
  end

  # Hijri date display (requires hijri gem or custom implementation)
  def hijri_date(date, format: :default)
    return unless date
    
    # Using the hijri gem if available
    if defined?(Hijri)
      hijri = Hijri::Date.new(date.year, date.month, date.day)
      format_hijri_date(hijri, format)
    else
      # Fallback: just show Gregorian
      I18n.l(date, format: format)
    end
  end

  # Format phone number for Saudi Arabia
  def format_saudi_phone(phone)
    return phone unless phone.present?
    
    # Remove non-digits
    digits = phone.gsub(/\D/, '')
    
    # Format: +966 XX XXX XXXX
    if digits.start_with?('966')
      "+966 #{digits[3..4]} #{digits[5..7]} #{digits[8..11]}"
    elsif digits.start_with?('0')
      "+966 #{digits[1..2]} #{digits[3..5]} #{digits[6..9]}"
    else
      phone
    end
  end

  # Arabic-aware truncation (doesn't break in middle of word)
  def arabic_truncate(text, length: 100, separator: ' ', omission: '...')
    return '' unless text
    
    if I18n.locale == :ar
      # Arabic omission
      omission = '...'
    end
    
    truncate(text, length: length, separator: separator, omission: omission)
  end

  # Wrap Arabic text in proper direction span
  def bidi_text(text, direction: nil)
    direction ||= detect_direction(text)
    content_tag(:span, text, dir: direction)
  end

  private

  def detect_direction(text)
    return 'ltr' unless text
    
    # Check if first letter is Arabic
    text.match?(/[\u0600-\u06FF]/) ? 'rtl' : 'ltr'
  end

  def format_hijri_date(hijri, format)
    # Custom Hijri date formatting
    case format
    when :short
      "#{hijri.day}/#{hijri.month}/#{hijri.year}"
    when :long
      month_names = %w[محرم صفر ربيع\ الأول ربيع\ الثاني جمادى\ الأولى جمادى\ الآخرة رجب شعبان رمضان شوال ذو\ القعدة ذو\ الحجة]
      "#{hijri.day} #{month_names[hijri.month - 1]} #{hijri.year} هـ"
    else
      "#{hijri.day}/#{hijri.month}/#{hijri.year} هـ"
    end
  end
end
```

## View Components

### Layout with RTL Support

```erb
<%# app/views/layouts/application.html.erb %>
<!DOCTYPE html>
<html lang="<%= I18n.locale %>" dir="<%= text_direction %>">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title><%= yield(:title) || t('app.name') %></title>
  
  <%# Load RTL stylesheet when needed %>
  <%= stylesheet_link_tag "application", "data-turbo-track": "reload" %>
  <% if rtl? %>
    <%= stylesheet_link_tag "rtl", "data-turbo-track": "reload" %>
  <% end %>
  
  <%= javascript_importmap_tags %>
</head>
<body class="<%= direction_class %>" data-locale="<%= I18n.locale %>">
  <%= render 'shared/header' %>
  
  <main class="container">
    <%= render 'shared/flash_messages' %>
    <%= yield %>
  </main>
  
  <%= render 'shared/footer' %>
</body>
</html>
```

### Language Switcher Component

```erb
<%# app/views/shared/_language_switcher.html.erb %>
<div class="language-switcher" data-controller="language-switcher">
  <button type="button" 
          class="language-button"
          data-action="click->language-switcher#toggle"
          aria-expanded="false"
          aria-haspopup="true">
    <span class="current-language">
      <%= I18n.t('language_name_native') %>
    </span>
    <svg class="icon" aria-hidden="true"><!-- dropdown icon --></svg>
  </button>
  
  <ul class="language-menu hidden" role="menu">
    <% I18n.available_locales.each do |locale| %>
      <li role="menuitem">
        <%= link_to switch_locale_path(locale: locale),
                    class: "language-option #{'active' if I18n.locale == locale}",
                    data: { locale: locale } do %>
          <span dir="<%= locale == :ar ? 'rtl' : 'ltr' %>">
            <%= I18n.t('language_name_native', locale: locale) %>
          </span>
          <span class="language-name-english">
            (<%= I18n.t('language_name', locale: locale) %>)
          </span>
        <% end %>
      </li>
    <% end %>
  </ul>
</div>
```

### Bidirectional Form Example

```erb
<%# app/views/users/_form.html.erb %>
<%= form_with model: @user, class: "form #{direction_class}" do |f| %>
  <% if @user.errors.any? %>
    <div class="error-summary" role="alert">
      <h3><%= t('activerecord.errors.messages.not_saved', 
                 count: @user.errors.count, 
                 resource: t('activerecord.models.user.one')) %></h3>
      <ul>
        <% @user.errors.full_messages.each do |message| %>
          <li><%= message %></li>
        <% end %>
      </ul>
    </div>
  <% end %>

  <div class="form-group">
    <%= f.label :email, class: 'form-label' %>
    <%= f.email_field :email, 
                      class: 'form-input',
                      dir: 'ltr',  # Email always LTR
                      placeholder: t('placeholders.email'),
                      required: true %>
  </div>

  <div class="form-group">
    <%= f.label :first_name, class: 'form-label' %>
    <%= f.text_field :first_name, 
                     class: 'form-input',
                     dir: 'auto',  # Auto-detect direction
                     required: true %>
  </div>

  <div class="form-group">
    <%= f.label :last_name, class: 'form-label' %>
    <%= f.text_field :last_name, 
                     class: 'form-input',
                     dir: 'auto',
                     required: true %>
  </div>

  <div class="form-group">
    <%= f.label :phone_number, class: 'form-label' %>
    <%= f.telephone_field :phone_number, 
                          class: 'form-input',
                          dir: 'ltr',  # Phone numbers always LTR
                          placeholder: '+966 5X XXX XXXX' %>
  </div>

  <div class="form-group">
    <%= f.label :bio, class: 'form-label' %>
    <%= f.text_area :bio, 
                    class: 'form-input',
                    dir: 'auto',
                    rows: 4 %>
  </div>

  <div class="form-actions">
    <%= f.submit t('common.actions.save'), class: 'btn btn-primary' %>
    <%= link_to t('common.actions.cancel'), users_path, class: 'btn btn-secondary' %>
  </div>
<% end %>
```

## CSS for RTL Support

```css
/* app/assets/stylesheets/rtl.css */

/* Base RTL styles */
[dir="rtl"] {
  text-align: right;
}

/* Flip flexbox and grid directions */
[dir="rtl"] .flex-row {
  flex-direction: row-reverse;
}

[dir="rtl"] .grid {
  direction: rtl;
}

/* Form alignment */
[dir="rtl"] .form-label {
  text-align: right;
}

[dir="rtl"] .form-input {
  text-align: right;
}

/* Keep certain inputs LTR */
[dir="rtl"] input[type="email"],
[dir="rtl"] input[type="url"],
[dir="rtl"] input[type="tel"],
[dir="rtl"] input[type="number"],
[dir="rtl"] input[dir="ltr"] {
  direction: ltr;
  text-align: left;
}

/* Navigation */
[dir="rtl"] .nav {
  flex-direction: row-reverse;
}

[dir="rtl"] .nav-item {
  margin-left: 0;
  margin-right: 1rem;
}

/* Buttons with icons */
[dir="rtl"] .btn-icon-start {
  flex-direction: row-reverse;
}

[dir="rtl"] .btn-icon-start svg {
  margin-left: 0.5rem;
  margin-right: 0;
}

/* Tables */
[dir="rtl"] table {
  direction: rtl;
}

[dir="rtl"] th,
[dir="rtl"] td {
  text-align: right;
}

/* Numbers in tables stay LTR for readability */
[dir="rtl"] .numeric,
[dir="rtl"] .currency,
[dir="rtl"] .date {
  direction: ltr;
  text-align: left;
}

/* Pagination */
[dir="rtl"] .pagination {
  flex-direction: row-reverse;
}

/* Sidebar */
[dir="rtl"] .sidebar {
  right: 0;
  left: auto;
  border-left: 1px solid var(--border-color);
  border-right: none;
}

/* Dropdowns */
[dir="rtl"] .dropdown-menu {
  right: 0;
  left: auto;
  text-align: right;
}

/* Modals */
[dir="rtl"] .modal-close {
  right: auto;
  left: 1rem;
}

/* Icons that should flip */
[dir="rtl"] .icon-arrow-left {
  transform: scaleX(-1);
}

[dir="rtl"] .icon-arrow-right {
  transform: scaleX(-1);
}

/* Margins and paddings - use logical properties */
.container {
  margin-inline-start: auto;
  margin-inline-end: auto;
  padding-inline-start: 1rem;
  padding-inline-end: 1rem;
}

/* Border radius for RTL */
[dir="rtl"] .rounded-start {
  border-radius: 0 0.25rem 0.25rem 0;
}

[dir="rtl"] .rounded-end {
  border-radius: 0.25rem 0 0 0.25rem;
}
```

```css
/* Tailwind RTL support with logical properties */
/* app/assets/stylesheets/tailwind-rtl.css */

/* Use with Tailwind - these utilities support both directions */
.ms-auto { margin-inline-start: auto; }
.me-auto { margin-inline-end: auto; }
.ms-0 { margin-inline-start: 0; }
.me-0 { margin-inline-end: 0; }
.ms-1 { margin-inline-start: 0.25rem; }
.me-1 { margin-inline-end: 0.25rem; }
.ms-2 { margin-inline-start: 0.5rem; }
.me-2 { margin-inline-end: 0.5rem; }
.ms-4 { margin-inline-start: 1rem; }
.me-4 { margin-inline-end: 1rem; }

.ps-0 { padding-inline-start: 0; }
.pe-0 { padding-inline-end: 0; }
.ps-1 { padding-inline-start: 0.25rem; }
.pe-1 { padding-inline-end: 0.25rem; }
.ps-2 { padding-inline-start: 0.5rem; }
.pe-2 { padding-inline-end: 0.5rem; }
.ps-4 { padding-inline-start: 1rem; }
.pe-4 { padding-inline-end: 1rem; }

.start-0 { inset-inline-start: 0; }
.end-0 { inset-inline-end: 0; }

.text-start { text-align: start; }
.text-end { text-align: end; }

.border-s { border-inline-start-width: 1px; }
.border-e { border-inline-end-width: 1px; }

.rounded-s { border-start-start-radius: 0.25rem; border-end-start-radius: 0.25rem; }
.rounded-e { border-start-end-radius: 0.25rem; border-end-end-radius: 0.25rem; }
```

## Testing Localization

```ruby
# spec/support/i18n_helpers.rb
module I18nHelpers
  def with_locale(locale, &block)
    original_locale = I18n.locale
    I18n.locale = locale
    yield
  ensure
    I18n.locale = original_locale
  end

  def t(key, **options)
    I18n.t(key, **options)
  end

  def l(object, **options)
    I18n.l(object, **options)
  end
end

RSpec.configure do |config|
  config.include I18nHelpers
end
```

```ruby
# spec/helpers/localization_helper_spec.rb
require 'rails_helper'

RSpec.describe LocalizationHelper, type: :helper do
  describe '#text_direction' do
    it 'returns ltr for English' do
      with_locale(:en) do
        expect(helper.text_direction).to eq('ltr')
      end
    end

    it 'returns rtl for Arabic' do
      with_locale(:ar) do
        expect(helper.text_direction).to eq('rtl')
      end
    end
  end

  describe '#to_eastern_arabic' do
    it 'converts Western to Eastern Arabic numerals' do
      expect(helper.to_eastern_arabic('123')).to eq('١٢٣')
      expect(helper.to_eastern_arabic('0')).to eq('٠')
      expect(helper.to_eastern_arabic('9876543210')).to eq('٩٨٧٦٥٤٣٢١٠')
    end
  end

  describe '#localized_currency' do
    it 'formats currency for English locale' do
      with_locale(:en) do
        expect(helper.localized_currency(1000, currency: 'SAR')).to include('SAR')
      end
    end

    it 'formats currency for Arabic locale' do
      with_locale(:ar) do
        expect(helper.localized_currency(1000, currency: 'SAR')).to include('ر.س')
      end
    end
  end
end
```

```ruby
# spec/i18n_spec.rb
require 'rails_helper'

RSpec.describe 'I18n' do
  describe 'locale files' do
    it 'has all required locales' do
      expect(I18n.available_locales).to contain_exactly(:en, :ar)
    end

    it 'has no missing translations for English' do
      I18n.with_locale(:en) do
        expect { I18n.t('common.actions.save', raise: true) }.not_to raise_error
        expect { I18n.t('activerecord.models.user.one', raise: true) }.not_to raise_error
      end
    end

    it 'has no missing translations for Arabic' do
      I18n.with_locale(:ar) do
        expect { I18n.t('common.actions.save', raise: true) }.not_to raise_error
        expect { I18n.t('activerecord.models.user.one', raise: true) }.not_to raise_error
      end
    end
  end

  describe 'Arabic pluralization' do
    it 'handles all plural forms' do
      I18n.with_locale(:ar) do
        expect(I18n.t('datetime.distance_in_words.x_days', count: 0)).to include('صفر')
        expect(I18n.t('datetime.distance_in_words.x_days', count: 1)).to include('يوم واحد')
        expect(I18n.t('datetime.distance_in_words.x_days', count: 2)).to include('يومان')
        expect(I18n.t('datetime.distance_in_words.x_days', count: 5)).to include('أيام')
        expect(I18n.t('datetime.distance_in_words.x_days', count: 20)).to include('يومًا')
        expect(I18n.t('datetime.distance_in_words.x_days', count: 100)).to include('يوم')
      end
    end
  end

  describe 'date formatting' do
    let(:date) { Date.new(2024, 1, 15) }

    it 'formats dates in English' do
      I18n.with_locale(:en) do
        expect(I18n.l(date, format: :long)).to eq('January 15, 2024')
      end
    end

    it 'formats dates in Arabic' do
      I18n.with_locale(:ar) do
        expect(I18n.l(date, format: :long)).to include('يناير')
      end
    end
  end
end
```

```ruby
# spec/system/localization_spec.rb
require 'rails_helper'

RSpec.describe 'Localization', type: :system do
  describe 'language switching' do
    it 'switches to Arabic' do
      visit root_path

      click_link 'العربية'

      expect(page).to have_css('html[dir="rtl"]')
      expect(page).to have_css('html[lang="ar"]')
    end

    it 'persists locale preference' do
      visit root_path(locale: :ar)
      
      visit users_path
      
      expect(page).to have_css('html[lang="ar"]')
    end
  end

  describe 'RTL layout' do
    before { visit root_path(locale: :ar) }

    it 'applies RTL direction to body' do
      expect(page).to have_css('body.rtl')
    end

    it 'displays Arabic content' do
      expect(page).to have_content('أهلاً وسهلاً')
    end
  end

  describe 'form localization' do
    it 'displays localized labels and errors' do
      visit new_user_path(locale: :ar)

      click_button 'إرسال'

      expect(page).to have_content('لا يمكن أن يكون فارغًا')
    end
  end
end
```

## Common Pitfalls & Best Practices

### Pitfalls to Avoid

1. **Direct Translation**: Never use Google Translate or similar for production translations. Hire native Arabic speakers.

2. **Ignoring Pluralization**: Arabic has 6 plural forms. Always provide all forms:
   ```yaml
   # Wrong
   items:
     one: "item"
     other: "items"
   
   # Correct for Arabic
   items:
     zero: "عناصر"
     one: "عنصر"
     two: "عنصران"
     few: "عناصر"
     many: "عنصرًا"
     other: "عنصر"
   ```

3. **Hardcoded Strings**: Never hardcode user-facing strings.
   ```ruby
   # Wrong
   flash[:notice] = "User created successfully"
   
   # Correct
   flash[:notice] = t('users.created_successfully')
   ```

4. **Assuming LTR Layout**: Always use CSS logical properties.
   ```css
   /* Wrong */
   margin-left: 1rem;
   
   /* Correct */
   margin-inline-start: 1rem;
   ```

5. **Breaking Numbers in RTL**: Keep numbers, dates, and technical content LTR.
   ```erb
   <%# Wrong - numbers will display incorrectly %>
   <span><%= amount %></span>
   
   <%# Correct %>
   <span dir="ltr"><%= amount %></span>
   ```

### Best Practices

1. **Use Lazy Lookup**: Let Rails find translations automatically.
   ```erb
   <%# In app/views/users/show.html.erb %>
   <%= t('.welcome_message') %>
   <%# Looks for: en.users.show.welcome_message %>
   ```

2. **Namespace Translations**: Organize by feature, not by language structure.
   ```yaml
   en:
     users:
       index:
         title: "Users"
       show:
         title: "User Details"
   ```

3. **Use Interpolation**: Don't concatenate strings.
   ```ruby
   # Wrong
   "Hello " + name
   
   # Correct
   t('greetings.hello_name', name: name)
   ```

4. **Test Both Languages**: Include locale tests in your test suite.

5. **Document Cultural Differences**: Maintain a guide for translators explaining context.

## Resources

- [Rails I18n Guide](https://guides.rubyonrails.org/i18n.html)
- [Unicode CLDR Plural Rules](https://cldr.unicode.org/index/cldr-spec/plural-rules)
- [Arabic Localization Best Practices](https://www.w3.org/International/articles/article-text-size)
- [RTL Styling Guide](https://rtlstyling.com/)
