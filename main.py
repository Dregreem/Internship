import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- 1. AYARLAR VE DEV HEDEF LİSTESİ (55+ Şirket) ---
URL_LISTESI = [
    # --- 🇹🇷 TÜBİTAK VE AR-GE ENSTİTÜLERİ ---
    {"url": "https://kariyer.tubitak.gov.tr/giris.htm", "sirket": "TÜBİTAK Kariyer Portalı"},
    {"url": "https://sage.tubitak.gov.tr/tr/duyurular", "sirket": "TÜBİTAK SAGE"},
    {"url": "https://bilgem.tubitak.gov.tr/tr/kariyer", "sirket": "TÜBİTAK BİLGEM"},
    {"url": "https://uzay.tubitak.gov.tr/tr/duyurular", "sirket": "TÜBİTAK UZAY"},
    {"url": "https://mam.tubitak.gov.tr/tr/duyurular", "sirket": "TÜBİTAK MAM"},
    {"url": "https://rute.tubitak.gov.tr/tr/duyurular", "sirket": "TÜBİTAK RUTE"},

    # --- 🛡️ SAVUNMA VE HAVACILIK ---
    {"url": "https://www.baykartech.com/tr/kariyer/acik-pozisyonlar/", "sirket": "Baykar"},
    {"url": "https://kariyer.tusas.com/ilanlar", "sirket": "TUSAŞ (TAI)"},
    {"url": "https://www.aselsan.com/tr/kariyer/acik-pozisyonlar", "sirket": "Aselsan"},
    {"url": "https://ik.roketsan.com.tr/", "sirket": "Roketsan"},
    {"url": "https://kariyer.havelsan.com.tr/", "sirket": "Havelsan"},
    {"url": "https://www.tei.com.tr/kariyer/acik-pozisyonlar", "sirket": "TEI (Motor Sanayi)"},
    {"url": "https://www.stm.com.tr/tr/kariyer/acik-pozisyonlar", "sirket": "STM Savunma"},
    {"url": "https://www.fnss.com.tr/kariyer/acik-pozisyonlar", "sirket": "FNSS"},
    {"url": "https://www.otokar.com.tr/kariyer", "sirket": "Otokar Savunma"},
    {"url": "https://www.bmc.com.tr/kariyer", "sirket": "BMC"},
    {"url": "https://www.katmerciler.com.tr/TR/Kariyer", "sirket": "Katmerciler"},
    {"url": "https://www.kale.com.tr/kariyer", "sirket": "Kale Havacılık"},
    {"url": "https://turksh.com.tr/kariyer", "sirket": "TUSAŞ Sistem Helikopter"},
    {"url": "https://turkhizy.com/kariyer/", "sirket": "THY Teknik"},

    # --- 🚗 OTOMOTİV ---
    {"url": "https://www.togg.com.tr/content/kariyer", "sirket": "Togg"},
    {"url": "https://live.fordotosan.com.tr/kariyer", "sirket": "Ford Otosan"},
    {"url": "https://kariyer.mercedes-benz.com.tr/", "sirket": "Mercedes-Benz Türk"},
    {"url": "https://tr.toyota.com.tr/pages/insan-kaynaklari", "sirket": "Toyota Türkiye"},
    {"url": "https://tofas.com.tr/kariyer", "sirket": "Tofaş"},
    {"url": "https://www.renault.com.tr/renault-dunyasi/insan-kaynaklari.html", "sirket": "Renault Mais"},
    {"url": "https://www.man.com.tr/kariyer", "sirket": "MAN Türkiye"},
    {"url": "https://www.turktraktor.com.tr/insan-kaynaklari/acik-pozisyonlar", "sirket": "Türk Traktör"},
    {"url": "https://www.karsan.com/tr/insan-kaynaklari/kariyer-firsatlari", "sirket": "Karsan"},
    {"url": "https://www.anadoluisuzu.com.tr/kariyer", "sirket": "Anadolu Isuzu"},

    # --- 🤖 ROBOTİK, OTOMASYON VE ENERJİ ---
    {"url": "https://jobs.siemens.com/careers?location=Turkey", "sirket": "Siemens Türkiye"},
    {"url": "https://www.se.com/tr/tr/about-us/careers/job-opportunities.jsp", "sirket": "Schneider Electric TR"},
    {"url": "https://altinay.com/kariyer/", "sirket": "Altınay Robot Teknolojileri"},
    {"url": "https://kontrolmatik.com/kariyer", "sirket": "Kontrolmatik"},
    {"url": "https://www.hktm.com.tr/kariyer", "sirket": "HKTM (Hidropar)"},
    {"url": "https://enerjisa.com.tr/kariyer", "sirket": "Enerjisa Üretim"},
    {"url": "https://www.tupras.com.tr/kariyer", "sirket": "Tüpraş"},
    {"url": "https://www.petkim.com.tr/kariyer", "sirket": "Petkim"},

    # --- 🚜 İŞ MAKİNELERİ VE AĞIR SANAYİ ---
    {"url": "https://www.hidromek.com.tr/tr/insan-kaynaklari", "sirket": "Hidromek"},
    {"url": "https://www.sanko.com.tr/kariyer", "sirket": "Sanko Makina (MST)"},
    {"url": "https://www.caterpillar.com/en/careers/search-jobs.html", "sirket": "Caterpillar (Borusan Cat)"},

    # --- 🍫 HIZLI TÜKETİM VE GIDA ---
    {"url": "https://cci.com.tr/tr/kariyer/kariyer-firsatlari", "sirket": "Coca-Cola İçecek"},
    {"url": "https://www.eti.com.tr/insan-kaynaklari", "sirket": "Eti"},
    {"url": "https://www.ulker.com.tr/tr/insan-kaynaklari", "sirket": "Ülker (Pladis)"},
    {"url": "https://www.unilever.com.tr/careers/", "sirket": "Unilever Türkiye"},
    {"url": "https://www.pmi.com/careers/explore-our-job-opportunities", "sirket": "Philip Morris (PML)"},
    {"url": "https://tr.pg.com/kariyer/", "sirket": "P&G Türkiye"},

    # --- 🧬 SAĞLIK VE TEKNOLOJİ ---
    {"url": "https://www.meteksan.com/tr/kariyer/acik-pozisyonlar", "sirket": "Meteksan"},
    {"url": "https://www.abdiibrahim.com.tr/kariyer/is-ilanlari", "sirket": "Abdi İbrahim"},
    {"url": "https://www.gehealthcare.com.tr/hakkimizda/kariyer", "sirket": "GE HealthCare"},
    
    # --- ⚙️ BEYAZ EŞYA VE AĞIR SANAYİ ---
    {"url": "https://www.arcelik.com.tr/kariyer", "sirket": "Arçelik"},
    {"url": "https://www.vestel.com.tr/kariyer", "sirket": "Vestel"},
    {"url": "https://www.bsheverri.com/tr/", "sirket": "BSH (Bosch Siemens)"},
    {"url": "https://www.erdemir.com.tr/kariyer/", "sirket": "Erdemir"},
    {"url": "https://sisecam.com.tr/tr/kariyer", "sirket": "Şişecam"},
]

