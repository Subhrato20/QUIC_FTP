# Echo Client-Server Application Using QUIC

This application demonstrates a client-server interaction using the QUIC protocol to perform operations such as uploading, downloading files, and listing directory contents. The application is built using Python and utilizes `aioquic` for QUIC communication.

## Requirements

- Python 3.7 or higher

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Subhrato20/QUIC_FTP.git
   ```
2. Install required Python libraries:
   ```
   pip3 install -r requirements.txt
   ```

## Directory Structure

- `echo_client.py` - Client script.
- `echo_server.py` - Server script.
- `echo.py` - Entry point script to run the client or server.
- `pdu.py` - Defines the Datagram class for message passing.
- `certs/` - Contains SSL/TLS certificates.


# Note

To run the file you have to add an absolute directory to serverdata (you have to make changes in the echo_server.py, I have highlighted it with comments).

# Demo Video
The link to demo is https://drive.google.com/file/d/1ZIrFIUT5J6Jb2tg0LZX1kJLPWP5CMkNW/view?usp=sharing


## Running the Server

To start the server, use the following command:

```
python3 echo.py server
```

## Running the Client

To run the client, use the following command:

```
python3 echo.py client

```
Then perform the required Operations

## Operations

- **Upload**: Sends a file to the server.
- **Download**: Requests a file from the server.
- **List Directory**: Requests a list of files available on the server directory.
- **Rename**: Renames a file on the server
- **Delete**: Deletes a file on the server 


