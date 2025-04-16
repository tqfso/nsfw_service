
class Code:
    SUCCESS = 0
    FAILURE = 1
    UNKNOWN = 2
    FILE_NOT_FOUND = 3

class Error(Exception):
    def __init__(self, code = 0, msg = None):
        super().__init__()
        self._code = code
        self._msg = msg

    def __str__(self) -> str:
        return f'code: {self._code} msg: {self._msg}'

    @property
    def code(self):
        return self._code

    @property
    def msg(self):
        return self._msg