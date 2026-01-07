#%%
import csv

# 文件路径
yaml_file = r'E:\Downloads\jichu.dict.yaml'
csv_file = r'E:\E_hobbies\百度输入法皮肤修改\rime-pindu-simple\拼读简并\5映射out.csv'
output_file = 'output_codes.txt'

# ========== 1. 读取CSV编码映射表 ==========
pinyin_to_code_map = {}

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        code = row['code']
        pinyin = row['pinyin']
        pinyinwithtone = row['pinyinwithtone']
        
        # 使用带声调的拼音作为key
        pinyin_to_code_map[pinyinwithtone] = code
        # 同时也保存不带声调的（pinyin列）作为key，以防需要
        pinyin_to_code_map[pinyin] = code

print("映射表前10条：")
for i, (k, v) in enumerate(list(pinyin_to_code_map.items())[:10]):
    print(f"  {k} -> {v}")
print(f"总共 {len(pinyin_to_code_map)} 个映射\n")


# ========== 2. 读取词库 ==========
entries = []

with open(yaml_file, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
reading_data = False

for line in lines:
    line = line.strip()
    
    if line == '---':
        continue
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
            word = parts[0]
            pinyin = parts[1]
            weight = parts[2] if len(parts) > 2 else ''
            entries.append((word, pinyin, weight))

print("词库前10条：")
for entry in entries[:10]:
    print(f"  {entry}")
print(f"总共 {len(entries)} 个词条\n")


# ========== 3. 转换并输出 ==========

# 打开输出文件
with open(output_file, 'w', encoding='utf-8') as f:
    
    for word, pinyin, weight in entries:
        # 分离每个字的拼音
        pinyin_list = [p.strip() for p in pinyin.split(' ')]
        codes = []
        
        # ========== DEBUG信息开始 ==========
        if word == '阿彬' or word == '阿斌' or word == '阿宾':
            print(f"\n=== 处理词: {word} ===")
            print(f"原始拼音: {pinyin}")
            print(f"拼音列表: {pinyin_list}")
        # ========== DEBUG信息结束 ==========
        
        for pinyin_item in pinyin_list:
            # 直接查找带声调的拼音
            if pinyin_item in pinyin_to_code_map:
                code = pinyin_to_code_map[pinyin_item]
                codes.append(code)
            else:
                # 找不到映射
                if word == '阿彬' or word == '阿斌' or word == '阿宾':
                    print(f"  {pinyin_item} -> 找不到编码！")
                codes.append(None)
        
        # ========== DEBUG信息开始 ==========
        if word == '阿彬' or word == '阿斌' or word == '阿宾':
            print(f"编码列表: {codes}")
        # ========== DEBUG信息结束 ==========
        
        # 根据字数生成编码
        word_len = len(word)
        final_code = None
        
        if word_len == 2:
            # 两字词：两个编码直接拼接
            if len(codes) >= 2 and codes[0] and codes[1]:
                final_code = codes[0] + codes[1]
                # 确保是6个字母
                if len(final_code) < 6:
                    final_code = final_code.ljust(6, 'Z')
        elif word_len >= 3:
            # 三字及以上词：前两字编码 + 改第6个字母为a + 最后一个字编码
            if len(codes) >= 2 and codes[0] and codes[1]:
                base_code = codes[0] + codes[1]
                # 确保前6位
                if len(base_code) < 6:
                    base_code = base_code.ljust(6, 'Z')
                
                # 第6个字母改为a
                if len(base_code) >= 6:
                    base_code = base_code[:5] + 'a'
                
                # 追加最后一个字的编码
                if codes[-1]:
                    final_code = base_code + codes[-1]
                else:
                    final_code = base_code + 'ZZ'
        
        # 输出
        if final_code:
            f.write(f"{word}\t{final_code}\n")
            if word == '阿彬' or word == '阿斌' or word == '阿宾':
                print(f"最终编码: {final_code}")
                print(f"写入: {word}\t{final_code}")
            print(f"{word}\t{final_code}")
        else:
            print(f"跳过: {word}\t{pinyin} (无法生成编码)")

print(f"\n转换完成！输出文件: {output_file}")

# %%
