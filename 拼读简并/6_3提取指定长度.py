
#%%
from collections import defaultdict

#%%
filepath = r'E:\Downloads\output_codes.txt'

# 直接按文本方式读取
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 解析数据，跳过开头到"..."之间的说明信息
entries = []
reading_data = False
two_char_entries = []  # 专门存储2字词组

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
            
            # 如果词组正好是2个字，单独存储
            if len(text) == 2:
                two_char_entries.append((text, full_code, stem))

print(f"成功读取 {len(entries)} 条数据")
print(f"其中2字词组: {len(two_char_entries)} 条\n")

print("=== 所有2字词组列表 ===")
for i, (text, full_code, stem) in enumerate(two_char_entries, 1):
    print(f"{i}. {text}\t{full_code}\t{stem}")

print(f"\n=== 汇总 ===")
print(f"总条目数: {len(entries)}")
print(f"2字词组数: {len(two_char_entries)}")

# 可选：保存到文件
output_file = r'E:\Downloads\two_char_entries.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    for text, full_code, stem in two_char_entries:
        f.write(f"{text}\t{full_code}\t{stem}\n")

print(f"\n已保存到: {output_file}")

# %% 和pdbj.word.dict.yaml比较，重复的就删除
from collections import defaultdict

# 读取2字词组文件
two_char_file = r'E:\Downloads\two_char_entries.txt'
word_dict_file = r'D:\RIME_config\pdbj_dict\pdbj.word.dict.yaml'

# 读取2字词组
two_char_entries = []
with open(two_char_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            parts = line.split('\t')
            if len(parts) >= 2:
                text = parts[0]
                code = parts[1]
                stem = parts[2] if len(parts) >= 3 else ''
                two_char_entries.append((text, code, stem))

print(f"读取到 {len(two_char_entries)} 个2字词组\n")

# 读取词库文件
word_dict_entries = {}
reading_data = False

with open(word_dict_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        
        if line == '...':
            reading_data = True
            continue
        
        if reading_data and line:
            parts = line.split('\t')
            if len(parts) >= 2:
                text = parts[0]
                code = parts[1]
                # 使用 (text, code) 作为唯一键
                word_dict_entries[(text, code)] = True

print(f"读取到 {len(word_dict_entries)} 个词库条目\n")

# 找出需要删除的条目（词组和编码都相同）
to_remove = []
keep_entries = []

for entry in two_char_entries:
    text, code, stem = entry
    key = (text, code)
    if key in word_dict_entries:
        to_remove.append(entry)
    else:
        keep_entries.append(entry)

print(f"发现 {len(to_remove)} 个重复条目（词组和编码完全相同）\n")

# 显示将被删除的条目
print("=== 将被删除的条目 ===")
for text, code, stem in to_remove:
    print(f"{text}\t{code}\t{stem}")

# 保存去重后的2字词组
output_file = r'E:\Downloads\two_char_entries_cleaned.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    for text, code, stem in keep_entries:
        f.write(f"{text}\t{code}\t{stem}\n")

print(f"\n=== 汇总 ===")
print(f"原始2字词组数: {len(two_char_entries)}")
print(f"删除重复条目数: {len(to_remove)}")
print(f"剩余2字词组数: {len(keep_entries)}")
print(f"已保存到: {output_file}")

# %%
