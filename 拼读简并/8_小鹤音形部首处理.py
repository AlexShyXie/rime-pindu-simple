
#%%
# -*- coding: utf-8 -*-

def process_xiaohe_file(input_file, output_file):
    """
    处理小鹤拆分文件
    输入格式：字	部首：XX	小鹤：xxxx	鹤形：XX XX	拆分：XX XX
    输出格式：字  第1个拆分偏旁  第3个字母
    """
    results = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('\t')
            if len(parts) < 4:
                continue
            
            char = parts[0]  # 第1列：字
            
            # 找到小鹤编码
            xiaohe_code = None
            for part in parts:
                if part.startswith('小鹤：'):
                    xiaohe_code = part.replace('小鹤：', '')
                    break
            
            # 找到鹤形
            hexing = None
            for part in parts:
                if part.startswith('鹤形：'):
                    hexing = part.replace('鹤形：', '')
                    break
            
            if not xiaohe_code or not hexing:
                continue
            
            # 获取第1个拆分偏旁
            first_radical = hexing.split()[0]
            
            # 获取第3个字母（只取第一个编码的第3个字母）
            first_code = xiaohe_code.split()[0]
            third_letter = first_code[2] if len(first_code) >= 3 else ''
            
            results.append(f"{char}\t{first_radical}|{third_letter}")
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
    
    print(f"处理完成！共处理 {len(results)} 行")
    print(f"结果已保存到：{output_file}")
    
    return results


# 使用示例
#%%
# 修改为你的实际文件路径
input_file = r'D:\RIME_config\flypy\小鹤拆分+部首.txt'
output_file = 'output.txt'

process_xiaohe_file(input_file, output_file)


# %% 小鹤自己的重码率分析
# -*- coding: utf-8 -*-

def analyze_xiaohe_overlap(input_file):
    """
    统计小鹤编码前3个字母的重码率
    """
    code_dict = {}  # 存储每个编码对应的字
    overlap_dict = {}  # 存储每个编码的字数
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('\t')
            if len(parts) < 4:
                continue
            
            char = parts[0]  # 字
            
            # 找到小鹤编码
            xiaohe_code = None
            for part in parts:
                if part.startswith('小鹤：'):
                    xiaohe_code = part.replace('小鹤：', '')
                    break
            
            if not xiaohe_code:
                continue
            
            # 取第一个编码的前3个字母
            first_code = xiaohe_code.split()[0]
            three_letters = first_code[:3]
            
            if three_letters:
                if three_letters not in code_dict:
                    code_dict[three_letters] = []
                code_dict[three_letters].append(char)
    
    # 统计重码情况
    total_codes = len(code_dict)  # 总共多少个不同编码
    overlap_codes = 0  # 有重码的编码数量
    max_overlap = 0  # 最大重码数
    overlap_details = []  # 重码详情
    
    for code, chars in code_dict.items():
        char_count = len(chars)
        overlap_dict[code] = char_count
        
        if char_count > 1:
            overlap_codes += 1
            if char_count > max_overlap:
                max_overlap = char_count
            overlap_details.append((code, char_count, chars))
    
    # 排序：按重码数从高到低
    overlap_details.sort(key=lambda x: x[1], reverse=True)
    
    # 输出统计结果
    print("=" * 50)
    print("小鹤编码前3个字母重码率统计")
    print("=" * 50)
    print(f"总编码数：{total_codes}")
    print(f"有重码的编码数：{overlap_codes}")
    print(f"无重码的编码数：{total_codes - overlap_codes}")
    print(f"重码率：{overlap_codes/total_codes*100:.2f}%")
    print(f"最大重码数：{max_overlap}")
    print("=" * 50)
    
    # 输出前20个重码最多的编码
    print("\n重码最多的前20个编码：")
    print("-" * 50)
    for i, (code, count, chars) in enumerate(overlap_details[:20], 1):
        print(f"{i}. {code}: {count}个字 - {' '.join(chars)}")
    
    # # 可选：保存完整结果到文件
    # with open('overlap_analysis.txt', 'w', encoding='utf-8') as f:
    #     f.write("小鹤编码前3个字母重码分析\n")
    #     f.write("=" * 50 + "\n\n")
    #     f.write(f"总编码数：{total_codes}\n")
    #     f.write(f"有重码的编码数：{overlap_codes}\n")
    #     f.write(f"无重码的编码数：{total_codes - overlap_codes}\n")
    #     f.write(f"重码率：{overlap_codes/total_codes*100:.2f}%\n")
    #     f.write(f"最大重码数：{max_overlap}\n\n")
        
    #     f.write("所有重码编码详情（按重码数排序）：\n")
    #     f.write("-" * 50 + "\n")
    #     for code, count, chars in overlap_details:
    #         f.write(f"{code}: {count}个字 - {' '.join(chars)}\n")
    
    # print(f"\n详细结果已保存到：overlap_analysis.txt")
    # print("=" * 50)
    
    return {
        'total_codes': total_codes,
        'overlap_codes': overlap_codes,
        'overlap_rate': overlap_codes/total_codes*100,
        'max_overlap': max_overlap,
        'overlap_details': overlap_details
    }


# 使用示例
input_file = r'D:\RIME_config\flypy\小鹤拆分+部首.txt'
result = analyze_xiaohe_overlap(input_file)

# %%
