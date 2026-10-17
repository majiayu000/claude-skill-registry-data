---
name: solidworks-design-vault-cad
description: Access and utilize production-ready SolidWorks parametric 3D CAD models with manufacturing intelligence for mechanical design projects.
triggers:
  - "open a SolidWorks model from the design vault"
  - "find a parametric CAD assembly for manufacturing"
  - "load a gear or sprocket model with design tables"
  - "get a production-ready SolidWorks part file"
  - "access mechanical CAD templates with BOM automation"
  - "use SolidWorks files with manufacturing constraints"
  - "configure a parametric assembly from the vault"
  - "export CAD models with material properties"
---

# SolidWorks Design Vault CAD Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## Overview

The SolidWorks Design Vault is a curated repository of production-ready parametric 3D CAD models built for professional mechanical design. It contains `.SLDPRT` (part files), `.SLDASM` (assembly files), and `.SLDDRW` (drawing files) optimized for real-world manufacturing with GD&T principles, tolerance analysis, and material-conscious geometry.

Each model features:
- **Parametric DNA**: Global variables and linked dimensions for automatic updates
- **Manufacturing Intelligence**: Draft angles, wall thickness, thread forms (ASME B1.1, ISO 68-1)
- **Design Tables**: Multiple configurations for common variations
- **BOM Automation**: Auto-populated bills of materials with material density and machining time
- **Multi-format Export**: STEP, IGES, STL outputs with proper face normals

## Installation

### Download the Repository

```bash
# Clone the repository
git clone https://github.com/fgiafrica/SolidWork-Design-Vault.git
cd SolidWork-Design-Vault
```

### Access via Web Interface

Visit the project page and use the download button:
```
https://fgiafrica.github.io/SolidWork-Design-Vault/
```

### File Requirements

- **SolidWorks Version**: 2021 or later recommended
- **File Extensions**: `.SLDPRT`, `.SLDASM`, `.SLDDRW`
- **Dependencies**: Some assemblies reference standard parts libraries

## Repository Structure

```
SolidWork/
├── Assemblies/          # Multi-body interlocking systems
│   ├── Linear_Actuator/ # Ball screw mechanism with preload
│   └── Vise_Grip/       # Compound leverage simulation
├── Parts/               # Standalone manufacturable elements
│   ├── Sprockets/       # ISO-standard tooth profiles
│   └── Gaskets/         # Compressed elastomer shapes
├── Templates/           # Custom property tabs & BOM formats
│   └── Sheet_Metal/     # Bend allowance tables included
└── Drawings/            # 2D representations with ordinate dims
    └── Gearbox_Exploded/ # Ballooned view for assembly instructions
```

## Working with Part Files

### Opening a Basic Part

```python
# Example: Accessing part metadata (pseudo-code for automation scripts)
import os

part_path = "Parts/Sprockets/Double_Pitch_40_Bore.sldprt"

# Check file exists
if os.path.exists(part_path):
    print(f"Part located: {part_path}")
    # Open in SolidWorks API or convert to neutral format
```

### Understanding Design Tables

Design tables allow configuration switching within a single file:

1. Open `Double_Pitch_40_Bore.sldprt`
2. Right-click on "Design Table" in Feature Manager
3. Select configuration from dropdown (e.g., "1/2 inch bore", "12mm bore")
4. Model regenerates with updated hub geometry and keyway

**Key Parameters in Design Tables:**
- `Bore_Diameter`: Shaft size
- `Hub_Length`: Axial engagement
- `Keyway_Width`: Per ISO 2491 or ANSI B17.1
- `Material`: Steel, Aluminum, Nylon

### Custom Properties

Each part contains manufacturing metadata:

```
Custom Properties:
├── Vendor_Part_Number: "SPK-40-2P-B12"
├── Material_Grade: "AISI 1045 Steel"
├── Surface_Finish: "125 RMS"
├── Weight: Auto-calculated from density
└── Estimated_Cost: Based on material volume
```

## Working with Assemblies

### Loading an Assembly

```bash
# Navigate to assembly directory
cd Assemblies/Linear_Actuator/

# Files you'll find:
# - Linear_Actuator_Main.sldasm (top-level)
# - Drive_Screw.sldasm (sub-assembly)
# - Motor_Mount.sldprt
# - Ball_Nut.sldprt
```

### Assembly Mate Structure

Assemblies use disciplined mating:
- **Concentric mates**: For shaft/bore relationships
- **Coincident mates**: For planar surfaces
- **Distance mates**: With limit constraints
- **NO "Width" or "Symmetric" mates** (per contributing protocols)

### BOM Extraction

```python
# Example: Extracting BOM data for manufacturing
import csv

def extract_bom(assembly_path):
    """
    Parse SolidWorks custom properties for BOM generation
    Note: Requires SolidWorks API or pre-exported CSV
    """
    bom_data = {
        'part_number': 'LA-001',
        'description': 'Linear Actuator Assembly',
        'components': [
            {'name': 'Drive_Screw', 'qty': 1, 'material': 'AISI 4140'},
            {'name': 'Ball_Nut', 'qty': 1, 'material': 'Bronze'},
            {'name': 'Motor_Mount', 'qty': 2, 'material': 'AL 6061-T6'}
        ]
    }
    return bom_data

# Export to CSV
bom = extract_bom("Linear_Actuator_Main.sldasm")
with open('bom_export.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'qty', 'material'])
    writer.writeheader()
    writer.writerows(bom['components'])
```

