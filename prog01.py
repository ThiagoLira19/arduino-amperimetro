# importaçoes de libs
import serial
import json
import time

# Indica a porta onde está conectado o arduíno
porta = 'COM6'
# Indica a taxa de transmissão da porta
baud_rate = 9600
# Cria o objeto instânciado com a leitura dos dados da porta
Obj_porta = serial.Serial(porta, baud_rate)

# Função que remove os caracteres indesejados e limpa a string dos dados lidos
def remove_caracteres(linha):
    result = linha[2:(len(linha)-5)]
    return result

# Variáveis que serão usadas nos calculos
cont_expurgo = 0                # Contador de iterações que serão expurgadas dos calculos
cont_segundos = 0               # Contador de segundos decorridos              
soma_watts_min = 0              # Acumulador de watts lidos por minutos
media_watts_min = 0             # Média dos watts lidos no acumulador de watts por minutos
preco_kw_minuto = 0.754/60      # Preço do kwh por minuto
total_consumido = 0             # Total consumido em Reais(R$)
tempo_total_min = 0             # Tempo total decorrido em segundos

# Tempo total que será executado a medição
tempo_de_medicao = 5

print("Calibrando, por favor aguarde um momento...")

# Tempo total que será executado a medição
tempo_de_medicao = 5

# Loop principal da execução do programa durante o tempo de medição
while tempo_total_min < tempo_de_medicao:
    # Conta o expurgo
    cont_expurgo += 1
    # Lê os dados da porta serial
    linha = str(Obj_porta.readline())
    # Executa após o expurgo das 10 primeiras leituras para calibração do sensor
    if cont_expurgo > 10:
        linha = remove_caracteres(linha)
        linha_json = json.loads(linha)      # Converte o texto em json
        cont_segundos += 1
        c = float(linha_json["Corrente"])       # Lê o valor da corrente
        if(c > 0.12):       # Aplica uma ajuste de margem de erro na leitura
            c = c - 0.12
        potencia_real = c * 127         # Calcula o valor da potência em watts
        soma_watts_min += potencia_real         # Acumula a potência por minutos
        print(f"Corrente: {c:.2f} A | Potência: {potencia_real:.2f} watts")
        # Executa após 60 segundos (1 minuto)
        if cont_segundos > 60:
            media_watts_min = soma_watts_min/60         # Calcula a média de watts em 1 minuto
            soma_watts_min = 0          # Zera o acumulador de watts depois de 1 minuto
            cont_segundos = 0           # Zera o contador de segundos depois de 1 minuto
            total_consumido += (media_watts_min/1000)*preco_kw_minuto       # Acumula o total consumido em Reais(R$) 
            tempo_total_min += 1
    time.sleep(0.1)         # Espera 1 segundo para executar novamente

# Converte o total de minutos decorridos em horas
h = int(tempo_total_min / 60)
m = int(tempo_total_min - (h * 60))

# Exibe a saída Final do programa
print(f"O total gasto foi de: R$ {total_consumido:.2f}")
print(f"O tempo total de medição foi de: {h}:{m}")