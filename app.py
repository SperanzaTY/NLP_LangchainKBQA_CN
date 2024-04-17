from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
from config import Config
from encoder import TextFileEncoder
from document import DocumentService
from chainKBQA import LangChainApplication

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    filename = secure_filename(file.filename)
    file_path = os.path.join(Config.docs_path, filename)
    file.save(file_path)
    reprocess_documents()
    return redirect(url_for('index'))

def reprocess_documents():
    global application
    # 转换文件编码
    encoder = TextFileEncoder(Config.docs_path)
    encoder.convert_files_encoding()

    # 重新向量化文档
    print("开始向量化！")
    text2vec = DocumentService()
    text2vec.init_source_vector()
    print("向量化成功！")

@app.route('/ask', methods=['POST'])
def ask():
    application = LangChainApplication()
    question = request.form['question']
    llm_answer = application.get_llm_answer(question)
    kb_answer = application.get_knowledge_based_answer(question)
    return render_template('index.html', question=question, llm_answer=llm_answer, kb_answer=kb_answer)

if __name__ == '__main__':
    app.run(debug=True)
