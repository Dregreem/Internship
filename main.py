import os
import time
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException

# --- 1. HEDEF LİSTESİ ---
URL_LISTESI = [
    # --- 🇹🇷 TÜBİTAK VE AR-GE ---
    {"url": "https://kariyer.tubitak.gov.tr/giris.htm", "sirket": "TÜBİTAK Kariyer"},
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
    {"url": "https://www.tei.com.tr/kariyer/acik-pozisyonlar", "sirket": "TEI"},
    {"url": "https://www.stm.com.tr/tr/kariyer/acik-pozisyonlar", "sirket": "STM"},
    {"url": "https://www.fnss.com.tr/kariyer/acik-pozisyonlar", "sirket": "FNSS"},
    {"url": "https://www.otokar.com.tr/kariyer", "sirket": "Otokar"},
    {"url": "https://www.bmc.com.tr/kariyer", "sirket": "BMC"},
    {"url": "https://www.katmerciler.com.tr/TR/Kariyer", "sirket": "Katmerciler"},
    {"url": "https://www.kale.com.tr/kariyer", "sirket": "Kale Havacılık"},
    {"url": "https://turksh.com.tr/kariyer", "sirket": "TUSAŞ Helikopter"},
    {"url": "https://turkhizy.com/kariyer/", "sirket": "THY Teknik"},

    # --- 🚗 OTOMOTİV ---
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

    # --- 🤖 ROBOTİK & ENERJİ ---
    {"url": "https://jobs.siemens.com/careers?location=Turkey", "sirket": "Siemens TR"},
    {"url": "https://www.se.com/tr/tr/about-us/careers/job-opportunities.jsp", "sirket": "Schneider Electric"},
    {"url": "https://altinay.com/kariyer/", "sirket": "Altınay Robotik"},
    {"url": "https://kontrolmatik.com/kariyer", "sirket": "Kontrolmatik"},
    {"url": "https://www.hktm.com.tr/kariyer", "sirket": "HKTM (Hidropar)"},
    {"url": "https://enerjisa.com.tr/kariyer", "sirket": "Enerjisa"},
    {"url": "https://www.tupras.com.tr/kariyer", "sirket": "Tüpraş"},
    {"url": "https://www.petkim.com.tr/kariyer", "sirket": "Petkim"},
    {"url": "https://www.hidromek.com.tr/tr/insan-kaynaklari", "sirket": "Hidromek"},
    
    # --- 🚜 İŞ MAKİNELERİ & GIDA ---
    {"url": "https://www.sanko.com.tr/kariyer", "sirket": "Sanko Makina"},
    {"url": "https://www.caterpillar.com/en/careers/search-jobs.html", "sirket": "Caterpillar"},
    {"url": "https://cci.com.tr/tr/kariyer/kariyer-firsatlari", "sirket": "Coca-Cola"},
    {"url": "https://www.eti.com.tr/insan-kaynaklari", "sirket": "Eti"},
    {"url": "https://www.ulker.com.tr/tr/insan-kaynaklari", "sirket": "Ülker"},
    {"url": "https://www.unilever.com.tr/careers/", "sirket": "Unilever"},
    {"url": "https://www.pmi.com/careers/explore-our-job-opportunities", "sirket": "Philip Morris"},
    {"url": "https://tr.pg.com/kariyer/", "sirket": "P&G Türkiye"},

    # --- 🧬 DİĞER DEVLER ---
    {"url": "https://www.meteksan.com/tr/kariyer/acik-pozisyonlar", "sirket": "Meteksan"},
    {"url": "https://www.abdiibrahim.com.tr/kariyer/is-ilanlari", "sirket": "Abdi İbrahim"},
    {"url": "https://www.gehealthcare.com.tr/hakkimizda/kariyer", "sirket": "GE HealthCare"},
    {"url": "https://www.arcelik.com.tr/kariyer", "sirket": "Arçelik"},
    {"url": "https://www.vestel.com.tr/kariyer", "sirket": "Vestel"},
    {"url": "https://www.bsheverri.com/tr/", "sirket": "BSH"},
    {"url": "https://www.erdemir.com.tr/kariyer/", "sirket": "Erdemir"},
    {"url": "https://sisecam.com.tr/tr/kariyer", "sirket": "Şişecam"},
]

ARANACAK_KELIMELER = [
    "staj", "intern", "part-time", "yarı zamanlı", 
    "aday mühendis", "uzun dönem", "kısa dönem", 
    "student", "werkstudent", "trainee", "yetenek"
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

def tarayici_yarat():
    """Optimize edilmiş, hafif tarayıcı ayarları"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage") # Bellek taşmasını önler
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false") # Resimleri kapat
    
    # EAGER STRATEJİSİ: Sayfanın tamamen bitmesini bekleme, HTML gelince başla!
    chrome_options.page_load_strategy = 'eager' 
    
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30) # 30 saniye üst sınır
    return driver

def siteyi_incele(hedef):
    driver = None
    sonuc = None
    # print(f"⏳ Başlıyor: {hedef['sirket']}") # Log kirliliğini azaltmak için kapattım
    
    try:
        driver = tarayici_yarat()
        try:
            driver.get(hedef["url"])
            # Eager modunda olduğumuz için sleep'e gerek yok, element var mı diye bakarız
            time.sleep(1) 
        except TimeoutException:
            # Zaman aşımı olsa bile driver.page_source dolu olabilir, devam et
            driver.execute_script("window.stop();")
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        metin = soup.get_text().lower().replace('i̇', 'i').replace('ı', 'i')
        
        for kelime in ARANACAK_KELIMELER:
            if kelime in metin:
                sonuc = f"✅ **{hedef['sirket']}** ({kelime})\n🔗 {hedef['url']}"
                print(f"--> BULUNDU! {hedef['sirket']}")
                break
                
    except Exception as e:
        print(f"❌ Hata ({hedef['sirket']}): {str(e)[:50]}")
    finally:
        if driver: 
            try: driver.quit()
            except: pass
        
    return sonuc

def main():
    print(f"🚀 OPTİMİZE TARAMA BAŞLIYOR... ({len(URL_LISTESI)} Şirket)")
    start_time = time.time()
    bulunanlar = []

    # MAX_WORKERS = 2 (Sunucuyu yormamak için düşürdük)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = executor.map(siteyi_incele, URL_LISTESI)
        
        for result in results:
            if result:
                bulunanlar.append(result)

    duration = time.time() - start_time
    print(f"\n🏁 Tarama tamamlandı! Süre: {duration:.2f} saniye")

    if bulunanlar:
        baslik = f"📢 **GÜNLÜK STAJ RAPORU ({len(bulunanlar)} İlan)**\n\n"
        icerik = "\n\n".join(bulunanlar)
        telegram_gonder(baslik + icerik)
    else:
        print("❌ Yeni ilan bulunamadı.")

if __name__ == "__main__":
    main()