## Export Workflows

### Convert to Neutral Formats

For CNC programming or FEA analysis:

**SolidWorks GUI Method:**
1. File → Save As
2. Select format: `.STEP` (AP214 for machining), `.IGES`, `.STL`
3. Options → Check "Export as one file" for assemblies
4. Confirm face normals are outward-pointing

**Automated Export (SolidWorks API - VBA Example):**

```vba
Sub ExportToSTEP()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim filePath As String
    
    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc
    
    filePath = "C:\Export\" & swModel.GetTitle & ".STEP"
    
    ' Export with AP214 protocol
    swModel.SaveAs3 filePath, 0, 0
End Sub
```

### Python Automation with pywin32

```python
import win32com.client
import os

def export_part_to_step(sldprt_path, output_dir):
    """
    Automate SolidWorks export using Windows COM interface
    Requires SolidWorks installed and pywin32 package
    """
    sw = win32com.client.Dispatch("SldWorks.Application")
    sw.Visible = True
    
    # Open document
    doc = sw.OpenDoc(sldprt_path, 1)  # 1 = Part document
    
    # Set STEP export options
    output_path = os.path.join(output_dir, 
                               os.path.basename(sldprt_path).replace('.SLDPRT', '.STEP'))
    
    # Save as STEP AP214
    doc.SaveAs(output_path)
    sw.CloseDoc(doc.GetTitle())
    
    return output_path

# Usage
export_part_to_step(
    "Parts/Sprockets/Double_Pitch_40_Bore.sldprt",
    "/export/cnc_models/"
)
```

## Configuration Management

### Parametric Modification

```javascript
// Example: Modifying global variables programmatically
// (SolidWorks API - JavaScript via Node.js with edge-js)

const edge = require('edge-js');

const modifyParameter = edge.func(`
    async (input) => {
        var swApp = (SldWorks.SldWorks)System.Activator.CreateInstance(
            System.Type.GetTypeFromProgID("SldWorks.Application"));
        var doc = swApp.ActiveDoc;
        
        // Access equation manager
        var eqnMgr = doc.GetEquationMgr();
        
        // Update global variable (e.g., gear module)
        int index = eqnMgr.FindEquation("\"Module\"");
        eqnMgr.SetEquationValue(index, (double)input.value);
        
        doc.ForceRebuild3(true);
        return "Parameter updated";
    }
`);

modifyParameter({ value: 2.5 }, (error, result) => {
    console.log(result); // "Parameter updated"
});
```

### Design Table Templates

Create custom configurations:

```html
<!-- Design Table in Excel format embedded in .SLDPRT -->
<table>
  <tr>
    <th>Configuration</th>
    <th>Bore_Diameter@Sketch1</th>
    <th>Hub_Length@Boss-Extrude1</th>
    <th>Material</th>
  </tr>
  <tr>
    <td>Config_12mm</td>
    <td>12</td>
    <td>30</td>
    <td>Steel_1045</td>
  </tr>
  <tr>
    <td>Config_1/2in</td>
    <td>0.5in</td>
    <td>1.25in</td>
    <td>Aluminum_6061</td>
  </tr>
</table>
```

## Common Patterns

### Pattern 1: Rapid Prototyping Workflow

```bash
# 1. Select base part
cd Parts/Sprockets/

# 2. Open in SolidWorks
# File: Double_Pitch_40_Bore.sldprt

# 3. Modify design table for your shaft size
# Right-click Design Table → Edit Table

# 4. Export to 3D printer format
# File → Save As → .STL
# Resolution: Fine (0.01mm deviation)

# 5. Generate 2D drawing for documentation
# Make Drawing from Part → Template: ANSI_B
```

### Pattern 2: Assembly Integration

```python
# Workflow for integrating vault parts into custom assembly

def integrate_vault_part(vault_part_path, custom_assembly_path):
    """
    Add a vault component to your custom assembly
    """
    steps = [
        "1. Open your target assembly in SolidWorks",
        "2. Insert → Component → Existing Part/Assembly",
        f"3. Browse to: {vault_part_path}",
        "4. Place component at desired location",
        "5. Add mates: Concentric (shaft to bore), Coincident (faces)",
        "6. Verify clearances with Interference Detection"
    ]
    return "\n".join(steps)

print(integrate_vault_part(
    "Parts/Sprockets/Double_Pitch_40_Bore.sldprt",
    "MyProject/CustomGearbox.sldasm"
))
```

### Pattern 3: Material Library Linkage

```html
<!-- Custom material XML for SolidWorks material database -->
<material name="AISI_1045_Normalized">
  <density>7850</density> <!-- kg/m³ -->
  <elastic_modulus>200000</elastic_modulus> <!-- MPa -->
  <poisson_ratio>0.29</poisson_ratio>
  <yield_strength>530</yield_strength> <!-- MPa -->
  <thermal_expansion>11.5e-6</thermal_expansion> <!-- /°C -->
</material>
```

