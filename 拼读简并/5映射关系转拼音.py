
#%%
import csv

def pinyin_with_tone_correct(pinyin_with_number):
    """正确转换数字声调为声调符号, 仍然存在问题"""
    
    # 元音+声调符号映射
    tone_map = {
        'a': ('ā', 'á', 'ǎ', 'à'),
        'e': ('ē', 'é', 'ě', 'è'),
        'i': ('ī', 'í', 'ǐ', 'ì'),
        'o': ('ō', 'ó', 'ǒ', 'ò'),
        'u': ('ū', 'ú', 'ǔ', 'ù'),
        'v': ('ǖ', 'ǘ', 'ǚ', 'ǜ'),
    }
    
    # 提取声调数字
    tone = None
    base_pinyin = pinyin_with_number
    
    for i in range(len(base_pinyin) - 1, -1, -1):
        if base_pinyin[i] in '1234':
            tone = int(base_pinyin[i])
            base_pinyin = base_pinyin[:i] + base_pinyin[i+1:]
            break
    
    if tone is None:
        return pinyin_with_number
    
    # 检查特殊韵母组合
    if 'iu' in base_pinyin:
        # iu → 声调在 u 上 (例如: niu3 → niǔ)
        u_idx = base_pinyin.find('u')  # 找到 u 的位置
        tone_chars = tone_map['u']
        new_char = tone_chars[tone - 1]
        base_pinyin = base_pinyin[:u_idx] + new_char + base_pinyin[u_idx+1:]
        return base_pinyin
    
    if 'ui' in base_pinyin:
        # ui → 声调在 i 上 (例如: dui1 → duī)
        i_idx = base_pinyin.find('i')  # 找到 i 的位置
        tone_chars = tone_map['i']
        new_char = tone_chars[tone - 1]
        base_pinyin = base_pinyin[:i_idx] + new_char + base_pinyin[i_idx+1:]
        return base_pinyin
    
    # 常规规则：优先级 a > o/e > i/u/v
    if 'a' in base_pinyin:
        a_idx = base_pinyin.find('a')
        tone_chars = tone_map['a']
        new_char = tone_chars[tone - 1]
        base_pinyin = base_pinyin[:a_idx] + new_char + base_pinyin[a_idx+1:]
        return base_pinyin
    
    if 'o' in base_pinyin:
        o_idx = base_pinyin.find('o')
        tone_chars = tone_map['o']
        new_char = tone_chars[tone - 1]
        base_pinyin = base_pinyin[:o_idx] + new_char + base_pinyin[o_idx+1:]
        return base_pinyin
    
    if 'e' in base_pinyin:
        e_idx = base_pinyin.find('e')
        tone_chars = tone_map['e']
        new_char = tone_chars[tone - 1]
        base_pinyin = base_pinyin[:e_idx] + new_char + base_pinyin[e_idx+1:]
        return base_pinyin
    
    if 'i' in base_pinyin:
        i_idx = base_pinyin.find('i')
        tone_chars = tone_map['i']
        new_char = tone_chars[tone - 1]
        base_pinyin = base_pinyin[:i_idx] + new_char + base_pinyin[i_idx+1:]
        return base_pinyin
    
    if 'u' in base_pinyin:
        u_idx = base_pinyin.find('u')
        tone_chars = tone_map['u']
        new_char = tone_chars[tone - 1]
        base_pinyin = base_pinyin[:u_idx] + new_char + base_pinyin[u_idx+1:]
        return base_pinyin
    
    if 'v' in base_pinyin:
        v_idx = base_pinyin.find('v')
        tone_chars = tone_map['v']
        new_char = tone_chars[tone - 1]
        base_pinyin = base_pinyin[:v_idx] + new_char + base_pinyin[v_idx+1:]
        return base_pinyin
    
    return base_pinyin


def convert_csv_to_tone(input_file, output_file):
    """转换CSV文件中的拼音列"""
    
    with open(input_file, 'r', encoding='utf-8') as f_in:
        reader = csv.reader(f_in)
        header = next(reader)
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
            writer = csv.writer(f_out)
            
            # 写入表头（添加新列）
            writer.writerow(header + ['拼音带声调'])
            
            for row in reader:
                if len(row) >= 2:
                    code = row[0]
                    pinyin_number = row[1]
                    
                    # 转换声调
                    pinyin_display = pinyin_with_tone_correct(pinyin_number)
                    
                    # 写入新行
                    writer.writerow(row + [pinyin_display])
                else:
                    writer.writerow(row)


