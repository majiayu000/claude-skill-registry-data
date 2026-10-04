---
name: "DevExpress/DEXT Components"
description: "Standards for using DevExpress (DEXT) components in Delphi VCL applications"
---

# DevExpress (DEXT) Components — Skill

Use this skill when developing rich interfaces with **DevExpress** (DEXT) components for Delphi VCL.

## When to Use

- When creating advanced grids with `TcxGrid`
- When using `TcxDBTreeList` for hierarchical structures
- When implementing layout managers (`TdxLayoutControl`)
- When customizing skins and themes

## Main Components

| Component | Usage | Prefix |
|-----------|-----|---------|
| `TcxGrid` | Advanced grid with grouping, filters, summaries | `grd` |
| `TcxGridDBTableView` | Data-aware tabular view | `tvw` |
| `TcxGridDBBandedTableView` | View with grouped bands/columns | `btvw` |
| `TcxGridDBCardView` | Card view | `cvw` |
| `TcxDBTreeList` | TreeList data-aware | `trl` |
| `TdxLayoutControl` | Responsive layout manager | `lyt` |
| `TdxLayoutGroup` | Grupo dentro de layout | `lgrp` |
| `TdxLayoutItem` | Item within layout | `litm` |
| `TcxDBTextEdit` | Edit text data-aware | `edt` |
| `TcxDBComboBox` | ComboBox data-aware | `cmb` |
| `TcxDBDateEdit` | Date picker data-aware | `dte` |
| `TcxDBCurrencyEdit` | Data-aware currency editor | `cur` |
| `TcxDBCheckBox` | Checkbox data-aware | `chk` |
| `TcxDBLookupComboBox` | Lookup combo data-aware | `lcb` |
| `TcxDBMemo` | Memo data-aware | `mmo` |
| `TdxBarManager` | Toolbar/ribbon | `bar` |
| `TdxRibbon` | Ribbon UI | `rbn` |
| `TdxNavBar` | Navigation Bar | `nav` |
| `TdxSkinController` | Skin controller | `skn` |
| `TcxPageControl` | Advanced PageControl | `pgc` |
| `TcxGroupBox` | Styled GroupBox | `grp` |

## TcxGrid Configuration

```pascal
// Criaction programática de colunas
procedure TfrmCustomerList.ConfigureGrid;
var
  LView: TcxGridDBTableView;
begin
  LView := grdCustomers.Views[0] as TcxGridDBTableView;
  LView.DataController.DataSource := dsCustomers;

  // Configurar comportamento
  LView.OptionsData.Editing := False;        // Somente leitura
  LView.OptionsData.Deleting := False;
  LView.OptionsData.Inserting := False;
  LView.OptionsView.GroupByBox := True;       // Agrupamento visual
  LView.OptionsView.Footer := True;          // Rodapé com sumários
  LView.OptionsView.Indicator := True;       // Indicador de linha
  LView.OptionsCustomize.ColumnFiltering := True;
  LView.OptionsCustomize.ColumnSorting := True;
  LView.OptionsSelection.MultiSelect := True;

  // Configurar colunas individualmente
  ConfigureColumn(LView.GetColumnByFieldName('name'), 'Nome', 200);
  ConfigureColumn(LView.GetColumnByFieldName('cpf'), 'CPF', 120);
  ConfigureColumn(LView.GetColumnByFieldName('email'), 'E-mail', 250);
end;

procedure TfrmCustomerList.ConfigureColumn(
  AColumn: TcxGridDBColumn; const ACaption: string; AWidth: Integer);
begin
  if not Assigned(AColumn) then Exit;
  AColumn.Caption := ACaption;
  AColumn.Width := AWidth;
  AColumn.HeaderAlignmentHorz := taCenter;
end;
```

## Summaries in the Grid

```pascal
// Sumário no Footer
procedure ConfigureFooterSummary(AView: TcxGridDBTableView);
var
  LSummary: TcxGridDBTableSummaryItem;
begin
  AView.DataController.Summary.FooterSummaryItems.Clear;

  LSummary := AView.DataController.Summary.FooterSummaryItems.Add
    as TcxGridDBTableSummaryItem;
  LSummary.FieldName := 'value';
  LSummary.Kind := skSum;
  LSummary.Format := 'Total: R$ #,##0.00';
  LSummary.Column := AView.GetColumnByFieldName('value');

  LSummary := AView.DataController.Summary.FooterSummaryItems.Add
    as TcxGridDBTableSummaryItem;
  LSummary.FieldName := 'id';
  LSummary.Kind := skCount;
  LSummary.Format := 'Registros: %d';
  LSummary.Column := AView.GetColumnByFieldName('name');
end;
```

