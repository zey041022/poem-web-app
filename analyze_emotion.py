import json
import re
from collections import Counter

# 情感关键词词典，按情感类别分类
emotion_keywords = {
    '思乡怀人': ['乡', '归', '忆', '思', '念', '望', '盼', '寄', '怀', '故', '旧', '远', '客', '旅', '愁', '离', '别', '梦', '魂', '情'],
    '壮志豪情': ['志', '壮', '豪', '雄', '英', '勇', '气', '节', '忠', '国', '报', '济', '安', '定', '功', '名', '业', '勋', '烈', '雄'],
    '感慨伤怀': ['感', '慨', '伤', '悲', '哀', '愁', '苦', '恨', '怨', '叹', '泪', '泣', '孤', '独', '寂', '寞', '冷', '凉', '凄', '惨'],
    '闲适愉悦': ['闲', '适', '悠', '然', '乐', '悦', '喜', '笑', '欢', '畅', '舒', '爽', '醉', '酣', '甜', '美', '静', '宁', '安', '怡'],
    '山水田园': ['山', '水', '田', '园', '村', '野', '郊', '庄', '农', '耕', '渔', '樵', '牧', '林', '泉', '石', '云', '雾', '烟', '霞'],
    '边塞战争': ['边', '塞', '战', '争', '军', '旅', '征', '戍', '战', '斗', '杀', '敌', '马', '剑', '枪', '弓', '箭', '旗', '鼓', '营'],
    '咏史怀古': ['古', '史', '昔', '往', '旧', '曾', '历', '经', '迹', '痕', '遗', '废', '兴', '亡', '盛', '衰', '荣', '辱', '鉴', '叹'],
    '爱情婚姻': ['爱', '情', '恋', '思', '慕', '忆', '念', '望', '盼', '情', '缘', '姻', '婚', '妻', '夫', '妾', '郎', '女', '心', '意']
}

# 情感强度词（增强或减弱情感）
intensity_words = {
    '强': ['最', '极', '太', '甚', '尤', '特', '非常', '十分', '极其', '格外', '异常', '无比', '莫大', '深深', '浓浓'],
    '弱': ['略', '稍', '微', '些', '较', '还算', '有点', '隐约', '淡淡', '轻轻']
}

def analyze_emotion(text):
    """分析文本中的主要情感"""
    if not text:
        return [], {}
    
    # 清洗文本，去除标点符号
    cleaned_text = re.sub(r'[，。！？；：“”‘’（）【】《》、\s]', '', text)
    
    # 统计各情感类别的得分
    emotion_scores = {}
    emotion_keywords_found = {}
    
    # 初始化
    for emotion in emotion_keywords:
        emotion_scores[emotion] = 0
        emotion_keywords_found[emotion] = []
    
    # 检查强度词
    has_strong_intensity = any(word in cleaned_text for word in intensity_words['强'])
    has_weak_intensity = any(word in cleaned_text for word in intensity_words['弱'])
    
    # 计算各情感得分
    for emotion, keywords in emotion_keywords.items():
        for keyword in keywords:
            # 查找关键词
            matches = re.findall(rf'{re.escape(keyword)}', cleaned_text)
            if matches:
                count = len(matches)
                emotion_scores[emotion] += count
                emotion_keywords_found[emotion].extend([keyword] * count)
    
    # 应用强度调整
    for emotion in emotion_scores:
        if has_strong_intensity:
            emotion_scores[emotion] *= 1.5
        elif has_weak_intensity:
            emotion_scores[emotion] *= 0.7
    
    # 过滤掉得分为0的情感
    valid_emotions = {k: v for k, v in emotion_scores.items() if v > 0}
    
    # 按得分排序，获取主要情感
    sorted_emotions = sorted(valid_emotions.items(), key=lambda x: x[1], reverse=True)
    main_emotions = [emotion for emotion, score in sorted_emotions[:3]]  # 取前3个主要情感
    
    # 统计每个情感中出现的关键词
    emotion_keyword_counts = {}
    for emotion, keywords in emotion_keywords_found.items():
        if keywords:
            emotion_keyword_counts[emotion] = dict(Counter(keywords))
    
    # 构建结果
    result = {
        'main_emotions': main_emotions,
        'emotion_scores': emotion_scores,
        'valid_emotions': valid_emotions,
        'emotion_keywords': emotion_keyword_counts,
        'has_strong_intensity': has_strong_intensity,
        'has_weak_intensity': has_weak_intensity
    }
    
    return main_emotions, result

