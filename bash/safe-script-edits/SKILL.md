---
name: safe-script-edits
description: Use when changing code or data files with a script or shell command instead of the Edit tool - bulk replacements across several files, multi-line edits, inserting blocks, or any edit where the text contains \n, backslashes, quotes or Windows line endings.
---

# Ediciones con script sin romper nada

## Reglas

| Regla | Caso real |
|---|---|
| Nunca escribas código con un heredoc de bash ni con `sed` si el texto lleva `\n`, `\` o comillas. Usa la herramienta Edit, o un script de Python escrito con Write en el scratchpad. | Pasó tres veces: un `\n` dentro de un string de C# se convirtió en un salto de línea real y el archivo no compiló. Un `sed` también borró el zumbido del menú. |
| Cada sustitución con `assert s.count(old) == 1` (o el número esperado) antes de reemplazar. Si no coincide, el script para sin escribir. | Una sustitución por regex encontró 51 casos en 22 archivos cuando se esperaban 12. |
| Conserva los finales de línea: abre con `newline=''`, detecta CRLF o LF, normaliza a `\n`, edita y escribe con el final original. | Un script dejó CR CR LF en `BotPlayer.cs`. |
| Un bloque nuevo delante de un miembro va **encima** de su comentario `/// <summary>`, nunca entre el comentario y el miembro. | La revisión encontró 6 `<summary>` colgando del miembro equivocado. |
| El arte original y los assets base no se editan: lo derivado va a archivos nuevos. | Ver la skill `pixel-portrait-kitbash`. |
| Un `.cs` nuevo genera su `.meta` al abrir Unity. Súbelos juntos. | |

## Patrón

```python
import io
def edit(path, pairs, expected=1):
    s = io.open(path, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    s = s.replace('\r\n', '\n')
    for old, new in pairs:
        assert s.count(old) == expected, (path, old[:60], s.count(old))
        s = s.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
```

## Después

Compila y ejecuta los tests de lo tocado (ver la skill `batchmode-capture`). Revisa `git diff --stat`: si un archivo sale entero como cambiado, son los finales de línea.
