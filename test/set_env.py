import os

os.environ.setdefault("test", 'hello')

def tt():
    print(os.environ.get("test"))