import serial
import requests
import time
import msvcrt
 
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
 
def Arduino3000():
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            if key.lower() == 'p':
                print("Tasto 'p' premuto: uscita dal programma...")
                break

        linea = ser.readline().decode('utf-8', errors='ignore').strip()
    
        if linea:
            print("Ricevuto:", linea)
    
            #Quetsa stringa ci permette di estrarre solo i numeri ignorando le string (quelle date da arduino: in particolare la strina "Dati Gas:")        
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
    
            # questa parte di codice ci permette di evitare lo spam inviando il messaggio solo quando lo stato cambia
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


if __name__ == "__main__":
    try:
        Arduino3000()
    except KeyboardInterrupt:
        print("Chiusura programma...")
    finally:
        ser.close()