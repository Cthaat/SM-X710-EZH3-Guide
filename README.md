# 三星 Samsung Galaxy Tab S9 SM-X710：国行 One UI 8.5 升级、KernelSU-Next Root 与救援教程

[English](README.en.md) · [下载刷机包 / Downloads](https://github.com/Cthaat/SM-X710-EZH3-Guide/releases/latest) · [Root 步骤](docs/03-root.md) · [启动循环救援](docs/04-rescue.md)

这是一次真实升级记录：原机为三星 Tab S9（TabS9），已解锁，从 BXG5 经 CYH4 ABL + EZH3 混合 BL 恢复原 PIN 解锁，再使用自编译 KernelSU-Next 3.4.2 boot-only 包取得 Root。这里记录了国行 CHN 固件升级、混合 BL、Odin 刷机、启动循环（bootloop）恢复和文件校验的完整过程。

Single-device verified guide for **Samsung Galaxy Tab S9 SM-X710 (gts9wifi, China/CHN)**: **One UI 8.5 / Android 16 / EZH3 firmware upgrade**, **KernelSU-Next 3.4.2 root**, hybrid bootloader and stock boot/init_boot rescue. [Read in English](README.en.md).

**实机验收日期：2026-10-16；整理日期：2026-10-22。仅验证一台已解锁的 SM-X710。** 不能推广到其他机型、地区、固件位数或模块组合。文件名中的 PRESERVE_DATA 是制作目标，不是保留数据保证。务必另存自己的备份。

| 项目 | 本次真实版本 |
|---|---|
| 机型 | Samsung Galaxy Tab S9 **SM-X710 / gts9wifi / CHN / Wi-Fi** |
| 起点 | X710ZCS4BXG5，Android 14；原机已解锁并已有 Root |
| 旧 ABL 来源 | **X710ZCU5CYH4**，不是最初示例中的 CYG2 |
| 目标系统 | X710ZCS6EZH3，Android 16 / SDK 36 / One UI 8.5（80500） |
| 完整 build | BP4A.251205.006.X710ZCS6EZH3 |
| 混合 BL | CYH4 ABL5 + EZH3 其他 BL 成员，vbmeta flags=3 |
| 最终内核 | 5.15.189-android13-8-33413632-abX710ZCS6EZH3 |
| Root | builtin KernelSU-Next v3.4.2 / 33355 / UAPI 5 |
| KernelSU 提交 | 4c706b5938665866ebe16944a481a7b91e3396af |
| 实际 Odin | 3.14.4（engine 3.1401） |

## 下载与文件还原

**[进入 Release 下载页](https://github.com/Cthaat/SM-X710-EZH3-Guide/releases/tag/v1.0-ezh3-ksun342)**，文件清单见 [FILES.md](FILES.md)。Release 含 25 个附件：完整系统 AP 的 9 个分片、混合 BL、HOME_CSC、Root AP、救援 AP、管理器、Odin、对应内核源码、教程和校验工具。

1. 将 Release 的全部附件下载到同一个文件夹；完整 AP 必须先合并，分片不能直接交给 Odin。
2. 安装 Python 3.10 或更新版，在**附件下载目录**打开 PowerShell：

```powershell
python assets.py verify release-upload-manifest.json .
python assets.py join parts.json AP_STOCK_EZH3_PRESERVE_DATA_NO_ROOT.tar
```

工具会逐片并对合并文件做 SHA-256 核验，拒绝覆盖已有输出。合并需额外约 8.7 GB；完整 AP 的预期 SHA-256 为 `6e5333c80f71d0b59fd8139f68c5aa7fa7090397981ce85e4635be24f89cf647`。

GitHub 的 “Code → Download ZIP” 只包含教程源码；刷机附件在 Release。Release 内的教程 ZIP 是发布时快照，最新说明以本仓库为准。具体文件用途和槽位见下面的分步教程。

## 阅读顺序

1. [适用条件与备份](docs/01-preparation.md)
2. [文件清单与校验](FILES.md)
3. [混合 BL + 原版 EZH3 升级](docs/02-upgrade.md)：先确认 PIN、文件与基本功能正常。
4. [boot-only Root](docs/03-root.md)：AP 单槽刷入。
5. [启动循环救援](docs/04-rescue.md)：原版 boot + init_boot。

另见 [失败经过](docs/05-failures.md)、[私有备份边界](docs/06-backups.md)、[源码与构建](docs/07-source.md)、[自行发布](docs/08-publishing.md)、[脱敏验收证据](evidence/acceptance.json)。

## 常见问题

**适用于哪些机型？** 仅本次实测的国行 Samsung Galaxy Tab S9 SM-X710 / CHN / gts9wifi。其他地区、SM-X716、Tab S9 FE 或不同固件版本，需要重新核对兼容性。

**升级后还是完整 BL4 吗？** 起点是 BXG5，成功组合使用 CYH4 ABL5 和 EZH3 其他 BL 成员。不能据此保证整套降回 BXG5，详见 [位数与回滚限制](docs/01-preparation.md)。

**Root 后无限重启怎么办？** 本次经原版 EZH3 `boot + init_boot` 恢复系统；救援前提是 Download 可进入、故障在这两个分区范围内，详见 [救援步骤](docs/04-rescue.md)。不要因开机失败直接清数据或重新锁定。

**管理器可以“直接安装”升级吗？** 此启动组合曾在直接安装并启用模块后出现循环，根因未唯一确定。请使用冻结的 boot-only AP 流程。附件官方 Next 3.4.2 APK 与最终实测的 `com.sukisu.ultra v4.1.0/40201` 管理器不同，身份与验证边界见 [Root 说明](docs/03-root.md)。

## 本地仓库布局

- docs、manifests、evidence、tools、tests：进入 Git 的教程、清单、证据与校验工具。
- **release-assets/**：完整刷机附件、管理器、Odin 与内核对应源码；被 Git 忽略，需要另行上传 Release。
- **private-backups/**：本机旧分区备份和本地位置索引；被 Git 忽略，禁止公开。

本次整理没有再次刷机、重启或修改模块，也没有删除源文件。实机结果来自上述验收日期，并非今日重新运行设备测试。

在仓库根目录用 Python 3 校验：

```powershell
python tools/assets.py verify manifests/assets.json release-assets
python -m unittest discover -s tests -v
```

新编写的教程和工具采用 [MIT](LICENSE)。三星固件、Odin、KernelSU 与 Linux 等仍适用各自权利和许可，见 [NOTICE](NOTICE.md)。
