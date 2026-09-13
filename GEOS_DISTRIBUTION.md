# GEOS 分发与兼容库替换

标书工作台通过 RapidOCR、Shapely 使用 GEOS 3.13.1。GEOS 按 LGPL-2.1 分发；相关权利不受标书工作台其他说明的限制。用户可以为自己的使用修改使用该库的软件，并为调试这些修改进行逆向工程。

分发时须同时提供 GEOS 许可证原文及对应源码 `geos-3.13.1.tar.bz2`。原始源码下载地址：<https://download.osgeo.org/geos/geos-3.13.1.tar.bz2>，SHA-256：`df2c50503295f325e7c8d7b783aca8ba4773919cde984193850cf9e361dfd28c`。Shapely 2.1.2 的 Windows 构建脚本位于 <https://github.com/shapely/shapely/blob/2.1.2/ci/install_geos.cmd>；随源码一并提供该版本 Shapely 源码作为构建参考。

## 构建自己的兼容动态库

使用 Windows x64 C++ 工具链和 CMake，在解压后的 GEOS 源码目录旁执行：

```powershell
cmake -S geos-3.13.1 -B geos-build -G "Visual Studio 17 2022" -A x64 -DBUILD_SHARED_LIBS=ON -DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreaded
cmake --build geos-build --config Release
ctest --test-dir geos-build -C Release --output-on-failure
```

允许修改源码；替换库应保留 GEOS 3.13.1 所需的 C API 和 Windows x64 ABI。将生成的 `geos.dll`、`geos_c.dll` 及它们需要的依赖放进自己选择的目录。把 `geos_c.dll` 复制为当前包所需的名称 `geos_c-072b7a9224d16d3e4ab2395bb855b2d3.dll`；保留 `geos.dll` 原名以供依赖加载。该名称用于匹配导入表，不会检查或限制修改库的内容哈希。

## 验证并启动

先关闭正在运行的标书工作台。在新的 PowerShell 窗口中设置仅对当前进程及其子进程生效的环境变量，使用实际安装目录：

```powershell
$env:BIAOSHU_GEOS_LIBRARY_DIR = 'C:\MyGeos'
& 'C:\实际安装目录\biaoshu-engine.exe' --geos-library-check
& 'C:\实际安装目录\biaoshu-desktop.exe'
```

检查结果应为 `status: passed`、`replacement_loaded: true`，`libraries` 应指向自己选择的目录。程序会在加载 Shapely 前预先加载指定的 GEOS C API 动态库，目录不存在、缺少库或加载失败时直接报错，不静默使用包内库。

退出程序后，在该 PowerShell 窗口执行 `Remove-Item Env:BIAOSHU_GEOS_LIBRARY_DIR`，再启动程序即可恢复默认包内版本；无需修改注册表、系统环境变量或安装目录。其他已启动的程序不会因这条命令改变其运行环境。

本说明覆盖兼容库替换方式；公开分发材料必须另外附完整第三方许可证与所需对应源码，不以本文中的下载链接替代实际分发资料。
