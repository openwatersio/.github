# Swift toolchains

Use this guidance for Swift libraries, language ports and their consumer builds. Keep each repository’s supported platforms, compiler versions and exact test commands in its `CONTRIBUTING.md`.

## Choose the compiler

Record whether each CI job uses the runner’s Swift, Xcode’s toolchain or a mise installation. A successful runner-provided build does not verify that the local mise installer works. Node setup through `actions/setup-node` reads the Node pin only; it does not install Swift from the same file.

Choose local pins from the toolchains the repository validates. The [Swift tools version](https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html#about-the-swift-tools-version) in `Package.swift` is a package requirement; the development compiler pin is a separate choice. Keep application signing, Xcode selection and SDK requirements in the application repository.

On macOS, a standalone Swift compiler uses SDKs from the installed Xcode. Check compatibility with that SDK, including package-manifest compilation and the Apple targets consumers use. Linux tests cannot establish Apple SDK compatibility. A compiler older than the SDK can fail with errors such as an unknown `-target-arch-variant` argument or a missing `URL` type.

## Pin Swift with mise

When macOS and Linux use the same compiler version, declare it once. For example, the configuration validated with Swift 6.4.0 on Ubuntu 26.04 is:

```toml
min_version = "2026.9.11"

[tools]
swift = "6.4.0"
```

Each repository chooses the compiler version its supported platforms validate. Use platform-specific entries when the required versions differ, and verify installation with the declared minimum mise on each platform. Equal-version platform entries can conflict over one installation destination in older mise releases.

Swift installation on Ubuntu 26.04 requires mise 2026.9.11 or newer. That release [selects the distribution build from Swift’s release index](https://github.com/jdx/mise/releases/tag/v2026.9.11). Older mise can download an Ubuntu 24.04 archive on Ubuntu 26.04: `swift --version` works, while package tools fail with missing `libxml2.so.2`. The [official Swift release index](https://www.swift.org/api/v1/install/releases.json) identifies the archives available for each compiler, distribution and architecture.

This guidance uses mise’s [built-in Swift installer](https://mise.jdx.dev/lang/swift.html). Check `mise plugins ls` when installation behaves differently: an installed `swift` plugin takes precedence over the built-in backend. Document any required plugin in the repository.

Keep `min_version` and the contributor setup instructions in agreement. A repository that uses runner-provided Swift and has no local Swift pin can retain that setup; document how contributors select a compatible compiler.

## Validate an installation or runner change

Test both the installer and the repository’s Swift code. A compiler version check alone does not exercise SwiftPM or its shared-library dependencies.

- Start with empty mise data, download-cache and state directories. Disable CI cache restoration for that check, and verify the selected compiler resolves inside the isolated installation.
- Install through the repository’s declared minimum mise and committed Swift pin. Record the downloaded archive’s distribution and architecture, along with `mise --version`, `mise which swift` and `mise exec swift -- swift --version`.
- Run the repository’s full Swift suite using its documented mode and package path. Run parity, performance and consumer/platform checks required by that repository. Keep their tolerances and coverage requirements intact.
- Check warm-cache behavior separately. A cached compiler working on a new runner does not prove that a fresh installation works. A fresh native binary built on a newer Linux host may also need an OS-specific cache key if the same key can be restored on an older host.
- Record the exact tested commit, runner image, compiler and run links. Distinguish Linux installation, Apple builds and release/publication coverage. Preserve production gates; validation does not require a release or production write.

Use the native runner/compiler setup in ordinary CI unless the job needs mise-managed tools. Keep temporary validation workflows separate from lasting fixes. After a temporary runner-only candidate passes, restore its original workflow tree and close an empty PR without merging; retain the tested-commit evidence.

## Recover an incompatible installed archive

Updating mise does not replace a Swift installation that already occupies the requested version’s directory. On Ubuntu 26.04, Swift 6.4.0 installed through mise older than 2026.9.11 can contain the Ubuntu 24.04 archive and fail on `libxml2.so.2`.

For that affected installation, update mise to the repository’s required minimum, then run from the repository root:

```sh
mise uninstall swift@6.4.0
mise install swift
```

Run the repository’s Swift suite again. [Almanac’s validation evidence](https://github.com/openwatersio/almanac/pull/101) covers these commands with native Swift 6.4.0 on Ubuntu 26.04. The check exercises reinstall commands after a fresh installation; a full simulation of an older incompatible installation remains unverified. For another compiler or distribution, identify the selected archive and missing dependency before choosing a recovery step. Do not alias incompatible shared-library ABIs to hide a loader error.
