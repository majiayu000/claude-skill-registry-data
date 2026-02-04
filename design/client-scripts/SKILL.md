---
name: client-scripts
description: Frappe client-side JavaScript patterns for form events, field manipulation, dialogs, and UI customization. Use when writing form scripts, handling field changes, creating dialogs, or customizing the Frappe desk interface.
---

# Frappe Client Scripts Reference

Complete reference for client-side JavaScript development in Frappe Framework.

## When to Use This Skill

- Writing form scripts (refresh, validate, field events)
- Manipulating form fields (show/hide, require, read-only)
- Creating dialogs and prompts
- Making API calls from client
- Customizing list views
- Adding custom buttons
- Handling child table events

## Form Script Location

```
my_app/
└── my_module/
    └── doctype/
        └── my_doctype/
            └── my_doctype.js    # Client script
```

## Form Events

### Complete Event Reference

```javascript
frappe.ui.form.on('My DocType', {
    // === LOAD EVENTS ===

    setup: function(frm) {
        // Called once when form is created (before data loads)
        // Use for: setting queries, initializing variables
        frm.set_query('customer', () => ({ filters: { status: 'Active' } }));
    },

    onload: function(frm) {
        // Called when form data is loaded (before refresh)
        // Use for: setting defaults for new docs
        if (frm.is_new()) {
            frm.set_value('posting_date', frappe.datetime.nowdate());
        }
    },

    onload_post_render: function(frm) {
        // Called after form is rendered
        // Use for: DOM manipulation, focus setting
        frm.get_field('customer').focus();
    },

    refresh: function(frm) {
        // Called every time form refreshes
        // Use for: custom buttons, field toggles, indicators
        if (!frm.is_new()) {
            frm.add_custom_button(__('Action'), () => do_action(frm));
        }
        frm.toggle_display('section_name', frm.doc.show_section);
    },

    // === SAVE EVENTS ===

    validate: function(frm) {
        // Called before save - return false to prevent
        if (frm.doc.end_date < frm.doc.start_date) {
            frappe.msgprint(__('End Date cannot be before Start Date'));
            return false;
        }
    },

    before_save: function(frm) {
        // Called after validate, before server request
        frm.doc.last_updated_by = frappe.session.user;
    },

    after_save: function(frm) {
        // Called after successful save
        frappe.show_alert({
            message: __('Saved successfully'),
            indicator: 'green'
        });
    },

    // === WORKFLOW EVENTS ===

    before_submit: function(frm) {
        // Called before document submission
    },

    on_submit: function(frm) {
        // Called after successful submission
    },

    before_cancel: function(frm) {
        // Called before cancellation
    },

    after_cancel: function(frm) {
        // Called after cancellation
    },

    // === FIELD EVENTS ===

    customer: function(frm) {
        // Called when 'customer' field changes
        if (frm.doc.customer) {
            fetch_customer_details(frm);
        }
    },

    posting_date: function(frm) {
        // Called when 'posting_date' field changes
        calculate_due_date(frm);
    }
});
```

## Field Manipulation

### Display Properties

```javascript
// Show/hide field
frm.toggle_display('fieldname', true);  // Show
frm.toggle_display('fieldname', false); // Hide
frm.toggle_display(['field1', 'field2'], condition);

// Set read-only
frm.set_df_property('fieldname', 'read_only', 1);
frm.toggle_enable('fieldname', false);  // Disable

// Set required
frm.set_df_property('fieldname', 'reqd', 1);
frm.toggle_reqd('fieldname', true);
frm.toggle_reqd(['field1', 'field2'], condition);

// Set hidden
frm.set_df_property('fieldname', 'hidden', 1);

// Change label
frm.set_df_property('fieldname', 'label', 'New Label');

// Change description
frm.set_df_property('fieldname', 'description', 'Help text');

// Change options (for Select)
frm.set_df_property('fieldname', 'options', 'Option1\nOption2\nOption3');

// Refresh after changes
frm.refresh_field('fieldname');
frm.refresh_fields();
```

### Set Values

```javascript
// Set single value
frm.set_value('fieldname', value);

// Set multiple values
frm.set_value({
    'field1': 'value1',
    'field2': 'value2',
    'field3': 'value3'
});

// Set with callback
frm.set_value('fieldname', value).then(() => {
    // After value is set
});

// Clear field
frm.set_value('fieldname', null);
frm.set_value('fieldname', '');

// Set default value
frm.set_df_property('fieldname', 'default', 'default_value');
```

### Link Field Queries

