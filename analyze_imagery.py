import json
import re
from collections import Counter

# 常见诗词意象词典，按类别分类
common_imagery = {
    # 自然意象
    '天文': ['日', '月', '星', '云', '雾', '霞', '虹', '霜', '雪', '雨', '风', '露', '冰', '雷', '电', '银河', '北斗', '夕阳', '朝阳', '暮色', '晨光'],
    '地理': ['山', '水', '江', '河', '湖', '海', '溪', '泉', '瀑', '石', '峰', '岩', '岭', '谷', '原', '野', '洲', '渚', '滩', '岸'],
    '植物': ['花', '草', '树', '木', '竹', '菊', '梅', '兰', '莲', '桃', '李', '杏', '柳', '松', '柏', '枫', '梧桐', '芭蕉', '芙蓉', '牡丹'],
    '动物': ['鸟', '雁', '燕', '鹤', '鹰', '鸥', '鸦', '杜鹃', '黄鹂', '蝴蝶', '蜜蜂', '蝉', '蛙', '鱼', '龙', '虎', '马', '牛', '羊', '猿'],
    # 人文意象
    '器物': ['酒', '剑', '琴', '棋', '书', '画', '笔', '墨', '纸', '砚', '笛', '箫', '琵琶', '鼓', '钟', '镜', '灯', '烛', '扇', '伞'],
    '建筑': ['楼', '台', '亭', '阁', '榭', '轩', '馆', '殿', '宫', '苑', '宅', '院', '窗', '门', '栏', '墙', '桥', '路', '舟', '船'],
    '时间': ['春', '夏', '秋', '冬', '晨', '昏', '昼', '夜', '朝', '暮', '年', '岁', '月', '日', '时', '刻', '久', '暂', '瞬间', '永恒'],
    '情感相关': ['泪', '恨', '愁', '喜', '笑', '梦', '魂', '思', '忆', '念', '望', '盼', '归', '别', '离', '聚', '爱', '怨', '情', '绪']
}

# 构建所有意象的扁平列表
all_imagery = []
for category, items in common_imagery.items():
    all_imagery.extend(items)

def extract_imagery(text):
    """从文本中提取主要意象"""
    if not text:
        return [], {}
    
    # 清洗文本，去除标点符号
    cleaned_text = re.sub(r'[，。！？；：“”‘’（）【】《》、\s]', '', text)
    
    # 统计意象出现次数
    imagery_counts = Counter()
    category_counts = {}
    
    # 初始化类别计数
    for category in common_imagery:
        category_counts[category] = 0
    
    # 查找意象
    for category, items in common_imagery.items():
        for item in items:
            # 使用正则表达式查找，确保是完整的词（避免重叠匹配）
            matches = re.findall(rf'{re.escape(item)}', cleaned_text)
            if matches:
                count = len(matches)
                imagery_counts[item] = count
                category_counts[category] += count
    
    # 获取主要意象（按出现次数排序，取前5个）
    main_imagery = [item for item, _ in imagery_counts.most_common(5)]
    
    # 获取主要意象类别（按类别中意象总出现次数排序）
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    main_categories = [cat for cat, count in sorted_categories if count > 0]
    
    # 构建结果字典
    result = {
        'main_imagery': main_imagery,
        'imagery_counts': dict(imagery_counts),
        'main_categories': main_categories[:3],  # 取前3个主要类别
        'category_counts': {k: v for k, v in category_counts.items() if v > 0}
    }
    
    return main_imagery, result

def analyze_poetry_imagery(poetry_file):
    """分析诗词文件中的意象"""
    try:
        with open(poetry_file, 'r', encoding='utf-8') as f:
            poems = json.load(f)
        
        print(f"开始分析{len(poems)}首诗词的意象...")
        
        # 为每首诗词添加意象分析
        for i, poem in enumerate(poems):
            print(f"分析第{i+1}/{len(poems)}首: {poem['title']}")
            
            # 合并标题和正文进行分析
            full_text = poem['title'] + ' ' + poem['content']
            main_imagery, imagery_details = extract_imagery(full_text)
            
            # 添加意象信息到诗词数据中
            poem['imagery'] = main_imagery
            poem['imagery_details'] = imagery_details
        
        # 保存分析结果
        output_file = poetry_file.replace('.json', '_with_imagery.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(poems, f, ensure_ascii=False, indent=2)
        
        print(f"意象分析完成！结果已保存到 {output_file}")
        return poems
        
    except Exception as e:
        print(f"分析意象时出错: {e}")
        return None

def analyze_all_poetry():
    """分析所有诗词文件"""
    # 分析唐诗
    print("===== 开始分析唐诗意象 =====")
    tang_result = analyze_poetry_imagery('tang_poems.json')
    
    # 分析宋词
    print("\n===== 开始分析宋词意象 =====")
    song_result = analyze_poetry_imagery('song_poems.json')
    
    # 统计整体意象使用情况
    if tang_result and song_result:
        all_imagery_counter = Counter()
        for poem in tang_result + song_result:
            if 'imagery_details' in poem and 'imagery_counts' in poem['imagery_details']:
                for imagery, count in poem['imagery_details']['imagery_counts'].items():
                    all_imagery_counter[imagery] += count
        
        # 保存整体统计结果
        overall_stats = {
            'total_poems': len(tang_result) + len(song_result),
            'top_imagery': dict(all_imagery_counter.most_common(20)),
            'tang_poems_count': len(tang_result),
            'song_poems_count': len(song_result)
        }
        
        with open('imagery_statistics.json', 'w', encoding='utf-8') as f:
            json.dump(overall_stats, f, ensure_ascii=False, indent=2)
        
        print("\n整体意象统计完成！")
        print(f"最常用的20个意象: {dict(all_imagery_counter.most_common(20))}")

if __name__ == '__main__':
    analyze_all_poetry()