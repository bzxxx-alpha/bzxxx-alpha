import re
import sys
import os

def read_file(path):
    """读取文件内容"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def normalize_text(s):
    """文本规范化：去空白字符、去标点、英文小写化"""
    s = re.sub(r'\s+', '', s)
    punct_pattern = r"[，。！？；：、,.!?;:\"'()（）\[\]【】<>《》—\-…·/\\]"
    s = re.sub(punct_pattern, '', s)
    return s.lower()

def lcs_length(a, b):
    """标准 LCS，滚动数组优化空间"""
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return 0
    if m < n:  # 保证 b 更长，节省空间
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
        prev, curr = curr, prev
    return prev[m]

def compute_duplicate_rate_segmented(orig_text, plag_text, seg_len=1000, as_percentage=True):
    """分段 LCS 重复率计算"""
    o = normalize_text(orig_text)
    p = normalize_text(plag_text)
    if len(o) == 0:
        return 0.0

    total_lcs = 0
    total_len = len(o)

    # 按 seg_len 分段
    for i in range(0, len(o), seg_len):
        o_seg = o[i:i+seg_len]
        p_seg = p[i:i+seg_len]  # 简单对齐切分，也可用滑动窗口改进
        total_lcs += lcs_length(o_seg, p_seg)

    rate = total_lcs / total_len
    if as_percentage:
        rate *= 100
    return rate

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <orig_path> <plag_path> <out_path>")
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

    # 修正调用：compute_duplicate_rate_segmented 不接受 n 参数
    rate = compute_duplicate_rate_segmented(orig_text, plag_text, as_percentage=True)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("{:.2f}".format(rate))

if __name__ == '__main__':
    main()