## TdxLayoutControl (Responsive Layout)

```pascal
// Organizaction de formulário com LayoutControl
// Vantagens: responsivo, reposiciona automaticamente, visual consistente

procedure TfrmCustomerEdit.ConfigureLayout;
begin
  lytMain.BeginUpdate;
  try
    // Grupo de data pessoais
    lgrpPersonal.Caption := 'Dados Pessoais';
    lgrpPersonal.LayoutDirection := ldHorizontal;

    // Grupo de address
    lgrpAddress.Caption := 'Endereço';
    lgrpAddress.LayoutDirection := ldHorizontal;

    // Configurar itens
    litmName.Control := edtName;
    litmName.CaptionOptions.Text := 'Nome:';
    litmName.CaptionOptions.Width := 80;
  finally
    lytMain.EndUpdate;
  end;
end;
```

## Skinning / Themes

```pascal
// Aplicar skin globalmente
uses
  dxSkinsCore,
  dxSkinOffice2019Colorful;  // Skin específico

procedure TfrmMain.ApplySkin;
begin
  // Via SkinController (recomendado)
  sknController.NativeStyle := False;
  sknController.SkinName := 'Office2019Colorful';

  // OU programaticamente
  cxLookAndFeelController.NativeStyle := False;
  cxLookAndFeelController.SkinName := 'Office2019Colorful';
end;

// Skins populares: 'Office2019Colorful', 'WXI', 'Metropolis',
// 'MetropolisDark', 'TheBezier', 'Fluent', 'Office2019DarkGray'
```

## Filters in the Grid

```pascal
// Filtro programático
procedure TfrmCustomerList.ApplyFilter(const AField, AValue: string);
var
  LView: TcxGridDBTableView;
begin
  LView := grdCustomers.Views[0] as TcxGridDBTableView;
  LView.DataController.Filter.Root.Clear;
  LView.DataController.Filter.Root.AddItem(
    LView.GetColumnByFieldName(AField),
    foLike,
    '%' + AValue + '%',
    AValue
  );
  LView.DataController.Filter.Active := True;
end;

// Limpar filtro
procedure TfrmCustomerList.ClearFilter;
begin
  (grdCustomers.Views[0] as TcxGridDBTableView)
    .DataController.Filter.Root.Clear;
end;
```

## Grid Export

```pascal
uses
  cxGridExportLink;

// Exportar para Excel
procedure TfrmCustomerList.ExportToExcel;
begin
  cxGridExportLink.ExportGridToXLSX(
    'customers.xlsx',
    grdCustomers,
    False,   // AExpand
    True,    // AUseNativeFormat
    True     // AShowProgress
  );
end;

// Exportar para PDF
procedure TfrmCustomerList.ExportToPDF;
begin
  cxGridExportLink.ExportGridToPDF(
    'customers.pdf',
    grdCustomers
  );
end;
```

## DEXT Conventions

| Appearance | Convention |
|---------|-----------|
| **Prefixes** | Follow the table above (`grd`, `tvw`, `lyt`, etc.) |
| **Skins** | Use `TdxSkinController` in the main form |
| **Layout** | Prefer `TdxLayoutControl` to manual positioning |
| **Grid** | Configure at `FormCreate`, never at design-time for dynamic columns |
| **Filters** | Use `DataController.Filter` — do not filter via SQL when possible |
| **Summaries** | Configure `FooterSummaryItems` instead of calculating manually |
| **Exports** | Use `cxGridExportLink` — do not redeploy export |

## Checklist for DEXT Projects

- [ ] `TdxSkinController` configured in the main form?
- [ ] Grids configured with `OptionsData` (read-only when appropriate)?
- [ ] Footer summaries configured with BR formats (`R$ #,##0.00`)?
- [ ] `TdxLayoutControl` used for editing forms?
- [ ] Grid columns with `Caption`, `Width` and `Alignment`?
- [ ] Filters using `DataController.Filter` (not SQL)?
- [ ] Export via `cxGridExportLink`?
- [ ] Component prefixes following the standard table?
