"""Cross-file contracts required by the stock Xiaomi Camera pipeline."""
import os
from pathlib import Path
import unittest


ROOT = Path(os.environ.get("XIAOMI_CAMERA_TEST_DEVICE_ROOT", Path(__file__).resolve().parents[1]))


def proprietary_destinations() -> set[str]:
    paths = set()
    for raw in (ROOT / "proprietary-files.txt").read_text().splitlines():
        line = raw.partition("#")[0].strip().removeprefix("-")
        if line:
            paths.add(line.split(";", 1)[0].split("|", 1)[0].split(":")[-1])
    return paths


class XiaomiCameraContractTests(unittest.TestCase):
    def test_afbc_nv21_video_buffers_have_the_stock_capability_level(self):
        properties = dict(
            line.split("=", 1) for raw in (ROOT / "vendor.prop").read_text().splitlines()
            if (line := raw.partition("#")[0].strip()) and "=" in line
        )
        # libmtkcam_grallocutils defaults to 0; its NV21 conversion requires >2.
        # Without this, video buffer creation returns null and the HAL crashes.
        self.assertEqual(properties.get("ro.vendor.afbc.enable"), "3")

    def test_stock_postprocessing_resources_are_packaged(self):
        paths = proprietary_destinations()
        watermark = {path for path in paths
                     if path.startswith("odm/etc/camera/xiaomi/watermark/")}
        self.assertEqual(len(watermark), 105)
        self.assertLessEqual({
            "odm/etc/camera/xiaomi/watermark/MiSans-Demibold.ttf",
            "odm/etc/camera/xiaomi/watermark/MiSans-Medium.ttf",
            "odm/etc/camera/xiaomi/watermark/Roboto-Bold.ttf",
            "odm/etc/camera/xiaomi/watermark/Roboto-Medium.ttf",
        }, watermark)
        self.assertLessEqual({
            "odm/etc/camera/110_BlackGold.png",
            *{f"odm/etc/camera/{number}_{name}.png" for number, name in (
                (148, "Mild"), (149, "LilyWhite"), (150, "Bright"),
                (151, "Fresh"), (152, "Limpid"), (153, "KC64"),
                (154, "V250"), (155, "H400"), (156, "ColdWhite"),
                (157, "Native"), (158, "BWClassical"), (159, "Flowers"),
                (160, "Vivid"), (161, "KP160"), (162, "Natural"),
                (163, "KG200"), (164, "FC400"), (165, "C50D"),
                (166, "F50"), (167, "CC"), (168, "NC"),
            )},
            "odm/etc/camera/beauty/resources/TStools_default_param.json",
            "odm/etc/camera/beauty/resources/Version.txt",
            "odm/etc/camera/beauty/resources/default_param.json",
        }, paths)

    def test_xiaomi_background_service_uses_its_stock_hal_boundary(self):
        context = (ROOT / "sepolicy/vendor/service_contexts").read_text()
        self.assertIn(
            "vendor.xiaomi.hardware.aidlbgservice.IBGService/default "
            "u:object_r:hal_aidlbgservice_service:s0", context)
        policy = (ROOT / "sepolicy/vendor/hal_aidlbgservice.te").read_text()
        self.assertIn("hal_attribute(aidlbgservice)", policy)
        self.assertIn("hal_attribute_service(hal_aidlbgservice, hal_aidlbgservice_service)", policy)
        self.assertIn("hal_server_domain(mtk_hal_camera, hal_aidlbgservice)", policy)
        client = (ROOT / "sepolicy/vendor/platform_app.te").read_text()
        self.assertIn("hal_client_domain(platform_app, hal_aidlbgservice)", client)
        self.assertIn("binder_call(hal_aidlbgservice, platform_app)", client)


    def test_downloaded_feature_split_libraries_can_be_mapped(self):
        # Panorama, clone, vlog... are qigsaw splits whose native libraries
        # live in the app's own data directory (app_data_file).
        policy = (ROOT / "sepolicy/private/platform_app.te").read_text()
        rules = [line.strip() for line in policy.splitlines()
                 if line.strip() and not line.lstrip().startswith("#")]
        self.assertIn("allow platform_app app_data_file:file execute;", rules)
        # execve() of app data stays denied, as for every other app domain.
        self.assertFalse(any("execute_no_trans" in rule for rule in rules))

    def test_camera_variant_comes_from_the_bootloader_and_board(self):
        # The camera loads com.mi.device.<Build.DEVICE><suffix>: "_pro" (200 MP
        # Ultra HD mode) when ro.boot.camera.config is 0, which LK sets only on
        # the Global Redmi board; "_y" when ro.product.marketname is exactly
        # "POCO X7". Nothing here may override the LK value, and only the POCO
        # boards may carry the POCO market name.
        for path in ROOT.rglob("*"):
            if path.is_file() and path.suffix in {".prop", ".rc", ".mk", ".sh"}:
                self.assertNotIn("camera.config", path.read_text(errors="ignore"), path)
        poco = {p.stem: p.read_text() for p in (ROOT / "marketname").glob("*.prop")}
        self.assertEqual(set(poco), {"S99016IA1", "S99116EA1"})
        for text in poco.values():
            self.assertEqual(text, "ro.product.marketname=POCO X7\n")

if __name__ == "__main__":
    unittest.main()
