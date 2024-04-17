from langchain_community.document_loaders import UnstructuredFileLoader, TextLoader, DirectoryLoader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import Config
from utils.AliTextSplitter import AliTextSplitter
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

class DocumentService(object):
    def __init__(self):

        self.config = Config.vector_store_path
        self.embeddings = HuggingFaceEmbeddings(model_name=Config.embedding_model_name)
        self.docs_path = Config.docs_path
        self.vector_store_path = Config.vector_store_path
        self.vector_store = None
    
    def load_text_file(self, file_path, encoding='utf-8'):
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
        
    def init_source_vector(self):
        """
        初始化本地知识库向量
        :return:
        """
        text_loader_kwargs={'autodetect_encoding': True}
        loader = DirectoryLoader(self.docs_path, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
        # 读取文本文件
        documents = loader.load()

        """
        # 新的加载方式
        documents = []
        for root, dirs, files in os.walk(self.docs_path):
            for filename in files:
                if filename.endswith('.txt'):
                    file_path = os.path.join(root, filename)
                    try:
                        document = self.load_text_file(file_path)
                        documents.append(document)
                    except UnicodeDecodeError as e:
                        print(f"无法读取文件 {file_path}：{e}")
        """

                        
        text_splitter = AliTextSplitter()
        # 使用阿里的分段模型对文本进行分段
        split_text = text_splitter.split_documents(documents)
        """
        split_text = []
        for document_content in documents:  # 这里documents是一个包含文档内容的字符串列表
            split_text.extend(text_splitter.split_text(document_content))

        """
        # 采用embeding模型对文本进行向量化
        self.vector_store = FAISS.from_documents(split_text, self.embeddings)
        # 把结果存到faiss索引里面
        self.vector_store.save_local(self.vector_store_path)

    def load_vector_store(self):
        self.vector_store = FAISS.load_local(self.vector_store_path, self.embeddings,allow_dangerous_deserialization=True)



if __name__ == '__main__':
    s = DocumentService()
    ###将文本分块向量化存储起来
    s.init_source_vector()
