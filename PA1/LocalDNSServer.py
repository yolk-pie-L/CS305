import threading
from dns import resolver, rdatatype
import socket

from dns.resolver import NoNameservers, NXDOMAIN, Timeout
from dnslib import DNSRecord, QTYPE, RD, SOA, DNSHeader, RR, A, CNAME, DNSQuestion

"""
clue about multithread:
many dns server thread and each one get dns query, resolve the query and build response.you may put the result into a 
send_queue
a receiver thread that used to receive message from client and distribute message to dns server, you may put it into a 
queue
a sender thread to send dns resolving result back to client
attention that in some system, socket is not thread safe, you may need thread lock
don't forget thread safe in your cache if needed cause many thread will access it
"""


class CacheManager:
    # NOTE: class that manage cache.
    def __init__(self):
        self.fileName = 'dns_cache.txt'
        self.content = []

    def readCache(self, domain_name):
        """
        read cache from file
        :return: ans: list of strings, information needed
        """
        all_names = [domain_name]
        ans = []
        with open(self.fileName, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    f.close()
                    break
                fractions = line.strip('\n').split(' ')
                if fractions[0] in all_names:
                    if fractions[2] == 'CNAME':
                        all_names.append(fractions[1])
                        ans.append(fractions[0]+" "+fractions[-1]+" "+"IN"+" "+fractions[2]+" "+fractions[1])
                    if fractions[2] == 'A':
                        ans.append(fractions[0]+" "+fractions[-1]+" "+"IN"+" "+fractions[2]+" "+fractions[1])
        return ans

    def writeCache(self, response):
        """
        write the record to the file
        :param response: response: string
        """
        with open(self.fileName, 'a') as f:
            for i in response:
                fractions = i.split(" ")
                f.write(fractions[0] + " " + fractions[-1] + " " + fractions[-2] + " " + fractions[1] + "\n")
        f.close()


class ReplyGenerator:
    """
    when exception is raised, call the static method to reply
    """

    @staticmethod
    def replyForNotFound(income_record):
        """
        when raise exception NXDOMAIN, use this function to reply
        :param income_record: the income dns record from dig
        :return: the reply record
        """
        header = DNSHeader(id=income_record.header.id, bitmap=income_record.header.bitmap, qr=1)
        header.set_rcode(3)  # 3 DNS_R_NXDOMAIN, 2 DNS_R_SERVFAIL, 0 DNS_R_NOERROR
        record = DNSRecord(header, q=income_record.q)
        return record

    @staticmethod
    def replyForServerFailed(income_record):
        """
        when raise exception NoNameservers, use this function to reply
        :param income_record:
        :return:
        """
        header = DNSHeader(id=income_record.header.id, bitmap=income_record.header.bitmap, qr=1)
        header.set_rcode(2)  # 3 DNS_R_NXDOMAIN, 2 DNS_R_SERVFAIL, 0 DNS_R_NOERROR
        record = DNSRecord(header, q=income_record.q)
        return record

    @staticmethod
    def replyForTimeout(income_record):
        header = DNSHeader(id=income_record.header.id, bitmap=income_record.header.bitmap, qr=1)
        header.set_rcode(2)  # 3 DNS_R_NXDOMAIN, 2 DNS_R_SERVFAIL, 0 DNS_R_NOERROR
        record = DNSRecord(header, q=income_record.q)
        return record


class DNSServer:
    """
    In this class, you need to implement several methods which set up your
    local DNS server,such as receive, query, reply and others you need
    """

    def __init__(self, source_ip, source_port, ip='127.0.0.1', port=5533):
        self.source_ip = source_ip
        self.source_port = source_port
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))
        self.cache_manager = CacheManager()
        self.dns_handler = DNSHandler(self.source_ip, self.source_port, self.cache_manager)

    def start(self):
        while True:
            message, address = self.receive()
            response = self.dns_handler.handle(message)
            self.reply(address, response)

    # 从命令行里接收信息
    def receive(self):
        return self.socket.recvfrom(8192)

    # 返回到命令行
    def reply(self, address, response):
        self.socket.sendto(response.pack(), address)


