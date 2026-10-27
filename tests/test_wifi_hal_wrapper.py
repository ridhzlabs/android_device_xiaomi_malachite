import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WifiHalWrapperTests(unittest.TestCase):
    def test_wrapper_uses_the_vendor_blobs_table_layout(self):
        # hardware/mediatek's libwifi-hal-wrapper defaults to the Android 16 QPR0 table; our
        # libwifi-hal-mtk.so uses the pre-U-QPR2 one. A mismatch crashes the Wi-Fi HAL at
        # chip setup (registerSubsystemRestartCallbackHandler -> wifi_multi_sta_set_primary_connection).
        mk = (ROOT / "device.mk").read_text()
        self.assertIn("$(call soong_config_set_bool,mediatek_wifi_hal,use_pre_u_qpr2_struct,true)", mk)
        self.assertIn("libwifi-hal-wrapper", mk)


if __name__ == "__main__":
    unittest.main()
