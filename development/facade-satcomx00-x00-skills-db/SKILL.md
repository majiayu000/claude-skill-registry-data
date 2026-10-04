---
name: facade
description: Provide a simplified interface to a complex subsystem.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: structural-pattern
---

# Facade

Provides a single, simplified interface that hides the complexity of a subsystem. Clients use the facade instead of the many subsystem classes directly.

## When to Use

- A subsystem has many classes with complex interactions
- You want to layer your architecture (facade = entry point to a layer)
- Integration with a complex library or framework should be encapsulated
- You need a simple default use case while keeping the subsystem accessible for advanced use

## How to Apply

1. Check whether a simpler interface is possible and valuable
2. Declare and implement the `Facade` class, delegating to subsystem classes
3. Clients call the facade instead of directly accessing subsystem classes
4. Keep subsystem classes accessible for clients that need fine-grained control

## Example

```ts
// Complex subsystem
class VideoDecoder  { decode(file: string)  { /* … */ } }
class AudioMixer    { fix(audio: string)    { /* … */ } }
class BitrateReader { read(file: string)    { return 1080; } }

// Facade
class VideoConverter {
  private decoder = new VideoDecoder();
  private mixer   = new AudioMixer();
  private reader  = new BitrateReader();

  convert(filename: string, format: string): string {
    const bitrate = this.reader.read(filename);
    this.decoder.decode(filename);
    this.mixer.fix(filename);
    return `output.${format}`;
  }
}

// Client only needs one call
const converter = new VideoConverter();
const output = converter.convert('funny-cats.ogg', 'mp4');
```

## References

- [refactoring.guru/design-patterns/facade](https://refactoring.guru/design-patterns/facade)
