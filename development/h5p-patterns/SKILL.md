---
name: h5p-patterns
description: Create interactive H5P content for Moodle and web platforms. Use when building interactive exercises, quizzes, or multimedia learning content.
allowed-tools: Read, Write, Grep, Glob
---

# H5P Integration Skill

Embed and style H5P interactive content in Cloodle.

## Trigger
- H5P content requests
- Interactive element creation
- H5P embedding in Kirby or Moodle

## H5P in Moodle
H5P activities are native in Moodle 4+. Key features:
- Interactive Video
- Course Presentation
- Question Sets
- Branching Scenarios

### Embedding in Moodle Page
```html
<div class="cloodle-h5p-wrapper">
    <iframe src="/mod/h5pactivity/embed.php?id=123"
            class="h5p-iframe"
            allowfullscreen>
    </iframe>
</div>
```

## H5P in Kirby
Use iframe embedding with public H5P URLs:

```php
<?php snippet('h5p-embed', ['id' => $block->h5pId()]) ?>
```

### Snippet Template
```php
<div class="uk-card uk-card-default uk-card-body cloodle-h5p">
    <iframe
        src="<?= $moodleUrl ?>/mod/h5pactivity/embed.php?id=<?= $id ?>"
        class="uk-width-1-1"
        style="border: none; min-height: 400px;">
    </iframe>
</div>
```

## Styling H5P
```scss
.cloodle-h5p-wrapper {
    border-radius: $cloodle-border-radius;
    overflow: hidden;
    box-shadow: $card-box-shadow;

    iframe {
        width: 100%;
        min-height: 500px;
        border: none;
    }
}
```

## Content Types for Education
| Type | Use Case |
|------|----------|
| Interactive Video | Lecture with quizzes |
| Course Presentation | Slide-based learning |
| Question Set | Assessment |
| Dialog Cards | Vocabulary/flashcards |
| Timeline | Historical content |
