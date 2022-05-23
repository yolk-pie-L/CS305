import math
from multiprocessing.dummy import active_children
import re
import socket
import sys
import threading
import time
from threading import Thread
from xml.dom.minidom import parseString

from dns.query import udp
from dns import *
import dns
import argparse


bbbf4m="" # place the big_buck_bunny.f4m file contents here，判断如果不为空就不用存了（相当于缓存起来）
bitrates=[] # 从bbbf4m解析得到的bitrates


def recv(s):
    """
    recevie the request passed to proxy.
    """

def send(s):
    """
    send the response here.
    """  

def exit():
    """
    you should provide a way to exit your proxy well.
    """

def accept(PORT):
    """
    you should bind the ip of your socket to 0.0.0.0 to make the proxy work well
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", PORT))


def modify_request(message):
    """
    Here you should change the requested bit rate according to your computation of throughput.
    And if the request is for big_buck_bunny.f4m, you should instead request big_buck_bunny_nolist.f4m 
    for client and leave big_buck_bunny.f4m for the use in proxy.
    """

def request_dns(Port: int) -> int:
    dns_resolver = resolver.Resolver()
    dns_resolver.nameservers=['127.0.0.1']
    dns_resolver.port=Port
    result=dns_resolver.resolve(qname='localhost/index.html', rdtype=rdatatype.A)
    web_port=0
    for i in result.response.answer:
        for j in i.items:
            web_port=int(j.to_text())
    return web_port
    

def bitrate_adaptation(B: int, ts: float, tf: float, T_old: float, a: float, f, serverport: int, chunkname: str) -> tuple:
    """
    calculate throughput, choose appropriate bitrate, and write to log

    Parameters:
    B: the length of the video trunk in bytes, ts: start time, tf: end time, Told: previous throughput, \
        a: alpha, f: fileIO, serverport: web server port, chunkname: Seg%d-Frag%d, e.g. Seg1-Frag2

    Returns:
    a tuple with the form (current_throughput: float, bitrate_selection: str)
    """
    # calculate throughput
    T_new = B * 8 / (1024 * (tf - ts))
    T_avg = a * T_new + (1 - a) * T_old
    # bitrate selection
    if bitrates:
        doc = parseString(bbbf4m)
        collection = doc.documentElement
        media = collection.getElementsByTagName("media")
        for m in media:
            bitrates.append(int(m.attributes['bitrate'].value))
        bitrates.sort(reverse=True)
    T_choose=T_avg/1.5
    for b in bitrates:
        if b <= T_choose:
            bitchoose = str(b)
            break
    # write to log
    chunkname=bitchoose+chunkname
    f.write(str(int(time)) + ' ' + str(tf-ts) + ' ' + str(T_new) + ' ' + str(T_avg) + \
        bitchoose + ' ' + str(serverport) + ' ' + chunkname + '\n')
    return (T_avg, bitchoose)


class Proxy():
    """
    The class is used to manage connections from clients.
    """
    def __init__(self):
        self.connection = None
        self.send_buffer = None
        self.receive_buffer = None
        """
        Add field as you want
        """


class Connection():
    def __init__(self, conn, address):
        self.conn = conn
        self.address = address
        """
        Add field as you want
        """
    


if __name__ == '__main__':
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='start proxying......')
    parser.add_argument('-l', '--logfile', required=True, help='log file path')
    parser.add_argument('-a', '--alpha', required=True, type=float, help='set value of alpha')
    parser.add_argument('-p', '--port', required=True, type=int, help='listening port for proxy.')
    parser.add_argument('-P', '--Port', required=True, type=int, help='DNS server port')
    parser.add_argument('-s', '--webserverport', required=False, type=int, help='default webserver port')

    args = parser.parse_args()
    
    f=open(args.logfile, 'w')

    """
    Start your proxy. 需要把f也传进来
    """

    accept(args.port)
    
    f.close()
    

