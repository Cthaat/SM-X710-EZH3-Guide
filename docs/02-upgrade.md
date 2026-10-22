# 混合 BL 与 EZH3 系统升级

先完成准备与完整 SHA-256 校验。本步骤改写引导链与系统；已有解锁状态及备份是前提。

| Odin 槽位 | 精确文件 |
|---|---|
| BL | BL_HYBRID_EZH3_CYH4_ABL5_AVB3.tar |
| AP | AP_STOCK_EZH3_PRESERVE_DATA_NO_ROOT.tar |
| CP | 留空（SM-X710 Wi-Fi） |
| CSC | **HOME_CSC_CHN_X710CHN6EZH3_MQB114014704_REV00_user_low_ship_MULTI_CERT.tar.md5** |
| USERDATA | 留空 |

Options 仅勾 **F. Reset Time**。Auto Reboot、Nand Erase、Re-Partition、Flash Lock、Decompress Data 全关，不加载 PIT。确保使用 HOME_CSC，不能误选清数据 CSC。

1. Download 连接后核对机型、COM、全部槽位与选项，点击一次 Start。
2. 刷写期间保持连接；等 PASS、RES OK、succeed 1 / failed 0。
3. Auto Reboot 关闭时，完成后按侧键 + 音量下退出 Download，黑屏后松开正常启动。首次启动较久，避免反复重启。
4. 用原 PIN 解锁，检查原应用、照片文件、Wi-Fi、触控和声音。正常后才刷 Root。

本次 AP 包含九个原版压缩镜像，压缩内容不改：boot、dtbo、super、recovery、vendor_boot、vbmeta_system、init_boot、modem、qweslicstore。Wi-Fi AP 内有 modem.bin 不表示需要另填 CP。

本次 Odin PASS 用时 04:12。BL 归档有 32 成员，HOME 模式跳过 quest.fv、testvector.fv、QcomCate.fv、Core_NON-HLOS.bin，实际写入 BL 28 + AP 9 + HOME_CSC 3 个成员。归档存在不等于全部写入。

机主确认原 PIN、原文件及基本功能正常，未做全盘逐文件比对。若仍报 PIN 错误，先保存错误并停止追加 Root；不要删除锁屏凭据、EFS、metadata 或执行 factory reset。

## 成品制作边界

使用 CYH4 原签名 ABL 替换 EZH3 ABL；其余 BL 成员取 EZH3，vbmeta flags=3，修改后 OEM 签名不再有效，依赖已解锁启动路径。AP 是从 EZH3 原 AP 选出的九个不变压缩镜像。

.lz4 后缀不证明格式正确。成品核验格式、解压及哈希后冻结，不再随意混入其他 ABL、Magisk init_boot 或 vbmeta。早期完整源固件后来已清理；成品完整保留，制作时源包哈希见 manifests/provenance.json。
