---
name: rune-langium-visual-editor
description: "Langium port for Rune DSL tooling Use when working with rune, rosetta, dsl, langium, cdm, isda, drr, finos, language-server, lsp, visual-editor, reactflow."
license: SEE LICENSE IN LICENSE
---

# @rune-langium/visual-editor

Langium port for Rune DSL tooling

## When to Use

- Working with rune, rosetta, dsl, langium, cdm, isda, drr, finos, language-server, lsp, visual-editor, reactflow
- API surface: 49 functions, 68 types, 10 constants

## Quick Reference

**DetailPanel:** `DetailPanel`, `DetailPanelProps`
**TypeSelector:** `TypeSelector`, `getKindBadgeClasses`, `getKindLabel`, `TypeSelectorProps`, `TypeSelectorTriggerProps`, `TypeSelectorPopoverProps`, `TypeSelectorGroup`
**CardinalityPicker:** `CardinalityPicker`, `CardinalityPickerProps`
**MetadataSection:** `MetadataSection`, `MetadataSectionProps`
**AttributeRow:** `AttributeRow`, `AttributeRowProps`
**DataTypeForm:** `DataTypeForm`, `DataTypeFormProps`
**EnumValueRow:** `EnumValueRow`, `EnumValueRowProps`
**EnumForm:** `EnumForm`, `EnumFormProps`
**ChoiceOptionRow:** `ChoiceOptionRow`, `ChoiceOptionRowProps`
**ChoiceForm:** `ChoiceForm`, `ChoiceFormProps`
**FunctionForm:** `FunctionForm`, `FunctionFormProps`
**ast-to-model:** `astToModel`
**model-to-ast:** `modelsToAst`, `ModelOutput`, `SyntheticModel`, `SyntheticElement`
**model-helpers:** `formatCardinality`, `parseCardinality`, `getTypeRefText`, `getRefText`, `annotationsToDisplay`, `conditionsToDisplay`, `classExprSynonymsToStrings`, `enumSynonymsToStrings`, `AST_TYPE_TO_NODE_TYPE`, `NODE_TYPE_TO_AST_TYPE`
**dagre-layout:** `computeLayout`, `computeLayoutIncremental`, `clearLayoutCache`
**layout-worker:** `computeLayoutAsync`, `cancelAsyncLayout`
**grouped-layout:** `computeGroupedLayout`, `findInheritanceGroups`, `GroupInfo`
**namespace-tree:** `buildNamespaceTree`, `filterNamespaceTree`
**editor-store:** `createEditorStore`, `EditorStore`, `EditorState`, `EditorActions`, `useEditorStore`
**history:** `useTemporalStore`, `useCanUndo`, `useCanRedo`, `useUndo`, `useRedo`, `TrackedState`
**ExpressionBuilder:** `ExpressionBuilder`, `ExpressionBuilderProps`
**useAutoSave:** `useAutoSave`
**useExpressionAutocomplete:** `useExpressionAutocomplete`, `CompletionItem`, `UseExpressionAutocompleteResult`
**edit-validator:** `detectCircularInheritance`, `detectDuplicateName`, `validateCardinality`, `detectDuplicateEnumValue`, `validateNotEmpty`, `validateIdentifier`, `validateExpression`, `validateGraph`, `ExpressionValidationResult`
**EditorFormPanel:** `EditorFormPanelProps`, `EditorFormPanel`
**NamespaceExplorerPanel:** `NamespaceExplorerPanelProps`, `NamespaceExplorerPanel`
**TypeCreator:** `TypeCreatorProps`, `TypeCreator`
**AttributeEditor:** `AttributeEditorProps`, `AttributeEditor`
**CardinalityEditor:** `CardinalityEditorProps`, `CardinalityEditor`
**types:** `AstNodeModel`, `AstNodeShape`, `GraphNode`, `AnyGraphNode`, `GraphMetadata`, `RootAstElement`, `TypeKind`, `EdgeKind`, `EdgeData`, `ValidationError`, `ExpressionEditorSlotProps`, `TypeOption`, `CommonFormActions`, `DataFormActions`, `EnumFormActions`, `ChoiceFormActions`, `FuncFormActions`, `FormActionsKindMap`, `AllEditorFormActions`, `EditorFormActions`, `GraphFilters`, `LayoutDirection`, `LayoutOptions`, `NodeStyleConfig`, `EdgeStyleConfig`, `RuneTypeGraphConfig`, `RuneTypeGraphCallbacks`, `RuneTypeGraphProps`, `RuneTypeGraphRef`, `TypeGraphNode`, `TypeGraphEdge`, `NamespaceTreeNode`, `NamespaceTypeEntry`, `VisibilityState`, `NavigateToNodeCallback`, `BUILTIN_TYPES`
**expression-store:** `FunctionScope`, `FunctionScopeEntry`
**RuneTypeGraph:** `RuneTypeGraph`

## Links

- [Repository](https://github.com/pradeepmouli/rune-langium)
- Author: Pradeep Mouli <pmouli@mac.com>