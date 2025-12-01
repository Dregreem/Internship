import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException

# --- 1. AYARLAR ---
ARANACAK_KELIMELER = [
    "staj", "intern", "part-time", "yarı zamanlı", 
    "aday mühendis", "uzun dönem", "kısa dönem", 
    "student", "werkstudent", "trainee", "yetenek"
]

NEGATIF_KELIMELER = [
    "sona erdi", "sona ermiştir", "başvurular tamamlandı", 
    "kapandı", "kapanmıştır", "no longer accepting", "closed", 
    "süresi doldu", "yayından kaldırıldı",
    "2023", "2024" 
]

# --- HEDEF LİSTESİ ---
URL_LISTESI = [
    {"url": "https://kariyer.tubitak.gov.tr/giris.htm", "sirket": "TÜBİTAK Kariyer"},
    {"url": "https://sage.tubitak.gov.tr/tr/duyurular", "sirket": "TÜBİTAK SAGE"},
    {"url": "https://bilgem.tubitak.gov.tr/tr/kariyer", "sirket": "TÜBİTAK BİLGEM"},
    {"url": "https://uzay.tubitak.gov.tr/tr/duyurular", "sirket": "TÜBİTAK UZAY"},
    {"url": "https://mam.tubitak.gov.tr/tr/duyurular", "sirket": "TÜBİTAK MAM"},
    {"url": "https://rute.tubitak.gov.tr/tr/duyurular", "sirket": "TÜBİTAK RUTE"},
    {"url": "https://www.baykartech.com/tr/kariyer/acik-pozisyonlar/", "sirket": "Baykar"},
    {"url": "https://kariyer.tusas.com/ilanlar", "sirket": "TUSAŞ (TAI)"},
    {"url": "https://www.aselsan.com/tr/kariyer/acik-pozisyonlar", "sirket": "Aselsan"},
    {"url": "https://ik.roketsan.com.tr/", "sirket": "Roketsan"},
    {"url": "https://kariyer.havelsan.com.tr/", "sirket": "Havelsan"},
    {"url": "https://www.tei.com.tr/kariyer/acik-pozisyonlar", "sirket": "TEI"},
    {"url": "https://www.stm.com.tr/tr/kariyer/acik-pozisyonlar", "sirket": "STM"},
    {"url": "https://www.fnss.com.tr/kariyer/acik-pozisyonlar", "sirket": "FNSS"},
    {"url": "https://www.otokar.com.tr/kariyer", "sirket": "Otokar"},
    {"url": "https://www.bmc.com.tr/kariyer", "sirket": "BMC"},
    {"url": "https://www.katmerciler.com.tr/TR/Kariyer", "sirket": "Katmerciler"},
    {"url": "https://www.kale.com.tr/kariyer", "sirket": "Kale Havacılık"},
    {"url": "https://turksh.com.tr/kariyer", "sirket": "TUSAŞ Helikopter"},
    {"url": "https://turkhizy.com/kariyer/", "sirket": "THY Teknik"},
    {"url": "https://www.togg.com.tr/content/kariyer", "sirket": "Togg"},
    {"url": "https://live.fordotosan.com.tr/kariyer", "sirket": "Ford Otosan"},
    {"url": "https://kariyer.mercedes-benz.com.tr/", "sirket": "Mercedes-Benz"},
    {"url": "https://tr.toyota.com.tr/pages/insan-kaynaklari", "sirket": "Toyota TR"},
    {"url": "https://tofas.com.tr/kariyer", "sirket": "Tofaş"},
    {"url": "https://www.renault.com.tr/renault-dunyasi/insan-kaynaklari.html", "sirket": "Renault Mais"},
    {"url": "https://www.man.com.tr/kariyer", "sirket": "MAN Türkiye"},
    {"url": "https://www.turktraktor.com.tr/insan-kaynaklari/acik-pozisyonlar", "sirket": "Türk Traktör"},
    {"url": "https://www.karsan.com/tr/insan-kaynaklari/kariyer-firsatlari", "sirket": "Karsan"},
    {"url": "https://www.anadoluisuzu.com.tr/kariyer", "sirket": "Anadolu Isuzu"},
    {"url": "https://jobs.siemens.com/careers?location=Turkey", "sirket": "Siemens TR"},
    {"url": "https://www.se.com/tr/tr/about-us/careers/job-opportunities.jsp", "sirket": "Schneider Electric"},
    {"url": "https://altinay.com/kariyer/", "sirket": "Altınay Robotik"},
    {"url": "https://kontrolmatik.com/kariyer", "sirket": "Kontrolmatik"},
    {"url": "https://www.hktm.com.tr/kariyer", "sirket": "HKTM (Hidropar)"},
    {"url": "https://enerjisa.com.tr/kariyer", "sirket": "Enerjisa"},
    {"url": "https://www.tupras.com.tr/kariyer", "sirket": "Tüpraş"},
    {"url": "https://www.petkim.com.tr/kariyer", "sirket": "Petkim"},
    {"url": "https://www.hidromek.com.tr/tr/insan-kaynaklari", "sirket": "Hidromek"},
    {"url": "https://www.sanko.com.tr/kariyer", "sirket": "Sanko Makina"},
    {"url": "https://www.caterpillar.com/en/careers/search-jobs.html", "sirket": "Caterpillar"},
    {"url": "https://cci.com.tr/tr/kariyer/kariyer-firsatlari", "sirket": "Coca-Cola"},
    {"url": "https://www.eti.com.tr/insan-kaynaklari", "sirket": "Eti"},
    {"url": "https://www.ulker.com.tr/tr/insan-kaynaklari", "sirket": "Ülker"},
    {"url": "https://www.unilever.com.tr/careers/", "sirket": "Unilever"},
    {"url": "https://www.pmi.com/careers/explore-our-job-opportunities", "sirket": "Philip Morris"},
    {"url": "https://tr.pg.com/kariyer/", "sirket": "P&G Türkiye"},
    {"url": "https://www.meteksan.com/tr/kariyer/acik-pozisyonlar", "sirket": "Meteksan"},
    {"url": "https://www.abdiibrahim.com.tr/kariyer/is-ilanlari", "sirket": "Abdi İbrahim"},
    {"url": "https://www.gehealthcare.com.tr/hakkimizda/kariyer", "sirket": "GE HealthCare"},
    {"url": "https://www.arcelik.com.tr/kariyer", "sirket": "Arçelik"},
    {"url": "https://www.vestel.com.tr/kariyer", "sirket": "Vestel"},
    {"url": "https://www.bsheverri.com/tr/", "sirket": "BSH"},
    {"url": "https://www.erdemir.com.tr/kariyer/", "sirket": "Erdemir"},
    {"url": "https://sisecam.com.tr/tr/kariyer", "sirket": "Şişecam"},
]

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def telegram_gonder(mesaj):
    if not TOKEN or not CHAT_ID: return
    if len(mesaj) > 4000: mesaj = mesaj[:4000] + "..."
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown", "disable_web_page_preview": True}, timeout=10)
    except: pass

