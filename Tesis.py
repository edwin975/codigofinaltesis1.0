#coding=utf-8

""" Prueba captura de imagen sincronizada con ruta """

import os
import picamera
import subprocess
import time
import threading
from gps import *

import samba
import Coordenadas
import DemoledorDeHilos
import DatosServidor

gpsd = None                                                                            # incializando la variable global
 
os.system('clear')

class GpsPoller(threading.Thread):

  def __init__(self):

    threading.Thread.__init__(self)
    global gpsd
    gpsd = gps(mode=WATCH_ENABLE)                                                    # iniciando el flujo de información
    self.current_value = None
    self.running = True                                                                     # Habilita el WHile del hilo
 
  def run(self):

    global gpsd
    while gpsp.running:
        gpsd.next()                                                                         # Contiene los datos del GPS
 
if __name__ == '__main__':

  gpsp = GpsPoller()                                                                                   # creando el hilo
  
  subprocess.call(["sudo", "gpsd", "/dev/ttyS0", "-F", "/var/run/gpsd.sock"])                           # Arranca el GPS

  a = os.getpid()                                                                       # Devuelve el codigo del proceso
  b = str(a)

  try:

    gpsp.start()                                                                                        # Inicia el hilo

    i = cont1 = reset = tomadas = cont = 0

    LimLa,  LimLo = Coordenadas.coord()                     # Devuelve las coordenadas ingresadas en el archivo de texto

    numpuntos = len(LimLa)
    error = 5e-5

    while True:

      os.system('clear')
      print("\n GPS reading")
      print("---------------------------------------------------------")
      print("latitude    ", gpsd.fix.latitude)
      print("longitude   ", gpsd.fix.longitude)
      print("time utc    ", gpsd.utc," + ", gpsd.fix.time)
      print("altitude (m)", gpsd.fix.altitude)
      print("eps         ", gpsd.fix.eps)
      print("epx         ", gpsd.fix.epx)
      print("epv         ", gpsd.fix.epv)
      print("ept         ", gpsd.fix.ept)
      print("speed (m/s) ", gpsd.fix.speed)
      print("climb       ", gpsd.fix.climb)
      print("track       ", gpsd.fix.track)
      print("mode        ", gpsd.fix.mode)
      print("\nsats        ", gpsd.satellites)

      i = i+1

      if (i>=2) and tomadas == 0:

          for c in range(numpuntos):

            if (LimLa[c]-error<gpsd.fix.latitude<LimLa[c]+error) and (LimLo[c]-error<gpsd.fix.longitude<LimLo[c]+error):

                tomadas = 1
                pos = c                                             # guarda la posicion donde encuentra un coincidencia
                Latitud = str(gpsd.fix.latitude)
                Longitud = str(gpsd.fix.longitude)
                d = "-exif:gpslatitude="
                Latitud = d + Latitud
                d = "-exif:gpslongitude="
                Longitud = d + Longitud
                Altitud = str(gpsd.fix.altitude)
                d = "-exif:gpsaltitude="
                Altitud = d + Altitud

                with picamera.PiCamera() as picam:
                    picam.start_preview()
                    time.sleep(1)
                    print ("TOMADA")
                    num = str(cont+1)
                    nombre = "/home/pi/fotos/foto" + num + ".jpg"
                    picam.capture(nombre)
                    picam.stop_preview()
                    subprocess.call(["exiftool", Latitud, "-exif:gpslatituderef=S", Longitud, "-exif:gpslongituderef=E", Altitud, "-overwrite_original", nombre])
                    picam.close()

                if cont == numpuntos-1:
                    cont = 0
                    reset = 1
                else:
                    cont = cont + 1
                    reset = 0

                break                                           # Una vez encuentra una coincidencia, rompe el ciclo for

      else:

          EvaluarLa = LimLa[pos] - error < gpsd.fix.latitude < LimLa[pos] + error    # Latitud fija hasta siguiente zona
          EvaluarLo = LimLo[pos] - error < gpsd.fix.longitude < LimLo[pos] + error  # Longitud fija hasta siguiente zona

          if ((cont >= 1) or (reset == 1)) and not((EvaluarLa) and (EvaluarLo)):          # Entra si se sale zona fijada

              cont1 = cont1+1
              ubicacion = "/home/pi/fotos/ubicacion"+str(cont1)+".txt"
              data = open(ubicacion, "a")
              data.write("Se salió de la zona %s \n" % cont1)
              data.close()
              tomadas = 0                                                   # Habilita la busqueda de una nueva zona

              if reset == 1:
                  cont1 = 0
                  DemoledorDeHilos.Matar()    # Cancela todos los hilos una vez que haya tomado fotos en todas las zonas

  except (KeyboardInterrupt, SystemExit):

    print("\n")
    gpsp.running = False
    gpsp.join()                                                      # Espera a que el hilo termine lo que este haciendo

  print("Iniciando conexion con servidor...\n")

  us,pas,ip = DatosServidor.obtener()                                   # Devuelve usuario, contraseña e ip del servidor

  try:
      while True:

          Conexion = samba.mount(us, pas, ip)

          if Conexion == 0:
              print("Intentando conexion...")
          else:
              print("Conexion establecida")
              time.sleep(1)
              DemoledorDeHilos.Matar()       # Cancela todos los hilos cuando se logre conexion entre cliente y servidor

  except:

      print("\nFinalizando proceso samba\n")

  for i in range(numpuntos):                                                               # Envia las fotos al servidor
      nombrefoto = "/home/pi/fotos/foto"+str(i+1)+".jpg"
      subprocess.call(["mv", nombrefoto, "/home/pi/compartir"])
  print("Trasferencia completa")
  subprocess.call(["sudo", "umount", "/home/pi/compartir"])                                     # Desconecta el servidor



