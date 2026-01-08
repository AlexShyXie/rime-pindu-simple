

#%%
from collections import defaultdict

filepath = r'D:\RIME_config\pdbj_dict\pdbj.charfull_flypy.dict.yaml'
filepath = r'D:\RIME_config\pdbj_dict\pdbj.word.dict.yaml'
# filepath = r'E:\Downloads\output_codes.txt'
# 直接按文本方式读取
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 解析数据，跳过开头到"..."之间的说明信息
entries = []
reading_data = False

for line in lines:
    line = line.rstrip('\n\r')
    
    # 遇到"..."标记，开始读取数据
    if line.strip() == '...':
        reading_data = True
        continue
    
    # 只要在"..."之后就读取数据
    if reading_data and line.strip():
        parts = line.split('\t')
        # 至少要有2列
        if len(parts) >= 2:
            text = parts[0]
            full_code = parts[1]
            # 如果有第3列就用，没有就设为空字符串
            stem = parts[2] if len(parts) >= 3 else ''
            entries.append((text, full_code, stem))

print(f"成功读取 {len(entries)} 条数据\n")

# 统计6位全码重复
code_map = defaultdict(list)

for text, full_code, _ in entries:
    if len(full_code) == 6:  # 只统计6位全码
        code_map[full_code].append(text)

# 找出重复的全码
duplicate_codes = {code: chars for code, chars in code_map.items() if len(chars) > 1}

print(f"IME配置文件路径: {filepath}")
print("=== 6位全码重复统计（按重复次数排序）===")
print(f"发现 {len(duplicate_codes)} 个6位全码有重复\n")

# 按重复次数从大到小排序
sorted_duplicates = sorted(duplicate_codes.items(), key=lambda x: len(x[1]), reverse=True)

for code, chars in sorted_duplicates:
    print(f"全码: {code}  重复次数: {len(chars)}")
    print(f"  对应字:")
    for char in chars:
        print(f"    {char}")
    print()

print("=== 汇总 ===")
print(f"总条目数: {len(entries)}")
total_6code = len(code_map)
print(f"唯一6位全码数: {total_6code}")
print(f"重复6位全码数: {len(duplicate_codes)}")
print(f"重复率: {len(duplicate_codes)}/{total_6code} ({len(duplicate_codes)/total_6code*100:.2f}%)")

# %% 统计612个一击词
#%%
from collections import defaultdict

filepath = r'D:\RIME_config\pdbj.wordoneshot.dict.yaml'
"""统计编码末位是a结尾的所有词，并提取相关条目"""

# 直接按文本方式读取
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 解析数据
entries = []
reading_data = False

for line in lines:
    line = line.rstrip('\n\r')
    
    if line.strip() == '...':
        reading_data = True
        continue
    
    if reading_data and line.strip():
        parts = line.split('\t')
        if len(parts) == 2:
            text = parts[0]
            full_code = parts[1]
            entries.append((text, full_code))

print(f"成功读取 {len(entries)} 条数据\n")

# 1. 构建词到所有编码的映射（反向查找）
word_to_codes = defaultdict(list)
for text, full_code in entries:
    word_to_codes[text].append(full_code)

# 2. 找出编码末位是 'a' 结尾的所有词
a_ending_entries = []
for text, full_code in entries:
    if full_code.endswith('a'):
        a_ending_entries.append((text, full_code))

print(f"=== 编码末位是 'a' 结尾的词统计 ===")
print(f"发现 {len(a_ending_entries)} 个词\n")

# 3. 提取这些词对应的编码的所有条目
a_ending_codes = set(entry[1] for entry in a_ending_entries)
all_entries_for_a_codes = defaultdict(list)

for text, full_code in entries:
    if full_code in a_ending_codes:
        all_entries_for_a_codes[full_code].append((text, full_code))

# 4. 找到每个编码前两位对应的第1个出现的条目
prefix_first_entry = defaultdict(list)  # 前两位 -> (text, full_code)
prefix_all_entries = defaultdict(list)  # 前两位 -> 所有条目

for text, full_code in entries:
    if len(full_code) >= 2:
        prefix = full_code[:2]
        if prefix not in prefix_first_entry:
            prefix_first_entry[prefix].append((text, full_code))
        prefix_all_entries[prefix].append((text, full_code))

len(prefix_first_entry)
# 5. 收集所有需要的条目
all_needed_entries = []
used_entries = set()  # 改为存储 (text, full_code) 元组

for code in sorted(all_entries_for_a_codes.keys()):
    # 获取该编码的所有条目
    all_words = all_entries_for_a_codes[code]
    a_ending_words = [t for t, c in a_ending_entries if c == code]
    
    # 输出详细信息
    print(f"\n编码: {code}")
    print(f"  该编码第1个出现的词: {all_words[0][0]}")
    print(f"  编码末位是 'a' 的词: {a_ending_words}")
    print(f"  该编码的所有词: {[t for t, c in all_words]}")
    
    # 步骤1: 添加该编码的所有条目
    for text, full_code in all_words:
        entry_key = (text, full_code)
        if entry_key not in used_entries:
            all_needed_entries.append((text, full_code))
            used_entries.add(entry_key)
    
    # 步骤2: 找到以 'a' 结尾的词的所有编码
    for word in a_ending_words:
        if word in word_to_codes:
            print(f"  '{word}' 的所有编码: {word_to_codes[word]}")
            # 添加该词的所有编码条目
            for other_code in word_to_codes[word]:
                entry_key = (word, other_code)
                if entry_key not in used_entries:
                    all_needed_entries.append((word, other_code))
                    used_entries.add(entry_key)
    
    # 步骤3: 添加该编码前两位对应的第1个条目
    if len(code) >= 2:
        prefix = code[:2]
        if prefix in prefix_first_entry:
            print(f"  前两位 '{prefix}' 的所有条目数: {len(prefix_first_entry[prefix])}")
            for text, full_code in prefix_first_entry[prefix]:
                entry_key = (text, full_code)
                if entry_key not in used_entries:
                    all_needed_entries.append((text, full_code))
                    used_entries.add(entry_key)

# 6. 输出汇总统计
print(f"\n=== 汇总 ===")
print(f"涉及的以 'a' 结尾的编码数: {len(all_entries_for_a_codes)}")
print(f"以 'a' 结尾的词总数: {len(a_ending_entries)}")
print(f"收集到的所有条目数: {len(all_needed_entries)}")

# 7. 输出新词库
print(f"\n=== 新词库 ===")
for text, code in reversed(all_needed_entries):
    print(f"{text}\t{code}")



# %%
