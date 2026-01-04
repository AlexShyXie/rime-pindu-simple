
#%%
import pandas as pd
from collections import defaultdict
import re

def parse_buzhou_to_dict(csv_file_path, output_file_path="radical_to_keys_dict.py"):
    """
    解析CSV文件，生成radical_to_keys字典
    格式：'偏旁': {'sheng 按键'}
    
    参数:
        csv_file_path: CSV文件路径
        output_file_path: 输出的Python文件路径
    
    返回:
        radical_to_keys: 偏旁到按键的映射字典
    """
    
    # 读取CSV文件
    df = pd.read_csv(csv_file_path, encoding='utf-8-sig')
    
    print(f"✓ 读取CSV文件: {csv_file_path}")
    print(f"  共 {len(df)} 行数据")
    
    # 初始化字典
    radical_to_keys = defaultdict(set)
    
    # 遍历每一行
    for index, row in df.iterrows():
        sheng = row['sheng']
        buzhou = row['buzhou']
        anjian = row['anjian']
        
        # 跳过空值
        if pd.isna(sheng) or pd.isna(buzhou) or pd.isna(anjian):
            continue
        
        # 组合 sheng 和 anjian
        sheng_anjian = f"{sheng} {anjian}"
        
        # 1. 提取括号外的偏旁（去掉括号）
        buzhou_clean = re.sub(r'[（）()]', '', buzhou)
        
        # 2. 提取括号内的偏旁
        radicals_in_parentheses = re.findall(r'[（(]([^）)]*)[）)]', buzhou)
        
        # 3. 组合所有偏旁
        all_radicals = list(buzhou_clean)
        
        # 添加括号内的偏旁（可能有多个字符）
        for r in radicals_in_parentheses:
            if r:  # 非空
                all_radicals.extend(list(r))
        
        # 4. 去重
        unique_radicals = set(all_radicals)
        
        # 5. 添加到字典，格式：'偏旁': {'sheng 按键'}
        for radical in unique_radicals:
            if radical.strip():  # 忽略空字符
                radical_to_keys[radical].add(sheng_anjian)
    
    print(f"✓ 解析完成，共 {len(radical_to_keys)} 个偏旁")
    
    # 生成Python字典格式字符串
    output = "radical_to_keys = defaultdict(set,\n            {"
    for radical in sorted(radical_to_keys.keys()):
        keys = sorted(radical_to_keys[radical])
        key_str = "','".join(keys)
        output += f"\n             '{radical}': {{'{key_str}'}},"
    output += "\n            })"
    
    print(output)
    # # 保存到文件
    # with open(output_file_path, 'w', encoding='utf-8') as f:
    #     f.write(output)
    
    # print(f"✓ 已保存到: {output_file_path}")
    
    return radical_to_keys


# %%使用示例

# 输入的CSV文件路径
csv_file_path = r"E:\E_hobbies\百度输入法皮肤修改\FlypyBingji-main\拼读简并\0radical_keys.csv"  # 修改为你的实际文件路径

# 输出的Python文件路径
output_file_path = r"E:\E_hobbies\百度输入法皮肤修改\FlypyBingji-main\拼读简并\radical_to_keys_dict.txt"

print("=" * 70)
print("开始转换 CSV 到 Python 字典")
print("=" * 70)
print()

# 执行转换
radical_to_keys = parse_buzhou_to_dict(csv_file_path, output_file_path)

print()
print("=" * 70)
print("转换完成！")
print("=" * 70)

# 打印前10个结果示例
print("\n前10个偏旁示例:")
count = 0
for radical in sorted(radical_to_keys.keys()):
    keys = radical_to_keys[radical]
    print(f"  '{radical}': {set(keys)}")
    count += 1
    if count >= 10:
        break

#%%
radical_to_keys

# %% 重新映射新代码：
from collections import defaultdict

