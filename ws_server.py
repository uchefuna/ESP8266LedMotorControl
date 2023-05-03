

# from itertools import count
import os
import re
import socket as skt
import network as net  # type: ignore
import select as sel
import websocket_helper as wsh  # type: ignore
from time import sleep as slp
from ws_connection import WebSocketConnection as WSC


class WebSocketClient:
    def __init__(self, conn):
        self.connection = conn

    def process(self):
        pass


class WebSocketServer:
    def __init__(self, page, max_connections=1):
        self._listen_s = None
        self._clients = []
        self._max_connections = max_connections
        self._page = page

    def _setup_conn(self, port, accept_handler):
        self._listen_s = skt.socket()
        self._listen_s.setsockopt(skt.SOL_SOCKET, skt.SO_REUSEADDR, 1)

        ai = skt.getaddrinfo("0.0.0.0", port)
        addr = ai[0][4]

        self._listen_s.bind(addr)
        self._listen_s.listen(1)
        if accept_handler:
            self._listen_s.setsockopt(skt.SOL_SOCKET, 20, accept_handler)
        for i in (net.AP_IF, net.STA_IF):
            iface = net.WLAN(i)
            if iface.active():
                print("WebSocket started on ws://%s:%d" %
                      (iface.ifconfig()[0], port))

    def _accept_conn(self, listen_sock):
        cl, remote_addr = listen_sock.accept()
        print(f"Client connection from: {remote_addr}")

        exconn = -1
        for i in range(len(self._clients)):
            lcli = self._clients[i]
            if lcli.connection.address[0] == remote_addr[0]:
                exconn = i
                break

        if len(self._clients) >= (self._max_connections +
                                  (0 if exconn < 0 else 1)):
            # Maximum connections limit reached
            cl.setblocking(True)
            cl.sendall("HTTP/1.1 503 Too many connections\n\n")
            cl.sendall("\n")
            # TODO: Make sure the data is sent before closing
            slp(0.1)
            cl.close()
            return

        try:
            (r, w, e) = sel.select([cl.makefile("rwb", 0)], [], [], 1)
            if len(r) == 1:
                wsh.server_handshake(cl)
            else:
                return
        except OSError:
            # Not a websocket connection, serve webpage
            self._serve_page(cl)
            return

        if exconn >= 0:
            del self._clients[exconn]
        self._clients.append(
            self._make_client(WSC(remote_addr, cl, self.remove_connection)))

    def _make_client(self, conn):
        return WebSocketClient(conn)

    def _serve_page(self, sock):
        try:
            sock.sendall(
                'HTTP/1.1 200 OK\nConnection: close\nServer: WebSocket Server\nContent-Type: text/html\n'
            )
            length = os.stat(self._page)[6]
            sock.sendall('Content-Length: {}\n\n'.format(length))
            # Process page by lines to avoid large strings
            with open(self._page, 'r') as f:
                # text = f.read()
                for line in f:
                    sock.sendall(line)
        except OSError:
            # Error while serving webpage
            pass
        sock.close()

    def stop(self):
        if self._listen_s:
            self._listen_s.close()
        self._listen_s = None
        for client in self._clients:
            client.connection.close()
        print("Stopped WebSocket server.")

    def start(self, port=80):
        if self._listen_s:
            self.stop()
        self._setup_conn(port, self._accept_conn)
        print("Started WebSocket server.")

    def process_all(self):
        for client in self._clients:
            client.process()

    def remove_connection(self, conn):
        for client in self._clients:
            if client.connection is conn:
                self._clients.remove(client)
                return
