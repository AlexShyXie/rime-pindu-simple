
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


# %%
