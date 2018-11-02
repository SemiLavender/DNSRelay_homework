
class DNSHeader:
    """
         DNS Header
	    0  1  2  3  4  5  6  7  0  1  2  3  4  5  6  7
	  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
	  |                      ID                       |
	  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
	  |QR|  opcode   |AA|TC|RD|RA|   Z    |   RCODE   |
	  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
	  |                    QDCOUNT                    |
	  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
	  |                    ANCOUNT                    |
	  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
	  |                    NSCOUNT                    |
	  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
	  |                    ARCOUNT                    |
	  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    """
    def __init__(self, transID, flags, qdcount, ancount, nscount, arcount):
        """
        :param transID: 会话标识    2byte
        :param flags: 标志字段      2byte
        :param qdcount: 问题数目    2byte
        :param ancount: 资源记录数目  2byte
        :param nscount: 授权资源数目  2byte
        :param arcount: 额外资源数目  2byte
        """
        self.transID = transID
        self.flags = flags
        self.qdcount = qdcount
        self.ancount = ancount
        self.nscount = nscount
        self.arcount = arcount

    # 输出包含DNS协议头所有信息的字节数组
    def toByteArray(self):
        pass
