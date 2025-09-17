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
    # 删除 ASCII 标点和常见中文标点
    punct_pattern = r"[，。！？；：、,.!?;:\"'()（）\[\]【】<>《》—\-…·/\\]"
    s = re.sub(punct_pattern, '', s)
    # 将英文字母小写化
    s = s.lower()
    return s


def lcs_length(a, b):
    """
    经典动态规划求解最长公共子序列长度（空间优化到两行）
    """
    n = len(a)
    m = len(b)
    if n == 0 or m == 0:
        return 0

    # 让 m >= n，减少内存占用
    if m < n:
        a, b = b, a
        n, m = m, n

    prev = [0] * (m + 1)
    curr = [0] * (m + 1)

    for i in range(1, n + 1):
        ai = a[i - 1]
        for j in range(1, m + 1):
            if ai == b[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(curr[j - 1], prev[j])
        prev, curr = curr, prev  # 交换引用，复用数组

    return prev[m]


def compute_duplicate_rate(orig_text, plag_text, as_percentage=True):
    o = normalize_text(orig_text)
    p = normalize_text(plag_text)
    if len(o) == 0:
        return 0.0

    L = lcs_length(o, p)
    rate = L / len(o)
    if as_percentage:
        rate *= 100.0
    return rate

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <orig_path> <plag_path> <out_path>")
        sys.exit(2)

    orig_path = sys.argv[1]
    plag_path = sys.argv[2]
    out_path = sys.argv[3]

    if not os.path.isfile(orig_path):
        print("原文文件不存在:", orig_path)
        sys.exit(2)
    if not os.path.isfile(plag_path):
        print("抄袭版文件不存在:", plag_path)
        sys.exit(2)

    orig_text = read_file(orig_path)
    plag_text = read_file(plag_path)
    rate = compute_duplicate_rate(orig_text, plag_text, as_percentage=True)

    # 写入答案文件，保留两位小数
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("{:.2f}".format(rate))


if __name__ == '__main__':
    main()

