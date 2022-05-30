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
        self.send_count = 0
        self.recv_count = 0
        self.br = 10
        self.a = alpha
        self.dns_port = dns_port
        self.webserver_port = webserver_port

    def getClientRequest(self):
        # print('receving from client')
        request = self.client.recv(4096)
        return request

    def connectServer(self, request):
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
        self.target.send(request)
        self.communicating()


    def chooseBitrate(self, throughput):
        global bitrate
        for b in bitrate:
            if throughput / 1.5 > b:
                return b
        return bitrate[-1]

    def communicating(self):
        global bitrate
        # patterns for finding corresponding information
        pat_bbb = re.compile(b'.f4m')
        pat_length = re.compile(b'Content-Length: .\w+')
        pat_name = re.compile(b'Seg[0-9]*-Frag[0-9]*')
        pat_bitrate = re.compile(b'bitrate="[0-9]*"')
        # initialize parameters
        inputs = [self.client, self.target]
        buff_size = 4096
        cur_count = 0
        ts = time.time()
        chunkname = ''
        while True:
            readable, writeable, errs = select.select(inputs, [], inputs, 20)
            if errs:
                break
            for soc in readable:
                # receive data and check whether it is from client or server
                data = soc.recv(buff_size)
                if data:
                    if soc is self.client:
                        # ts = time.time() # if start timer when receving request, start ts here.
                        self.send_count += 1
                        result = re.search(pat_bbb, data, flags=0)
                        if result != None: # if the request is for .f4m
                            data.decode()
                            real_data = data
                            data = data.replace('.f4m', '_nolist.f4m')  # request no_list.f4m instead of original .f4m
                            data.encode()
                            real_data.encode()
                            self.target.send(real_data)
                            manifest = self.target.recv(409600)
                            bitrate_list = re.findall(pat_bitrate, manifest)
                            for i in bitrate_list:
                                bitrate.append(int(i.split('"')[1]))  # add received bitrates into a list
                            bitrate.sort(reverse=True)
                        result = re.search(pat_name, data)
                        if result != None: # if the request is for a chunk
                            data.decode()
                            data = re.sub(r'[0-9]*Seg', str(self.br) + 'Seg', data)
                            data.encode()
                            chunkname = result.group(0)
                        else:
                            chunkname = ''

                        self.target.send(data)
                    if soc is self.target:
                        tf = time.time()
                        # use content length and packet count to find the last packet's postion
                        result = re.search(pat_length, data, flags=0)
                        if result != None:
                            length = float(result.group(0)[16:])
                            cur_count = 1
                        else:
                            cur_count += 1
                        self.client.send(data)
                        # locate the last packet
                        if cur_count * buff_size > length:
                            cur_count = 1
                            if self.recv_count > 0:
                                dur = tf - ts
                                thr = 8 * length / (dur) / 1024
                                avg_thr = self.a * thr + (1 - self.a) * t_old
                                ts = time.time()  # start ts here to have a better duration estimation
                                t_old = avg_thr
                                print("chunkname"+"("+chunkname+")")
                                if chunkname != '':
                                    log.write('%d %f %d %.1f %d %s %s %s\n' % (
                                        ts, dur, thr, avg_thr, self.br, self.webserver_ip, self.webserver_port,
                                        chunkname))
                                    self.br = self.chooseBitrate(avg_thr)
                            else:
                                t_old = 0
                            self.recv_count += 1
                else:
                    break
        self.client.close()
        self.target.close()
        log.close()

    def run(self):
        request = self.getClientRequest()
        if request:
            self.connectServer(request)


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
