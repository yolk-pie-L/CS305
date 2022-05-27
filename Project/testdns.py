import socket
from dns import resolver, rdatatype
import dnslib
from dnslib.dns import QTYPE, RR


def request_dns(Port: int) -> int:
    # BUG: dns.resolver.NoNameservers: All nameservers failed to answer the query localhost/index.html. IN TXT: Server 127.0.0.1 UDP port 53 answered A DNS query response does not respond to the question asked.
    dns_resolver = resolver.Resolver()
    dns_resolver.nameservers = ["127.0.0.1"]
    dns_resolver.port = Port
    result = dns_resolver.resolve(qname="localhost/index.html")
    print(str(result))
    web_port = 0
    for i in result.response.answer:
        for j in i.items:
            print(j.to_text())
            web_port = int(j.to_text())
    return web_port


def request_dns_alt(Port: int, Type: int) -> int:
    """DNS Client For Port Acquisition

    Args:
        Port (int): Target port number of the DNS server that provides port information
        Type (int): Type of the DNS RR that carries the port information

    Returns:
        int: Acquisited port number
    """
    # USE THIS ONE
    dns_request = dnslib.DNSRecord.question("localhost/index.html", "TXT")
    data = dns_request.pack()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.sendto(data, ("127.0.0.1", Port))
    result, addr = server_socket.recvfrom(1024)
    answer = dnslib.DNSRecord.parse(result)
    ports = 0
    for resources in answer.rr:
        if resources.rtype == Type:
            ports = resources.rdata.data[0]
    server_socket.close()
    return ports


def request_dns_test_loop(Port: int, Type: int):
    # FOR TEST ONLY
    dns_request = dnslib.DNSRecord.question("localhost/index.html", "TXT")
    data = dns_request.pack()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    flag = "y"
    try:
        while flag == "y":
            server_socket.sendto(data, ("127.0.0.1", Port))
            result, addr = server_socket.recvfrom(1024)
            answer = dnslib.DNSRecord.parse(result)
            ports = []
            for resources in answer.rr:
                if resources.rtype == dnslib.QTYPE[Type]:
                    ports.append(resources.rdata)
            print(ports)
            flag = input("Do you want to continue? (y/n) ")
    except KeyboardInterrupt:
        print("\nExiting...")
        server_socket.close()


print("DNS Port: " + str(request_dns_alt(53, dnslib.QTYPE.TXT)))
