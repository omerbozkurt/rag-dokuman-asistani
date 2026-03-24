from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def process_documents(self, documents):
        """Dökümanları küçük parçalara (chunks) ayırır."""
        return self.text_splitter.split_documents(documents)
