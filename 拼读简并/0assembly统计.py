
#%%
from collections import defaultdict
import os


#%%
def analyze_assembly_file(file_path):
    """
    分析assembly.txt文件，统计偏旁和按键的对应关系
    格式：字[Tab]偏旁[空格][空格]|[空格][空格]按键
    文件编码：UTF-8 with BOM
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 文件 '{file_path}' 不存在")
        print(f"当前目录: {os.getcwd()}")
        return None
    
    # 统计字典
    radical_to_keys = defaultdict(set)   # 偏旁 -> 按键集合
    key_to_radicals = defaultdict(set)   # 按键 -> 偏旁集合
    radical_to_chars = defaultdict(list) # 偏旁 -> 汉字列表
    key_to_chars = defaultdict(list)     # 按键 -> 汉字列表
    
    # 使用 utf-8-sig 编码自动处理 BOM
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        print(f"✓ 成功使用 UTF-8 with BOM 编码读取文件")
    except Exception as e:
        print(f"✗ 读取文件时出错: {e}")
        return None
    
    lines = content.split('\n')
    print(f"文件共 {len(lines)} 行\n")
    
    # 显示前几行内容用于调试
    print("前5行原始内容:")
    for i, line in enumerate(lines[:5], 1):
        if line.strip():
            print(f"  第{i}行: {repr(line[:50])}")
    print()
    
    # 解析每一行
    success_count = 0
    line_num = 0
    for line in lines:
        line_num+=1
        line = line.strip()
        if not line:
            continue
        
        # 按 tab 分割
        if '\t' not in line:
            print(f"第{line_num}行: 没有找到tab分隔符 - {repr(line)}")
            continue
        
        # 分割成左右两部分
        left_part, right_part = line.split('\t', 1)
        
        # 提取汉字（左边第一个字符）
        if not left_part:
            print(f"第{line_num}行: 左边部分为空")
            continue
        char = left_part[0]
        

        
        # 从右边部分提取按键
        # 格式是 "⺈  |  F "，需要去掉 "| " 和前后空格
        # 提取偏旁（左边剩余部分，去掉多余空格）
        radical = right_part.split('|')[0].strip()
        key_part = right_part.split('|')[-1].strip()
        key = key_part.strip()
        
        # 验证提取的数据
        if not char or not radical or not key:
            print(f"第{line_num}行: 数据不完整 - 字='{char}' 偏旁='{radical}' 按键='{key}'")
            continue
        
        # 统计
        radical_to_keys[radical].add(key)
        key_to_radicals[key].add(radical)
        radical_to_chars[radical].append(char)
        key_to_chars[key].append(char)
        success_count += 1
        
        # 显示前几行的解析结果
        if line_num <= 3:
            print(f"第{line_num}行解析: 字='{char}' 偏旁='{radical}' 按键='{key}'")
    
    print(f"\n成功解析 {success_count} 行数据\n")
    
    return radical_to_keys, key_to_radicals, radical_to_chars, key_to_chars

def print_statistics(radical_to_keys, key_to_radicals, radical_to_chars, key_to_chars):
    """打印统计结果"""
    print("=" * 70)
    print("按偏旁统计：")
    print("=" * 70)
    for radical in sorted(radical_to_keys.keys()):
        keys = sorted(radical_to_keys[radical])
        chars = radical_to_chars[radical]
        print(f"偏旁 '{radical}' -> 按键 {keys}")
        print(f"  对应汉字 ({len(chars)}个): {' '.join(chars)}")
        print()
    
    print("=" * 70)
    print("按按键统计：")
    print("=" * 70)
    for key in sorted(key_to_radicals.keys()):
        radicals = sorted(key_to_radicals[key])
        chars = key_to_chars[key]
        print(f"按键 '{key}' -> 偏旁 {radicals}")
        print(f"  对应汉字 ({len(chars)}个): {' '.join(chars)}")
        print()

def save_statistics(radical_to_keys, key_to_radicals, radical_to_chars, key_to_chars, output_file="统计结果.txt"):
    """保存统计结果到文件"""
    with open(output_file, 'w', encoding='utf-8-sig') as f:
        f.write("按偏旁统计：\n")
        f.write("=" * 70 + "\n")
        for radical in sorted(radical_to_keys.keys()):
            keys = sorted(radical_to_keys[radical])
            chars = radical_to_chars[radical]
            f.write(f"偏旁 '{radical}' -> 按键 {keys}\n")
            f.write(f"  对应汉字 ({len(chars)}个): {' '.join(chars)}\n\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("按按键统计：\n")
        f.write("=" * 70 + "\n")
        for key in sorted(key_to_radicals.keys()):
            radicals = sorted(key_to_radicals[key])
            chars = key_to_chars[key]
            f.write(f"按键 '{key}' -> 偏旁 {radicals}\n")
            f.write(f"  对应汉字 ({len(chars)}个): {' '.join(chars)}\n\n")
    
    print(f"统计结果已保存到 '{output_file}'")

#%% 使用示例
file_path = r"D:\RIME_config\lua\pdbj\assembly.txt"  # 修改为你的文件路径

print(f"开始分析文件: {file_path}\n")

result = analyze_assembly_file(file_path)

if result:
    radical_to_keys, key_to_radicals, radical_to_chars, key_to_chars = result
    print_statistics(radical_to_keys, key_to_radicals, radical_to_chars, key_to_chars)
    #save_statistics(radical_to_keys, key_to_radicals, radical_to_chars, key_to_chars)
else:
    print("分析失败，请检查文件路径和格式")

# %%
