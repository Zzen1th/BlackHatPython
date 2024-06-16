# DNS
https://yangwang.hk/?p=878
https://www.cnblogs.com/mggahui/p/13899888.html#_label7
https://www.cnblogs.com/crazymakercircle/p/14976612.html#autoid-h3-12-1-0

## 请求结构
1、HEADER：头部，固定 12 字节。六个字段，网络序，无符号二字节打包。
2、QUESTIONS：域名查询记录
3、ADDITIONAL：一般为空
### python struct.pack打包
    # H 代表的意思是将数据打包为一个无符号短整型（unsigned short），其长度为2个字节（16位）。
    # I：无符号整型，占用4个字节。
    # B: 无符号字节，占用1个字节。


## 响应结构
1、HEADER：12字节头部
2、QUESTIONS：查询部分
    # 区分普通label和压缩label，当域名查询时存在重复根域名压缩label就是一个压缩指针指向报文中存在的重复根域名，减少包长度。
3、ANSWERS：应答部分