## Troubleshooting

### Issue: File Won't Open

**Cause**: SolidWorks version mismatch (file created in newer version)

**Solution**:
```bash
# Check SolidWorks version required
# Look in file properties or README

# Option 1: Update SolidWorks to 2021+
# Option 2: Request STEP export from repository maintainer
```

### Issue: Missing References in Assembly

**Cause**: External component paths broken

**Solution**:
```python
# Fix broken references
def fix_assembly_references(assembly_path):
    """
    Update file paths for moved components
    """
    print("In SolidWorks:")
    print("1. File → Find References")
    print("2. Browse to new component locations")
    print("3. Save assembly to update paths")
    print("Alternative: Use Pack and Go to collect all files")

fix_assembly_references("Assemblies/Linear_Actuator/Linear_Actuator_Main.sldasm")
```

### Issue: Design Table Not Updating

**Cause**: Excel link broken or cell formulas incorrect

**Solution**:
```vba
' Rebuild design table
Sub RefreshDesignTable()
    Dim swApp As SldWorks.SldWorks
    Dim swModel As SldWorks.ModelDoc2
    Dim swDesignTable As SldWorks.DesignTable
    
    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc
    Set swDesignTable = swModel.GetDesignTable
    
    ' Force update
    swDesignTable.Edit True
    swDesignTable.UpdateModel
End Sub
```

### Issue: Export File Size Too Large

**Cause**: Unnecessary detail in STL/STEP export

**Solution**:
```bash
# Reduce file size for exports
# SolidWorks → Tools → Options → Export

# STL Settings:
#   Resolution: Coarse (0.1mm for prototypes)
#   Binary format: YES (smaller than ASCII)

# STEP Settings:
#   Protocol: AP203 (simpler than AP214 for viewing)
#   Spline to polyline: YES (reduces complexity)
```

## Advanced Usage

### FEA Preparation

```python
# Prepare models for Finite Element Analysis
def prepare_for_fea(part_path):
    """
    Export with mid-surface extraction for shell elements
    """
    instructions = {
        'sheet_metal_parts': [
            'Insert → Surface → Mid-Surface',
            'Select all sheet metal faces',
            'Export mid-surface as separate body'
        ],
        'solid_parts': [
            'Simplify geometry: Suppress small fillets',
            'Remove cosmetic features',
            'Export as Parasolid (.x_t) for solver import'
        ]
    }
    return instructions

print(prepare_for_fea("Parts/Gaskets/O-Ring_Housing.sldprt"))
```

### Batch Processing

```python
import os
import subprocess

def batch_convert_to_pdf(drawings_dir):
    """
    Convert all .SLDDRW files to PDF for manufacturing
    Requires SolidWorks batch converter or API
    """
    drawings = [f for f in os.listdir(drawings_dir) if f.endswith('.SLDDRW')]
    
    for dwg in drawings:
        input_path = os.path.join(drawings_dir, dwg)
        output_path = input_path.replace('.SLDDRW', '.PDF')
        
        # Using SolidWorks Task Scheduler (command line)
        cmd = [
            'C:\\Program Files\\SOLIDWORKS\\swScheduler.exe',
            '/task:ExportFiles',
            f'/input:{input_path}',
            f'/output:{output_path}',
            '/format:PDF'
        ]
        subprocess.run(cmd)
        
    return f"Converted {len(drawings)} drawings"

# Usage
batch_convert_to_pdf("Drawings/Gearbox_Exploded/")
```

## Contributing to the Vault

### File Preparation Checklist

```markdown
Before submitting new models:

- [ ] Design table with ≥3 configurations
- [ ] Custom properties filled (Vendor_Part_Number, Material_Grade)
- [ ] Mates use only Concentric/Coincident/Distance (no Width/Symmetric)
- [ ] Mass properties calculated (Tools → Mass Properties)
- [ ] Drawings follow ASME Y14.5 dimensioning standards
- [ ] README.md in model directory with design intent notes
```

### Pull Request Template

```bash
# Fork repository
git clone https://github.com/YOUR_USERNAME/SolidWork-Design-Vault.git
cd SolidWork-Design-Vault

# Create feature branch
git checkout -b feature/new-planetary-gearbox

# Add your files
cp ~/MyDesigns/Planetary_Gearbox/*.sldprt Parts/Gearboxes/

# Commit with descriptive message
git add .
git commit -m "Add planetary gearbox with 3:1, 5:1, 10:1 ratios"

# Push and create PR
git push origin feature/new-planetary-gearbox
```

## Resources

- **Official Repository**: https://github.com/fgiafrica/SolidWork-Design-Vault
- **SolidWorks API Documentation**: https://help.solidworks.com/API
- **GD&T Standards**: ASME Y14.5-2018
- **Thread Standards**: ISO 68-1 (metric), ASME B1.1 (unified)

## License

MIT License - Free for commercial use with attribution. Design intent notes must remain accessible in redistributed files.
