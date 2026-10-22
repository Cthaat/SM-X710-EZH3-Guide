# 启动循环救援

仅适用于这套 EZH3 + 混合 BL，且 **Download 可进入**、故障涉及 boot/init_boot 修改。不是通用救砖，不修复硬件或所有引导链损坏。

1. 按准备章节手动进入 Download。
2. Odin Reset，**AP 仅选 AP_RESCUE_EZH3_STOCK_BOOT_INIT_BOOT_ONLY.tar**。
3. BL、CP、CSC、USERDATA 全空，仅 F. Reset Time；不加载 PIT，不擦除、不重分区、不锁定。
4. Start，PASS 后退出 Download 正常启动。
5. 恢复的是 EZH3 原版 boot 与 init_boot，不写混合 BL 和用户数据分区。Root 暂时消失是预期结果；先检查 PIN、文件和系统，再决定是否重新 Root。

这对原版镜像是本次实测退出循环的路径，之前只回刷旧 Root boot 未成功。直接安装可能改 init_boot，同时模块也有改动，不能唯一确定根因。

救援不清理 /data/adb 模块；再次 Root 时可能重新生效。需要在有权限的可用环境核对模块及更新，不能假定已删除。

仍循环或无法进入 Download 就停止，保存错误，使用对应机型专业维修。不要整套降级 BXG5、反复混 BL、擦除 EFS/metadata、重新锁定或 factory reset。恢复原版镜像不能撤销已发生的熔丝/安全状态变化。
