---
name: astropy
description: Astropy is the core Python package for astronomy, providing essential functionality for astronomical research and data analysis. 
category: Document Processing
source: antigravity
tags: [python, ai, workflow, document, presentation, image, cro]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/astropy
---


# Astropy

## Overview

Astropy is the core Python package for astronomy, providing essential functionality for astronomical research and data analysis. Use astropy for coordinate transformations, unit and quantity calculations, FITS file operations, cosmological calculations, precise time handling, tabular data manipulation, and astronomical image processing.

## When to Use This Skill

Use astropy when tasks involve:
- Converting between celestial coordinate systems (ICRS, Galactic, FK5, AltAz, etc.)
- Working with physical units and quantities (converting Jy to mJy, parsecs to km, etc.)
- Reading, writing, or manipulating FITS files (images or tables)
- Cosmological calculations (luminosity distance, lookback time, Hubble parameter)
- Precise time handling with different time scales (UTC, TAI, TT, TDB) and formats (JD, MJD, ISO)
- Table operations (reading catalogs, cross-matching, filtering, joining)
- WCS transformations between pixel and world coordinates
- Astronomical constants and calculations

## Quick Start

```python
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.io import fits
from astropy.table import Table
from astropy.cosmology import Planck18

# Units and quantities
distance = 100 * u.pc
distance_km = distance.to(u.km)

# Coordinates
coord = SkyCoord(ra=10.5*u.degree, dec=41.2*u.degree, frame='icrs')
coord_galactic = coord.galactic

# Time
t = Time('2023-01-15 12:30:00')
jd = t.jd  # Julian Date

# FITS files
data = fits.getdata('image.fits')
header = fits.getheader('image.fits')

# Tables
table = Table.read('catalog.fits')

# Cosmology
d_L = Planck18.luminosity_distance(z=1.0)
```

## Core Capabilities

### 1. Units and Quantities (`astropy.units`)

Handle physical quantities with units, perform unit conversions, and ensure dimensional consistency in calculations.

**Key operations:**
- Create quantities by multiplying values with units
- Convert between units using `.to()` method
- Perform arithmetic with automatic unit handling
- Use equivalencies for domain-specific conversions (spectral, doppler, parallax)
- Work with logarithmic units (magnitudes, decibels)

**See:** `references/units.md` for comprehensive documentation, unit systems, equivalencies, performance optimization, and unit arithmetic.

### 2. Coordinate Systems (`astropy.coordinates`)

Represent celestial positions and transform between different coordinate frames.

**Key operations:**
- Create coordinates with `SkyCoord` in any frame (ICRS, Galactic, FK5, AltAz, etc.)
- Transform between coordinate systems
- Calculate angular separations and position angles
- Match coordinates to catalogs
- Include distance for 3D coordinate operations
- Handle proper motions and radial velocities
- Query named objects from online databases

**See:** `references/coordinates.md` for detailed coordinate frame descriptions, transformations, observer-dependent frames (AltAz), catalog matching, and performance tips.

### 3. Cosmological Calculations (`astropy.cosmology`)

Perform cosmological calculations using standard cosmological models.

**Key operations:**
- Use built-in cosmologies (Planck18, WMAP9, etc.)
- Create custom cosmological models
- Calculate distances (luminosity, comoving, angular diameter)
- Compute ages and lookback times
- Determine Hubble parameter at any redshift
- Calculate density parameters and volumes
- Perform inverse calculations (find z for given distance)

**See:** `references/cosmology.md` for available models, distance calculations, time calculations, density parameters, and neutrino effects.

### 4. FITS File Handling (`astropy.io.fits`)

Read, write, and manipulate FITS (Flexible Image Transport System) files.

**Key operations:**
- Open FITS files with context managers
- Access HDUs (Header Data Units) by index or name
- Read and modify headers (keywords, comments, history)
- Work with image data (NumPy arrays)
- Handle table data (binary and ASCII tables)
- Create new FITS files (single or multi-extension)
- Use memory mapping for large files
- Access remote FITS files (S3, HTTP)

**See:** `references/fits.md` for comprehensive file operations, header manipulation, image and table handling, multi-extension files, and performance considerations.

### 5. Table Operations (`astropy.table`)

Work with tabular data with support for units, metadata, and various file formats.

**Key operations:**
- Create tables from arrays, lists, or dictionaries
- Read/write tables in multiple formats (FITS, CSV, HDF5, VOTable)
- Access and modify columns and rows
- Sort, filter, and index tables
- Perform database-style operations (join, group, aggregate)
- Stack and concatenate tables
- Work with unit-aware columns (QTable)
- Handle missing data with masking

**See:** `references/tables.md` for table creation, I/O operations, data manipulation, sorting, filtering, joins, grouping, and performance tips.

### 6. Time Handling (`astropy.time`)

Precise time representa
