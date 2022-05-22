
# README

## 分工
- [ ] 第一部分--cry
- [ ] 第二部分--lx


## 运行指令

```sh
python3 proxy.py -l log.txt -a 0.5 -p 7777 -P 53 -s 8081
```
参数解析
-l log_file的路径
-a alpha
-p listen port
-P DNS server port
-s default webserver port, 可选参数

## docker

进入容器

```
docker run -it -p 7778:7778 -p 7779:7779 project:latest /bin/bash
```



运行netsim.py

```
cd /autograder/netsim
./netsim.py servers start -s servers/2servers
```

## Linux

从根目录下开始寻找文件

```
find / -name netsim.py
```

## 环境问题

在vscode里面每次都要提交变化才能运行（好像）

使用python3在容器外面进行编译  
  


安装pip包
```sh
sudo apt-get update
apt-get install python3
sudo  apt-get install python3-pip
pip3 install numpy
```


## 参考代码

https://github.com/OmerBaddour/VideoCDN

https://github.com/yuanjihuang/csee4119_project1
