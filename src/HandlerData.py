"""
    The structure of  DNS packet
+---------------------+
|       Header        |  12bytes
+---------------------+
|       Question      | the question for the name server
+---------------------+
|       Answer        | RRs answering the question
+---------------------+
|       Authority     | RRs pointing toward an authority
+---------------------+
|       Additional    | RRs holding additional information
+---------------------+
"""
import random


class Head:
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

    def __init__(self, ID, flag, QDCOUNT, ANCOUNT):
        self.ID = ID
        self.flag = flag
        self.QDCOUNT = QDCOUNT
        self.ANCOUNT = ANCOUNT
        self.NSCOUNT = 0x0000
        self.ARCOUNT = 0x0000

    def unpack(self):
        return {
            'ID': self.ID,
            'flag': self.flag,
            'QDCOUNT': self.QDCOUNT,
            'ANCOUNT': self.ANCOUNT,
            'NSCOUNT': self.NSCOUNT,
            'ARCOUNT': self.ARCOUNT
        }

    def pack(self):
        return self.ID + self.flag + self.QDCOUNT + \
            self.ANCOUNT + self.NSCOUNT + self.ARCOUNT


class Question:
    def __init__(self, QName):
        self.QName = QName
        self.QType = 0x0001
        self.QClass = 0x0001

    def unpack(self):
        return {'QName': self.QName}

    def pack(self):
        return self.QName + self.QType + self.QClass
