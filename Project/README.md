
# README

此版本proxy.py包含一段时间没有网络请求代理会自动退出。鉴于浏览器的缓存问题，可能看起来有bug，可以翻之前没有添加close的版本。

## 运行指令
运行proxy.py
```sh
python proxy.py -l log.txt -a 0.5 -p 7777 -P 53 -s 8081
```
参数解析  
-l log_file的路径  
-a alpha  
-p listen port  
-P DNS server port  
-s default webserver port, 可选参数 
  
运行dns.py，dns.py和10servers放在一个目录下
```sh
python dns.py -s 10servers
```
  
运行netsim.py

```
cd /root/CS305-proj/docker_setup/netsim
./netsim.py servers start -s servers/2servers
```
改变带宽

```sh
python3 netsim.py onelink start
```
 ```sh
 python3 netsim.py onelink run -e topology/onelink/onelink.events
 ```


## docker

进入容器

```
docker run -it -p 7778:7778 -p 7779:7779 project:latest /bin/bash
```


## Linux

从根目录下开始寻找文件

```
find / -name netsim.py
```

模糊寻找文件，从根目录下寻找所有后缀为.f4m的文件
```sh
find / -name "*.f4m"
```

## 环境问题

运行环境，python2.7.17

file too short
```sh
apt install libapr1
```
```sh
chmod +x /usr/local/apache2/bin/httpd
cd /usr/local/apache2/lib/
rm libaprutil-1.so.0
ln -s libaprutil-1.so.0.5.3 libaprutil-1.so.0
rm libexpat.so.0
ln -s libexpat.so.0.5.0 libexpat.so.0
rm libapr-1.so.0
ln -s libapr-1.so.0.5.1 libapr-1.so.0
```

目前的依赖库
- dnspython
- numpy
- matplotlib
- dnslib
- eventlet


安装不了dns可以安装dnspython，实现同样的效果  
matplotlib安装问题
https://blog.csdn.net/qq_41221841/article/details/123114200


## 其他

VScode中打开代码
```sh
code /com.docker.devenvironments.code/docker_setup/www/vod/big_buck_bunny.f4m
```


## 参考代码

https://github.com/OmerBaddour/VideoCDN

https://github.com/yuanjihuang/csee4119_project1
