import math
from multiprocessing.dummy import active_children
import re
import socket
import sys
import threading
import time
from threading import Thread

from dns.query import udp
from dns import *
import dns
import argparse

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

def request_dns():
    """
    Request dns server here. Specify the domain name as you want.
    """
    query = message.make_query("xxx", dns.rdatatype.A,
                                        dns.rdataclass.IN)

def calculate_throughput(B: int, ts: float, tf: float, Tcurrent: float, a: float) -> float:
    """
    calculate throughput

    Parameters:
    B: the length of the video trunk in bytes, ts: start time, tf: end time, a: alpha

    Returns:
    Tcurrent: current throughput
    """
    Tnew = B * 8 / (1024 * (tf - ts))
    Tcurrent = a * Tnew + (1 - a) * Tcurrent
    return Tcurrent
    

def bitrate_selection() -> str:
    raise NotImplementedError


def write_to_log(f, time: float, duration: float, tput: float, \
    avg_tput: float, bitrate: int, serverport: int, chunkname: str):
    f.write(str(int(time)) + ' ' + str(duration) + ' ' + str(tput) + ' ' + str(avg_tput) + \
        str(bitrate) + ' ' + str(serverport) + ' ' + chunkname + '\n')



def bitrate_adaptation(B: int, ts: float, tf: float, Tcurrent: float, a: float, f) -> tuple:
    Tcurrent = calculate_throughput(B, ts, tf, Tcurrent, a)


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
    

