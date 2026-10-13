---
name: law-generate
description: >
  Generates machine_readable execution logic for Dutch law YAML files: writes the
  machine_readable sections, validates against the schema, and (when a shell is
  available) runs the BDD suites until the model is correct. Use this skill
  proactively when: editing or creating machine_readable sections in law YAML
  files, working with corpus regulation files, or when user mentions 'generate',
  'machine_readable', or wants to make a law executable. Activate automatically
  when user discusses law YAML files that need executable logic.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
user-invocable: true
---

# Law Generate

Writes `machine_readable` sections for Dutch law YAML files against
`schema/latest/schema.json`. The schema is the single source of truth and
`just validate` is the arbiter. When in doubt, read the schema.

## Text before intent

**The specification describes what the legal text says, not what the legislature
meant.** You translate the words in the `text` field of the entry you are
working on. Nothing else.

The mistake comes from reading the article well. You will see which outcome is
evidently intended, and model the shortest route to that outcome. That route is
almost always simpler than the text, and it is almost always wrong: it drops a
condition the text states, or supplies one the text does not, and the model then
produces the right answer for the wrong reason until a case arrives where the
intent and the text part ways.

So no shortcuts and no repair of a provision that reads badly. When faithfulness
to the text yields something other than what was evidently intended, that is the
correct result, and one this corpus is meant to make visible. Record it and move
on. Where the text genuinely cannot be followed, say so with a marking or an open
term, both described below, and never by quietly modelling the intent instead.

## Setup

1. Read the target law YAML file.
2. Read `reference.md` (schema shapes) and `examples.md` (worked patterns) in
   this skill directory.
3. Count the entries. Over 20, work in batches of roughly 15. This does not
   apply when the prompt names the entries: then that list is the batch.

Do not read another corpus law as a template. The existing corpus predates
several of the rules below and copying its habits reproduces its defects;
`examples.md` has the patterns that are current.

## The entries you were given

**When the prompt names entry numbers, that list is your entire scope.** Leave
every entry outside it untouched, including one that plainly needs work.

The length of the list says which kind of run this is, and the two ask different
things of you.

**Several entries is a window of a walk through the law.** A run before this one
took the entries above and a run after it takes the ones below. Covering the
window is the assignment: every entry in the list is answered, with a model, a
marking, an open term or a declaration, and none is passed over. The worker
measures progress inside the window and rejects a run that shows none.

**One entry is targeted work, and there is no walk.** No later run picks up the
rest, and the entry was named because something specific is wanted from it: an
article a waiting root needs, an article whose open term a newly harvested
regulation now fills, or an entry that came back wrong. Coverage of the law is
not the assignment here. Judge what the entry needs from the entry, report on it
alone, and do not list what other entries still lack: that reads as work someone
forgot rather than work nobody asked for.

## Scope

Each `machine_readable` interprets ONLY the text of its own entry.

**Do not pull anything in.** No conditions from other articles, no hardcoded
values that another provision sets, no "obvious" requirement the text does not
mention, no merging of two leden the text keeps apart. If article 2 grants an
entitlement and the age requirement sits in article 11 of another law, article 2
gets a cross-law `input`, not an inline `leeftijd >= 18`.

**And do not leave a condition unconnected.** This half is easier to forget, and
it is the half this corpus gets wrong. If your entry produces an output that
expresses a restriction (an age test, an asset test, an insurance requirement),
some entry has to read it. Where the restriction belongs to the
entitlement in *this* entry, this model reads it. Where it belongs elsewhere, the
entry that grants the entitlement reads it across a `source` binding, and that is
not a scope violation: the condition it then applies is "geen aanspraak op grond
van artikel 3", which its own text does refer to.

An output that nothing consumes restricts nothing, however cautious it looks.
Measured on the zorgtoeslag in round 3: the age test of article 1 and the asset
test of article 3 were both produced and neither was ever read. The
model granted the allowance to a sixteen-year-old and to a millionaire, and every
individual article looked correct.

Binding to an entry outside your scope is allowed and expected, in a window run
and in a targeted one alike. Editing your own entry to add a binding is not
editing another entry.

**The law may be inefficient, redundant or circular. Model it as written.**

## Aanhef and onderdelen

An aanhef with its onderdelen is one norm spread over several entries. The corpus
splits below article level. A lid with an enumeration is stored as one
entry for the aanhef (`3.2`) and one per onderdeel (`3.2.a` to `3.2.f`), each
with its own `text` and its own place for a `machine_readable`. Neither entry
states a rule on its own.

