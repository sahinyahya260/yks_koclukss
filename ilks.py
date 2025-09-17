import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def main():
    st.set_page_config(page_title="🎓 YKS Kişiselleştirilmiş Çalışma Programı", layout="wide")
    
    # Ana başlık ve açıklama
    st.title("🎓 Psikoloji Temelli Kişiselleştirilmiş YKS Programı")
    st.markdown("---")
    
    # Sidebar - Öğrenci Bilgileri
    with st.sidebar:
        st.header("📝 Öğrenci Bilgileri")
        
        # Kişisel bilgiler
        ad_soyad = st.text_input("Ad Soyad", placeholder="Örn: Ahmet Yılmaz")
        yas = st.number_input("Yaş", min_value=16, max_value=25, value=18)
        hedef_universite = st.text_input("Hedef Üniversite/Bölüm", placeholder="Örn: Boğaziçi/Bilgisayar Mühendisliği")
        
        # Çalışma tercihleri
        st.subheader("⏰ Çalışma Tercihleri")
        uyku_saati = st.time_input("Uyku Saati", value=datetime.strptime("23:00", "%H:%M").time())
        kalkma_saati = st.time_input("Kalkış Saati", value=datetime.strptime("06:00", "%H:%M").time())
        gunluk_ders_sayisi = st.slider("Günlük Çalışılacak Ders Sayısı", 2, 6, 4)
        
        # Kişilik analizi
        st.subheader("🧠 Kişilik Analizi")
        odaklanma_suresi = st.selectbox("Başlangıç Odaklanma Süresi", 
                                      ["25 dakika (Başlangıç)", "45 dakika (Orta)", "60 dakika (İleri)"])
        ogrenme_stili = st.selectbox("Öğrenme Stili", 
                                   ["Görsel", "İşitsel", "Kinestetik", "Okuma/Yazma"])
        motivasyon_tipi = st.selectbox("Motivasyon Tipi", 
                                     ["Kısa vadeli hedefler", "Uzun vadeli hedefler", "Rekabetçi", "İş birlikçi"])

    # Ana içerik alanı
    if ad_soyad:
        # Ders seviye değerlendirmesi
        st.header("📊 Mevcut Ders Seviyeleri Değerlendirmesi")
        
        dersler = ["Matematik", "Türkçe", "Fizik", "Kimya", "Biyoloji", "Tarih", "Coğrafya", "Felsefe"]
        seviyeler = ["Zayıf (0-30)", "Temel (30-50)", "Orta (50-70)", "İyi (70-85)", "Uzman (85-100)"]
        
        col1, col2, col3, col4 = st.columns(4)
        ders_seviyeleri = {}
        
        for i, ders in enumerate(dersler):
            if i % 4 == 0:
                with col1:
                    ders_seviyeleri[ders] = st.selectbox(f"{ders}", seviyeler, key=f"seviye_{ders}")
            elif i % 4 == 1:
                with col2:
                    ders_seviyeleri[ders] = st.selectbox(f"{ders}", seviyeler, key=f"seviye_{ders}")
            elif i % 4 == 2:
                with col3:
                    ders_seviyeleri[ders] = st.selectbox(f"{ders}", seviyeler, key=f"seviye_{ders}")
            else:
                with col4:
                    ders_seviyeleri[ders] = st.selectbox(f"{ders}", seviyeler, key=f"seviye_{ders}")
        
        if st.button("🚀 Kişiselleştirilmiş Program Oluştur", type="primary"):
            # Program oluşturma
            create_personalized_program(ad_soyad, ders_seviyeleri, gunluk_ders_sayisi, 
                                      odaklanma_suresi, ogrenme_stili, motivasyon_tipi,
                                      uyku_saati, kalkma_saati, hedef_universite)

def get_seviye_sayisi(seviye_str):
    """Seviye stringinden sayısal değer çıkarır"""
    if "Zayıf" in seviye_str:
        return 1
    elif "Temel" in seviye_str:
        return 2
    elif "Orta" in seviye_str:
        return 3
    elif "İyi" in seviye_str:
        return 4
    else:
        return 5

def get_zayif_dersler(ders_seviyeleri):
    """En zayıf dersleri belirler"""
    zayif_dersler = []
    for ders, seviye in ders_seviyeleri.items():
        if get_seviye_sayisi(seviye) < 4:  # İyi seviyesinin altındakiler
            zayif_dersler.append((ders, get_seviye_sayisi(seviye)))
    
    # Seviye puanına göre sırala
    zayif_dersler.sort(key=lambda x: x[1])
    return [ders[0] for ders in zayif_dersler]

