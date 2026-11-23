#!/usr/bin/env python3
"""Survey bias check: a rule-based linter for questionnaires.

Reads a questionnaire (Markdown/plain text or JSON, see SKILL.md "Input format") and prints
CANDIDATE problems: question, line, rule ID, severity, the matched text and why it matters.
Rules match patterns; they do not understand the question. Every finding needs a human or
agent judgment before it is called a defect, and many real problems (built-in assumptions,
social desirability, order effects) are not detectable by rules at all.

Standard library only, Python 3.9+. No network. Every threshold is cited in
references/sources.md.

Usage:
  python3 scripts/survey_bias_check.py survey.md
  python3 scripts/survey_bias_check.py survey.json --json
  python3 scripts/survey_bias_check.py survey.md --strict        # exit 1 when there are findings
  python3 scripts/survey_bias_check.py survey.md --mode phone --audience expert --keep Q7,Q9
  python3 scripts/survey_bias_check.py survey.md --route-skip Q5,Q6  # length of the longest route only
  cat survey.md | python3 scripts/survey_bias_check.py -          # read stdin
  python3 scripts/survey_bias_check.py --list-rules

Exit codes: 0 = ran (with or without findings), 1 = findings and --strict, 2 = bad input.
"""
import argparse
import json
import math
import re
import sys

# ---------------------------------------------------------------------------------------
# Thresholds (each one is cited in references/sources.md)
# ---------------------------------------------------------------------------------------
MAX_WORDS = 20  # Payne 1951, as summarised in the DePaul handout (secondhand)
MAX_OPTIONS = 10  # tool default, no primary source (sources.md)
POINTS_PER_MINUTE = 8  # Versta Research length method
POINTS = {"single": 1.0, "per_grid_row": 1.0, "per_two_multi_options": 1.0, "number": 2.0, "open": 3.0}
SENTENCES_PER_POINT = 3  # Versta: one point per three sentences of reading
IDEAL_MINUTES = 10  # Revilla & Ochoa 2017 (web-panel median "ideal" length)
MAX_MINUTES = 20  # Revilla & Ochoa 2017 (web-panel median "maximum" length)
MAX_GRID_ROWS = 10  # convention, no primary source (sources.md, "Conventions")
MAX_OPEN = 3  # convention, no primary source
PHONE_MAX_OPTIONS = 5  # Pew: "four or perhaps five at most", especially by telephone
PHONE_MAX_GRID_ROWS = 5  # convention
PHONE_TIME_FACTOR = 1.5  # Versta: phone minutes = online minutes x 1.5
PARENTHETICAL_WORDS = 5  # convention (SB026)
INLINE_LIST_COMMAS = 3  # convention (SB026)
LOAD_SIGNALS = 2  # convention (SB026): flag when at least two signals are present
CONTINUOUS_GAP_SEVERITY = "medium"  # convention (SB010): integer-adjacent ranges of a continuous measure

RULES = {
    "SB001": ("double-barreled", "Asks about two things at once; an answer cannot be assigned to either one."),
    "SB002": ("leading or loaded wording", "Wording pushes toward one answer or carries an evaluation."),
    "SB003": ("absolute", "Absolute terms force a literal reading that almost nobody can affirm."),
    "SB004": ("hypothetical", "Stated intent about a hypothetical overstates what people actually do or pay."),
    "SB005": ("negation", "Negated wording makes the meaning of each answer hard to work out."),
    "SB006": ("vague quantifier", "The word means a different amount to each respondent."),
    "SB007": ("jargon or acronym", "Respondents may not know the term, and guess."),
    "SB008": ("long question", "Long questions are harder to hold in mind and are skimmed."),
    "SB009": ("unbalanced scale", "Unequal numbers of positive and negative labels shift answers toward the larger side."),
    "SB010": ("numeric ranges", "Ranges must be mutually exclusive and cover every value."),
    "SB011": ("missing answer option", "Respondents with no fitting option pick a wrong one or drop out."),
    "SB012": ("inconsistent scales", "Scales that change direction or length between questions cause misreads."),
    "SB013": ("too many options", "Long lists are skimmed; early options get picked more on screen."),
    "SB014": ("agree/disagree format", "Agree/disagree items invite acquiescence; item-specific options measure better."),
    "SB015": ("survey length", "Longer questionnaires lose respondents and get lower-quality late answers."),
    "SB016": ("sensitive question handling", "Sensitive or demographic questions placed first or forced cost completions."),
    "SB017": ("reference period", "Without a stated, short period respondents recall different time spans, and recall badly."),
    "SB018": ("built-in assumption", "The question assumes something that may not be true of the respondent."),
    "SB019": ("stem and options mismatch", "The answer options do not answer the question as it is asked."),
    "SB020": ("unlabelled numeric scale", "Numbers without verbal labels are read differently by each respondent."),
    "SB021": ("sensitive behaviour", "People under-report disapproved behaviour and over-report approved behaviour."),
    "SB022": ("combined opt-out", "None, Other, Don't know and Prefer not to say are different answers."),
    "SB023": ("mental computation", "Averages, percentages and totals worked out in the head come back as rounded guesses."),
    "SB024": ("introduction", "The introduction can prime answers, and should say how long the survey takes."),
    "SB025": ("grid and open-question burden", "Long grids and many open questions tire respondents and get skipped."),
    "SB026": ("syntax load", "Conditions, exclusions, parentheticals and lists must all be held in mind at once."),
    "SB027": ("even-point scale", "A bipolar scale with no midpoint forces neutral respondents to pick a side."),
    "SB028": ("duplicate option", "Two options with the same wording cannot be told apart, and one option is probably missing."),
}

