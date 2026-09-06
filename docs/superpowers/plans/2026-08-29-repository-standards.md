# Shared Repository Standards Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish an advisory Open Waters repository standard and bring `station-metadata` into compliance as the tier 3 pilot.

**Architecture:** Keep the policy in one Markdown file in `openwatersio/.github`; do not create a sync script or template repository. Apply the pilot's tracked-file changes in `openwatersio/station-metadata`, then update and verify its live GitHub settings and repository-level rulesets explicitly.

**Tech Stack:** Markdown, JSON, YAML, npm, GitHub Actions, Dependabot, GitHub REST API and repository settings UI

**Spec:** `docs/superpowers/specs/2026-08-29-repository-standards-design.md`

## Global Constraints

- The standard is advisory: audits report differences and agents mutate nothing unless requested.
- Tier 3 is the default; `station-metadata` is tier 3.
- Do not add a sync script, template repository, scheduled enforcement, default community-policy files, dependency, or new release tool.
- Every third-party GitHub Action must be pinned to a full commit SHA with a version comment.
- npm publishing uses GitHub OIDC with provenance and no `NPM_TOKEN` or workflow OTP.
- GitHub repository homepages and `package.json.homepage` are distinct: the former may point to npm; the latter defaults to `https://openwaters.io`.
- Run every shell command through `rtk` as required by the workspace `AGENTS.md`.

---

## File map

### `openwatersio/.github`

- Create `REPOSITORY_STANDARDS.md`: the single agent-readable convention and audit checklist.
- Keep `profile/README.md` unchanged: it remains the organization profile, not the policy store.

### `openwatersio/station-metadata`

- Modify `.github/dependabot.yml`: monthly GitHub Actions checks and weekly npm checks.
- Modify `package.json`: set the package homepage to the Open Waters apex.
- Keep `.github/workflows/ci.yml` and `.github/workflows/publish.yml` unchanged: they already meet the pilot requirements.
- Update live repository settings and the existing `Protect main` and `Protect release tags` rulesets; do not add configuration scripts to the repository.

---

### Task 1: Publish the advisory convention

**Repository:** `/Users/clarkbw/src/openwaters/.github`

**Files:**
- Create: `REPOSITORY_STANDARDS.md`
- Reference: `docs/superpowers/specs/2026-08-29-repository-standards-design.md`

**Interfaces:**
- Consumes: the approved design specification.
- Produces: one standalone policy that an agent can use to classify, create, or audit a repository without reading the design history.

- [ ] **Step 1: Create the policy document**

Create `REPOSITORY_STANDARDS.md` with these sections and exact decisions from the spec:

```markdown
# Open Waters Repository Standards

## How to use this document
## Repository tiers
## Required files
## Repository metadata
## Repository settings
## Branch and release-tag rulesets
## Dependencies and GitHub Actions
## npm packages and trusted publishing
## Agent audit checklist
## Exceptions
```

The document must be operational, not a link back to the spec. Include the tier 1–3 definitions,
all required files, separate GitHub/npm homepage rules, exact settings defaults, tier-specific
approval counts, `v*` and `*@*` release-tag examples, Dependabot schedules, SHA pinning, npm OIDC
requirements, and the five-step agent audit flow. State that an unavailable API or permission is
reported as **not verified**.

- [ ] **Step 2: Check the policy against the approved design**

Run:

```bash
rtk rg -n 'Tier 1|Tier 2|Tier 3|README.md|CONTRIBUTING.md|AGENTS.md|CLAUDE.md|LICENSE|monthly|weekly|OIDC|NPM_TOKEN|not verified|v\*|\*@\*' REPOSITORY_STANDARDS.md
rtk git diff --check
```

Expected: every listed policy term has a matching line and `git diff --check` exits 0.

- [ ] **Step 3: Review the rendered structure**

Run:

```bash
rtk read REPOSITORY_STANDARDS.md
```

Expected: the document stands alone, distinguishes advisory defaults from exceptions, and contains no enforcement-script instructions.

- [ ] **Step 4: Commit the convention**

```bash
rtk git add REPOSITORY_STANDARDS.md
rtk git commit -m "Document shared repository standards"
```

---

### Task 2: Update the station-metadata tracked configuration

**Repository:** `/Users/clarkbw/src/openwaters/station-metadata`

**Files:**
- Modify: `.github/dependabot.yml`
- Modify: `package.json`

**Interfaces:**
- Consumes: the npm and dependency schedules in `openwatersio/.github/REPOSITORY_STANDARDS.md`.
- Produces: a weekly npm update schedule, monthly Actions update schedule, and npm package metadata pointing to the Open Waters apex.

- [ ] **Step 1: Verify the current differences**

Run:

```bash
rtk read .github/dependabot.yml
rtk rg -n '"homepage"' package.json
```

Expected: npm and GitHub Actions are both weekly, and `package.json.homepage` is `https://github.com/openwatersio/station-metadata#readme`.

- [ ] **Step 2: Make the minimal file edits**

Change only the GitHub Actions interval and package homepage:

