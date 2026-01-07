#%% 读取词库文件，找出所有包含"不是"的词和编码
def find_words_with_keyword(filename, keyword):
    results = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行和注释行（yaml中#开头是注释）
            if not line or line.startswith('#'):
                continue
            
            # 分割词和编码
            parts = line.split('\t')
            if len(parts) >= 2:
                word = parts[0]
                code = parts[1]
                
                # 检查词中是否包含关键字
                if keyword in word:
                    results.append((word, code))
    
    return results

def find_wordsIncode_with_keyword(filename, keyword):
    results = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行和注释行（yaml中#开头是注释）
            if not line or line.startswith('#'):
                continue
            
            # 分割词和编码
            parts = line.split('\t')
            if len(parts) >= 2:
                word = parts[0]
                code = parts[1]
                
                # 检查词中是否包含关键字
                if keyword in code:
                    results.append((word, code))
    
    return results
# 使用示例

filename = r'E:\Downloads\jichu.dict.yaml'
keyword = 'bú'

# results = find_words_with_keyword(filename, keyword)
results = find_wordsIncode_with_keyword(filename, keyword)
print(f"找到 {len(results)} 个包含'{keyword}'的词:\n")
for word, code in results:
    print(f"{word}\t{code}")

# %%
