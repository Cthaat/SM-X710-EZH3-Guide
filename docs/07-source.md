# 内核对应源码与原构建记录

release-assets/kernel-corresponding-source.tar.gz 保存实际 common 源树（含项目修改）、KernelSU-Next v3.4.2 Git bundle、配置、符号表、ABI 白名单、实际编译器/辅助工具及原构建/打包脚本、原版 boot 输入。不含个人分区镜像。

这是源码与原工程记录归档，**尚未在全新环境验证一键构建或字节级重现**。分发自制内核二进制时须同时提供对应源码及原许可。来源：[KernelSU-Next](https://github.com/KernelSU-Next/KernelSU-Next/tree/4c706b5938665866ebe16944a481a7b91e3396af)、[Samsung Open Source](https://opensource.samsung.com/)、[Android Common Kernel](https://android.googlesource.com/kernel/common/)。

在 Linux/WSL 保留符号链接解包：

```bash
tar -xzf kernel-corresponding-source.tar.gz
cd kernel-source
git clone KernelSU-Next-v3.4.2.bundle KernelSU-Next
git -C KernelSU-Next checkout --detach v3.4.2
git -C KernelSU-Next rev-parse HEAD
# 4c706b5938665866ebe16944a481a7b91e3396af
git -C KernelSU-Next rev-list --count HEAD
# 3355
```

common/drivers/kernelsu 指向 ../../KernelSU-Next/kernel。不能直接复制原 worktree 的 .git 指针，也不能用无历史压缩包代替 Git 历史而假设版本号计算不变。

records/ 为原配置、符号表、ABI 白名单及构建脚本。原脚本包含固定路径和一次性目录保护，**不应原样执行**；prepare_v14_package.py 仅保留打包 helper 的历史依赖，其 main 是旧实验，不能当作本教程刷机入口。

toolchain/ 为实际 clang-r450784e（14.0.7）与 kernel-build-tools 的归档，保留许可；构建还需 Linux make、Python3、lz4 等。重建先把 records/config 复制到单独 out/.config，将 CONFIG_UNUSED_KSYMS_WHITELIST 等旧绝对路径改成当前 records/abi_symbollist.raw，核对所有路径，并设置 toolchain 内 bin 路径。

```bash
export ARCH=arm64 LLVM=1 LLVM_IAS=1
export KBUILD_BUILD_USER=edge KBUILD_BUILD_HOST=diagnostic-v14
export SOURCE_DATE_EPOCH=1791960000
export KBUILD_BUILD_TIMESTAMP='Wed Oct 14 06:40:00 UTC 2026'
export GOOGLE_BRANCH=android13-5.15 KMI_GENERATION=8 BUILD_NUMBER=X710ZCS6EZH3
make -C common O="$PWD/out" LLVM=1 LLVM_IAS=1 olddefconfig
make -C common O="$PWD/out" LLVM=1 LLVM_IAS=1 KCFLAGS=-D__ANDROID_COMMON_KERNEL__ LOCALVERSION=-33413632 -j3 Image modules
```

旧构建的 8558 个导出符号 CRC 在新构建中一致，不等于全部驱动运行时验证。包替换 Android V4 boot 内核、添加 kernelsu.norc=1、保留 528 字节早期签名尾、生成 AVB NONE hash footer，再标准 LZ4 frame + USTAR。

保留签名尾不使旧 OEM 签名对新内核有效，AVB 自洽也不是 OEM 认证；依赖已解锁启动路径。

| 输入/输出 | SHA-256 |
|---|---|
| 原版 boot | ac8700ad9d716e43e7d4b90e878012452424927539d36f05f2f1719d2806bcf3 |
| 原版 init_boot | b1a9cf1643487b9c59a809da298280987e49745241322b3502d5d209e79b5f27 |
| 最终 Image | 5ad0112ac03c3c7bb123b26c315fddd28fb979461d05f2fb5f869759361adca8 |
| 未压缩 Root boot | ebbe4338edc383fd2efc8bfc514290d56d2e67d5fa2793c5cbdf43802a442719 |
