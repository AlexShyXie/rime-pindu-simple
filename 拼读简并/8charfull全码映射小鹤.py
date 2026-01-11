
# %%-*- coding: utf-8 -*-
import pandas as pd

# ============== 配置文件路径 ==============
# 请修改为你的实际文件路径
radical_file = r"D:\RIME_config\flypy\小鹤拆分+部首tab格式.txt"  # 格式：一\t一|a
mapping_csv = "8_字母映射编码.csv"
dict_yaml = r"D:\RIME_config\pdbj.charfull.dict.yaml"
output_yaml = r"D:\RIME_config\pdbj.charfull_modified.dict.yaml"
# =======================================

# %%========== 步骤1: 读取映射表 ==========
print("步骤1: 读取字母映射编码表...")
df_mapping = pd.read_csv(mapping_csv, encoding='utf-8-sig')

# 创建 小写字母 -> code 的映射
alpha_to_code = {}
for _, row in df_mapping.iterrows():
    alpha = row['alpha']  # 例如：aZZ
    code = row['code']     # 例如：Q
    if len(alpha) > 0:
        first_char = alpha[0].lower()  # 转成小写作为key
        alpha_to_code[first_char] = code

print(f"  ✓ 加载了 {len(alpha_to_code)} 个映射关系")

# 打印映射表，方便调试
print("\n  映射表（前10个）：")
for k in sorted(list(alpha_to_code.keys())):
    print(f"    {k} -> {alpha_to_code[k]}")

#%% ========== 步骤2: 读取小鹤拆分文件 ==========
print(f"\n步骤2: 读取小鹤拆分文件: {radical_file}")
char_to_target_code = {}

with open(radical_file, 'r', encoding='utf-8-sig') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split('\t')
        if len(parts) < 2:
            continue
        
        char = parts[0]  # 字
        radical_info = parts[1]
        
        if '|' not in radical_info:
            continue
        
        radical_parts = radical_info.split('|')
        first_shape = radical_parts[0]  # 首形
        shape_code = radical_parts[1] if len(radical_parts) > 1 else ''  # 编码，比如a
        
        # 在映射表中查找对应的code
        target_code = alpha_to_code.get(shape_code.lower(), '')
        if target_code:
            char_to_target_code[char] = {
                'first_shape': first_shape,
                'shape_code': shape_code,
                'target_code': target_code
            }

print(f"  ✓ 加载了 {len(char_to_target_code)} 个字的映射关系")

# 打印前10个字的映射，方便调试
print("\n  字映射表（前10个）：")
for char, info in list(char_to_target_code.items())[:10]:
    print(f"    {char} | 首形:{info['first_shape']} 编码:{info['shape_code']} -> {info['target_code']}")

# %%========== 步骤3: 处理字典文件 ==========
print(f"\n步骤3: 处理字典文件: {dict_yaml}")
modifications = []

with open(dict_yaml, 'r', encoding='utf-8') as infile, \
     open(output_yaml, 'w', encoding='utf-8') as outfile:
    
    for line in infile:
        line = line.rstrip('\n')
        
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
        
        # 检查这个字是否有目标映射
        if char not in char_to_target_code:
            outfile.write(line + '\n')
            continue
        
        # 获取目标编码
        target_code = char_to_target_code[char]['target_code']
        
        # 处理编码
        modified_codes = []
        line_modified = False
        
        for i, code in enumerate(codes):
            # 只处理字母编码
            if not code.isalpha():
                modified_codes.append(code)
                continue
            
            # 只处理第一个6位字母的编码
            if i == 0 and len(code) == 6:
                # 替换后3位
                new_code = code[:3] + target_code
                modifications.append({
                    'char': char,
                    'first_shape': char_to_target_code[char]['first_shape'],
                    'shape_code': char_to_target_code[char]['shape_code'],
                    'target_code': target_code,
                    'old_code': code,
                    'new_code': new_code
                })
                modified_codes.append(new_code)
                line_modified = True
            else:
                # 其他编码保持原样
                modified_codes.append(code)
        
        # 写入处理后的行
        if line_modified:
            new_line = char + '\t' + '\t'.join(modified_codes)
            outfile.write(new_line + '\n')
        else:
            outfile.write(line + '\n')

print(f"  ✓ 处理完成，结果保存到: {output_yaml}")
print(f"  ✓ 共修改 {len(modifications)} 个编码")

# 打印修改结果
if modifications:
    print("\n修改详情：")
    for mod in modifications[:20]:
        print(f"  字:{mod['char']} | 首形:{mod['first_shape']} 编码:{mod['shape_code']} -> {mod['target_code']} | {mod['old_code']} -> {mod['new_code']}")


# %%
