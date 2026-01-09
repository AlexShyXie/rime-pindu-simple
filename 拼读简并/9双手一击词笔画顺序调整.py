#%%

# 读取原始词库文件
with open(r'E:\E_hobbies\百度输入法皮肤修改\rime-pindu-simple\pdbj_dict\pdbj.wordoneshot.dict.yaml', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 编码转换规则
conversion_rules = {
    'X': 'S',  # UI -> S (横一)
    'I': 'T',  # IO -> T (竖丨) 
    'O': 'U',  # OP -> U (撇丿)
    'P': 'V',  # IP -> V (点丶)
    'U': 'X',  # UP -> X (折乛)
    'W': 'W',  # UO -> W (人日口)
}

# 转换后的词库
converted_lines = []

for line in lines:
    # 跳过注释行和空行
    if line.startswith('#') or line.strip() == '' or line.startswith('---') or ':' in line:
        converted_lines.append(line)
        continue
    
    # 处理词库条目
    parts = line.strip().split('\t')
    if len(parts) >= 2:
        word = parts[0]
        code = parts[1]
        
        if len(code) >= 2:
            first_char = code[0]
            second_char = code[1]
            third_char = code[2] if len(code) > 2 else ''
            
            # 转换第2个字母
            new_second_char = conversion_rules.get(second_char, second_char)
            
            new_code = first_char + new_second_char + third_char
            
            # 重建行
            if len(parts) >= 3:
                new_line = f"{word}\t{new_code}\t{parts[2]}\n"
            else:
                new_line = f"{word}\t{new_code}\n"
            
            converted_lines.append(new_line)
        else:
            converted_lines.append(line)
    else:
        converted_lines.append(line)

# 输出转换结果
print("转换后的词库：")
for line in converted_lines:
    print(line, end='')

# 保存转换后的文件
with open(r'D:\RIME_config\pdbj_dict\pdbj.wordoneshot_new.dict.yaml', 'w', encoding='utf-8') as f:
    f.writelines(converted_lines)

print("\n\n转换完成，已保存到原文件")

# %%
