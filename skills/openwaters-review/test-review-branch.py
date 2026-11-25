import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("review-branch")


class ReviewerSelectionTest(unittest.TestCase):
    def run_review(self, *args, prev=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, text in (prev or {}).items():
                (root / name).write_text(text)
            args = [a.replace("PREV", tmp) for a in args]
            stub = root / "stub"
            stub.write_text('''#!/bin/sh
name="${0##*/}"
printf '%s\\n' "$name $*" >> "$CALLS"
case "$name" in
  git) case "$1" in merge-base) echo abc123 ;; rev-parse) echo tree0 ;; write-tree) echo tree2 ;; esac ;;
  gh) exit 1 ;;
  mktemp) echo "$REPORTS" ;;
  codex)
    [ "$1" != --version ] || exit 0
    while [ "$1" != -o ]; do shift; done
    echo report > "$2" ;;
  *) echo report ;;
esac
''')
            stub.chmod(0o755)
            for name in ("git", "gh", "mktemp", "codex", "copilot", "claude"):
                (root / name).symlink_to(stub)
            reports = root / "reports"
            reports.mkdir()
            calls = root / "calls"
            env = dict(os.environ, PATH=f"{root}:/usr/bin:/bin",
                       CALLS=str(calls), REPORTS=str(reports))
            result = subprocess.run(["sh", str(SCRIPT), *args], env=env,
                                    text=True, capture_output=True)
            self.round = (reports / "round").read_text() if (reports / "round").exists() else ""
            return result, calls.read_text() if calls.exists() else ""

    def test_later_round_reviews_changes_since_the_last(self):
        prev = {"tree": "tree1\n", "base": "abc123\n", "round": "1\n",
                "findings.md": "F1 a.py:3 unused: dismissed, no caller\n"}
        result, calls = self.run_review("--after=PREV", prev=prev)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.round, "2\n")
        self.assertEqual(calls.count("diff tree1 tree2"), 2)
        self.assertEqual(calls.count("F1 a.py:3 unused: dismissed, no caller"), 2)
        self.assertNotIn("codex ", calls)
        _, calls = self.run_review("--after=PREV", "--only=codex", prev=prev)
        self.assertIn("codex exec", calls)

    def test_later_round_refused(self):
        ok = {"tree": "tree1", "base": "abc123", "round": "1", "findings.md": "F1 fixed\n"}
        for change, reason in (({"findings.md": ""}, "first write"), ({"round": "3"}, "three rounds"),
                               ({"round": ""}, "not the report"), ({"base": "moved"}, "merge base"),
                               ({"tree": "tree2"}, "nothing has changed")):
            with self.subTest(change=change):
                result, calls = self.run_review("--after=PREV", prev={**ok, **change})
                self.assertEqual(result.returncode, 2)
                self.assertIn(reason, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("--model", calls)

    def test_snapshot_keeps_untracked_files_and_the_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "claude").write_text("#!/bin/sh\necho \"$2\"\n")
            (root / "claude").chmod(0o755)
            env = dict(os.environ, PATH=f"{root}:{os.environ['PATH']}", GIT_CONFIG_GLOBAL="/dev/null")
            def run(*cmd):
                return subprocess.run(cmd, cwd=root, env=env, text=True, capture_output=True, check=True).stdout
            run("git", "init", "-q", "-b", "main")
            run("git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "base")
            (root / "new.txt").write_text("new\n")
            first = Path(run("sh", str(SCRIPT), "--only=opus", "main").splitlines()[0])
            self.addCleanup(shutil.rmtree, first)
            self.assertIn("new.txt", run("git", "ls-tree", "--name-only", (first / "tree").read_text().strip()))
            self.assertEqual(run("git", "diff", "--cached", "--name-only"), "")
            (first / "findings.md").write_text("F1 fixed\n")
            (root / "fix.txt").write_text("fix\n")
            second = Path(run("sh", str(SCRIPT), "--after=" + str(first), "--only=opus", "main").splitlines()[0])
            self.addCleanup(shutil.rmtree, second)
            trees = [(d / "tree").read_text().strip() for d in (first, second)]
            self.assertIn("diff " + " ".join(trees), (second / "opus.md").read_text())
            self.assertEqual(run("git", "diff", "--name-only", *trees), "fix.txt\n")
            (first / "tree").write_text("0" * 40)
            gone = subprocess.run(["sh", str(SCRIPT), "--after=" + str(first), "main"], cwd=root, env=env,
                                  text=True, capture_output=True)
            self.assertEqual((gone.returncode, gone.stdout), (2, ""))
            self.assertIn("snapshot is gone", gone.stderr)

    def test_invalid_selection_stops_before_external_commands(self):
        for selection in ("", "   ", "unknown", "opus unknown", "*", "opus *"):
            with self.subTest(selection=selection):
                result, calls = self.run_review(f"--only={selection}")
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("Usage:", result.stderr)
                self.assertEqual(calls, "")

    def test_duplicates_run_once(self):
        result, calls = self.run_review("--only=opus opus sonnet opus")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls.count("--model opus "), 1)
        self.assertEqual(calls.count("--model sonnet "), 1)
        self.assertNotIn("codex ", calls)
        self.assertNotIn("copilot ", calls)

    def test_default_and_single_reviewer(self):
        for args, expected in (((), ("codex", "copilot", "opus", "sonnet")),
                               (("--only=copilot", "origin/develop"), ("copilot",))):
            with self.subTest(args=args):
                result, calls = self.run_review(*args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(len(result.stdout.splitlines()), len(expected) + 1)
                for reviewer in expected:
                    self.assertIn(f"/{reviewer}.md", result.stdout)
                if args:
                    self.assertIn("git merge-base origin/develop HEAD", calls)


if __name__ == "__main__":
    unittest.main()