```yaml
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: monthly
```

```json
"homepage": "https://openwaters.io"
```

Keep npm's schedule `weekly` and preserve all other keys and ordering.

- [ ] **Step 3: Run the repository checks**

Run:

```bash
rtk npm test
rtk npm pack --dry-run
rtk git diff --check
```

Expected: the test command exits 0, the dry run lists the intended package contents without publishing, and the diff check exits 0.

- [ ] **Step 4: Inspect the exact diff**

Run:

```bash
rtk git diff -- .github/dependabot.yml package.json
```

Expected: exactly two value changes—`weekly` to `monthly` for Actions and the homepage URL.

- [ ] **Step 5: Commit the tracked changes**

```bash
rtk git add .github/dependabot.yml package.json
rtk git commit -m "Align repository metadata and dependency checks"
```

---

### Task 3: Align station-metadata repository settings

**Repository:** `openwatersio/station-metadata` on GitHub

**Files:** None. These are live GitHub settings.

**Interfaces:**
- Consumes: repository-settings defaults from `REPOSITORY_STANDARDS.md`.
- Produces: the tier-independent repository settings for the pilot.

- [ ] **Step 1: Capture the current API-visible settings**

Run:

```bash
rtk gh api repos/openwatersio/station-metadata --jq '{has_issues,has_projects,has_wiki,homepage,allow_squash_merge,allow_merge_commit,allow_rebase_merge,allow_auto_merge,delete_branch_on_merge,allow_update_branch,squash_merge_commit_title}'
```

Expected before the update: projects are enabled, update-branch suggestions are disabled, and merge commits are enabled. Preserve the npm package URL already stored in GitHub's `homepage` field.

- [ ] **Step 2: Apply the API-visible settings**

Run:

```bash
rtk gh api --method PATCH repos/openwatersio/station-metadata \
  -F has_issues=true \
  -F has_projects=false \
  -F has_wiki=false \
  -F allow_squash_merge=true \
  -F allow_merge_commit=false \
  -F allow_rebase_merge=true \
  -F allow_auto_merge=true \
  -F delete_branch_on_merge=true \
  -F allow_update_branch=true \
  -f squash_merge_commit_title=PR_TITLE
```

Expected: HTTP 200 and a repository object containing the new values.

- [ ] **Step 3: Enable automatic closing of linked issues**

Open `https://github.com/openwatersio/station-metadata/settings` in the authenticated browser.
Under the pull-request merge settings, enable **Automatically close linked issues when pull
requests are merged**. GitHub's public repository REST response does not currently expose this
setting reliably, so do not claim API verification for it.

- [ ] **Step 4: Verify repository settings**

Repeat the API query from Step 1 and inspect the auto-close checkbox in the repository settings UI.

Expected: issues on; projects and wikis off; squash and rebase on; merge commits off; auto-merge,
branch deletion, and update suggestions on; squash title `PR_TITLE`; GitHub homepage unchanged;
auto-close checkbox on.

---

### Task 4: Align station-metadata branch and release-tag rulesets

**Repository:** `openwatersio/station-metadata` on GitHub

**Files:** None. These are live GitHub rulesets.

**Interfaces:**
- Consumes: tier 3 branch protection and single-package release-tag rules from `REPOSITORY_STANDARDS.md`.
- Produces: effective `main` and `v*` rulesets with organization-admin bypass.

- [ ] **Step 1: Resolve current ruleset IDs and save a read-only snapshot**

Run:

```bash
rtk gh api repos/openwatersio/station-metadata/rulesets --jq '.[] | [.id,.name,.target,.enforcement] | @tsv'
rtk gh api repos/openwatersio/station-metadata/rulesets/21806159
rtk gh api repos/openwatersio/station-metadata/rulesets/21806162
```

Expected: `21806159` is `Protect main`; `21806162` is `Protect release tags`. If IDs differ, use the IDs returned by the first command and do not create duplicate rulesets.

- [ ] **Step 2: Update Protect main**

Save this complete body as `/private/tmp/station-metadata-protect-main.json` using `apply_patch`:

```json
{
  "name": "Protect main",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [
    {"actor_id": null, "actor_type": "OrganizationAdmin", "bypass_mode": "always"}
  ],
  "conditions": {
    "ref_name": {"exclude": [], "include": ["~DEFAULT_BRANCH"]}
  },
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": true,
        "required_reviewers": [],
        "require_code_owner_review": false,
        "dismissal_restriction": {"enabled": false, "allowed_actors": []},
        "require_last_push_approval": false,
        "required_review_thread_resolution": true,
        "require_extra_approval_for_unattributed_changes": false,
        "allowed_merge_methods": ["squash", "rebase"]
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "do_not_enforce_on_create": true,
        "required_status_checks": [{"context": "test"}]
      }
    }
  ]
}
```

Then run:

```bash
rtk gh api --method PUT repos/openwatersio/station-metadata/rulesets/21806159 --input /private/tmp/station-metadata-protect-main.json
```

