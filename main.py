import os
import datetime
import time
from dotenv import load_dotenv
import pywhatkit
import logging

# Çevresel değişkenleri yükle
load_dotenv()

# Çevresel değişkenlerden bilgileri al
to_number = os.getenv("TO_NUMBER")
msg = os.getenv("MESSAGE")
send_time = os.getenv("SEND_TIME", "17:53")  # Eğer `SEND_TIME` boşsa "17:53" olarak ayarla

# Saat ve dakika olarak ayrıştır
send_time_hour = int(send_time.split(":")[0])
send_time_minute = int(send_time.split(":")[1])

# Logging yapılandırması
logging.basicConfig(filename="message_sender.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Gönderim zamanı ve tarih bilgileri
def get_next_send_time():
    send_time = datetime.datetime.now().replace(hour=send_time_hour, minute=send_time_minute, second=0, microsecond=0)
    if send_time <= datetime.datetime.now():
        # Bugünün saatini geçtiyse yarına ayarla
        send_time += datetime.timedelta(days=1)
    return send_time

# Mesaj gönderme fonksiyonu
def send_message():
    try:
        # Mevcut saatten 5 dakika sonrasına göre gönderim ayarla
        pywhatkit.sendwhatmsg_instantly(to_number, msg, wait_time=15)
        logging.info(f"Mesaj başarıyla gönderildi: {msg} - {to_number}")
        print("Mesaj gönderildi.")
    except Exception as e:
        logging.error(f"Mesaj gönderilemedi: {e}")
        print(f"Mesaj gönderme hatası: {e}")

# Döngüye durma koşulu ekleyerek mesajı gönder
next_send_time = get_next_send_time()
while True:
    now = datetime.datetime.now()
    if now >= next_send_time:
        send_message()
        next_send_time = get_next_send_time()  # Bir sonraki gün aynı saate ayarla
    time.sleep(60)  # Her dakika bir kez kontrol et
