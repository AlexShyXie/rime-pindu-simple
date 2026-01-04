# %%
import pandas as pd
import re
from collections import defaultdict
# 3charfull全码补充只有3码的

#%% 【步骤1】读取 0radical_keys.csv
csv_file_path = r"E:\E_hobbies\百度输入法皮肤修改\FlypyBingji-main\拼读简并\0radical_keys.csv"
df = pd.read_csv(csv_file_path, encoding='utf-8-sig')

print(f"✓ 读取CSV文件: {csv_file_path}")
print(f"  共 {len(df)} 行数据")

# 初始化字典
# 存所有部首对应的code（不再区分声母，只要有效code都存）
radical_to_code_all = {}

# 遍历每一行
for index, row in df.iterrows():
    sheng = row['sheng']
    buzhou = row['buzhou']
    code = row['code']
    
    # 跳过空值
    if pd.isna(sheng) or pd.isna(buzhou):
        continue
    
    if pd.notna(code):
        # 1. 提取括号外的偏旁（去掉括号）
        buzhou_clean = re.sub(r'[（）()]', '', buzhou)
        
        # 2. 提取括号内的偏旁
        radicals_in_parentheses = re.findall(r'[（(]([^）)]*)[）)]', buzhou)
        
        # 3. 组合所有偏旁
        all_radicals = list(buzhou_clean)
        for r in radicals_in_parentheses:
            if r:
                all_radicals.extend(list(r))
        
        # 4. 去重并建立映射
        unique_radicals = set(all_radicals)
        for radical in unique_radicals:
            if radical.strip():
                # 存入字典，只要有code就存
                radical_to_code_all[radical] = code

print(f"✓ 解析完成，共 {len(radical_to_code_all)} 个部首映射(所有声母)")

# %%
# 【步骤2】读取 assembly.txt，建立 字 -> 部首 的映射
assembly_file_path = r"G:\OneDrive - csu.edu.cn\重要软件备份\输入法\拼读并击250412\lua\pdbj\assembly.txt"

char_to_radical_map = {}

with open(assembly_file_path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

print(f"✓ 读取assembly文件: {assembly_file_path}")
print(f"  共 {len(lines)} 行")

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    if '\t' not in line:
        continue
    
    char, radical = line.split('\t', 1)
    char_to_radical_map[char] = radical
# %%
# 【步骤3】逐行读取、处理、写入
input_file_path = r"E:\E_hobbies\百度输入法皮肤修改\FlypyBingji-main\拼读简并\pdbj.char.dict.yaml"
output_file_path = r"E:\E_hobbies\百度输入法皮肤修改\FlypyBingji-main\拼读简并\pdbj.char_modified.dict.yaml"

modifications = []

print(f"✓ 开始处理: {input_file_path}")

# 同时打开输入和输出文件
with open(input_file_path, 'r', encoding='utf-8') as infile, \
     open(output_file_path, 'w', encoding='utf-8') as outfile:
    
    for line in infile:
        line = line.rstrip('\n')  # 保留原始行的格式（包括\t），只去掉末尾换行
        
        # 跳过空行和注释
        if not line.strip() or line.startswith('#'):
            outfile.write(line + '\n')
            continue
        
        # 按tab分割
        parts = line.split('\t')
        if len(parts) < 2:
            outfile.write(line + '\n')
            continue
        
        char = parts[0]
        codes = parts[1:]
        
        # 检查这个字是否在assembly映射表中
        if char not in char_to_radical_map:
            # 不在映射表，直接原样写入
            outfile.write(line + '\n')
            continue
        
        # 获取部首
        radical = char_to_radical_map[char]
        
        # 检查部首是否在部首code映射表中
        if radical not in radical_to_code_all:
            # 部首不在映射表，直接原样写入
            outfile.write(line + '\n')
            continue
        
        # 遍历这一行的所有编码
        modified_codes = []
        line_modified = False
        
        for code in codes:
            # 只处理3个字母的编码
            if len(code) == 3 and code.isalpha():
                target_suffix = radical_to_code_all[radical]
                new_code = code + target_suffix
                
                modifications.append({
                    'char': char,
                    'radical': radical,
                    'old_code': code,
                    'new_code': new_code,
                    'reason': '补全3码'
                })
                
                modified_codes.append(new_code)
                line_modified = True
            else:
                # 不是3个字母，保持原样
                modified_codes.append(code)
        
        # 写入处理后的行
        if line_modified:
            new_line = char + '\t' + '\t'.join(modified_codes)
            outfile.write(new_line + '\n')
        else:
            # 没有修改，写入原行
            outfile.write(line + '\n')

print(f"✓ 处理完成，结果已保存到: {output_file_path}")

# 打印修改结果
print(f"\n找到 {len(modifications)} 个需要处理的编码")
for i, mod in enumerate(modifications[:20]):
    print(f"{i+1}. 字: {mod['char']} | 部首: {mod['radical']} | {mod['old_code']} -> {mod['new_code']}")

# %%
