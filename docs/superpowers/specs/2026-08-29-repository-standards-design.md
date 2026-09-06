# Open Waters Repository Standards Design

## Purpose

Keep Open Waters repositories consistent enough to create and audit confidently without
forcing unlike projects through an enforcement script. The organization `.github` repository
will hold one human-readable standard that an agent can apply with judgment.

## Approach

Add one `REPOSITORY_STANDARDS.md` to the organization `.github` repository. It will define the
tiers, baseline files and GitHub settings, npm and release requirements, permitted exceptions,
and an audit checklist. It is advisory: an audit reports differences, and changes are made only
when requested.

Do not add a synchronization script, repository template, or scheduled enforcement. Those would
duplicate the policy and make legitimate repository variance harder to maintain.

## Repository tiers

Tiers describe visibility and contribution posture, not engineering quality. Tier 3 is the
default; promotion to tier 1 or 2 is deliberate and recorded in the standards document.

- **Tier 1 — promoted public product.** Listed in the organization README and has a dedicated
  landing page.
- **Tier 2 — supported shared component.** Listed in the organization README; a dedicated
  landing page is optional.
- **Tier 3 — maintained utility.** Discoverable through GitHub or its package registry and open
  to contributions, but not actively promoted in the organization README.

`station-metadata` is tier 3.

## Required repository files

Every repository tracks these files locally:

- `README.md`, covering purpose, use, development, and release basics.
- `CONTRIBUTING.md`, containing repository-specific contribution and validation steps.
- `AGENTS.md`, the canonical repository instructions for coding agents.
- `CLAUDE.md`, a short compatibility pointer to `AGENTS.md`.
- `LICENSE` for every public repository.

The organization `.github` repository may later provide `SECURITY.md` or other default community
files when Open Waters has an actual policy to state. Until then it will not add placeholder
community files. Inherited defaults do not satisfy the local-file requirements above.

## Repository metadata

Every repository has a concise description and useful topics.

- Tier 1 GitHub homepages point to the dedicated landing page.
- Tier 2 and 3 npm repositories point their GitHub homepage to the npm package page unless a
  better landing page exists.
- Non-npm repositories may leave the GitHub homepage empty unless they have a meaningful product
  or documentation page.
- An npm package's `package.json.homepage` points to `https://openwaters.io` by default, or to its
  dedicated product or documentation page. It does not duplicate the npm package URL.

## Repository settings

The default settings for all tiers are:

- Wikis off.
- Issues on.
- Projects off, enabled only when a larger project needs them.
- Suggest updating pull-request branches on.
- Auto-merge on.
- Automatically delete merged head branches on.
- Automatically close linked issues when a pull request merges on.
- Squash and rebase merges allowed; merge commits disabled.
- Squash commits use the pull-request title as the commit title.

## Branch and tag rulesets

The default branch requires a pull request, blocks force-pushes and deletion, and requires the
repository's CI check when one exists. Tier 1 and 2 repositories require one approving review.
Tier 3 repositories require no approval, allowing a maintainer to merge a passing pull request
without manufacturing a second reviewer. Repository administrators may bypass the ruleset.

Release tags cannot be updated or deleted. New tags remain allowed so release automation can
create them, and repository administrators may bypass the ruleset for recovery. Protect the tag
pattern the repository actually uses:

- Single-package repositories such as `station-metadata`: `v*`.
- Independently versioned monorepos using Changesets, such as `neaps`: `*@*`.

## Dependency and workflow security

Each repository using GitHub Actions has a `.github/dependabot.yml` check for Actions updates
monthly. Each npm repository additionally checks npm dependencies weekly. Dependabot
vulnerability alerts and security updates are enabled. Repositories may group version updates
when individual pull-request volume becomes noisy.

Every third-party action is pinned to a full commit SHA with a version comment. Dependabot owns
updates to those pins.

## npm packages and publishing

An npm package commits `package-lock.json`. Its `package.json` includes a description, license,
repository, bugs URL, homepage, keywords, an explicit `files` list, and
`publishConfig.access: public`.

CI installs with `npm ci`, runs the package's tests, and runs `npm pack --dry-run`. Publishing
uses npm trusted publishing through GitHub OIDC with provenance and never stores an `NPM_TOKEN`
or OTP in Actions. A simple workflow normally needs only `contents: read` and `id-token: write`;
a Changesets workflow may also write contents and pull requests.

A new package receives one manual first publish because npm cannot configure a trusted publisher
before the package exists. Afterward, npm records the exact repository and workflow filename as
its trusted publisher.

Single-package repositories may publish from a protected GitHub Release. Independently versioned
monorepos may use a Changesets release pull request and publish after it merges. No particular
build system, Node `engines` value, or release tool is otherwise required.

## Agent audit flow

An agent auditing or creating a repository will:

1. Read `REPOSITORY_STANDARDS.md` and determine the tier; use tier 3 unless promotion is explicit.
2. Inspect tracked files, package metadata, workflows, Dependabot configuration, and action pins.
3. Inspect live GitHub metadata, settings, security features, and effective rulesets.
4. For npm packages, inspect the public package and ask for confirmation of npm's trusted
   publisher when it cannot be verified through public metadata.
5. Report compliant items, deviations, intentional exceptions, and proposed changes. Do not
   mutate settings or files unless requested.

An unavailable API or permission is reported as **not verified**, never as compliant. Repository
variance is acceptable when its reason is recorded; exceptions do not silently redefine the
baseline.

## Pilot: station-metadata

The pilot will make only these changes:

- Disable GitHub Projects.
- Enable pull-request branch update suggestions and automatic closing of linked issues.
- Disable merge commits while retaining squash and rebase merges.
- Update the `main` ruleset to require a pull request and the `test` check, require zero approvals
  for tier 3, and permit repository-admin bypass.
- Keep `v*` tags immutable while permitting repository-admin bypass.
- Change the Dependabot Actions schedule from weekly to monthly.
- Change `package.json.homepage` from the repository README to `https://openwaters.io`.

Its GitHub homepage already points to the npm package. Existing required files, metadata, OIDC
publishing, action SHA pins, weekly npm updates, and branch cleanup remain unchanged.

## Verification

Review the standards document as rendered Markdown. Audit `station-metadata` before and after the
pilot using tracked files plus GitHub API reads. Run its existing test suite after file changes.
Confirm the effective rulesets, repository settings, action pins, Dependabot schedules, npm
package contents, and absence of npm credentials.
