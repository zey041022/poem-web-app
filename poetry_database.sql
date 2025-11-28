-- 创建诗词数据库表结构
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
    imagery_details TEXT COMMENT '意象详细分析（JSON格式）',
    emotion_details TEXT COMMENT '情感详细分析（JSON格式）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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
    imagery_details TEXT COMMENT '意象详细分析（JSON格式）',
    emotion_details TEXT COMMENT '情感详细分析（JSON格式）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 唐诗示例数据插入
INSERT INTO tang_poetry (title, author, dynasty, content, genre, url, main_imagery, emotions) VALUES
('静夜思', '李白', '唐代', '床前明月光，疑是地上霜。举头望明月，低头思故乡。', '五言绝句', 'https://www.gushiwen.cn/shiwenv_9b8e95f39c0a.aspx', '明月,床前,地霜', '思乡怀人,感慨伤怀'),
('望庐山瀑布', '李白', '唐代', '日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_653a968147a5.aspx', '瀑布,银河,香炉,紫烟', '山水田园,惊叹赞美'),
('黄鹤楼送孟浩然之广陵', '李白', '唐代', '故人西辞黄鹤楼，烟花三月下扬州。孤帆远影碧空尽，唯见长江天际流。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_2f74d036a3be.aspx', '黄鹤楼,孤帆,长江,碧空', '送别惜别,感慨伤怀');

-- 宋词示例数据插入
INSERT INTO song_poetry (title, author, dynasty, content, genre, ci_pai, url, main_imagery, emotions) VALUES
('水调歌头·明月几时有', '苏轼', '宋代', '明月几时有？把酒问青天。不知天上宫阙，今夕是何年。我欲乘风归去，又恐琼楼玉宇，高处不胜寒。起舞弄清影，何似在人间？转朱阁，低绮户，照无眠。不应有恨，何事长向别时圆？人有悲欢离合，月有阴晴圆缺，此事古难全。但愿人长久，千里共婵娟。', '词', '水调歌头', 'https://www.gushiwen.cn/shiwenv_6d817b79b8aa.aspx', '明月,青天,宫阙,琼楼玉宇', '思乡怀人,人生哲理,感慨伤怀'),
('念奴娇·赤壁怀古', '苏轼', '宋代', '大江东去，浪淘尽，千古风流人物。故垒西边，人道是，三国周郎赤壁。乱石穿空，惊涛拍岸，卷起千堆雪。江山如画，一时多少豪杰。遥想公瑾当年，小乔初嫁了，雄姿英发。羽扇纶巾，谈笑间，樯橹灰飞烟灭。故国神游，多情应笑我，早生华发。人生如梦，一尊还酹江月。', '词', '念奴娇', 'https://www.gushiwen.cn/shiwenv_4771121c9b51.aspx', '长江,赤壁,乱石,惊涛,雪', '咏史怀古,壮志豪情,感慨伤怀');

-- 创建索引以提高查询性能
CREATE INDEX idx_tang_author ON tang_poetry(author);
CREATE INDEX idx_tang_title ON tang_poetry(title);
CREATE INDEX idx_song_author ON song_poetry(author);
CREATE INDEX idx_song_title ON song_poetry(title);
CREATE INDEX idx_song_ci_pai ON song_poetry(ci_pai);

-- 完整导入说明：
-- 1. 对于完整数据导入，可以编写Python脚本读取JSON文件并批量插入数据
-- 2. 可以使用参数化查询防止SQL注入
-- 3. 对于imagery_details和emotion_details字段，可以存储完整的JSON分析结果
-- 4. 建议使用事务处理确保数据完整性