def get_kitap_onerisi(ogrenme_stili, motivasyon_tipi):
    """Kişilik analizine göre kitap önerir"""
    kitaplar = {
        "Görsel": ["Atomik Alışkanlıklar - James Clear", "Mindset - Carol Dweck"],
        "İşitsel": ["7 Alışkanlık - Stephen Covey", "Derin Çalışma - Cal Newport"],
        "Kinestetik": ["Peak - Anders Ericsson", "Grit - Angela Duckworth"],
        "Okuma/Yazma": ["Öğrenme Nasıl Öğrenilir - Barbara Oakley", "Make It Stick - Peter Brown"]
    }
    return random.choice(kitaplar.get(ogrenme_stili, kitaplar["Görsel"]))

def create_haftalik_program(zayif_dersler, gunluk_ders_sayisi, odaklanma_suresi):
    """Haftalık çalışma programı oluşturur"""
    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    program = {}
    
    # Odaklanma süresini parse et
    if "25" in odaklanma_suresi:
        pomodoro = "25+5 dakika"
        hedef_sure = "90+15 dakika (4 hafta sonra)"
    elif "45" in odaklanma_suresi:
        pomodoro = "45+10 dakika"
        hedef_sure = "90+15 dakika (3 hafta sonra)"
    else:
        pomodoro = "60+15 dakika"
        hedef_sure = "90+15 dakika (2 hafta sonra)"
    
    rutinler = ["Paragraf Çözümü", "Problem Çözme", "Geometri", "Test Tekniği", "Konu Tekrarı"]
    
    for gun in gunler:
        if gun == "Pazar":
            program[gun] = {
                "06:30-07:30": "🌅 Günün Başlangıcı + Kahvaltı",
                "08:00-09:30": "📚 Haftalık Genel Tekrar",
                "10:00-11:30": "📖 Kitap Okuma + Feynman Tekniği",
                "12:00-13:00": "🥗 Hafif Öğle Yemeği",
                "14:00-15:30": "🧠 Mind Mapping + Cornell Notları",
                "16:00-17:00": "⚡ Blitz Tekrar",
                "18:00-19:00": "🍽️ Hafif Akşam Yemeği",
                "20:00-21:30": "🎯 Aktif Hatırlama + Essay Yazma",
                "22:00-23:00": "😌 Dinlenmek + Gevşeme"
            }
        else:
            gunluk_dersler = []
            for i in range(min(gunluk_ders_sayisi, len(zayif_dersler))):
                gunluk_dersler.append(zayif_dersler[i % len(zayif_dersler)])
            
            program[gun] = {
                "06:30-07:30": "🌅 Günün Başlangıcı + Kahvaltı",
                "08:00-09:30": f"📚 {gunluk_dersler[0] if gunluk_dersler else 'Matematik'} ({pomodoro})",
                "10:00-11:30": f"🔄 {random.choice(rutinler)}",
                "12:00-13:00": "🥗 Hafif Öğle Yemeği",
                "14:00-15:30": f"📝 {gunluk_dersler[1] if len(gunluk_dersler) > 1 else 'Türkçe'}",
                "16:00-17:00": "📖 Kitap Okuma",
                "18:00-19:00": "🍽️ Hafif Akşam Yemeği",
                "20:00-21:30": f"🎯 {gunluk_dersler[2] if len(gunluk_dersler) > 2 else 'Fen Bilgisi'} + Tekrar",
                "22:00-23:00": "😌 Dinlenmek + Günü Değerlendirme"
            }
    
    return program, hedef_sure

