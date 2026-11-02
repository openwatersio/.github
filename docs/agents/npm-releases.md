# npm releases

How Open Waters packages are named and published to npm.

## Scope policy

- **`@openwaters/*`** — general-purpose packages for the org (e.g. `@openwaters/seamap`, `@openwaters/seascape`). New packages default here. The GitHub org is `openwatersio`, but the npm scope is `@openwaters`; never create an `@openwatersio/*` package.
- **`@slackwater/*`** — the tide ecosystem (`@slackwater/engine`, `@slackwater/cli`, `@slackwater/api`, `@slackwater/react`, `@slackwater/database`). Existing `@neaps/*` names belong to the same ecosystem; renaming a published package needs an explicit migration.
- **Unscoped** — Use an unscoped name when the ecosystem or package calls for it: `signalk-aiscast` follows the Signal K plugin convention, `slackwater` is the umbrella package, and `coordinate-format` is a standalone utility.

## Trusted publishing

All packages publish from GitHub Actions via [npm trusted publishing](https://docs.npmjs.com/trusted-publishers) (OIDC) with provenance. No npm tokens in repo secrets. The workflow needs:

```yaml
permissions:
  contents: read
  id-token: write # npm trusted publishing + provenance

steps:
  - uses: actions/checkout@v7
  - uses: actions/setup-node@v7
    with:
      node-version-file: mise.toml
      registry-url: https://registry.npmjs.org
```

The committed mise configuration must select a Node version whose bundled npm is at least 11.5.1 for trusted publishing, such as Node 24. Use the actual configuration path when it differs from `mise.toml`, and follow the shared [Node toolchain guidance](../../REPOSITORY_STANDARDS.md#node-toolchains). setup-node reads the Node pin only; a separately pinned npm version needs its own installation step.

A workflow that creates a GitHub release or pushes tags needs `contents: write` instead of `contents: read`, and a changesets workflow also needs `pull-requests: write`.

If publishing needs a newer Node/npm version than test CI, document that release-only requirement in `CONTRIBUTING.md`. Keep a fixed release-only Node pin in a separate committed mise configuration and select it with `node-version-file`. Document how to select the publishing versions when reproducing a release locally.

Register the exact repository and workflow filename as a trusted publisher for the package on npmjs.com. A new package needs one manual first publish, because npm can't configure a trusted publisher before the package exists:

1. Any member of the `@openwaters` npm org can create a package in the scope, so try the publish before asking an owner for access.
2. Stage every verification step first, then ask for a one-time password and run `npm publish --otp=<code>` right away. Codes expire in about 30 seconds.
3. Register the trusted publisher.
4. Don't cut a GitHub release or tag for the hand-published version: a publish workflow triggered by it runs and fails on a version that already exists. The next patch release is the first through OIDC, as with `@openwaters/chs-constituents` (0.3.0 by hand, 0.3.1 through OIDC with provenance).

Every package sets `publishConfig.access: public` and commits `package-lock.json`. [REPOSITORY_STANDARDS.md](../../REPOSITORY_STANDARDS.md) lists the required `package.json` metadata fields and the CI checks packages run.

Follow the shared [release preparation checklist](releases.md#release-preparation-checklist) before publishing.

## Release systems

Packages use reviewed-version publishing or Changesets. Generated data releases have an explicit exception for the version source. The trigger alone does not define a release system: a tag push, a published GitHub Release, and a manual dispatch can all publish a version that was reviewed and committed first.

Every release follows these rules:

- Version changes land through a pull request under the repository's normal CI and review requirements. The generated-data exception below commits the version floor and generation rule instead of each released version.
- Publication uses an identified commit from the default branch. A release tag identifies that commit; a dispatch must select the default branch and retain the run's source SHA.
- A tag that names an npm version must match the committed package version before publishing, including any repository-specific prefix. Generated data releases check the derived version against the packed artifact instead.
- Release checks finish before publishing. Keep the package's tests, packaging checks, consumer smoke tests, and any compatibility checks against other release tracks.
- Publishing uses OIDC with provenance and never commits a version back to the default branch, moves a published tag, or deletes a published tag for a retry.
- Release automation uses the normal PR path and needs no default-branch or release-tag update bypass. The administrator recovery bypass in the [repository standards](../../REPOSITORY_STANDARDS.md#branch-and-release-tag-rulesets) is not part of a normal release.

### Reviewed-version publishing

Use this for a package whose version is chosen during release preparation, including a package inside a larger repository or a shared version across language ports.

1. Follow the repository's versioning policy. Open a PR with the package version, corresponding lockfile entries, changelog or release notes, and the shared release-preparation cleanup. The bump may be part of the change PR or a separate release PR.
2. Merge after required checks and reviews pass. Fetch the default branch and identify the merged commit carrying the intended version.
3. Use the repository's documented trigger for that commit. For a tag release, create a new matching tag at the identified commit and push only that tag. For a GitHub Release, publish from that tag. For a manual dispatch, select the default branch and confirm the run's SHA contains the reviewed version.
4. The workflow checks version agreement and runs the repository's release validation before publishing. It creates a GitHub Release when that release track needs one.
5. Verify the workflow result, the intended version on npm, and the GitHub Release and assets when applicable. Finish the title and notes using the [release notes guidance](releases.md#release-notes).

Existing variants share this preparation and publication order:

| Repository | Trigger and version source | Release-specific checks and outputs |
| --- | --- | --- |
| [aiscast](https://github.com/openwatersio/aiscast/blob/main/CONTRIBUTING.md#releases) | Push `signalk-plugin-v<version>` matching `signalk-plugin/package.json`. | Check the changelog entry, test, publish `signalk-aiscast`, and create the GitHub Release from those notes. The prefix keeps the plugin separate from service deployment. |
| [almanac](https://github.com/openwatersio/almanac/blob/main/CONTRIBUTING.md#releasing) | Push `v<version>` matching `typescript/package.json`, the shared version source. | Test the language ports and SwiftPM consumer, smoke-test the npm tarball, publish that tested artifact, and create the GitHub Release. |
| [seamap](https://github.com/openwatersio/seamap/blob/main/CONTRIBUTING.md#releases) | Push `v<version>` matching `style/package.json`. | Build sprites, test and publish `@openwaters/seamap`, and create the GitHub Release. Tile builds and deployment are separate tracks. |
| [seascape](https://github.com/openwatersio/seascape/blob/main/CONTRIBUTING.md#releases) | Publish a GitHub Release tagged `style-v<version>` matching `style/package.json`. | Verify main ancestry and compatibility with the live tile pipeline and schema, then test and publish `@openwaters/seascape`. Tile promotion has its own release path. |
| [maritime-zones](https://github.com/openwatersio/maritime-zones/blob/main/CONTRIBUTING.md#reader-changes-and-npm-releases) | Dispatch `publish.yml` on `main` after merging the npm version. | Check and publish the reader package. `version` and `tileVersion` are independent: a reader-only release needs no tile rebuild or new GitHub Release. Publish new tile assets before publishing a reader pinned to them. |

These examples describe publishing mechanisms, not an audit of repository settings. During release preparation, verify the live protections and follow this PR requirement even if a repository's local instructions still permit a direct push to `main`.

### Changesets publishing

Use this for independently versioned packages in a monorepo. [slackwater](https://github.com/openwatersio/slackwater/blob/main/CONTRIBUTING.md#package-publishing) uses this system:

1. Each PR that changes published behavior includes a changeset through `npm run changeset`. Its summary becomes release notes, so write it for package users. Include compatible dependent-package releases when an internal dependency change requires them.
2. On a push to `main`, `changesets/action` opens or updates the Version Packages PR. Its version command updates package versions, changelogs, and the lockfile.
3. Merge that PR under the same branch rules as any other PR. The release workflow publishes the committed versions through OIDC with provenance and creates package tags and GitHub Releases.
4. Verify the intended package versions and dist-tags on npm, then finish the release title and notes. A successful workflow that only updated the version PR does not mean packages were published.

Slackwater's `scripts/release.sh` publishes workspaces sequentially in dependency order, skips package versions already on npm, and selects the prerelease dist-tag from Changesets pre mode. Keep those behaviors when maintaining the workflow. Its SwiftPM `v*` tags are a separate track; npm package tags use `<package>@<version>`. Protect both namespaces.

### Generated data releases

[slackwater-database](https://github.com/openwatersio/slackwater-database/blob/main/CONTRIBUTING.md#releases) is an exception to committing the exact published version. `packages/database/package.json` commits a version floor, such as `1.0.0-beta.0`; `publish.yml` replaces the final numeric segment with the UTC date, such as `1.0.0-beta.20261102`. A stable floor derives `<major>.<minor>.<YYYYMMDD>`. The released version is written into the build workspace and is not committed back.

The committed floor and generation rule determine versioning. The GitHub Release tag and source commit, npm artifact version, and dated data assets identify what shipped. A repository using this exception documents those identities, the version-generation rule, its trigger, and its consumer checks in `CONTRIBUTING.md`.

Before dispatching Slackwater Database from `main`, follow its local release checklist: build the local tarball with the derived version, validate it in slackwater.xyz and slackwater-ios, and prepare the consumer updates. The workflow validates and builds the npm package and TCD artifacts, publishes the package, and creates the GitHub Release with `.tcd` and `.tcdb` assets. Prereleases publish under `beta`.

The date rule permits one version per UTC day. A correction after publication needs a new version; the same dated version cannot be overwritten. Code packages do not inherit this exception merely because a release workflow can set a version from a tag.

## Repository release instructions

Each repository's `CONTRIBUTING.md` records:

- The release system, version source and package path, including how the lockfile is updated.
- The trigger, tag prefix or namespaces, and how the source commit is selected from the default branch.
- Required tests, packaging and consumer checks, release-only toolchains, and dependencies on other release tracks.
- npm dist-tags, output artifacts, release notes source, and how to verify publication.
- Any generated-version exception and its reason.

Audit the workflow against those instructions and the [branch and tag rules](../../REPOSITORY_STANDARDS.md#branch-and-release-tag-rulesets). Flag post-publish version commits, direct default-branch pushes, tag relocation or deletion, missing tag/version checks, and release automation bypasses as deviations. A working workflow does not prove that protections are configured. Resolve conflicting workflows before enabling protections; do not add a general Actions bypass to keep a write-back release working.

## Release agents and recovery

An agent follows the repository's checklist: prepare the version PR or changesets, wait for required review and CI, select the merged source commit, use the documented trigger, and verify publication. A small model can run the mechanical steps; failed checks, unexpected versions, or partial publication need a more capable model or a human.

After a failed run, inspect what reached npm and GitHub before retrying. npm publication can succeed before GitHub Release creation or another package fails. Retry only the unfinished work using the repository's documented recovery path; never overwrite a published version, move or recreate a published tag, bypass checks, or switch to manual publication. The manual first publish described above is the package-bootstrap exception. Allow for registry propagation before treating an immediate old-version response as a failed publish.

## Build on pack

Packages build via a `prepack` or `prepublishOnly` script; `dist/` is not committed. When the release workflow tests a packed tarball, publish that same tarball instead of rebuilding a different artifact. A workflow using `--ignore-scripts` must build and validate the artifact before publication.
