import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# AES encryption key (must match server's key)
AES_KEY = b'my_secure_chat_key_2024_v1.00000'
class ChatServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.nicknames = []
        
    def encrypt_message(self, plaintext):
        """Encrypt message using AES-256-CBC"""
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Pad the plaintext
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        
        # Encrypt
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Return IV + ciphertext
        return iv + ciphertext
    
    def decrypt_message(self, encrypted_data):
        """Decrypt message using AES-256-CBC"""
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Decrypt
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Unpad
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext.decode()
    
    def broadcast(self, message, sender_client):
        """Send encrypted message to all clients except sender"""
        encrypted_msg = self.encrypt_message(message)
        
        for client in self.clients:
            if client != sender_client:
                try:
                    # Send length first, then the encrypted message
                    client.send(len(encrypted_msg).to_bytes(4, 'big'))
                    client.send(encrypted_msg)
                except:
                    # Remove client if sending fails
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    nickname = self.nicknames[index]
                    self.nicknames.remove(nickname)
                    self.broadcast(f'{nickname} left the chat!', None)
    
    def handle_client(self, client):
        """Handle individual client connection"""
        while True:
            try:
                # Receive message length
                msg_length = int.from_bytes(client.recv(4), 'big')
                
                # Receive encrypted message
                encrypted_msg = client.recv(msg_length)
                
                # Decrypt message
                message = self.decrypt_message(encrypted_msg)
                
                # Broadcast to other clients
                index = self.clients.index(client)
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname}: {message}', client)
                print(f'{nickname}: {message}')
                
            except:
                # Remove client on error
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                print(f'{nickname} disconnected!')
                self.broadcast(f'{nickname} left the chat!', None)
                break
    
    def receive_connections(self):
        """Accept incoming client connections"""
        print(f'Server listening on {self.host}:{self.port}')
        
        while True:
            client, address = self.server_socket.accept()
            print(f'Connected with {address}')
            
            # Request nickname
            client.send('NICK'.encode())
            nickname = client.recv(1024).decode()
            
            self.nicknames.append(nickname)
            self.clients.append(client)
            
            print(f'Nickname: {nickname}')
            self.broadcast(f'{nickname} joined the chat!', client)
            
            # Send encrypted welcome message to the client
            welcome_msg = self.encrypt_message('Connected to the server!')
            client.send(len(welcome_msg).to_bytes(4, 'big'))
            client.send(welcome_msg)
            
            # Start thread to handle client
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()
    
    def start(self):
        """Start the server"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.receive_connections()

if __name__ == '__main__':
    server = ChatServer()
    server.start()