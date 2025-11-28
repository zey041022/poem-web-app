import requests
from bs4 import BeautifulSoup
import time
import random
import json

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_tang_poetry_links():
    """获取唐诗链接列表"""
    links = []
    page = 1
    
    print("开始获取唐诗链接...")
    
    while len(links) < 100:
        # 古诗文网唐诗页面
        url = f'https://www.gushiwen.cn/tangshi/default.aspx?p={page}'
        
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
    
    print(f"共获取到{len(links)}个唐诗链接")
    return links[:100]

def crawl_poem_detail(link):
    """爬取单首诗词的详细信息"""
    try:
        response = requests.get(link, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 获取标题
        title = soup.select_one('.cont h1').text.strip()
        
        # 获取作者
        author_info = soup.select_one('.cont .source').text.strip()
        # 提取作者名字（通常格式：朝代 作者）
        if ' ' in author_info:
            dynasty = author_info.split(' ')[0]
            author = author_info.split(' ')[1]
        else:
            dynasty = '唐代'
            author = author_info
        
        # 获取正文
        content_tags = soup.select('.cont .contson')
        if content_tags:
            content = ''.join([tag.text.strip() for tag in content_tags])
        else:
            content = ''
        
        # 尝试判断体裁
        # 简单的体裁判断：根据标题长度和内容结构
        lines = content.split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        
        if len(lines) == 4 and all(len(line) in [5, 7] for line in lines):
            # 五言或七言绝句
            if all(len(line) == 5 for line in lines):
                genre = '五言绝句'
            else:
                genre = '七言绝句'
        elif len(lines) == 8 and all(len(line) in [5, 7] for line in lines):
            # 五言或七言律诗
            if all(len(line) == 5 for line in lines):
                genre = '五言律诗'
            else:
                genre = '七言律诗'
        else:
            genre = '古体诗'
        
        poem_data = {
            'title': title,
            'author': author,
            'dynasty': dynasty,
            'content': content,
            'genre': genre,
            'url': link
        }
        
        return poem_data
        
    except Exception as e:
        print(f"爬取 {link} 时出错: {e}")
        return None

def main():
    """主函数"""
    # 获取唐诗链接
    links = get_tang_poetry_links()
    
    # 爬取详细信息
    poems = []
    print("开始爬取唐诗详细信息...")
    
    for i, link in enumerate(links, 1):
        print(f"正在爬取第{i}/100首唐诗: {link}")
        poem_data = crawl_poem_detail(link)
        
        if poem_data:
            poems.append(poem_data)
            # 保存已爬取的数据
            with open('tang_poems_temp.json', 'w', encoding='utf-8') as f:
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
    with open('tang_poems.json', 'w', encoding='utf-8') as f:
        json.dump(unique_poems, f, ensure_ascii=False, indent=2)
    
    print(f"唐诗爬取完成！共获取{len(unique_poems)}首不重复的唐诗")

if __name__ == '__main__':
    main()