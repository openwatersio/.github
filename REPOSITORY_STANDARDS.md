# Open Waters Repository Standards

This is the advisory baseline for creating and auditing Open Waters repositories. Apply it with
judgment: report differences and intentional exceptions, and change files or settings only when
asked. It is not an enforcement manifest.

## How to use this document

1. Classify the repository. Use tier 3 unless promotion is explicit.
2. Inspect its tracked files, metadata, workflows, Dependabot configuration, and action pins.
3. Inspect its live GitHub settings, security features, and effective rulesets.
4. For npm packages, inspect the public package and confirm npm trusted-publisher settings when
   authorized. Public metadata alone cannot verify them.
5. Report compliant items, deviations, intentional exceptions, and proposed changes.

An unavailable API, setting, or permission is **not verified**, never compliant by assumption.

## Repository tiers

Tiers describe visibility and contribution posture, not engineering quality.

- **Tier 1 — promoted public product.** Listed in the organization README and has a dedicated
  landing page.
- **Tier 2 — supported shared component.** Listed in the organization README; a dedicated
  landing page is optional.
- **Tier 3 — maintained utility.** Discoverable through GitHub or its package registry and open
  to contributions, but not actively promoted in the organization README.

Tier 3 is the default. Record tier 1 and tier 2 promotions here when they happen.

| Repository | Tier |
| --- | --- |
| `neaps` | 1 |
| `slackwater-engine` | 2 |
| `noaa-current-stations` | 3 |
| `station-metadata` | 3 |

## Required files

Every repository tracks:

- `README.md` with its purpose, use, development, and release basics.
- `CONTRIBUTING.md` as the canonical project instructions for humans and coding agents alike: layout, build, checks, releases, and gotchas. See [docs/agents/agent-instructions.md](docs/agents/agent-instructions.md).
- `AGENTS.md` and `CLAUDE.md` as short pointers to `CONTRIBUTING.md`, so every agent harness finds it.
- `LICENSE` when the repository is public.

The organization `.github` repository may provide `SECURITY.md` or other default community files
when Open Waters has an actual policy to state. Do not add placeholder policies. Inherited files
do not replace the repository-specific files above.

## Repository metadata

Every repository has a concise description and useful topics.

- A tier 1 GitHub homepage points to its dedicated landing page.
- A tier 2 or tier 3 npm repository points its GitHub homepage to its npm package page unless a
  better landing page exists.
- A non-npm repository may leave the GitHub homepage empty unless it has a meaningful product or
  documentation page.
- An npm package's `package.json.homepage` points to `https://openwaters.io` by default, or to its
  dedicated product or documentation page. It does not duplicate the npm package URL.

## Repository settings

Use these defaults for every tier:

- Wikis off.
- Issues on.
- Projects off; enable them only when a larger project needs them.
- Suggest updating pull-request branches on.
- Auto-merge on.
- Automatically delete merged head branches on.
- Automatically close linked issues when a pull request merges on.
- All three merge methods allowed. Squash a branch whose commits are incremental steps toward one
  change; use a merge commit when the individual commit messages are history worth keeping.
- Squash commits use the pull-request title as the commit title.

## Branch and release-tag rulesets

The default branch:

- Requires a pull request.
- Requires the repository's CI check when one exists and requires the branch to be current.
- Blocks force-pushes and deletion.
- Requires one approving review for tiers 1 and 2.
- Requires zero approving reviews for tier 3, so a maintainer can merge a passing pull request
  without manufacturing another reviewer.
- Allows repository administrators to bypass the rules.

Release tags block updates and deletion while allowing new tags and repository-admin bypass.
Protect the pattern the repository actually releases:

- Single-package repositories such as `station-metadata`: `v*`.
- Independently versioned monorepos using Changesets, such as `neaps`: `*@*`.

## Dependencies and GitHub Actions

Repositories using GitHub Actions include `.github/dependabot.yml` with a monthly
`github-actions` check. npm repositories also check npm dependencies weekly. Enable Dependabot
vulnerability alerts and security updates. A repository may group version updates when separate
pull requests become noisy.

Pin third-party actions to a full commit SHA with a version comment:

```yaml
- uses: pnpm/action-setup@a7487c7e89a18df4991f7f222e4898a00d66ddda # v4.1.0
```

GitHub-maintained `actions/*` may use a major version tag (`actions/checkout@v5`). Dependabot owns
updates to both.

## npm packages and trusted publishing

Commit `package-lock.json`. Include these `package.json` fields:

- `description`
- `license`
- `repository`
- `bugs`
- `homepage`
- `keywords`
- An explicit `files` list
- `publishConfig.access: public`

CI uses `npm ci`, runs the package tests, and runs `npm pack --dry-run`.

Publish with npm trusted publishing through GitHub OIDC and provenance. Never store an
`NPM_TOKEN` or OTP in GitHub Actions. A simple publish workflow normally needs only:

```yaml
permissions:
  contents: read
  id-token: write
```

A Changesets workflow may also write contents and pull requests. New packages require one manual
first publish because npm cannot configure a trusted publisher before the package exists. Then
register the exact GitHub repository and workflow filename with npm.

A single package may publish from a protected GitHub Release. An independently versioned
monorepo may publish after its Changesets release pull request merges. No particular build
system, Node `engines` value, or release tool is required.

## Agent audit checklist

Report each item as compliant, a deviation, an intentional exception, or **not verified**:

- Repository tier and organization README visibility.
- Required local files.
- Description, topics, GitHub homepage, and npm homepage when applicable.
- Issues, projects, wikis, merge methods, auto-merge, branch updates, branch deletion, and linked
  issue closing.
- Effective default-branch and release-tag rulesets, including admin bypass.
- Dependabot schedules, vulnerability alerts, security updates, and third-party action pins.
- npm metadata, package lock, CI, package dry run, OIDC permissions, absence of npm credentials,
  and trusted-publisher registration.

Do not publish a package or create a release merely to test publishing.

## Exceptions

Variance is expected when a repository has a concrete need. Record the reason in the audit or
repository documentation. An exception does not silently redefine the baseline for other
repositories.

The organization profile lists `station-metadata` and `noaa-current-stations` as part of its
broader project directory. These are visibility exceptions: both retain their explicitly
recorded tier 3 status and zero required approvals.
