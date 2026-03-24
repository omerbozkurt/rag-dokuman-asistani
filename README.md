<div align="center">
  <img src="https://img.icons8.com/bubbles/200/robot.png" width="100" />
  <h1>🚀 Doküman Asistanı (RAG)</h1>
  <p><b>Yapay Zeka Destekli Akıllı Dökümantasyon Analizi ve Soru-Cevap Sistemi</b></p>
  
  ![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
  ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
  ![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google-gemini&logoColor=white)
  ![FAISS](https://img.shields.io/badge/FAISS-Vektör--DB-lightgrey?style=for-the-badge)
</div>

---

## ✨ Proje Hakkında
Bu proje, dökümanlarınızı (Markdown) analiz eden ve onları kaynak göstererek sorularınızı yanıtlayan gelişmiş bir **RAG (Retrieval-Augmented Generation)** asistanıdır. Google Gemini API'nin güçlü dil modellerini FAISS vektör veritabanı ile birleştirerek size milisaniyeler içinde doğru ve güvenilir yanıtlar sunar.

### 🌟 Öne Çıkan Özellikler
- 🧠 **Zeki Analiz:** Google Gemini ile döküman içeriğini derinlemesine anlar.
- ⚡ **Online Yükleme:** Dosyaları doğrudan tarayıcınızdan sürükleyip bırakın.
- 📚 **Kaynak Gösterme:** Her yanıtın hangi dökümandan alındığını şeffafça belirtir.
- 🎨 **Premium Arayüz:** Modern "Midnight Aurora" teması, cam efekti ve akıcı animasyonlar.
- ☁️ **Bulut Uyumlu:** Streamlit Cloud ile tek tıkla her yerden erişim.

---

## 🛠️ Hızlı Kurulum (Yerel Çalıştırma)

Bilgisayarınızda çalıştırmak için aşağıdaki 3 basit adımı izleyin:

### 1. Dosyaları Hazırlayın
Projeyi indirin ve gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

### 2. API Anahtarınızı Ekleyin
Proje ana dizininde `.env` adında bir dosya oluşturun ve içine Google API anahtarınızı yapıştırın:
```env
GOOGLE_API_KEY=Burası_Sizin_API_Anahtarınız
```

### 3. Uygulamayı Başlatın
Sadece şu komutu çalıştırın:
```bash
streamlit run frontend/app.py
```

---

## 📁 Dosya Yapısı
```text
├── 📂 data_ingestion  # Veri işleme ve okuma mantığı
├── 📂 frontend        # Kullanıcı arayüzü ve tasarım
│   ├── 📂 assets      # CSS ve görsel dosyalar
│   └── 📂 components  # UI bileşenleri
├── 📂 rag_backend     # Gemini ve Vektör DB entegrasyonu
├── 📂 docs            # Kaynak dökümanlarınız (.md)
└── 📄 app.py          # Ana uygulama dosyası
```


