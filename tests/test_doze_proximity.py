"""SystemUI must not use the ultrasound proximity sensor."""
import os
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(os.environ.get("MALACHITE_DEVICE_ROOT", Path(__file__).resolve().parents[1]))


def systemui_bools() -> dict:
    values = {}
    for path in (ROOT / "overlay" / "SystemUIOverlayMalachite").rglob("*.xml"):
        if path.name == "AndroidManifest.xml":
            continue
        for item in ET.parse(path).getroot().iter("bool"):
            values[item.get("name")] = item.text.strip()
    return values


def systemui_string_arrays() -> dict:
    values = {}
    for path in (ROOT / "overlay" / "SystemUIOverlayMalachite").rglob("*.xml"):
        if path.name == "AndroidManifest.xml":
            continue
        for item in ET.parse(path).getroot().iter("string-array"):
            values[item.get("name")] = [i.text.strip() for i in item.iter("item")]
    return values


def systemui_strings() -> dict:
    values = {}
    for path in (ROOT / "overlay" / "SystemUIOverlayMalachite").rglob("*.xml"):
        if path.name == "AndroidManifest.xml":
            continue
        for item in ET.parse(path).getroot().iter("string"):
            values[item.get("name")] = (item.text or "").strip()
    return values


class DozeProximityTests(unittest.TestCase):
    def test_doze_does_not_use_proximity(self):
        # Ultrasound proximity reads "near" when flat or while the speaker
        # plays; DozeTriggers then ignores touches on a pulsing call.
        self.assertEqual(systemui_bools().get("doze_proximity_sensor_supported"), "false")

    def test_keyguard_does_not_use_proximity(self):
        # Keyguard falsing turned the ultrasound sensor on at every wake to
        # the lockscreen; the audio HAL then restarts the speaker amp and
        # music playing on the speaker cuts out.
        mapping = systemui_string_arrays().get("proximity_sensor_posture_mapping")
        self.assertTrue(mapping, "posture mapping must be set to override the default sensor")
        self.assertNotIn("android.sensor.proximity", mapping)
        self.assertTrue(all(m and "." not in m for m in mapping))
        self.assertNotIn("proximity_sensor_type", systemui_strings())


if __name__ == "__main__":
    unittest.main()
