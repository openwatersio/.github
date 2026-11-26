# Agent docs

Shared conventions for working in Open Waters repositories, written for both humans and AI coding agents. Contributors here use different agent harnesses (Claude Code, Codex, Copilot, and others), so these docs are harness-neutral: plain markdown any agent can read.

Individual repos link here from their `AGENTS.md`, `CLAUDE.md`, or `CONTRIBUTING.md`. Repo-specific instructions (build commands, architecture, gotchas) stay in each repo; only conventions shared across the org live here.

- [rigor.md](rigor.md) — diagnose and fix causes instead of working around them, verify against reality and independent references, follow every lead before asking, and finish the whole job
- [agent-instructions.md](agent-instructions.md) — how repos document themselves for agents: one CONTRIBUTING.md, pointer files for the rest
- [swift.md](swift.md) — Swift compiler selection, mise installation, runner validation and recovery
- [iOS projects](../../REPOSITORY_STANDARDS.md#ios-projects) — native Xcode JSON projects, committed project inputs, and mise-managed development tools
- [commands.md](commands.md) — shared npm command names: `check`, `test`, and the `import`, `refresh:`, `report:` workspace verbs
- [writing-style.md](writing-style.md) — prose, stating each fact once in code and docs, commit messages, and PR/issue conventions
- [marketing.md](marketing.md) — required marketing skills, setup, and when to use them
- [releases.md](releases.md) — preparation checklist and release notes for every release, including Swift, apps, npm, and data artifacts
- [npm-releases.md](npm-releases.md) — npm scope policy and how packages are published

Procedural conventions also ship as [Agent Skills](https://agentskills.io) in [`skills/`](../../skills/) at the root of this repo. Claude Code subagents live in [`agents/`](../../agents/). Each is plain markdown, so other harnesses can read one as instructions. Repository tiers, GitHub settings, and the audit baseline live in [REPOSITORY_STANDARDS.md](../../REPOSITORY_STANDARDS.md).

## Install the shared skills

The marketplace packages the skills for Claude Code, Codex, and GitHub Copilot CLI. The skills share their source files; individual instructions may depend on tools installed on your machine.

### Claude Code

In a Claude Code session:

```text
/plugin marketplace add openwatersio/.github
/plugin install openwaters@openwaters
```

To receive updates automatically, open `/plugin`, select **Marketplaces**, choose **openwaters**, and enable auto-update. Changes load on the next launch, or in the current session with `/reload-plugins`.

### Codex

In a terminal, add the marketplace:

```sh
codex plugin marketplace add openwatersio/.github
```

In the Codex desktop app, open the Plugins directory, select the Open Waters marketplace, and install **openwaters**. To refresh the Git marketplace, run `codex plugin marketplace upgrade openwaters`; restart the desktop app to load updated files. Automatic refresh of Git marketplaces is not documented.

### GitHub Copilot CLI

In a Copilot CLI session:

```text
/plugin marketplace add openwatersio/.github
/plugin install openwaters@openwaters
```

To enable session-start updates, set `autoUpdate` to `true` on the `openwaters` entry under `extraKnownMarketplaces` in `~/.copilot/settings.json`, preserving the source recorded when adding the marketplace. This applies to interactive and `-p` sessions; SDK and server sessions do not auto-update. See the [Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference).

The plugin has no pinned version so Claude Code can detect updates from repository commits without a manual version bump. Claude Code also discovers the repository's `agents/`; the portable plugin installs the skills in Codex and Copilot CLI.
