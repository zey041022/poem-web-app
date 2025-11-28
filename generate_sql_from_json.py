import json
import os

# 设置文件路径
TANG_COMPLETE_FILE = 'tang_poems_complete_analysis.json'
SONG_COMPLETE_FILE = 'song_poems_complete_analysis.json'
OUTPUT_SQL_FILE = 'full_poetry_database.sql'

def read_json_file(file_path):
    """读取JSON文件"""
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        # 返回空列表作为备选
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_tang_sql(poems):
    """生成唐诗插入SQL语句"""
    if not poems:
        # 如果没有数据，使用默认数据
        return """
-- 唐诗插入语句
INSERT INTO tang_poetry (title, author, dynasty, content, genre, url, main_imagery, emotions) VALUES
('静夜思', '李白', '唐代', '床前明月光，疑是地上霜。举头望明月，低头思故乡。', '五言绝句', 'https://www.gushiwen.cn/shiwenv_9b8e95f39c0a.aspx', '明月,床前,地霜', '思乡怀人,感慨伤怀'),
('望庐山瀑布', '李白', '唐代', '日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_653a968147a5.aspx', '瀑布,银河,香炉,紫烟', '山水田园,惊叹赞美'),
('黄鹤楼送孟浩然之广陵', '李白', '唐代', '故人西辞黄鹤楼，烟花三月下扬州。孤帆远影碧空尽，唯见长江天际流。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_2f74d036a3be.aspx', '黄鹤楼,孤帆,长江,碧空', '送别惜别,感慨伤怀');
"""
    
    sql_statements = []
    for poem in poems:
        # 提取必要字段，使用默认值处理缺失字段
        title = poem.get('title', '').replace("'", "''")
        author = poem.get('author', '').replace("'", "''")
        dynasty = poem.get('dynasty', '唐代').replace("'", "''")
        content = poem.get('content', '').replace("'", "''")
        genre = poem.get('genre', '').replace("'", "''")
        url = poem.get('url', '').replace("'", "''")
        
        # 处理意象字段
        main_imagery = ''
        if 'main_imagery' in poem:
            if isinstance(poem['main_imagery'], list):
                main_imagery = ','.join(poem['main_imagery']).replace("'", "''")
            elif isinstance(poem['main_imagery'], str):
                main_imagery = poem['main_imagery'].replace("'", "''")
        
        # 处理情感字段
        emotions = ''
        if 'emotions' in poem:
            if isinstance(poem['emotions'], list):
                emotions = ','.join(poem['emotions']).replace("'", "''")
            elif isinstance(poem['emotions'], str):
                emotions = poem['emotions'].replace("'", "''")
        
        # 构造插入语句
        sql = f"('{title}', '{author}', '{dynasty}', '{content}', '{genre}', '{url}', '{main_imagery}', '{emotions}')"
        sql_statements.append(sql)
    
    # 拼接完整的INSERT语句
    if sql_statements:
        values_str = ',\n'.join(sql_statements)
        return f"""
-- 唐诗插入语句
INSERT INTO tang_poetry (title, author, dynasty, content, genre, url, main_imagery, emotions) VALUES
{values_str};
"""
    return ""

def generate_song_sql(poems):
    """生成宋词插入SQL语句"""
    if not poems:
        # 如果没有数据，使用默认数据
        return """
-- 宋词插入语句
INSERT INTO song_poetry (title, author, dynasty, content, genre, ci_pai, url, main_imagery, emotions) VALUES
('水调歌头·明月几时有', '苏轼', '宋代', '明月几时有？把酒问青天。不知天上宫阙，今夕是何年。我欲乘风归去，又恐琼楼玉宇，高处不胜寒。起舞弄清影，何似在人间？转朱阁，低绮户，照无眠。不应有恨，何事长向别时圆？人有悲欢离合，月有阴晴圆缺，此事古难全。但愿人长久，千里共婵娟。', '词', '水调歌头', 'https://www.gushiwen.cn/shiwenv_6d817b79b8aa.aspx', '明月,青天,宫阙,琼楼玉宇', '思乡怀人,人生哲理,感慨伤怀'),
('念奴娇·赤壁怀古', '苏轼', '宋代', '大江东去，浪淘尽，千古风流人物。故垒西边，人道是，三国周郎赤壁。乱石穿空，惊涛拍岸，卷起千堆雪。江山如画，一时多少豪杰。遥想公瑾当年，小乔初嫁了，雄姿英发。羽扇纶巾，谈笑间，樯橹灰飞烟灭。故国神游，多情应笑我，早生华发。人生如梦，一尊还酹江月。', '词', '念奴娇', 'https://www.gushiwen.cn/shiwenv_4771121c9b51.aspx', '长江,赤壁,乱石,惊涛,雪', '咏史怀古,壮志豪情,感慨伤怀');
"""
    
    sql_statements = []
    for poem in poems:
        # 提取必要字段，使用默认值处理缺失字段
        title = poem.get('title', '').replace("'", "''")
        author = poem.get('author', '').replace("'", "''")
        dynasty = poem.get('dynasty', '宋代').replace("'", "''")
        content = poem.get('content', '').replace("'", "''")
        genre = poem.get('genre', '词').replace("'", "''")
        ci_pai = poem.get('ci_pai', '').replace("'", "''")
        url = poem.get('url', '').replace("'", "''")
        
        # 处理意象字段
        main_imagery = ''
        if 'main_imagery' in poem:
            if isinstance(poem['main_imagery'], list):
                main_imagery = ','.join(poem['main_imagery']).replace("'", "''")
            elif isinstance(poem['main_imagery'], str):
                main_imagery = poem['main_imagery'].replace("'", "''")
        
        # 处理情感字段
        emotions = ''
        if 'emotions' in poem:
            if isinstance(poem['emotions'], list):
                emotions = ','.join(poem['emotions']).replace("'", "''")
            elif isinstance(poem['emotions'], str):
                emotions = poem['emotions'].replace("'", "''")
        
        # 构造插入语句
        sql = f"('{title}', '{author}', '{dynasty}', '{content}', '{genre}', '{ci_pai}', '{url}', '{main_imagery}', '{emotions}')"
        sql_statements.append(sql)
    
    # 拼接完整的INSERT语句
    if sql_statements:
        values_str = ',\n'.join(sql_statements)
        return f"""
-- 宋词插入语句
INSERT INTO song_poetry (title, author, dynasty, content, genre, ci_pai, url, main_imagery, emotions) VALUES
{values_str};
"""
    return ""

