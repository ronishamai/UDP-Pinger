from socket import *
import sys
import struct

### GLOBAL VARIABLES ###
host = 'localhost'
port = 1337

def init_connection():
    global host
    global port
    
    agent = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create an (IPV4, UDP) socket object 
    agent.bind((host, port))
    return agent

def message_manipulator(data): 
    agent_enc = struct.pack('!B', 1)
    return agent_enc + data[1:]

def interact(agent):
    data, pinger_addr = agent.recvfrom(1405)
    message = message_manipulator(data)
    agent.sendto(message, pinger_addr)

def main():
    try:
        agent = init_connection()
    except:
        print('couldnt connect')
        exit(1)
    try:
        while True:
            interact(agent)
    except:
        print('interacted enough')
        agent.close()
        exit(1)
    agent.close()

if __name__ == "__main__":
    if ((len(sys.argv) < 1) or (len(sys.argv) > 3)):
        print("Error! Too many variables \ few variables")
        sys.exit(1)

    try:
        port_index = sys.argv.index('-p') + 1
        port = int(sys.argv[port_index])

    except:
        pass
 
    main()