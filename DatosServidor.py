
def obtener():

    directorio = "/home/pi/fotos/DatosReceptor.txt"

    archivo = open(directorio, "r")
    Data = archivo.read()
    archivo.close()
    Datos = []
    cont = puntos = -1
    for i in Data:
        cont += 1
        if i == ':':
            pos = cont
            puntos = 1
        if (i == '\n') and (puntos == 1):
            Datos.append(Data[pos+1:cont])
            puntos = 0

    Info = []
    for j in Datos:
        lista = list(j)
        cont = 0
        aux = list(lista)
        for i in aux:
            if i == chr(32):
                cont += 1
                lista.remove(chr(32))
        lista = "".join(lista)
        Info.append(lista)

    return Info[0], Info[1], Info[2]






