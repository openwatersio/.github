# npm releases

How Open Waters packages are named and published to npm.

## Scope policy

- **`@openwaters/*`** — general-purpose packages for the org (e.g. `@openwaters/seamap`, `@openwaters/seascape`). New packages default here.
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

Register the exact repository and workflow filename as a trusted publisher for the package on npmjs.com. A new package needs one manual first publish, because npm can't configure a trusted publisher before the package exists.

Every package sets `publishConfig.access: public` and commits `package-lock.json`. [REPOSITORY_STANDARDS.md](../../REPOSITORY_STANDARDS.md) lists the required `package.json` metadata fields and the CI checks packages run.

## Release flows in use

Pick the one that matches the repo's shape; all four exist in the org today.

### Changesets (multi-package monorepos)

Used by neaps. Every PR that changes published behavior includes a changeset (`npm run changeset`). A release workflow on push to `main` runs `changesets/action`, which opens or updates a "Version Packages" PR; merging that PR publishes to npm with `NPM_CONFIG_PROVENANCE: true`. Changelogs are generated with `@changesets/changelog-github`.

### Tag-driven (a package inside a larger repo)

Used by seamap for `@openwaters/seamap`. To release: bump `version` in the package's `package.json` per the repo's versioning policy, commit, then `git tag v<version> && git push origin main --tags`. The workflow verifies the tag matches the package version, runs the package's tests, publishes, and creates the GitHub release with generated notes.

### Release-driven with a tag prefix (several release tracks in one repo)

Used by ais for `signalk-aiscast`. Creating a GitHub release with a prefixed tag (`signalk-plugin-v1.2.3`) triggers a workflow that filters on the prefix, sets the package version from the tag, tests, and publishes. Other tags in the repo belong to other release tracks and are ignored.

### Date-stamped dispatch (data packages)

Used by tide-database. A manually dispatched workflow sets the version to `<major>.<minor>.<YYYYMMDD>`, publishes to npm, and attaches built artifacts to a GitHub release. Fits packages whose releases are data refreshes rather than code changes.

## Build on pack

Packages build via a `prepack` (or `prepublishOnly`) script so `npm publish` always ships a fresh build; `dist/` is not committed.
