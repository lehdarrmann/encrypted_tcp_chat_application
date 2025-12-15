# encrypted_tcp_chat_application

A secure multi-client chat application built with Python featuring AES-256 encryption for real-time communication.

## Features

- **TCP Socket Communication**: Reliable client-server architecture using TCP protocol
- **Multi-Client Support**: Server handles multiple simultaneous clients using threading
- **AES-256 Encryption**: All messages encrypted with AES-256-CBC for secure transmission
- **Real-Time Messaging**: Instant broadcast messaging to all connected clients
- **User Authentication**: Nickname system for user identification

## Technologies Used

- Python 3
- Socket Programming
- Multi-threading
- Cryptography Library (AES-256-CBC with PKCS7 padding)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/lehdarrmann/encrypted_tcp_chat_application.git
cd encrypted_tcp_chat_application
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python -m chatroom.server
```

2. In separate terminals, start client(s):
```bash
python -m chatroom.client
```

3. Enter a nickname when prompted and start chatting!

## How It Works

- Server listens on `localhost:5555` for incoming connections
- Each client connection spawns a new thread for concurrent handling
- Messages are encrypted with AES-256-CBC before transmission
- All messages are broadcast to connected clients (except sender)
- Graceful handling of client disconnections

## Security Note

This project uses a hardcoded encryption key for demonstration purposes. In a production environment, implement proper key exchange mechanisms such as Diffie-Hellman or use TLS/SSL for secure key distribution.

## Future Enhancements

- Private messaging between users
- Persistent chat history
- User authentication system
- GUI interface
- File transfer capability

## License

MIT License - feel free to use this project for learning purposes.

## Author

Will Lehdarrmann
