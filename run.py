import vimport

import requests

req = __import__("requests", globals(), locals(), [], 0)
req19 = __import__("requests@2_19_1", globals(), locals(), [], 0)
req25 = __import__("requests@2_25_0", globals(), locals(), [], 0)

req19.__version__
req19.__path__
httperror = __import__("requests@2_19_1.HTTPError", globals(), locals(), [], 0)

assert req25 != req19
assert req25.__version__ != req19.__version__
assert req25.HTTPError == req19.HTTPError
