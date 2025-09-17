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


# ----------------- LCS 测试 -----------------
def test_lcs_length_identical():
    assert pc.lcs_length("abc", "abc") == 3

def test_lcs_length_partial():
    assert pc.lcs_length("abcdef", "ace") == 3

def test_lcs_length_empty():
    assert pc.lcs_length("", "abc") == 0
    assert pc.lcs_length("abc", "") == 0


# ----------------- 重复率计算测试 -----------------
def test_compute_duplicate_rate_identical():  #完全相同
    rate = pc.compute_duplicate_rate("今天 天气 晴", "今天 天气 晴")
    assert rate == pytest.approx(100.0)

def test_compute_duplicate_rate_partial():  #部分字符重复
    rate = pc.compute_duplicate_rate("今天 天气 晴", "今天 下雨")
    assert rate == pytest.approx(40.0)

def test_compute_duplicate_rate_empty_orig():  #原文为空
    rate = pc.compute_duplicate_rate("", "任意文本")
    assert rate == pytest.approx(0.0)

def test_compute_duplicate_rate_empty_copy():    #抄袭文本为空
    rate = pc.compute_duplicate_rate("原文有内容", "")
    assert rate == pytest.approx(0.0)

def test_compute_duplicate_rate_whitespace_only():  #原文、抄袭文本都是空格
    rate = pc.compute_duplicate_rate("     ", "  ")
    assert rate == pytest.approx(0.0)

def test_compute_duplicate_rate_punctuation():     #文本含标点
    rate = pc.compute_duplicate_rate("今天，天气晴！", "今天天气晴")
    # 标点符号应该被忽略或不计入 LCS，重复率接近 100%
    assert rate >= 90.0


# ----------------- 主函数文件执行测试 -----------------
def test_main_correct_execution():
    with tempfile.TemporaryDirectory() as tmpdir:
        orig_path = os.path.join(tmpdir, "orig.txt")
        plag_path = os.path.join(tmpdir, "plag.txt")
        out_path = os.path.join(tmpdir, "out.txt")

        with open(orig_path, "w", encoding="utf-8") as f:
            f.write("今天是星期天，天气晴")

        with open(plag_path, "w", encoding="utf-8") as f:
            f.write("今天是周天，天气晴朗")

        sys.argv = ["plagiarism_checker.py", orig_path, plag_path, out_path]
        pc.main()

        with open(out_path, "r", encoding="utf-8") as f:
            result = f.read().strip()

        assert result.replace(".", "").isdigit() and len(result.split(".")[1]) == 2


def test_main_missing_file():
    sys.argv = ["plagiarism_checker.py", "nofile.txt", "also_no.txt", "out.txt"]
    with pytest.raises(SystemExit):
        pc.main()

