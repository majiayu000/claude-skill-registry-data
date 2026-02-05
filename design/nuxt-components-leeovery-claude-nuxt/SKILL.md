---
name: nuxt-components
description: Vue component patterns with Composition API and script setup. Use when creating components, understanding script setup order convention, organizing component directories, or implementing component patterns like slideovers, modals, and tables.
---

# Nuxt Components

Vue 3 Composition API components with standardized organization and patterns.

## Core Concepts

**[components.md](references/components.md)** - Script setup order, patterns, organization

## Directory Structure

```
components/
├── Common/       # Shared utilities (Copyable, LoadingLine)
├── Detail/       # Entity detail views (PostDetail)
├── Form/         # Reusable form inputs (AuthorSelect)
├── Modals/       # Confirmation/action modals
├── Nav/          # Navigation elements
├── Slideovers/   # Slideout panels (CreatePostSlideover)
├── TabSections/  # Tab content sections
└── Tables/       # Data tables (PostsTable)
```

## Script Setup Order

```vue
<script lang="ts" setup>
// 1. Imports
import createPostActionFactory from '~/features/posts/actions/create-post-action'

// 2. Props & Emits
const props = defineProps<{ author?: Author }>()
const emits = defineEmits<{ close: [success: boolean] }>()

// 3. Composables
const flash = useFlash()

// 4. Injections
const slideover = inject(SlideoverKey)

// 5. Refs
const formRef = useTemplateRef('formRef')

// 6. Toggles
const isOpen = ref(false)

// 7. Reactive props
const formData = ref<CreatePostData>({ title: '', content: '' })

// 8. Computed
const canSubmit = computed(() => formData.value.title && formData.value.content)

// 9. Fetch + queries
const { data: posts, refresh } = getPostsQuery(filters)

// 10. Builders (action/mutation factories)
const createPostAction = createPostActionFactory()

// 11. Watchers
watch(selectedAuthor, (a) => { formData.value.authorId = a?.ulid || '' })

// 12. Methods
const onSubmit = async (data) => { await createPostAction(data) }

// 13. Real-time listeners
privateChannel(Posts).on(PostCreated, refresh)

// 14. Provides
provide(SlideoverKey, { isOpen })

// 15. Lifecycles
onMounted(() => { /* ... */ })
</script>
```
