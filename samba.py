"""Prueba montaje de SAMBA"""
def mount (us, pas, ip):

    import subprocess

    a = "username="+us+",password="+pas
    b = "//"+ip+"/compartir"

    subprocess.call (["sudo", "mount", "-t", "cifs", "-o",a,b, "/home/pi/compartir"])
    subprocess.call (["sudo", "touch", "/home/pi/compartir/conectado.txt"])

    dato = open("/home/pi/compartir/archivo.txt", "r")
    desicion = int(dato.read())
    dato.close()

    return desicion




