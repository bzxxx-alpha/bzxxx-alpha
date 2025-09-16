import sys
import os
import re

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def normalize_text(s):
    # 去掉空白字符（空格、制表、换行）
    s = re.sub(r'\s+', '', s)
    # 去掉常见标点（保留中英文数字和字母和中文字符）
    # 这里用一个简单的方式：删除 ASCII 标点和常见中文标点
    punct_pattern = r"[，。！？；：、,.!?;:\"'()（）\[\]【】<>《》—\-…·/\\]"
    s = re.sub(punct_pattern, '', s)
    # 将英文字母小写化
    s = s.lower()
    return s

