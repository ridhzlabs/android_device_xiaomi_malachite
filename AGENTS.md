# AGENTS.md

Instructions for coding agents, and the people driving them, working in the malachite
device tree. People follow the same rules; the full guides are
[BUILDING.md](BUILDING.md) and
[CONTRIBUTING.md](https://github.com/malachite-project/.github/blob/main/CONTRIBUTING.md).

## How to work

Work as an official LineageOS maintainer for this device would. Find the cause of a
problem before changing anything, then fix it properly, the way LineageOS and AOSP do it:
port the real fix, use the platform's own mechanisms, and write code that would pass
LineageOS review. No workarounds, half fixes, or changes that only make an error go
away. If the proper fix is out of reach, stop and explain what it would take instead of
shipping a hack.

## The project

- Device: Redmi Note 14 Pro 5G / POCO X7 5G, codename **malachite**, MediaTek MT6878.
- Branches: `lineage-23.2` (Android 16, stable) and `lineage-24.0` (Android 17, test
  line). New work goes on `fix/<name>` or `feature/<name>` made from the branch it is for,
  and reaches that branch only after it has been built and tested on a phone.
- A change that applies to both Android versions is made on both, with the same result.
  Behaviour must not drift between them.
- `manifests/malachite.xml` lists every repository the build uses; the comment at its top
  says what each fork changes.

## Code

- Read the files around your change first, and make the change look like them. If it is
  large or introduces a new pattern, stop and ask before writing it.
- Reuse what the tree already has. Don't add new subsystems or invasive changes that
  risk existing behaviour.
- Comments are short and say something a later reader needs (a non-obvious reason), never
  what the line does or what task you were given. Don't add comments to code you copied.
- ASCII only in code, comments and commit messages: `-` not an em dash, `->` not an arrow,
  `...` not an ellipsis.
- An agent never runs `git push` or opens a pull request. The person reviews the diff,
  tests it and sends it.

## Hard rules

1. **Never edit stock blobs.** No hand edits, hex patches or replaced files in
   `vendor/xiaomi/malachite`. Change `proprietary-files.txt` and re-extract from a stock
   dump:
   ```
   ./extract-files.py <stock dump> --no-cleanup --section '<exact section name>'
   ```
   Patch a blob's behaviour with a fixup in `extract-files.py` (`fix_soname`,
   `replace_needed`, `add_needed`, ...), never in the binary. The vendor diff must contain
   only the files you meant to change.
2. **Fix the cause.** No permissive SELinux domains, no `audit2allow` dumps, no
   `dontaudit` over a real denial, no removed checks or disabled features to make a build
   pass. If the cause can't be fixed, say why in the commit body.
3. **Use LineageOS's mechanisms** (Soong config variables, overlays, `PRODUCT_*` lists,
   `lineage.frameworks`, blob fixups) rather than one-off hacks, and follow stock's
   behaviour where stock does something. Cite stock's value in the commit body.
4. **Don't touch the dangerous parts** without an explicit request: partition layout,
   fstab, AVB and signing, boot and recovery images, DTBO, preloader or bootloader. Never
   run flashing commands.
5. **No CI workflows and no unit tests.** A device tree can't be executed; changes are
   verified by building them and testing on a phone.
6. **Never commit** keys, tokens, passwords, personal data, phone logs with identifiers, or
   the build snapshot in `source/`.
7. **Don't remove or weaken the source ID** (`tools/source-id.sh`,
   `tools/source-snapshot.sh`, `sepolicy/private/source_id.te`).

## Files

- **License header** on every new file that takes comments, unless the file comes from
  someone else under another license (then keep theirs):
  ```
  #
  # SPDX-FileCopyrightText: The LineageOS Project
  # SPDX-License-Identifier: Apache-2.0
  #
  ```
  Use `//` for `.bp`, `<!-- -->` for `.xml`. Keep existing headers as they are.
- **`proprietary-files.txt`:** one blob per line, grouped in commented sections, entries
  sorted alphabetically within their section. Add new entries in their sorted place, in
  the right section. Keep existing `|<sha1>` pins.
- **Properties** (`*.prop`, `PRODUCT_*_PROPERTIES`): sorted alphabetically within their
  commented group, each property set once. A property set twice changes meaning when
  sorted (the last one wins), so check for duplicates first.
- Sorting existing unsorted sections is its own commit, with nothing else in it.
- **SELinux:** vendor domains in `sepolicy/vendor`, system_ext policy in
  `sepolicy/private`. Every new label or rule gets a comment saying what needs it.
- Comments say why something is there, not what the next line does.

## Commits

**Subject:** `malachite: <subdir>: <what it does>` - short, plain, lowercase after the
prefixes, no full stop. Add the sub-directory when the change is inside one.

```
malachite: overlay: check proximity before a double tap wake
malachite: sepolicy: let the Xiaomi camera load its feature splits
malachite: wifi: use the pre-U-QPR2 vendor HAL table layout
malachite: set ro.sf.lcd_density again
```

When picking a commit from another device, change its codename to `malachite`, keep the
original author, and end the body with `(cherry picked from commit <sha>)` or a link.

**Body:** why the change is needed: what was wrong, what caused it, why this fixes it.
Short, plain sentences, wrapped at 72 columns. Leave it out when the subject says it all.

Too wordy:

> This commit addresses a critical issue wherein the Wi-Fi HAL experiences a segmentation
> fault during chip initialization, resulting in a complete loss of wireless connectivity.
> Configure the appropriate structure layout to ensure robust and reliable operation.

Right:

> Stock's libwifi-hal-mtk.so uses the pre-U-QPR2 function table. With the
> default layout every entry after wifi_rtt_range_request is shifted, so
> the HAL calls the wrong function at chip setup and Wi-Fi never starts.

Too wordy:

> These properties were previously configured by MIUI but are no longer being set,
> rendering their associated triggers obsolete and effectively non-functional.

Right:

> MIUI set these properties; nothing sets them now, so these triggers never
> fire.

**Also:**
- One logical change per commit. No unrelated formatting or renames.
- The author is the person responsible for the change, with their real name and e-mail.
  No generated-by or co-authored-by trailers for tools.
- Never rewrite history that is already pushed.

## Verifying

- A device tree can't be executed, so a change is verified by building it and testing it
  on a phone. Don't write unit tests for device-tree changes.
- When reporting work, say exactly what was verified (a build, a phone test, with the
  command and result) and what wasn't. Never claim a test that wasn't run.
