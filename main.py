from wineserver import WineServer


def run():
    if __name__ == '__main__':
        print('Running on', __name__)
        server = WineServer()
        server.run_server()


run()
