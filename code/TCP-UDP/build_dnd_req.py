import struct


# 构造 dns 查询请求
def build_dns_query(domain):
    # DNS请求报文的格式：Header + Question + Additional

    # 构造Header部分
    transaction_id = 0x1234  # 事务ID
    flags = 0x0100  # 标志：标准查询
    questions = 1  # 问题数
    answer_rrs = 0  # 应答记录数
    authority_rrs = 0  # 授权记录数
    additional_rrs = 0  # 附加记录数
    # 使用 struct.pack 将数据打包为二进制格式
    header = struct.pack(
        "!HHHHHH",
        transaction_id,
        flags,
        questions,
        answer_rrs,
        authority_rrs,
        additional_rrs,
    )
    # H 代表的意思是将数据打包为一个无符号短整型（unsigned short），其长度为2个字节（16位）。
    # I：无符号整型，占用4个字节。
    # B: 无符号字节，占用1个字节。

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
