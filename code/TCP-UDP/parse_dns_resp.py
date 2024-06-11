import struct


def decode_name(dns_data, offset):
    labels = []
    jumped = False
    jump_offset = 0

    while True:
        (length,) = struct.unpack_from("!B", dns_data, offset)
        if length & 0xC0 == 0xC0:  # 检测到压缩指针
            if not jumped:
                jump_offset = offset + 2
            (pointer,) = struct.unpack_from("!H", dns_data, offset)
            offset = pointer & 0x3FFF  # 获取指针指向的位置
            jumped = True
        elif length == 0:
            offset += 1
            break
        else:
            offset += 1
            labels.append(dns_data[offset : offset + length].decode())
            offset += length

    if jumped:
        return ".".join(labels), jump_offset
    else:
        return ".".join(labels), offset


def parse_dns_response(dns_resp):
    # 解析DNS响应头部
    transaction_id, flags, questions, answer_rrs, authority_rrs, additional_rrs = (
        struct.unpack(">HHHHHH", dns_resp[:12])
    )

    print("Transaction ID:", transaction_id)
    print("Flags:", flags)
    print("Questions:", questions)
    print("Answer RRs:", answer_rrs)
    print("Authority RRs:", authority_rrs)
    print("Additional RRs:", additional_rrs)

    offset = 12
    # 解析问题部分
    for _ in range(questions):
        name, offset = decode_name(dns_resp, offset)
        qtype, qclass = struct.unpack_from(">HH", dns_resp, offset)
        offset += 4
        print(f"Question: {name}, Type: {qtype}, Class: {qclass}")

    # 解析应答部分
    for _ in range(answer_rrs):
        name, offset = decode_name(dns_resp, offset)
        rtype, rclass, ttl, rdlength = struct.unpack_from(">HHIH", dns_resp, offset)
        offset += 10
        rdata = dns_resp[offset : offset + rdlength]
        offset += rdlength

        if rtype == 1:  # A记录
            rdata = ".".join(map(str, rdata))
        else:
            rdata = rdata.hex()

        print(
            f"Answer: {name}, Type: {rtype}, Class: {rclass}, TTL: {ttl}, RData: {rdata}"
        )


if __name__ == "__main__":
    # 示例DNS响应包（十六进制字符串）
    hex_data = "abcd818000010001000000000377777706676f6f676c6503636f6d0000010001c00c00010001000000bc0004d8ef200a"
    data = bytes.fromhex(hex_data)
    parse_dns_response(data)
