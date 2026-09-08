# Agent instructions in repos

Every repo keeps one source of truth for project instructions: `CONTRIBUTING.md`, written for humans and AI agents alike. `AGENTS.md` and `CLAUDE.md` exist only so each harness finds it, and each is a one-line pointer:

```markdown
Read [CONTRIBUTING.md](CONTRIBUTING.md) — the project layout, build, dev loop, checks, and release process all live there.
```

Don't duplicate content across the three files. When a harness-specific file needs more than the pointer, limit it to things that genuinely only apply to that harness (for example, notes about that agent's tooling), and keep policy in CONTRIBUTING.md.

## What CONTRIBUTING.md contains

Document what the repo actually does, not aspirations. A convention belongs in the doc because the code and CI enforce or practice it, not because it sounds good.

- **Layout** — what each top-level directory is, one line each.
- **Getting started** — the commands to install, build, test, and run locally, copy-pasteable. CI defines the tested toolchain using GitHub Actions' native setup actions and runner-provided tools. Derive local [mise](https://mise.jdx.dev) tool versions in `mise.toml` from CI so contributors can reproduce that environment. Don't add mise to Actions merely to share a version file.
- **Checks** — the exact commands CI runs, so a contributor can run them before pushing.
- **Releases** — how each artifact ships and what triggers it. Document release-only toolchain differences and why they are needed, such as a newer Node/npm version for [trusted publishing](npm-releases.md#trusted-publishing).
- **Gotchas** — traps that have cost real time, each entry stating what failure it prevents. These earn their place by having actually burned someone; don't write speculative warnings.

Point to GitHub issues for planned work rather than maintaining roadmap sections that go stale.

## Keep docs and CI in sync

When CONTRIBUTING.md documents commands, CI should run those same entrypoints (for example, `bin/*` scripts used by both). If you change the build, update the doc, the scripts, and the workflow together.

When a CI toolchain or runner image changes, include the corresponding local `mise.toml` update in the same change. For runner-provided tools, check the versions in the runner image when choosing the local pins.

## Retire completed specs and plans

Every release is a checkpoint for retiring development specs and plans, including Swift packages, apps, npm packages, and data artifacts, regardless of how the release is triggered. Include the shared [release preparation checklist](releases.md#release-preparation-checklist) in the repository's `CONTRIBUTING.md`. Review specs and plans created or updated since the previous release, along with any carried forward from earlier releases. A self-contained implementation PR can do the cleanup at merge time; the release review catches anything left over.

Before deleting a spec or plan whose implementation is complete and merged:

- Preserve lasting API contracts, constraints, rationale, and operational guidance in maintained documentation. Describe the current behavior without retaining step-by-step implementation instructions for work already built.
- Record user-facing changes in the changelog or release notes.
- Update temporary roadmaps to show only remaining work, with links to the relevant issues. Carry forward unfinished plans; age alone is not a reason to delete them.

Include the documentation updates and completed spec or plan deletions in the release PR so a human can review what will remain. For releases triggered by a tag, GitHub release, or manual dispatch without a release PR, use a documentation cleanup PR reviewed and merged before publishing. Committed specs and plans remain available in Git history; they do not need to stay in the working tree for reference.
