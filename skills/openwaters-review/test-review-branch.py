import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("review-branch")


class ReviewerSelectionTest(unittest.TestCase):
    def run_review(self, *args):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stub = root / "stub"
            stub.write_text('''#!/bin/sh
name="${0##*/}"
printf '%s\\n' "$name $*" >> "$CALLS"
case "$name" in
  git) [ "$1" != merge-base ] || echo abc123 ;;
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
            return result, calls.read_text() if calls.exists() else ""

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
