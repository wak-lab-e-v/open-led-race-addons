#!/usr/bin/python3
 
import serial
import serial.tools.list_ports as port_list
import time
import os


def OuputHex(byes):
    # using join() + format() 
    # Converting bytearray to hexadecimal string 
    return str(''.join(format(x, '02x')+' ' for x in byes))+byes.decode()

def raceHandshake():
        Code = "#"
        ser.write((Code+"\n").encode())
        Code = "?" # Get Software Id (Type)
        ser.write((Code+"\n").encode())
        Code = "%" # Software Version
        ser.write((Code+"\n").encode())

def raceConfiguration(start,nlap,repeat,finish):
        Code = "C%d,%d,%d,%d" % (start,nlap,repeat,finish)
        ser.write((Code+"\n").encode())

def raceParameters():
        ser.write(("Q\n").encode())

def raceWriteEEPROM():
        ser.write(("W\n").encode())

def raceEnterConfigurationMode():
        Code = "@" # Software Version
        ser.write((Code+"\n").encode())


def raceTracklengthConfiguration(nrLEDs):
        Code = "T%d" % (nrLEDs)
        ser.write((Code+"\n").encode())

def raceBoxLengthConfiguration():
        Code = "B%d" % (nrLEDs)
        ser.write((Code+"\n").encode())

def raceRampConfiguration(start,center,end,high=6,perm=1):
        Code = "A%d,%d,%d,%d,%d" % (start,center,end,high,perm)
        ser.write((Code+"\n").encode())

def raceWeightFrictionConfiguration(Weight=0.006, Frictions=0.015):
        if Weight > 1.999:
                Weight = 1.999
        if Frictions > 1.999:
                Frictions = 1.999        
        Code = "K%.3f,%.3f" % (Weight,Frictions)
        ser.write((Code+"\n").encode())
        

# Verfügbare Serielle Ports
ports = list(port_list.comports())
print(ports[0].device)
#port = ports[0].device
 
# Seriellen Port Konfigurieren:
ser = serial.Serial()
# Hier den passenden Port angeben
ser.port = 'COM15' if os.name=='nt' else '/dev/ttyACM0'
ser.baudrate = 115200
ser.timeout = 1
 
# Port öffnen
ser.open()
print("Port geöffnet")
time.sleep(3)

raceHandshake()
raceParameters()
raceConfiguration(1,4,1,1)
raceRampConfiguration(75,80,85,high=1,perm=1)
raceWeightFrictionConfiguration(0.005, 0.014)
raceTracklengthConfiguration(1200)
raceWriteEEPROM()
#
#raceEnterConfigurationMode()

try:
    while 1:
        # Zeile als Bytestring einlesen und
        # mit decode in normalen string konvertieren.
        string = ser.readline()
        try:
            string = string.decode()
            print(string)
        except:
            print("Decodierungsfehler")

            
# Keyboard Interrupt abfangen, zum beenden mit [STRG]+[C].
except(KeyboardInterrupt, SystemExit):
    print("\nWird Beendet:")
    ser.close()
    print("Com Port geschlossen!")
    print("\nENDE")