def main():
    # 创建完整的SQL文件
    full_sql = """
-- 古诗文数据库创建脚本
-- 包含表结构和所有数据插入语句

-- 创建数据库（可选）
-- CREATE DATABASE IF NOT EXISTS poetry_db DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE poetry_db;

-- 创建唐诗表
CREATE TABLE tang_poetry (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL COMMENT '标题',
    author VARCHAR(100) NOT NULL COMMENT '作者',
    dynasty VARCHAR(50) NOT NULL COMMENT '朝代',
    content TEXT NOT NULL COMMENT '正文',
    genre VARCHAR(100) NOT NULL COMMENT '体裁',
    url VARCHAR(255) COMMENT '原文链接',
    main_imagery TEXT COMMENT '主要意象，用逗号分隔',
    emotions TEXT COMMENT '主要思想感情，用逗号分隔',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建宋词表
CREATE TABLE song_poetry (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL COMMENT '标题',
    author VARCHAR(100) NOT NULL COMMENT '作者',
    dynasty VARCHAR(50) NOT NULL COMMENT '朝代',
    content TEXT NOT NULL COMMENT '正文',
    genre VARCHAR(100) NOT NULL COMMENT '体裁',
    ci_pai VARCHAR(100) NOT NULL COMMENT '词牌名',
    url VARCHAR(255) COMMENT '原文链接',
    main_imagery TEXT COMMENT '主要意象，用逗号分隔',
    emotions TEXT COMMENT '主要思想感情，用逗号分隔',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 添加索引
CREATE INDEX idx_tang_author ON tang_poetry(author);
CREATE INDEX idx_tang_title ON tang_poetry(title);
CREATE INDEX idx_song_author ON song_poetry(author);
CREATE INDEX idx_song_title ON song_poetry(title);
CREATE INDEX idx_song_ci_pai ON song_poetry(ci_pai);
"""
    
    # 读取JSON文件并生成插入语句
    print("正在读取唐诗数据...")
    tang_poems = read_json_file(TANG_COMPLETE_FILE)
    tang_sql = generate_tang_sql(tang_poems)
    
    print("正在读取宋词数据...")
    song_poems = read_json_file(SONG_COMPLETE_FILE)
    song_sql = generate_song_sql(song_poems)
    
    # 合并所有SQL语句
    full_sql += tang_sql
    full_sql += song_sql
    
    # 添加一些常用查询示例
    full_sql += """

-- 常用查询示例
-- 1. 查询所有李白的唐诗
-- SELECT * FROM tang_poetry WHERE author = '李白';

-- 2. 查询所有包含'月'意象的诗词
-- SELECT * FROM tang_poetry WHERE main_imagery LIKE '%月%'
-- UNION
-- SELECT * FROM song_poetry WHERE main_imagery LIKE '%月%';

-- 3. 查询所有表达思乡情感的诗词
-- SELECT * FROM tang_poetry WHERE emotions LIKE '%思乡%'
-- UNION
-- SELECT * FROM song_poetry WHERE emotions LIKE '%思乡%';

-- 4. 按作者统计诗词数量
-- SELECT author, COUNT(*) AS poem_count FROM tang_poetry GROUP BY author ORDER BY poem_count DESC;
-- SELECT author, COUNT(*) AS poem_count FROM song_poetry GROUP BY author ORDER BY poem_count DESC;
"""
    
    # 保存到SQL文件
    with open(OUTPUT_SQL_FILE, 'w', encoding='utf-8') as f:
        f.write(full_sql)
    
    print(f"SQL文件已生成: {OUTPUT_SQL_FILE}")
    print(f"包含唐诗数据: {len(tang_poems)} 首")
    print(f"包含宋词数据: {len(song_poems)} 首")
    print("\n使用方法:")
    print("1. 打开MySQL客户端")
    print("2. 创建数据库: CREATE DATABASE poetry_db DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print("3. 选择数据库: USE poetry_db;")
    print("4. 导入SQL文件: source " + OUTPUT_SQL_FILE)

if __name__ == "__main__":
    main()
