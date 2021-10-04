import sys
import socket
import ujson
import ussl
import epd5in65f

class Http:
    def socket_connect(self, method, url, data):
        try:
            _, _, host, path = url.split('/', 3)
            addr = socket.getaddrinfo(host, 443, 0, socket.SOCK_STREAM)[0]
            self.s = socket.socket(addr[0], addr[1], addr[2])
            self.s.connect(addr[-1])
            self.s = ussl.wrap_socket(s, server_hostname=host)
            self.s.write(b'%s /%s HTTP/1.1\r\n' % (method, path))
            self.s.write(b'Host: %s\r\n' % host)
            self.s.write(b'Content-Type: application/x-www-form-urlencoded\r\n')
            if data:
                self.s.write(b'Content-Length: %d\r\n' % len(data))
            self.s.write(b"\r\n")
            self.s.write(data)
        except:
            print('can\'t connect socket')
            sys.exit()
    
    def get_header(self):
        try:
            self.response = Response()
            header = []
            l = self.s.readline()
            header.append(l)
            summary = l.split(None, 2)
            self.response.status = int(summary[1])
            self.response.reason = ''
            if len(l) > 2:
                self.response.reason = summary[2].rstrip()
            while True:
                l = self.s.readline()
                if l != b'\r\n':
                    header.append(l)
                else:
                    break
        except:
            print('can\'t get header')
    
    def display(self, epd):
        try:
            epd.read_send_data(self.s, 30000)
        except OSError:
            self.s.close()
            raise

class Response:
    status = None
    reason = None

def run():
    epd = epd5in65f.EPD()
    epd.init()
    epd.Clear()
    data = {}

    f = open('token.json', 'r')
    data['access_token'] = ujson.load(f)
    f.close()

    f = open('config.json', 'r')
    data['config'] = ujson.load(f)
    f.close()

    url = 'https://e-indicator-api.herokuapp.com/'
    http = Http()
    http.socket_connect('POST', url, ujson.dumps(data).encode('utf-8'))
    http.get_header()
    http.display(epd)

    print(http.response.status, http.response.reason)

if __name__ == '__main__':
    run()