---
name: hex-math
description: Reference for hexagonal grid algorithms and coordinate systems. Use when implementing movement, pathfinding, range calculations, or line of sight. Triggers on "hex", "hexagon", "grid", "coordinates", "pathfinding", "neighbors".
allowed-tools: Read
---

# Hex Grid Mathematics Reference

## Coordinate Systems

### Cube Coordinates (Recommended)
- Three axes: q, r, s where q + r + s = 0
- Best for algorithms and math
- Easy neighbor calculation, distance, rotation

### Offset Coordinates
- Two axes: col, row
- Better for storage and display
- Odd-q or even-q offset for pointy-top hexes

## Key Algorithms

### Cube to Offset (odd-q)
```dart
int col = q;
int row = r + (q - (q & 1)) ~/ 2;
```

### Offset to Cube (odd-q)
```dart
int q = col;
int r = row - (col - (col & 1)) ~/ 2;
int s = -q - r;
```

### Distance
```dart
int distance(Hex a, Hex b) {
  return (abs(a.q - b.q) + abs(a.r - b.r) + abs(a.s - b.s)) ~/ 2;
}
```

### Neighbors (6 directions)
```dart
const directions = [
  Hex(1, -1, 0), Hex(1, 0, -1), Hex(0, 1, -1),
  Hex(-1, 1, 0), Hex(-1, 0, 1), Hex(0, -1, 1),
];

List<Hex> neighbors(Hex h) {
  return directions.map((d) => Hex(h.q + d.q, h.r + d.r, h.s + d.s)).toList();
}
```

### Hex to Pixel (pointy-top)
```dart
double x = size * (sqrt(3) * q + sqrt(3)/2 * r);
double y = size * (3/2 * r);
```

### Pixel to Hex
```dart
double q = (sqrt(3)/3 * x - 1/3 * y) / size;
double r = (2/3 * y) / size;
// Then round to nearest hex
```

### Line Drawing (for line of sight)
```dart
List<Hex> lineDraw(Hex a, Hex b) {
  int n = distance(a, b);
  List<Hex> results = [];
  for (int i = 0; i <= n; i++) {
    results.add(hexRound(hexLerp(a, b, i / max(n, 1))));
  }
  return results;
}
```

### Range (all hexes within N)
```dart
List<Hex> hexesInRange(Hex center, int range) {
  List<Hex> results = [];
  for (int q = -range; q <= range; q++) {
    for (int r = max(-range, -q - range); r <= min(range, -q + range); r++) {
      int s = -q - r;
      results.add(Hex(center.q + q, center.r + r, center.s + s));
    }
  }
  return results;
}
```

## Reference
Full guide: https://www.redblobgames.com/grids/hexagons/
