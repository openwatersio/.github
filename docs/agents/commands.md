# Command names

Every npm repo gives the same job the same command name, so a contributor or agent who knows one repo can run another without reading its `package.json`. [slackwater-database](https://github.com/openwatersio/slackwater-database/blob/main/CONTRIBUTING.md#commands) is the reference implementation.

## Root commands

| Command                           | Does                                                                                                                                                                                      |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `npm run check`                   | Everything the main CI job checks: lint, test, and any validation. Run it before pushing.                                                                                                 |
| `npm test`                        | Every workspace's `test` script, found by `npm test --workspaces --if-present` rather than a hand-kept list, so a new workspace's tests run in CI without anyone remembering to add them. |
| `npm run build`                   | Build what other workspaces or the published package depend on.                                                                                                                           |
| `npm run lint` / `npm run format` | Check / write formatting.                                                                                                                                                                 |
| `npm run validate`                | Fail when committed generated data or published output is out of date.                                                                                                                    |

A single-package repo uses the same names. A repo with nothing to validate omits `validate` and lets `check` run lint and test.

## Workspace verbs

Each workspace names its scripts with the same verbs, run with `-w <workspace>`:

| Verb             | Means                                                                                                                                                 |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `import`         | Pull a source's data into the repo's data directory.                                                                                                  |
| `refresh:<name>` | Rewrite a pinned snapshot or fixture. The diff is reviewed before it is committed.                                                                    |
| `report:<name>`  | A diagnostic that changes no tracked file. It may write to an ignored `tmp/`.                                                                         |
| `validate`       | Check data against its publisher or its own schema.                                                                                                   |
| `test:<variant>` | Tests that need something CI runs separately, such as `test:docker` or `test:swift`. Keep them out of `test` so `npm test` works on a plain checkout. |

Name a script for what it does to the repo, not for the tool or the old habit: `refresh:places`, not `fetch-places`.

## Rules

- `test` runs once and exits: `vitest run`, never bare `vitest`, which waits in watch mode and hangs `npm run check` and CI.
- CI calls the same entrypoints CONTRIBUTING.md documents, per [Keep docs and CI in sync](agent-instructions.md#keep-docs-and-ci-in-sync).
- CONTRIBUTING.md lists every root command and workspace verb in one table under a `Commands` heading.
- Renaming a script means updating workflows, READMEs, `Usage:` comments, and error messages in the same change. Search for the old name before opening the PR; a stale name in an error message sends the next reader to a command that does not exist.
