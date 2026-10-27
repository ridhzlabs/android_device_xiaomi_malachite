"""The double tap gesture must not wake the phone in a pocket."""
import os
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(os.environ.get("MALACHITE_DEVICE_ROOT", Path(__file__).resolve().parents[1]))


def overlay_values(name: str) -> dict:
    values = {}
    for path in (ROOT / name).rglob("*.xml"):
        if path.name == "AndroidManifest.xml":
            continue
        for item in ET.parse(path).getroot():
            values[item.get("name")] = (item.text or "").strip()
    return values


class PocketWakeTests(unittest.TestCase):
    def test_double_tap_wake_checks_proximity(self):
        framework = overlay_values("overlay/FrameworkResOverlayMalachite")
        if framework.get("config_supportDoubleTapWake") != "true":
            self.skipTest("double tap to wake is not offered")
        lineage = overlay_values("overlay-lineage/LineageSDKResMalachite")
        self.assertEqual(lineage.get("config_proximityCheckOnWake"), "true")
        self.assertEqual(lineage.get("config_proximityCheckOnWakeEnabledByDefault"), "true")

    def test_timeout_covers_ultrasound_latency(self):
        # The Elliptic sensor's first event came 160-240 ms after activation;
        # on timeout PowerManagerService wakes without a reading.
        lineage = overlay_values("overlay-lineage/LineageSDKResMalachite")
        self.assertGreaterEqual(int(lineage.get("config_proximityCheckTimeout", "250")), 400)


if __name__ == "__main__":
    unittest.main()