**The model for such a lid goes on the aanhef entry; the onderdeel entries stay
without a `machine_readable`.** The aanhef states the operative words ("wordt
mede verstaan onder partner degene die ... en:"), so it is the only entry whose
text names what is being decided. Each onderdeel then appears in that model as
its own named parameter or intermediate output, with the onderdeel letter in its
`description` and its own `legal_basis`, so a reader can still see which onderdeel
produced which branch. The condition the aanhef states applies to all of them and
is modelled once, as an `AND` around the `OR` of the onderdelen.

Modelling an onderdeel by itself drops that condition silently. In round 3
`is_partner_op_grond_van_erkenning` came out as a bare `OR` of the two
erkenningsvormen, without the requirement that both are registered at the same
woonadres, which makes the rule wider than the law.

An onderdeel that is a self-standing definition ("Onze Minister: Onze Minister
van Volksgezondheid, Welzijn en Sport") is the exception: it states a complete
norm and gets its own model.

**The aanhef is read for its own words too, not only as the place the onderdelen
land.** It carries what holds for all of them at once: the reach of what is being
defined, and the caveats that qualify every onderdeel under it. Those go first
when the onderdelen are worked through one by one, because each onderdeel is
answerable on its own and the sentence above them belongs to no single one. Read
the aanhef twice: once for what it opens, and once for what it says.

## Four options at a hard spot

At every place where an entry resists translation, exactly one of these applies.
Work down the list in order and take the first that fits. Round 4 structurally
chose the cheapest option, which is the last one in this list.

**The place is the unit, not the entry.** An entry has as many of these answers
as it has hard spots, and the four never compete for one slot. Definitions that
all bind to another law (option 1) under a chapeau that states a reach the format
has no field for (option 3) give you the bindings *and* the marking, and neither
makes the other unnecessary. One answer per entry is how a construct nobody can
express ends up unrecorded behind a model that looks finished.

**1. The value comes from another law or another article: bind to it.**
"de schadeverzekering, bedoeld in artikel 1, onder d, van de Zorgverzekeringswet"
is not a gap. It is an `input` with `source.regulation` and `source.output`. That
the target law is not in the corpus yet changes nothing about the entry: whether
a regulation has been harvested is a state of the corpus, it is fixed by
harvesting, and it does not belong in the law file. Write the binding and leave
it standing. In round 4, 43 of the 101 norm gaps were cross-law references
written up as gaps.

**2. The law leaves the content open and another regulation or implementing
policy fills it: `open_terms`.** "Bij ministeriële regeling wordt de
standaardpremie vastgesteld" is a complete legal instruction that lacks a number.
So is "voor zover dat redelijk is", "zo spoedig mogelijk" and "onverwijld": the
law states a norm and leaves its content to be filled. Where the article names
who fills it, `delegated_to` and `delegation_type` say so; where it names nobody,
`decided_per_case_by` names the authority that is competent in the individual
case and fills the term through implementing policy with a motivation. The
concept does not change with the question whether the law appoints a filler, and
every open term names one of the three (see below).

**3. The format cannot express the construct: `markings`.** The words are clear
and the language has no shape for them. See below.

**4. None of the above: model it.** Most articles land here, including many that
look procedural at first read.

Two mistakes from round 4 come straight from skipping this list. "Zo spoedig
mogelijk" and "onverwijld" were marked as untranslatable while they are open
norms (option 2). The citeertitel was marked as untranslatable while `declares`
exists for exactly that (option 4, see Declarations below).

**Silence is never one of the options.** An entry you pass over without a word is
indistinguishable from an entry nobody read, and a check now reports it as such.
An entry can also be silent about one construct while it answers the rest, and
that shape costs a reader more: the model beside it vouches for the omission.
Look hard before concluding an entry states nothing: going through the Awir and
the zorgtoeslag entry by entry turned up almost none, and every candidate turned
out to be a kind of provision nobody had looked for. A definition by reference is
a cross-law binding. A naming provision ("de normpremie: de aan de hand van het
drempelinkomen berekende premie") belongs to an output another entry computes.
Even the citation title fixes what every execution trace calls this law.

**A provision that limits what the administration may do is never passed over.**
Limitation periods, minimum and maximum amounts, rounding floors, hardship
clauses, revision windows, exclusions, transitional law: these bound the
citizen's exposure, and leaving them out shifts the balance one way while every
rule you did translate shifts it the other. Measured on the Awir in round 3: the
five-year limitation periods that protect the administration were translated, and
the € 24 rounding floor, the € 121 threshold, the revision limitation period and
the hardship clause were all passed over without a word.

## Markings

A marking flags one construct in an article that is otherwise worked out. It says
the format cannot express that construct, it names it, and it leaves standing
everything that does fit.

```yaml
machine_readable:
  markings:
    - about: de week waarin de aanvraag is ingediend
      reason: >-
        DATE_PART leest jaar, maand en dag uit een datum en kent geen
        weeknummer; de week is hier een zelfstandige waarde waarop de
        bepaling rust.
      resolution: operation       # operation | model
      resolved_by: Een weeknummer als waarde van `in` bij DATE_PART
      target: []
      legal_text_excerpt: de week waarin de aanvraag is ingediend
      accepted: false
  execution:
    # everything that CAN be expressed, which is nearly always most of it
```

`resolution: operation` means the operation does not exist and has to be built.
The value names the thing to be added, not the place it runs: building one
touches the schema, the model, the evaluation in the engine, the BDD grammar and
the frontend.
`resolution: model` means the operation set is not the problem: the format has no
shape for the construct at all (quantification over persons, a rule about a set
rather than a value, a legal fiction). Nothing else belongs in a marking. Group
markings by `resolved_by` and you can read the backlog of missing operations off
the corpus, which is what the field is for.

`legal_text_excerpt` is required and quotes this entry's own text. A marking that
cannot quote the words it is about is about something else.

### A provision that repeats per period

A provision saying an outcome is established anew for every period, continuing
through time, is `resolution: model`. The format has no shape for a result that
is re-established per period, and no operation gives it one. Do not approximate
it with a loop and do not file it as `operation`.

Article 2, fifth paragraph of the Wet op de zorgtoeslag is the case: "De
aanspraak op een zorgtoeslag wordt voor iedere kalendermaand afzonderlijk
bepaald." An enricher asked for "periodieke evaluatie (iteratie over
kalendermaanden) in de engine", which is the wrong answer. The entitlement is
decided again each month, running through time, and that needs state outside the
execution recording which months are already decided. One execution covers one
month.

`resolved_by` names what is missing: an execution per period with state held
outside it. The marking is the result of reading the provision, not a shortfall
in the model: it turns a silent gap into a known one.

### The three prose fields

`about`, `reason` and `resolved_by` do different work, and each of the three is
required because none of them can be recovered from the other two.

- **`about` is what.** The construct, in the words the article uses.
- **`reason` is why.** Why that construct does not fit, stated in terms of what
  the format does have. This is the diagnosis.
- **`resolved_by` is what would close it.** The change, concrete enough to
  become work.

The order is not free. The change follows from the reading of the provision; the
reading does not follow from the change. A marking from round 4 shows it:

> **about:** de toepassing van deze wet voor zover een oude regeling haar van
> toepassing verklaart
>
> **reason:** "Voor zover" beperkt de toepassing per bepaling van deze wet, en
> niet de wet als geheel: een oude regeling kan deze wet voor het ene onderwerp
> wel en voor het andere niet van toepassing verklaren. Het model kent alleen
> toepasselijkheid van een hele wet.
>
> **resolved_by:** Een vorm waarin toepasselijkheid per bepaling van een wet kan
> worden uitgedrukt, in plaats van als één booleaanse uitkomst voor de hele wet.

Read the third line on its own and you have a wish. Nothing in it says what
"voor zover" does in this provision, so nothing in it tells you whether the wish
is earned. That is the half a reviewer needs, because without a diagnosis a gap
somebody worked through reads exactly like a gap nobody opened.

**What separates a good reason from a bad one:** a good one names what the
format *does* have and says where it falls short. "Het model kent alleen
toepasselijkheid van een hele wet" names the shape that comes closest and the
distance to it. "Dit past niet in het model" names nothing: it is the claim the
marking already makes by existing, written out a second time. Two more failures
of the same kind, and a check reports all three:

- A reason that restates `about`. A restatement answers the first question a
  second time, and this field asks the second one.
- A reason that is `resolved_by` said again. Then the wish stands there twice
  and the reading is gone.

### The test for a marking

The test is not whether you can execute the article. It is: **which word can I
not fill in, and what is left when I leave that word as an open value?**

An entry that stays empty behind a marking is a defect. You lose every rule that
was derivable, and the marking then measures the gap far larger than it is. This
was the biggest failure form of round 4, and the file shows both shapes two
entries apart, in
`corpus/regulation/nl/wet/wet_op_de_zorgtoeslag/2026-01-01.yaml`:

- Entry `1.1`, the aanhef of article 1, got one marking about the reach of a
  begrippenlijst and nothing else. No outputs, no actions, nothing a reader can
  do anything with. **The marking was the right half.** The empty article beside
  it was the defect, so the repair fills the article and keeps the marking. It
  never drops the marking and fills the article. Round 5 did the second, on this
  same article.
- Entry `1.1.c`, the definition of "verzekerde", is fully worked out: parameters,
  four cross-law inputs, an output and the actions that compute it. It has one
  marking, for "vanaf de eerste dag van de kalendermaand volgende op de maand
  waarin hij achttien jaar wordt", because at the time no operation read the
  month out of a date. The model asks for the first day of the assessed month as
  a parameter, compares the eighteenth birthday against it, and still produces
  `is_verzekerde`.

Write markings like the second one.

That second marking is also the example of a marking that has since expired.
`START_OF` and `DATE_PART` write the figure it names in two lines, so an entry
that carries it today is stale. A marking states what the format cannot do at
the moment of writing, and the operation list in `reference.md` is what that
claim is checked against. Read it before you mark.

### An article that works and still owes a marking

The empty article behind a marking is one failure. Dropping the marking and
filling the article is the other, and it is the more expensive of the two,
because the file then looks finished. Nothing is left blank and no check reports
a gap; the construct the format cannot hold has stopped being mentioned.

Round 5 produced it on the article round 4 got wrong. Article 1 of the Wet op de
zorgtoeslag came back fully modelled: three begripsbepalingen as `definitions`,
an executable `is_verzekerde` with four cross-law bindings, `drempelinkomen`
computed from the minimumloon, an action and a `legal_basis` for every onderdeel.
Its chapeau appears nowhere in the file:

> In deze wet **en de daarop berustende bepalingen** wordt, **tenzij anders is
> geregeld**, verstaan onder: a. Onze Minister: … b. zorgverzekering: …

Those words say something about the definitions under them that no onderdeel
says about itself. **"En de daarop berustende bepalingen" gives them a reach past
this document.** They govern the wording of every regulation that rests on this
law, and that regulation does not have to refer to them for it to hold. What the
corpus can express is the opposite direction: a document reads another through a
`source` binding it writes itself. Reading is not governing, there is no field
for the reach of a definition, and no operation supplies one. That is a marking
with `resolution: model`.

```yaml
markings:
  - about: het bereik van de begripsbepalingen over de daarop berustende bepalingen
    reason: >-
      De begrippen van dit artikel beheersen ook het woordgebruik van elke
      regeling die op deze wet berust, zonder dat die regeling ernaar verwijst.
      Het model kent alleen de omgekeerde richting: een document leest een ander
      document via een source-binding die het zelf schrijft. Een bereik dat geldt
      zonder dat de andere kant het aanroept, heeft geen veld en geen bewerking.
    resolution: model
    resolved_by: >-
      Een vorm waarin de begripsbepalingen van een wet in bereik komen bij het
      uitvoeren van een regeling die op die wet berust, afgeleid uit de
      legal_basis die de regeling zelf declareert.
    target: []
    legal_text_excerpt: In deze wet en de daarop berustende bepalingen wordt, tenzij anders is geregeld, verstaan onder
    accepted: false
```

**"Tenzij anders is geregeld" is not a second marking.** A displacement is
declared by the regulation that departs and not by the article departed from, so
this clause asks nothing of article 1: it permits displacement, and `overrides`
is that mechanism already. It belongs in the `legal_basis.explanation` of the
definitions it qualifies, in this article's own words. Two clauses in one
sentence, two different answers, and reading them as one is how the marking
channel fills with work that the format can already do.

The chapeau of a begrippenlijst is the standard place for this, and a check
reports an article whose chapeau reaches past the document while the model beside
it says nothing about that reach.

### The `target` list

`target` is an assertion, so it has to be true. It lists the values in this entry
that cannot be produced because of this marking: outputs, inputs or parameters by
name.

- **An empty list is a claim, not an omission.** It says the entry stays
  executable and only its explanation is incomplete. That is the normal case.
- **A name in the list is a value this entry's own model declares:** an input, a
  parameter, an output, a definition or an open term. An invented word is not a
  target, and a check reports a name the entry declares nowhere.
  Naming what the entry would have produced is the work.
- **A name in the list means that value is computed nowhere in this entry.** If
  an action produces it anyway, the marking contradicts the model. The same
  holds for reading it: an action that calculates with a targeted name rests on
  a value the marking says is not there, and the check reports both shapes.

Today the predecessor field `blocks` is empty in 39 of 39 markings, and
of the 72 values that stood marked as blocked not one is actually left out. Both
halves of that are wrong and both are cheap to get right. Name the values the
entry genuinely does not produce, and make sure the actions really leave them
out.

Do not approximate around a marking. No ten-case `IF` tree standing in for a
table, no arithmetic trick standing in for rounding, no pre-computed aggregate
hardcoded as a literal.

## Open terms

The law declares the term and references it as a `$variable`; the regulation
that fills it registers as filling it. Under delegation that regulation is a
ministeriële regeling or AMvB. A municipal ordinance in co-government
(*medebewind*, e.g. Participatiewet art. 8) is not delegated: the municipality
executes the act on its own authority. It is still bound by the act and yields
to it (Gemeentewet art. 121-122). The mechanism is the same; do not call the
ordinance delegated.

```yaml
# wet_op_de_zorgtoeslag, article 4
machine_readable:
  open_terms:
    - id: standaardpremie
      type: amount              # string | number | boolean | amount | date
      required: true
      delegated_to: Onze Minister          # omit when the article names nobody
      delegation_type: MINISTERIELE_REGELING   # omit likewise
      legal_basis: artikel 4 Wet op de zorgtoeslag
  execution:
    output:
      - name: standaardpremie
        type: amount
        type_spec:
          unit: eurocent
    actions:
      - output: standaardpremie
        value: $standaardpremie   # the engine resolves this through implements
```

```yaml
# regeling_standaardpremie, article 1
machine_readable:
  implements:
    - law: wet_op_de_zorgtoeslag
      article: '4'
      open_term: standaardpremie
      gelet_op: Gelet op artikel 4 van de Wet op de zorgtoeslag
  execution:
    actions:
      - output: standaardpremie
        value: 211200
```

The output name in the implementing regulation matches the open term `id`. Priority
between competing implementations follows lex superior and lex posterior.

### Who fills it

Every open term names someone. A check reports a term with none of
`delegated_to`, `expected_source` and `decided_per_case_by` filled in: a norm
nobody is competent to fill is not left open, it is left out.

- `delegated_to` plus `delegation_type` where the article authorises a layer
  ("bij ministeriële regeling wordt ... vastgesteld"). The type is a closed list
  and it is a competence claim: a regulation at another layer does not fill this
  term.
- `expected_source` where the text names the filling regulation itself ("de
  regeling, bedoeld in artikel 1 van de Regeling zorgverzekering"), by title or
  by BWB id. Which regulation is meant is a property of the law. Whether that
  regulation is in the corpus today is not, and it is recorded nowhere.
- `decided_per_case_by` where the article appoints nobody and the norm is filled
  in the individual case ("voor zover dat redelijk is", "in bijzondere
  gevallen"). Name the authority and the article that makes it competent. Its
  answer needs a motivation under Awb 3:46 and is part of the besluit, which is
  what separates a discretionary power from a value that is merely missing.

Do not record whether the filling regulation is currently in the corpus. That is
a state of the corpus, it is untrue by next week, and nobody cleans it up. The
resolve step and the work queue track it (RFC-026).

## Declarations

Some provisions compute nothing and are not open either. They establish something
the rest of the corpus depends on.

```yaml
declares:
  - property: name        # name | officiele_titel | valid_from | valid_to |
                          # regulatory_layer | legal_basis
    value: Algemene wet inkomensafhankelijke regelingen
```

Awir article 51 ("Deze wet wordt aangehaald als: ...") is the clearest case:
every execution trace that names this law is quoting that article. Article 50
("treedt in werking op 1 september 2005 en geldt voor berekeningsjaren die
aanvangen op of na 1 januari 2006") fixes `valid_from` and, through
`applies_from`, a floor on the berekeningsjaar that no calculation may go below.

The document header already contains these values, copied there by the harvester.
Recording the article that decides them turns a copy into a derivation, and a
check holds the two against each other: when they disagree, the article is right
and the header is stale.

## Displacement, "in afwijking van"

Two things go wrong here often enough to state.

**The article named is not the article displaced.** "In afwijking van artikel 7,
derde lid, van de Awir, bestaat geen aanspraak op een zorgtoeslag" names the rule
being departed from, while the subject of the clause says what is displaced: the
entitlement that another article of *this* law establishes. Put the override on
the article that produces the thing, not on the article the sentence cites. An
override addressed at the wrong article never fires, and the engine then returns
both the displaced value and the displacing one without complaint. The `article`
field must match the producing entry's `number` exactly as this file writes it:
in round 3 four of five overrides pointed at `"2"`, `"3"` and `"7"` while the
producers are stored as `2.1`, `3.1` and `7.3`, so nothing fired.

**"Bestaat geen aanspraak" is not an entitlement of zero.** With an entitlement
of zero there is a decision, legal remedies and a ground for recovery; with no
entitlement there is none of that. Article 2 of the zorgtoeslag says "aanspraak
**ter grootte van** dat verschil": the amount is a property of the entitlement,
so where the entitlement does not arise there is no amount to compute either.

```yaml
overrides:
  - article: '2.1'                  # where the entitlement is produced
    output: aanspraak_op_zorgtoeslag
    voids: true                     # it does not arise, rather than becoming zero
    legal_text_excerpt: bestaat geen aanspraak op een zorgtoeslag
```

`voids` is what the engine acts on. `legal_text_excerpt` is why, in this
article's own words, quoted verbatim. Do not classify the ground into a category
of your own; copy the statute.

A derogation exists only where words say so. "In afwijking van", "onverminderd",
"blijft buiten toepassing" and "met dien verstande" are such words. A second
sentence that adds a ground is not one, and neither is a reading that makes the
article tidier. Quote the words you relied on in the `legal_basis.explanation` of
the action they shaped. If you cannot quote them, you invented the derogation.

Do not let the producing article read the exclusion instead. Article 2 says
nothing about wealth, so pulling that condition in is a scope violation, however
helpful it looks.

## Numbers and units

Every number in a model appears literally in the text of the entry the model
belongs to. Not "derivable from", not "equal to": present.

- "vier weken" is `weeks: 4`, never `days: 28`.
- "ten minste 10 percent lager" is a comparison against 10 percent, never a
  multiplication by `0.9`.
- "naar tijdsgelang herrekend" states no denominator. If the text names no
  measure, the measure is an open term, not a division by 12 you supply.
- A fallback that borrows a number from another lid is a number from another lid.
  If this lid states no fallback, it has none.

**The one sanctioned conversion is money.** Every monetary value in every file is
`type: amount` with `type_spec: { unit: eurocent }`, and the literal from the text
is multiplied by 100. This is a corpus-wide convention and it outranks the rule
above, because `unit` is a label and never a conversion (RFC-023): a law written
in euro and a law written in eurocent will bind to each other and the engine will
not notice. In round 3 the Awir chose euro and the zorgtoeslag chose eurocent,
each internally consistent, and the same person came out at € 827,63 or
€ 1.550,46 depending on which file you believed. A file that uses `unit: euro`
anywhere is broken even if it is consistent with itself.

Rounding is not part of this. The engine has `ROUND`, `CEIL` and `FLOOR`, so
model the rounding the law states and round nothing where it states none.

## Actions and operations

Every action has an `output` and a `value`. The `value` is a literal, a
`$variable`, or an operation.

Naming an output is not computing it. An entry that declares outputs and has no
action, definition, open term or `implements` that produces any of them is
reported by a check, because from the outside it promises a value the engine
never delivers.

```yaml
actions:
  - output: heeft_recht
    value:
      operation: AND
      conditions:
        - operation: GREATER_THAN_OR_EQUAL
          subject: $leeftijd
          value: 18
        - operation: EQUALS
          subject: $is_verzekerd
          value: true
    legal_basis:
      law: Wet op de zorgtoeslag
      article: '2'
      paragraph: '1'
      explanation: Dutch explanation of how this action follows from the text
```

| Category | Operations | Operand shape |
|----------|-----------|---------------|
| Arithmetic | `ADD`, `SUBTRACT`, `MULTIPLY`, `DIVIDE`, `MIN`, `MAX` | `values:` array |
| Comparison | `EQUALS`, `GREATER_THAN`, `LESS_THAN`, `GREATER_THAN_OR_EQUAL`, `LESS_THAN_OR_EQUAL` | `subject:` (must be a `$variable`) + `value:` |
| Logical | `AND`, `OR` | `conditions:` array |
| Negation | `NOT` | `value:` |
| Membership | `IN` | `subject:` + `values:` or `value:` |
| Conditional | `IF` | `cases:` (each `when`/`then`) + `default:` |
| Collection | `LIST` | `items:` array |
| Rounding | `ROUND`, `CEIL`, `FLOOR` | `value:` + `precision:` (required) |
| Date | `AGE` (`date_of_birth`, `reference_date`), `DATE_ADD` (`date` + `years`/`months`/`weeks`/`days`), `DATE` (`year`, `month`, `day`), `DATE_DIFF` (`from`, `to`, `in`), `DAY_OF_WEEK` (`date`), `DATE_PART` (`date`, `in`), `START_OF` (`date`, `in`) | named fields |

`ROUND` is half-up (rekenkundig, the Hoge Raad default), `CEIL` rounds up,
`FLOOR` rounds down. `precision` counts decimals in the value's own unit, so a
eurocent amount rounded to whole euros is `precision: -2`.

Operations nest: any operand may itself be an operation. `reference.md` has the
full shapes and `examples.md` the worked cases.

### Legal text to operation

| Legal text | Operation |
|------------|-----------|
| "heeft de leeftijd van X jaar bereikt" | `AGE` + `GREATER_THAN_OR_EQUAL` |
| "ten minste X" | `GREATER_THAN_OR_EQUAL` |
| "niet meer dan X" | `LESS_THAN_OR_EQUAL` |
| "indien ... en ... " / "indien ... of ..." | `AND` / `OR` with `conditions` |
| "tenzij" / "niet" | `NOT` wrapping the positive condition |
| "vermenigvuldigd met" / "verminderd met" / "vermeerderd met" | `MULTIPLY` / `SUBTRACT` / `ADD` |
| "afgerond op hele euro's" | `ROUND` with `precision: -2` on a eurocent value |
| "binnen X weken na" | `DATE_ADD` with `weeks` |
| "het aantal maanden tussen" | `DATE_DIFF` with `in: months` |
| "het kalenderjaar waarin" / "het berekeningsjaar" | `DATE_PART` with `in: year` |
| "de eerste dag van de kalendermaand volgende op" | `DATE_ADD` with `months: 1` over `START_OF` with `in: month`, in that order |
| "na de eerste dag van de maand" | `GREATER_THAN` on `DATE_PART` with `in: day`, value 1 |
| "voor zover" | a bound on an amount: `MAX`/`MIN` around the qualifying part. A boolean here loses the partial case, and always in the citizen's disfavour |
| "dan wel" (two measures side by side) | `OR` over two comparisons, each with its own parameter. One parameter whose description covers both is not a model of the disjunction |
| "in afwijking van artikel X" | `overrides` declaration |
| "bij ministeriële regeling" | `open_terms` + `implements` |

## Bindings

An `input` that names a concept another provision owns MUST carry a real
`source:` block. A description is documentation; it makes the engine resolve
nothing.

```yaml
input:
  - name: toetsingsinkomen
    type: amount
    source:
      regulation: algemene_wet_inkomensafhankelijke_regelingen
      output: toetsingsinkomen
      parameters:
        bsn: $bsn
    type_spec:
      unit: eurocent
```

Omit `regulation` for a reference to another article of the same law.

**A `source:` belongs under `input:`, never under `parameters:`.** This is the
most common way a binding looks real and silently does nothing. `Parameter` has no
`source` field, so a `source:` under `parameters:` is dropped at parse time and
the value degrades to a plain caller-supplied parameter. It still passes any BDD
scenario that injects the value directly, which hides the defect. The bound value
goes under `input:` with its `source:`; the leaf parameters that feed
`source.parameters` stay under `parameters:`.

Never fall back to a plain parameter because "the engine cannot resolve multiple
source bindings per article". It can, and they resolve.

If the local name differs from the target's output name, put the target's name in
`source.output`, the local name in `name`, and the reason in `description`.

Where the target law does not produce the output you need, add that output to the
target law first, on the article that should own it, then bind to it. Do not
leave the reference in a description only.

**Every law the entry's text cites is read by the model or fills an open term.**
The harvester records the citation in the entry's `references` block, and a check
holds that block against what the model does: a cited law that the model neither
binds to nor names on an open term is a reference nobody acted on. Bind to the
article the text names, or put the regulation in `expected_source` on the term it
fills.

## Hooks and produces

```yaml
machine_readable:
  hooks:
    - hook_point: pre_actions        # pre_actions | post_actions
      applies_to:
        legal_character: BESCHIKKING # required
        stage: BESLUIT               # AANVRAAG | BEHANDELING | BESLUIT |
                                     # BEKENDMAKING | BEZWAAR
  execution:
    produces:
      legal_character: BESCHIKKING   # BESCHIKKING | TOETS | WAARDEBEPALING |
                                     # BESLUIT_VAN_ALGEMENE_STREKKING | INFORMATIEF
      decision_type: TOEKENNING
```

Hooks let an article (typically from the AWB) fire on every matching lifecycle
event, which is how cross-cutting duties such as the motivation requirement are
modelled. Procedures with their stages are declared at the top level of the file,
not inside an article; `reference.md` has the shape.

## Field types

| Context | Valid types |
|---------|------------|
| `parameters` | `string`, `number`, `boolean`, `date` |
| `input` and `output` | `string`, `number`, `boolean`, `amount`, `object`, `array`, `date` |

`$referencedate` is not a built-in. Declare it as a `parameter` with `type: date`
if you use it.

## Quoting in the YAML

You write with Edit, straight into the file, and a file that stops parsing is
broken from that keystroke onward. Nothing after it can be read: not by the
schema check, not by the measurement afterwards, not by you. In round 5 one
unquoted sentence in article 5 cost the whole law, and the actual defect of that
run was never found because there was no longer a file to look at.

**A value that contains a colon followed by a space must be quoted.** Everything
before that colon is read as a key, and the file ends there. This is the sentence
that broke:

```yaml
explanation: Eerste lid: de Dienst Toeslagen is belast met de uitvoering van deze wet.
```

Quoted, or as a block scalar, it is fine:

```yaml
explanation: "Eerste lid: de Dienst Toeslagen is belast met de uitvoering van deze wet."
explanation: >-
  Eerste lid: de Dienst Toeslagen is belast met de uitvoering van deze wet.
```

Dutch legal prose walks into this constantly, and the openings are recognisable:
"Eerste lid: ", "Let op: ", "Onze Minister: ", "wordt aangehaald als: ". The
corpus already quotes the ones it has: `text: 'Deze regeling wordt aangehaald
als: Subsidieregeling …'`, `description: 'Leeftijd in jaren (bron: BRP)'`.

The trap sits unnoticed because most colons in legal text are harmless. `Zie
artikel 5:2 Awb` and `AWB 4:1` parse without a murmur: the rule is about the
space, not about the colon. So the habit you build on article numbers does not
carry over, and the one sentence that puts a space after the colon is the one
that breaks the file. Quote on the punctuation you see, not on how dangerous
the sentence feels.

**Quote what would otherwise read as a number or a date.** `number` and
`valid_from` are strings in the schema, and unquoted they change type silently:
`number: 3.1` becomes the float 3.1, `valid_from: 2025-01-01` becomes a date.
Every article number and every date in this corpus is quoted (`number: '3.1'`,
`valid_from: '2025-01-01'`); keep it that way. A value that genuinely is a
number, `value: 198700`, stays unquoted.

The same caution covers a value that opens with punctuation YAML reserves
(`*`, `&`, `!`, `%`, `@`, `` ` ``, `[`, `{`), which is read as syntax rather
than as text. Quote it and the question does not come up.

The safe default for any prose field is a `>-` block scalar. It holds a colon, a
quote and an apostrophe without escaping, and it is what the rest of the file
already does.

## Validate and test

When a shell is available, follow `testing.md` in this skill directory for the
validate-and-test loop. In the enrichment pipeline there is no shell and the
worker validates instead.

## Write the related-legislation envelope

After the `machine_readable` sections are final, write a sibling envelope so the
pipeline can harvest the legislation this law depends on. It goes next to the law
YAML as `.enrichment-result.yaml`.

```yaml
law_id: wet_op_de_zorgtoeslag
related_legislation:
  - name: Regeling vaststelling standaardpremie en bestuursrechtelijke premie
    relation: delegated_regeling      # source_regulation | legal_basis | delegated_regeling
    bwb_id: BWBR0037841               # optional, best effort
    slug: regeling_standaardpremie    # optional, best effort
    open_term: standaardpremie        # optional, delegations only
  - name: Algemene wet inkomensafhankelijke regelingen
    relation: source_regulation
```

One entry for every `source.regulation` you bound, every `legal_basis` you
anchored on, and every open term you declared. `name` is required; the rest is
best effort.

**This must not go in the law YAML.** The law file stays strictly
schema-conformant. There is no `related_legislation:` key anywhere inside it.

## Report

Report on the entries you were given and on nothing else. `{TOTAL}` is the size
of that scope, not the size of the law: a targeted run of one entry reports one.

```
Interpreted {LAW_NAME}

  Entries processed: {TOTAL}
  Made executable: {EXECUTABLE_COUNT}
  Validation: {PASSED/FAILED}
  BDD scenarios: {PASS}/{TOTAL}

  Markings: {N} in {N} entries
  - {entry}: {about} ({resolution}), target: {names or "none"}

  Open terms: {N} in {N} entries
  - {entry}: {id}, filled by {delegated_to or "any competent authority"}

  Remaining issues:
  - {unresolved failures}

  TODOs:
  - {laws that still have to be harvested}
  - Review markings and set accepted: true for the ones a human has confirmed
```
