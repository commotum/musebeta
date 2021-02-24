class ReqMock:
    def __init__(self, method, get, body=''):
        self.method = method
        self.GET = get
        self.body = body.encode()