# ---------------------------------------------------------------------------------------
# Word lists. Short on purpose: a missed candidate costs less than a flood of false ones.
# ---------------------------------------------------------------------------------------
FIXED_PHRASES = [
    "terms and conditions", "pros and cons", "health and safety", "research and development",
    "bed and breakfast", "questions and answers", "and/or", "one or more", "more or less",
    "whether or not", "why or why not", "or not", "yes or no", "friend or colleague",
    "colleague or friend", "friends or family", "family or friends", "friend or family member",
    "or more", "or less", "or older", "or younger", "or fewer", "or so",
]
ANTONYM_PAIRS = [
    ("agree", "disagree"), ("satisfied", "dissatisfied"), ("likely", "unlikely"), ("easy", "difficult"),
    ("easy", "hard"), ("good", "bad"), ("good", "poor"), ("better", "worse"), ("favor", "oppose"),
    ("favour", "oppose"), ("support", "oppose"), ("approve", "disapprove"), ("increase", "decrease"),
    ("increased", "decreased"), ("positive", "negative"), ("higher", "lower"), ("too high", "too low"),
    ("more", "fewer"), ("more", "less"), ("important", "unimportant"), ("useful", "useless"),
]
LEADING_PATTERNS = [
    r"\bdon't you\b", r"\bwouldn't you\b", r"\bisn't it\b", r"\baren't you\b", r"\bshouldn't\b",
    r"\bdo you agree that\b", r"\bwould you agree\b", r"\bmost people\b", r"(?<!how )\bmany people\b",
    r"\bexperts (?:say|agree|recommend)\b", r"\bas you know\b", r"\bas everyone knows\b",
    r"\bit is well known\b", r"\bobviously\b", r"\bof course\b", r"\bstudies show\b", r"\bresearch shows\b",
    r"\b(?:amazing|awesome|fantastic|wonderful|incredible|world-class|award-winning|revolutionary)\b",
    r"\b(?:terrible|awful|horrible|disastrous)\b", r"(?<![-\w])great\b(?!-| (?:deal|extent|many))",
    r"\bhow much (?:do|did) you (?:love|enjoy)\b", r"\bnew and improved\b",
]
ABSOLUTE_PATTERN = r"\b(?:always|never|everyone|everybody|nobody|no one|every time|all the time|at all times|every single)\b"
HYPOTHETICAL_PATTERNS = [
    r"\bwould you (?:be willing|be interested|be likely|buy|pay|purchase|use|consider|switch|subscribe|sign up|try|attend|upgrade|prefer|choose|want)\b",
    r"\bif (?:we|you|it|there|your \w+|the \w+) (?:were|was|had|did|could|added|offered|launched|built|introduced|released|made|increased|raised|lowered|changed|removed)\b",
    r"\b(?:imagine|suppose|supposing|hypothetically)\b", r"\bin the future\b", r"\bwill you\b",
    r"\bhow likely (?:are|would) you (?:be )?to (?:buy|pay|purchase|use|subscribe|switch|upgrade|sign up|renew|try|attend)\b",
]
NEGATION_PATTERN = r"\bnot\b|n't\b|\bcannot\b|\bnever\b"
NEGATIVE_WORDS = [
    "unable", "unlikely", "unhappy", "dissatisfied", "unsatisfied", "unaware", "unnecessary", "unclear",
    "unreliable", "impossible", "disagree", "oppose", "prevent", "prohibit", "ban", "refuse", "fail",
]
VAGUE_STEM_PATTERN = r"\b(?:regularly|frequently|occasionally|recently|lately|sometimes|seldom|a lot)\b|(?<!how )\boften\b"
VAGUE_OPTION_WORDS = {
    "often", "sometimes", "rarely", "occasionally", "frequently", "regularly", "seldom", "usually",
    "a lot", "hardly ever", "a few", "several", "many", "a couple",
}
KNOWN_ACRONYMS = {
    "US", "USA", "UK", "EU", "UN", "TV", "OK", "ID", "AM", "PM", "PC", "IT", "HR", "CEO", "ATM", "DVD",
    "GPS", "SMS", "PDF", "FAQ",
}
JARGON_PATTERN = r"\b(?:synerg(?:y|ies)|omnichannel|paradigm|utili[sz]e|holistic|touchpoints?|value proposition|pain points?|use cases?)\b"
POSITIVE = {
    "satisfied": "satisfaction", "agree": "agreement", "likely": "likelihood", "good": "quality",
    "excellent": "quality", "easy": "ease", "useful": "usefulness", "helpful": "helpfulness",
    "positive": "valence", "better": "comparison", "happy": "happiness", "favorable": "favor",
    "favourable": "favor", "favor": "favor", "favour": "favor", "support": "support", "approve": "approval",
}
INTENSITY_LOW = ("not at all", "slightly", "a little", "somewhat", "moderately", "fairly")
INTENSITY_HIGH = ("very", "extremely", "completely", "strongly", "mostly", "quite")
ORDINAL_STARTS = (
    "not ", "a great deal", "a fair amount", "a lot", "daily", "weekly", "monthly", "yearly", "annually", "never",
    "always", "once", "twice", "every", "several times", "a few times", "less than", "more than", "less often",
    "more often", "today", "yesterday", "this ", "longer ago", "in the last", "in the past", "within",
)
# Whole words only, so "Everyday notes" or "This app" in a list of names does not start an ordinal ladder.
ORDINAL_RE = re.compile(r"^(?:%s)\b" % "|".join(re.escape(s.strip()) for s in INTENSITY_LOW + INTENSITY_HIGH + ORDINAL_STARTS))
# "1 - Very dissatisfied", "(2) Agree", "3. Neutral": a code in front of a verbal label.
CODE_PREFIX_RE = re.compile(r"^\s*\(?-?\d{1,3}\)?\s*[-\u2013\u2014:=.)]\s*(?=[^\W\d_])")
NEGATIVE = {
    "dissatisfied": "satisfaction", "unsatisfied": "satisfaction", "disagree": "agreement",
    "unlikely": "likelihood", "poor": "quality", "bad": "quality", "terrible": "quality",
    "difficult": "ease", "hard": "ease", "useless": "usefulness", "unhelpful": "helpfulness",
    "negative": "valence", "worse": "comparison", "unhappy": "happiness", "unfavorable": "favor",
    "unfavourable": "favor", "oppose": "support", "disapprove": "approval",
}
SPECIAL = {
    "other": r"^other\b|something else|somewhere else|someone else|anywhere else|not listed",
    "none": r"^none\b|^nothing\b|none of|not applicable|^n/?a$|^no,? i\b|i (?:do not|don't) use|"
            r"^i (?:have not|haven't|did not|didn't|do not|don't|have never|never)\b|^(?:have )?not used\b",
    "dk": r"don't know|do not know|not sure|unsure|no opinion|can't (?:say|recall|remember)|do not recall",
    "pnts": r"prefer not|rather not|decline to",
}
MULTI_PATTERN = r"select all|check all|tick all|choose all|all that apply|select up to|choose up to"
DEMOGRAPHIC_PATTERN = (
    r"\bincome\b|\bsalary\b|\bage\b|how old|date of birth|year were you born|\bgender\b|\bsex\b|\brace\b|"
    r"ethnic|religio|marital|sexual orientation|level of education|political|vote for|disabilit|"
    r"health condition|medical|diagnos|\bweight\b|phone number|home address"
)
SENSITIVE_PATTERN = (
    r"\bincome\b|\bsalary\b|\brace\b|ethnic|religio|sexual orientation|political|vote for|disabilit|"
    r"health condition|medical|diagnos|\bweight\b|phone number|home address"
)
THIRD_PARTY_PATTERN = r"^(?:does|did|has|is|are|do|have) (?:your|the) (?:company|employer|organi[sz]ation|team|household|manager|department|school)\b"
FREQ_COUNT_PATTERN = r"\bhow (?:often|frequently)\b|\bhow many times\b|\bhow many (?:days|hours|minutes|weeks)\b"
HAVE_YOU_PATTERN = (
    r"\bhave you (?:used|contacted|bought|purchased|visited|attended|experienced|received|made|taken|seen|tried|"
    r"called|ordered|returned|recommended|read|watched|eaten|exercised|travell?ed|shopped|paid|downloaded|searched)\b"
)
TIME_PATTERN = (
    r"\b(?:past|last|previous|since|during|today|yesterday|daily|weekly|monthly|yearly|annually|ever|currently|so far)\b|"
    r"\b(?:per|a|an|each|every) (?:day|week|month|year|hour)\b|\bthis (?:week|month|year|morning)\b|"
    r"\b(?:typical|average|usual|normal) (?:day|week|month|weekday)\b|\bin (?:19|20)\d\d\b|"
    r"\b\d+ (?:days?|weeks?|months?|years?|hours?)\b|\bmost recent\b"
)
LONG_WINDOW_PATTERN = (
    r"\b(?:past|last) (?:1[2-9]|[2-9]\d) months\b|\b(?:past|last|previous) (?:\w+ )?years?\b|"
    r"\bin your (?:life|lifetime)\b|\bever\b|\bsince you (?:started|joined|began)\b"
)
ASSUME_BEHAVIOUR_PATTERN = (
    r"\bhow (?:often|frequently)\b|\bhow many times\b|\bwhen did you last\b|\bwhen was the last time\b|"
    r"\bwhy (?:do|did) you\b"
)
ASSUME_EXPERIENCE_PATTERN = r"\bhow satisfied\b"
ZERO_OPTION_PATTERN = (
    r"^(?:never|none|no\b|zero|not at all|not once|i (?:have not|haven't|do not|don't|did not|didn't|never)|"
    r"have not|haven't|did not|didn't|not used|does not apply)"
)
HOW_FAMILY = {
    "satisfied": "satisfaction", "dissatisfied": "satisfaction", "often": "frequency", "frequently": "frequency",
    "likely": "likelihood", "unlikely": "likelihood", "easy": "ease", "difficult": "ease", "hard": "ease",
}
ONE_SIDED = {"satisfied": r"dissatisfied|unsatisfied", "likely": r"unlikely", "easy": r"difficult|hard"}
CLOSED_STEM_PATTERN = r"^(?:do|did|does|have|has|is|are|was|were|can|could|will|should) "
ANCHOR_PATTERN = r"\b\d+\s*(?:=|is|means|being)\s|\bwhere \d+\b|\(\s*\d+\s*[=:\u2013-]"
SENSITIVE_BEHAVIOUR_PATTERN = (
    r"\bcheat(?:ed|ing)?\b|\bst(?:eal|ole|olen)\b|\bshoplift\w*|\billegal(?:ly)?\b|\bdrug use\b|"
    r"\b(?:use|used|using|take|taken|took) (?:any )?(?:illegal |recreational )?drugs\b|\balcohol\w*|\bdrunk\b|"
    r"\bbinge drink\w*|\bsmok(?:e|ed|ing)\b|\bvap(?:e|ed|ing)\b|\btobacco\b|\bcannabis\b|\bmarijuana\b|"
    r"\bgambl\w+|\barrested\b|\bconvicted\b|\bcriminal record\b|\babortion\b|\bsexual partners?\b|"
    r"\bsexually active\b|\bsuicid\w+|\bself-harm\w*|\bbankrupt\w*|\bin debt\b|\btax evasion\b|\blied\b|\blying\b|"
    r"\bbribe\w*|\bpirated\b|\bdomestic violence\b|\bdid you vote\b|\bhave you voted\b|\bdonated? to charit\w+|"
    r"\bcharitable (?:giving|donations?)\b|\battend(?:ed)? (?:church|religious services|mosque|synagogue)\b"
)
COMPUTE_PATTERN = (
    r"\bon average\b|\baverage\b|\bas a (?:percentage|share|proportion)\b|\bpercentage of\b|\bpercent of\b|"
    r"\bwhat (?:percent|percentage|proportion|share)\b|\bin total\b|\bper year\b|\bannually\b"
)
NUMBER_STEM_PATTERN = (
    r"\bhow (?:much|many)\b|\bwhat (?:is|was|are|were) (?:your|the) (?:average|total|annual|monthly)\b|"
    r"\bwhat (?:percent|percentage|proportion|share)\b|\bnumber of\b"
)
HYPOTHESIS_PATTERN = (
    r"\bwe (?:believe|think|expect|hope|want to (?:show|prove|demonstrate))\b|\bour hypothesis\b|"
    r"\b(?:to|help us) (?:prove|show|demonstrate) that\b|\bwe are (?:trying|looking) to (?:show|prove)\b"
)
TIME_ESTIMATE_PATTERN = (
    r"\b\d+(?:\s*(?:-|to|\u2013)\s*\d+)?\s*(?:min|mins|minutes?|seconds?|questions)\b|"
    r"\b(?:few|couple of) minutes\b|\b(?:one|a) minute\b"
)
CONDITIONAL_PATTERN = r"\b(?:if|unless|provided that|assuming|in case)\b"
EXCLUSION_PATTERN = r"\b(?:excluding|not counting|not including|other than|apart from|aside from|except(?: for)?)\b"
FILTER_STOP_WORDS = {
    "have", "with", "that", "from", "often", "many", "times", "satisfied", "dissatisfied", "about", "been", "they",
    "there", "could", "should", "last", "past", "days", "day", "week", "weeks", "month", "months", "year", "years",
    "select", "apply", "following", "these", "those", "used", "use", "ever", "much", "long", "time", "all", "each",
    "part", "overall", "not", "had", "can", "will", "most", "more", "very", "some", "them", "its", "get", "got",
    "one", "two",
}
PRETEST_NOTE = (
    "A desk review does not replace a pretest: try the questionnaire on a few people from the target group "
    "(for example with cognitive interviews) before fielding."
)
NUMERIC_ENTRY_PATTERN = (
    r"\bhow (?:many|long|old)\b|\bhow much\b(?! do you (?:like|love|enjoy|agree|trust|care|value))|\bwhat is your age\b|\b(?:in )?(?:what|which) year\b"
)
WHICH_USE_PATTERN = (
    r"\bwhich\b.*\bdo you (?:currently )?(?:use|have|own)\b|\bwhich\b.*\bhave you (?:used|tried|bought|owned)\b"
)
COMPARISON_PATTERN = r" or |\b(?:more|most|prefer|main|mainly)\b"
LADDER_HIGH = ("a lot", "quite a lot", "a great deal", "very much", "extremely", "very", "completely")
LADDER_MID = ("somewhat", "moderately", "a fair amount", "fairly")
LADDER_LOW = ("a little", "slightly", "not much", "not very", "hardly")
LADDER_ZERO = ("not at all", "none", "never", "nothing")
ENGLISH_FUNCTION_WORDS = {
    "the", "a", "an", "you", "your", "do", "does", "did", "is", "are", "was", "were", "how", "what",
    "which", "who", "when", "where", "why", "to", "of", "in", "on", "for", "with", "have", "has", "i",
    "it", "this", "that", "and", "or", "any", "our", "we", "would", "please", "at", "be", "from",
}
# Words that are also common function words in German, Dutch, French, Spanish, Italian or Portuguese
# ("was", "in", "an", "a", "i", "on", "do", "is"); they do not count as evidence of English.
SHARED_FUNCTION_WORDS = {"a", "an", "i", "in", "on", "do", "is", "was"}
STRONG_ENGLISH_WORDS = (ENGLISH_FUNCTION_WORDS - SHARED_FUNCTION_WORDS) | {"not", "my", "about", "been", "there"}
ANSWER_INSTRUCTION_PATTERN = (
    r"(?:^|(?<=[.?!])\s+)(?:please )?(?:enter|type|write) (?:0|zero|a (?:whole )?number|the number|a figure)\b"
    r"[^.?!]*[.?!]?"
)
ROUTING_LINE_PATTERN = r"^\(\s*(?:if\b|skip\b|go to\b|goes to\b|only (?:if|for|shown)\b|shown (?:only|if|to)\b)[^)]*\)\.?$"
CONTINUOUS_UNIT_PATTERN = (
    r"\b(?:hours?|hrs?|minutes?|mins?|seconds?|secs?|kg|kilograms?|grams?|lbs?|km|kilomet(?:er|re)s?|miles?|"
    r"met(?:er|re)s?|lit(?:er|re)s?|gallons?|degrees?)\b"
)
DURATION_STEM_PATTERN = r"\bhow long\b|\bhow much time\b|\bfor how long\b"
DURATION_UNIT_PATTERN = r"\b(?:days?|weeks?|months?|years?)\b"
CENTS_PATTERN = r"\bcents?\b|\bpence\b"
NOT_CHECKED = (
    "Rules cannot judge: loaded wording outside the word lists, built-in assumptions, social "
    "desirability, question-order effects, whether options fit the audience, or whether a question "
    "serves the survey's decision. Review those by reading."
)


