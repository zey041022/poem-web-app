import requests
from bs4 import BeautifulSoup
import time
import random
import json

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_song_poetry_links():
    """获取宋词链接列表"""
    links = []
    page = 1
    
    print("开始获取宋词链接...")
    
    while len(links) < 100:
        # 古诗文网宋词页面
        url = f'https://www.gushiwen.cn/songci/default.aspx?p={page}'
        
        try:
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 获取每页的诗词链接
            poem_items = soup.select('.sons .cont')
            for item in poem_items:
                title_tag = item.select_one('p a')
                if title_tag and 'href' in title_tag.attrs:
                    link = 'https://www.gushiwen.cn' + title_tag['href']
                    links.append(link)
                    if len(links) >= 100:
                        break
            
            print(f"第{page}页完成，已获取{len(links)}个链接")
            page += 1
            
            # 随机延时，避免被封
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"获取链接时出错: {e}")
            time.sleep(5)
    
    print(f"共获取到{len(links)}个宋词链接")
    return links[:100]

def crawl_poem_detail(link):
    """爬取单首宋词的详细信息"""
    try:
        response = requests.get(link, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 获取标题（可能包含词牌名）
        title = soup.select_one('.cont h1').text.strip()
        
        # 获取作者信息
        author_info = soup.select_one('.cont .source').text.strip()
        # 提取作者名字（通常格式：朝代 作者）
        if ' ' in author_info:
            dynasty = author_info.split(' ')[0]
            author = author_info.split(' ')[1]
        else:
            dynasty = '宋代'
            author = author_info
        
        # 获取正文
        content_tags = soup.select('.cont .contson')
        if content_tags:
            content = ''.join([tag.text.strip() for tag in content_tags])
        else:
            content = ''
        
        # 判断词牌名
        ci_pai = ''
        if title.count('·') > 0 or title.count('（') > 0 or title.count('(') > 0:
            # 如果标题包含分隔符，尝试提取词牌名
            if '·' in title:
                ci_pai = title.split('·')[0].strip()
            elif '（' in title and '）' in title:
                ci_pai = title[:title.find('（')].strip()
            elif '(' in title and ')' in title:
                ci_pai = title[:title.find('(')].strip()
        else:
            # 如果没有分隔符，整个标题可能就是词牌名
            ci_pai = title
        
        # 宋词的体裁通常就是词牌名
        genre = f'词（{ci_pai}）'
        
        poem_data = {
            'title': title,
            'author': author,
            'dynasty': dynasty,
            'content': content,
            'genre': genre,
            'ci_pai': ci_pai,
            'url': link
        }
        
        return poem_data
        
    except Exception as e:
        print(f"爬取 {link} 时出错: {e}")
        return None

def main():
    """主函数"""
    # 获取宋词链接
    links = get_song_poetry_links()
    
    # 爬取详细信息
    poems = []
    print("开始爬取宋词详细信息...")
    
    for i, link in enumerate(links, 1):
        print(f"正在爬取第{i}/100首宋词: {link}")
        poem_data = crawl_poem_detail(link)
        
        if poem_data:
            poems.append(poem_data)
            # 保存已爬取的数据
            with open('song_poems_temp.json', 'w', encoding='utf-8') as f:
                json.dump(poems, f, ensure_ascii=False, indent=2)
        
        # 随机延时
        time.sleep(random.uniform(2, 5))
    
    # 去重
    unique_poems = []
    titles = set()
    for poem in poems:
        if poem['title'] not in titles:
            titles.add(poem['title'])
            unique_poems.append(poem)
    
    # 保存最终结果
    with open('song_poems.json', 'w', encoding='utf-8') as f:
        json.dump(unique_poems, f, ensure_ascii=False, indent=2)
    
    print(f"宋词爬取完成！共获取{len(unique_poems)}首不重复的宋词")

if __name__ == '__main__':
    main()