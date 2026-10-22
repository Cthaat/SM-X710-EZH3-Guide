# Samsung Galaxy Tab S9 SM-X710: One UI 8.5, KernelSU-Next Root & Bootloop Rescue

[中文教程](README.md) · [Download flash packages](https://github.com/Cthaat/SM-X710-EZH3-Guide/releases/tag/v1.0-ezh3-ksun342) · [File manifest](FILES.md)

A **single-device verified** upgrade record for the **China/CHN Samsung Galaxy Tab S9 Wi-Fi, SM-X710 / gts9wifi**. It documents a hybrid bootloader, **X710ZCS6EZH3 / Android 16 / One UI 8.5**, a **builtin KernelSU-Next v3.4.2 boot-only root image**, and recovery from a bootloop using stock boot and init_boot.

**Hardware acceptance: 2026-10-16.** The device was already bootloader-unlocked and rooted before this procedure. Compatibility with other devices, regions, rollback levels, firmware or modules has not been established. Keep your own backups before flashing.

## Verified configuration

| Component | Actual version |
|---|---|
| Device / region | Samsung Galaxy Tab S9 SM-X710 / gts9wifi / CHN / Wi-Fi |
| Starting firmware | X710ZCS4BXG5 / Android 14, already unlocked |
| Old ABL donor | **X710ZCU5CYH4** |
| Target firmware | **X710ZCS6EZH3 / Android 16 / SDK 36 / One UI 8.5** |
| Full Android build | BP4A.251205.006.X710ZCS6EZH3 |
| Hybrid BL | CYH4 ABL5 + other EZH3 BL members; vbmeta flags=3 |
| Kernel | 5.15.189-android13-8-33413632-abX710ZCS6EZH3 |
| Root kernel / daemon | KernelSU-Next v3.4.2 / 33355 / UAPI 5 |
| Flash tool | Odin 3.14.4, engine 3.1401 |

The owner confirmed the original PIN, existing apps/photos/files, Wi-Fi, touch and sound worked after the upgrade and root. This was not a full bitwise comparison of every user file. KernelSU source and build records are included with the binary; a clean-machine reproducible build has not been verified.

## Download and reconstruct the system AP

Download the **25 Release assets into one directory**. They include nine parts of the 8.7 GB system AP, the hybrid BL, HOME_CSC, root AP, stock rescue AP, manager APK, Odin ZIP, corresponding kernel source, tutorial ZIP and verification files.

GitHub's **Code → Download ZIP** contains repository documentation and tools only. Firmware is attached to the [Release](https://github.com/Cthaat/SM-X710-EZH3-Guide/releases/tag/v1.0-ezh3-ksun342). The tutorial ZIP attached to that Release is a publication-time snapshot; this repository holds the current guide.

With Python 3.10+ installed, open PowerShell in the asset directory:

```powershell
python assets.py verify release-upload-manifest.json .
python assets.py join parts.json AP_STOCK_EZH3_PRESERVE_DATA_NO_ROOT.tar
```

The tool verifies every part and the reconstructed AP, and refuses to overwrite an existing output. Allow another 8.7 GB for the combined AP. **Never flash a part file directly.**

Expected complete AP SHA-256:

```text
6e5333c80f71d0b59fd8139f68c5aa7fa7090397981ce85e4635be24f89cf647
```

## Flashing sequence

Read the [preconditions and backup boundaries](docs/01-preparation.md) and the detailed linked steps before using Odin.

1. **Firmware upgrade:** BL = `BL_HYBRID_EZH3_CYH4_ABL5_AVB3.tar`; AP = reconstructed `AP_STOCK_EZH3_PRESERVE_DATA_NO_ROOT.tar`; CSC = the supplied **HOME_CSC**. Leave CP and USERDATA empty for this SM-X710 Wi-Fi model. See [upgrade steps](docs/02-upgrade.md).
2. **Check normal operation first:** verify the original PIN, access to existing files and basic functions before rooting. Retaining data was observed on this device, not guaranteed for other devices.
3. **Root:** AP = `AP_ROOT_EZH3_KSUN_NEXT_3.4.2_BOOT_ONLY.tar`. Clear BL, CP, CSC and USERDATA. This changes only boot. See [root steps](docs/03-root.md).
4. **Bootloop rescue:** AP = `AP_RESCUE_EZH3_STOCK_BOOT_INIT_BOOT_ONLY.tar`, all four other slots empty. It restores stock EZH3 boot + init_boot while retaining the mixed BL. Download mode must still be accessible. See [rescue steps](docs/04-rescue.md).

For these steps, only **F. Reset Time** was enabled. Auto Reboot, Nand Erase, Re-Partition, Flash Lock and Decompress Data were off; no PIT was loaded. Follow the manual reboot instructions after Odin PASS. Do not format data, re-lock the bootloader or attempt a full BXG5 downgrade as a routine repair.

## Root and rollback details

- CYH4 ABL5 with other EZH3 BL components does not mean the entire device remains at BL4. Full downgrade compatibility is unproven.
- `kernelsu.norc=1` skips cached custom module init.rc injection; it does **not** disable all modules. Existing modules and pending updates can affect startup.
- Updating a manager, using **Direct Install**, and enabling modules preceded a bootloop. The evidence does not isolate one cause. Restoring stock boot + init_boot succeeded; the frozen builtin v3.4.2 AP then worked.
- The official Next v3.4.2 APK is included. The final observed manager was **com.sukisu.ultra v4.1.0 / 40201**, a different package; its APK was not archived. Root was independently confirmed from the kernel/daemon, physical boot hash and `uid=0`.
- Some modules spoof `getprop` lock-state values. The original bootconfig was **orange**. Preserve the existing unlocked state; do not infer it from a manager label or spoofable properties.
- Rescue covers boot/init_boot faults with working Download mode. It does not establish recovery from every firmware or hardware failure.

## Evidence, source and feedback

- [Acceptance record](evidence/acceptance.json) and [file hashes](manifests/SHA256SUMS.txt)
- [Failure history](docs/05-failures.md), [source/build notes](docs/07-source.md), [private backup policy](docs/06-backups.md)
- [Report a documentation issue](https://github.com/Cthaat/SM-X710-EZH3-Guide/issues): include model, region, firmware build, affected step and exact error. Omit PINs, accounts, serial numbers, EFS and encryption metadata. Additional devices remain unverified until evidence is reviewed.

New tutorial content and tools use [MIT](LICENSE). Samsung firmware, Odin, Linux, KernelSU and the toolchain retain their respective rights and licenses; see [NOTICE](NOTICE.md). Device-specific private backups are excluded from the public repository and Release.
