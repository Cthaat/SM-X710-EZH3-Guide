# 适用条件与准备

本记录仅针对已解锁的国行 SM-X710 Wi-Fi。不能直接用于 SM-X716、Tab S9 FE、其他地区或更新版。原机已有 Root；不包含新机解锁流程，也不承诺解锁不清数据。

1. 核对平板实际型号、当前固件及 Download 画面状态，照片自己保存，不公开设备身份信息。
2. 备份照片、应用文件与账号恢复手段到另一介质。原有环境能读取底层分区时，另存本机 EFS、sec_efs、persist、metadata 和引导分区；不要为了备份再解锁一次。
3. 先完整保存并校验五个核心包，尤其是救援 AP。稳定 USB、足够电量与供电是前提。
4. 旧 Root 模块先记录版本，建议在原可用环境禁用影响启动的模块；不要盲目批量恢复。
5. 电脑准备三星 USB 驱动与 Odin 3.14.4。本地附件有实际 Odin，USB 驱动安装包未收录；如尚未识别设备，先从三星官方渠道安装驱动再继续。

## 位数与回滚限制

起点虽是 BXG5 的 4 版，成功混合包中 ABL 为 CYH4 的 5 版，其余安全固件来自 EZH3 的 6 版。**升级后不是完整 BL4，不能保证整套降回 BXG5。** bootloader 属性显示 CYH4 不能代表所有安全组件都是旧版。

混合 BL 的可用性只有本次实测支持。遇到 SW REV CHECK FAIL、Secure Check、KG/FRP 等，保存原文停止，不以改后缀、换 Odin、PIT、擦除或强刷代替兼容性核对。

## 手动进入 Download

正常时先关机。按住音量上 + 音量下并连接电脑 USB；警告画面后**短按**音量上继续。不要长按进入解锁/重新锁定操作。

循环启动时可按侧键 + 音量下至黑屏，再切换音量上 + 音量下并连接 USB；成功进入就停止重复按键。按键时机以屏幕为准。Odin 的 COM 连接仍需结合平板画面确认。

ADB 仅用于管理器安装与只读核对，可从 [Android 官方 Platform Tools](https://developer.android.com/tools/releases/platform-tools) 获取；本地附件未收录 Platform Tools。已装兼容管理器时刷机本身不依赖 ADB。三星 USB 驱动参考 [官方 USB Driver](https://developer.samsung.com/android-usb-driver)。
