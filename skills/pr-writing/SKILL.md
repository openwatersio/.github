---
name: pr-writing
description: Open Waters conventions for writing pull requests, issues, commit messages, and docs prose. Use when drafting or editing a PR/issue title or body, a commit message, or durable documentation in an Open Waters repo.
---

# PR and prose writing

The essentials:

- Titles are concise and plain-language, written for the project's consumer, not the implementer: "Fix water appearing over land in the Great Lakes", not "Clamp great_lakes negative values under land".
- Bodies never start with a heading — the first paragraph is the summary. Use checklists for progress; keep the body updated as the PR evolves.
- Durable writing describes the current state only, never what changed or what came before. History belongs in commit messages.
- Commit subjects are imperative and plain-language; the body explains why. Match the prefix style already in the repo's log.
- Never hard-wrap prose at a column width.
- Never put a `Claude-Session:` trailer or a claude.ai/code session URL in a commit message, PR, or issue. Most openwatersio repos are public, so a URL that is private to the account only leaks internal workflow, and a merged commit message can't be fixed without rewriting public history. Keep the `Co-Authored-By:` trailer.

## Screenshots

`gh issue create`, `gh issue edit`, `gh pr create`, and `gh pr edit` take `--attach 'path#alt text'`, which uploads the file and rewrites a matching `![alt](./shot.png)` reference in the body to the asset URL. The rewrite only fires when the `--attach` path matches the body's path form. An absolute path still uploads and exits 0, but appends a second copy to the end of the body and leaves the in-body link broken.

- Run `gh` from the images' directory and use the same relative path in both places.
- Verify with `gh issue view N --json body -q .body | grep '!\['` (or `gh pr view`). A `user-attachments/assets/` URL means it rewrote; a `./` path means it didn't.

Read [docs/agents/writing-style.md](../../docs/agents/writing-style.md) for the full rules.
