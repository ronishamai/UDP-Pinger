## Overview
In order to run our UDP pinger, the agent must be up and running first.
Our UDP pinger sends packets with one byte "0", then 4 bytes sequence number, and finally "."s. The input size field determines how many dots will be in the packet. If a size field is not determined, we shall use the default size of 100.
The agent will respond with the same message (save for the first byte, which will be "1") to the Pinger.
The way we deal with late incoming responses from the agent (packets that timed out but were not totally lost to the abyss) is by allowing our pinger to receive them, check that the sequence number matches the expected sequence from the message that we recently sent and ignoring it if there is no match. Because we only send out new pings after we receive a response or time out, we can expect to receive packets with sequence numbers that are *only* smaller than the current sequence number.
We additionally assume that only one pinger will send request to the agent each time.

## Possible error messages from Pinger:
- Error! Size is bigger than 1400: sent when size field is greater than 1400.
- could not connect: if UDP socket creation failed.
- could not ping: If an error occurs during the sending of the UDP packet or receiving one from the agent.
- Error! Too many variables \ few variables: bad input from user when running the pinger.

## Possible error messages from Agent:
- couldn't connect: could not create a UDP socket.
- interacted enough: received some error during sending and receiving.
- Error! Too many variables \ few variables: bad input from user when running the agent.
