# Agent docs

Shared conventions for working in Open Waters repositories, written for both humans and AI coding agents. Contributors here use different agent harnesses (Claude Code, Codex, Copilot, and others), so these docs are harness-neutral: plain markdown any agent can read.

Individual repos link here from their `AGENTS.md`, `CLAUDE.md`, or `CONTRIBUTING.md`. Repo-specific instructions (build commands, architecture, gotchas) stay in each repo; only conventions shared across the org live here.

- [agent-instructions.md](agent-instructions.md) — how repos document themselves for agents: one CONTRIBUTING.md, pointer files for the rest
- [writing-style.md](writing-style.md) — prose, commit messages, and PR/issue conventions
- [releases.md](releases.md) — preparation checklist for every release, including Swift, apps, npm, and data artifacts
- [npm-releases.md](npm-releases.md) — npm scope policy and how packages are published

Procedural conventions also ship as [Agent Skills](https://agentskills.io) in [`skills/`](../../skills/) at the root of this repo. Repository tiers, GitHub settings, and the audit baseline live in [REPOSITORY_STANDARDS.md](../../REPOSITORY_STANDARDS.md).