class InputError(Exception):
    """Raised for input the script refuses to guess about."""


# ---------------------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------------------
Q_RE = re.compile(r"^(\s{0,3})(?:\*\*)?(?:Q\s*)?(\d+)[.):]\s+(.*\S)\s*$", re.I)
ROW_RE = re.compile(r"^\s*([a-z])[.)]\s+(.*\S)\s*$")
OPT_RE = re.compile(r"^\s*(?:[-*+•○●]|\( ?\)|\[ ?\])\s+(.*\S)\s*$")
TYPE_RE = re.compile(r"\[(single|multi|open|text|number|scale|grid)(?:\s*[,:][^\]]*)?\]", re.I)
REQ_RE = re.compile(r"\[required\]|\(required\)|\*\s*$", re.I)
OPTIONAL_RE = re.compile(r"\[optional\]|\(optional\)", re.I)
TYPES = {"single", "multi", "open", "number", "scale", "grid"}
TYPE_ALIASES = {"text": "open"}
PLAIN_OPTION_MAX_WORDS = 8  # convention: a short unmarked line after a finished stem reads as an option


def norm(text):
    return text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')


def clean_stem(raw):
    """Return (text, explicit_type, required) from a raw question line."""
    text = norm(raw).strip()
    if text.endswith("**"):
        text = text[:-2].rstrip()
    qtype = None
    m = TYPE_RE.search(text)
    if m:
        qtype = m.group(1).lower()
        qtype = TYPE_ALIASES.get(qtype, qtype)
        text = TYPE_RE.sub("", text).strip()
    text = OPTIONAL_RE.sub("", text).strip()
    required = False
    while REQ_RE.search(text):
        required = True
        text = REQ_RE.sub("", text).strip()
    return text, qtype, required


