#%%
# -*- coding: utf-8 -*-
import csv

def process_radical_mapping():
    """
    处理部首映射文件，添加按键大写和编码
    """
    
    # 读取按键编码映射文件
    key_code_map = {}
    with open('10_字母映射编码_flypy.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key_code_map[row['alpha']] = row['code']
    
    # 读取部首映射文件并处理
    results = []
    with open('10radical_mapping_flypy.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('\t')
            if len(parts) < 2:
                continue
            
            radical = parts[0]  # 部首
            key_lower = parts[1]  # 按键小写
            
            # 转换为大写
            key_upper = key_lower.upper()
            
            # 查找对应的编码
            code = key_code_map.get(key_upper, '')
            
            # 新格式：部首 编码 按键大写
            results.append(f"{radical}\t{code}\t{key_upper}")
    
    # 写入输出文件
    with open('10radical_mapping_with_code.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
    
    print(f"处理完成！共处理 {len(results)} 行")
    print(f"结果已保存到：10radical_mapping_with_code.txt")
    
    # 显示前10行示例
    print("\n示例输出：")
    for line in results[:10]:
        print(line)
    
    return results


# 执行处理
#%%
results = process_radical_mapping()

# %%
