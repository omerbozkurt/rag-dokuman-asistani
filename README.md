# 🤖 Doküman Asistanı (RAG)

Bu proje, yerel dökümanlarınızı (Markdown vb.) analiz edebilen ve onları kaynak göstererek sorularınızı yanıtlayan gelişmiş bir **RAG (Retrieval-Augmented Generation)** asistanıdır.

## 🚀 Özellikler
- **Google Gemini AI**: Soruları yanıtlamak için en güncel ve güçlü yapay zeka modellerinden birini kullanır.
- **FAISS Vektör DB**: Dökümanlar içinde milisaniyeler içinde arama yapar.
- **Premium UI/UX**: Streamlit ve özel CSS ile modern, akıcı ve kullanıcı dostu bir arayüz.
- **Kaynak Gösterme**: Verdiği her yanıt için dökümanın hangi kısmından yararlandığını belirtir.

## 🛠️ Kurulum

1. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. `.env` dosyasını oluşturun ve Google API anahtarınızı ekleyin:
   ```text
   GOOGLE_API_KEY=AIzaSy...
   ```

3. Dökümanları işleyin (İlk çalıştırmada):
   ```bash
   python data_ingestion/md_ingestor.py
   ```

4. Uygulamayı başlatın:
   ```bash
   streamlit run frontend/app.py
   ```

## 📂 Dosya Yapısı
- `data_ingestion/`: Markdown dosyalarını okuma, parçalama ve JSON olarak hazırlama.
- `rag_backend/`: Gemini entegrasyonu, FAISS vektör veritabanı yönetimi ve konfigürasyon.
- `frontend/`: Streamlit chat arayüzü, özel CSS animasyonları ve bileşenler.

---
*Üniversite Veri Biliminde İleri Programlama Dersi için geliştirilmiştir.*
