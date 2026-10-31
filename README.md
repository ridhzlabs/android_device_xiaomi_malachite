# Lunaris AOSP for the Redmi Note 14 Pro 5G / POCO X7 5G (malachite)

Device tree for an unofficial **Lunaris AOSP 16.2** (Android 16 QPR2) build for
malachite, based on the LineageOS 23.2 trees from the malachite project.

**Maintainer:** [ridhzlabs](https://github.com/ridhzlabs)

**Device:** Redmi Note 14 Pro 5G / POCO X7 5G, codename **malachite**, MediaTek
MT6878.

## Branch

`lunaris-16.2` is the Lunaris AOSP branch. It is based on the malachite
`lineage-23.2` trees (from [noamtu123](https://github.com/noamtu123)'s fork)
with the Lunaris product flags and local manifest added. `lineage-23.2` stays
in sync with upstream and carries no ROM changes.

## Building

```bash
repo init -u https://github.com/Lunaris-AOSP/android -b 16.2 --git-lfs
repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags

mkdir -p .repo/local_manifests
curl -o .repo/local_manifests/lunaris.xml \
  https://raw.githubusercontent.com/ridhzlabs/android_device_xiaomi_malachite/lunaris-16.2/manifests/lunaris.xml
repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags

. build/envsetup.sh
lunch lineage_malachite-bp4a-user
m bacon
```

The build is `user`, signed with release keys, ships GApps
(`WITH_GMS := true`), uses Lunaris' own Launcher3
(`WITH_PIXEL_LAUNCHER := false`) and the custom UDFPS handler.

Kernel and vendor blobs are prebuilt from the malachite trees; see
[BUILDING.md](BUILDING.md) for the upstream rules and [AGENTS.md](AGENTS.md)
for the working rules.

## Lunaris changes

- `lunaris.mk`: Lunaris flags and `ro.lunaris.maintainer`
- `manifests/lunaris.xml`: Lunaris local manifest
- Native eSIM, libgui ABI, face unlock, backlight, voice-call volume and market
  name patches from the malachite trees are cherry-picked onto the Lunaris
  forks with `tools/apply-malachite-patches.sh`

## Credits

Device tree originally written by **[noamtu123 (Noam)](https://github.com/noamtu123)**,
built on the work of [mt6878-devs](https://github.com/mt6878-devs),
[puhboo](https://github.com/puhboo) and
[cmdr-chara](https://github.com/cmdr-chara), and of the
[LineageOS](https://lineageos.org) project.

Vendor blobs, kernel, hardware and sepolicy trees are the
[malachite-project](https://github.com/malachite-project) forks. The last
`lineage-23.2` snapshots are kept at [FMIUI](https://github.com/FMIUI),
[cmdr-chara](https://github.com/cmdr-chara) and
[nanerb25](https://github.com/nanerb25). `hardware/mediatek` is FMIUI's tree
plus the upstream `mdota` symlink module the device tree lists.

ROM: [Lunaris AOSP](https://github.com/Lunaris-AOSP).

```
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#
```
