---
name: xlsform
description: Authoring data collection forms in Excel for mobile surveys. XLSForm converts Excel files to XForms for ODK, KoBoToolbox, and similar platforms. Use for field surveys, data collection, conditional forms, GPS tracking, and offline data gathering.
---

# XLSForm Skill

## What is XLSForm?

XLSForm is a simple, human-friendly form standard that lets you design data collection forms in Excel. Your forms convert to XForm (XML) and work with mobile platforms like ODK Collect, KoBoToolbox, SurveyCTO, and Enketo. Perfect for surveys, GPS tracking, offline data gathering, and complex conditional logic.

## Five Key Concepts

1. **Survey Sheet** - Lists your questions (type, name, label). One row per question.
2. **Choices Sheet** - Defines answer options for select_one and select_multiple questions.
3. **Question Types** - 20+ types: text, integer, select_one, geopoint, image, date, calculate, and more.
4. **Skip Logic** - The `relevant` column shows/hides questions based on previous answers.
5. **Calculations** - The `calculate` question type and `calculation` column compute derived values.

## Minimal Working Example

**Survey Sheet:**
| type | name | label |
|------|------|-------|
| text | respondent_name | What is your name? |
| integer | age | How old are you? |
| select_one yes_no | consent | Do you agree? |
| calculate | timestamp | now() |

**Choices Sheet:**
| list_name | name | label |
|-----------|------|-------|
| yes_no | yes | Yes |
| yes_no | no | No |

This creates a 3-question form with a hidden timestamp calculation.

## Essential Constraints

| Aspect | Limit | Note |
|--------|-------|------|
| Question name | 255 chars | Alphanumeric + underscore only |
| Label/hint | No hard limit | Practical: keep under 500 chars |
| Choices per list | No hard limit | ~100+ works well |
| Calculation expression | ~2000 chars | Complex expressions may slow form |
| Form size | No hard limit | Very large forms (500+ questions) may be slow |
| Languages | Unlimited | Use label::language, hint::language syntax |

## Core Reference Files

Detailed documentation organized by topic:

**Form Structure:**
- [survey-sheet.md](reference/survey-sheet.md) - Survey worksheet columns and structure
- [choices-sheet.md](reference/choices-sheet.md) - Multiple-choice list structure
- [settings-sheet.md](reference/settings-sheet.md) - Form metadata and settings

**Questions & Types:**
- [question-types.md](reference/question-types.md) - All 20+ question types with examples

**Logic & Calculations:**
- [skip-logic.md](reference/skip-logic.md) - Conditional display with `relevant`
- [calculations.md](reference/calculations.md) - `calculate` type and `calculation` column
- [constraints.md](reference/constraints.md) - Validation rules with `constraint` column
- [xpath-expressions.md](reference/xpath-expressions.md) - XPath functions for expressions

**Advanced Features:**
- [cascading-selects.md](reference/cascading-selects.md) - Dependent choice lists
- [appearances.md](reference/appearances.md) - Widget customization
- [external-data.md](reference/external-data.md) - Load choices from CSV/XML files
- [multilingual.md](reference/multilingual.md) - Multiple language support

**Best Practices & Troubleshooting:**
- [best-practices.md](reference/best-practices.md) - Design patterns and recommendations
- [common-errors.md](reference/common-errors.md) - Error messages and fixes

**Navigation:**
- [TABLE_OF_CONTENTS.md](reference/TABLE_OF_CONTENTS.md) - Find docs by topic, use case, or question type

## Examples

See [examples.md](examples.md) for 6 complete, working XLSForms:
1. **Basic Survey** - Simple questions (text, integer, select_one)
2. **Conditional Logic** - Skip logic with relevant
3. **Calculations & Validation** - Constraints and calculated fields
4. **GPS & Media** - Location tracking and photo capture
5. **Multilingual Form** - Multiple languages
6. **Advanced Features** - Repeat groups, cascading selects, external data

## Common Tasks

### Generate an XLSForm Excel file
When asked to create an XLSForm, output a properly structured Excel file (.xlsx):

**Required worksheets:**
1. **survey** - Question definitions (type, name, label columns required)
2. **choices** - Choice lists for select questions (list_name, name, label required)
3. **settings** - Optional form metadata (form_title, form_id, version)

**Format:**
- Use clear tabular markdown showing each worksheet
- Include all required columns (type, name, label)
- Add optional columns as needed (hint, relevant, constraint, etc.)
- Users can copy tables into Excel, or use `scripts/create_xlsform.py` to generate .xlsx from CSV

