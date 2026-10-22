# 自行推送与发布

当前公开仓库为 https://github.com/Cthaat/SM-X710-EZH3-Guide ，附件在 Release。下述命令供自行复制发布时参考。

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

## GitHub Pages 教程网页

网页地址：https://cthaat.github.io/SM-X710-EZH3-Guide/ 。Pages 以 main 分支的 /docs 目录为发布源，.nojekyll 禁止二次处理生成的 HTML。正文仍以根 README、FILES、NOTICE 和本目录的 Markdown 为编辑源，不要手动修改生成的 HTML。

修改正文后运行：

```powershell
python -m pip install -r tools/site-requirements.txt
python tools/build_site.py
python tools/build_site.py --check
```

构建工具仅读取显式列出的公开教程，生成 12 个 HTML 页面、CSS 和 sitemap.xml。不要把 release-assets、private-backups、.local 或设备原始日志复制到 docs。提交生成文件并推送 main 后由 GitHub Pages 发布。

页面含独立标题、摘要、canonical、中英文首页互指和结构化文章信息。站点地图地址为 https://cthaat.github.io/SM-X710-EZH3-Guide/sitemap.xml 。项目子目录的 robots.txt 不能控制域名根的爬虫规则，因此这里不放误导性的 robots.txt。

站长可在 Google Search Console 添加上述网址前缀资源，完成所有权验证后提交 sitemap.xml，并对首页执行一次 URL 检查 / 请求编入索引。验证代码由站长本人从 Search Console 获取，不要公开账号凭据。Bing Webmaster Tools 也可添加并验证站点。发布网页或提交站点地图均不保证收录、排名或具体时间。


IndexNow 的项目内所有权验证文件为 `indexnow-key.txt`，仅用于通知参与该协议的搜索引擎，不是 GitHub 或 Google 账号凭据。提交时必须指定 keyLocation 为本项目内的完整验证文件地址，只提交本项目路径下的网页。HTTP 200 表示收到 URL；HTTP 202 表示收到但仍待验证，都不能当作已收录证明。Google Search Console 仍需站长独立验证。