class DNSHandler(threading.Thread):
    """
    In this class, you need to implement several methods which provide strategies
    for your DNS server, such as handle, query and others you need
    """

    def __init__(self, source_ip, source_port, cache_manager):
        super().__init__()
        self.source_ip = source_ip
        self.source_port = source_port
        self.LOCAL_DNS_SERVER_IP = '8.8.8.8'
        self.DNS_SERVER_PORT = 53
        self.cache_manager = cache_manager
        self.root_info = []
        self.root_ips = []

    def handle(self, message):
        """
        handle message from DNSServer, and use query to get corresponding answer
        :param message: dns message from dig
        :return response: DNSRecord
        """
        try:
            income_record = DNSRecord.parse(message)
        except:
            return

        domain_name = str(income_record.q.qname)

        response = DNSRecord()
        response.add_question(DNSQuestion(domain_name))
        response.header.id = income_record.header.id
        response.header.qr = 1  # indicates the header is a response

        # 如果可以从cache中读，则从cache中读，并将string变成answer添加到response中
        cache_answer = self.cache_manager.readCache(domain_name)
        if cache_answer:
            print("read from cache")
            for i in cache_answer:
                response.add_answer(*RR.fromZone(i))
            return response

        # 使用query方法向各级服务器发出询问，并处理异常
        try:
            responses = self.query(domain_name, source_ip, source_port)
        except NXDOMAIN:
            return ReplyGenerator.replyForNotFound(income_record)
        except NoNameservers:
            return ReplyGenerator.replyForServerFailed(income_record)
        except KeyboardInterrupt:
            return
        except Timeout:
            return ReplyGenerator.replyForNotFound(income_record)

        # 写入缓存
        self.cache_manager.writeCache(responses)

        # 将query得到的string类型的结果封装成answer放入response中
        for i in responses:
            response.add_answer(*RR.fromZone(i))

        return response

    def query(self, query_name, source_ip, source_port):
        """
        Whole iterative process. Firstly get IP address of root server,
        then enter into a loop until get response whose answer type is A.
        :return: responses: all corresponding response, datatype: string
        """
        # Instantiate dns.resolver.Resolver and set flag (value of rd) as 0.
        dns_resolver = resolver.Resolver()
        dns_resolver.flags = 0X0000

        # Get IP address of root server
        server_ip, server_name = self.queryRoot(source_ip, source_port)
        server_port = self.DNS_SERVER_PORT

        # 从根路径开始查询, 如果查到就break
        hasIP = False
        responses = []
        server_IPs = self.root_ips  # 存储查询途中所有的additional record中的IP，以栈的形式存储IP
        # 当查询出错的时候，或者没有answer与记录的时候，就从server_IPs中弹出栈顶元素，再对栈顶元素继续查询
        # 如果查询中无answer只有additional record的时候，将additional record中所有的ip都压栈压入server_IPs中
        while True:
            dns_resolver.nameservers = [server_ip]
            try:
                result = dns_resolver.resolve(qname=query_name, rdtype=rdatatype.A, source=source_ip,
                                              raise_on_no_answer=False,
                                              source_port=source_port)
            except NoNameservers:
                if not server_IPs:
                    if responses:
                        return responses
                    raise NXDOMAIN
                server_ip = server_IPs.pop()
                continue

            response = result.response
            answer = response.answer
            additional = response.additional
            if len(answer) != 0:  # 如果answer不为空，就在answer里面继续寻找
                for ans in answer:
                    if ans.rdtype == 1:
                        hasIP = True
                        responses = responses + ans.to_text().split("\n")
                        for i in ans.items:
                            server_ip = i.to_text()
                            # print("IP:" + server_ip)
                    if ans.rdtype == 5:
                        responses = responses + [ans.to_text()]
                        for i in ans.items:
                            query_name = i.to_text()
                            print("canonical name:" + query_name)
                if hasIP:
                    return responses
            elif additional:  # 如果answer为空，则在additional里面寻找
                for record in additional:
                    if record.rdtype == 1:
                        re = record.to_text().split("\n")
                        # print("found in server_ip:" + server_ip + " name:" + record.to_text().split(' ')[0])
                        for r in re:
                            server_ip = r.split(" ")[-1]
                            if server_ip not in server_IPs:
                                server_IPs.append(server_ip)
            else:
                if not server_IPs:
                    if responses:
                        return responses
                    raise NXDOMAIN
                server_ip = server_IPs.pop()

    def queryRoot(self, source_ip, source_port):
        """
        Query IP address and name of root DNS server.
        :param source_ip: source IP address of query
        :param source_port: source port number of query
        :return: server_ip, server_name
        """
        # Instantiate dns.resolver.Resolver and set flag (value of rd) as 0.
        dns_resolver = resolver.Resolver()
        dns_resolver.flags = 0X0000
        # Set initial IP name, address and port number.
        server_name = 'Local DNS Server'
        server_ip = self.LOCAL_DNS_SERVER_IP
        server_port = self.DNS_SERVER_PORT
        # Set nameservers of dns_resolver as list of IP address of server.
        dns_resolver.nameservers = [server_ip]

        # Use dns_resolver to query name of root server and receive response.
        answer = dns_resolver.resolve(qname='', rdtype=rdatatype.NS, source=source_ip, raise_on_no_answer=False,
                                      source_port=source_port)
        response = answer.response
        query_name = []  # 将root所有的名字都存到query_name中
        for i in response.answer:
            for j in i.items:
                query_name.append(j.to_text())

        # Use dns_resolver to query addresses of root servers and receive response.
        for query in query_name:
            answer = dns_resolver.resolve(qname=query, rdtype=rdatatype.A, source=source_ip,
                                          raise_on_no_answer=False, source_port=source_port)
            response = answer.response
            for i in response.answer:
                for j in i.items:
                    self.root_info.append([i.name.to_text(), j.to_text()])
                    self.root_ips.append(j.to_text())

        # 将所有root信息以[name, ip]存储到root_info中
        # print(self.root_info)

        server_ip = response.answer[0][0].to_text()
        server_name = response.answer[0].name

        return server_ip, server_name


if __name__ == '__main__':
    source_ip = '192.168.43.196'
    source_port = 5566
    # source_ip = input('Enter your ip: ')
    # source_port = input('Enter your port: ')
    source_ip = str(source_ip)
    source_port = int(source_port)
    local_dns_server = DNSServer(source_ip, source_port)
    dns_handler = DNSHandler(None, None, None)
    root_sever_ip, root_severs = dns_handler.queryRoot(source_ip=source_ip, source_port=source_port)
    print(root_sever_ip)
    print(root_severs)
    local_dns_server.start()
