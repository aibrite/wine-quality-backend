from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
from quality import WineQuality
import json
import os


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = parse.urlparse(self.path)

        message_parts = [
            'CLIENT VALUES:',
            'client_address={} ({})'.format(
                self.client_address,
                self.address_string()),
            'command={}'.format(self.command),
            'path={}'.format(self.path),
            'real path={}'.format(parsed_path.path),
            'query={}'.format(parsed_path.query),
            'request_version={}'.format(self.request_version),
            '',
            'SERVER VALUES:',
            'server_version={}'.format(self.server_version),
            'sys_version={}'.format(self.sys_version),
            'protocol_version={}'.format(self.protocol_version),
            '',
            'HEADERS RECEIVED:',
        ]

        for name, value in sorted(self.headers.items()):
            message_parts.append(
                '{}={}'.format(name, value.rstrip())
            )
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

    def do_POST(self):
        length = int(self.headers['Content-Length'])

        quality_calculator = WineQuality()
        params = parse.parse_qs(
            self.rfile.read(length).decode('utf-8'))

        data = []
        for key in params:
            print(params[key])
            data.append(int(params[key][0]))
        try:
            quality = quality_calculator.estimate_quality(data)
            print(quality)
            self.send_response(200)
            self.send_header('Content-Type',
                             'text/html; charset=utf-8')
            self.end_headers()

            self.wfile.write(quality[0])

        except TypeError as e:
            self.send_error(500, message=None, explain=e.args[0])
        except ValueError as e:
            self.send_error(500, message=None, explain=e.args[0])
        except IOError as e:
            self.send_error(500, message=None, explain=e.args[0])
        except Exception as e:
            self.send_error(500, message=None, explain=e.args[0])
        else:
            print('Server response sent.')


class WineServer:

    def run_server(self):
        print('Starting server...')
        if __name__ == 'wineserver':
            server_address = 'https://wine-quality.herokuapp.com/'
            server_port = int(os.environ.get('PORT', 5000))
            server = HTTPServer((server_address, server_port), RequestHandler)
            print('Server started, use <Ctrl-C> to stop')
            server.serve_forever()
