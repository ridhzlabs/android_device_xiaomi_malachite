#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Lunaris AOSP flags. Included before vendor/lineage so its config sees them.
TARGET_CUSTOM_UDFPS := true
WITH_PIXEL_LAUNCHER := false
WITH_GMS := true

PRODUCT_SYSTEM_PROPERTIES += \
    ro.lunaris.maintainer=ridhzlabs
