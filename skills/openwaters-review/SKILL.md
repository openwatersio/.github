---
name: openwaters-review
description: Open Waters local code review before and during a pull request. Runs independent reviewers (Codex, Copilot, Claude) in parallel with a shared prompt, then verifies and fixes findings. Later rounds check only the fixes, for at most three rounds. Use before a branch is first pushed as a PR, and whenever later commits change behavior, data, or interfaces.
---

# Code review

Run the local review before a branch is first pushed as a PR, and again without asking whenever later commits change behavior, data, or interfaces. Skip it for changes that can't affect behavior, such as docs, comments, formatting, or a merge with no conflicts in code. Prompts and skill text that agents follow are behavior, not docs.

## Before writing code

Map the system before writing code, not during review: every other writer and reader of the data, files, caches, and APIs the change will touch; all the data those paths can produce; the upgrade from what is deployed; and what the tests and validation data will leave out. Design the change against that map. The review checks the map; it is not where the change's reach gets discovered.

## Running a round

Start the review when the change is complete. One that grows between rounds never reviews clean.

Run the [`review-branch`](review-branch) script that sits in this skill's directory, with the branch's worktree as the current directory. It reviews the working tree, committed or not, so a round never needs a commit. Independent, read-only reviewers run in parallel with [review-prompt.md](review-prompt.md). It prints the report directory, then each reviewer's report path, or `FAILED` with the path to that reviewer's log.

- The first round runs `review-branch`: Codex, Copilot, Claude Opus and Claude Sonnet review the whole change against the merge base.
- A later round runs `review-branch --after=<report directory of the round before>`: Opus and Sonnet review only what changed since that round. First write `findings.md` in that directory, one line per finding: its file:line and claim, then fixed, dismissed with the reason, or left open. Reviewers repeat a listed finding only when they can show its fix or reason is wrong.
- Pass a base branch when it is not `origin/main`. Run a round in the background; it takes minutes.
- Do not edit the worktree while a round runs. The reviewers read the live files.

Read every report in full. A reviewer that failed or skipped its step 1 map has not reviewed the change. Run the round again only when fewer than two reviewers completed.

Do not write your own review prompt. Change [review-prompt.md](review-prompt.md) instead, so every reviewer gets the same one.

## Acting on findings

- Check each finding against the code or data before fixing or dismissing it. Fix the real ones, look for the same class of bug elsewhere, and add a test that fails without the fix.
- Keep each fix as small as its finding. One that adds a mechanism (a thread, a timeout, a cache, a retry) is a design change: map it first.
- Rate each finding yourself; the reviewer's severity is a claim. Run another round only when a fix for a high or medium finding changed behavior. Low findings, and fixes to comments, docs, or tests, do not trigger one: fix them when cheap and list the rest in the PR's `Review` section. `--after` refuses a fourth round, and a round after the merge base moved. If the third still finds high or medium issues, bring them to the user, with the change as a draft pull request at most: the change is too large or was not mapped well enough.
- Commit once the review is clean, and keep review history out of commit messages. Report to the user what each reviewer found, what you fixed, and what you dismissed with the reason.
- When a reviewer on the pull request (such as GitHub Copilot) finds something the local reviews missed, record the check so the miss does not repeat:
  - If it depends on this project's data, stack, or domain, add it to the `Review checks` section of the repository's CONTRIBUTING.md, which every local reviewer reads.
  - If it would apply to any project, find the class in [review-prompt.md](review-prompt.md) it belongs to and sharpen that class's wording or examples. Add a new class only when the miss fits none of them. Keep the prompt general: each class names a kind of defect, not one project's case.

## Reporting review in the PR

Every PR description must include a `Review` section. Keep it current when creating or updating the PR, with:

- Completed round counts and the reviewers/models in each round. List skipped or failed attempts separately; they are not completed reviews.
- Main findings by reviewer or round, what was fixed, what was dismissed and why, and any unresolved findings.
- Review limits, such as static-only inspection or restricted tool access, and verification run after fixes.
- When a change affects which tests run, compare the job summary or test artifact with the suite the job is meant to cover. Report executed and skipped counts, and name missing cases when the change targets specific tests. Treat unexplained gaps as unresolved findings. Follow affected jobs through completion and update the PR with their results. Identify any suite left unverified by a failed or cancelled job.
- Changes made after the last model review, their verification, and whether another model review ran.

If no review completed, say so and explain why. Summarize the extent of review actually performed rather than implying unperformed checks or approval.