def analyze_poetry_emotion(poetry_file):
    """分析诗词文件中的情感"""
    try:
        with open(poetry_file, 'r', encoding='utf-8') as f:
            poems = json.load(f)
        
        print(f"开始分析{len(poems)}首诗词的情感...")
        
        # 为每首诗词添加情感分析
        for i, poem in enumerate(poems):
            print(f"分析第{i+1}/{len(poems)}首: {poem['title']}")
            
            # 合并标题和正文进行分析
            full_text = poem['title'] + ' ' + poem['content']
            main_emotions, emotion_details = analyze_emotion(full_text)
            
            # 添加情感信息到诗词数据中
            poem['main_emotions'] = main_emotions
            poem['emotion_details'] = emotion_details
        
        # 保存分析结果
        output_file = poetry_file.replace('.json', '_with_emotion.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(poems, f, ensure_ascii=False, indent=2)
        
        print(f"情感分析完成！结果已保存到 {output_file}")
        return poems
        
    except Exception as e:
        print(f"分析情感时出错: {e}")
        return None

def merge_imagery_and_emotion(imagery_file, emotion_file):
    """合并意象和情感分析结果"""
    try:
        # 读取意象分析结果
        with open(imagery_file, 'r', encoding='utf-8') as f:
            imagery_data = json.load(f)
        
        # 读取情感分析结果
        with open(emotion_file, 'r', encoding='utf-8') as f:
            emotion_data = json.load(f)
        
        # 合并数据（假设标题相同则为同一首诗词）
        merged_data = []
        emotion_dict = {poem['title']: poem for poem in emotion_data}
        
        for imagery_poem in imagery_data:
            title = imagery_poem['title']
            if title in emotion_dict:
                # 合并数据
                merged_poem = imagery_poem.copy()
                merged_poem['main_emotions'] = emotion_dict[title].get('main_emotions', [])
                merged_poem['emotion_details'] = emotion_dict[title].get('emotion_details', {})
                merged_data.append(merged_poem)
        
        # 保存合并结果
        output_file = imagery_file.replace('_with_imagery.json', '_complete_analysis.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=2)
        
        print(f"数据合并完成！结果已保存到 {output_file}")
        return merged_data
        
    except Exception as e:
        print(f"合并数据时出错: {e}")
        return None

def analyze_all_emotions():
    """分析所有诗词文件的情感并合并结果"""
    # 分析唐诗情感
    print("===== 开始分析唐诗情感 =====")
    tang_result = analyze_poetry_emotion('tang_poems.json')
    
    # 分析宋词情感
    print("\n===== 开始分析宋词情感 =====")
    song_result = analyze_poetry_emotion('song_poems.json')
    
    # 合并意象和情感分析结果
    if tang_result and song_result:
        print("\n===== 开始合并唐诗意象和情感分析 =====")
        merge_imagery_and_emotion('tang_poems_with_imagery.json', 'tang_poems_with_emotion.json')
        
        print("\n===== 开始合并宋词意象和情感分析 =====")
        merge_imagery_and_emotion('song_poems_with_imagery.json', 'song_poems_with_emotion.json')
        
        # 统计整体情感分布
        all_emotions = Counter()
        for poem in tang_result + song_result:
            if 'main_emotions' in poem:
                all_emotions.update(poem['main_emotions'])
        
        # 保存情感统计
        emotion_stats = {
            'total_poems': len(tang_result) + len(song_result),
            'emotion_distribution': dict(all_emotions),
            'top_emotions': dict(all_emotions.most_common()),
            'tang_poems_count': len(tang_result),
            'song_poems_count': len(song_result)
        }
        
        with open('emotion_statistics.json', 'w', encoding='utf-8') as f:
            json.dump(emotion_stats, f, ensure_ascii=False, indent=2)
        
        print("\n整体情感统计完成！")
        print(f"情感分布: {dict(all_emotions.most_common())}")

if __name__ == '__main__':
    analyze_all_emotions()