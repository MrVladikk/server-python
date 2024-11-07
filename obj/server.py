import socket

class Server:
    def __new__(cls):
        instance = super().__new__(cls)
        instance.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            instance.sck.bind(("localhost", 8080))
            instance.sck.listen(10)
            return instance
        except Exception as e:
            return repr(e)

    def run(self):
        while True:
            print('Waiting for connection...')
            conn, addr = self.sck.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    try:
                        data = conn.recv(1024)
                    except ConnectionError:
                        print('Client closed while receiving')
                        break
                    print(f'Received: {data} | from :{addr}')
                    if data:
                        data = data.decode()
                        data_new = self.string_to_dict(data)
                        print(f'Send: {data_new} | to: {addr}')
                        try:
                            conn.sendall(data.encode())
                        except ConnectionError:
                            print('Cannot send :c')
                            break
                    else:
                        break
                print('Disconnected by', addr)

    def __repr__(self):
        return f'socket: {self.sck}, connection: {self.connection[0]}, address: {self.connection[1]}'

    def string_to_dict(self, request):
        response = {}
        token = ''
        for i in request:
            if i == '\n':
                try:
                    response[token.split(':')[0]] = token.split(':')[1]
                except:
                    continue
                token = ''
            else:
                token += i
        return response