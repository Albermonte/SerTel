# Diccionarios y Flujos

dicc = { 'temp': 22, 'luz': 136, 'humedad': 20}

for i in dicc:
    print(i + ' ' + str(dicc[i]))

print('----------------')

dicc.update({ 'movimiento': False })

dicc['temp'] = 25

for i in dicc:
    print(i + ' ' + str(dicc[i]))