# 使用示例
input_file=r'E:\E_hobbies\百度输入法皮肤修改\rime-pindu-simple\拼读简并\5映射out.csv'
output_file=r'E:\E_hobbies\百度输入法皮肤修改\rime-pindu-simple\拼读简并\5映射outout.csv'

convert_csv_to_tone(input_file, output_file)

print(f"转换完成！")
print(f"输入文件: {input_file}")
print(f"输出文件: {output_file}")

# %%
import csv

# 读取已有的映射表
def load_existing_mapping(csv_file):
    """读取现有的映射表"""
    pinyin_to_code = {}
    existing_rows = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row['code']
            pinyin = row['pinyin']
            pinyinwithtone = row['pinyinwithtone']
            
            existing_rows.append(row)
            
            # 保存：拼音（去声调数字） -> code 的映射
            # 例如：de1 -> abZ
            pinyin_to_code[pinyin] = code
    
    return pinyin_to_code, existing_rows

# 轻声列表
qingsheng_list = [
    "a", "ba", "bai", "bao", "bei", "bing", "bo", "bu", "cha", "chang", "chao",
    "chen", "cheng", "chi", "chou", "chu", "da", "dai", "dang", "dao", "de",
    "di", "duo", "er", "fa", "fan", "fang", "fen", "fu", "gan", "ge", "gong",
    "gou", "gu", "guo", "gu", "hai", "han", "he", "hou", "hu", "hua",
    "huan", "huo", "ji"
]

# 生成新行
def generate_qingsheng_rows(qingsheng_list, pinyin_to_code):
    """为轻声生成新行"""
    new_rows = []
    
    for qingsheng in qingsheng_list:
        # 轻声转1声：在末尾加1
        pinyin_with_tone = qingsheng + "1"
        
        # 查找对应的编码
        if pinyin_with_tone in pinyin_to_code:
            code = pinyin_to_code[pinyin_with_tone]
            pinyinwithtone = pinyin_with_tone_correct(qingsheng + "1")
            
            new_row = {
                'code': code,
                'pinyin': qingsheng,  # 保持轻声原样
                'pinyinwithtone': pinyinwithtone
            }
            new_rows.append(new_row)
            print(f"生成: {qingsheng} -> {code} ({pinyinwithtone})")
        else:
            print(f"跳过: {qingsheng} + '1' = {pinyin_with_tone} (找不到对应的编码)")
    
    return new_rows

# 保存到CSV
def save_to_csv(existing_rows, new_rows, output_file):
    """保存原有行和新行到CSV"""
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['code', 'pinyin', 'pinyinwithtone']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        # 写入原有行
        for row in existing_rows:
            writer.writerow(row)
        
        # 写入新行
        for row in new_rows:
            writer.writerow(row)

# 主函数
def process_qingsheng(input_file, output_file):
    """处理轻声并生成新行"""
    
    # 读取已有映射表
    pinyin_to_code, existing_rows = load_existing_mapping(input_file)
    
    print(f"已读取 {len(existing_rows)} 行现有映射")
    print(f"拼音映射表大小: {len(pinyin_to_code)}\n")
    
    # 生成轻声的新行
    new_rows = generate_qingsheng_rows(qingsheng_list, pinyin_to_code)
    
    print(f"\n生成了 {len(new_rows)} 个轻声新行")
    
    # 保存
    save_to_csv(existing_rows, new_rows, output_file)
    print(f"已保存到: {output_file}")

# 使用
input_file = r'E:\E_hobbies\百度输入法皮肤修改\rime-pindu-simple\拼读简并\5映射out.csv'      # 原有映射表
output_file = r'E:\E_hobbies\百度输入法皮肤修改\rime-pindu-simple\拼读简并\5映射out_with_qingsheng.csv'  # 输出文件

process_qingsheng(input_file, output_file)

# %%
