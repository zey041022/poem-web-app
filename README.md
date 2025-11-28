# 古诗文爬取与分析系统

本项目用于从古诗文网爬取唐诗宋词数据，并进行意象和情感分析。

## 功能特点

1. **数据爬取**：自动从 https://www.gushiwen.cn/ 爬取唐诗和宋词
   - 每类诗词爬取100首不重复作品
   - 包含标题、作者、正文、体裁等信息

2. **意象分析**：提取诗词中的主要意象
   - 按自然意象（天文、地理、植物、动物）和人文意象（器物、建筑、时间、情感相关）分类
   - 统计意象出现频率和主要类别

3. **情感分析**：识别诗词中的主要思想感情
   - 包括思乡怀人、壮志豪情、感慨伤怀、闲适愉悦等情感类别
   - 分析情感强度和关键词

4. **数据验证**：确保爬取和分析的数据质量

5. **报告生成**：生成完整的数据分析报告

## 项目结构

```
诗界2.0/
├── crawl_tang_poetry.py    # 爬取唐诗的脚本
├── crawl_song_poetry.py    # 爬取宋词的脚本
├── analyze_imagery.py      # 意象分析脚本
├── analyze_emotion.py      # 情感分析脚本
├── main.py                 # 主程序，整合所有功能
├── README.md               # 项目说明文档
└── 生成的数据文件/         # 执行后会生成的文件
```

## 生成的数据文件

- `tang_poems.json` - 爬取的唐诗数据
- `song_poems.json` - 爬取的宋词数据
- `tang_poems_with_imagery.json` - 带意象分析的唐诗数据
- `song_poems_with_imagery.json` - 带意象分析的宋词数据
- `tang_poems_with_emotion.json` - 带情感分析的唐诗数据
- `song_poems_with_emotion.json` - 带情感分析的宋词数据
- `tang_poems_complete_analysis.json` - 完整分析的唐诗数据
- `song_poems_complete_analysis.json` - 完整分析的宋词数据
- `imagery_statistics.json` - 意象统计数据
- `emotion_statistics.json` - 情感统计数据
- `analysis_report.json` - 最终分析报告

## 使用方法

### 1. 安装依赖

程序会自动检查并安装必要的依赖库，但也可以手动安装：

```bash
pip install requests beautifulsoup4 lxml
```

### 2. 运行程序

直接运行主程序即可：

```bash
python main.py
```

程序会自动执行以下步骤：
- 检查必要的依赖库
- 爬取唐诗和宋词（如果数据文件不存在）
- 验证爬取的数据
- 进行意象分析
- 进行情感分析
- 合并分析结果
- 生成分析报告

### 3. 单独运行功能

也可以单独运行各个功能模块：

```bash
# 仅爬取唐诗
python crawl_tang_poetry.py

# 仅爬取宋词
python crawl_song_poetry.py

# 仅分析意象
python analyze_imagery.py

# 仅分析情感
python analyze_emotion.py
```

## 数据格式说明

完整分析后的数据格式示例：

```json
{
  "title": "静夜思",
  "author": "李白",
  "dynasty": "唐代",
  "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
  "genre": "五言绝句",
  "imagery": ["月", "床", "地", "霜"],
  "main_emotions": ["思乡怀人", "感慨伤怀"],
  "imagery_details": {...},  # 详细的意象分析数据
  "emotion_details": {...}   # 详细的情感分析数据
}
```

## 注意事项

1. 爬取过程中会有随机延时，以避免被网站封禁
2. 如果爬取失败，可以重新运行程序，已爬取的数据会被保留
3. 情感和意象分析基于关键词匹配，结果仅供参考
4. 分析结果可能会因网站内容更新而有所变化

## 技术栈

- Python 3.x
- Requests - 网络请求
- BeautifulSoup4 - HTML解析
- LXML - XML解析器
- JSON - 数据存储格式

## 作者

张恩扬

## 日期

2023年