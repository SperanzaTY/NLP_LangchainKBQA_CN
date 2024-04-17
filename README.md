# LongChainKBQA
#### 项目技术
+  ChatYuan-large-v2 大语言模型进行基于知识库的问答 
+  nlp_bert_document-segmentation_chinese-base 语义分割模型对文本进行拆分
+  text2vec-large-chinese 模型 对文本向量化  
+  faiss进行向量检索
+  langchain 进行各个模块的组合，并完成基于知识库的问答
#### 项目结构
+ config.py：配置文件,配置llm模型和文本向量化模型
+ document.py：文本拆分和文本向量化
+ llm.py：大语言模型加载
+ chainKBQA.py：利用文本向量化搜索和大语言模型进行知识库问答

#### 项目使用
+ 运行document.py 主函数对文本进行拆分以及向量化
+ 运行chainKBQA.py 加载文本向量和llm模型进行知识问答

