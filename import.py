import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import random
import numpy as np
import time

# Sayfa yapılandırması
st.set_page_config(
    page_title="YKS Master Pro | Profesyonel Konu Takip Sistemi",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS stilleri
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subheader {
        font-size: 1.2rem;
        color: #6c757d;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border-left: 5px solid #6a11cb;
    }
    .progress-container {
        height: 24px;
        background-color: #e9ecef;
        border-radius: 12px;
        margin: 10px 0;
        overflow: hidden;
    }
    .progress-bar {
        height: 100%;
        border-radius: 12px;
        background: linear-gradient(45deg, #6a11cb, #2575fc);
        text-align: center;
        color: white;
        line-height: 24px;
        font-weight: bold;
        font-size: 0.8rem;
        transition: width 0.5s ease;
    }
    .subject-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 15px;
        border: 1px solid #e9ecef;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .subject-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #6a11cb 0%, #2575fc 100%);
        color: white;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        color: white;
    }
    .stats-number {
        font-size: 2rem;
        font-weight: 800;
        color: #6a11cb;
    }
    .stats-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .nav-button {
        background: linear-gradient(45deg, #6a11cb, #2575fc);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 15px;
        margin: 5px 0;
        width: 100%;
        text-align: left;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .nav-button:hover {
        background: linear-gradient(45deg, #2575fc, #6a11cb);
        transform: translateX(5px);
    }
    .calendar-day {
        border-radius: 50%;
        width: 35px;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 2px;
        font-weight: 500;
    }
    .calendar-day.active {
        background: linear-gradient(45deg, #6a11cb, #2575fc);
        color: white;
    }
    .calendar-day.inactive {
        background: #f8f9fa;
        color: #adb5bd;
    }
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        background: linear-gradient(45deg, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    /* Ders renkleri */
    .turkce { border-left: 5px solid #e74c3c; }
    .matematik { border-left: 5px solid #3498db; }
    .geometri { border-left: 5px solid #2ecc71; }
    .fizik { border-left: 5px solid #9b59b6; }
    .kimya { border-left: 5px solid #f1c40f; }
    .biyoloji { border-left: 5px solid #1abc9c; }
    .tarih { border-left: 5px solid #e67e22; }
    .cografya { border-left: 5px solid #34495e; }
    .felsefe { border-left: 5px solid #7f8c8d; }
    .din { border-left: 5px solid #16a085; }
    .edebiyat { border-left: 5px solid #d35400; }
</style>
""", unsafe_allow_html=True)

# Oturum durumu başlatma
if 'konu_durumu' not in st.session_state:
    st.session_state.konu_durumu = {}
if 'calisma_gunleri' not in st.session_state:
    st.session_state.calisma_gunleri = []
if 'motivasyon' not in st.session_state:
    st.session_state.motivasyon = 100
if 'ogrenme_stili' not in st.session_state:
    st.session_state.ogrenme_stili = "Henüz belirlenmedi"
if 'feynman_notlari' not in st.session_state:
    st.session_state.feynman_notlari = {}
if 'aktif_hatirlama_sorulari' not in st.session_state:
    st.session_state.aktif_hatirlama_sorulari = {}
if 'hedefler' not in st.session_state:
    st.session_state.hedefler = {}
if 'son_calisma' not in st.session_state:
    st.session_state.son_calisma = {}
if 'tum_konular' not in st.session_state:
    # Tüm konuları düzleştirilmiş şekilde sakla
    st.session_state.tum_konular = []

# YKS konularını tanımla (kısaltılmış versiyon)
yks_konulari = {
    "TYT Türkçe": {
        "Anlam Bilgisi": {
            "Sözcükte Anlam": [
                "Gerçek, Mecaz, Terim Anlam",
                "Çok Anlamlılık",
                "Deyimler ve Atasözleri",
                "Sözcükler Arası Anlam İlişkileri"
            ],
            "Cümlede Anlam": [
                "Cümle Yorumlama",
                "Kesin Yargıya Ulaşma",
                "Anlatım Biçimleri",
                "Duygu ve Düşünceleri İfade Etme",
                "Amaç-Sonuç, Neden-Sonuç, Koşul-Sonuç"
            ],
            "Paragraf": [
                "Anlatım Teknikleri",
                "Düşünceyi Geliştirme Yolları",
                "Paragrafta Yapı",
                "Paragrafta Konu-Ana Düşünce",
                "Paragrafta Yardımcı Düşünce"
            ]
        },
        "Dil Bilgisi": {
            "Ses Bilgisi": [
                "Ünlü-Ünsüz Uyumları",
                "Ses Olayları"
            ],
            "Yazım Kuralları": [
                "Büyük Harflerin Kullanımı",
                "Birleşik Kelimelerin Yazımı",
                "Sayıların ve Kısaltmaların Yazımı",
                "Bağlaçların Yazımı"
            ],
            "Noktalama İşaretleri": [
                "Nokta, Virgül",
                "Noktalı Virgül, İki Nokta, Üç Nokta",
                "Soru, Ünlem, Tırnak İşareti",
                "Yay Ayraç ve Kesme İşareti"
            ],
            "Sözcükte Yapı": [
                "Kök ve Gövde",
                "Ekler (Yapım/Çekim)",
                "Basit, Türemiş, Birleşik Sözcükler"
            ],
            "Sözcük Türleri": [
                "İsimler ve Zamirler",
                "Sıfatlar ve Zarflar",
                "Edat, Bağlaç, Ünlem"
            ],
            "Fiiller": [
                "Fiilde Anlam",
                "Ek Fiil",
                "Fiilimsi",
                "Fiilde Çatı"
            ],
            "Cümlenin Ögeleri": [
                "Temel Ögeler (Yüklem, Özne, Nesne)",
                "Yardımcı Ögeler (Dolaylı, Zarf, Edat Tümleci)"
            ],
            "Cümle Türleri": [
                "Yüklem ve Yapılarına Göre Cümleler"
            ],
            "Anlatım Bozukluğu": [
                "Anlamsal ve Yapısal Bozukluklar"
            ]
        }
    },
    # Diğer dersler de buraya eklenecek (kısaltma nedeniyle gösterilmiyor)
    "TYT Matematik": {},
    "TYT Geometri": {},
    "TYT Fizik": {},
    "TYT Kimya": {},
    "TYT Biyoloji": {},
    "TYT Tarih": {},
    "TYT Coğrafya": {},
    "TYT Felsefe": {},
    "TYT Din Kültürü": {},
    "AYT Matematik": {},
    "AYT Geometri": {},
    "AYT Fizik": {},
    "AYT Kimya": {},
    "AYT Biyoloji": {},
    "AYT Edebiyat": {},
    "AYT Tarih": {},
    "AYT Coğrafya": {}
}

# Tüm konuları düzleştirilmiş şekilde hazırla
def konulari_hazirla():
    tum_konular = []
    for ders, konu_alanlari in yks_konulari.items():
        for alan, alt_konular in konu_alanlari.items():
            for alt_konu, detaylar in alt_konular.items():
                for detay in detaylar:
                    konu_key = f"{ders} > {alan} > {alt_konu} > {detay}"
                    tum_konular.append(konu_key)
    return tum_konular

if not st.session_state.tum_konular:
    st.session_state.tum_konular = konulari_hazirla()

# Öğrenme teknikleri
ogrenme_teknikleri = {
    "Feynman Tekniği": {
        "icon": "📝",
        "açıklama": "Bir konuyu basitçe açıklayamıyorsanız, onu tam olarak anlamamışsınız demektir.",
        "adımlar": [
            "Öğrenmek istediğiniz konuyu seçin",
            "Konuyu birine anlatıyormuş gibi basitçe açıklayın",
            "Açıklarken zorlandığınız noktaları belirleyin ve bu noktalara geri dönün",
            "Analojiler ve basit örnekler kullanarak açıklamanızı basitleştirin"
        ]
    },
    "Aktif Hatırlama": {
        "icon": "🔁",
        "açıklama": "Pasif okuma yerine, bilgiyi zihninizden aktif olarak çağırmaya çalışın.",
        "adımlar": [
            "Okuduktan sonra kitabı kapatın ve anahtar noktaları hatırlamaya çalışın",
            "Kendinize sorular sorun ve cevaplamaya çalışın",
            "Öğrendiklerinizi başka birine anlatın",
            "Düzenli aralıklarla tekrarlar yapın"
        ]
    },
    "Pomodoro Tekniği": {
        "icon": "⏰",
        "açıklama": "Zamanı 25 dakikalık çalışma ve 5 dakikalık mola bloklarına bölün.",
        "adımlar": [
            "Yapılacak işi belirleyin",
            "Zamanlayıcıyı 25 dakikaya kurun",
            "Zamanlayıcı çalana kadar sadece o işe odaklanın",
            "Zamanlayıcı çaldığında 5 dakika mola verin",
            "Her 4 pomodoro'dan sonra 15-30 dakika uzun mola verin"
        ]
    }
}

# Öğrenme stilleri
ogrenme_stilleri = {
    "Okuyarak/Yazarak Öğrenenler": {
        "icon": "📖",
        "tavsiyeler": [
            "Detaylı notlar çıkarmak",
            "Okuduklarınızı kendi cümlelerinizle özetlemek",
            "Konuları flash kartlara yazmak",
            "Denemeler yazmak",
            "Listeler oluşturmak ve doldurmak",
            "Kendi kendine test etmek"
        ]
    },
    "Görsel Öğrenenler": {
        "icon": "🎨",
        "tavsiyeler": [
            "Renkli notlar almak",
            "Zihin haritaları oluşturmak",
            "Grafikler ve diyagramlar çizmek",
            "Görsel ipuçları kullanmak",
            "Video dersler izlemek",
            "Şemalar oluşturmak"
        ]
    },
    "İşitsel Öğrenenler": {
        "icon": "🔊",
        "tavsiyeler": [
            "Dersleri sesli olarak kaydetmek",
            "Bilgileri yüksek sesle tekrarlamak",
            "Grupla çalışmak ve tartışmak",
            "Ritimler ve şarkılar kullanmak",
            "Podcast'ler dinlemek",
            "Kendi kendine anlatım yapmak"
        ]
    },
    "Kinestetik Öğrenenler": {
        "icon": "🔄",
        "tavsiyeler": [
            "Öğrenirken hareket etmek",
            "Modeller oluşturmak",
            "Role-play yapmak",
            "Deneyler yapmak",
            "Pratik uygulamalar bulmak",
            "Elleri kullanarak öğrenmek"
        ]
    }
}

# Yardımcı fonksiyonlar
def ders_renki_bul(ders_adi):
    ders_renkleri = {
        "Türkçe": "turkce",
        "Matematik": "matematik",
        "Geometri": "geometri",
        "Fizik": "fizik",
        "Kimya": "kimya",
        "Biyoloji": "biyoloji",
        "Tarih": "tarih",
        "Coğrafya": "cografya",
        "Felsefe": "felsefe",
        "Din": "din",
        "Edebiyat": "edebiyat"
    }
    
    for anahtar, deger in ders_renkleri.items():
        if anahtar in ders_adi:
            return deger
    return ""

def konu_ilerleme_hesapla():
    toplam_konu = len(st.session_state.tum_konular)
    tamamlanan_konu = sum(1 for konu, seviye in st.session_state.konu_durumu.items() 
                         if seviye == "Uzman (Derece) Seviye")
    
    if toplam_konu > 0:
        return (tamamlanan_konu / toplam_konu) * 100
    return 0

def ders_bazli_ilerleme_hesapla():
    ders_ilerleme = {}
    for ders in yks_konulari.keys():
        ders_konulari = [k for k in st.session_state.tum_konular if k.startswith(ders)]
        tamamlanan = sum(1 for konu in ders_konulari 
                        if konu in st.session_state.konu_durumu and 
                        st.session_state.konu_durumu[konu] == "Uzman (Derece) Seviye")
        
        if len(ders_konulari) > 0:
            ders_ilerleme[ders] = (tamamlanan / len(ders_konulari)) * 100
        else:
            ders_ilerleme[ders] = 0
    return ders_ilerleme

def gunluk_calisma_grafigi():
    # Son 30 günü al
    bugun = date.today()
    gunler = [bugun - timedelta(days=x) for x in range(29, -1, -1)]
    calisma_durum = [1 if gun.strftime("%Y-%m-%d") in st.session_state.calisma_gunleri else 0 for gun in gunler]
    
    fig = go.Figure(data=go.Scatter(
        x=gunler,
        y=calisma_durum,
        mode='lines+markers',
        line=dict(color='#6a11cb', width=3),
        marker=dict(size=8, color='#6a11cb')
    ))
    
    fig.update_layout(
        title="Son 30 Günlük Çalışma Durumu",
        xaxis_title="Tarih",
        yaxis_title="Çalışma Durumu",
        yaxis=dict(tickvals=[0, 1], ticktext=['Çalışılmadı', 'Çalışıldı']),
        height=300,
        showlegend=False
    )
    
    return fig

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-header">YKS Master Pro</div>', unsafe_allow_html=True)
    
    # Navigasyon
    sayfa = st.radio("", ["🏠 Ana Sayfa", "📊 İlerleme", "🎯 Konu Takip", "📚 Öğrenme Araçları", "⚙️ Ayarlar"], label_visibility="collapsed")
    
    st.markdown("---")
    
    # Kullanıcı bilgileri
    st.markdown("### Kullanıcı Bilgileri")
    kullanici_adi = st.text_input("İsim", "Sadd")
    sinif = st.selectbox("Sınıf", ["12. Sınıf", "Mezun", "11. Sınıf", "Diğer"])
    hedef_puan = st.slider("Hedef Puan", 200, 500, 450)
    
    st.markdown("---")
    
    # Motivasyon
    st.markdown("### Motivasyon Durumu")
    st.markdown(f'<div style="text-align: center;"><span class="stats-number">{st.session_state.motivasyon}%</span></div>', unsafe_allow_html=True)
    st.progress(st.session_state.motivasyon / 100)
    
    if st.button("Motivasyon Artır 💪"):
        st.session_state.motivasyon = min(100, st.session_state.motivasyon + random.randint(5, 15))
        st.rerun()
    
    st.markdown("---")
    
    # Hızlı erişim
    st.markdown("### Hızlı Erişim")
    if st.button("Bugünkü Çalışmayı Kaydet ✅"):
        bugun = date.today().strftime("%Y-%m-%d")
        if bugun not in st.session_state.calisma_gunleri:
            st.session_state.calisma_gunleri.append(bugun)
            st.session_state.motivasyon = min(100, st.session_state.motivasyon + 5)
            st.success("Çalışma kaydedildi!")
        else:
            st.info("Bugün zaten çalışma kaydınız var.")
    
    if st.button("Rastgele Konu Çalış 🎲"):
        if st.session_state.tum_konular:
            rastgele_konu = random.choice(st.session_state.tum_konular)
            st.info(f"Şu konuyu çalış: **{rastgele_konu}**")
    
    st.markdown("---")
    st.markdown("*© 2023 YKS Master Pro*")

# Ana içerik
if sayfa == "🏠 Ana Sayfa":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="main-header">YKS Master Pro</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">Profesyonel YKS Hazırlık ve Konu Takip Sistemi</div>', unsafe_allow_html=True)
    
    with col2:
        st.metric("Kalan Gün", (date(2024, 6, 15) - date.today()).days)
    
    st.markdown("---")
    
    # İstatistikler
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        tamamlanan_yuzde = konu_ilerleme_hesapla()
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stats-number">{tamamlanan_yuzde:.1f}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="stats-label">Genel Tamamlama</div>', unsafe_allow_html=True)
        st.progress(tamamlanan_yuzde / 100)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stats-number">{len(st.session_state.konu_durumu)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stats-label">Eklenen Konu</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stats-number">{len(st.session_state.calisma_gunleri)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stats-label">Çalışma Günü</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stats-number">{st.session_state.motivasyon}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="stats-label">Motivasyon</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Ders bazlı ilerleme
    st.markdown("### Ders Bazlı İlerleme")
    ders_ilerleme = ders_bazli_ilerleme_hesapla()
    
    for ders, yuzde in ders_ilerleme.items():
        renk_sinifi = ders_renki_bul(ders)
        st.markdown(f'<div class="subject-card {renk_sinifi}">', unsafe_allow_html=True)
        st.markdown(f"**{ders}**")
        st.markdown(f'<div class="progress-container"><div class="progress-bar" style="width: {yuzde}%">{yuzde:.1f}%</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Çalışma takvimi
    st.markdown("### Son Çalışma Takvimi")
    st.plotly_chart(gunluk_calisma_grafigi(), use_container_width=True)
    
    # Öneriler
    st.markdown("### Bugün için Öneriler")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">📚</div>', unsafe_allow_html=True)
        st.markdown('**Zayıf Olduğun Konular**')
        st.markdown('Geometri ve Fizik konularına odaklan')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">⏰</div>', unsafe_allow_html=True)
        st.markdown('**Çalışma Planı**')
        st.markdown('3 saat aktif çalışma + 1 saat tekrar')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-icon">🎯</div>', unsafe_allow_html=True)
        st.markdown('**Günlük Hedef**')
        st.markdown('2 yeni konu + 3 eski konu tekrarı')
        st.markdown('</div>', unsafe_allow_html=True)

elif sayfa == "📊 İlerleme":
    st.markdown('<div class="main-header">Detaylı İlerleme Analizi</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Genel ilerleme grafiği
        labels = ['Tamamlanan', 'Kalan']
        values = [konu_ilerleme_hesapla(), 100 - konu_ilerleme_hesapla()]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values,
            hole=.4,
            marker_colors=['#6a11cb', '#e9ecef']
        )])
        
        fig.update_layout(
            title="Genel Konu Tamamlama Durumu",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Ders bazlı ilerleme
        ders_ilerleme = ders_bazli_ilerleme_hesapla()
        
        fig = go.Figure(data=[go.Bar(
            x=list(ders_ilerleme.values()),
            y=list(ders_ilerleme.keys()),
            orientation='h',
            marker_color='#6a11cb'
        )])
        
        fig.update_layout(
            title="Ders Bazlı İlerleme (%)",
            xaxis=dict(range=[0, 100]),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Aylık çalışma analizi
    st.markdown("### Aylık Çalışma Analizi")
    
    # Son 6 ayın çalışma verileri (simüle edilmiş)
    aylar = ['Ekim', 'Kasım', 'Aralık', 'Ocak', 'Şubat', 'Mart']
    calisma_gunleri = [15, 20, 18, 22, 19, 25]  # Örnek veri
    
    fig = go.Figure(data=[go.Bar(
        x=aylar,
        y=calisma_gunleri,
        marker_color='#6a11cb'
    )])
    
    fig.update_layout(
        title="Aylık Çalışılan Gün Sayısı",
        xaxis_title="Aylar",
        yaxis_title="Çalışılan Gün Sayısı",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif sayfa == "🎯 Konu Takip":
    st.markdown('<div class="main-header">Detaylı Konu Takip Sistemi</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Konu Ekle", "Konu Listesi", "Hedef Belirle"])
    
    with tab1:
        st.markdown("### Yeni Konu Ekle")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Ders seçimi
            dersler = list(yks_konulari.keys())
            secilen_ders = st.selectbox("Ders Seç", dersler, key="ders_secimi")
        
        with col2:
            if secilen_ders:
                # Konu alanı seçimi
                konu_alanlari = list(yks_konulari[secilen_ders].keys())
                secilen_alan = st.selectbox("Konu Alanı Seç", konu_alanlari, key="alan_secimi")
        
        if secilen_ders and secilen_alan:
            # Alt konu seçimi
            alt_konular = list(yks_konulari[secilen_ders][secilen_alan].keys())
            secilen_alt_konu = st.selectbox("Alt Konu Seç", alt_konular, key="alt_konu_secimi")
        
        if secilen_ders and secilen_alan and secilen_alt_konu:
            # Detay konu seçimi
            detay_konular = yks_konulari[secilen_ders][secilen_alan][secilen_alt_konu]
            secilen_detay = st.selectbox("Detay Konu Seç", detay_konular, key="detay_secimi")
            
            if secilen_detay:
                konu_key = f"{secilen_ders} > {secilen_alan} > {secilen_alt_konu} > {secilen_detay}"
                
                # Seviye belirleme
                mastery_seviyeleri = ["Hiç Bilmiyor", "Temel Bilgi", "Orta Seviye", "İyi Seviye", "Uzman (Derece) Seviye"]
                secilen_seviye = st.select_slider("Konu Seviyesi", options=mastery_seviyeleri, value="Hiç Bilmiyor")
                
                if st.button("Konuyu Kaydet"):
                    st.session_state.konu_durumu[konu_key] = secilen_seviye
                    st.session_state.son_calisma[konu_key] = date.today().strftime("%Y-%m-%d")
                    st.success(f"**{konu_key}** konusu {secilen_seviye} seviyesinde kaydedildi!")
    
    with tab2:
        st.markdown("### Konu Listesi ve İlerleme")
        
        # Filtreleme seçenekleri
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtre_ders = st.selectbox("Derse Göre Filtrele", ["Tümü"] + list(yks_konulari.keys()))
        
        with col2:
            filtre_seviye = st.selectbox("Seviyeye Göre Filtrele", ["Tümü"] + mastery_seviyeleri)
        
        with col3:
            arama = st.text_input("Konu Ara")
        
        # Konuları listele
        for konu, seviye in st.session_state.konu_durumu.items():
            # Filtreleme
            if filtre_ders != "Tümü" and not konu.startswith(filtre_ders):
                continue
            if filtre_seviye != "Tümü" and seviye != filtre_seviye:
                continue
            if arama and arama.lower() not in konu.lower():
                continue
            
            # Seviye indeksini bul
            seviye_index = mastery_seviyeleri.index(seviye)
            renk_sinifi = ders_renki_bul(konu)
            
            st.markdown(f'<div class="subject-card {renk_sinifi}">', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.markdown(f"**{konu}**")
                st.markdown(f'*Son çalışma: {st.session_state.son_calisma.get(konu, "Henüz yok")}*')
            
            with col2:
                st.markdown(f'<div class="progress-container"><div class="progress-bar" style="width: {(seviye_index/4)*100}%">{seviye}</div></div>', unsafe_allow_html=True)
            
            with col3:
                if st.button("🔄", key=f"tekrar_{konu}"):
                    st.session_state.son_calisma[konu] = date.today().strftime("%Y-%m-%d")
                    st.success(f"{konu} için tekrar kaydedildi!")
            
            with col4:
                if st.button("❌", key=f"sil_{konu}"):
                    del st.session_state.konu_durumu[konu]
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Hedef Belirleme")
        
        col1, col2 = st.columns(2)
        
        with col1:
            hedef_ders = st.selectbox("Hedef Ders", list(yks_konulari.keys()))
            hedef_tarih = st.date_input("Hedef Tarih", date.today() + timedelta(days=30))
        
        with col2:
            hedef_yuzde = st.slider("Hedef Tamamlama Yüzdesi", 0, 100, 80)
            oncelik = st.select_slider("Öncelik", options=["Düşük", "Orta", "Yüksek"], value="Orta")
        
        if st.button("Hedefi Kaydet"):
            hedef_key = f"{hedef_ders}_{hedef_tarih.strftime('%Y%m%d')}"
            st.session_state.hedefler[hedef_key] = {
                "ders": hedef_ders,
                "tarih": hedef_tarih.strftime("%Y-%m-%d"),
                "yuzde": hedef_yuzde,
                "oncelik": oncelik
            }
            st.success("Hedef kaydedildi!")
        
        st.markdown("### Mevcut Hedefler")
        for hedef_key, hedef in st.session_state.hedefler.items():
            st.markdown(f'<div class="subject-card">', unsafe_allow_html=True)
            st.markdown(f"**{hedef['ders']}** - %{hedef['yuzde']} tamamlama - {hedef['tarih']} - Öncelik: {hedef['oncelik']}")
            
            # İlerleme durumu
            ders_konulari = [k for k in st.session_state.tum_konular if k.startswith(hedef['ders'])]
            tamamlanan = sum(1 for konu in ders_konulari 
                            if konu in st.session_state.konu_durumu and 
                            st.session_state.konu_durumu[konu] == "Uzman (Derece) Seviye")
            
            if len(ders_konulari) > 0:
                mevcut_yuzde = (tamamlanan / len(ders_konulari)) * 100
                st.markdown(f'<div class="progress-container"><div class="progress-bar" style="width: {mevcut_yuzde}%">{mevcut_yuzde:.1f}%</div></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

elif sayfa == "📚 Öğrenme Araçları":
    st.markdown('<div class="main-header">Öğrenme Araçları ve Teknikleri</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Öğrenme Teknikleri", "Öğrenme Stili", "Motivasyon"])
    
    with tab1:
        st.markdown("### Etkili Öğrenme Teknikleri")
        
        for teknik_adi, teknik in ogrenme_teknikleri.items():
            with st.expander(f"{teknik['icon']} {teknik_adi}"):
                st.markdown(f"**{teknik['açıklama']}**")
                st.markdown("**Adımlar:**")
                for adim in teknik['adımlar']:
                    st.markdown(f"- {adim}")
                
                # Feynman Tekniği için özel uygulama
                if teknik_adi == "Feynman Tekniği" and st.session_state.konu_durumu:
                    st.markdown("---")
                    st.markdown("**Uygulama**")
                    
                    feynman_konu = st.selectbox("Açıklamak istediğiniz konu:", 
                                              list(st.session_state.konu_durumu.keys()),
                                              key="feynman_konu")
                    
                    feynman_aciklama = st.text_area("Konuyu basitçe açıklayın:", 
                                                  height=150,
                                                  key="feynman_aciklama")
                    
                    if st.button("Kaydet", key="feynman_kaydet") and feynman_aciklama:
                        st.session_state.feynman_notlari[feynman_konu] = {
                            "aciklama": feynman_aciklama,
                            "tarih": date.today().strftime("%Y-%m-%d")
                        }
                        st.success("Açıklamanız kaydedildi!")
    
    with tab2:
        st.markdown("### Öğrenme Stilinizi Belirleyin")
        
        if st.button("Öğrenme Stili Testi Yap"):
            # Basit bir öğrenme stili testi
            sorular = [
                "Yeni bir konuyu öğrenirken en çok hangi yöntemi tercih edersiniz?",
                "Bir şeyi hatırlamak istediğinizde genellikle:",
                "Çalışırken nasıl bir ortamı tercih edersiniz?",
                "Bir cihazı nasıl kullanmayı öğrenirsiniz?"
            ]
            
            secenekler = [
                ["Okumak", "Dinlemek", "İzlemek", "Yaparak denemek"],
                ["Yazılı bilgileri hatırlarım", "Sesleri hatırlarım", "Görüntüleri hatırlarım", "Hissettiklerimi hatırlarım"],
                ["Sessiz ve sakin", "Müzikli", "Görsel materyallerle dolu", "Rahat hareket edebileceğim"],
                ["Kılavuzu okurum", "Birine sorarım", "Resimlere bakarak anlarım", "Kendim kurcalayarak öğrenirim"]
            ]
            
            cevaplar = []
            for i, soru in enumerate(sorular):
                cevap = st.radio(soru, secenekler[i], key=f"soru_{i}")
                cevaplar.append(cevap)
            
            if st.button("Testi Tamamla"):
                # Basit bir puanlama sistemi
                puanlar = {"Okuyarak/Yazarak Öğrenenler": 0, 
                          "İşitsel Öğrenenler": 0, 
                          "Görsel Öğrenenler": 0, 
                          "Kinestetik Öğrenenler": 0}
                
                for cevap in cevaplar:
                    if cevap in secenekler[0]:
                        index = secenekler[0].index(cevap)
                        if index == 0: puanlar["Okuyarak/Yazarak Öğrenenler"] += 1
                        elif index == 1: puanlar["İşitsel Öğrenenler"] += 1
                        elif index == 2: puanlar["Görsel Öğrenenler"] += 1
                        else: puanlar["Kinestetik Öğrenenler"] += 1
                
                # En yüksek puanlı stil
                st.session_state.ogrenme_stili = max(puanlar, key=puanlar.get)
                st.success(f"Öğrenme stiliniz: **{st.session_state.ogrenme_stili}**")
        
        if st.session_state.ogrenme_stili != "Henüz belirlenmedi":
            st.markdown(f"### {st.session_state.ogrenme_stili} için Öneriler")
            stil = ogrenme_stilleri[st.session_state.ogrenme_stili]
            
            for tavsiye in stil['tavsiyeler']:
                st.markdown(f"- {tavsiye}")
    
    with tab3:
        st.markdown("### Motivasyon Artırıcı Teknikler")
        
        motivasyon_teknikleri = [
            "Küçük hedefler belirleyin: Büyük hedefi küçük parçalara ayırın",
            "Kendinizi ödüllendirin: Başarılarınızı küçük ödüllerle kutlayın",
            "Olumlu iç konuşma: Kendinize motive edici cümleler söyleyin",
            "Görselleştirme: Başarılı olacağınız anları zihninizde canlandırın",
            "Sosyal destek: Aileniz ve arkadaşlarınızdan destek isteyin",
            "İlerlemeyi takip edin: Günlük ve haftalık ilerlemenizi kaydedin",
            "Esneklik: Programınızda esnek olun, kendinize zaman tanıyın"
        ]
        
        for i, teknik in enumerate(motivasyon_teknikleri):
            st.markdown(f'<div class="motivation-box"><b>{i+1}.</b> {teknik}</div>', unsafe_allow_html=True)
        
        st.markdown("### Motivasyonunu Artır")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("İlham Verici Söz 🎯"):
                sozler = [
                    "Başarı, hazırlık và fırsatın buluştuğu yerdir.",
                    "Bugünün işini yarına bırakma.",
                    "Zorluklar, başarının değerini artıran baharatlardır.",
                    "Hedeflerine ulaşmak için her gün küçük bir adım at.",
                    "En büyük zafer, kendine karşı kazandığın zaferdir."
                ]
                st.info(random.choice(sozler))
        
        with col2:
            if st.button("Başarı Hikayesi 📖"):
                hikayeler = [
                    "Thomas Edison, ampulü icat etmeden önce 1000'den fazla başarısız deneme yaptı.",
                    "J.K. Rowling, Harry Potter kitabı 12 yayınevi tarafından reddedildikten sonra kabul edildi.",
                    "Michael Jordan, lise takımına seçilmemişti ama pes etmedi ve çalışmaya devam etti.",
                    "Walt Disney, ilk animasyon stüdyosu iflas etmişti ama sonraki girişimleriyle efsane oldu.",
                    "Stephen King, ilk romanı Carrie 30 yayınevi tarafından reddedilmişti."
                ]
                st.info(random.choice(hikayeler))
        
        with col3:
            if st.button("Hızlı Motivasyon 🚀"):
                st.session_state.motivasyon = min(100, st.session_state.motivasyon + 10)
                st.success("Motivasyonunuz arttı! 💪")

elif sayfa == "⚙️ Ayarlar":
    st.markdown('<div class="main-header">Ayarlar ve Kişiselleştirme</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### Uygulama Ayarları")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tema = st.selectbox("Tema", ["Açık", "Koyu", "Sistemle Aynı"])
        bildirimler = st.checkbox("Bildirimleri Aç", value=True)
        otomatik_yedekleme = st.checkbox("Otomatik Yedekleme", value=True)
    
    with col2:
        dil = st.selectbox("Dil", ["Türkçe", "İngilizce"])
        zorluk_seviyesi = st.select_slider("Zorluk Seviyesi", options=["Kolay", "Orta", "Zor"])
        hedef_ogrenme_suresi = st.slider("Günlük Hedef Öğrenme Süresi (saat)", 1, 12, 4)
    
    st.markdown("### Veri Yönetimi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Verileri Yedekle", help="Tüm ilerleme verilerinizi yedekler"):
            st.success("Verileriniz yedeklendi! (Simüle edildi)")
    
    with col2:
        if st.button("Verileri Sıfırla", help="Tüm verileri siler (dikkatli kullanın)"):
            if st.checkbox("Emin misiniz? Tüm verileriniz silinecek."):
                st.session_state.konu_durumu = {}
                st.session_state.calisma_gunleri = []
                st.session_state.motivasyon = 100
                st.session_state.hedefler = {}
                st.success("Tüm veriler sıfırlandı!")
    
    st.markdown("### Hakkında")
    st.markdown("""
    **YKS Master Pro** v1.0  
    Profesyonel YKS hazırlık ve konu takip sistemi  
    Geliştirici: Sadd  
    © 2023 Tüm hakları saklıdır.
    """)