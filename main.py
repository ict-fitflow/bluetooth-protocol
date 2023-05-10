#!/usr/bin/env python3
import bluetooth, time

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
    profiles=[bluetooth.SERIAL_PORT_PROFILE],
    # protocols=[bluetooth.OBEX_UUID]
)

print("Waiting for connection on RFCOMM channel", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

# State: ready, pouring, check

try:
    while True:
        data = client_sock.recv(1024).decode('utf-8')
        data = data.split()

        if not data:
            break

        print("Received", data)

        if data[0] == "pour":
            print('POURING')
            grams = int(data[1])
            for g in range(grams + 1):
                client_sock.send(f"{g}")
                time.sleep(0.1)
            client_sock.send("STOP")
            print('FINISH')
        elif data[0] == "check":
            print('CHECK')
            client_sock.send("80") # battery percentage
            client_sock.send("STOP")
            print('FINISH')

except OSError:
    pass

print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.")
