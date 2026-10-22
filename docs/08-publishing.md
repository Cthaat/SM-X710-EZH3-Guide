# 自行推送与发布

本仓库只在本地创建和提交，未连接或上传 GitHub。

## 先审查公开内容和已有提交身份

```powershell
git status --short
git ls-files
git log -1 --format=fuller
```

先检查实际提交的作者/提交者姓名、邮箱及所有已跟踪文件，再推送。修改 git config 只影响未来提交，不会改掉历史邮箱。若需匿名，在首次推送前自行设置合适的 GitHub noreply 身份并用 git commit --amend --reset-author 更新本地首个提交，再检查 git log。不要公开 private-backups 或原始设备日志。

确认后在 GitHub 创建空仓库，再运行（替换为自己的地址）：

```powershell
git status --short
git ls-files
git remote add origin https://github.com/YOUR_NAME/SM-X710-EZH3-Guide.git
git push -u origin main
```



## 大文件单独上传 Release

如果使用已整理好的平铺 Release 附件目录，直接上传目录内全部文件即可，不必再次分片。下载者的校验和合并命令见附件中的 README-RELEASE.md；以下命令用于从完整 release-assets 重新制作分片。

普通 Git 阻止大于 100 MiB 的文件，Release 单附件须小于 2 GiB，见 [大文件说明](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) 和 [Release 限制](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)。

release-assets/ 被忽略，不随 push 上传。创建 Release 后另上传五个核心包、需要的管理器、**对应内核源码**、manifests/assets.json 和 SHA256SUMS.txt。第三方工具与三星固件再分发权限须自行核对。

8.7 GB AP 用工具切为 1 GiB：

```powershell
python tools/assets.py split release-assets/AP_STOCK_EZH3_PRESERVE_DATA_NO_ROOT.tar release-assets/ap-parts
```

上传生成的全部 partNNNN 与 parts.json；下载者同目录放齐再合并：

```powershell
python tools/assets.py join release-assets/ap-parts/parts.json release-assets/AP_STOCK_EZH3_PRESERVE_DATA_NO_ROOT.tar
python tools/assets.py verify manifests/assets.json release-assets
```

合并拒绝覆盖已有文件，逐片/整文件校验。**分片不能直接刷 Odin。** 自行重新生成分片会额外占约 8.7 GB。源码如超过限制也可同法切片。

绝不上传 private-backups。不要把整个仓库文件夹压缩上传；不能把单台实测宣传为全机型或无风险救砖。

工具要求 Python 3.10 或更新版。合并使用同目录硬链接防止覆盖，支持 NTFS/WSL ext4；不支持硬链接的 FAT/exFAT 上请换到支持的磁盘。失败不会生成可用的最终 tar。