def parse_markdown(text):
    """Return (questions, warnings, intro). Without any numbered question, each non-option line that ends
    in '?' is taken as a question and numbered 1, 2, 3 ..."""
    lines = text.splitlines()
    numbered = any(Q_RE.match(l) and not OPT_RE.match(l) for l in lines)
    questions, warnings, current, intro, intro_line, skipped = [], [], None, [], None, 0
    routed, pending, plain_options = [], [], set()

    def start(qid, raw, lineno, indent=0):
        stem, qtype, required = clean_stem(raw)
        question = {"id": qid, "text": stem, "type": qtype, "required": required, "line": lineno,
                    "options": [], "rows": [], "indent": indent}
        questions.append(question)
        return question

    def flush_pending():
        """One unmarked line after a stem continues the stem; two or more are read as options."""
        if not pending:
            return
        if len(pending) == 1 and not current["options"]:
            more, qtype, required = clean_stem(pending[0][1])
            current["text"] = (current["text"] + " " + more).strip()
            current["type"] = current["type"] or qtype
            current["required"] = current["required"] or required
        else:
            for lineno, raw in pending:
                current["options"].append({"text": norm(raw.strip()), "line": lineno})
            plain_options.add(current["id"])
        del pending[:]

    for lineno, line in enumerate(lines, 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        opt = OPT_RE.match(line)
        if current is not None and not opt and re.match(ROUTING_LINE_PATTERN, norm(line.strip()), re.I):
            routed.append(current["id"])  # skip logic written for the respondent view; not part of the stem
            continue
        if current is not None and not opt and re.match(r"^\s*(?:thank you|thanks)\b", line, re.I):
            flush_pending()
            current["done"] = True  # a closing line ends the questionnaire text; it is not part of a stem
            continue
        if numbered and not opt:
            m = Q_RE.match(line)
            indent = len(line) - len(line.lstrip())
            if m and current is not None and indent > current["indent"] and not pending:
                # an indented numbered line inside a question ("   1) Very satisfied") is an answer option
                opt = re.match(r"^\s*\d+[.)]\s+(.*\S)\s*$", line)
            elif m:
                if current is not None:
                    flush_pending()
                current = start(m.group(2), m.group(3), lineno, indent)
                continue
        row = ROW_RE.match(line) if current is not None and not opt else None
        if not numbered and not opt and not row and clean_stem(line)[0].endswith("?"):
            current = start(str(len(questions) + 1), line.strip(), lineno)
            continue
        if current is None:
            intro.append(norm(line.strip()))  # introduction before the first question
            intro_line = intro_line or lineno
            continue
        stem_only = clean_stem(line)[0] == "" and TYPE_RE.search(line)
        if stem_only:  # a line holding only a type tag such as "[number]" or "[text]"
            current["type"] = current["type"] or clean_stem(line)[1]
            current["done"] = True  # the answer box ends the question; later plain lines are notes
            continue
        if current.get("done") and not opt and not ROW_RE.match(line):
            continue
        if opt or row:
            flush_pending()
        if opt:
            current["options"].append({"text": norm(opt.group(1)), "line": lineno})
        elif row:
            current["rows"].append({"id": current["id"] + row.group(1), "text": norm(row.group(2)), "line": lineno})
        elif numbered and not current["rows"] and (pending or not current["options"]):
            plain = clean_stem(line)[0]
            finished = current["text"].rstrip().endswith(("?", ":"))
            if (finished or current["id"] in plain_options) and not plain.endswith("?") \
                    and len(plain.split()) <= PLAIN_OPTION_MAX_WORDS:
                pending.append((lineno, line))
                if len(pending) >= 2:
                    flush_pending()
            else:
                flush_pending()
                more, qtype, required = clean_stem(line)
                current["text"] = (current["text"] + " " + more).strip()
                current["type"] = current["type"] or qtype
                current["required"] = current["required"] or required
        elif numbered and current["id"] in plain_options and not current["rows"]:
            plain = clean_stem(line)[0]
            if not plain.endswith("?") and len(plain.split()) <= PLAIN_OPTION_MAX_WORDS:
                current["options"].append({"text": norm(line.strip()), "line": lineno})
        elif not numbered:
            skipped += 1
        # in numbered input, any other line after the options is a note and is ignored
    if current is not None:
        flush_pending()
    for q in questions:
        q.pop("indent", None)
        q.pop("done", None)
        if q["rows"] and not q["options"] and q["type"] != "grid":
            # lettered lines with no bulleted answer options are the options themselves ("a) Very satisfied")
            q["options"] = [{"text": r["text"], "line": r["line"]} for r in q["rows"]]
            q["rows"] = []
            warnings.append("question %s: lettered lines with no '-' options were read as answer options; "
                            "tag the question [grid] if they are grid rows" % q["id"])
    if plain_options:
        warnings.append("question(s) %s: unmarked lines after the question were read as answer options; "
                        "start each option with '- ' to be sure" % ", ".join(sorted(plain_options, key=_id_key)))
    if routed:
        warnings.append("skip logic found after question(s) %s; routing is not checked and the length "
                        "estimate counts every question unless --route-skip is given"
                        % ", ".join(sorted(dict.fromkeys(routed), key=_id_key)))
    if not numbered and questions:
        warnings.append("no question numbers found; each line ending in '?' was read as a question")
    if skipped:
        warnings.append("%d line(s) were not recognised as questions or options (no number and no '?'); "
                        "check them by hand" % skipped)
    return questions, warnings, ({"text": " ".join(intro), "line": intro_line} if intro else None)


QSF_HEADING_RE = re.compile(r"^###\s+(\S+)\s+\[([a-z-]+)\](?:\s+(required|request))?\s*$")
QSF_TYPES = {
    "single": "single", "dropdown": "single", "rank": "single", "sum": "single", "multi": "multi",
    "text": "open", "text-long": "open", "essay": "open", "form": "open", "matrix": "grid",
    "matrix-multi": "grid", "matrix-text": "grid", "slider": "grid", "nps": "single", "info": None,
}
QSF_MARK_RE = re.compile(r"\s*\{(?:text|exclusive|code:-?\d+|var:[^}]*)\}")
NPS_DEFAULT_LABELS = ("Not at all likely", "Extremely likely")


def is_qsf_markdown(text):
    """True for the Markdown that qsf-convert writes: questions start with '### tag [type]'."""
    return any(QSF_HEADING_RE.match(line) for line in text.splitlines())


def parse_qsf_markdown(text):
    """Read the survey Markdown of the qsf-convert skill (`### tag [type]` headings, `Rows:` / `Columns:`,
    `> skip:` and `> show if:` rules). Question IDs are the tags. `[info]` screens before the first question
    are the introduction; later ones are left out and counted in a warning."""
    questions, warnings, intro, intro_line = [], [], [], None
    current, target, labels, routed, info_later = None, "options", {}, [], 0
    in_comment = False
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if in_comment or line.startswith("<!--"):
            in_comment = "-->" not in line
            continue
        if line.startswith(("# ", "## ")):
            current = None  # a block heading ends the question before it
            continue
        if not line or line == "---":
            continue
        m = QSF_HEADING_RE.match(line)
        if m:
            qtype = QSF_TYPES.get(m.group(2), "single")
            current = {"id": m.group(1), "text": "", "type": qtype, "required": m.group(3) == "required",
                       "line": lineno, "options": [], "rows": [], "qsf_type": m.group(2), "info": qtype is None}
            target = "options"
            if not current["info"]:
                questions.append(current)
            elif questions:
                info_later += 1
            continue
        if current is None:
            continue
        if line.startswith(">"):
            rule = line[1:].strip()
            if rule.startswith(("skip:", "show if:")):
                routed.append(current["id"])
            elif rule.startswith("labels:"):
                labels[current["id"]] = [part.strip() for part in rule[len("labels:"):].split("|")]
            continue
        if line in ("Rows:", "Columns:"):
            target = "rows" if line == "Rows:" else "options"
            continue
        opt = re.match(r"^-\s+(.*\S)\s*$", line)
        if opt:
            label = norm(QSF_MARK_RE.sub("", opt.group(1)).strip())
            if current["info"]:
                continue
            if current["qsf_type"] == "slider":
                target = "rows"  # each slider bar is rated on the same scale, like a grid row
            if target == "rows":
                current["rows"].append({"id": current["id"] + "abcdefghijklmnopqrstuvwxyz"[len(current["rows"]) % 26],
                                        "text": label, "line": lineno})
            else:
                current["options"].append({"text": label, "line": lineno})
            continue
        line = line[1:] if line.startswith("\\") else line
        line = re.sub(r"<[^>]+>", "", norm(line)).strip()
        if current["info"] and not questions:
            intro.append(line)
            intro_line = intro_line or lineno
        elif not current["info"]:
            current["text"] = (current["text"] + " " + line).strip()
    for q in questions:
        if q["qsf_type"] == "nps":
            given = labels.get(q["id"], [])
            low = given[0] if given else NPS_DEFAULT_LABELS[0]
            high = given[-1] if len(given) >= 2 else NPS_DEFAULT_LABELS[1]
            q["options"] = ([{"text": "0 - %s" % low, "line": None}] + [{"text": str(n), "line": None} for n in range(1, 10)]
                            + [{"text": "10 - %s" % high, "line": None}])
        elif q["qsf_type"] in ("matrix-text", "slider", "form"):
            q["options"] = []  # text boxes, slider bars and form fields are not answer options
            if q["qsf_type"] == "form":
                q["rows"] = []
        if not q["text"]:
            warnings.append("question %s has no text" % q["id"])
        for key in ("qsf_type", "info"):
            q.pop(key, None)
    warnings.append("read as qsf-convert Markdown: %d question(s), IDs are the tags; matrix rows are grid rows; "
                    "slider bars are grid rows; text-box matrix and form fields are not checked as options"
                    % len(questions))
    if info_later:
        warnings.append("%d descriptive text screen(s) after the first question were not checked" % info_later)
    if routed:
        warnings.append("skip or display logic on %s; routing is not checked and the length estimate counts every "
                        "question unless --route-skip is given" % ", ".join(dict.fromkeys(routed)))
    return questions, warnings, ({"text": " ".join(intro), "line": intro_line} if intro else None)


def _id_key(qid):
    m = re.match(r"(\d+)", str(qid))
    return (int(m.group(1)) if m else 10 ** 9, str(qid))


def parse_json(text):
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise InputError("not valid JSON: %s" % exc)
    items = data.get("questions") if isinstance(data, dict) else data
    intro = None
    if isinstance(data, dict):
        raw_intro = data.get("intro", data.get("introduction", data.get("description")))
        if raw_intro is not None and not isinstance(raw_intro, str):
            raise InputError('"intro" must be text')
        if raw_intro and raw_intro.strip():
            intro = {"text": norm(raw_intro.strip()), "line": None}
    if not isinstance(items, list):
        raise InputError('JSON must be a list of questions or an object with a "questions" list')
    questions = []
    for i, item in enumerate(items, 1):
        if not isinstance(item, dict):
            raise InputError("question %d is not an object" % i)
        raw = item.get("text", item.get("question"))
        if not isinstance(raw, str) or not raw.strip():
            raise InputError('question %d has no "text"' % i)
        stem, tagged, starred = clean_stem(raw)
        qtype = item.get("type", tagged)
        if qtype is not None and not isinstance(qtype, str):
            raise InputError('question %d: "type" must be text, not %s' % (i, type(qtype).__name__))
        if qtype is not None:
            qtype = TYPE_ALIASES.get(qtype.strip().lower(), qtype.strip().lower())
        if qtype is not None and qtype not in TYPES:
            raise InputError("question %d has unknown type %r (use one of %s)" % (i, qtype, ", ".join(sorted(TYPES))))
        required = item.get("required", starred)
        if isinstance(required, str) and required.strip().lower() in ("true", "yes", "false", "no"):
            required = required.strip().lower() in ("true", "yes")
        if isinstance(required, int) and not isinstance(required, bool) and required in (0, 1):
            required = bool(required)
        if not isinstance(required, bool):
            raise InputError('question %d: "required" must be true or false, not %r' % (i, required))
        raw_id = item.get("id", i)
        if isinstance(raw_id, bool) or not isinstance(raw_id, (str, int)) or not str(raw_id).strip():
            raise InputError('question %d: "id" must be text or a whole number' % i)
        qid = str(raw_id).strip()
        options, rows = [], []
        for key, target in (("options", options), ("rows", rows)):
            values = item.get(key, [])
            if not isinstance(values, list):
                raise InputError('question %d: "%s" must be a list' % (i, key))
            for j, value in enumerate(values):
                if isinstance(value, dict):
                    value = value.get("text", value.get("label"))
                if not isinstance(value, (str, int, float)) or isinstance(value, bool) or not str(value).strip():
                    raise InputError('question %d: every entry of "%s" needs text' % (i, key))
                entry = {"text": norm(str(value)), "line": None}
                if key == "rows":
                    entry["id"] = qid + "abcdefghijklmnopqrstuvwxyz"[j % 26]
                target.append(entry)
        questions.append({"id": qid, "text": stem, "type": qtype, "required": required,
                          "line": None, "options": options, "rows": rows})
    return questions, [], intro


def load(path, fmt):
    try:
        text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError) as exc:
        raise InputError("cannot read %s: %s" % (path, exc))
    if text.startswith("\ufeff"):  # a UTF-8 byte order mark from Windows editors and Excel exports
        text = text[1:]
    if not text.strip():
        raise InputError("input is empty")
    if fmt == "auto":
        fmt = ("json" if path.lower().endswith(".json") or text.lstrip()[:1] in "[{"
               else "qsf-md" if is_qsf_markdown(text) else "md")
    parsers = {"json": parse_json, "qsf-md": parse_qsf_markdown, "md": parse_markdown}
    questions, warnings, intro = parsers[fmt](text)
    if not questions:
        raise InputError("no questions found: number each question (1. ...) or end each question line with '?', "
                         "and list options as '- ' items")
    seen = set()
    for q in questions:
        if q["id"] in seen:
            warnings.append("question number %s appears more than once" % q["id"])
        seen.add(q["id"])
        if len(q["options"]) == 1:
            warnings.append("question %s has a single answer option; check the input format" % q["id"])
    if not any(q["options"] for q in questions):
        warnings.append("no answer options found; only wording rules could run")
    infer_types(questions)
    return questions, warnings, intro


def infer_types(questions):
    """Fill in the type of questions that carry no [type] tag."""
    for q in questions:
        if q["type"] is None:
            if q["rows"]:
                q["type"] = "grid"
            elif not q["options"]:
                # a count, an amount, an age or a year is typed as a number, not written as free text
                q["type"] = "number" if re.search(NUMERIC_ENTRY_PATTERN, q["text"], re.I) else "open"
            elif re.search(MULTI_PATTERN, q["text"], re.I):
                q["type"] = "multi"
            else:
                q["type"] = "single"


# ---------------------------------------------------------------------------------------
# Answer-option analysis
# ---------------------------------------------------------------------------------------
def special_kind(label):
    low = label.lower().strip()
    for kind, pattern in SPECIAL.items():
        if re.search(pattern, low):
            return kind
    return None


def special_kinds(label):
    """All opt-out kinds a label carries; two or more means a combined opt-out such as 'None / Other'."""
    low = label.lower().strip().replace("n/a", "not applicable")
    parts = [p for p in re.split(r"\s*/\s*|\s+or\s+|\s*,\s*", low) if p]
    kinds = [special_kind(p) for p in parts]
    if len(parts) >= 2 and all(kinds) and len(set(kinds)) >= 2 and all(len(p.split()) <= 4 for p in parts):
        return list(dict.fromkeys(kinds))
    whole = special_kind(label)
    return [whole] if whole else []


def polarity(label):
    """Return (balance, direction, family). balance/direction are -1, 0 or +1."""
    low = label.lower()
    words = re.findall(r"[a-z]+", low)
    pos = [w for w in words if w in POSITIVE]
    neg = [w for w in words if w in NEGATIVE]
    family = NEGATIVE[neg[0]] if neg else (POSITIVE[pos[0]] if pos else None)
    if low.startswith("neither") or (pos and neg):
        return 0, 0, family
    if neg:
        return -1, -1, family
    if re.match(r"not at all\b", low):
        return 0, -1, family  # the zero point of a unipolar scale, not a negative pole
    if re.match(r"(?:not|never|no)\b", low):
        return (-1 if pos else 0), -1, family
    if pos:
        return 1, 1, family
    if low.startswith(INTENSITY_HIGH):
        return 0, 1, None
    if low.startswith(INTENSITY_LOW):
        return 0, -1, None
    return 0, 0, None


NUM = r"(-?\d[\d,]*(?:\.\d+)?)\s*([km])?\b"
UNIT = r"(?:\s*%|\s+[a-z%/.]+){0,3}"


def _number(digits, suffix):
    value = float(digits.replace(",", ""))
    return value * {"k": 1e3, "m": 1e6, None: 1}[suffix]


