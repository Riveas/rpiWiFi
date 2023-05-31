import network
import socket
from machine import Pin

ssid = ""
password = ""

buzzer = Pin(15, Pin.OUT)


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected to {ip}')
    return ip


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection


def webpage(state):
    # Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./buzzeron">
            <input type="submit" value="Buzzer on" />
            </form>
            <form action="./buzzeroff">
            <input type="submit" value="Buzzer off" />
            </form>
            <p>Buzzer is {state}</p>
            </body>
            </html>
            """
    return str(html)


def serve(connection):
    # Start a web server
    state = 'OFF'
    buzzer.off()
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/buzzeron?':
            buzzer.on()
            state = 'ON'
        elif request == '/buzzeroff?':
            buzzer.off()
            state = 'OFF'
        html = webpage(state)
        client.send(html)
        client.close()


try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()

