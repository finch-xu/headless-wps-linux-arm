# docker headless wps arm 执行word转pdf

本项目是在ARM64操作系统上，运行wps office程序在docker容器内，并启用RPC端口，能够实现python脚本调用wps进行word文件转pdf的操作。

## 免责声明

项目仅供个人学习和技术研究使用，不得用于商业用途。项目中涉及的 WPS Office 软件版权归金山办公软件股份有限公司所有，请自行前往WPS官网购买正版授权并完成激活。因未经授权使用所产生的一切法律责任，由使用者自行承担，与本项目无关。

## 部署

### ARM64架构

查看项目`ARM64`目录下readme即可，包含基础镜像打包和一个简单的word转pdf的api服务。    

> 我在macOS ARM芯片上打包docker镜像调试的，因为没有Linux ARM环境。请在自己的ARM环境自行测试。       

### x86_64架构

https://github.com/akkuman/headless-wps/  直接使用这个大佬做的镜像。    


## 开发调试

### ARM64架构

使用 https://github.com/timxx/pywpsrpc 的wps rpc sdk     
这是别人做的编译好的ARM版本 https://github.com/kevinhonor/pywpsrpc/blob/master/packages/aarch64/pywpsrpc-2.3.9-cp310-cp310-linux_aarch64.whl    

ARM版本的wps linux程序个人版没有RPC功能，把RPC组件库复制过来也不行，当前项目使用wps365的arm版本。    
wps365有试用30天和激活限制，但是有人发现超过30天也能继续用RPC的功能。所以你可以试试，如果不行，那么就`down`掉容器再`up`一下。    

一些资料参考：
https://github.com/timxx/wpsrpc-sdk/tree/main/lib/aarch64 别人提取麒麟系统的Linux arm wps的RPC组件。  
https://github.com/timxx/pywpsrpc/issues/121   arm的讨论。  
https://github.com/akkuman/headless-wps/issues/7    arm的讨论。     

### x86_64架构

一些资料参考：
https://github.com/timxx/pywpsrpc/ RPC sdk。  


## 其他

用不到但是也保存一下。    

https://forum.wps.cn/topic/41160 这个帖子给了Linux arm 个人版的下载链接。    

64-bit Rpm format Version 11.1.0.9719 2020.10.28    
For X64 https://wdl1.cache.wps.cn/wps/download/ep/Linux2019/9719/wps-office-11.1.0.9719-1.x86_64.rpm     
For MIPS https://wdl1.cache.wps.cn/wps/download/ep/Linux2019/9719/wps-office-11.1.0.9719-1.mips64el.rpm     
For ARM https://wdl1.cache.wps.cn/wps/download/ep/Linux2019/9719/wps-office-11.1.0.9719-1.aarch64.rpm     

64-bit Deb format Version 11.1.0.9719 2020.10.28     
For X64 https://wdl1.cache.wps.cn/wps/download/ep/Linux2019/9719/wps-office_11.1.0.9719_amd64.deb     
For MIPS https://wdl1.cache.wps.cn/wps/download/ep/Linux2019/9719/wps-office_11.1.0.9719_mips64el.deb     
For ARM https://wdl1.cache.wps.cn/wps/download/ep/Linux2019/9719/wps-office_11.1.0.9719_arm64.deb       