def parse_range(label):
    """Return (lo, hi, lo_strict, hi_strict) or None. Strict bounds are resolved by the caller."""
    low = re.sub(r"[$€£]", "", label.lower().replace("−", "-")).strip()
    low = re.sub(r"\s+", " ", low)
    inf = math.inf
    m = re.match(r"^" + NUM + r"\s*%?\s*(?:-|–|—|to)\s*(?:under|less than|below|fewer than|<)\s*" + NUM + UNIT + r"$", low)
    if m:  # "1 to under 5 hours": includes 1, excludes 5
        return (_number(m.group(1), m.group(2)), _number(m.group(3), m.group(4)), False, True)
    m = re.match(r"^(?:under|below|less than|fewer than|<)\s*" + NUM, low)
    if m and not low.startswith("<="):
        return (-inf, _number(m.group(1), m.group(2)), False, True)
    m = re.match(r"^(?:up to|at most|<=)\s*" + NUM, low) or re.match(r"^" + NUM + r".{0,12}\bor (?:less|fewer|under|younger|below)\b", low)
    if m:
        return (-inf, _number(m.group(1), m.group(2)), False, False)
    m = re.match(r"^(?:over|above|more than|greater than|>)\s*" + NUM, low)
    if m and not low.startswith(">="):
        return (_number(m.group(1), m.group(2)), inf, True, False)
    m = (re.match(r"^(?:at least|>=)\s*" + NUM, low) or re.match(r"^" + NUM + r"\s*\+", low)
         or re.match(r"^" + NUM + r".{0,12}\b(?:or|and) (?:more|older|over|above|up)\b", low))
    if m:
        return (_number(m.group(1), m.group(2)), inf, False, False)
    m = re.match(r"^" + NUM + r"\s*%?\s*(?:-|–|—|to)\s*" + NUM + UNIT + r"$", low)
    if m:
        return (_number(m.group(1), m.group(2)), _number(m.group(3), m.group(4)), False, False)
    m = re.match(r"^" + NUM + UNIT + r"$", low)
    if m:
        value = _number(m.group(1), m.group(2))
        return (value, value, False, False)
    return None


def range_step(labels, stem=""):
    decimals = 2 if re.search(CENTS_PATTERN, stem.lower()) else 0
    for label in labels:
        for frac in re.findall(r"\d\.(\d+)", label):
            decimals = max(decimals, len(frac))
    return 10 ** -decimals


def is_continuous(labels, stem=""):
    """A measure that can take any value between two whole numbers: durations in hours or minutes, weights,
    distances, or any duration asked with 'how long'. Counts, ages in years and money are not continuous."""
    text = " ".join(labels).lower() + " " + stem.lower()
    if re.search(CONTINUOUS_UNIT_PATTERN, text):
        return True
    return bool(re.search(DURATION_STEM_PATTERN, stem.lower()) and re.search(DURATION_UNIT_PATTERN, text))


def check_ranges(labels, stem=""):
    """Return a list of (kind, matched text) for overlap, gap, continuous_gap and reversed ranges.

    Ranges are swept in order of their lower bound against the furthest upper bound seen so far, so a wide
    range that contains later ones is reported as overlapping each of them and does not hide or invent gaps.
    For a continuous measure, two ranges that meet at whole numbers ("5-6 hours / 7-8 hours") leave the values
    in between (6.5 hours) without an option: a continuous_gap."""
    step = range_step(labels, stem)
    eps = step / 1000.0
    raw, problems = [], []
    for label in labels:
        lo, hi, lo_open, hi_open = parse_range(label)
        if lo > hi + eps:
            problems.append(("reversed", label))
            continue
        raw.append((lo, hi, lo_open, hi_open, label))
    raw.sort(key=lambda r: (r[0], r[2], r[1]))
    continuous = is_continuous(labels, stem)
    furthest = None  # (closed upper bound, raw upper bound, raw upper bound open, label)
    for lo, hi, lo_open, hi_open, label in raw:
        lo_c = lo + step if lo_open else lo
        hi_c = hi - step if hi_open else hi
        if furthest is not None:
            f_hi_c, f_hi, f_open, f_label = furthest
            pair = "%s / %s" % (f_label, label)
            if lo_c <= f_hi_c + eps:
                problems.append(("overlap", pair))
            elif lo_c > f_hi_c + step + eps:
                problems.append(("gap", pair))
            elif continuous and (lo > f_hi + eps or (abs(lo - f_hi) <= eps and lo_open and f_open)):
                problems.append(("continuous_gap", pair))
        if furthest is None or hi_c > furthest[0] + eps:
            furthest = (hi_c, hi, hi_open, label)
    return problems


TIME_UNIT_PATTERN = r"\b(second|minute|hour|day|week|month|year)s?\b"


def time_units(labels):
    """The distinct time units named in the labels; ranges in mixed units ("6 months to 1 year") are not compared."""
    return {m.group(1) for label in labels for m in re.finditer(TIME_UNIT_PATTERN, label.lower())}


