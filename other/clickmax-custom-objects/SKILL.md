---
name: clickmax-custom-objects
description: Use when the user wants to model, fill, link, filter or clean up CUSTOM OBJECTS (objetos personalizados) in the CRM — entities beyond contacts/opportunities/companies like Imóveis, Veículos, Contratos, Turmas — their records, fields, links (ligações/vínculos), history notes, saved views, bulk changes, or segmenting contacts by linked records.
---

## When this applies

The account keeps things that are not people or deals — properties, cars, contracts, classes, equipment — and wants them as real records with their own fields, linked to contacts, opportunities, companies or each other.

Not this skill:

- an extra attribute OF a contact or card (budget, CPF, source) -> a custom field on that entity, `clickmax-custom-fields`
- a yes/no label on contacts -> a tag, `clickmax-tags`
- deal stages and cards -> `clickmax-pipelines`

Rule of thumb for "object or field?": object when the thing has its OWN identity and fields, can relate to several contacts/cards, or a contact can have several of it. Field when it is one value per contact/card.

## Key assumptions

- the feature may be off for the workspace: a 403 on `mcp__plugin_clickmax_clickmax__custom_objects_list` means "not available here or no access" — say so, do not retry other tools
- everything is resolved by id: object -> `objectId` (`custom_objects_list`), fields -> field `id` (`custom_fields_list` with `objectId`), records -> `recordId` (`custom_object_records_search`), relations -> `relationId`. Never send a field NAME where an id is expected
- every object has ONE title field (text) that names its records; it is the only field the server requires on create
- `apiName` is born from the plural name and NEVER changes; renaming the object keeps it. Field keys are derived too
- objects are never deleted, only archived (records and links kept, new records/links refused); records ARE deleted with no restore
- ownership: users without the "Todos" access only reach records where they are responsible; anything else answers 404 — treat "not found" as "not found or not yours", and never assign someone else on their behalf
- relations are created FROM the object (source). Cardinality is read from the source and decides what a new link does to old ones:
  - `many_to_one` (each record has one target): linking a new target REPLACES the old one
  - `one_to_many` (each target has one record): linking a target that already belongs to another record MOVES it
  - `many_to_many`: just adds
- cardinality cannot change once a relation has links; the ends of a relation never change

## Thought process

1. Modeling request ("quero cadastrar meus imóveis"):
   - `mcp__plugin_clickmax_clickmax__custom_objects_overview` first, to avoid a duplicate object or relation.
   - Propose the object (names, gender, icon, color), the title field, 3-8 starting fields and each relation with its cardinality written as a plain sentence ("cada contrato pertence a 1 contato; um contato pode ter vários contratos"). Confirm, then create.
   - Order: `mcp__plugin_clickmax_clickmax__custom_objects_create` (object + fields) -> `mcp__plugin_clickmax_clickmax__custom_object_relations_create` per relation -> optional saved views.
2. Data request ("cadastre o imóvel da Rua X para a Ana"):
   - Resolve the object, the field ids and the contact; create the record with `values` AND `links` in ONE `mcp__plugin_clickmax_clickmax__custom_object_records_create` (single transaction).
   - Before linking on a "one" side, read the relation cardinality and tell the user when an existing link will be replaced or moved.
3. Question request ("quais imóveis de 3 quartos estão disponíveis?", "quem tem contrato vencendo?"):
   - `mcp__plugin_clickmax_clickmax__custom_object_records_query` with filters; page through `meta` when the user wants the full list.
   - "Which contacts…" questions over objects -> `mcp__plugin_clickmax_clickmax__segments_preview_count` with the `customObject` filter, not a loop over records.
4. Cleanup/mass change -> count with the query first, then `bulk_update` / `bulk_delete` with the same filters; async beyond 200 records.

## Execute guide

- Fields of an object: `mcp__plugin_clickmax_clickmax__custom_fields_list` with `entityType: "objects"` + `objectId`. Add a field later with `mcp__plugin_clickmax_clickmax__custom_fields_create` (same pair; `fieldName` is ignored, labels are unique inside the object).
- Read one record fully: `mcp__plugin_clickmax_clickmax__custom_object_records_get` (values + linked groups with `linkId`). The query rows carry only the fields shown in the list.
- Edit values: `mcp__plugin_clickmax_clickmax__custom_object_records_set_values` (writing the title field renames the record). It is NOT atomic: values are written in order and a failure leaves the earlier ones saved — re-read before reporting. Empty a field with `clear_value`.
- Responsible: `set_responsible` only; restricted users may only take records themselves.
- Links: `mcp__plugin_clickmax_clickmax__custom_object_links_create` pairs are always `{ recordId: <source object record>, targetId: <other side> }`. What a contact/card/record has linked: `mcp__plugin_clickmax_clickmax__custom_object_links_list` (groups as that page shows them, including empty ones = what COULD be linked there).
- Filtering records by what they are linked to: a `relation` item in the object filters, whose JSON carries the other side's filter tree (contact segment filters, opportunity filters, or object filters). Labels (`"g1"`) are fine everywhere, including inside the JSON.
- Notes: `notes_create` writes into the record history; only the author or a manager can edit/delete a note.
- Saved views are shared with the whole workspace; create one only when the user asks for a reusable view.

## Report

- Modeling: one short block per object (singular/plural, title field, fields with types) and one line per relation in plain words with its cardinality.
- Records: show the title and the 2-4 fields the user cares about; cap at 10 rows with `+N more` and the total from `meta`.
- After creating/linking, say what was created, what was linked to what, and any link that was replaced or moved by the cardinality rule.

## Warnings

- Changing the title field re-computes every record title; records with no value in the new field end up with an empty title.
- Deleting a relation deletes all its links; archiving an object hides it from filters and pickers but keeps data.
- Record history and values may include personal data of linked contacts; summarize.
- `search` and `custom_object_records_search` look at the TITLE only; other fields need filters.

## Anti-patterns

- Creating an object for what is just one attribute of a contact (use a custom field).
- Writing values by field name or display label instead of field id.
- Creating a record and then linking in separate calls when one create with `links` would do it atomically.
- Linking on a "one" side without warning that the previous link will be replaced or moved.
- Looping over records to answer "how many contacts have…" instead of a segment count with the `customObject` filter.

---

Clickmax skill revision: `b8294822a4d6`
