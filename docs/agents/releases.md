# Releases

This checklist applies to every Open Waters release, including Swift packages, apps, npm packages, and data artifacts. Run it during release preparation whether the release starts with a PR, a Git tag, a GitHub release, a manual dispatch, or another publishing mechanism.

## Release preparation checklist

Follow the [spec and plan cleanup convention](agent-instructions.md#retire-completed-specs-and-plans) before cutting any release:

- [ ] Review specs and plans from this release cycle and any carried forward from earlier releases.
- [ ] Preserve lasting guidance in maintained docs and user-facing changes in the changelog or release notes.
- [ ] Delete completed, merged specs and plans; keep unfinished plans and update temporary roadmaps to show remaining work.
- [ ] Have a human review the documentation updates and deletions in the release PR. If there is no release PR, merge a separate cleanup PR before creating the release tag or triggering publication.

Each repository's `CONTRIBUTING.md` release checklist includes these steps alongside its build, validation, and publishing commands. Package-specific instructions, such as [npm publishing](npm-releases.md), supplement this checklist.