Expected: HTTP 200. If Step 1 returned a different ID for `Protect main`, substitute that observed
numeric ID. Do not create a duplicate ruleset or remove the `test` check, review-thread
resolution, deletion rule, or force-push protection.

- [ ] **Step 3: Update Protect release tags**

Save this complete body as `/private/tmp/station-metadata-protect-release-tags.json` using `apply_patch`:

```json
{
  "name": "Protect release tags",
  "target": "tag",
  "enforcement": "active",
  "bypass_actors": [
    {"actor_id": null, "actor_type": "OrganizationAdmin", "bypass_mode": "always"}
  ],
  "conditions": {
    "ref_name": {"exclude": [], "include": ["refs/tags/v*"]}
  },
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"}
  ]
}
```

Keep tag creation unrestricted so `.github/workflows/publish.yml` can continue publishing from newly created GitHub Releases.

Run:

```bash
rtk gh api --method PUT repos/openwatersio/station-metadata/rulesets/21806162 --input /private/tmp/station-metadata-protect-release-tags.json
```

Expected: HTTP 200. If Step 1 returned a different ID for `Protect release tags`, substitute that
observed numeric ID. Do not create a duplicate ruleset.

- [ ] **Step 4: Verify both effective rulesets**

Run:

```bash
rtk gh api repos/openwatersio/station-metadata/rulesets/21806159
rtk gh api repos/openwatersio/station-metadata/rulesets/21806162
```

Expected: both are active and contain organization-admin `always` bypass; `main` targets the default branch, allows only squash/rebase, requires zero approvals and `test`; tags target `refs/tags/v*` and block deletion and non-fast-forward updates.

---

### Task 5: Verify security features and complete the pilot audit

**Repositories:** `/Users/clarkbw/src/openwaters/.github`, `/Users/clarkbw/src/openwaters/station-metadata`, and `openwatersio/station-metadata` on GitHub

**Files:** None unless verification reveals an approved task was not applied correctly.

**Interfaces:**
- Consumes: every deliverable from Tasks 1–4.
- Produces: an evidence-backed compliance report with unobservable npm trusted-publisher state marked **not verified** unless checked by an authorized user.

- [ ] **Step 1: Verify Dependabot security features**

Run:

```bash
rtk gh api repos/openwatersio/station-metadata/vulnerability-alerts --silent
rtk gh api repos/openwatersio/station-metadata/automated-security-fixes
```

Expected: the vulnerability-alert endpoint returns HTTP 204 and automated security fixes report `enabled: true`. If either is disabled, enable it through the corresponding GitHub REST endpoint, then repeat the read.

- [ ] **Step 2: Verify tracked policy and package changes**

Run in `/Users/clarkbw/src/openwaters/.github`:

```bash
rtk git status --short
rtk rg -n 'Tier 3|monthly|weekly|OIDC|not verified' REPOSITORY_STANDARDS.md
```

Run in `/Users/clarkbw/src/openwaters/station-metadata`:

```bash
rtk git status --short
rtk git ls-files README.md CONTRIBUTING.md AGENTS.md CLAUDE.md LICENSE package-lock.json
rtk rg -n 'interval: (weekly|monthly)' .github/dependabot.yml
rtk rg -n '"homepage": "https://openwaters.io"' package.json
rtk rg -n '"(description|license|repository|bugs|homepage|keywords|files|publishConfig)"' package.json
rtk rg -n 'uses: [^ ]+@[0-9a-f]{40} # v' .github/workflows
rtk rg -n 'id-token: write|contents: read|npm ci|npm test|npm pack --dry-run|npm publish' .github/workflows
rtk rg -n 'NPM_TOKEN|--otp' .github/workflows
rtk npm test
rtk npm pack --dry-run
```

Expected: both worktrees are clean after their task commits; npm is weekly; Actions is monthly;
the package homepage is the apex; every `uses:` line matches a 40-character SHA and version
comment; the credential search has no matches; tests and package dry run exit 0.

- [ ] **Step 3: Verify live metadata and rulesets**

Run:

```bash
rtk gh repo view openwatersio/station-metadata --json homepageUrl,hasIssuesEnabled,hasProjectsEnabled,hasWikiEnabled,deleteBranchOnMerge,mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed
rtk gh api repos/openwatersio/station-metadata --jq '{allow_auto_merge,allow_update_branch,squash_merge_commit_title}'
rtk gh api repos/openwatersio/station-metadata/rulesets --jq '.[] | {id,name,target,enforcement}'
```

Expected: GitHub homepage remains `https://www.npmjs.com/package/@openwaters/station-metadata`; issues on; projects and wikis off; branch deletion, auto-merge, and update suggestions on; merge commits off; squash and rebase on; squash title `PR_TITLE`; both rulesets active.

- [ ] **Step 4: Report the audit**

Report four short groups: compliant items, changes made, intentional tier-3 choices, and anything
not verified. Specifically mark npm's trusted-publisher registration **not verified** unless its
package settings were inspected by an authorized user. Do not publish a package or create a test
release merely to verify OIDC.
