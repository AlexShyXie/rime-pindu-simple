#%%
import csv
import re

# 读取编码映射表
def load_code_mapping(csv_file):
    """读取CSV编码映射表"""
    pinyin_to_code = {}
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pinyin = row['pinyinwithtone']
            code = row['code']
            pinyin_to_code[pinyin] = code
    
    return pinyin_to_code

# 读取词库并统计拼音
def analyze_pinyin_in_dict(yaml_file, pinyin_to_code_map):
    """分析词库中的拼音"""
    
    with open(yaml_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    reading_data = False
    
    missing_pinyins = set()
    found_pinyins = set()
    
    for line in lines:
        line = line.strip()
        
        if line == '...':
            reading_data = True
            continue
        if line.startswith('name:'):
            continue
        if line.startswith('version:'):
            continue
        if line.startswith('sort:'):
            continue
            
        if reading_data and line and not line.startswith('#'):
            parts = line.split('\t')
            if len(parts) >= 2:
                pinyin_str = parts[1]
                # 分离每个字的拼音
                pinyin_list = [p.strip() for p in pinyin_str.split(' ')]
                
                for pinyin in pinyin_list:
                    if pinyin in pinyin_to_code_map:
                        found_pinyins.add(pinyin)
                    else:
                        missing_pinyins.add(pinyin)
    
    return found_pinyins, missing_pinyins

# %%分析
yaml_file = r'E:\Downloads\jichu.dict.yaml'
csv_file = r'E:\E_hobbies\百度输入法皮肤修改\rime-pindu-simple\拼读简并\5映射out.csv'

pinyin_to_code_map = load_code_mapping(csv_file)
found, missing = analyze_pinyin_in_dict(yaml_file, pinyin_to_code_map)

print(f"编码表中已映射的拼音数量: {len(found)}")
print(f"缺少映射的拼音数量: {len(missing)}")
print(f"\n缺少映射的拼音:")
for pinyin in sorted(list(missing)):  # 只显示前50个
    print(f"  {pinyin}")

# %%
