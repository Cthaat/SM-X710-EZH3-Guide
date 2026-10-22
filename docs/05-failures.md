# 真实失败经过

| 阶段 | 结果 | 边界 |
|---|---|---|
| 保留原 BL 的 EZH3 与 HDM/Weaver、诊断 Recovery 实验 | 到锁屏但原 PIN 错误，未修复 | 不纳入成功操作，不分发废弃诊断包 |
| 早期正常系统实验 AP | File analysis 报 LZ4 is invalid | 后改标准 frame 能刷入但仍未修复 PIN；后缀本身不证明有效 |
| CYH4 ABL + EZH3 BL、原版 AP、HOME_CSC | PASS，原 PIN 和文件可用 | 单台组合成功，不足以确认 Gatekeeper/Knox 根因 |
| Next 3.4.1 boot | 曾可用 | 不等于所有直接安装路径安全 |
| 更新 3.4.2 管理器后直接安装，并启用模块 | 循环；回刷旧 Root boot 仍循环 | 不能唯一归因管理器、内核或模块 |
| 原版 EZH3 boot + init_boot | 恢复系统 | 本次实测救援 |
| 冻结 builtin Next 3.4.2 boot AP | uid=0，机主使用正常 | 保存此版本，不直接安装改写启动组合 |

最初粘贴的方案含 Magisk init_boot/vbmeta、清数据 CSC、失败就 factory reset；并非本次最终成功流程。最终使用 HOME_CSC 与 boot-only KernelSU。

Odin PASS 只能证明工具完成刷写，不能单独证明 PIN、解密数据、Root 或模块稳定。离线校验、刷写完成、机主验收在证据中分开记录。
