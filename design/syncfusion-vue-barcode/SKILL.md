---
name: syncfusion-vue-barcode
description: Create and customize barcode, QR code, and Data Matrix components using Syncfusion Vue Barcode Generator. Use this skill when implementing barcode generation, QR code creation, Data Matrix codes, export functionality, and barcode styling. Covers Syncfusion's BarcodeGenerator, QRCodeGenerator, and DataMatrixGenerator components for Vue applications (Composition API and Options API).
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing Syncfusion Vue Barcode Generator

Generate professional barcodes, QR codes, and Data Matrix codes in Vue applications using Syncfusion's barcode components. Supports multiple barcode types, export formats, and comprehensive customization options.

## When to Use This Skill

- **Implement barcode generation:** Create Code39, Code128, Code93, and other barcode types
- **Generate QR codes:** Create scannable 2D QR codes for URLs, contact info, or data sharing
- **Create Data Matrix codes:** Generate industrial 2D barcodes for product tracking and labels
- **Export barcodes:** Download barcodes as images (PNG, JPG, SVG) or Base64 strings
- **Customize appearance:** Style barcode dimensions, colors, rendering modes (SVG vs Canvas)
- **Add barcodes to Vue apps:** Integrate components using Composition API or Options API
- **Real-world implementations:** Product barcodes, inventory tracking, shipping labels, QR code menus

## Documentation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and npm dependencies
- Vue 2 and Vue 3 setup
- Composition API vs Options API registration
- Basic component configuration

### Barcode Generator Component
📄 **Read:** [references/barcode-generator.md](references/barcode-generator.md)
- BarcodeGenerator component overview
- Barcode types (Code39, Code128, Code93, Code32, Code11)
- Implementation and configuration
- Type-specific examples
- Props reference

### QR Code Generator Component
📄 **Read:** [references/qrcode-generator.md](references/qrcode-generator.md)
- QRCodeGenerator component
- QR code versions and data capacity
- 2D QR code generation
- Configuration options
- Real-world use cases

### Data Matrix Generator Component
📄 **Read:** [references/datamatrix-generator.md](references/datamatrix-generator.md)
- DataMatrixGenerator component
- Data Matrix 2D encoding
- Industrial applications
- Configuration and sizing
- Performance considerations

### Export Functionality
📄 **Read:** [references/export-functionality.md](references/export-functionality.md)
- Export as image (PNG, JPG, SVG formats)
- Export as Base64 string
- Browser downloads
- File naming conventions
- Composition API and Options API export patterns

### Styling and Rendering Modes
📄 **Read:** [references/styling-and-modes.md](references/styling-and-modes.md)
- SVG vs Canvas rendering modes
- Width and height configuration
- CSS styling and responsive design
- Color customization
- Theme integration

### Common Use Cases and Patterns
📄 **Read:** [references/common-use-cases.md](references/common-use-cases.md)
- Product barcode generation workflows
- QR code for URL sharing
- Shipping label barcodes
- Real-world implementation patterns
- Performance and optimization tips

## Quick Start Example

### Generate a Simple QR Code

```vue
<template>
  <div class="barcode-container">
    <ejs-qrcodegenerator
      id="qrcode"
      ref="qrcodeControl"
      :width="width"
      :height="height"
      :value="value"
      :mode="mode"
    ></ejs-qrcodegenerator>
  </div>
</template>

<style>
  .barcode-container {
    height: 200px;
    width: 200px;
    padding: 20px;
  }
</style>

<script setup>
import { QRCodeGeneratorComponent as EjsQrcodegenerator } from '@syncfusion/ej2-vue-barcode-generator';

const width = "200px";
const height = "200px";
const mode = "SVG";
const value = "https://www.syncfusion.com";
</script>
```

## Common Patterns

### Pattern 1: Dynamic Barcode Generation with User Input

```vue
<template>
  <div>
    <input v-model="barcodeValue" placeholder="Enter barcode data" />
    <button @click="generateBarcode">Generate Barcode</button>
    <ejs-barcodegenerator
      id="barcode"
      ref="barcodeControl"
      :value="barcodeValue"
      :type="barcodeType"
      width="200px"
      height="150px"
    ></ejs-barcodegenerator>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { BarcodeGeneratorComponent as EjsBarcodegenerator } from '@syncfusion/ej2-vue-barcode-generator';

const barcodeValue = ref("PRODUCT123");
const barcodeType = ref("Code128");

const generateBarcode = () => {
  // Barcode updates automatically when value changes
  console.log("Generated barcode for:", barcodeValue.value);
};
</script>
```

### Pattern 2: Export Barcode as Image

```vue
<template>
  <div>
    <ejs-qrcodegenerator
      id="qrcode"
      ref="qrcodeControl"
      value="https://www.example.com"
      width="200px"
      height="200px"
    ></ejs-qrcodegenerator>
    <button @click="exportAsImage">Download QR Code</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { QRCodeGeneratorComponent as EjsQrcodegenerator } from '@syncfusion/ej2-vue-barcode-generator';

const qrcodeControl = ref(null);

const exportAsImage = () => {
  if (qrcodeControl.value) {
    const instance = qrcodeControl.value.ej2_instances[0];
    instance.exportImage('qrcode', 'PNG');
  }
};
</script>
```

### Pattern 3: Multiple Barcode Types in One View

```vue
<template>
  <div class="barcode-grid">
    <div class="barcode-item">
      <h3>Barcode (Code128)</h3>
      <ejs-barcodegenerator
        type="Code128"
        value="SYNC123456"
        width="200px"
        height="150px"
      ></ejs-barcodegenerator>
    </div>
    <div class="barcode-item">
      <h3>QR Code</h3>
      <ejs-qrcodegenerator
        value="https://www.syncfusion.com"
        width="200px"
        height="200px"
      ></ejs-qrcodegenerator>
    </div>
    <div class="barcode-item">
      <h3>Data Matrix</h3>
      <ejs-datamatrixgenerator
        value="SHIPMENT-12345"
        width="200px"
        height="200px"
      ></ejs-datamatrixgenerator>
    </div>
  </div>
</template>

<style scoped>
  .barcode-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }
  
  .barcode-item {
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
  }
</style>

<script setup>
import { BarcodeGeneratorComponent as EjsBarcodegenerator } from '@syncfusion/ej2-vue-barcode-generator';
import { QRCodeGeneratorComponent as EjsQrcodegenerator } from '@syncfusion/ej2-vue-barcode-generator';
import { DataMatrixGeneratorComponent as EjsDatamatrixgenerator } from '@syncfusion/ej2-vue-barcode-generator';
</script>
```

## Key Props Summary

| Prop | Type | Purpose | Common Values |
|------|------|---------|----------------|
| `value` | string | Data to encode | "PRODUCT123", URLs, text |
| `width` | string | Component width | "200px", "100%" |
| `height` | string | Component height | "150px", "200px" |
| `type` | string | Barcode type (BarcodeGenerator only) | "Code39", "Code128", "Code93" |
| `mode` | string | Rendering mode | "SVG", "Canvas" |
| `displayText` | boolean | Show text below barcode | true, false |

## Related Skills

- [Implementing Syncfusion Vue Components](../) - Overview of all Vue components
- [Implementing Calendars](../calendars/implementing-calendars/) - For date-related barcode data