# --- 2. TARAMA PARAMETRELERİ ---
ARANACAK_KELIMELER = [
    "staj", "intern", "part-time", "yarı zamanlı", 
    "aday mühendis", "uzun dönem", "kısa dönem", 
    "student", "werkstudent", "trainee", "yetenek"
]

# GitHub Secrets
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# --- 3. FONKSİYONLAR ---
def telegram_gonder(mesaj):
    if not TOKEN or not CHAT_ID:
        return
    
    # Telegram mesaj limiti (4096 karakter) kontrolü
    if len(mesaj) > 4000:
        mesaj = mesaj[:4000] + "\n... (Devamı kırpıldı)"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown", "disable_web_page_preview": True}
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Hatası: {e}")

def tarayiciyi_baslat():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Arayüzsüz mod (Sunucular için şart)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    # Gerçek kullanıcı gibi görünmek için User-Agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def main():
    print(f"🚀 Selenium motoru çalıştırılıyor... ({len(URL_LISTESI)} Dev Şirket)")
    
    driver = None
    try:
        driver = tarayiciyi_baslat()
    except Exception as e:
        print(f"❌ Tarayıcı başlatılamadı: {e}")
        return

    bulunanlar = []

    for i, hedef in enumerate(URL_LISTESI, 1):
        print(f"[{i}/{len(URL_LISTESI)}] {hedef['sirket']}...", end=" ", flush=True)
        try:
            driver.get(hedef["url"])
            # JavaScript'in yüklenmesi ve sitenin oturması için bekleme süresi
            time.sleep(3) 
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            metin = soup.get_text().lower().replace('i̇', 'i').replace('ı', 'i')
            
            kelime_bulundu = False
            for kelime in ARANACAK_KELIMELER:
                if kelime in metin:
                    bulunanlar.append(f"✅ **{hedef['sirket']}** ({kelime})\n🔗 {hedef['url']}")
                    print(f"--> BULUNDU! ({kelime})")
                    kelime_bulundu = True
                    break
            
            if not kelime_bulundu:
                print("Temiz.")
            
        except Exception as e:
            print(f"❌ Hata: {str(e)[:100]}") # Hatayı kısaltarak göster

    if driver:
        driver.quit()

    if bulunanlar:
        baslik = f"📢 **GELİŞMİŞ STAJ RAPORU ({len(bulunanlar)} İlan)**\n\n"
        icerik = "\n\n".join(bulunanlar)
        telegram_gonder(baslik + icerik)
        print("✅ Rapor Telegram'a gönderildi.")
    else:
        print("❌ Yeni ilan bulunamadı.")

if __name__ == "__main__":
    main()
