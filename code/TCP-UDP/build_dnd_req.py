import struct

# 构造 dns 查询请求
def build_dns_query(domain):
    # DNS请求报文的格式：Header + Question + Additional
    # 构造Header部分
    header = struct.pack("!HHHHHH", 0x1234, 0x0100, 1, 0, 0, 0)

    # 构造Question部分
    qname = b""
    labels = domain.split(".")
    for label in labels:
        length = len(label)
        qname += struct.pack("!B", length)
        qname += struct.pack("!{}s".format(length), label.encode())
    qname += b"\x00"
    qtype = struct.pack("!H", 1)  # 查询类型为A记录
    qclass = struct.pack("!H", 1)  # 查询类别为Internet

    question = qname + qtype + qclass

    # 构造Additional部分

    additional = b""

    # 构造整个DNS请求报文
    dns_query = header + question + additional

    return dns_query