```javascript
// Basic filter
frm.set_query('customer', function() {
    return {
        filters: {
            status: 'Active',
            customer_type: 'Company'
        }
    };
});

// Dynamic filter based on form values
frm.set_query('item_code', function() {
    return {
        filters: {
            item_group: frm.doc.item_group,
            is_stock_item: 1
        }
    };
});

// Filter in child table
frm.set_query('item_code', 'items', function(doc, cdt, cdn) {
    let row = locals[cdt][cdn];
    return {
        filters: {
            warehouse: row.warehouse || doc.default_warehouse
        }
    };
});

// Custom query (server method)
frm.set_query('supplier', function() {
    return {
        query: 'my_app.api.get_suppliers',
        filters: {
            region: frm.doc.region
        }
    };
});

// Clear query
frm.set_query('fieldname', null);
```

## Custom Buttons

```javascript
refresh: function(frm) {
    // Simple button
    frm.add_custom_button(__('Do Something'), function() {
        do_something(frm);
    });

    // Button in group/dropdown
    frm.add_custom_button(__('Action 1'), function() {
        action_1(frm);
    }, __('Actions'));

    frm.add_custom_button(__('Action 2'), function() {
        action_2(frm);
    }, __('Actions'));

    // Primary button (highlighted)
    frm.add_custom_button(__('Submit'), function() {
        submit_doc(frm);
    }).addClass('btn-primary');

    // Button with icon
    let btn = frm.add_custom_button(__('Print'), function() {
        print_doc(frm);
    });
    btn.prepend('<i class="fa fa-print"></i> ');

    // Conditional buttons
    if (frm.doc.status === 'Draft') {
        frm.add_custom_button(__('Submit for Review'), function() {
            submit_for_review(frm);
        });
    }

    // Remove button
    frm.remove_custom_button(__('Do Something'));
    frm.remove_custom_button(__('Action 1'), __('Actions'));

    // Clear all buttons
    frm.clear_custom_buttons();

    // Page actions
    frm.page.set_primary_action(__('Save'), function() {
        frm.save();
    });

    frm.page.set_secondary_action(__('Cancel'), function() {
        frappe.set_route('List', 'My DocType');
    });
}
```

## Child Table Operations

### Events

```javascript
frappe.ui.form.on('My DocType Item', {
    // Row added
    items_add: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.warehouse = frm.doc.default_warehouse;
        frm.refresh_field('items');
    },

    // Before row removed (can prevent)
    before_items_remove: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.is_mandatory) {
            frappe.throw(__('Cannot remove mandatory item'));
        }
    },

    // Row removed
    items_remove: function(frm, cdt, cdn) {
        calculate_total(frm);
    },

    // Field in row changes
    qty: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.amount = flt(row.qty) * flt(row.rate);
        frm.refresh_field('items');
        calculate_total(frm);
    },

    rate: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.amount = flt(row.qty) * flt(row.rate);
        frm.refresh_field('items');
        calculate_total(frm);
    },

    item_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code) {
            frappe.call({
                method: 'my_app.api.get_item_details',
                args: { item_code: row.item_code },
                callback: function(r) {
                    if (r.message) {
                        frappe.model.set_value(cdt, cdn, {
                            'rate': r.message.rate,
                            'uom': r.message.uom,
                            'description': r.message.description
                        });
                    }
                }
            });
        }
    }
});

function calculate_total(frm) {
    let total = 0;
    frm.doc.items.forEach(item => {
        total += flt(item.amount);
    });
    frm.set_value('total', total);
}
```

### Manipulating Rows

```javascript
// Add row
let row = frm.add_child('items', {
    item_code: 'ITEM-001',
    qty: 10,
    rate: 100
});
frm.refresh_field('items');

// Get row by index
let first_row = frm.doc.items[0];

// Get row by name
let row = locals['My DocType Item'][cdn];

// Update row
frappe.model.set_value(cdt, cdn, 'fieldname', value);
frappe.model.set_value(cdt, cdn, {
    'field1': 'value1',
    'field2': 'value2'
});

// Remove row
frm.get_field('items').grid.grid_rows[0].remove();
frm.refresh_field('items');

// Remove all rows
frm.clear_table('items');
frm.refresh_field('items');

// Iterate rows
frm.doc.items.forEach((item, idx) => {
    console.log(idx, item.item_code);
});
```

## Dialogs

### Simple Prompt

```javascript
// Single field
frappe.prompt(
    {
        fieldname: 'reason',
        fieldtype: 'Small Text',
        label: 'Reason',
        reqd: 1
    },
    function(values) {
        console.log(values.reason);
    },
    __('Enter Reason'),
    __('Submit')
);
```

### Multi-field Prompt

