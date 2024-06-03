import asyncio
from typing import Dict
import os
from echo_quic import EchoQuicConnection, QuicStreamEvent
import pdu

async def echo_server_proto(scope: Dict, conn: EchoQuicConnection):
    while True:
        message: QuicStreamEvent = await conn.receive()

        dgram_in = pdu.Datagram.from_bytes(message.data)

########################################## Download ####################################################
        if dgram_in.mtype == pdu.MSG_TYPE_FILE:

            file_path = os.path.join('/Users/subhratosom/Desktop/python/serverdata', dgram_in.msg) #Change it to '/yourfilepath/serverdata'
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    file_content = file.read()
                file_datagram = pdu.Datagram(pdu.MSG_TYPE_FILE, file_content)
                rsp_msg = file_datagram.to_bytes()
                rsp_evnt = QuicStreamEvent(message.stream_id, rsp_msg, True)
                await conn.send(rsp_evnt)
                print(f"[svr] sent file: {file_path}")
            else:
                error_msg = "Error: File not found"
                print("[svr] " + error_msg)
                error_datagram = pdu.Datagram(pdu.MSG_TYPE_ERROR, error_msg)
                error_bytes = error_datagram.to_bytes()
                rsp_evnt = QuicStreamEvent(message.stream_id, error_bytes, True)
                await conn.send(rsp_evnt)

########################################## Upload ####################################################
        elif dgram_in.mtype == pdu.MSG_TYPE_DATA:

            save_folder = '/Users/subhratosom/Desktop/python/serverdata' #Change it to '/yourfilepath/serverdata'
            file_path = os.path.join(save_folder, 'received_file.txt')
            with open(file_path, 'w') as file:
                file.write(dgram_in.msg)
            print(f"[svr] received file and saved to: {file_path}")
            ack_message = "File received successfully"
            dgram_out = pdu.Datagram(pdu.MSG_TYPE_DATA_ACK, ack_message)
            rsp_msg = dgram_out.to_bytes()
            rsp_evnt = QuicStreamEvent(message.stream_id, rsp_msg, True)
            await conn.send(rsp_evnt)

########################################## List Directory ###############################################
        elif dgram_in.mtype == pdu.MSG_TYPE_DIR_LIST:

            directory_path = '/Users/subhratosom/Desktop/python/serverdata' #Change it to '/yourfilepath/serverdata'
            try:
                files = os.listdir(directory_path)
                dgram_out = pdu.Datagram(pdu.MSG_TYPE_DIR_LIST, files)
                rsp_msg = dgram_out.to_bytes()
                rsp_evnt = QuicStreamEvent(message.stream_id, rsp_msg, True)
                await conn.send(rsp_evnt)
                print(f"[svr] sent directory listing: {files}")
            except OSError as e:
                file_list = "Error listing directory: " + str(e)
                print(f"[svr] {file_list}")
                dgram_out = pdu.Datagram(pdu.MSG_TYPE_ERROR, file_list)
                rsp_msg = dgram_out.to_bytes()
                rsp_evnt = QuicStreamEvent(message.stream_id, rsp_msg, True)
                await conn.send(rsp_evnt)

########################################## Rename ####################################################
        elif dgram_in.mtype == pdu.MSG_TYPE_RENAME:

            old_file_name, new_file_name = dgram_in.msg.split(';')
            old_file_path = os.path.join('/Users/subhratosom/Desktop/python/serverdata', old_file_name) #Change it to '/yourfilepath/serverdata'
            new_file_path = os.path.join('/Users/subhratosom/Desktop/python/serverdata', new_file_name) #Change it to '/yourfilepath/serverdata'
            try:
                os.rename(old_file_path, new_file_path)
                response_msg = f"File renamed successfully from {old_file_name} to {new_file_name}"
                print(f"[svr] {response_msg}")
                success_datagram = pdu.Datagram(pdu.MSG_TYPE_ACK, response_msg)
                success_bytes = success_datagram.to_bytes()
                rsp_evnt = QuicStreamEvent(message.stream_id, success_bytes, True)
                await conn.send(rsp_evnt)
            except OSError as e:
                error_msg = f"Error renaming file: {str(e)}"
                print("[svr] " + error_msg)
                error_datagram = pdu.Datagram(pdu.MSG_TYPE_ERROR, error_msg)
                error_bytes = error_datagram.to_bytes()
                rsp_evnt = QuicStreamEvent(message.stream_id, error_bytes, True)
                await conn.send(rsp_evnt)

########################################## Delete ####################################################
        elif dgram_in.mtype == pdu.MSG_TYPE_DELETE:
            # Delete
            file_path = os.path.join('/Users/subhratosom/Desktop/python/serverdata', dgram_in.msg) #Change it to '/yourfilepath/serverdata'
            try:
                os.remove(file_path)
                response_msg = f"File {dgram_in.msg} deleted successfully"
                print(f"[svr] {response_msg}")
                success_datagram = pdu.Datagram(pdu.MSG_TYPE_ACK, response_msg)
                success_bytes = success_datagram.to_bytes()
                rsp_evnt = QuicStreamEvent(message.stream_id, success_bytes, True)
                await conn.send(rsp_evnt)
            except OSError as e:
                error_msg = f"Error deleting file: {str(e)}"
                print("[svr] " + error_msg)
                error_datagram = pdu.Datagram(pdu.MSG_TYPE_ERROR, error_msg)
                error_bytes = error_datagram.to_bytes()
                rsp_evnt = QuicStreamEvent(message.stream_id, error_bytes, True)
                await conn.send(rsp_evnt)

        else:
            print("[svr] received message: ", dgram_in.msg)
            ack_message = "SVR-ACK: " + dgram_in.msg
            dgram_out = pdu.Datagram(dgram_in.mtype | pdu.MSG_TYPE_DATA_ACK, ack_message)
            rsp_msg = dgram_out.to_bytes()
            rsp_evnt = QuicStreamEvent(message.stream_id, rsp_msg, False)
            await conn.send(rsp_evnt)
