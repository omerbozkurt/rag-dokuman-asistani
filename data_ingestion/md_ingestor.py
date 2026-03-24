import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MarkdownIngestor:
    """
    Markdown dosyalarını okuyan, parçalara (chunk) bölen ve 
    metadata ile birlikte JSON formatında dışa aktaran sınıf.
    """

    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n## ", "\n### ", "\n#### ", "\n", " ", ""]
        )

    def extract_title(self, content: str) -> str:
        """Markdown içeriğinden ilk # başlığını çıkarır."""
        for line in content.split("\n"):
            if line.startswith("# "):
                return line.replace("# ", "").strip()
        return "Başlıksız Döküman"

    def process_folder(self, input_folder: str) -> List[Dict[str, Any]]:
        """Klasördeki tüm .md dosyalarını işler."""
        processed_data = []
        folder_path = Path(input_folder)

        if not folder_path.exists():
            logger.error(f"Hata: '{input_folder}' klasörü bulunamadı.")
            return []

        logger.info(f"'{input_folder}' klasöründeki .md dosyaları taranıyor...")

        for md_file in folder_path.glob("**/*.md"):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()

                title = self.extract_title(content)
                filename = md_file.name

                # Metni parçalara böl
                chunks = self.text_splitter.split_text(content)

                for i, chunk in enumerate(chunks):
                    processed_data.append({
                        "id": f"{filename}_{i}",
                        "text": chunk,
                        "metadata": {
                            "source": filename,
                            "title": title,
                            "chunk_index": i
                        }
                    })
                
                logger.info(f"Başarıyla işlendi: {filename} ({len(chunks)} parça)")

            except Exception as e:
                logger.error(f"'{md_file.name}' işlenirken hata oluştu: {str(e)}")

        return processed_data

    def save_to_json(self, data: List[Dict[str, Any]], output_file: str):
        """İşlenen verileri JSON dosyasına kaydeder."""
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_all_ascii=False, indent=4)
            
            logger.info(f"İşlem tamamlandı! Veriler '{output_file}' dosyasına kaydedildi. Toplam parça: {len(data)}")

        except Exception as e:
            logger.error(f"JSON kaydedilirken hata oluştu: {str(e)}")

if __name__ == "__main__":
    # Örnek kullanım
    INPUT_DIR = "docs" # Buraya markdown dosyalarınızın olduğu klasörü girin
    OUTPUT_FILE = "data/processed_docs.json"

    # Eğer docs klasörü yoksa test için oluştur (kullanıcıya kolaylık)
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        with open(f"{INPUT_DIR}/example.md", "w", encoding="utf-8") as f:
            f.write("# Örnek Başlık\nBu bir test dökümanıdır.\n\n## Alt Başlık\nİçerik buraya gelir.")
        logger.info(f"'{INPUT_DIR}' klasörü bulunamadığı için örnek bir dosya ile oluşturuldu.")

    ingestor = MarkdownIngestor()
    data = ingestor.process_folder(INPUT_DIR)
    
    if data:
        ingestor.save_to_json(data, OUTPUT_FILE)
    else:
        logger.warning("İşlenecek veri bulunamadı.")
