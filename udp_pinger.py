from socket import *
import sys
import struct
import time

### GLOBAL VARIABLES ###
agent_port = 1337
agent_IP = None
agent_address = None
size = 100
count = 10
timeout = 1
ID = 0
fails = 0


def message_builder(data):
    global ID
    ID = ID + 1
    encoded_message = data.encode("utf-8")
    pinger_enc = struct.pack("!B", 0)
    ID_enc = struct.pack("!I", ID)
    return pinger_enc + ID_enc + encoded_message


def print_ok_message(t, rcv_msg, IP):
    # we will use the global value instead of decoding the message, bc we already made sure we got back the correct message using validate data
    global ID
    data_len = len(rcv_msg[5:])
    print(f"{data_len} bytes from {IP}: seq={ID} rtt={t} ms")


def print_bad_message(msg_ID):
    print(f"request timeout for icmp_seq {msg_ID}")


def print_summary():
    global count
    global fails
    global agent_IP
    print(f"--- {agent_IP} statistics ---")
    print(
        f"{count} packets transmitted, {count - fails} packets received, {(fails/count):.2f}% packet loss"
    )


def validate_data(rcv_msg, send_msg):
    return (rcv_msg[0] == 1) and (rcv_msg[1:] == send_msg[1:])


def init_connection():
    pinger = socket(AF_INET, SOCK_DGRAM)  # create an (IPV4, UDP) socket object
    pinger.settimeout(timeout)
    return pinger


def ping(pinger, agent_address, data):
    global fails
    global count
    global ID

    # send message
    send_msg = message_builder(data)
    pinger.sendto(send_msg, agent_address)
    start_time = time.perf_counter()

    # receive message
    time_window = start_time + timeout
    while time.perf_counter() < time_window:
        try:
            rcv_msg, agent = pinger.recvfrom(1405)
            end_time = time.perf_counter()
            if validate_data(rcv_msg, send_msg):
                rtt = (end_time - start_time) * 1000
                print_ok_message(rtt, rcv_msg, agent[0])
                return
        except TimeoutError:
            break

    print_bad_message(ID)
    fails = fails + 1


def main():
    try:
        pinger = init_connection()
    except:
        print("could not connect")
        exit(1)
    try:
        data = size * "."
        for i in range(count):
            ping(pinger, agent_address, data)
        print_summary()
    except:
        print("could not ping")
        pinger.close()
        exit(1)
    pinger.close()


if __name__ == "__main__":
    if (len(sys.argv) < 2) or (len(sys.argv) > 10):
        print("Error! Too many variables \ few variables")
        sys.exit(1)

    agent_IP = sys.argv[1]
    agent_address = (agent_IP, agent_port)

    try:
        port_index = sys.argv.index("-p") + 1
        agent_port = int(sys.argv[port_index])
        agent_address = (agent_IP, agent_port)
    except:
        pass

    try:
        size_index = sys.argv.index("-s") + 1
        size = int(sys.argv[size_index])
        if size > 1400:
            print("Error! Size is bigger than 1400")
            sys.exit(1)
    except:
        pass

    try:
        count_index = sys.argv.index("-c") + 1
        count = int(sys.argv[count_index])
    except:
        pass

    try:
        timeout_index = sys.argv.index("-t") + 1
        timeout = float(sys.argv[timeout_index]) / 1000
    except:
        pass

    main()
