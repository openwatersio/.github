# Writing style

Rules for prose in docs, READMEs, commit messages, pull requests, and issues across Open Waters repos, and in outbound email sent on behalf of Open Waters, plus where code and docs state the values they share.

## Prose

- Run all content intended for human consumption through the [humanizer](https://github.com/blader/humanizer) skill, if your agent harness has it installed, not to hide that it's AI generated, but to make it easier for humans to read.
- Never hard-wrap prose at a column width. Each paragraph and list item stays on one physical line; the editor soft-wraps it. Code blocks and genuinely intentional line breaks (CLI output, addresses) keep their newlines. Don't reflow existing wrapped files unless you're already editing them.
- American English, unless a file or project already consistently uses British English.

## Current state only

Anything durable — docs, READMEs, code, comments, issue and PR bodies — describes the current state and what comes next. Never narrate what it used to say or do, what was added or rewritten, or what was missing before. No "previously", "now supports", "replaces the old X", "as of this rewrite". Write as if the reader has no history and the artifact has always looked this way. History belongs in commit messages, git blame, and the PR conversation.

Exceptions:

- a changelog, migration guide, or ADR whose purpose is history
- a PR review summary that records review coverage, findings and follow-up verification
- a comment whose WHY genuinely requires the old behavior (a workaround for a bug that still ships, a compatibility shim) — name the constraint, not the change

## Don't count our own things

Never state how many of something we ship: "five read-only tools", "three chart styles", "the four supported datums". Adding one makes the sentence false, and the number is almost always next to the list it counts, so it tells the reader nothing they can't see. Name the things, or describe what they cover, and let the list be its own count.

This is about inventories of our own features, not about facts with a source. Documented limits and measurements stay in the one place that defines them: "100 requests per minute", "at most 10 MMSIs", "the next seven days" when that is the API's default. So do figures about the outside world, as long as they say when they were checked — the way the comparison sections date their claims. Each is written once, and everywhere else links there, as [State each fact once](#state-each-fact-once) describes.

The test is whether shipping one more of a thing would make the sentence wrong. If it would, drop the number.

## State each fact once

A value that something else dictates, such as a limit, threshold, timeout, port, version, schedule, path, or format, has one source: a named constant or config key in code, or one section of one doc. Everything else refers to that source by name or link instead of repeating the value. This applies to code, comments, and docs alike.

- Code uses the constant, not the literal: `MAX_CONNECTIONS`, not `5`. A value set by an outside system, such as an upstream API's rate limit, becomes a constant at the boundary with a link to the upstream doc.
- Comments and docs say what the value does and point to where it is set: "Clients over the connection limit are refused (see [limits](docs/limits.md))", not "Clients that open more than 5 connections in 10 minutes are refused".
- The source states the value, and why it is that value when that isn't obvious.
- Text a reader can't follow a link from, such as an error message, CLI help, or an API description, reads the value from the source instead of typing it out.
- Tests are the exception: they pin the value by hand. A test that reads the constant still passes when the constant is wrong.

The test: if the value changed at its source, which files would need editing? Any file beyond the source and the tests that pin it holds a copy.

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
- Every PR body includes a `Review` section following the [review reporting requirements](../../skills/openwaters-review/SKILL.md#reporting-review-in-the-pr), including when no review completed.
- As a PR evolves, update the original body to describe the current state of the code. A one-line note at the end ("_Updated to reflect x in commit deadbeef_") is fine but not always necessary.
- A PR that changes committed generated data should say what the numbers went from and to, because a giant regenerated diff can't be reviewed any other way.
