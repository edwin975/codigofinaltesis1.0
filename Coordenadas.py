
def coord():

    directorio = "/home/pi/fotos/coordenadas.txt"

    archivo = open(directorio, "r")
    Data = archivo.read()
    archivo.close()

    cont = -1
    coma = 0

    for i in Data:
        cont += 1
        if i == '\n':
            pos = cont
        if i == ".":
            Data = Data[pos+1:]
            cont = -1
            break

    Latitud = []
    Longitud = []

    Datos = Data

    for i in Data:

        if i == ",":
            la = float(Datos[0:cont+1])
            Latitud.append(la)
            pos = cont+1                                       # Guarda la posicion donde empieza la coordenada Longitud
            coma = 1

        if (i == "\n") and (coma == 1):           # Si previamente no encontro latitud, entonces no debe buscar longitud
            lo = float(Datos[pos+1:cont+1])
            Longitud.append(lo)
            Datos = Datos[cont+2:]
            cont = -1
            coma = 0
        else:
            cont += 1

    return Latitud, Longitud
    

