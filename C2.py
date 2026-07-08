import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class C2Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.running = False

    def start(self):
        self.running = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"[*] Listening on {self.host}:{self.port}")

        self.ui_thread = threading.Thread(target=self.start_ui)
        self.ui_thread.start()

        while self.running:
            client, address = self.server.accept()
            print(f"[*] Accepted connection from {address[0]}:{address[1]}")
            self.clients.append(client)
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def handle_client(self, client):
        while self.running:
            try:
                data = client.recv(1024)
                if not data:
                    break
                print(f"[*] Received: {data.decode('utf-8')}")
                self.ui_output.insert(tk.END, f"[*] Received: {data.decode('utf-8')}\n")
                self.ui_output.see(tk.END)
            except:
                break
        client.close()
        self.clients.remove(client)
        print(f"[*] Connection closed")

    def start_ui(self):
        self.root = tk.Tk()
        self.root.title("C2 Server")

        self.ui_output = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=20)
        self.ui_output.pack(padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.root.mainloop()

    def stop(self):
        self.running = False
        for client in self.clients:
            client.close()
        self.server.close()
        self.root.quit()
        self.root.destroy()
        print("[*] Server stopped")

if __name__ == "__main__":
    server = C2Server('0.0.0.0', 4444)
    server.start()
