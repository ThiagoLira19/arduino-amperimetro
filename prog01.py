import serial
import json
import time

porta = 'COM4'
baud_rate = 9600

Obj_porta = serial.Serial(porta, baud_rate)

def remove_caracteres(linha):
    result = linha[2:(len(linha)-5)]
    return result
    
cont_expurgo = 0
cont_segundos = 0
soma_watts_min = 0
media_watts_min = 0
preco_kw_minuto = 0.754/60
total_consumido = 0
tempo_total_min = 0

print("Calibrando, por favor aguarde um momento...")
while tempo_total_min < 30:
    cont_expurgo += 1
    linha = str(Obj_porta.readline())
    if cont_expurgo > 10:
        linha = remove_caracteres(linha)
        linha_json = json.loads(linha)
        cont_segundos += 1
        c = float(linha_json["Corrente"])-0.12
        potencia_real = c * 127
        soma_watts_min += potencia_real
        print(f"Corrente: {c:.2f} A | Potência: {potencia_real:.2f} watts")
        if cont_segundos > 60:
            media_watts_min = soma_watts_min/60
            soma_watts_min = 0
            cont_segundos = 0
            total_consumido += (media_watts_min/1000)*preco_kw_minuto
            tempo_total_min += 1
    time.sleep(0.1)

h = int(tempo_total_min / 60)
m = int(tempo_total_min - (h * 60))

print(f"O total gasto foi de: R$ {total_consumido:.2f}")
print(f"O tempo total de medição foi de: {h}:{m}")