def create_personalized_program(ad_soyad, ders_seviyeleri, gunluk_ders_sayisi, 
                               odaklanma_suresi, ogrenme_stili, motivasyon_tipi,
                               uyku_saati, kalkma_saati, hedef_universite):
    
    st.success(f"🎉 {ad_soyad} için kişiselleştirilmiş program hazırlandı!")
    
    # Analiz sonuçları
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Analiz Sonuçları")
        zayif_dersler = get_zayif_dersler(ders_seviyeleri)
        
        if zayif_dersler:
            st.warning(f"🎯 **Öncelik verilecek dersler:** {', '.join(zayif_dersler[:3])}")
        else:
            st.success("✅ Tüm derslerde iyi seviyedesiniz! Pekiştirme odaklı program hazırlanıyor.")
    
    with col2:
        st.subheader("📚 Önerilen Kitap")
        kitap = get_kitap_onerisi(ogrenme_stili, motivasyon_tipi)
        st.info(f"📖 **{kitap}**")
        st.caption(f"*{ogrenme_stili} öğrenme stiline uygun seçildi*")
    
    # Haftalık program
    st.header("📅 Haftalık Çalışma Programı")
    program, hedef_sure = create_haftalik_program(zayif_dersler, gunluk_ders_sayisi, odaklanma_suresi)
    
    # Tarih aralığı
    bugun = datetime.now()
    hafta_sonu = bugun + timedelta(days=7)
    st.subheader(f"📆 {bugun.strftime('%d %B')} - {hafta_sonu.strftime('%d %B %Y')}")
    
    # Program tablosu
    for gun, aktiviteler in program.items():
        with st.expander(f"📋 **{gun}** Programı", expanded=True):
            df = pd.DataFrame(list(aktiviteler.items()), columns=['⏰ Saat', '📚 Aktivite'])
            st.table(df)
    
    # Çalışma teknikleri
    st.header("🧠 Önerilen Çalışma Teknikleri")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 Feynman Tekniği**
        - Konuyu 5 yaşındaki çocuğa anlat
        - Anlamadığın yerleri tespit et
        - Basit kelimelerle açıkla
        """)
        
        st.markdown("""
        **📝 Cornell Not Alma**
        - Sayfayı 3 bölüme ayır
        - Ana notlar, anahtar kelimeler, özet
        - Sistematik tekrar
        """)
    
    with col2:
        st.markdown("""
        **🎯 Aktif Hatırlama**
        - Kitaba bakmadan hatırla
        - Beyni zorla
        - Derinlemesine işle
        """)
        
        st.markdown("""
        **⚡ Blitz Tekrar**
        - 24 saat içinde hızlı tekrar
        - Uzun süreli hafızaya geçiş
        - Kısa ve etkili
        """)
    
    with col3:
        st.markdown("""
        **🔄 Interleaving**
        - Farklı konuları karıştır
        - Beyin bağlantısı güçlenir
        - Ayırt etme yetisi artar
        """)
        
        st.markdown("""
        **🎨 Mind Mapping**
        - Görsel bağlantılar kur
        - Anahtar kelimeler kullan
        - Ağaç yapısında organize et
        """)
    
    # Beslenme önerileri
    st.header("🥗 Beslenme Önerileri")
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ Önerilen Yiyecekler:**
        - Fındık, ceviz, badem (beyin gıdası)
        - Balık (omega-3)
        - Yumurta (protein)
        - Meyve ve sebze (vitamin)
        - Bol su (hidrasyon)
        """)
    
    with col2:
        st.warning("""
        **❌ Kaçınılması Gerekenler:**
        - Ağır öğle yemekleri
        - Şekerli atıştırmalıklar
        - Fazla kafein
        - İşlenmiş gıdalar
        - Geç saatlerde yemek
        """)
    
    # Aylık hedefler
    st.header("🎯 Aylık İlerleme Hedefleri")
    
    ilerleme_df = pd.DataFrame({
        'Ders': list(ders_seviyeleri.keys()),
        'Mevcut Seviye': [get_seviye_sayisi(seviye) * 20 for seviye in ders_seviyeleri.values()],
        'Hedef Seviye (Ay Sonu)': [min(100, get_seviye_sayisi(seviye) * 20 + 15) for seviye in ders_seviyeleri.values()],
        'Beklenen İlerleme': ['+15 puan' if get_seviye_sayisi(seviye) < 4 else '+10 puan' for seviye in ders_seviyeleri.values()]
    })
    
    st.dataframe(ilerleme_df, use_container_width=True)
    
    # Motivasyon kartı
    st.header("💪 Motivasyon Kartın")
    st.info(f"""
    🎓 **{ad_soyad}**, hedefin **{hedef_universite}**!
    
    📊 **Bu ay %80 başarı ile:**
    - Zayıf derslerinde ortalama 15 puan artış
    - Güçlü derslerinde pekiştirme
    - {hedef_sure} odaklanma süresi kazanımı
    
    💡 **Hatırla:** Her gün küçük adımlar büyük başarıları getirir!
    """)
    
    # İstatistikler
    st.header("📊 Program İstatistikleri")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Günlük Ders", f"{gunluk_ders_sayisi} ders")
    
    with col2:
        st.metric("Haftalık Çalışma", "42 saat")
    
    with col3:
        st.metric("Odaklanma", odaklanma_suresi.split('(')[0])
    
    with col4:
        st.metric("Öncelik Ders", f"{len(zayif_dersler)} ders")

if __name__ == "__main__":
    main()