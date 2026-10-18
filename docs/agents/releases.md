# Releases

This checklist applies to every Open Waters release, including Swift packages, apps, npm packages, and data artifacts. Run it during release preparation whether the release starts with a PR, a Git tag, a GitHub release, a manual dispatch, or another publishing mechanism.

## Release preparation checklist

Follow the [spec and plan cleanup convention](agent-instructions.md#retire-completed-specs-and-plans) before cutting any release:

- [ ] Review specs and plans from this release cycle and any carried forward from earlier releases.
- [ ] Preserve lasting guidance in maintained docs and user-facing changes in the changelog or release notes.
- [ ] Delete completed, merged specs and plans; keep unfinished plans and update temporary roadmaps to show remaining work.
- [ ] Have a human review the documentation updates and deletions in the release PR. If there is no release PR, merge a separate cleanup PR before creating the release tag or triggering publication.
- [ ] Title the release and write its notes as described in [Release notes](#release-notes).

Each repository's `CONTRIBUTING.md` release checklist includes these steps alongside its build, validation, and publishing commands. Package-specific instructions, such as [npm publishing](npm-releases.md), supplement this checklist.

## Release notes

Stable GitHub releases appear on [openwaters.io/updates](https://openwaters.io/updates/), each project's updates page, and their RSS feeds. Most readers use the project, not its code, so write titles and notes for them.

### Title

The release title is a headline that says what changed. The tag already carries the version, and the updates page shows the package and version under the headline, so leave the version out of the title.

- Name the feature and what it does now, in the words the project's users use. "Names, call signs, and dimensions on chartplotters" tells a sailor what to look for; "Improve static data relay" doesn't.
- Write sentence case with no closing period, short enough to scan in a list.
- Give patch releases a headline too: "Connects over Starlink, satellite, and slow cellular links".
- Put a new requirement in the headline: "Requires Swift 6", or "Soundings placed at the transducer; requires Node 24".
- Avoid titles that could fit any release, such as "Bug fixes and improvements" or "Various updates", and avoid narrating a story about the bug. Say what works now.

A title that is only a version, such as `v0.8.0` or `signalk-aiscast 0.6.3`, shows as the package and version on the updates page.

### Notes

- Open with a sentence or two on what is new and who it is for.
- Put breaking changes and upgrade steps first.
- List the changes people will notice, one per bullet, each linking its pull request.
- Leave out chores, CI and test changes, refactors, bot dependency bumps, and commit hashes. Keep a dependency update when it matters to users, whoever opened its pull request: a new minimum Node, Swift, or OS version, a security fix, or a dependency they configure themselves. Rewrite a bot's pull request title into what changes for users, such as "Requires Node 24".
- Use the product's names: Open Waters AIS for the service, `aiscast` only for the software. Write app notes for the people using the app, and library notes for developers.
- Screenshots belong in the notes. The updates page copies images hosted on GitHub into the site.
- Mark betas, release candidates, and nightlies as prereleases. The updates page shows only stable releases, and leaves out a release whose notes hold nothing but chores and bot bumps.

### By release flow

- **Written by hand** (the release form, or a notes file the workflow reads): write the title and notes as above before publishing.
- **Generated notes:** add a [`.github/release.yml`](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes) that excludes bot authors and groups pull requests by label. Then edit the draft before publishing: replace the title, add the opening summary, and drop entries nobody using the project would notice.
- **Changesets:** each changeset summary becomes a line in the notes, so write it for users. After the release workflow publishes, title the umbrella package's release: `gh release edit <package>@<version> --title "<headline>"`.
- **Created by a workflow:** pass the headline as the release title instead of the tag, from a workflow input or the first line of the notes file.

Retitling a published release is safe: Open Waters release workflows run when a release is created or published, not when it is edited. The updates page picks up the new title on its next rebuild.
