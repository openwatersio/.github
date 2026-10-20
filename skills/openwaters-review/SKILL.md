---
name: openwaters-review
description: Open Waters local code review before and during a pull request. Runs independent reviewers (Codex, Copilot, Claude) in parallel with a shared prompt, then verifies and fixes findings round by round, for at most three rounds. Use before a branch is first pushed as a PR, and whenever later commits change behavior, data, or interfaces.
---

# Code review

Run the local review before a branch is first pushed as a PR, and decide for yourself when later changes need another one: run it without asking whenever new commits change behavior, data, or interfaces (new features, fixes, refactors, schema or format changes), whether they go on a new PR or an existing one. Skip it for changes that can't affect behavior, such as docs, comments, formatting, or a merge with no conflicts in code. Prompts and skill text that agents follow are behavior, not docs.

## Before writing code

Map the system before writing code, not during review: every other writer and reader of the data, files, caches, and APIs the change will touch; all the data those paths can produce; the upgrade from what is deployed; and what the tests and validation data will leave out. Design the change against that map. The review checks the map; it is not where the change's reach gets discovered.

## Running a round

Run the [`review-branch`](review-branch) script that sits in this skill's directory, with the branch's worktree as the current directory. It reviews the working tree against the merge base, committed or not, so a review round never needs a commit. It runs independent, read-only reviewers in parallel with [review-prompt.md](review-prompt.md). It prints the report directory first, then each reviewer's report path, or `FAILED` with the path to that reviewer's log.

- The first round runs `review-branch`: Codex, Copilot, Claude Opus and Claude Sonnet.
- Later rounds run `review-branch --claude`: Claude Opus and Sonnet only.
- Reviewers whose CLI is not installed are skipped, and the script says so. Pass a base branch when it is not `origin/main`.
- A round takes several minutes, often longer than a foreground command timeout. Run it in the background and wait for it to finish.
- Do not edit the worktree while a round runs. The reviewers read the live files.

Read every report in full. A failed reviewer, or one that skipped its step 1 map, has not reviewed the change; read its log and run the round again.

Do not write your own review prompt. Change [review-prompt.md](review-prompt.md) instead, so every reviewer gets the same one.

## Acting on findings

- Verify each finding before acting. Fix the real ones, look for the same class of bug elsewhere, and add a test that fails without the fix.
- Do not dismiss a finding on your own judgment when it involves data or behavior you have not checked. Check it against the code or data first.
- Run another round only when the last one led to a high or medium fix. Fix low findings when cheap and list the rest; they do not trigger a round. If a third round still finds high or medium issues, stop and bring the open findings to the user: the change is too large or was not mapped well enough.
- Commit once the review is clean, so commits describe the change, not the review rounds.
- Report what each reviewer found, what you fixed, and what you dismissed with the reason, to the user. Keep review history out of commit messages.
- When a reviewer on the pull request (such as GitHub Copilot) finds something the local reviews missed, add the class of check to [review-prompt.md](review-prompt.md), so the miss does not repeat.

## Reporting review in the PR

Every PR description must include a `Review` section. Keep it current when creating or updating the PR, with:

- Completed round counts and the reviewers/models in each round. List skipped or failed attempts separately; they are not completed reviews.
- Main findings by reviewer or round, what was fixed, what was dismissed and why, and any unresolved findings.
- Review limits, such as static-only inspection or restricted tool access, and verification run after fixes.
- Changes made after the last model review, their verification, and whether another model review ran.

If no review completed, say so and explain why. Summarize the extent of review actually performed rather than implying unperformed checks or approval.
