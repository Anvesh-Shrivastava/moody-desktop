import os
from itertools import cycle
curr_dir = os.path.dirname(os.path.abspath(__file__))
url = "https://api.unsplash.com/"
cl_id = [""]
id_iter = cycle(cl_id)

def client_id():
    return next(id_iter)
