#!/usr/bin/env python
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import select
import time
import re
import sys
import thread
from multiprocessing import Process
import argparse
import dnslib


def dnsRequest(Port, Type):
    dns_request = dnslib.DNSRecord.question("localhost/index.html", "TXT")
    data = dns_request.pack()
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.sendto(data, ("127.0.0.1", Port))
    result, addr = server_socket.recvfrom(1024)
    answer = dnslib.DNSRecord.parse(result)
    ports = 0
    for resources in answer.rr:
        if resources.rtype == Type:
            ports = resources.rdata.data[0]
    server_socket.close()
    return ports

class Proxy:
    def __init__(self, soc, alpha, dns_port, webserver_port):
        print('init: accepting client')
        self.client, _ = soc.accept()
        self.target = None
        self.webserver_ip = '127.0.0.1'
        self.proxy_ip = ('0.0.0.0', 0)
        self.br = 10
        self.thr = 0
        self.a = alpha
        self.dns_port = dns_port
        self.webserver_port = webserver_port

    def connectServer(self):
        self.target = socket(AF_INET, SOCK_STREAM)
        # print('connecting to server')
        self.target.bind(self.proxy_ip)  # bind socket to fake ip
        if self.webserver_port:
            self.target.connect((self.webserver_ip, int(self.webserver_port)))
        else:
            self.webserver_port = dnsRequest(self.dns_port, dnslib.QTYPE.TXT)
            print("webserver_port" + self.webserver_port)
            self.target.connect((self.webserver_ip, int(self.webserver_port)))
        # print('sending message to server')
        self.communicating()


    def chooseBitrate(self, throughput):
        global bitrate
        for b in bitrate:
            if throughput / 1.5 > b:
                return b
        return bitrate[-1]

    def recvFromApache(self):
        buff_size = 1024
        data = self.target.recv(buff_size)
        if len(data) < buff_size:
            return data
        while True:
            tempt = self.target.recv(buff_size)
            data += tempt
            if len(tempt) < buff_size:
                break
        print('apache length'+str(len(data)))
        # buff_size = 8192
        # pat_length = re.compile(b'Content-Length: .\w+')
        # data = self.target.recv(buff_size)
        # result = re.search(pat_length, data, flags=0)
        # cur_count = 0
        # if result != None:
        #     length = int(result.group(0)[16:])
        #     print("apache length"+str(length))
        #     cur_count = 1
        #     while cur_count * buff_size < length:
        #         data += self.target.recv(buff_size)
        #         cur_count = cur_count + 1
        # else:
            # print("no length field")
        return data


    def sendToClient(self, data):
        self.client.sendall(data)

    def communicating(self):
        global bitrate
        # patterns for finding corresponding information
        pat_bbb = re.compile(b'.f4m')
        pat_name = re.compile(b'Seg[0-9]*-Frag[0-9]*')
        pat_bitrate = re.compile(b'bitrate="[0-9]*"')

        # initialize parameters
        buff_size = 4096
        ts = time.time()
        chunkname = ''
        while True:
            data = self.client.recv(buff_size)
            result = re.search(pat_bbb, data, flags=0)
            if result != None: # if the request is for .f4m
                data.decode()
                real_data = data
                print("request f4m")
                data = data.replace('.f4m', '_nolist.f4m')  # request no_list.f4m instead of original .f4m
                data.encode()
                real_data.encode()
                self.target.send(real_data)
                manifest = self.recvFromApache()
                bitrate_list = re.findall(pat_bitrate, manifest)
                for i in bitrate_list:
                    bitrate.append(int(i.split('"')[1]))  # add received bitrates into a list
                bitrate.sort(reverse=True)
                self.target.send(data)
                fakefile = self.recvFromApache()
                self.sendToClient(fakefile)
                continue

            result = re.search(pat_name, data)
            if result != None: # if the request is for a chunk
                ts = time.time()
                data.decode()
                data = re.sub(r'[0-9]*Seg', str(self.br) + 'Seg', data)
                print(data)
                data.encode()
                chunkname = result.group(0)
                self.target.send(data)
                recv_data = self.recvFromApache()
                tf = time.time()
                self.sendToClient(recv_data)
                dur = tf - ts
                B = len(recv_data)
                t_new = B * 8 / dur / 1024
                self.thr = t_new * self.a + (1 - a) * self.thr
                self.br = self.chooseBitrate(self.thr)
                log.write('%d %f %d %.1f %d %s %s %s\n' % (
                    ts, dur, t_new, self.thr, self.br, self.webserver_ip, self.webserver_port, chunkname))
                continue

             # if the request is for other files
            self.target.send(data)
            recv_data = self.recvFromApache()
            self.sendToClient(recv_data)

            
        # self.client.close()
        # self.target.close()
        # log.close()

    def run(self):
        self.connectServer()


if __name__ == '__main__':

    # parse command line args
    parser = argparse.ArgumentParser(description='start proxying......')

    parser.add_argument('-l', '--logfile', required=True, help='log file path')
    parser.add_argument('-a', '--alpha', required=True, type=float, help='set value of alpha')
    parser.add_argument('-p', '--port', required=True, type=int, help='listening port for proxy.')
    parser.add_argument('-P', '--Port', required=True, type=int, help='DNS server port')
    parser.add_argument('-s', '--webserverport', required=False, type=int, help='default webserver port')

    args = parser.parse_args()

    log = open(args.logfile, 'w')
    a = args.alpha
    listen_port = args.port
    dns_port = args.Port
    webserver_port = args.webserverport

    proxySocket = socket(AF_INET, SOCK_STREAM)
    proxySocket.bind(('', int(listen_port)))
    proxySocket.listen(10)
    bitrate = []
    print('start')

    while True:
        try:
            # a new thread for each connection
            thread.start_new_thread(Proxy(proxySocket, float(a), int(dns_port), webserver_port).run,
                                    ())
        except Exception as e:
            log.close()
            proxySocket.close()
            print(e)
