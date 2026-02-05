---
name: hello-extended
description: Multi-language greetings in 6 languages. Use for non-English greetings or multiple people.
default_enabled: false
brief_description: "Multi-language greetings (es, fr, de, ja, zh)"
triggers:
  keywords: [hello-extended, greet, greeting, hello, bonjour, hola, hallo, konnichiwa, nihao, french, spanish, german, japanese, chinese, multilingual, language]
  verbs: [greet, welcome, say, speak]
  patterns:
    - "say .* in (?:french|spanish|german|japanese|chinese)"
    - "greet .* in (?:es|fr|de|ja|zh)"
    - "\\b(?:bonjour|hola|hallo)\\b"
    - "translate.*greeting"
toolsets:
  - toolsets.hello:HelloExtended
---

<skill-hello-extended>
  <triggers>
    <use>Non-English greetings, multi-person greetings, cultural context</use>
    <skip>Simple English (use built-in greet_user)</skip>
  </triggers>

  <tools>
    <direct>
      <greet_in_language>
        <sig>name:str, language:str</sig>
        <langs>es|fr|de|ja|zh|en</langs>
        <desc>Culturally appropriate greeting</desc>
      </greet_in_language>
      <greet_multiple>
        <sig>names:list[str]</sig>
        <desc>Greet multiple people efficiently</desc>
      </greet_multiple>
    </direct>

    <script name="advanced_greeting.py">
      <features>time-aware, formatted, bulk</features>
      <cmd>script_run hello-extended advanced_greeting.py --json</cmd>
      <opts>
        <opt>--names "Alice,Bob"</opt>
        <opt>--language es|fr|de|ja|zh|en</opt>
        <opt>--format plain|emoji|formal</opt>
        <opt>--time-aware</opt>
      </opts>
    </script>
  </tools>

  <examples>
    <ex case="single-lang">greet_in_language("Alice", "es")</ex>
    <ex case="multi-person">greet_multiple(["Alice", "Bob", "Charlie"])</ex>
    <ex case="advanced">script_run hello-extended advanced_greeting.py --json --names "Alice,Bob" --language es --format emoji</ex>
  </examples>

  <lang-map>
    <l c="es">Spanish: ¡Hola!</l>
    <l c="fr">French: Bonjour!</l>
    <l c="de">German: Hallo!</l>
    <l c="ja">Japanese: こんにちは!</l>
    <l c="zh">Chinese: 你好!</l>
    <l c="en">English: Hello!</l>
  </lang-map>
</skill-hello-extended>