**Example output structure:**
```
# survey worksheet
| type | name | label | hint |
|------|------|-------|------|
| ... | ... | ... | ... |

# choices worksheet
| list_name | name | label |
|-----------|------|-------|
| ... | ... | ... |

# settings worksheet (optional)
| form_title | form_id | version |
|------------|---------|---------|
| ... | ... | ... |
```

See [creating-xlsforms.md](reference/creating-xlsforms.md) for detailed instructions on generating forms.

### Create a simple survey
1. Read this quick start and the minimal example above
2. Check [question-types.md](reference/question-types.md) for basic types
3. Look at "Basic Survey" example in [examples.md](examples.md)
4. Use `python scripts/validate_xlsform.py form.xlsx` to check structure

### Add conditional questions
1. Read [skip-logic.md](reference/skip-logic.md)
2. Look at "Conditional Logic" example in [examples.md](examples.md)
3. Use `relevant` column with XPath expressions
4. Examples: `${age} >= 18`, `selected(${previous_answer}, 'option')`

### Add calculations
1. Read [calculations.md](reference/calculations.md)
2. Examples: sum, average, string concatenation, date arithmetic
3. Use `calculate` question type for hidden computed values
4. Use `calculation` column for visible computed fields

### Validate before using
```bash
python scripts/validate_xlsform.py form.xlsx     # Check Excel structure
python scripts/convert_to_xform.py form.xlsx     # Convert and validate XForm output
```

### Deploy to ODK Collect or KoBoToolbox
1. Run validation scripts to ensure no errors
2. Upload .xlsx to platform or convert to .xml first
3. Test on mobile device before deployment
4. Check [best-practices.md](reference/best-practices.md) for field readiness

## Best Practices Summary

**Form Design:**
- Keep labels clear and concise (questions, not statements)
- Test on mobile devices early—forms look different on small screens
- Use hints for clarification, not required instructions
- Order questions logically; use skip logic instead of long forms

**Performance:**
- Avoid complex nested calculations
- Use choice lists instead of free text when possible
- Limit repeat groups to reasonable counts (50+)
- Test on older devices

**Validation:**
- Always run `validate_xlsform.py` before conversion
- Use constraints for user-facing validation, not just data cleaning
- Add `constraint_message` to tell users why an answer is invalid
- Test edge cases: empty inputs, extreme values, rapid skips

**Multilingual Forms:**
- Use `label::English` and `label::French` syntax
- All languages in one cell (one column per language)
- Test right-to-left languages on mobile

See [best-practices.md](reference/best-practices.md) for detailed patterns and recommendations.

## Troubleshooting

**Parse errors when converting?**
- Run `validate_xlsform.py` first—it catches structural issues early
- Check [common-errors.md](reference/common-errors.md) for error-specific solutions
- Ensure question `name` fields are alphanumeric + underscore only

**Form displays wrong on mobile?**
- Check [question-types.md](reference/question-types.md) for type-specific appearances
- Use `appearance` column to customize widgets
- Test on actual mobile device—online converters may not match deployed forms

**Calculations not working?**
- Check [xpath-expressions.md](reference/xpath-expressions.md) for function reference
- Verify referenced question names match exactly (case-sensitive)
- Use `${variable_name}` syntax inside expressions

**Choice lists not showing?**
- Ensure `list_name` in survey matches `list_name` in choices sheet (case-sensitive)
- Run `validate_xlsform.py` to verify all references

See [common-errors.md](reference/common-errors.md) for a comprehensive troubleshooting guide.

## Version Information

XLSForm syntax evolves but maintains backward compatibility. Most forms work across versions 4.0–7.1+. Check [TABLE_OF_CONTENTS.md](reference/TABLE_OF_CONTENTS.md) for version-specific features.

## Getting Help

- **Quick questions?** Check [TABLE_OF_CONTENTS.md](reference/TABLE_OF_CONTENTS.md) to find relevant docs
- **See working examples?** Look at [examples.md](examples.md)
- **Stuck on a feature?** Search [reference/](reference/) by topic
- **Validation scripts not working?** See error message at bottom of script output

## Next Steps

1. **Start simple:** Create a basic form using the minimal example above
2. **Validate:** Run `validate_xlsform.py` to check structure
3. **Learn by example:** Read [examples.md](examples.md) for patterns you need
4. **Go deeper:** Read specific [reference/](reference/) docs for advanced features
5. **Deploy:** Test thoroughly on mobile before using in production
