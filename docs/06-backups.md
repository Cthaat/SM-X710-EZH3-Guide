# 本机私有备份

private-backups/ 被 Git 忽略，保存本机 BXG5 预刷分区副本，包括 EFS、sec_efs、persist、metadata、devinfo 等。这些可能含身份、校准和加密相关数据，**只适用于原设备，禁止公开，禁止刷给其他机器**。

原 Restic/个人资料仓库和旧系统大镜像保留原位置，路径在私有 LOCAL_BACKUP_LOCATIONS.json 中。为节省空间，没有复制整份 Restic 和旧 super。实际复制的分区大小/哈希在 PRIVATE_SHA256.json；它和位置索引也不进入 Git。

公开救援包只有原版 EZH3 boot + init_boot，没有用户数据、账号、PIN 或 EFS。旧 BXG5 备份不保证可整套降级。

发布前检查 git ls-files，不能含 private-backups、原始 ADB/USB 日志、序列号、账号、密钥或 Restic 密码。不要 git add -f，也不要把整个文件夹压缩后公开。Git 忽略不是加密，本机私有目录应另存自己的加密备份介质。
