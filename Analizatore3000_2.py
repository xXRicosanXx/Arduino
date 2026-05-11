import serial
import requests
import time
 
# 🔧 CONFIGURAZIONE
TOKEN = "8714534127:AAGNDatK7Xlw_YRmYshj4R2F4LTixMeU6Hs"
CHAT_ID = "6746242719"
PORTA_SERIALE = "COM7"   # cambia con la tua porta
BAUDRATE = 9600
 
def invia_messaggio(testo):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": testo})
 
ser = serial.Serial(PORTA_SERIALE, BAUDRATE, timeout=1)
 
print("In ascolto...")
 
ultimo_stato = None
 
while True:
    linea = ser.readline().decode('utf-8', errors='ignore').strip()
 
    if linea:
        print("Ricevuto:", linea)
 
        # prende solo i numeri anche se c'è testo
        numeri = ''.join(filter(str.isdigit, linea))
 
        if numeri == "":
            continue
 
        valore = int(numeri)
 
        # logica stati
        if valore > 210:
            stato = "PERICOLO"
        elif valore > 85:
            stato = "ATTENZIONE"
        else:
            stato = "SICURO"
 
        # invia solo se cambia stato (NO SPAM)
        if stato != ultimo_stato:
            ultimo_stato = stato
 
            if stato == "PERICOLO":
                invia_messaggio(f"🚨 PERICOLO GAS: {valore} ppm, se fossi in te cambierei aria -- attivazione ventilazione")
            elif stato == "ATTENZIONE":
                invia_messaggio(f"⚠️ Attenzione gas: {valore} ppm")
            else:
                invia_messaggio(f"✅ Gas sicuro: {valore} ppm")
 
            print("Messaggio inviato:", stato)
 
            time.sleep(2)  # evita blocchi Telegram