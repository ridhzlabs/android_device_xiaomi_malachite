import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReleaseBuildTests(unittest.TestCase):
    def test_nothing_makes_the_build_debuggable(self):
        # LineageOS keeps userdebug builds at ro.debuggable=0 through
        # PRODUCT_NOT_DEBUGGABLE_IN_USERDEBUG; Rooted debugging still works there.
        for path in ROOT.rglob("*.mk"):
            text = path.read_text(errors="ignore")
            with self.subTest(path=path.name):
                self.assertIsNone(re.search(r"PRODUCT_NOT_DEBUGGABLE_IN_USERDEBUG\s*:?=\s*$", text, re.M))
                self.assertNotIn("ro.debuggable=1", text)


if __name__ == "__main__":
    unittest.main()
