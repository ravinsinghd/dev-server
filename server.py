import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)


def file_not_found():
    response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Fount'
    return response


def get_file_name(request):
    headers = request.split('\n')
    if not headers[0]:
        return None

    file_name = headers[0].split()[1]

    if file_name == '/':
        return '/index.html'
    else:
        return file_name


def read_file_content(file_name):
    try:
        fin = open('content'+file_name)
        content = fin.read()
        fin.close()
        return 'HTTP/1.0 200 OK\n\n' + content
    except FileNotFoundError:
        return file_not_found()


print('listening on port %s ...' % SERVER_PORT)

while True:
    print('still live')
    client_connection, client_address = server_socket.accept()
    request = client_connection.recv(1024).decode()
    file_name = get_file_name(request)

    if file_name:
        response = read_file_content(file_name)
    else:
        response = file_not_found()

    client_connection.sendall(response.encode())
    client_connection.close()

server_socket.close()
