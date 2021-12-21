
def Matar ():

    import os
    import subprocess

    b = str(os.getpid())

    subprocess.call(["kill", "-2", b])