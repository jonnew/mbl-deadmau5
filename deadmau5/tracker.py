import zmq

class Tracker():

    def __init__(self):

        self.is_connected = False

    def __enter__(self):
        return self

    def connect(self, ctx, endpoint):
        try:
            self.socket = ctx.socket(zmq.SUB)
            self.socket.connect(endpoint)
            pos_filter = ''
            # Python 2 - ascii bytes to unicode str
            if isinstance(pos_filter, bytes):
                pos_filter = pos_filter.decode('ascii')
            self.socket.setsockopt_string(zmq.SUBSCRIBE, pos_filter)
            self.is_connected = True
        except zmq.ZMQError:
            self.conn_addr = None
            print ('E [Tracker]: Invalid ' + self.endpoint + ' endpoint.')
            return

    def disconnect(self):
        try:
            self.socket.close()
            self.is_connected = False
        except zmq.ZMQError:
            print ('E [Tracker]: Failed to disconnect from ' + self.endpoint + ' endpoint.')

    def get_position(self):
        if self.is_connected:
            return self.socket.recv_json()
        else:
            return False
