---
name: code-comments
description: Open Waters house rules for writing code comments — when to comment, format, and annotations.
---

# Code Comments

- Comment the WHY (constraint, workaround, business rule), never the what/how.
  - ❌ `// Increment x by 1`
  - ✅ `// Offset by 1: the API is 1-indexed`
- One line. Longer rationale goes in the commit message or a linked issue.
- Place the comment on, directly above, or as close as possible to the exact line it explains.
- Always comment: workarounds for external bugs, preconditions, "editing this breaks X",
  non-obvious regexes/math, code adapted from elsewhere (link the source).
- Never comment: self-explanatory code, restating names, section headers.
- Write for a reader with no history. Never reference how the code used to be
  ("like the legacy X", "replaces the old Y", "previously this did Z"), the change being
  made, or the task/conversation/plan that produced it — that context belongs in the commit
  message. A comment must make sense to someone seeing only the current file.
- Link tickets/issues for TODOs: `// TODO(#123): ...`. Use FIXME only for known-broken code.
- Before commenting, try renaming/extracting so the code explains itself.
- When editing existing code, delete comments the change makes stale or redundant.
- Avoid repeating magic numbers that mirror values in the code.