def tarayici_baslat():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.page_load_strategy = 'eager'
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    return driver

def main():
    print(f"🚀 İNATÇI TARAMA BAŞLIYOR... ({len(URL_LISTESI)} Şirket)")
    bulunanlar = []

    driver = None
    try:
        driver = tarayici_baslat()
    except Exception as e:
        print(f"❌ Driver başlatılamadı: {e}")
        return

    for i, hedef in enumerate(URL_LISTESI, 1):
        print(f"[{i}/{len(URL_LISTESI)}] {hedef['sirket']}...", end=" ", flush=True)
        
        # --- RETRY (YENİDEN DENEME) MEKANİZMASI ---
        basarili = False
        deneme_sayisi = 0
        
        while deneme_sayisi < 2 and not basarili: # En fazla 2 kere dene
            deneme_sayisi += 1
            try:
                driver.get(hedef["url"])
                basarili = True # Eğer buraya geldiyse hata vermemiştir
                time.sleep(1)
            except Exception as e:
                # Hata aldıysak
                if deneme_sayisi == 1:
                    print("⚠️ (Hata aldı, tekrar deniyor...)", end=" ", flush=True)
                    # Tarayıcıyı yenile ve biraz bekle
                    try: driver.quit() 
                    except: pass
                    time.sleep(5) # 5 Saniye dinlen
                    driver = tarayici_baslat()
                else:
                    # İkinci denemede de hata verirse yazdır ve geç
                    print(f"❌ Ulaşılamadı ({str(e)[:30]})")
        
        if not basarili:
            continue # Başarısızsa sonraki şirkete geç

        # --- SAYFA ANALİZİ ---
        try:
            # Zaman aşımı durumunda sayfanın yüklendiği kadarını al
            driver.execute_script("window.stop();") 
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            metin = soup.get_text().lower().replace('i̇', 'i').replace('ı', 'i')
            
            kelime_bulundu = False
            for kelime in ARANACAK_KELIMELER:
                if kelime in metin:
                    # Negatif kontrol
                    eski_mi = False
                    for negatif in NEGATIF_KELIMELER:
                        if negatif in metin:
                            print(f"🗑️ ESKİ ({negatif})")
                            eski_mi = True
                            break
                    
                    if eski_mi:
                        break

                    bulunanlar.append(f"✅ **{hedef['sirket']}** ({kelime})\n🔗 {hedef['url']}")
                    print(f"--> BULUNDU! ({kelime})")
                    kelime_bulundu = True
                    break
            
            if not kelime_bulundu:
                print("Temiz.")
                
        except Exception:
            print("❌ Analiz Hatası")

    if driver:
        try: driver.quit()
        except: pass

    if bulunanlar:
        baslik = f"📢 **GÜNCEL STAJ RAPORU ({len(bulunanlar)} İlan)**\n\n"
        icerik = "\n\n".join(bulunanlar)
        telegram_gonder(baslik + icerik)
        print("\n✅ Rapor gönderildi.")
    else:
        print("\n❌ Yeni ve güncel ilan bulunamadı.")

if __name__ == "__main__":
    main()