def map_radicals_to_keys(new_file_path, radical_to_keys, output_file="映射结果.txt"):
    """
    根据偏旁到按键的映射，把新文件中的偏旁转换为按键
    
    参数:
        new_file_path: 新文件的路径（格式：字\t偏旁）
        radical_to_keys: 偏旁到按键的映射字典 {偏旁: {按键集合}}
        output_file: 输出文件路径
    """
    # 结果字典
    char_to_key = {}
    char_to_radical = {}
    
    # 按键统计
    key_to_chars = defaultdict(list)
    
    # 读取新文件（UTF-8 BOM编码）
    try:
        with open(new_file_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        print(f"✓ 成功读取文件: {new_file_path}")
        print(f"  共 {len(lines)} 行\n")
    except Exception as e:
        print(f"✗ 读取文件失败: {e}")
        return None
    
    # 解析并映射
    success_count = 0
    no_mapping_count = 0
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        
        # 按 tab 分割
        if '\t' not in line:
            print(f"第{line_num}行: 没有找到tab分隔符 - {repr(line)}")
            continue
        
        char, radical = line.split('\t', 1)
        char = char.strip()
        radical = radical.strip()
        
        # 查找对应的按键
        if radical in radical_to_keys:
            keys = radical_to_keys[radical]
            # 如果有多个按键，取第一个（按字母排序）
            key = sorted(keys)[0] if keys else ""
            
            if key:
                char_to_key[char] = key
                char_to_radical[char] = radical
                key_to_chars[key].append(char)
                success_count += 1
                
                # 显示前几行结果
                if line_num <= 5:
                    print(f"第{line_num}行映射: 字='{char}' 偏旁='{radical}' -> 按键='{key}'")
            else:
                print(f"第{line_num}行: 偏旁 '{radical}' 没有对应的按键")
                no_mapping_count += 1
        else:
            print(f"第{line_num}行: 偏旁 '{radical}' 未在映射表中找到")
            no_mapping_count += 1
    
    print(f"\n映射完成:")
    print(f"  成功映射: {success_count} 个")
    print(f"  未找到映射: {no_mapping_count} 个\n")
    
    # 保存结果
    if char_to_key:
        with open(output_file, 'w', encoding='utf-8-sig') as f:
            f.write("字\t偏旁 || 按键\n")
            f.write("=" * 50 + "\n")
            
            # 按按键分组显示
            for key in sorted(key_to_chars.keys()):
                chars = key_to_chars[key]
                for char in chars:
                    radical = char_to_radical[char]
                    f.write(f"{char}\t{radical} | {key}\n")
            
            # f.write("\n" + "=" * 50 + "\n")
            # f.write("按按键分组:\n")
            # f.write("=" * 50 + "\n")
            # for key in sorted(key_to_chars.keys()):
            #     chars = key_to_chars[key]
            #     f.write(f"按键 '{key}': {' '.join(chars)}\n")
        
        print(f"✓ 结果已保存到 '{output_file}'")
    
    return char_to_key, char_to_radical, key_to_chars

#%% 使用示例

# 你的新文件路径
new_file_path = r"G:\OneDrive - csu.edu.cn\重要软件备份\输入法\拼读并击250412\lua\pdbj\assembly.txt"  # 修改为你的实际文件路径

# 使用之前统计得到的 radical_to_keys
# 如果你有完整的 radical_to_keys，直接使用即可
# radical_to_keys #= {'⺈': {'F'}, '⺌': {'T'}, '八': {'S'}}  # 示例数据，替换成你的实际数据

print("=" * 60)
print("开始偏旁到按键的映射")
print("=" * 60 + "\n")

result = map_radicals_to_keys(new_file_path, radical_to_keys, "E:\Downloads\映射结果.txt")

if result:
    char_to_key, char_to_radical, key_to_chars = result
    
    print("\n" + "=" * 60)
    print("按按键分组的结果:")
    print("=" * 60)
    for key in sorted(key_to_chars.keys()):
        chars = key_to_chars[key]
        print(f"按键 '{key}': {' '.join(chars)}")


# %%
