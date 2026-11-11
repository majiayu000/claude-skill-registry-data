---
description: Add labels, captions, and text references to every figure in a LaTeX paper
model: haiku
---

# Check References
- Every picture and table needs a label and a caption, and must be referenced in
  the text
- Captions should only say what is done. Comments and other content go in the text

# Add Captions and Labels

- For all figures in the LaTeX files in the passed dir, add the caption and label to
  the commented section.

- For instance convert

  ````latex
  %     ```
  % rendered_images:end
  % render_images:begin
  \begin{figure}[!ht]
    \centering
    \includegraphics[width=\linewidth]{figs/02_architecture.1.png}
    \caption{Confounding adjustment in causal inference}
    \label{fig:confounding_adjustment}
  \end{figure}
  % render_images:end
  ````

  to

  ````latex
  %     ```
  % caption=Confounding adjustment in causal inference
  % label=fig:confounding_adjustment
  % rendered_images:end
  % render_images:begin
  \begin{figure}[!ht]
    \centering
    \includegraphics[width=\linewidth]{figs/02_architecture.1.png}
    \caption{Confounding adjustment in causal inference}
    \label{fig:confounding_adjustment}
  \end{figure}
  % render_images:end
  ````

# Create Labels and Captions From Scratch

- If a figure has no caption or label, infer them from the filename and surrounding
  context
  - E.g., `figs/02_architecture.1.png` becomes `label=fig:architecture`,
    `caption=System architecture overview`
- Use short, lowercase label names with underscores

# Add References in the Text

- If a figure has a label but no citation in the text, add a parenthetical reference
  near the most relevant paragraph:
  ```latex
  (see Fig.~\ref{fig:confounding_adjustment})
  ```

# Verify No Orphaned References

- Scan the text for `\ref{fig:xxx}` or `\ref{tab:xxx}` with no matching `\label` in
  any figure or table environment
- Report orphaned references as warnings. Do not silently delete them

# Verification

- [ ] Every figure and table has a `\label` and a `\caption`
- [ ] Every figure and table `\label` is referenced by a `\ref` in the text
- [ ] No orphaned `\ref{fig:xxx}` or `\ref{tab:xxx}` exists without a matching
      `\label` in any figure or table environment
