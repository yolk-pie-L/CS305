
# README

**使用flask**

## docker

进入容器

```
docker run -it -p 7778:7778 -p 7779:7779 project:latest /bin/bash
```



运行netsim.py

```
cd /autograder/netsim
/netsim.py servers start -s servers/2servers
```

## Linux

从根目录下开始寻找文件

```
find / -name netsim.py
```

## 当前阶段感想

在vscode里面每次都要提交变化才能运行（好像）

使用python3在容器外面进行编译  

安装pip包
```sh
apt-get update
apt-get install python3
pip3 install numpy
```


## 参考代码

https://github.com/OmerBaddour/VideoCDN

https://github.com/yuanjihuang/csee4119_project1
