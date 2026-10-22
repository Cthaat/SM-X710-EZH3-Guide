# 文件清单

本地附件在 `release-assets/`，不进入 Git。刷机前必须逐文件核验；分片需合并后验证。

| 文件 | 字节数 | 用途 |
|---|---:|---|
| `BL_HYBRID_EZH3_CYH4_ABL5_AVB3.tar` | 114196480 | system BL |
| `AP_STOCK_EZH3_PRESERVE_DATA_NO_ROOT.tar` | 8705925120 | system AP |
| `HOME_CSC_CHN_X710CHN6EZH3_MQB114014704_REV00_user_low_ship_MULTI_CERT.tar.md5` | 73789548 | system HOME_CSC |
| `AP_ROOT_EZH3_KSUN_NEXT_3.4.2_BOOT_ONLY.tar` | 24903680 | Root AP only |
| `AP_RESCUE_EZH3_STOCK_BOOT_INIT_BOOT_ONLY.tar` | 31539200 | rescue AP only |
| `KernelSU_Next_v3.4.2_33355-release.apk` | 16682167 | optional official manager |
| `Odin3.14.4/Odin3_v3.14.4_Samfw.com.exe` | 3167744 | third-party Odin local tool |
| `Odin3.14.4/cpprest141_2_10.dll` | 5213184 | third-party Odin local tool |
| `Odin3.14.4/SS_DL.dll` | 2555904 | third-party Odin local tool |
| `kernel-corresponding-source.tar.gz` | 994632972 | corresponding kernel source + toolchain archive |

完整 SHA-256 见 [SHA256SUMS](manifests/SHA256SUMS.txt) 与 [机器可读清单](manifests/assets.json)。

Root AP 与救援 AP 都只放 AP 单槽；完整系统升级才用 BL + AP + HOME_CSC。不要跨步骤残留槽位。

官方 Next 管理器附件不是最终实机观察到的 SukiSU 管理器 APK；后者仅记录版本与哈希，没有本地安装包备份。USB 驱动和 Platform Tools 未收录，官方来源见准备章节。

本机私有备份在 `private-backups/`，不属于公共刷机附件。原 Restic 与旧完整系统镜像仅保留原位置索引。
