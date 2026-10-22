# KernelSU-Next 3.4.2 boot-only Root

先确认 EZH3 原 PIN、文件和基本功能正常，并保存校验过的救援包。本方法是内建 KernelSU-Next 的自编译 boot，不是 Magisk init_boot 修补。

1. 手动进入 Download，Odin **AP 仅选 AP_ROOT_EZH3_KSUN_NEXT_3.4.2_BOOT_ONLY.tar**。
2. BL、CP、CSC、USERDATA 全空，清掉上次完整升级包。
3. 仅 F. Reset Time，Auto Reboot 关闭，不擦除、不重分区、不锁定。
4. Start，PASS 后退出 Download 正常启动。包只有 boot.img.lz4，不写 BL 或 init_boot。

存在旧模块时可在第一启动早期连续按下并松开音量下至少三次，尝试 KernelSU 安全模式；按键时机未对所有设备验证，不能只凭按过就认为模块已隔离。循环时按救援流程处理。

boot 的 kernelsu.norc=1 仅跳过缓存的自定义模块 init.rc 注入，**不会禁用所有模块或所有脚本**。核对模块及待生效更新，逐个启用、逐个确认。

## 管理器与核对

附件官方 KernelSU_Next_v3.4.2_33355-release.apk 来源与哈希见清单。已有兼容管理器可先保留，不要把不同包名当成同一应用升级。正常开机且 ADB 已授权时，可运行：

```powershell
adb devices
adb install -r release-assets/KernelSU_Next_v3.4.2_33355-release.apk
```

若签名冲突先停止核对，不卸载清数据强行覆盖。本次最终管理器观察到的是 **com.sukisu.ultra v4.1.0 / 40201**，不同于所附官方 Next APK；不能声称官方 APK UI 是最终验收的管理器。其余管理器组合需另行验证。

管理器授权 shell 后，只读检查：

```powershell
adb shell uname -r
adb shell su -c id
adb shell su -c 'cat /proc/bootconfig'
```

本次内核为 5.15.189-android13-8-33413632-abX710ZCS6EZH3，返回 uid=0(root)，守护进程版本/哈希对应 3.4.2。模块能伪装 getprop 的 locked/green，本次原始 bootconfig 是 orange。管理器标签和被修改的属性不能单独证明内核版本或锁状态。

**不要用管理器“直接安装”重复更新此启动组合。** 此前管理器更新后直接安装并启用模块导致循环，回刷旧 Root boot 仍失败；原版 boot + init_boot 恢复后，本冻结 3.4.2 包成功。不能把故障归结为 3.4.2 一概不可用。

最终机主确认原 PIN、应用文件、Wi-Fi、触控、声音正常；当时 10 个模块由机主手动启用。模块未打包，也不保证跨版本兼容。
