# Galaxy Tab S9 SM-X710 国行 EZH3 升级与 Root 实测教程

这是一次真实升级记录：原机已解锁，从 BXG5 经 CYH4 ABL + EZH3 混合 BL 恢复原 PIN 解锁，再使用自编译 KernelSU-Next 3.4.2 boot-only 包取得 Root。

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

## 阅读顺序

1. [适用条件与备份](docs/01-preparation.md)
2. [文件清单与校验](FILES.md)
3. [混合 BL + 原版 EZH3 升级](docs/02-upgrade.md)：先确认 PIN、文件与基本功能正常。
4. [boot-only Root](docs/03-root.md)：AP 单槽刷入。
5. [启动循环救援](docs/04-rescue.md)：原版 boot + init_boot。

另见 [失败经过](docs/05-failures.md)、[私有备份边界](docs/06-backups.md)、[源码与构建](docs/07-source.md)、[自行发布](docs/08-publishing.md)、[脱敏验收证据](evidence/acceptance.json)。

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
