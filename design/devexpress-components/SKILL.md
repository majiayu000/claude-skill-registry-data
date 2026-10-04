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
//Programmatic column creation
procedure TfrmCustomerList.ConfigureGrid;
var
  LView: TcxGridDBTableView;
begin
  LView := grdCustomers.Views[0] as TcxGridDBTableView;
  LView.DataController.DataSource := dsCustomers;

  //Configure behavior
  LView.OptionsData.Editing := False;        //Read only
  LView.OptionsData.Deleting := False;
  LView.OptionsData.Inserting := False;
  LView.OptionsView.GroupByBox := True;       //Visual grouping
  LView.OptionsView.Footer := True;          //Footer with summaries
  LView.OptionsView.Indicator := True;       //Line indicator
  LView.OptionsCustomize.ColumnFiltering := True;
  LView.OptionsCustomize.ColumnSorting := True;
  LView.OptionsSelection.MultiSelect := True;

  //Configure columns individually
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
//Footer Summary
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
//Form organization with LayoutControl
//Advantages: responsive, automatically repositions, consistent look

procedure TfrmCustomerEdit.ConfigureLayout;
begin
  lytMain.BeginUpdate;
  try
    //Personal data group
    lgrpPersonal.Caption := 'Dados Pessoais';
    lgrpPersonal.LayoutDirection := ldHorizontal;

    //Address group
    lgrpAddress.Caption := 'Endereço';
    lgrpAddress.LayoutDirection := ldHorizontal;

    //Configure items
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
//Apply skin globally
uses
  dxSkinsCore,
  dxSkinOffice2019Colorful;  //Specific skin

procedure TfrmMain.ApplySkin;
begin
  //Via SkinController (recommended)
  sknController.NativeStyle := False;
  sknController.SkinName := 'Office2019Colorful';

  //OR programmatically
  cxLookAndFeelController.NativeStyle := False;
  cxLookAndFeelController.SkinName := 'Office2019Colorful';
end;

//Skins populares: 'Office2019Colorful', 'WXI', 'Metropolis',
//'MetropolisDark', 'TheBezier', 'Fluent', 'Office2019DarkGray'
```

## Filters in the Grid

```pascal
//Programmatic filter
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

//Clean filter
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

//Export to Excel
procedure TfrmCustomerList.ExportToExcel;
begin
  cxGridExportLink.ExportGridToXLSX(
    'customers.xlsx',
    grdCustomers,
    False,   // AExpand
    True,    //AUseNativeFormat
    True     //AShowProgress
  );
end;

//Export to PDF
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
