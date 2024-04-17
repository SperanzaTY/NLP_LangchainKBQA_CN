import os
import chardet

class TextFileEncoder:
    def __init__(self, directory):
        self.directory = directory
    
    def detect_encoding(self, file_path):
        with open(file_path, 'rb') as file:  # 读取二进制模式
            raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

    def convert_to_gbk(self, file_path, original_encoding):
        with open(file_path, 'r', encoding=original_encoding) as file:
            content = file.read()
        with open(file_path, 'w', encoding='gbk') as file:
            file.write(content)
    
    def convert_files_encoding(self):
        for filename in os.listdir(self.directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.directory, filename)
                current_encoding = self.detect_encoding(file_path)
                
                if current_encoding != 'gbk':
                    try:
                        self.convert_to_gbk(file_path, current_encoding)
                        print(f"文件 {filename} 已从 {current_encoding} 转换为 GBK 编码。")
                    except UnicodeDecodeError as e:
                        print(f"文件 {filename} 不能从 {current_encoding} 转换为 GBK 编码: {e}")
                else:
                    print(f"文件 {filename} 已经是 GBK 编码。")

# 使用类
if __name__ == '__main__':
    directory_path = 'resource/txt'
    encoder = TextFileEncoder(directory_path)
    encoder.convert_files_encoding()
