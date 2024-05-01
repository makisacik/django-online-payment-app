import threading
from datetime import datetime
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket, TTransport
from thrift_app.TimestampService import Iface, Processor


class TimestampServiceImpl(Iface):
    def getCurrentTimestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def start_server():
    handler = TimestampServiceImpl()
    processor = Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=10000)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    print('Starting the Thrift server')
    server.serve()


server_thread = None


def run_thrift_server():
    global server_thread
    if server_thread is None or not server_thread.is_alive():
        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()


if __name__ == '__main__':
    run_thrift_server()
