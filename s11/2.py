# Funciones
dicc = {'temp': 22, 'luz': 136, 'humedad': 20}


def printDicc(nombre, valor):
    print("El sensor " + nombre + " tiene el valor " + str(valor))


for i in dicc:
    printDicc(i, dicc[i])
