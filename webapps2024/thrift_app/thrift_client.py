from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift_app.TimestampService import Client


def get_current_timestamp():
    try:
        transport = TSocket.TSocket('localhost', 10000)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Client(protocol)

        transport.open()
        timestamp = client.getCurrentTimestamp()
        transport.close()

        return timestamp
    except Thrift.TException as tx:
        print(f"Thrift exception: {tx}")
        return None
