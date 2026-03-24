# 🤖 Doküman Asistanı (RAG)

Bu proje, modern web framework dökümantasyonlarını (Next.js vb.) okuyup analiz edebilen, gelişmiş bir RAG (Retrieval-Augmented Generation) asistanıdır.

## 🚀 Özellikler
- **Premium UI/UX**: Streamlit üzerine enjekte edilmiş özel CSS ile karanlık mod ve akıcı animasyonlar.
- **Esnek Veri Kaynağı**: Web URL'lerinden veya yerel PDF dosyalarından veri çekebilir.
- **Gelişmiş RAG**: LangChain ve OpenAI kullanarak dökümanları anlamlandırır.

## 🛠️ Kurulum

1. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. `.env` dosyasını düzenleyin ve OpenAI API anahtarınızı ekleyin:
   ```text
   OPENAI_API_KEY=sk-....
   ```

3. Uygulamayı başlatın:
   ```bash
   streamlit run frontend/app.py
   ```

## 📂 Dosya Yapısı
- `data_ingestion/`: Veri çekme ve işleme (loader, splitter).
- `rag_backend/`: Vektör veritabanı (ChromaDB) ve LLM orkestrasyonu.
- `frontend/`: Streamlit arayüzü ve özel CSS animasyonları.

---
*Üniversite Veri Biliminde İleri Programlama Dersi için geliştirilmiştir.*
