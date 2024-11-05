> 好像10-21把手动资源更新方式加回来了，在MAA中“设置”-“软件更新”中有“资源更新”按钮了（v5.8.0-beta.2之后）

# MAAResource-Update

从MaaAssistantArknights/MaaResource更新资源的脚本，资源地址：https://github.com/MaaAssistantArknights/MaaResource/archive/refs/heads/main.zip

**使用前**：将脚本文件与MAA根目录置于同级目录中。修改所用脚本中 `maa_dir`的值为MAA根目录名。

初始脚本实现为shell版，运行于linux/wsl。bat版和python版为gpt翻译加优化得来，均已进行基本验证运行无误。

- .sh：可以安装pv以更改解压进度显示方案
- .bat：基于powershell，可直接双击运行
- .py：需要request库和tqdm库

可能的todo：

- python版资源获取不稳容易失败，得命令行走代理才能稳定下载，可能考虑尝试增加重试机制/使用会话对象/设置适配器等方式
- python版tqdm库等的可选安装
- MAA目录自检测，并使能命令行参数配置
- 增加资源日期检查，如果已是最新就不下载
- 执行完后启动MAA，相当于把自动更新极简地加回去