
-- 古诗文数据库创建脚本
-- 包含表结构和所有数据插入语句

-- 创建数据库（可选）
-- CREATE DATABASE IF NOT EXISTS poetry_db DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE poetry_db;

-- 创建唐诗表
CREATE TABLE tang_poetry (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    dynasty VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    genre VARCHAR(100) NOT NULL,
    url VARCHAR(255),
    main_imagery TEXT,
    emotions TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 为tang_poetry表添加列注释
COMMENT ON COLUMN tang_poetry.title IS '标题';
COMMENT ON COLUMN tang_poetry.author IS '作者';
COMMENT ON COLUMN tang_poetry.dynasty IS '朝代';
COMMENT ON COLUMN tang_poetry.content IS '正文';
COMMENT ON COLUMN tang_poetry.genre IS '体裁';
COMMENT ON COLUMN tang_poetry.url IS '原文链接';
COMMENT ON COLUMN tang_poetry.main_imagery IS '主要意象，用逗号分隔';
COMMENT ON COLUMN tang_poetry.emotions IS '主要思想感情，用逗号分隔';

-- 创建宋词表
CREATE TABLE song_poetry (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    dynasty VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    genre VARCHAR(100) NOT NULL,
    ci_pai VARCHAR(100) NOT NULL,
    url VARCHAR(255),
    main_imagery TEXT,
    emotions TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 为song_poetry表添加列注释
COMMENT ON COLUMN song_poetry.title IS '标题';
COMMENT ON COLUMN song_poetry.author IS '作者';
COMMENT ON COLUMN song_poetry.dynasty IS '朝代';
COMMENT ON COLUMN song_poetry.content IS '正文';
COMMENT ON COLUMN song_poetry.genre IS '体裁';
COMMENT ON COLUMN song_poetry.ci_pai IS '词牌名';
COMMENT ON COLUMN song_poetry.url IS '原文链接';
COMMENT ON COLUMN song_poetry.main_imagery IS '主要意象，用逗号分隔';
COMMENT ON COLUMN song_poetry.emotions IS '主要思想感情，用逗号分隔';

-- 添加索引
CREATE INDEX idx_tang_author ON tang_poetry(author);
CREATE INDEX idx_tang_title ON tang_poetry(title);
CREATE INDEX idx_song_author ON song_poetry(author);
CREATE INDEX idx_song_title ON song_poetry(title);
CREATE INDEX idx_song_ci_pai ON song_poetry(ci_pai);

-- 唐诗插入语句
INSERT INTO tang_poetry (title, author, dynasty, content, genre, url, main_imagery, emotions) VALUES
('静夜思', '李白', '唐代', '床前明月光，疑是地上霜。举头望明月，低头思故乡。', '五言绝句', 'https://www.gushiwen.cn/shiwenv_9b8e95f39c0a.aspx', '', ''),
('望庐山瀑布', '李白', '唐代', '日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_653a968147a5.aspx', '', ''),
('黄鹤楼送孟浩然之广陵', '李白', '唐代', '故人西辞黄鹤楼，烟花三月下扬州。孤帆远影碧空尽，唯见长江天际流。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_2f74d036a3be.aspx', '', ''),
('望天门山', '李白', '唐代', '天门中断楚江开，碧水东流至此回。两岸青山相对出，孤帆一片日边来。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_7d404379a10a.aspx', '', ''),
('春望', '杜甫', '唐代', '国破山河在，城春草木深。感时花溅泪，恨别鸟惊心。烽火连三月，家书抵万金。白头搔更短，浑欲不胜簪。', '五言律诗', 'https://www.gushiwen.cn/shiwenv_7af80f457745.aspx', '', ''),
('登高', '杜甫', '唐代', '风急天高猿啸哀，渚清沙白鸟飞回。无边落木萧萧下，不尽长江滚滚来。万里悲秋常作客，百年多病独登台。艰难苦恨繁霜鬓，潦倒新停浊酒杯。', '七言律诗', 'https://www.gushiwen.cn/shiwenv_24c3b3a831a7.aspx', '', ''),
('绝句', '杜甫', '唐代', '两个黄鹂鸣翠柳，一行白鹭上青天。窗含西岭千秋雪，门泊东吴万里船。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_1e32f9115c1d.aspx', '', ''),
('赠汪伦', '李白', '唐代', '李白乘舟将欲行，忽闻岸上踏歌声。桃花潭水深千尺，不及汪伦送我情。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_f59a8c858d2c.aspx', '', ''),
('清明', '杜牧', '唐代', '清明时节雨纷纷，路上行人欲断魂。借问酒家何处有？牧童遥指杏花村。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_9d2fc3509ee3.aspx', '', ''),
('赤壁', '杜牧', '唐代', '折戟沉沙铁未销，自将磨洗认前朝。东风不与周郎便，铜雀春深锁二乔。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_a637dd08497e.aspx', '', ''),
('山居秋暝', '王维', '唐代', '空山新雨后，天气晚来秋。明月松间照，清泉石上流。竹喧归浣女，莲动下渔舟。随意春芳歇，王孙自可留。', '五言律诗', 'https://www.gushiwen.cn/shiwenv_790f29c68f13.aspx', '', ''),
('使至塞上', '王维', '唐代', '单车欲问边，属国过居延。征蓬出汉塞，归雁入胡天。大漠孤烟直，长河落日圆。萧关逢候骑，都护在燕然。', '五言律诗', 'https://www.gushiwen.cn/shiwenv_f2205bf8b413.aspx', '', ''),
('九月九日忆山东兄弟', '王维', '唐代', '独在异乡为异客，每逢佳节倍思亲。遥知兄弟登高处，遍插茱萸少一人。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_40015222e381.aspx', '', ''),
('送元二使安西', '王维', '唐代', '渭城朝雨浥轻尘，客舍青青柳色新。劝君更尽一杯酒，西出阳关无故人。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_a136b61d6376.aspx', '', ''),
('早发白帝城', '李白', '唐代', '朝辞白帝彩云间，千里江陵一日还。两岸猿声啼不住，轻舟已过万重山。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_21d0d83ba99a.aspx', '', ''),
('望洞庭', '刘禹锡', '唐代', '湖光秋月两相和，潭面无风镜未磨。遥望洞庭山水翠，白银盘里一青螺。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_22cf6a232b37.aspx', '', ''),
('乌衣巷', '刘禹锡', '唐代', '朱雀桥边野草花，乌衣巷口夕阳斜。旧时王谢堂前燕，飞入寻常百姓家。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_4c09b613786d.aspx', '', ''),
('赋得古原草送别', '白居易', '唐代', '离离原上草，一岁一枯荣。野火烧不尽，春风吹又生。远芳侵古道，晴翠接荒城。又送王孙去，萋萋满别情。', '五言律诗', 'https://www.gushiwen.cn/shiwenv_4e8b509c7f04.aspx', '', ''),
('大林寺桃花', '白居易', '唐代', '人间四月芳菲尽，山寺桃花始盛开。长恨春归无觅处，不知转入此中来。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_0ed243d8b383.aspx', '', ''),
('暮江吟', '白居易', '唐代', '一道残阳铺水中，半江瑟瑟半江红。可怜九月初三夜，露似真珠月似弓。', '七言绝句', 'https://www.gushiwen.cn/shiwenv_711771c1f46e.aspx', '', '');

-- 宋词插入语句
INSERT INTO song_poetry (title, author, dynasty, content, genre, ci_pai, url, main_imagery, emotions) VALUES
('水调歌头·明月几时有', '苏轼', '宋代', '明月几时有？把酒问青天。不知天上宫阙，今夕是何年。我欲乘风归去，又恐琼楼玉宇，高处不胜寒。起舞弄清影，何似在人间？转朱阁，低绮户，照无眠。不应有恨，何事长向别时圆？人有悲欢离合，月有阴晴圆缺，此事古难全。但愿人长久，千里共婵娟。', '词', '水调歌头', 'https://www.gushiwen.cn/shiwenv_6d817b79b8aa.aspx', '', ''),
('念奴娇·赤壁怀古', '苏轼', '宋代', '大江东去，浪淘尽，千古风流人物。故垒西边，人道是，三国周郎赤壁。乱石穿空，惊涛拍岸，卷起千堆雪。江山如画，一时多少豪杰。遥想公瑾当年，小乔初嫁了，雄姿英发。羽扇纶巾，谈笑间，樯橹灰飞烟灭。故国神游，多情应笑我，早生华发。人生如梦，一尊还酹江月。', '词', '念奴娇', 'https://www.gushiwen.cn/shiwenv_4771121c9b51.aspx', '', ''),
('如梦令·昨夜雨疏风骤', '李清照', '宋代', '昨夜雨疏风骤，浓睡不消残酒。试问卷帘人，却道海棠依旧。知否？知否？应是绿肥红瘦。', '词', '如梦令', 'https://www.gushiwen.cn/shiwenv_70a4b2d8159a.aspx', '', ''),
('声声慢·寻寻觅觅', '李清照', '宋代', '寻寻觅觅，冷冷清清，凄凄惨惨戚戚。乍暖还寒时候，最难将息。三杯两盏淡酒，怎敌他、晚来风急？雁过也，正伤心，却是旧时相识。满地黄花堆积。憔悴损，如今有谁堪摘？守着窗儿，独自怎生得黑？梧桐更兼细雨，到黄昏、点点滴滴。这次第，怎一个愁字了得！', '词', '声声慢', 'https://www.gushiwen.cn/shiwenv_3d29e5d5c5e6.aspx', '', ''),
('永遇乐·京口北固亭怀古', '辛弃疾', '宋代', '千古江山，英雄无觅孙仲谋处。舞榭歌台，风流总被雨打风吹去。斜阳草树，寻常巷陌，人道寄奴曾住。想当年，金戈铁马，气吞万里如虎。元嘉草草，封狼居胥，赢得仓皇北顾。四十三年，望中犹记，烽火扬州路。可堪回首，佛狸祠下，一片神鸦社鼓。凭谁问：廉颇老矣，尚能饭否？', '词', '永遇乐', 'https://www.gushiwen.cn/shiwenv_621575c57f3d.aspx', '', ''),
('破阵子·为陈同甫赋壮词以寄之', '辛弃疾', '宋代', '醉里挑灯看剑，梦回吹角连营。八百里分麾下炙，五十弦翻塞外声，沙场秋点兵。马作的卢飞快，弓如霹雳弦惊。了却君王天下事，赢得生前身后名。可怜白发生！', '词', '破阵子', 'https://www.gushiwen.cn/shiwenv_81133c07f1e2.aspx', '', ''),
('雨霖铃·寒蝉凄切', '柳永', '宋代', '寒蝉凄切，对长亭晚，骤雨初歇。都门帐饮无绪，留恋处，兰舟催发。执手相看泪眼，竟无语凝噎。念去去，千里烟波，暮霭沉沉楚天阔。多情自古伤离别，更那堪，冷落清秋节！今宵酒醒何处？杨柳岸，晓风残月。此去经年，应是良辰好景虚设。便纵有千种风情，更与何人说？', '词', '雨霖铃', 'https://www.gushiwen.cn/shiwenv_572a555c7d3a.aspx', '', ''),
('满江红·怒发冲冠', '岳飞', '宋代', '怒发冲冠，凭栏处、潇潇雨歇。抬望眼，仰天长啸，壮怀激烈。三十功名尘与土，八千里路云和月。莫等闲，白了少年头，空悲切！靖康耻，犹未雪。臣子恨，何时灭！驾长车，踏破贺兰山缺。壮志饥餐胡虏肉，笑谈渴饮匈奴血。待从头、收拾旧山河，朝天阙。', '词', '满江红', 'https://www.gushiwen.cn/shiwenv_93d57e36e8d7.aspx', '', ''),
('相见欢·无言独上西楼', '李煜', '五代', '无言独上西楼，月如钩。寂寞梧桐深院锁清秋。剪不断，理还乱，是离愁。别是一般滋味在心头。', '词', '相见欢', 'https://www.gushiwen.cn/shiwenv_7e7c7d8b4c1f.aspx', '', ''),
('虞美人·春花秋月何时了', '李煜', '五代', '春花秋月何时了？往事知多少。小楼昨夜又东风，故国不堪回首月明中。雕栏玉砌应犹在，只是朱颜改。问君能有几多愁？恰似一江春水向东流。', '词', '虞美人', 'https://www.gushiwen.cn/shiwenv_f3d7e8275d1c.aspx', '', ''),
('西江月·夜行黄沙道中', '辛弃疾', '宋代', '明月别枝惊鹊，清风半夜鸣蝉。稻花香里说丰年，听取蛙声一片。七八个星天外，两三点雨山前。旧时茅店社林边，路转溪桥忽见。', '词', '西江月', 'https://www.gushiwen.cn/shiwenv_5d3c17c1e7d8.aspx', '', ''),
('卜算子·咏梅', '陆游', '宋代', '驿外断桥边，寂寞开无主。已是黄昏独自愁，更着风和雨。无意苦争春，一任群芳妒。零落成泥碾作尘，只有香如故。', '词', '卜算子', 'https://www.gushiwen.cn/shiwenv_8c5a3e157c2d.aspx', '', ''),
('钗头凤·红酥手', '陆游', '宋代', '红酥手，黄縢酒，满城春色宫墙柳。东风恶，欢情薄。一怀愁绪，几年离索。错、错、错。春如旧，人空瘦，泪痕红浥鲛绡透。桃花落，闲池阁。山盟虽在，锦书难托。莫、莫、莫！', '词', '钗头凤', 'https://www.gushiwen.cn/shiwenv_4d8a3c72e5d7.aspx', '', ''),
('水龙吟·登建康赏心亭', '辛弃疾', '宋代', '楚天千里清秋，水随天去秋无际。遥岑远目，献愁供恨，玉簪螺髻。落日楼头，断鸿声里，江南游子。把吴钩看了，栏杆拍遍，无人会，登临意。休说鲈鱼堪脍，尽西风，季鹰归未？求田问舍，怕应羞见，刘郎才气。可惜流年，忧愁风雨，树犹如此！倩何人唤取，红巾翠袖，揾英雄泪？', '词', '水龙吟', 'https://www.gushiwen.cn/shiwenv_52d7c58e3a1f.aspx', '', ''),
('一剪梅·红藕香残玉簟秋', '李清照', '宋代', '红藕香残玉簟秋。轻解罗裳，独上兰舟。云中谁寄锦书来？雁字回时，月满西楼。花自飘零水自流。一种相思，两处闲愁。此情无计可消除，才下眉头，却上心头。', '词', '一剪梅', 'https://www.gushiwen.cn/shiwenv_8e3a2c15d7c6.aspx', '', ''),
('浣溪沙·一曲新词酒一杯', '晏殊', '宋代', '一曲新词酒一杯，去年天气旧亭台。夕阳西下几时回？无可奈何花落去，似曾相识燕归来。小园香径独徘徊。', '词', '浣溪沙', 'https://www.gushiwen.cn/shiwenv_6e3c15d8a2c7.aspx', '', ''),
('蝶恋花·庭院深深深几许', '欧阳修', '宋代', '庭院深深深几许，杨柳堆烟，帘幕无重数。玉勒雕鞍游冶处，楼高不见章台路。雨横风狂三月暮，门掩黄昏，无计留春住。泪眼问花花不语，乱红飞过秋千去。', '词', '蝶恋花', 'https://www.gushiwen.cn/shiwenv_3a8e15c7d2c6.aspx', '', ''),
('江城子·密州出猎', '苏轼', '宋代', '老夫聊发少年狂，左牵黄，右擎苍，锦帽貂裘，千骑卷平冈。为报倾城随太守，亲射虎，看孙郎。酒酣胸胆尚开张，鬓微霜，又何妨！持节云中，何日遣冯唐？会挽雕弓如满月，西北望，射天狼。', '词', '江城子', 'https://www.gushiwen.cn/shiwenv_5c7e82a13d6c.aspx', '', ''),
('江城子·十年生死两茫茫', '苏轼', '宋代', '十年生死两茫茫，不思量，自难忘。千里孤坟，无处话凄凉。纵使相逢应不识，尘满面，鬓如霜。夜来幽梦忽还乡，小轩窗，正梳妆。相顾无言，惟有泪千行。料得年年肠断处，明月夜，短松冈。', '词', '江城子', 'https://www.gushiwen.cn/shiwenv_7c5d2a13e8d6.aspx', '', ''),
('青玉案·元夕', '辛弃疾', '宋代', '东风夜放花千树。更吹落、星如雨。宝马雕车香满路。凤箫声动，玉壶光转，一夜鱼龙舞。蛾儿雪柳黄金缕。笑语盈盈暗香去。众里寻他千百度。蓦然回首，那人却在，灯火阑珊处。', '词', '青玉案', 'https://www.gushiwen.cn/shiwenv_4a13e8d6c572.aspx', '', '');


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
