import pytest
import os
import tempfile
import sys
import main as pc


# ----------------- 文件读取测试 -----------------
def test_read_file():
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
        tmp.write("hello world")
        tmp_path = tmp.name
    content = pc.read_file(tmp_path)
    assert content == "hello world"
    os.remove(tmp_path)


# ----------------- 文本规范化测试 -----------------
def test_normalize_text():
    text = "今天 是 星期天，天气晴！Hello, World。"
    normalized = pc.normalize_text(text)
    assert normalized == "今天是星期天天气晴hello world".replace(" ", "")




