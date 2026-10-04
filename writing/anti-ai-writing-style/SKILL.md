---
name: anti-ai-writing-style
description: Follow these guidelines when writing copy to avoid LLM frequently used styles and structures, and create more human sounding copy.
version: 2.0
---

{
  "title": "Guidelines to Avoid AI Writing Patterns",
  "description": "When writing content, avoid common AI writing patterns that make your output sound artificial. Follow these guidelines:",
  "how_to_use": "Rules are tagged with the source they came from and the year. AI tells rotate as models update, so treat the dated vocabulary lists as perishable and the structural rules as durable. Between the 2025 and 2026 research bases below, the overused-vocabulary list turned over almost completely and the em-dash finding reversed outright. Match the underlying habit, not just the words on the list.",
  "guidelines": [
    {
      "id": 1,
      "rule": "Break the rule of three",
      "source": "craft; confirmed Economist 2026",
      "description": "Don't consistently organize ideas in triplets or use three examples/points. Vary your structural patterns with different numbers of items or asymmetrical organization. This is one of the most heavily measured tells: every major model groups ideas in threes more often than human journalists or novelists do, and ChatGPT does it far more than any other model."
    },
    {
      "id": 2,
      "rule": "Avoid contrast framing",
      "source": "craft",
      "description": "Reduce usage of \"while X, Y\" or \"although X, Y\" constructions that artificially create tension between concepts."
    },
    {
      "id": 3,
      "rule": "Eliminate poetic shift phrases",
      "source": "craft",
      "description": "Don't rely on phrases like \"in a world where,\" \"in an era of,\" or \"in a landscape defined by\" to create dramatic transitions."
    },
    {
      "id": 4,
      "rule": "Use varied paragraph structures",
      "source": "craft",
      "description": "Don't consistently use odd-numbered structures (5, 7, or 9 paragraphs). Create natural flow with varied paragraph lengths based on content needs."
    },
    {
      "id": 5,
      "rule": "Limit hypophora",
      "source": "craft",
      "description": "Reduce the pattern of posing questions and immediately answering them. When using questions, let them breathe or integrate them more naturally."
    },
    {
      "id": 6,
      "rule": "Moderate adverb usage",
      "source": "craft; extended Economist 2026",
      "description": "Avoid overusing adverbs, particularly those ending in \"-ly\" (significantly, dramatically, effectively). Choose stronger verbs instead. \"Increasingly\" is now among the most overused words across all major models, so cut it on sight."
    },
    {
      "id": 7,
      "rule": "Avoid marketing cliché pairings",
      "source": "craft",
      "description": "Don't use predictable word combinations like \"seamless integration,\" \"robust solution,\" or \"game-changing innovation.\""
    },
    {
      "id": 8,
      "rule": "Use natural transitions",
      "source": "craft",
      "description": "Replace formulaic transitions (\"Let's explore,\" \"Let's dive into,\" \"Now, let's turn to\") with more varied and contextual connections between ideas."
    },
    {
      "id": 9,
      "rule": "End paragraphs naturally",
      "source": "craft",
      "description": "Don't conclude paragraphs with vague emotional insights or forced inspirational statements. End with substantive points that advance your argument."
    },
    {
      "id": 10,
      "rule": "Use em dashes rarely, and never trade them for less punctuation",
      "source": "craft; revised per Economist 2026",
      "description": "Allow at most one em dash in a long piece, and none in short copy. The reason has changed. As of 2026 the em dash is no longer a statistical marker of AI writing: ChatGPT uses markedly fewer em dashes than human writers, having reversed course sharply after earlier model versions overused them, and only Claude still uses more than humans. But readers have been trained to read the em dash as an AI signature, and reader perception is what matters in published work. Avoid it because your audience will flinch, not because a detector will flag it. Critical corollary: when you remove an em dash, replace it with a comma, semicolon, colon, or parentheses. Do not delete the punctuation and let the sentence run long. Sparse punctuation is now a stronger AI signal than the dash ever was. See rule 22."
    },
    {
      "id": 11,
      "rule": "Watch AI vocabulary, and know that the list expires",
      "source": "Russell 2025 and Economist 2026",
      "description": "Vocabulary was the single most common tell in the 2025 detection study, flagged in 53% of expert explanations. But the specific words rotate as models update, so this rule has two tiers. TIER ONE, the 2025 list, now largely retired by the models but still worth avoiding as plain cliché: tapestry, testament, landscape, realm, journey, quest, roadmap, toolkit, exploration, significance, nuance, delve, dive into, harness, underscores, fostering, navigate, elevate, empower, enhance, resonate, transcend, seamlessly, evoke, weave, crucial, pivotal, vibrant, robust, transformative, comprehensive, profound, groundbreaking, paramount, meaningful, curated, multifaceted, plus \"it's important to note,\" \"paving the way,\" \"when it comes to,\" and \"cautionary tale.\" TIER TWO, the current 2026 list, is what models actually overuse now: ordinary-looking polysyllables such as significant, increasingly, consequences, implications, framework, and considerations, alongside genuinely rare words such as interdependence and reindustrialisation. The 2026 tell is subtler than the 2025 one, because the words are unremarkable on their own. Judge by density, not by any single word. If a word from either list is genuinely the right word, use it, but never use two in the same paragraph."
    },
    {
      "id": 12,
      "rule": "Just say says",
      "source": "Russell 2025",
      "description": "When attributing quotes, humans repeat \"says\" over and over. AI rotates through descriptive synonyms (notes, explains, emphasizes, highlights, observes). Default to \"says\" or \"said\" for most attributions and let it repeat. An occasional alternative is fine, but constant variation is a tell."
    },
    {
      "id": 13,
      "rule": "Quote real people, and write messy quotes",
      "source": "Russell 2025 and Economist 2026",
      "description": "Start with presence. Models barely quote anyone at all, which is a measurable difference from human journalism and a major reason AI prose reads flat. If a piece would normally carry a source, get one in. Then handle quality. AI-generated quotes are overly formal, perfectly state a position, and match the surrounding article's style so every speaker sounds identical. Real quotes are short snippets with distinct voices, filler words, and rough edges that the writer had to work around. Make each speaker sound different from the article text and from each other, and don't let a quote tidily summarize the paragraph it sits in."
    },
    {
      "id": 14,
      "rule": "Allow imperfect grammar",
      "source": "Russell 2025",
      "description": "AI text is grammatically flawless, which itself reads as artificial (flagged in 25% of expert explanations). Permit sentence fragments. Start sentences with And, But, or So. Let an occasional long sentence run on a bit. Mix punctuation styles instead of uniform, textbook-correct sentences throughout."
    },
    {
      "id": 15,
      "rule": "Take risks and have opinions",
      "source": "Russell 2025",
      "description": "AI writing is safe, unsurprising, and humorless, leaving readers bored (originality was flagged in 24% of expert explanations). Include at least one unexpected analogy, specific opinion, or moment of humor per piece. Reference specific real things (brands, places, cultural moments) rather than generic examples. If every claim in the piece is one nobody could disagree with, it reads as AI."
    },
    {
      "id": 16,
      "rule": "Vary tone beyond neutral-positive",
      "source": "Russell 2025",
      "description": "AI defaults to a consistently neutral or uplifting tone and avoids darker or critical material. Don't sand off skepticism, frustration, or negative facts. A piece about a disease should sit with the hard parts, not rush to hopeful quotes and \"a new chapter.\" Subtle bias and a real point of view are human signals."
    },
    {
      "id": 17,
      "rule": "Skip generic and scenic intros",
      "source": "Russell 2025",
      "description": "AI introductions either summarize the entire article up front or open with a cinematic scene-setter (\"On a drab November morning...\"). Open instead with a specific, compelling detail or an angle that doesn't reveal the whole piece. The reader should need to keep reading to know where it's going."
    },
    {
      "id": 18,
      "rule": "Watch names, titles, and list formatting",
      "source": "Russell 2025",
      "description": "AI invents the same fictional experts repeatedly (Sarah Thompson, Emily Carter) and gives everyone the title Dr. regardless of field. Use real, verifiable, or context-specific names, and vary how people are titled and introduced. In formatting, avoid the AI-default list pattern of bolded header, colon, then description on every bullet, and avoid making all paragraphs the same length."
    },
    {
      "id": 19,
      "rule": "Prefer short Saxon words to long Latinate ones",
      "source": "Economist 2026; Orwell 1946",
      "description": "Word length is one of the cleanest separators between human and machine prose. Every major model writes with far more long words (eight letters or more) than journalists do, and journalists use more than novelists. Latinate suffixes such as -tion, -ity, -ance, and -ise cluster in AI text. Orwell named this habit \"pretentious diction\" in 1946: dressing up simple statements with complicated words to sound clever, on the assumption that Latin and Greek roots are grander than Saxon ones. Use the short word. Use rather than utilize, help rather than facilitate, start rather than commence, show rather than demonstrate, about rather than approximately."
    },
    {
      "id": 20,
      "rule": "Kill nominalizations",
      "source": "Economist 2026",
      "description": "Models are fond of turning verbs into nouns: expansion from expand, utilization from utilize, implementation from implement, optimization from optimize. The result is a sentence where the real action hides inside a noun and a weak verb carries the grammar. \"We conducted an evaluation of the process\" becomes \"we evaluated the process.\" Find the buried verb and let it do the work."
    },
    {
      "id": 21,
      "rule": "Cut scientific lingo from non-scientific copy",
      "source": "Economist 2026",
      "description": "Models reach for technical register regardless of subject, using words like parameter, methodology, mechanism, variable, and metric far more often than human writers do across every corpus tested. In copy that isn't actually technical, this reads as borrowed authority. Gemini and Claude lean hardest on it. If the piece isn't a paper, don't let it sound like one."
    },
    {
      "id": 22,
      "rule": "Punctuate more, not less",
      "source": "Economist 2026",
      "description": "This one runs against instinct. Models use fewer commas and semicolons than human writers and hardly any parentheses at all, which means the newer tell is a text with too little punctuation rather than too much. The absence has two causes worth fixing directly: models write longer sentences, and they don't quote people. So break the long sentences (rule 23), get real quotes in (rule 13), and let commas, semicolons, colons, parentheses, and the occasional ellipsis appear at human density. An unpunctuated stretch of clean prose now reads more like a machine than a page full of marks does."
    },
    {
      "id": 23,
      "rule": "Vary sentence length hard",
      "source": "Economist 2026",
      "description": "Models write sentences of stubbornly similar length, running at roughly half to three-quarters of the sentence-length variation found in human journalism. The rhythm gives it away even when every individual sentence is fine. Human writing bursts: a long, clause-heavy sentence that carries an argument through several turns, and then a short one. Like that. Follow a thirty-word sentence with a four-word sentence. Interrupt a paragraph with a fragment. If every sentence in a paragraph could be swapped for another without changing the rhythm, rewrite the paragraph."
    },
    {
      "id": 24,
      "rule": "Watch \"and\"",
      "source": "Economist 2026",
      "description": "\"And\" is the single most overused word in AI writing. It's the mechanism behind the long sentences: clauses get chained rather than cut. When you find a sentence with two or more \"and\"s, try replacing one with a period. Most of the time the sentence improves and the paragraph picks up rhythm."
    },
    {
      "id": 25,
      "rule": "Retire \"not X but Y\" and \"not only but also\"",
      "source": "Russell 2025; measured Economist 2026",
      "description": "These are the rhetorical devices models reach for when trying to sound lively, alongside the rule of three. Claude and ChatGPT deploy \"it's not X but Y\" far more often per thousand sentences than any human corpus, including bestselling fiction. The construction promises a reversal and usually delivers a restatement. State the thing you actually mean and drop the setup."
    }
  ],
  "conclusion": "Write with authentic voice, incorporating personal perspectives, specific examples, and occasional imperfections that reflect human writing patterns. Remember that the tells decay: models are trained on human writing and human feedback, so they pick up what people find impressive and drop what people flag. Two of these rules reversed between 2025 and 2026. Expect more to.",
  "sources": [
    {
      "id": "craft",
      "citation": "Original rules from hands-on content and pattern work, 2024-2025."
    },
    {
      "id": "Russell 2025",
      "citation": "Russell, J., Karpinska, M., & Iyyer, M. (2025). People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text. arXiv:2501.15654.",
      "url": "https://arxiv.org/abs/2501.15654"
    },
    {
      "id": "Economist 2026",
      "citation": "The Economist (July 30, 2026). How to spot AI writing. Study of 55,940 sentences and 1.2m words comparing ChatGPT, Claude, Gemini, and Grok against Economist journalism, CNN/NYT/Washington Post reporting, and bestselling fiction from 1950 to 2022.",
      "url": "https://www.economist.com/culture/2026/07/30/how-to-spot-ai-writing"
    },
    {
      "id": "Orwell 1946",
      "citation": "Orwell, G. (1946). Politics and the English Language."
    }
  ]
}
