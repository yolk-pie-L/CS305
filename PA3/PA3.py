import heapq
import math
import copy
import sys
import traceback

subnetIds = set()  # 二进制表示子网号


def ipv4ToBinarySubnet(ipv4: str) -> str:
    fractions = ipv4.split("/")
    preNum = int(fractions[1])
    decIP = fractions[0].split('.')
    res = ''
    for d in decIP:
        item = bin(int(d))[2:].zfill(8)
        if preNum >= 8:
            res += item
            preNum -= 8
        else:
            item = item[0: preNum]
            res += item
            break
    return res


def binarySubnetToIpv4(binSub: str) -> str:
    preNum = len(binSub)
    binSub += '0' * (32 - preNum)
    mask = preNum
    res = ""
    i = 0
    while i < 3:
        dec = int(binSub[i * 8:i * 8 + 8], 2)
        preNum = preNum - 8
        i = i + 1
        res += str(dec) + "."
    res += '0'
    res += "/" + str(mask)
    return res


class Node:
    def __init__(self):
        self.addresses = []  # 包含的所有端口ip地址
        self.dist = {}  # [destNode] = cost
        self.dist_port = {}  # [destNode] = port 到该点从路由器的哪个端口转发
        self.dist_nextHop = {}  # [destNode] = nextHopPort 到该点的下一跳
        self.nAggreRouteTable = {}  # 未聚集的路由表，子网和路由器端口的关系
        self.aggreRouteTable = {} # 聚集后的路由表

    def __lt__(self, other):
        return 0

    def dijkstra(self):
        heap = []
        for node in self.dist.keys():
            if not math.isinf(self.dist[node]):
                heapq.heappush(heap, (self.dist[node], node))
        while heap:
            destNode = heapq.heappop(heap)[1]
            for destNodeNeighbor in destNode.dist.keys():
                if self.dist[destNodeNeighbor] > destNode.dist[destNodeNeighbor] + self.dist[destNode]:
                    self.dist[destNodeNeighbor] = destNode.dist[destNodeNeighbor] + self.dist[destNode]
                    self.dist_port[destNodeNeighbor] = self.dist_port[destNode]
                    self.dist_nextHop[destNodeNeighbor] = self.dist_nextHop[destNode]
                    heapq.heappush(heap, (self.dist[destNodeNeighbor], destNodeNeighbor))
        if len(self.addresses) > 1:
            self.routeAggregation()

    def routeAggregation(self):
        # 先算出来没有聚集的路由表
        subnet_dist = {}
        for binIp in subnetIds:
            subnet_dist[binIp] = float("inf")
        for ports in self.addresses:
            subnet_dist[ipv4ToBinarySubnet(ports)] = 0
        for node in self.dist.keys():
            if node == self:
                continue
            for address in node.addresses:
                subnet = ipv4ToBinarySubnet(address)
                if subnet_dist[subnet] > self.dist[node]:
                    self.nAggreRouteTable[subnet] = self.dist_port[node]
                    subnet_dist[subnet] = self.dist[node]

        # 聚集路由表
        self.aggreRouteTable = copy.deepcopy(self.nAggreRouteTable)
        routeTableList = sorted(self.nAggreRouteTable)
        for i in range(23, 15, -1):  # i表示前缀长度，从23到16
            j = 0
            buffer = copy.deepcopy(routeTableList)
            while j < len(routeTableList) - 1:
                if len(routeTableList[j]) > i and len(routeTableList[j + 1]) > i and \
                        routeTableList[j][0:i] == routeTableList[j + 1][0:i] and \
                        self.aggreRouteTable[routeTableList[j]] == self.aggreRouteTable[routeTableList[j + 1]]:  # 如果前缀相同且via相同
                    addr = routeTableList[j][0:i]
                    if addr not in routeTableList or self.aggreRouteTable[addr] == self.aggreRouteTable[routeTableList[j]]:
                        self.aggreRouteTable[addr] = self.aggreRouteTable[routeTableList[j]]
                        del self.aggreRouteTable[routeTableList[j]]
                        del self.aggreRouteTable[routeTableList[j + 1]]
                        buffer.remove(routeTableList[j])
                        buffer.remove(routeTableList[j + 1])
                        if addr not in buffer:
                            buffer.append(addr)
                            j = j + 1
                j = j + 1
            routeTableList = sorted(buffer)


if __name__ == '__main__':
    address_node = {}
    with open(sys.argv[1], 'r') as f:
        str1 = f.readline().strip()  # 第一行，将所有地址和节点联系起来
        addresses = str1.split(" ")
        for address in addresses:
            node = Node()
            node.addresses.append(address)
            address_node[address] = node

        str2 = f.readline().strip()  # 第二行，路由器的不同端口的地址
        addresses = str2.split(" ")
        for ports in addresses:
            p_tuple = eval(ports)
            node = Node()
            for p in p_tuple:
                node.addresses.append(p)
                address_node[p] = node

        str3 = f.readline().strip()  # 第三行，网络连接拓扑
        edges = str3.split(" ")
        for edge in edges:
            e_tuple = eval(edge)
            subnetIds.add(ipv4ToBinarySubnet(e_tuple[0]))
            subnetIds.add(ipv4ToBinarySubnet(e_tuple[1]))
            node1 = address_node[e_tuple[0]]
            node2 = address_node[e_tuple[1]]
            cost = int(e_tuple[2])
            node1.dist[node2] = cost
            node2.dist[node1] = cost
            node1.dist_port[node2] = e_tuple[0]
            node2.dist_port[node1] = e_tuple[1]
            node1.dist_nextHop[node2] = e_tuple[1]
            node2.dist_nextHop[node1] = e_tuple[0]

        # 初始化每个Node的dist为正无穷，为之后的dijkstra做准备
        nodes = set(address_node.values())
        for node in nodes:
            for destNode in nodes:
                if destNode == node:
                    node.dist[destNode] = 0
                if destNode not in node.dist.keys():
                    node.dist[destNode] = float("inf")

        # 对于每个node算dijkstra
        for node in nodes:
            node.dijkstra()

        N = int(f.readline())
        for i in range(1, N + 1):
            line = f.readline()
            options = line.split(" ")
            if options[0] == 'PATH':
                path = ""
                startNode = address_node[options[1].strip()]
                endNode = address_node[options[2].strip()]
                curNode = startNode
                while curNode != endNode:
                    path += curNode.dist_port[endNode].split('/')[0] + " " + curNode.dist_nextHop[endNode].split('/')[0] + " "
                    curNode = address_node[curNode.dist_nextHop[endNode]]
                print(path)
            else:  # 路由表
                ip_tuple = eval(options[1])
                curNode = address_node[ip_tuple[1]]
                routeTableList = sorted(curNode.nAggreRouteTable)
                ans = []
                for key in routeTableList:
                    ans.append(binarySubnetToIpv4(key) + " via " + curNode.nAggreRouteTable[key].split('/')[0])
                for addr in curNode.addresses:
                    ans.append(binarySubnetToIpv4(ipv4ToBinarySubnet(addr)) + " is directly connected")
                ans = sorted(ans)
                for item in ans:
                    print(item)
                print("After")
                routeTableList = sorted(curNode.aggreRouteTable)
                ans = []
                for key in routeTableList:
                    ans.append(binarySubnetToIpv4(key) + " via " + curNode.aggreRouteTable[key].split('/')[0])
                for addr in curNode.addresses:
                    ans.append(binarySubnetToIpv4(ipv4ToBinarySubnet(addr)) + " is directly connected")
                ans = sorted(ans)
                for item in ans:
                    print(item)

