from config import Config
from encoder import TextFileEncoder
from chainKBQA import LangChainApplication
from document import DocumentService

# text2vec只能读gbk编码格式的txt文件，这里把txt文件夹下的所有文件都转换成gbk格式，上传的知识文档存储在Config.docs_path当中
encoder = TextFileEncoder(Config.docs_path)
encoder.convert_files_encoding()

#将文本分块向量化存储起来
text2vec = DocumentService()
text2vec.init_source_vector()

# 实例化模型
application = LangChainApplication()
question = '香港城市大学建校于哪一年？'
print(question)

# 直接调用llm模型回答
llm_result = application.get_llm_answer(question)
print("llm_result:" + llm_result)

# 结合文档回答,调用数据按照下面print格式中的部分调用
kb_result = application.get_knowledge_based_answer(question)
print("查询问题是：", kb_result['query'])
print("查询结果是：", kb_result['result'])
print("来源文档的内容是：", kb_result['source_documents'][0].page_content)
print("来源文档的元数据是：", kb_result['source_documents'][0].metadata)

encoder = TextFileEncoder(Config.docs_path)
encoder.convert_files_encoding()

