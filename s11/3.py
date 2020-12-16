# Librerias
import random
dicc = {
    'temperatura': random.randrange(30),
    'humedad': random.randrange(100),
    'luz': random.randrange(100),
    'movimiento': bool(random.getrandbits(1))
}


def printDicc(nombre, valor):
    print("El sensor " + nombre + " tiene el valor " + str(valor))


for i in dicc:
    printDicc(i, dicc[i])
