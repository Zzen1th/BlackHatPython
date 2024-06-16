import socket
import build_dnd_req
import parse_dns_resp


target_host = "223.5.5.5"
target_port = 53

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


client.sendto(
    build_dnd_req.build_dns_query("www.cib.com.cn"),
    (target_host, target_port),
)

response, addr = client.recvfrom(4096)

parse_dns_resp.parse_dns_response(response)

client.close()
