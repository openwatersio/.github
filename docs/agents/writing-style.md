# Writing style

Rules for prose in docs, READMEs, commit messages, pull requests, and issues across Open Waters repos.

## Prose

- Run all content intended for human consumption through the [humanizer](https://github.com/blader/humanizer) skill, if your agent harness has it installed, not to hide that it's AI generated, but to make it easier for humans to read.
- Never hard-wrap prose at a column width. Each paragraph and list item stays on one physical line; the editor soft-wraps it. Code blocks and genuinely intentional line breaks (CLI output, addresses) keep their newlines. Don't reflow existing wrapped files unless you're already editing them.
- American English, unless a file or project already consistently uses British English.

## Current state only

Anything durable — docs, READMEs, code, comments, issue and PR bodies — describes the current state and what comes next. Never narrate what it used to say or do, what was added or rewritten, or what was missing before. No "previously", "now supports", "replaces the old X", "as of this rewrite". Write as if the reader has no history and the artifact has always looked this way. History belongs in commit messages, git blame, and the PR conversation.

Exceptions:

- a changelog, migration guide, or ADR whose purpose is history
- a comment whose WHY genuinely requires the old behavior (a workaround for a bug that still ships, a compatibility shim) — name the constraint, not the change

## Commit messages

- Imperative, plain-language subject lines that describe the change: "Show boat rentals on the chart", "Drop stale events from the stream".
- The body explains why, not what — the diff already shows what.
- Some repos prefix subjects with an area token ("plugins:", "docs:") or conventional-commit types. Match the style already in that repo's log.

## Pull request and issue titles

- Concise and straightforward. Titles should make sense to the _consumer_ of the project, who may be a non-technical user. Prefer plain language over jargon.
  - ❌ "DEPARE: bound the nodata pass and re-enable-ready (perf + seam correctness)"
  - ✅ "Re-enable depth areas with improved performance and seam correctness"
  - ❌ "Clamp great_lakes negative values under land"
  - ✅ "Fix water appearing over land in the Great Lakes"
- State the problem or the outcome, not the implementation.

## Pull request and issue bodies

- Don't start with a heading (`# Summary`, `## Problem`). The first paragraph is obviously the summary.
- Headings never have emdashes or parentheticals: "## Licensing", not "## Licensing — passes the gate".
- Use checklists to track remaining tasks and progress.
- As a PR evolves, update the original body to describe the current state of the code. A one-line note at the end ("_Updated to reflect x in commit deadbeef_") is fine but not always necessary.
- A PR that changes committed generated data should say what the numbers went from and to, because a giant regenerated diff can't be reviewed any other way.
