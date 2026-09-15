# npm releases

How Open Waters packages are named and published to npm.

## Scope policy

- **`@openwaters/*`** — general-purpose packages for the org (e.g. `@openwaters/seamap`, `@openwaters/seascape`). New packages default here. The GitHub org is `openwatersio`, but the npm scope is `@openwaters`; never create an `@openwatersio/*` package.
- **`@neaps/*`** — the tide ecosystem only (`@neaps/tide-predictor`, `@neaps/cli`, `@neaps/api`, `@neaps/react`, `@neaps/tide-database`). Don't add non-tide packages to this scope.
- **Unscoped** — For various reasons, an unscoped package may make more sense. Examples: `signalk-aiscast` (unwritten convention for many Signal K Plugins), `neaps` (meta package), `coordinate-format` (stand-alone utility).

## Trusted publishing

All packages publish from GitHub Actions via [npm trusted publishing](https://docs.npmjs.com/trusted-publishers) (OIDC) with provenance. No npm tokens in repo secrets. The workflow needs:

```yaml
permissions:
  contents: read
  id-token: write # npm trusted publishing + provenance

steps:
  - uses: actions/setup-node@v7
    with:
      node-version: "24" # any Node whose bundled npm is >= 11.5.1 (required for trusted publishing)
      registry-url: https://registry.npmjs.org
```

A workflow that creates a GitHub release or pushes tags needs `contents: write` instead of `contents: read`, and a changesets workflow also needs `pull-requests: write`.

If publishing needs a newer Node/npm version than test CI, document that release-only requirement in `CONTRIBUTING.md`. Local `mise.toml` versions follow the tested CI toolchain; document how to select the publishing versions when reproducing a release locally.

Register the exact repository and workflow filename as a trusted publisher for the package on npmjs.com. A new package needs one manual first publish, because npm can't configure a trusted publisher before the package exists:

1. Any member of the `@openwaters` npm org can create a package in the scope, so try the publish before asking an owner for access.
2. Stage every verification step first, then ask for a one-time password and run `npm publish --otp=<code>` right away. Codes expire in about 30 seconds.
3. Register the trusted publisher.
4. Don't cut a GitHub release or tag for the hand-published version: a publish workflow triggered by it runs and fails on a version that already exists. The next patch release is the first through OIDC, as with `@openwaters/chs-constituents` (0.3.0 by hand, 0.3.1 through OIDC with provenance).

Every package sets `publishConfig.access: public` and commits `package-lock.json`. [REPOSITORY_STANDARDS.md](../../REPOSITORY_STANDARDS.md) lists the required `package.json` metadata fields and the CI checks packages run.

Follow the shared [release preparation checklist](releases.md#release-preparation-checklist) before publishing.

## Release flows in use

Pick the one that matches the repo's shape; all four exist in the org today.

### Changesets (multi-package monorepos)

Used by neaps. Every PR that changes published behavior includes a changeset (`npm run changeset`). A release workflow on push to `main` runs `changesets/action`, which opens or updates a "Version Packages" PR; merging that PR publishes to npm with `NPM_CONFIG_PROVENANCE: true`. Changelogs are generated with `@changesets/changelog-github`.

### Tag-driven (a package inside a larger repo)

Used by seamap for `@openwaters/seamap`. To release: bump `version` in the package's `package.json` per the repo's versioning policy, commit, then `git tag v<version> && git push origin main --tags`. The workflow verifies the tag matches the package version, runs the package's tests, publishes, and creates the GitHub release with generated notes.

#### Almanac's agent-operated variant

Almanac uses a release agent for its shared npm and Swift version. A small model can run the mechanical path:

1. Follow the repository's `CONTRIBUTING.md`, choose the next version under its versioning policy, and open a release pull request that updates the committed version source.
2. Wait for required CI to pass, then merge the pull request through the default branch protections.
3. Fetch `origin/main`, verify that the merged version matches a new release tag, create the tag at that exact merge commit, and push only that tag.
4. Wait for the tag workflow to recheck the version, run release tests and consumer smoke tests, publish the tested npm artifact through OIDC with provenance, and create the GitHub release with generated notes.
5. Verify that npm and GitHub show the new version before reporting the release complete.

If CI or publishing fails, hand the release to a more capable model or a human. Never bypass checks, publish manually, or move or recreate a protected release tag.

### Release-driven with a tag prefix (several release tracks in one repo)

Used by ais for `signalk-aiscast`. Creating a GitHub release with a prefixed tag (`signalk-plugin-v1.2.3`) triggers a workflow that filters on the prefix, sets the package version from the tag, tests, and publishes. Other tags in the repo belong to other release tracks and are ignored.

### Date-stamped dispatch (data packages)

Used by tide-database. A manually dispatched workflow sets the version to `<major>.<minor>.<YYYYMMDD>`, publishes to npm, and attaches built artifacts to a GitHub release. Fits packages whose releases are data refreshes rather than code changes.

## Build on pack

Packages build via a `prepack` (or `prepublishOnly`) script so `npm publish` always ships a fresh build; `dist/` is not committed.