```javascript
frappe.prompt([
    {
        fieldname: 'customer',
        fieldtype: 'Link',
        options: 'Customer',
        label: 'Customer',
        reqd: 1
    },
    {
        fieldname: 'date',
        fieldtype: 'Date',
        label: 'Date',
        default: frappe.datetime.nowdate()
    },
    {
        fieldname: 'priority',
        fieldtype: 'Select',
        label: 'Priority',
        options: 'Low\nMedium\nHigh',
        default: 'Medium'
    }
], function(values) {
    process_data(values);
}, __('Enter Details'), __('Process'));
```

### Custom Dialog

```javascript
let dialog = new frappe.ui.Dialog({
    title: __('Custom Dialog'),
    fields: [
        {
            fieldname: 'customer',
            fieldtype: 'Link',
            options: 'Customer',
            label: __('Customer'),
            reqd: 1,
            get_query: function() {
                return { filters: { status: 'Active' } };
            },
            change: function() {
                // Field change handler
                let value = dialog.get_value('customer');
                if (value) {
                    dialog.set_value('customer_name', 'Loading...');
                }
            }
        },
        { fieldtype: 'Column Break' },
        {
            fieldname: 'customer_name',
            fieldtype: 'Data',
            label: __('Customer Name'),
            read_only: 1
        },
        { fieldtype: 'Section Break', label: 'Items' },
        {
            fieldname: 'items',
            fieldtype: 'Table',
            label: __('Items'),
            cannot_add_rows: false,
            in_place_edit: true,
            fields: [
                {
                    fieldname: 'item',
                    fieldtype: 'Link',
                    options: 'Item',
                    in_list_view: 1,
                    label: __('Item')
                },
                {
                    fieldname: 'qty',
                    fieldtype: 'Float',
                    in_list_view: 1,
                    label: __('Qty')
                }
            ]
        }
    ],
    size: 'large', // small, large, extra-large
    primary_action_label: __('Submit'),
    primary_action: function(values) {
        console.log(values);
        dialog.hide();
        process_dialog(values);
    },
    secondary_action_label: __('Cancel')
});

dialog.show();

// Set values
dialog.set_value('customer', 'CUST-001');
dialog.set_values({
    'customer': 'CUST-001',
    'date': frappe.datetime.nowdate()
});

// Get values
let values = dialog.get_values();
let customer = dialog.get_value('customer');

// Access fields
let field = dialog.get_field('customer');
field.set_description('Select active customer');
```

### Confirmation Dialog

```javascript
frappe.confirm(
    __('Are you sure you want to delete this?'),
    function() {
        // On Yes
        delete_record();
    },
    function() {
        // On No (optional)
    }
);
```

## API Calls

### frappe.call

```javascript
// Basic call
frappe.call({
    method: 'my_app.api.get_data',
    args: {
        customer: frm.doc.customer
    },
    callback: function(r) {
        if (r.message) {
            frm.set_value('data', r.message);
        }
    }
});

// With loading indicator
frappe.call({
    method: 'my_app.api.process',
    args: { data: frm.doc },
    freeze: true,
    freeze_message: __('Processing...'),
    callback: function(r) {
        frappe.msgprint(__('Done!'));
    },
    error: function(r) {
        frappe.msgprint(__('Error occurred'));
    }
});

// Async/await
async function getData() {
    const r = await frappe.call({
        method: 'my_app.api.get_data',
        args: { id: 123 }
    });
    return r.message;
}

// Promise chain
frappe.call({
    method: 'my_app.api.get_data'
}).then(r => {
    return frappe.call({
        method: 'my_app.api.process',
        args: { data: r.message }
    });
}).then(r => {
    console.log('Done', r.message);
});
```

## Messages & Alerts

```javascript
// Toast alert
frappe.show_alert({
    message: __('Success!'),
    indicator: 'green'  // green, blue, orange, red
}, 5);  // seconds

// Message dialog
frappe.msgprint({
    title: __('Information'),
    message: __('This is important'),
    indicator: 'blue'
});

// Error (stops execution)
frappe.throw(__('Cannot proceed'));

// Confirmation required
frappe.validated = false;  // In validate event
```

## Utilities

```javascript
// Date/Time
frappe.datetime.nowdate();           // "2024-01-15"
frappe.datetime.now_datetime();      // "2024-01-15 10:30:00"
frappe.datetime.add_days("2024-01-15", 7);
frappe.datetime.add_months("2024-01-15", 1);

// Formatting
frappe.format(1234.56, {fieldtype: 'Currency'});
format_currency(1234.56, 'USD');
flt(value);  // Float
cint(value); // Integer

// Navigation
frappe.set_route('Form', 'Customer', 'CUST-001');
frappe.set_route('List', 'Customer');
frappe.new_doc('Customer');

// Translation
__('Translate this');
__('Hello {0}', [name]);
```