def analyse_options(q):
    labels = [o["text"] for o in q["options"]]
    specials = {}
    plain, combined = [], []
    for label in labels:
        kinds = special_kinds(label)
        for kind in kinds:
            specials.setdefault(kind, label)
        if len(kinds) >= 2:
            combined.append(label)
        if not kinds:
            plain.append(label)
    info = {"plain": plain, "specials": specials, "combined": combined, "kind": "none", "family": None,
            "direction": 0, "zero": "none" in specials, "neutrals": 0, "ranged": []}
    if not plain:
        return info
    if all(CODE_PREFIX_RE.match(p) for p in plain):
        # Numbered verbal labels are read by their words: the codes are not the scale's labels.
        plain = [CODE_PREFIX_RE.sub("", p) for p in plain]
        info["plain"] = plain
    lowered = [p.lower().strip() for p in plain]
    ranges = [parse_range(p) for p in plain]
    pols = [polarity(p) for p in plain]
    info["neutrals"] = sum(1 for p in pols if p[0] == 0)
    info["zero"] = info["zero"] or any(re.match(ZERO_OPTION_PATTERN, l) for l in lowered) or any(r and r[0] <= 0 for r in ranges)
    scale_labels = [p for p in pols if p[2]]
    stripped = [re.sub(r"^(?:very|quite|fairly) ", "", l) for l in lowered]
    parsed = [r for r in ranges if r]
    unparsed = len(ranges) - len(parsed)
    if set(lowered) <= {"yes", "no"} and len(set(lowered)) == 2:
        info["kind"] = "yesno"
    elif (len(parsed) >= 2 and any(r[0] != r[1] for r in parsed)
          and unparsed <= max(1, len(plain) // 3) and len(time_units(plain)) <= 1):
        # ranges, allowing one or two options in words ("It varies", "Never") that the parser cannot read
        info["kind"] = "numeric_range"
        info["ranged"] = [p for p, r in zip(plain, ranges) if r]
    elif all(re.match(r"^-?\d", l) for l in lowered):
        info["kind"] = "numeric_scale"
    elif len(scale_labels) >= 2 or sum(1 for l in lowered if l.startswith(INTENSITY_LOW + INTENSITY_HIGH)) >= 2:
        info["kind"] = "rating"
        info["family"] = scale_labels[0][2] if scale_labels else "intensity: " + lowered[-1].split()[-1]
        info["direction"] = (pols[0][1] > pols[-1][1]) - (pols[0][1] < pols[-1][1])
        if (any(re.match(r"not at all\b", l) for l in lowered)
                and any(re.match(r"not (?:very|too|so)\b", l) for l in lowered)):
            # "Very / Somewhat / Not very / Not at all likely": with a "not very" step below the middle, "not at
            # all" is the far end of that side, not a zero point outside it.
            pols = [(-1, d, f) if re.match(r"not at all\b", l) else (b, d, f)
                    for (b, d, f), l in zip(pols, lowered)]
        info["positives"] = sum(1 for p in pols if p[0] > 0)
        info["negatives"] = sum(1 for p in pols if p[0] < 0)
        info["midpoint"] = any(l == "neutral" or l.startswith("neither") for l in lowered)
    elif sum(1 for s in stripped if s in VAGUE_OPTION_WORDS) >= 2:
        info["kind"] = "frequency"
    elif 2 * sum(1 for l in lowered if re.search(r"\d", l) or ORDINAL_RE.match(l)) >= max(2, len(lowered)):
        info["kind"] = "ordinal"  # amounts or durations the range parser cannot read; list rules do not apply
    else:
        info["kind"] = "nominal"
    return info


# ---------------------------------------------------------------------------------------
# Wording rules (run on a question stem or a grid row)
# ---------------------------------------------------------------------------------------
def strip_fixed(low, pairs=True):
    low = re.sub(r"\([^)]*\)", " ", low)
    low = re.sub(r"\bbetween\b[^,;?]*?\band\b", " ", low)
    for phrase in FIXED_PHRASES:
        low = low.replace(phrase, " ")
    for a, b in ANTONYM_PAIRS if pairs else []:
        low = re.sub(r"\b%s or %s\b" % (a, b), " ", low)
        low = re.sub(r"\b%s or %s\b" % (b, a), " ", low)
    return low


def is_english(text):
    """True when the text reads as English. Mostly non-Latin letters means not English. Two words or fewer
    are too short to tell and pass; longer text needs English function words that other languages do not
    share ("the", "you", "how"): one for up to seven words, two above that."""
    letters = [c for c in text if c.isalpha()]
    if letters and sum(1 for c in letters if c < "\u0250") < 0.8 * len(letters):
        return False
    words = re.findall(r"[^\W\d_]+", text.lower())
    if len(words) <= 2:
        return True
    hits = sum(1 for w in words if w in STRONG_ENGLISH_WORDS)
    return hits >= (1 if len(words) <= 7 else 2)


def strip_instructions(text):
    """Remove answer instructions ("Enter 0 if none.") so the wording rules read the question itself."""
    return re.sub(ANSWER_INSTRUCTION_PATTERN, "", text, flags=re.I).strip() or text


def wording_findings(text, kind, max_words):
    """Yield (rule, sub-kind, severity, match, why) for one stem or grid row."""
    low = text.lower()
    bare = strip_fixed(low)

    joined = ["%s and %s" % m for m in re.findall(r"\b([a-z'-]+) and ([a-z'-]+)\b", bare)]
    if kind in ("rating", "yesno", "numeric_scale"):
        joined += ["%s or %s" % m for m in re.findall(r"\b([a-z'-]+) or ([a-z'-]+)\b", bare)]
    if joined:
        yield ("SB001", "joined", "medium", "; ".join(joined),
               "The stem joins two things; a respondent who would answer them differently has no accurate answer. "
               "Ignore if the phrase names one concept.")

    hits = [m.group(0) for p in LEADING_PATTERNS for m in re.finditer(p, low)]
    if hits:
        yield ("SB002", "wording", "high", "; ".join(hits),
               "The phrase suggests the expected answer or adds an evaluation. Reword neutrally and offer both sides.")

    hits = [m.group(0) for m in re.finditer(ABSOLUTE_PATTERN, low)]
    if hits:
        yield ("SB003", "absolute", "medium", "; ".join(hits),
               "Taken literally, one exception makes the answer 'no'. Ask how often or how many times in a set period.")

    hits = [m.group(0) for p in HYPOTHETICAL_PATTERNS for m in re.finditer(p, low)]
    if hits:
        yield ("SB004", "hypothetical", "medium", "; ".join(hits),
               "Answers about hypothetical or future behaviour overstate real behaviour. Ask about past behaviour; "
               "if intent must be asked, report it as stated intent, not as a forecast of what people will do.")

    unpaired = strip_fixed(low, pairs=False)
    negations = [m.group(0) for m in re.finditer(NEGATION_PATTERN, unpaired)]
    negative_words = [w for w in re.findall(r"[a-z]+", unpaired) if w in NEGATIVE_WORDS]
    if negations and len(negations) + len(negative_words) >= 2:
        yield ("SB005", "double", "high", "; ".join(negations + negative_words),
               "Two negations in one question: respondents cannot tell what 'yes' or 'agree' means. State it positively.")
    elif len(negations) == 1 and kind in ("yesno", "agree"):
        yield ("SB005", "single", "medium", negations[0],
               "A negated statement with yes/no or agree/disagree answers: 'no' or 'disagree' becomes a double "
               "negative. State it positively.")

    hits = [m.group(0) for m in re.finditer(VAGUE_STEM_PATTERN, low)]
    if hits:
        yield ("SB006", "stem", "low", "; ".join(hits),
               "Respondents read this word as different amounts. Give a reference period and ask for a count.")

    hits = []
    if text != text.upper():
        for m in re.finditer(r"\b[A-Z][A-Z0-9]{1,5}\b", text):
            token = m.group(0)
            defined = bool(re.search(r"\(\s*%s\s*\)" % re.escape(token), text)) or text[m.end():].lstrip().startswith("(")
            if sum(c.isalpha() for c in token) >= 2 and token not in KNOWN_ACRONYMS and not defined:
                hits.append(token)
    hits += [m.group(0) for m in re.finditer(JARGON_PATTERN, low)]
    if hits:
        yield ("SB007", "term", "low", "; ".join(dict.fromkeys(hits)),
               "Undefined acronym or trade term. Spell it out or define it unless every respondent uses it daily.")

    words = [w for w in text.split() if re.search(r"\w", w)]
    if len(words) > max_words:
        yield ("SB008", "words", "low", "%d words" % len(words),
               "Longer than %d words. Move context to an introduction line or split the question." % max_words)

    hits = [m.group(0) for m in re.finditer(SENSITIVE_BEHAVIOUR_PATTERN, low)]
    if hits:
        yield ("SB021", "behaviour", "low", "; ".join(dict.fromkeys(hits)),
               "Answers about disapproved or admired behaviour drift toward what looks good. Use neutral framing, "
               "self-completion and real anonymity, and make the question optional; for high stakes consider an "
               "indirect method such as a list experiment.")

    signals = []
    if re.search(CONDITIONAL_PATTERN, low):
        signals.append("conditional clause")
    if re.search(EXCLUSION_PATTERN, low):
        signals.append("exclusion")
    if any(len(p.split()) >= PARENTHETICAL_WORDS for p in re.findall(r"\(([^)]*)\)", text)):
        signals.append("long parenthetical")
    if text.count(",") >= INLINE_LIST_COMMAS:
        signals.append("inline list")
    if len(signals) >= LOAD_SIGNALS:
        yield ("SB026", "load", "low", "; ".join(signals),
               "Several things to hold in mind at once. Move the condition to a filter question and the "
               "definition or list to a separate line.")


# ---------------------------------------------------------------------------------------
# Length estimate
# ---------------------------------------------------------------------------------------
def question_points(q):
    if q["type"] == "grid":
        base = POINTS["per_grid_row"] * max(len(q["rows"]), 1)
    elif q["type"] == "multi":
        base = POINTS["per_two_multi_options"] * len(q["options"]) / 2.0
    elif q["type"] == "open":
        base = POINTS["open"]
    elif q["type"] == "number":
        base = POINTS["number"]
    else:
        base = POINTS["single"]
    sentences = len(re.findall(r"[.?!]+(?:\s|$)", q["text"])) or 1
    return base + sentences // SENTENCES_PER_POINT


def intro_points(text):
    """Reading time of the introduction: 1 point per three sentences, rounded up (it has no base point)."""
    sentences = len(re.findall(r"[.?!]+(?:\s|$)", text)) or 1
    return float(math.ceil(sentences / float(SENTENCES_PER_POINT)))


# ---------------------------------------------------------------------------------------
# Lint
# ---------------------------------------------------------------------------------------
def content_words(text):
    return {w for w in re.findall(r"[a-z]{3,}", text.lower())
            if w not in FILTER_STOP_WORDS and w not in ENGLISH_FUNCTION_WORDS}


def lint(questions, max_words=MAX_WORDS, max_options=MAX_OPTIONS, ignore=(), intro=None,
         max_grid_rows=MAX_GRID_ROWS, max_open=MAX_OPEN, phone=False, keep=(), route_skip=(), language="auto"):
    findings, unchecked = [], []
    lexical = set(POSITIVE.values()) | set(NEGATIVE.values())

    def english_text(text):
        return {"en": True, "other": False}.get(language, None) if language != "auto" else is_english(text)

    def add(q, rule, sub, severity, match, why, qid=None, line=None):
        if q is None:
            question, where = qid, line
        else:
            question, where = (qid, line) if qid else (q["id"], q["line"])
        findings.append({"question": question, "line": where, "rule": rule, "name": RULES[rule][0], "kind": sub,
                         "severity": severity, "match": match, "why": why})

    # SB024: introduction
    if intro:
        low = intro["text"].lower()
        hits = [m.group(0) for p in LEADING_PATTERNS + [HYPOTHESIS_PATTERN] for m in re.finditer(p, low)]
        if hits:
            add(None, "SB024", "leading", "medium", "; ".join(hits),
                "The introduction cites an authority or says what the study hopes to find. Describe the topic only.",
                qid="intro", line=intro["line"])
        if not re.search(TIME_ESTIMATE_PATTERN, low):
            add(None, "SB024", "no_time_estimate", "low", "no time or length estimate",
                "Say how long the survey takes or how many questions it has.", qid="intro", line=intro["line"])

    infos = [analyse_options(q) for q in questions]
    any_options = any(q["options"] for q in questions)  # a paste of bare questions has no known types
    filters = []  # content words of earlier yes/no and select-all questions
    for index, (q, info) in enumerate(zip(questions, infos)):
        plain, specials, kind = info["plain"], info["specials"], info["kind"]
        is_agree = kind == "rating" and info["family"] == "agreement"
        low = q["text"].lower()

        # wording rules on the stem and on each grid row
        wording_kind = "agree" if is_agree else kind
        targets = [(q["id"], q["line"], q["text"])] + [(r["id"], r["line"], r["text"]) for r in q["rows"]]
        for qid, line, text in targets:
            if not english_text(text):
                unchecked.append({"question": qid, "line": line,
                                  "reason": "not read as English (--language other, or no common English words); "
                                            "wording rules skipped"})
                continue
            for rule, sub, severity, match, why in wording_findings(strip_instructions(text), wording_kind, max_words):
                add(q, rule, sub, severity, match, why, qid=qid, line=line)

        if kind == "frequency":
            vague = [p for p in plain if re.sub(r"^(?:very|quite|fairly) ", "", p.lower().strip()) in VAGUE_OPTION_WORDS]
            add(q, "SB006", "options", "low", "; ".join(vague),
                "Vague frequency labels mean different amounts to different people. Offer counts for a set period.")

        if (kind == "rating" and info.get("midpoint") and not (info["positives"] and info["negatives"])
                and max(info["positives"], info["negatives"]) >= 2):
            add(q, "SB009", "balance", "high",
                "%d positive vs %d negative labels around a midpoint" % (info["positives"], info["negatives"]),
                "A scale with a neutral midpoint is two-sided: offer the same number of labels on each side.")
        if kind == "rating" and info["positives"] and info["negatives"] and info["positives"] != info["negatives"]:
            lows = {p.lower().strip() for p in plain}
            established = {"excellent", "fair", "poor"} <= lows
            add(q, "SB009", "balance", "low" if established else "high",
                "%d positive vs %d negative labels" % (info["positives"], info["negatives"]),
                "Excellent/good/fair/poor is an established unbalanced scale; keep it only for comparability."
                if established else "Offer the same number of labels on each side of the midpoint.")

        # SB009 on amount ladders: no zero end and more labels at the high end than at the low end
        if kind in ("rating", "ordinal") and len(plain) >= 3 and not info.get("positives") and not info.get("negatives"):
            lows = [p.lower().strip() for p in plain]
            steps = ["zero" if l.startswith(LADDER_ZERO) else "low" if l.startswith(LADDER_LOW)
                     else "high" if l.startswith(LADDER_HIGH) else "mid" if l.startswith(LADDER_MID) else None
                     for l in lows]
            if all(steps) and "zero" not in steps and steps.count("high") > steps.count("low"):
                add(q, "SB009", "ladder", "medium",
                    "%d high vs %d low labels, no zero point" % (steps.count("high"), steps.count("low")),
                    "The scale has more steps at the high end and no 'Not at all' end. Start at zero and space the labels evenly.")

        if kind == "numeric_range":
            why = {"overlap": "A value on the shared boundary fits two options. Make the ranges mutually exclusive.",
                   "gap": "Some values fit no option. Close the gap.",
                   "continuous_gap": "The measure is continuous, so values between the ranges (such as 6.5 hours "
                                     "between 5-6 and 7-8) fit no option. Write 'under N', 'N to under M' and 'M or "
                                     "more', or ask for the number itself.",
                   "reversed": "The lower bound is above the upper bound."}
            problems = check_ranges(info["ranged"], q["text"])
            for sub in ("overlap", "gap", "continuous_gap", "reversed"):
                matches = [m for k, m in problems if k == sub]
                if matches:
                    add(q, "SB010", sub, CONTINUOUS_GAP_SEVERITY if sub == "continuous_gap" else "high",
                        "; ".join(matches), why[sub])

        if q["type"] == "multi" and "none" not in specials:
            add(q, "SB011", "none", "medium", "no 'None of these' option",
                "In a select-all question, a blank answer cannot be told apart from 'none'. Add an exclusive 'None of these'.")
        which_use = (kind == "nominal" and len(plain) >= 2 and re.search(WHICH_USE_PATTERN, low)
                     and not re.search(COMPARISON_PATTERN, low))
        if which_use and q["type"] != "multi" and "none" not in specials:
            add(q, "SB011", "none", "low", "no 'None of these' option",
                "Someone who uses, has or owns none of the listed items cannot answer. Add 'None of these' "
                "or ask a filter question first.")
        if kind == "nominal" and (len(plain) >= 4 or which_use) and "other" not in specials:
            add(q, "SB011", "other", "low", "no 'Other' option",
                "If the list may not cover every respondent, add 'Other (please specify)'. Ignore if the list is complete.")
        if kind == "yesno" and "dk" not in specials and re.search(THIRD_PARTY_PATTERN, low):
            add(q, "SB011", "dk", "low", "no 'Not sure' option",
                "The question asks about a fact the respondent may not know. Add 'Not sure' unless it is a screener.")

        if kind == "nominal" and len(plain) > max_options:
            add(q, "SB013", "count", "low", "%d options" % len(plain),
                "More than %d options%s. Group them, use a dropdown or search, or randomise the order."
                % (max_options, " for a list read aloud" if phone else ""))

        if is_agree and info["positives"] and info["negatives"]:
            if q["rows"]:
                add(q, "SB014", "grid", "medium", "agree/disagree grid, %d rows" % len(q["rows"]),
                    "A battery of agree/disagree statements invites agreeing and straight-lining. Ask each item "
                    "directly with its own answer options.")
            else:
                add(q, "SB014", "single", "low", "agree/disagree options",
                    "Ask the question directly ('How easy or difficult ...') with item-specific options.")

        sensitive = re.search(SENSITIVE_PATTERN, low)
        if q["required"] and sensitive and "pnts" not in specials:
            add(q, "SB016", "required", "medium", sensitive.group(0),
                "Required sensitive question with no 'Prefer not to say'. Forcing an answer raises drop-out.")

        # SB017: reference period and recall
        english = english_text(q["text"])
        counted = re.search(FREQ_COUNT_PATTERN, low)
        asked = counted or re.search(HAVE_YOU_PATTERN, low)
        if english and asked and not re.search(TIME_PATTERN, low):
            add(q, "SB017", "no_period", "low", asked.group(0),
                "No reference period. Name one ('in the past 7 days') so that everyone answers about the same time span.")
        elif english and counted and re.search(LONG_WINDOW_PATTERN, low):
            add(q, "SB017", "long_window", "low", re.search(LONG_WINDOW_PATTERN, low).group(0),
                "A long recall window for a count. Shorten the period for frequent events; keep it for rare, memorable ones.")

        # SB018: built-in assumption
        mine = content_words(q["text"])
        filtered = any(mine & earlier for earlier in filters)
        if english and q["options"] and kind != "yesno" and not info["zero"] and not filtered:
            behaviour = re.search(ASSUME_BEHAVIOUR_PATTERN, low)
            experience = re.search(ASSUME_EXPERIENCE_PATTERN, low)
            if behaviour:
                add(q, "SB018", "behaviour", "medium", behaviour.group(0),
                    "Assumes the respondent does this, with no 'Never' or 'Does not apply' answer and no earlier filter "
                    "question. Add one of them.")
            elif experience and not re.search(r"\boverall\b|\bin general\b", low):
                add(q, "SB018", "experience", "low", experience.group(0),
                    "Assumes the respondent has used or experienced this. Add 'I have not used it' or a filter question "
                    "first, unless everyone surveyed has.")
        if kind == "yesno" or q["type"] == "multi":
            filters.append(mine)

        # SB019: stem and options
        how = re.search(r"\bhow (satisfied|dissatisfied|often|frequently|likely|unlikely|easy|difficult|hard)\b", low)
        if english and how and plain:
            expected = HOW_FAMILY[how.group(1)]
            family = info["family"] if kind == "rating" and info["family"] in lexical else None
            if kind == "yesno" or (family and family != expected) or (kind == "frequency" and expected != "frequency"):
                add(q, "SB019", "mismatch", "high", "%s / %s; %s" % (how.group(0), plain[0], plain[-1]),
                    "The question asks for a degree of %s but the options answer something else. Make the options "
                    "match the question." % expected)
            elif (how.group(1) in ONE_SIDED and not re.search(ONE_SIDED[how.group(1)], low) and kind == "rating"
                    and info["positives"] and info["negatives"]):
                add(q, "SB019", "one_sided", "low", how.group(0),
                    "The stem names only one end of a two-sided scale. Name both ('How satisfied or dissatisfied ...').")
        elif (english and re.search(CLOSED_STEM_PATTERN, low) and " or " not in low and kind == "rating"
                and info["family"] in lexical):
            roots = {w[:5] for p in plain for w in re.findall(r"[a-z]+", p.lower()) if w in POSITIVE or w in NEGATIVE}
            if not any(root in low for root in roots):
                add(q, "SB019", "closed_stem", "medium", "%s / %s; %s" % (" ".join(low.split()[:2]), plain[0], plain[-1]),
                    "A yes/no question with a rating scale. Ask 'How ...' or offer Yes / No.")

        # SB020: numeric scale with no verbal labels
        if english and not re.search(ANCHOR_PATTERN, low) and not re.search(r"\bhow many\b|\bnumber of\b", low):
            bare = [p.strip() for p in plain]
            if kind == "numeric_scale" and len(bare) >= 3 and all(re.fullmatch(r"\d+", b) for b in bare):
                numbers = [int(b) for b in bare]
                steps = {b - a for a, b in zip(numbers, numbers[1:])}
                if steps in ({1}, {-1}) and min(numbers) in (0, 1):
                    add(q, "SB020", "unlabelled", "medium", "%d to %d with no labels" % (min(numbers), max(numbers)),
                        "No point of the scale has a verbal label. Label the points, or at least both ends.")
            elif q["type"] == "scale" and not q["options"]:
                add(q, "SB020", "unlabelled", "medium", "scale with no labelled points",
                    "The scale's points are not described. Label the points, or at least both ends.")

        # SB028: the same option twice
        seen, dups = {}, []
        for o in q["options"]:
            key = re.sub(r"[\s.,;:!?]+", " ", o["text"].lower()).strip()
            if key in seen and key not in dups:
                dups.append(key)
            seen.setdefault(key, o["text"])
        if dups:
            add(q, "SB028", "duplicate", "high", "; ".join(seen[k] for k in dups),
                "The same answer option appears twice. Remove the copy and check which option it replaced.")

        # SB022: combined opt-outs
        if info["combined"]:
            add(q, "SB022", "combined", "medium", "; ".join(info["combined"]),
                "One option merges different answers. Offer each as its own option.")

        # SB023: mental computation
        wants_number = (q["type"] == "number" or kind == "numeric_range"
                        or (not q["options"] and re.search(NUMBER_STEM_PATTERN, low)))
        hits = [m.group(0) for m in re.finditer(COMPUTE_PATTERN, low)] if english and wants_number else []
        if hits:
            add(q, "SB023", "computation", "low", "; ".join(hits),
                "Asks for a figure the respondent must calculate. Ask for the parts over a short period, offer ranges, "
                "or let them check records.")

        # SB025: grid rows and an open question first
        if len(q["rows"]) > max_grid_rows:
            add(q, "SB025", "grid_rows", "low", "%d rows" % len(q["rows"]),
                "More than %d rows in one grid%s. Split it or cut items." % (max_grid_rows, " read aloud" if phone else ""))
        if index == 0 and q["type"] == "open" and any_options:
            add(q, "SB025", "open_first", "low", "open question first",
                "An open question first asks for the most effort before any commitment. Start with an easy closed question.")

        # SB027: even-point bipolar scale (information only)
        if (kind == "rating" and info["positives"] and info["negatives"] and not info["neutrals"]
                and len(plain) % 2 == 0):
            add(q, "SB027", "even_points", "info", "%d points, no midpoint" % len(plain),
                "No midpoint. Sources differ: Krosnick and Presser find a midpoint desirable; some practitioners "
                "leave it out to force a direction. Decide on purpose.")

    # SB016: demographic or sensitive questions that open the questionnaire
    demographic = [bool(re.search(DEMOGRAPHIC_PATTERN, q["text"].lower())) for q in questions]
    if not all(demographic):
        for q, is_demo in zip(questions, demographic):
            if not is_demo:
                break
            add(q, "SB016", "opening", "low", re.search(DEMOGRAPHIC_PATTERN, q["text"].lower()).group(0),
                "Demographic or sensitive question at the start. Move it to the end unless it screens or routes.")

    # SB012: scale direction across all rating questions, scale length within a family
    rated = [(q, i) for q, i in zip(questions, infos) if i["kind"] == "rating"]
    directed = [(q, i) for q, i in rated if i["direction"]]
    if directed:
        directions = [i["direction"] for _, i in directed]
        reference = _most_common(directions)
        tie = directions.count(reference) * 2 == len(directions)
        for q, i in directed:
            if i["direction"] != reference:
                side = "negative" if i["direction"] < 0 else "positive"
                add(q, "SB012", "direction", "medium", "%s ... %s" % (i["plain"][0], i["plain"][-1]),
                    ("This scale runs %s first; the questionnaire's scales are split evenly between the two directions, "
                     "starting the other way. Use one direction." % side) if tie else
                    ("This scale runs %s first; most scales in the questionnaire run the other way. Use one direction."
                     % side))
    families = {}
    for q, i in rated:
        families.setdefault(i["family"], []).append((q, i))
    for family, members in families.items():
        reference = _most_common([len(i["plain"]) for _, i in members])
        for q, i in members:
            if len(i["plain"]) != reference:
                add(q, "SB012", "length", "medium", "%d points, others have %d" % (len(i["plain"]), reference),
                    "The same %s scale has a different number of points elsewhere. Use one length." % family)

    # SB025: number of open questions
    open_count = sum(1 for q in questions if q["type"] == "open")
    if open_count > max_open and any_options:
        add(None, "SB025", "open_count", "low", "%d open questions" % open_count,
            "More than %d open questions. Keep the ones the decision needs; make the rest closed or optional." % max_open)

    # SB015: length estimate
    by_type = {}
    for q in questions:
        if q["id"] not in route_skip:
            by_type[q["type"]] = by_type.get(q["type"], 0) + question_points(q)
    if intro:
        by_type["intro"] = intro_points(intro["text"])
    points = sum(by_type.values())
    minutes = points / POINTS_PER_MINUTE * (PHONE_TIME_FACTOR if phone else 1)
    length = {"points": round(points, 2), "seconds": round(minutes * 60, 1), "minutes": round(minutes, 2),
              "minutes_rounded": math.ceil(minutes * 2 - 1e-9) / 2.0,
              "points_by_type": {k: round(v, 2) for k, v in sorted(by_type.items())},
              "route_skipped": sorted(route_skip, key=_id_key),
              "method": "Versta Research points; %d points per minute%s; each open question counted as one "
                        "expected sentence (3 points); introduction 1 point per three sentences; %s"
                        % (POINTS_PER_MINUTE, ", x %s for phone" % PHONE_TIME_FACTOR if phone else "",
                           "questions off the longest route left out" if route_skip else "every question counted")}
    if minutes > IDEAL_MINUTES:
        over_max = minutes > MAX_MINUTES
        add(None, "SB015", "over_maximum" if over_max else "over_ideal", "medium" if over_max else "low",
            "%.1f minutes" % minutes,
            "Estimated above the %d-minute median %s length that web-panel respondents report. Cut or split the "
            "questionnaire." % ((MAX_MINUTES, "maximum") if over_max else (IDEAL_MINUTES, "ideal")))

    findings = [f for f in findings if f["rule"] not in ignore]
    order, parent = {"intro": -1}, {}
    for n, q in enumerate(questions):
        order[q["id"]] = n
        for r in q["rows"]:
            order[r["id"]] = n + 0.5
            parent[r["id"]] = q["id"]
    for f in findings:
        kept = f["question"] in keep or parent.get(f["question"]) in keep
        f["status"] = "keep as is" if kept else "candidate"
    findings.sort(key=lambda f: (order.get(f["question"], len(order)), f["rule"], f["kind"]))
    return findings, length, unchecked


def _most_common(values):
    """Most frequent value; ties go to the one seen first."""
    best = None
    for value in values:
        if best is None or values.count(value) > values.count(best):
            best = value
    return best


# ---------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------
def build_report(path, questions, warnings, findings, length, unchecked, intro=None):
    active = [f for f in findings if f["status"] == "candidate"]
    counts = {s: sum(1 for f in active if f["severity"] == s) for s in ("high", "medium", "low", "info")}
    total = counts["high"] + counts["medium"] + counts["low"]
    return {"file": path, "questions": len(questions), "has_intro": bool(intro), "findings": findings,
            "summary": {"total": total, **counts, "kept": len(findings) - len(active)}, "length": length,
            "unchecked": unchecked, "warnings": warnings, "not_checked_by_rules": NOT_CHECKED,
            "pretest_note": PRETEST_NOTE}


def print_report(report):
    s = report["summary"]
    extra = "".join(", %d %s" % (s[k], label) for k, label in (("info", "note(s)"), ("kept", "kept as is")) if s[k])
    print("survey-bias-check: %s: %d questions, %d candidate findings (%d high, %d medium, %d low%s)"
          % (report["file"], report["questions"], s["total"], s["high"], s["medium"], s["low"], extra))
    for f in report["findings"]:
        where = {None: "survey", "intro": "intro"}.get(f["question"], "Q%s" % f["question"])
        if f["line"]:
            where += " (line %d)" % f["line"]
        keep = "  [keep as is]" if f["status"] != "candidate" else ""
        print("\n%s  %s  %s  %s%s" % (where, f["rule"], f["severity"], f["name"], keep))
        print("    match: %s" % f["match"])
        print("    why:   %s" % f["why"])
    for u in report["unchecked"]:
        print("\nQ%s  unchecked: %s" % (u["question"], u["reason"]))
    for w in report["warnings"]:
        print("\nwarning: %s" % w)
    if not report["has_intro"]:
        print("\nNo introduction text was given, so the introduction was not checked.")
    length = report["length"]
    print("\nEstimated length: %s points = %s min (%s s; report as about %s min). %s."
          % (length["points"], length["minutes"], length["seconds"], length["minutes_rounded"], length["method"]))
    print("These are candidates found by pattern rules; judge each one before reporting it.")
    print(report["not_checked_by_rules"])
    print(report["pretest_note"])


def resolve_ids(names, questions, flag):
    """Match each name to a question ID: the exact ID first, then the ID without a leading 'Q' (Q7 -> 7)."""
    ids = [q["id"] for q in questions]
    out, missing = set(), []
    for name in names:
        if name in ids:
            out.add(name)
            continue
        bare = re.sub(r"^[Qq]\s*", "", name)
        matches = [i for i in ids if i == bare or re.sub(r"^[Qq]\s*", "", i) == bare]
        if len(matches) == 1:
            out.add(matches[0])
        elif matches:
            raise InputError("%s %s matches more than one question (%s); use the exact ID" % (flag, name, ", ".join(matches)))
        else:
            missing.append(name)
    if missing:
        raise InputError("%s names a question that is not in the input: %s" % (flag, ", ".join(missing)))
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description="Rule-based linter for survey questionnaires (candidates, not verdicts).")
    parser.add_argument("input", nargs="?", help="questionnaire file (.md, .txt or .json); '-' reads stdin")
    parser.add_argument("--format", choices=["auto", "md", "json", "qsf-md"], default="auto",
                        help="input format; qsf-md is the Markdown the qsf-convert skill writes (default: auto)")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--strict", action="store_true", help="exit 1 when there is at least one high, medium or low finding")
    parser.add_argument("--mode", choices=["web", "phone"], default="web",
                        help="phone: option limit %d, grid limit %d, time x %s (default: web)"
                             % (PHONE_MAX_OPTIONS, PHONE_MAX_GRID_ROWS, PHONE_TIME_FACTOR))
    parser.add_argument("--audience", choices=["general", "expert"], default="general",
                        help="expert: skip the jargon and acronym rule SB007 (default: general)")
    parser.add_argument("--keep", default="", help="question numbers that must stay unchanged, e.g. Q7,Q9; "
                                                   "their findings are reported as 'keep as is' and not counted")
    parser.add_argument("--route-skip", default="", help="questions a respondent on the longest route never sees "
                                                         "(the shorter of two exclusive branches), e.g. Q5,Q6; "
                                                         "left out of the length estimate")
    parser.add_argument("--language", choices=["auto", "en", "other"], default="auto",
                        help="en: run the wording rules on every question; other: run none and list every question "
                             "as unchecked (default: auto-detect per question)")
    parser.add_argument("--max-words", type=int, default=MAX_WORDS, help="SB008 word limit (default %d)" % MAX_WORDS)
    parser.add_argument("--max-options", type=int, help="SB013 option limit (default %d; phone %d)" % (MAX_OPTIONS, PHONE_MAX_OPTIONS))
    parser.add_argument("--max-grid-rows", type=int, help="SB025 grid row limit (default %d; phone %d)" % (MAX_GRID_ROWS, PHONE_MAX_GRID_ROWS))
    parser.add_argument("--max-open", type=int, default=MAX_OPEN, help="SB025 open-question limit (default %d)" % MAX_OPEN)
    parser.add_argument("--ignore", default="", help="comma-separated rule IDs to skip, e.g. SB006,SB011")
    parser.add_argument("--list-rules", action="store_true", help="print the rule IDs and exit")
    args = parser.parse_args(argv)

    if args.list_rules:
        for rule, (name, why) in RULES.items():
            print("%s  %s: %s" % (rule, name, why))
        return 0
    if not args.input:
        parser.error("input file is required")
    phone = args.mode == "phone"
    max_options = args.max_options if args.max_options is not None else (PHONE_MAX_OPTIONS if phone else MAX_OPTIONS)
    max_grid_rows = args.max_grid_rows if args.max_grid_rows is not None else (PHONE_MAX_GRID_ROWS if phone else MAX_GRID_ROWS)
    ignore = {r.strip().upper() for r in args.ignore.split(",") if r.strip()}
    keep_raw = [k.strip() for k in args.keep.split(",") if k.strip()]
    skip_raw = [k.strip() for k in args.route_skip.split(",") if k.strip()]
    unknown = sorted(ignore - set(RULES))
    try:
        if unknown:
            raise InputError("unknown rule ID in --ignore: %s" % ", ".join(unknown))
        if min(args.max_words, max_options, max_grid_rows) < 1 or args.max_open < 0:
            raise InputError("--max-words, --max-options and --max-grid-rows must be positive; --max-open cannot be negative")
        questions, warnings, intro = load(args.input, args.format)
        keep = resolve_ids(keep_raw, questions, "--keep")
        route_skip = resolve_ids(skip_raw, questions, "--route-skip")
    except InputError as exc:
        print("survey-bias-check: error: %s" % exc, file=sys.stderr)
        return 2
    if args.audience == "expert":
        ignore.add("SB007")
    findings, length, unchecked = lint(questions, args.max_words, max_options, ignore, intro=intro,
                                       max_grid_rows=max_grid_rows, max_open=args.max_open, phone=phone, keep=keep,
                                       route_skip=route_skip, language=args.language)
    report = build_report(args.input, questions, warnings, findings, length, unchecked, intro)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)
    return 1 if args.strict and report["summary"]["total"] else 0


if __name__ == "__main__":
    sys.exit(main())
