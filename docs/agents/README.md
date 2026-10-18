# Agent docs

Shared conventions for working in Open Waters repositories, written for both humans and AI coding agents. Contributors here use different agent harnesses (Claude Code, Codex, Copilot, and others), so these docs are harness-neutral: plain markdown any agent can read.

Individual repos link here from their `AGENTS.md`, `CLAUDE.md`, or `CONTRIBUTING.md`. Repo-specific instructions (build commands, architecture, gotchas) stay in each repo; only conventions shared across the org live here.

- [agent-instructions.md](agent-instructions.md) — how repos document themselves for agents: one CONTRIBUTING.md, pointer files for the rest
- [commands.md](commands.md) — shared npm command names: `check`, `test`, and the `import`, `refresh:`, `report:` workspace verbs
- [writing-style.md](writing-style.md) — prose, commit messages, and PR/issue conventions
- [marketing.md](marketing.md) — required marketing skills, setup, and when to use them
- [releases.md](releases.md) — preparation checklist and release notes for every release, including Swift, apps, npm, and data artifacts
- [npm-releases.md](npm-releases.md) — npm scope policy and how packages are published

Procedural conventions also ship as [Agent Skills](https://agentskills.io) in [`skills/`](../../skills/) at the root of this repo. Claude Code subagents live in [`agents/`](../../agents/). Each is plain markdown, so other harnesses can read one as instructions. Repository tiers, GitHub settings, and the audit baseline live in [REPOSITORY_STANDARDS.md](../../REPOSITORY_STANDARDS.md).
