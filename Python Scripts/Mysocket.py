
import socket
import sys

SVR_address = "0.0.0.0"
Port = 44444
buffer_size = 1024

def start_socket_listener() : 
    s = None
    connection=None
    try : 
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((SVR_address,Port))
        s.listen(1)
        print(f"Server avviato. In attesa di connessioni TCP su {SVR_address}:{Port}...")
        connection,address = s.accept()
        print(f"Client connesso da :{address}")
        while True : 
            data = connection.recv(buffer_size)
            if not data : 
                print("Connessione chiusa dal client")
                break
            print(f"Dati in ingresso : {data.decode('utf-8')}")
            connection.sendall(b"Messaggio ricevuto\n") 
    except socket.error as error : 
        print(f"Errore del socket {error}")
        sys.exit(1)
    finally : 
        if 'connection' in locals() and connection : 
            connection.close()
        if 's' in locals() and s : 
            s.close()

if __name__ == "__main__":
    start_socket_listener()