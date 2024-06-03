import asyncio
import sys
from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu

async def echo_client_proto(scope, conn: EchoQuicConnection):
    while True:
        print("Enter operation (upload/download/list directory/rename/delete/exit):")
        operation = input().lower()

        if operation == 'exit':
            print("Exiting the client.")
            break
########################################## Upload ####################################################
        elif operation == 'upload':
            print("Enter file path to be uploaded to the server:")
            file_path = input()
            with open(file_path, 'r') as file:
                file_content = file.read()
            file_datagram = pdu.Datagram(pdu.MSG_TYPE_DATA, file_content)
            new_stream_id = conn.new_stream()
            qs = QuicStreamEvent(new_stream_id, file_datagram.to_bytes(), True)
            await conn.send(qs)
            print(f'[cli] file uploaded: {file_path}')

########################################## Download ####################################################
        elif operation == 'download':
            print("Enter file name to download from server:")
            file_name = input()
            file_request = pdu.Datagram(pdu.MSG_TYPE_FILE, file_name)
            new_stream_id = conn.new_stream()
            qs = QuicStreamEvent(new_stream_id, file_request.to_bytes(), False)
            await conn.send(qs)
            message: QuicStreamEvent = await conn.receive()
            file_data = pdu.Datagram.from_bytes(message.data)
            with open('received_' + file_name, 'w') as file:
                file.write(file_data.msg)
            print(f'[cli] received file: {file_name}')

########################################## List Directory ###############################################
        elif operation == 'list directory':
            dir_request = pdu.Datagram(pdu.MSG_TYPE_DIR_LIST, "List Directory")
            new_stream_id = conn.new_stream()
            qs = QuicStreamEvent(new_stream_id, dir_request.to_bytes(), False)
            await conn.send(qs)
            message: QuicStreamEvent = await conn.receive()
            dir_list = pdu.Datagram.from_bytes(message.data)
            print(f"[cli] Directory Content:\n{dir_list.msg}")

########################################## Rename ####################################################
        elif operation == 'rename':
            print("Enter current file name:")
            old_file_name = input()
            print("Enter new file name:")
            new_file_name = input()
            rename_request = pdu.Datagram(pdu.MSG_TYPE_RENAME, old_file_name + ';' + new_file_name)
            new_stream_id = conn.new_stream()
            qs = QuicStreamEvent(new_stream_id, rename_request.to_bytes(), False)
            await conn.send(qs)
            message: QuicStreamEvent = await conn.receive()
            response = pdu.Datagram.from_bytes(message.data)
            print(f"[cli] Rename Response: {response.msg}")

########################################## Delete ####################################################
        elif operation == 'delete':
            print("Enter file name to delete:")
            file_name = input()
            delete_request = pdu.Datagram(pdu.MSG_TYPE_DELETE, file_name)
            new_stream_id = conn.new_stream()
            qs = QuicStreamEvent(new_stream_id, delete_request.to_bytes(), False)
            await conn.send(qs)
            message: QuicStreamEvent = await conn.receive()
            response = pdu.Datagram.from_bytes(message.data)
            print(f"[cli] Delete Response: {response.msg}")
