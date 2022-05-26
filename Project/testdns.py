from dns import resolver, rdatatype


def request_dns(Port: int) -> int:
    dns_resolver = resolver.Resolver()
    dns_resolver.nameservers = ["127.0.0.1"]
    dns_resolver.port = Port
    result = dns_resolver.resolve(qname="localhost/index.html", rdtype=rdatatype.TXT)
    web_port = 0
    for i in result.response.answer:
        for j in i.items:
            print(j.to_text())
            web_port = int(j.to_text())
    return web_port


print("DNS Port: ", request_dns(53))
