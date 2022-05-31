import math
import re
from socket import socket, AF_INET, SOCK_STREAM, error
import sys
import threading
import time
from threading import Thread
from xml.dom.minidom import parseString

from dns.query import udp
from dns import *
import dns
import argparse

bbbf4m = b''
bitrates = []


def recv(req, s, sock):
    try:
        comp = re.compile(b'\r\n\r\n')
        while True:
            req += sock.recv(1)  # receive HTTP header
            result = re.search(comp,req,flags=0)
            if result !=None:
                break
        return req
    except error:
        print('Oooops! Error happened when recv : ' + str(error))
        s.stop()


def send(req, s, sock):
    try:
        sock.send(req)
    except error:
        print('Oooops! Error happened when send : ' + str(error))
        s.stop()



def accept(PORT: int):
    """
    you should bind the ip of your socket to 0.0.0.0 to make the proxy work well
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("0.0.0.0", PORT))
    return sock


def modify_request(message):
    """
    Here you should change the requested bit rate according to your computation of throughput.
    And if the request is for big_buck_bunny.f4m, you should instead request big_buck_bunny_nolist.f4m
    for client and leave big_buck_bunny.f4m for the use in proxy.
    """
    message=re.sub(b'.f4m',b'_nolist.f4m',message,1,flags=0)
    return message


def request_dns(Port: int) -> int:
    dns_resolver = resolver.Resolver()
    dns_resolver.nameservers = ['127.0.0.1']
    dns_resolver.port = Port
    result = dns_resolver.resolve(qname='localhost/index.html', rdtype=rdatatype.A)
    web_port = 0
    for i in result.response.answer:
        for j in i.items:
            web_port = int(j.to_text())
    return web_port


def first_chunk_req() -> str:
    pat_bitrate = re.compile(b'bitrate="[0-9]*"')
    bitrate_list = re.findall(pat_bitrate, bbbf4m)
    print(bitrate_list)
    for i in bitrate_list:
        bitrates.append(int(i.split(b'"')[1]))  # add received bitrates into a list
    bitrates.sort(reverse=True)
    print(bitrates)
    return bitrates[-1]


def bitrate_adaptation(B: int, ts: float, tf: float, T_old: float, a: float, f, serverport: int,
                       chunkname) -> tuple:
    """
    calculate throughput, choose appropriate bitrate, and write to log
    Parameters:
    B: the length of the video trunk in bytes, ts: start time, tf: end time, Told: previous throughput, \
        a: alpha, f: fileIO, serverport: web server port, chunkname: Seg%d-Frag%d, e.g. Seg1-Frag2
    Returns:
    a tuple with the form (current_throughput: float, bitrate_selection: str)
    """
    # calculate throughput
    T_new = B * 8 / (1024 * (tf - ts))*2
    T_avg = a * T_new + (1 - a) * T_old
    # bitrate selection
    if bitrates:
        doc = parseString(bbbf4m)
        collection = doc.documentElement
        media = collection.getElementsByTagName("media")
        for m in media:
            bitrates.append(int(m.attributes['bitrate'].value))
        bitrates.sort(reverse=True)
    T_choose = T_avg / 1.5
    bitchoose=b''
    for b in bitrates:
        if b <= T_choose:
            bitchoose = str(b).encode()
            break
    # write to log
    chunkname = bitchoose + chunkname
    f.write(str(int(ts)) + ' ' + str(tf - ts) + ' ' + str(T_new) + ' ' + str(T_avg) + \
            bitchoose.decode() + ' ' + str(serverport) + ' ' + chunkname.decode() + '\n')
    return T_avg, bitchoose


class Proxy(threading.Thread):
    def __init__(self, sock, log_file, alpha, dns_server_port, web_server_port):
        threading.Thread.__init__(self)
        self.sock = sock # browser connection
        self.log_file = log_file
        self.alpha = alpha
        self.web_server_port = web_server_port
        self.dns_server_port = dns_server_port
        self.server_socket = None
        self.count = 0
        self.thread_stop = False

    def stop(self):
        self.thread_stop = True
        self.sock.close()
        self.server_socket.close()

    def run(self) -> None:
        global bbbf4m
        t_current = 10.0
        bit_choose = b'10'
        while not self.thread_stop:
            body_len = 0
            # Receive HTTP request from Browser
            browser_req = b''
            browser_req = recv(browser_req, self, self.sock)
            web_server_port = self.web_server_port
            if self.web_server_port is None:
                web_server_port = request_dns(self.dns_server_port)
            self.server_socket = socket(AF_INET, SOCK_STREAM)
            self.server_socket.bind(("127.0.0.1", 0))
            self.server_socket.connect(("0.0.0.0", web_server_port))
            # Check if request is for manifest file
            result = re.search(b'.f4m',browser_req,flags=0)
            if result!=None:
                # Send HTTP request to server
                if len(bbbf4m)==0:
                    send(browser_req, self, self.server_socket)
                    # Receive HTTP header of response from Server
                    server_resp = b''
                    server_resp = recv(server_resp, self, self.server_socket)
                    # Reseive HTTP body of response
                    proxy_len = int(re.search(b'(?<=Content-Length: )\d+', server_resp).group(0).decode())
                    recvcount = 0
                    try:
                        while recvcount < proxy_len:
                            bbbf4m += self.server_socket.recv(1)
                            recvcount += 1
                        first_chunk_req()
                    except error:
                        print("Oooops! Error happened when receiving .f4m : ")
                        self.stop()
                # Modify browser response to be for browser manifest file
                browser_req = modify_request(browser_req)
            # check if request is for a chunk
            chunk_req = re.search(b'[\d]*Seg[\d]*-Frag[\d]*', browser_req)
            if chunk_req:
                # modify chunk request to be for same chunk, but of appropriate bitrate
                index_point_start = browser_req.find(chunk_req.group(0))
                index_point_end = browser_req.find(b'Seg')
                if not bitrates:
                    bit_choose = b'10'
                browser_req = browser_req[0:index_point_start] + bit_choose + browser_req[index_point_end:]

            t_s = time.time()
            # Send HTTP request to server
            send(browser_req, self, self.server_socket)
            # Receive HTTP header of response from server
            server_resp = b''
            server_resp = recv(server_resp, self, self.server_socket)
            # Receive HTTP body of response from server
            if re.search(b'Content-Length: ',server_resp,1):
                body_len = int(re.search(b'(?<=Content-Length: )\d+', server_resp).group(0).decode())
                recvcount = 0
                try:
                    while recvcount < body_len:
                        server_resp += self.server_socket.recv(1)
                        recvcount += 1
                except error:
                    print("Oooops! Error happened when receive : "+server_resp.decode())
                    self.stop()
            t_f = time.time()
            chunkname=b''
            if chunk_req:
                up_to_chunkname = re.match(b'GET [\S]*', browser_req).group(0)
                chunkname = re.sub(b'GET ',b'',up_to_chunkname,1)
            t_current, bit_choose = bitrate_adaptation(body_len, t_s, t_f, t_current, self.alpha, self.log_file, web_server_port,
                                     chunkname)
            # Send HTTP response to Browser
            send(server_resp, self, self.sock)


if __name__ == '__main__':

    # 解析命令行参数
    parser = argparse.ArgumentParser(description='start proxying......')
    parser.add_argument('-l', '--logfile', required=True, help='log file path')
    parser.add_argument('-a', '--alpha', required=True, type=float, help='set value of alpha')
    parser.add_argument('-p', '--port', required=True, type=int, help='listening port for proxy.')
    parser.add_argument('-P', '--Port', required=True, type=int, help='DNS server port')
    parser.add_argument('-s', '--webserverport', required=False, type=int, help='default webserver port')
    parser.add_argument('-e', '--exit', required=False, choices=['exit', 'start'])

    args = parser.parse_args()

    proxys = []
    if args.exit == 'exit':
        for p in proxys:
            p.stop()
        sys.exit(0)

    f = open(args.logfile, 'w')

    browser_socket = accept(args.port)  # browser listen
    browser_socket.listen(1000)

    while True:
        # accept browser request and create browser_connection_socket
        sock, addr = browser_socket.accept()  # browser connect
        proxy = Proxy(sock, f, args.alpha, args.Port, args.webserverport)
        proxys.append(proxy)
        proxy.start()