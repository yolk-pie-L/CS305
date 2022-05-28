from os import popen
import socket
import dnslib
from sys import exit
import argparse


class Round_Robin:
    def __init__(self, data):
        self.data = data
        self.data_rr = self.get_item()

    def cycle(self, iterable):
        saved = []
        for element in iterable:
            yield element
            saved.append(element)
        while saved:
            for element in saved:
                yield element

    def get_item(self):
        count = 0
        for item in self.cycle(self.data):
            count += 1
            yield (count, item)

    def get_next(self):
        return next(self.data_rr)


def loadServer(filepath):
    server = []
    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            else:
                s = line.split()[0]
                server.append(s)
    f.close()
    return server


def kill_process(port, type):
    with popen("netstat -aon|findstr /r :" + str(port)) as res:
        res = res.read().split("\n")
    result = []
    for line in res:
        temp = [i for i in line.split(" ") if i != ""]
        if (len(temp) >= 4) and (temp[0] == type):
            add_port = temp[1].split(":")
            if add_port[1] == str(port):
                result.append(
                    {
                        "pid": temp[-1],
                        "type": temp[0],
                        "address": add_port[0],
                        "port": add_port[1],
                    }
                )
    print(result)
    for proc in result:
        popen("taskkill /F /PID " + proc["pid"])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='start dns server')

    parser.add_argument('-s', '--servers', required=True)

    args = parser.parse_args()

    servers = loadServer(args.servers)
    print(servers)
    rr_obj = Round_Robin(servers)
    kill_process(53, "UDP")
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(("127.0.0.1", 53))
    try:
        while True:
            udp_message, clientAddress = serverSocket.recvfrom(1024)
            a = dnslib.DNSRecord(q=dnslib.DNSRecord.parse(udp_message).get_q())
            a_qname = a.get_q().get_qname()
            a_qname = str(a_qname).rstrip(".")
            port = rr_obj.get_next()[1]
            # a.add_answer(dnslib.RR("localhost",dnslib.QTYPE.A,rdata=dnslib.A("127.0.0.1")))
            a.add_answer(
                dnslib.RR(a_qname, dnslib.QTYPE.TXT, rdata=dnslib.TXT(port), ttl=60)
            )
            print(a)
            serverSocket.sendto(a.pack(), clientAddress)
    except KeyboardInterrupt as e:
        serverSocket.close()
        kill_process(53, "UDP")
        exit(0)
