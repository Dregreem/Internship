import requests
from bs4 import BeautifulSoup
import os
import time

# --- 1. AYARLAR VE HEDEF LİSTESİ ---
# Türkiye'nin en büyük sanayi ve teknoloji şirketlerinin kariyer sayfaları
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
    "staj", 
    "intern", 
    "part-time", 
    "part time",
    "yarı zamanlı", 
    "aday mühendis", 
    "uzun dönem", 
    "kısa dönem",
    "yetenek programı",
    "genç yetenek",
    "early career",
    "student",
    "werkstudent"
]

# GitHub Secrets'tan alınacak şifreler
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# --- 3. FONKSİYONLAR ---

def telegram_gonder(mesaj):
    if not TOKEN or not CHAT_ID:
        print("HATA: Token veya Chat ID bulunamadı! (GitHub Secrets ayarlarını kontrol et)")
        return
    
    # Mesaj çok uzunsa bölme işlemi (Telegram limiti 4096 karakter)
    if len(mesaj) > 4000:
        mesaj = mesaj[:4000] + "\n... (Mesajın devamı kırpıldı)"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": mesaj, 
        "parse_mode": "Markdown", 
        "disable_web_page_preview": True
    }
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram gönderme hatası: {e}")

def siteyi_tarama():
    print(f"🔍 Toplam {len(URL_LISTESI)} sanayi devi taranıyor...")
    bulunanlar = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    sayac = 0
    for hedef in URL_LISTESI:
        sayac += 1
        print(f"[{sayac}/{len(URL_LISTESI)}] Kontrol: {hedef['sirket']}...", end=" ")
        
        try:
            # Sunucuları yormamak için her istek arasında 1 saniye bekle
            time.sleep(1) 
            response = requests.get(hedef["url"], headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Türkçe karakter sorununu çözmek için özel işlem
                sayfa_metni = soup.get_text()
                sayfa_metni = sayfa_metni.replace('İ', 'i').replace('I', 'ı').lower()
                
                kelime_bulundu = False
                for kelime in ARANACAK_KELIMELER:
                    if kelime in sayfa_metni:
                        mesaj = f"✅ **{hedef['sirket']}** sitesinde '{kelime}' bulundu!\n🔗 [İlana Git]({hedef['url']})"
                        bulunanlar.append(mesaj)
                        print(f"--> BULUNDU! ({kelime})")
                        kelime_bulundu = True
                        break # Aynı sitede bir kelime bulmak yeterli
                
                if not kelime_bulundu:
                    print("Temiz.")
            else:
                print(f"⚠️ Erişim sorunu (Kod: {response.status_code})")

        except Exception as e:
            print(f"❌ Hata: {e}")

    # --- RAPORLAMA ---
    if bulunanlar:
        baslik = f"📢 **GÜNLÜK STAJ RAPORU ({len(bulunanlar)} Eşleşme)**\n\n"
        icerik = "\n\n".join(bulunanlar)
        telegram_gonder(baslik + icerik)
        print("\n🚀 Rapor Telegram'a gönderildi.")
    else:
        print("\n❌ Bu taramada yeni ilan bulunamadı.")

if __name__ == "__main__":
    siteyi_tarama()