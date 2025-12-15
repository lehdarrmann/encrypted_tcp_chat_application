import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# AES encryption key (must match server's key)
AES_KEY = b'my_secure_chat_key_2024_v1.00000'

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = input("Choose your nickname: ")
        
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
    
    def receive_messages(self):
        """Receive and decrypt messages from server"""
        while True:
            try:
                # Receive message length
                msg_length = int.from_bytes(self.client_socket.recv(4), 'big')
                
                # Receive encrypted message
                encrypted_msg = self.client_socket.recv(msg_length)
                
                # Decrypt and display message
                message = self.decrypt_message(encrypted_msg)
                print(message)
                
            except:
                print("An error occurred!")
                self.client_socket.close()
                break
    
    def send_messages(self):
        """Encrypt and send messages to server"""
        while True:
            try:
                message = input('')
                encrypted_msg = self.encrypt_message(message)
                
                # Send length first, then the encrypted message
                self.client_socket.send(len(encrypted_msg).to_bytes(4, 'big'))
                self.client_socket.send(encrypted_msg)
                
            except:
                print("An error occurred!")
                self.client_socket.close()
                break
    
    def start(self):
        """Connect to server and start chat"""
        self.client_socket.connect((self.host, self.port))
        
        # Handle nickname request
        message = self.client_socket.recv(1024).decode()
        if message == 'NICK':
            self.client_socket.send(self.nickname.encode())
        
        # Start threads for receiving and sending
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
        
        send_thread = threading.Thread(target=self.send_messages)
        send_thread.start()

if __name__ == '__main__':
    client = ChatClient()
    client.start()