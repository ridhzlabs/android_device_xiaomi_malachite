import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class UsbGadgetInitTests(unittest.TestCase):
    def test_our_usb_init_replaces_hardware_mediatek_common_one(self):
        # hardware/mediatek's aidl/gadget also builds init.<platform>.usb.rc unless the device
        # sets use_custom_usb_gadget_rc; two modules of that name fail the build.
        self.assertIn('name: "init.mt6878.usb.rc"', (ROOT / "init/Android.bp").read_text())
        self.assertIn("$(call soong_config_set_bool,mediatek_gadget,use_custom_usb_gadget_rc,true)",
                      (ROOT / "device.mk").read_text())

    def test_xiaomi_wlan_assistant_is_kept(self):
        # Stock's wlan_assistant picks the Wi-Fi NVRAM by board id; hardware/mediatek's must not
        # be built beside it (same module name).
        self.assertIn("$(call soong_config_set_bool,mediatek_wlan,use_vendor_wlan_assistant,true)",
                      (ROOT / "device.mk").read_text())
        self.assertIn("vendor/bin/wlan_assistant",
                      (ROOT / "proprietary-files.txt").read_text().splitlines())


if __name__ == "__main__":
    unittest.main()
