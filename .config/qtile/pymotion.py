from Pyro5.api import Proxy

def pymotion():
    pymotion = Proxy("PYRO:pymotion@0.0.0.0:9090")
    pymotion.move()
    del pymotion

pymotion()
