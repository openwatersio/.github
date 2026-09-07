# Agent instructions in repos

Every repo keeps one source of truth for project instructions: `CONTRIBUTING.md`, written for humans and AI agents alike. `AGENTS.md` and `CLAUDE.md` exist only so each harness finds it, and each is a one-line pointer:

```markdown
Read [CONTRIBUTING.md](CONTRIBUTING.md) — the project layout, build, dev loop, checks, and release process all live there.
```

Don't duplicate content across the three files. When a harness-specific file needs more than the pointer, limit it to things that genuinely only apply to that harness (for example, notes about that agent's tooling), and keep policy in CONTRIBUTING.md.

## What CONTRIBUTING.md contains

Document what the repo actually does, not aspirations. A convention belongs in the doc because the code and CI enforce or practice it, not because it sounds good.

- **Layout** — what each top-level directory is, one line each.
- **Getting started** — the commands to install, build, test, and run locally, copy-pasteable. Pin the toolchain with [mise](https://mise.jdx.dev) (`mise.toml`) and have CI install from that same file, so local and CI run identical versions.
- **Checks** — the exact commands CI runs, so a contributor can run them before pushing.
- **Releases** — how each artifact ships and what triggers it.
- **Gotchas** — traps that have cost real time, each entry stating what failure it prevents. These earn their place by having actually burned someone; don't write speculative warnings.

Point to GitHub issues for planned work rather than maintaining roadmap sections that go stale.

## Keep docs and CI in sync

When CONTRIBUTING.md documents commands, CI should run those same entrypoints (for example, `bin/*` scripts used by both). If you change the build, update the doc, the scripts, and the workflow together.
