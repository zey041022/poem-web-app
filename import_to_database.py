import json
import os
import mysql.connector
from mysql.connector import Error

def connect_to_database(host='localhost', user='root', password='', database='poetry_db'):
    """连接到MySQL数据库"""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        print(f"成功连接到数据库: {database}")
        return conn
    except Error as e:
        print(f"数据库连接失败: {e}")
        print("请确保MySQL服务已启动，并且用户名密码正确")
        return None

def create_tables(conn):
    """创建必要的数据表"""
    cursor = conn.cursor()
    
    # 创建唐诗表
    tang_table_sql = """
    CREATE TABLE IF NOT EXISTS tang_poetry (
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(255) NOT NULL COMMENT '标题',
        author VARCHAR(100) NOT NULL COMMENT '作者',
        dynasty VARCHAR(50) NOT NULL COMMENT '朝代',
        content TEXT NOT NULL COMMENT '正文',
        genre VARCHAR(100) NOT NULL COMMENT '体裁',
        url VARCHAR(255) COMMENT '原文链接',
        main_imagery TEXT COMMENT '主要意象，用逗号分隔',
        emotions TEXT COMMENT '主要思想感情，用逗号分隔',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    # 创建宋词表
    song_table_sql = """
    CREATE TABLE IF NOT EXISTS song_poetry (
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    try:
        cursor.execute(tang_table_sql)
        cursor.execute(song_table_sql)
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tang_author ON tang_poetry(author)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tang_title ON tang_poetry(title)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_song_author ON song_poetry(author)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_song_title ON song_poetry(title)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_song_ci_pai ON song_poetry(ci_pai)")
        
        conn.commit()
        print("数据表和索引创建成功")
    except Error as e:
        print(f"创建表失败: {e}")
        conn.rollback()
    finally:
        cursor.close()

def read_json_file(file_path):
    """读取JSON文件"""
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def import_tang_poems(conn, poems):
    """导入唐诗数据"""
    cursor = conn.cursor()
    
    # 先清空表（可选）
    # cursor.execute("DELETE FROM tang_poetry")
    
    insert_sql = """
    INSERT INTO tang_poetry (title, author, dynasty, content, genre, url, main_imagery, emotions)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    count = 0
    try:
        for poem in poems:
            # 提取数据，设置默认值
            title = poem.get('title', '')
            author = poem.get('author', '')
            dynasty = poem.get('dynasty', '唐代')
            content = poem.get('content', '')
            genre = poem.get('genre', '')
            url = poem.get('url', '')
            
            # 处理意象
            main_imagery = ''
            if 'main_imagery' in poem:
                if isinstance(poem['main_imagery'], list):
                    main_imagery = ','.join(poem['main_imagery'])
                else:
                    main_imagery = str(poem['main_imagery'])
            
            # 处理情感
            emotions = ''
            if 'emotions' in poem:
                if isinstance(poem['emotions'], list):
                    emotions = ','.join(poem['emotions'])
                else:
                    emotions = str(poem['emotions'])
            
            # 使用参数化查询
            cursor.execute(insert_sql, (
                title, author, dynasty, content, genre, url, main_imagery, emotions
            ))
            count += 1
            
            # 每10条提交一次
            if count % 10 == 0:
                conn.commit()
                print(f"已导入 {count} 首唐诗")
        
        # 最后一次提交
        conn.commit()
        print(f"唐诗导入完成，共导入 {count} 首")
    except Error as e:
        print(f"导入唐诗失败: {e}")
        conn.rollback()
    finally:
        cursor.close()

def import_song_poems(conn, poems):
    """导入宋词数据"""
    cursor = conn.cursor()
    
    # 先清空表（可选）
    # cursor.execute("DELETE FROM song_poetry")
    
    insert_sql = """
    INSERT INTO song_poetry (title, author, dynasty, content, genre, ci_pai, url, main_imagery, emotions)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    count = 0
    try:
        for poem in poems:
            # 提取数据，设置默认值
            title = poem.get('title', '')
            author = poem.get('author', '')
            dynasty = poem.get('dynasty', '宋代')
            content = poem.get('content', '')
            genre = poem.get('genre', '词')
            ci_pai = poem.get('ci_pai', '')
            url = poem.get('url', '')
            
            # 处理意象
            main_imagery = ''
            if 'main_imagery' in poem:
                if isinstance(poem['main_imagery'], list):
                    main_imagery = ','.join(poem['main_imagery'])
                else:
                    main_imagery = str(poem['main_imagery'])
            
            # 处理情感
            emotions = ''
            if 'emotions' in poem:
                if isinstance(poem['emotions'], list):
                    emotions = ','.join(poem['emotions'])
                else:
                    emotions = str(poem['emotions'])
            
            # 使用参数化查询
            cursor.execute(insert_sql, (
                title, author, dynasty, content, genre, ci_pai, url, main_imagery, emotions
            ))
            count += 1
            
            # 每10条提交一次
            if count % 10 == 0:
                conn.commit()
                print(f"已导入 {count} 首宋词")
        
        # 最后一次提交
        conn.commit()
        print(f"宋词导入完成，共导入 {count} 首")
    except Error as e:
        print(f"导入宋词失败: {e}")
        conn.rollback()
    finally:
        cursor.close()

def test_database_queries(conn):
    """测试数据库查询"""
    cursor = conn.cursor()
    
    print("\n=== 数据库查询测试 ===")
    
    # 查询唐诗数量
    cursor.execute("SELECT COUNT(*) FROM tang_poetry")
    tang_count = cursor.fetchone()[0]
    print(f"唐诗总数: {tang_count}")
    
    # 查询宋词数量
    cursor.execute("SELECT COUNT(*) FROM song_poetry")
    song_count = cursor.fetchone()[0]
    print(f"宋词总数: {song_count}")
    
    # 查询几个示例数据
    print("\n唐诗前3首:")
    cursor.execute("SELECT title, author FROM tang_poetry LIMIT 3")
    for row in cursor.fetchall():
        print(f"- {row[0]} - {row[1]}")
    
    print("\n宋词前3首:")
    cursor.execute("SELECT title, author FROM song_poetry LIMIT 3")
    for row in cursor.fetchall():
        print(f"- {row[0]} - {row[1]}")
    
    cursor.close()

def main():
    # 数据库连接信息（请根据实际情况修改）
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # MySQL密码
        'database': 'poetry_db'
    }
    
    # 提示用户输入数据库密码
    print("=== 古诗文数据库导入工具 ===")
    db_config['password'] = input("请输入MySQL密码（默认为空）: ")
    
    # 连接数据库
    conn = connect_to_database(**db_config)
    if not conn:
        print("程序退出")
        return
    
    try:
        # 创建数据表
        create_tables(conn)
        
        # 读取JSON数据
        print("\n正在读取数据文件...")
        tang_poems = read_json_file('tang_poems_complete_analysis.json')
        song_poems = read_json_file('song_poems_complete_analysis.json')
        
        # 如果没有完整分析文件，尝试使用基础文件
        if not tang_poems:
            tang_poems = read_json_file('tang_poems.json')
        if not song_poems:
            song_poems = read_json_file('song_poems.json')
        
        # 导入数据
        print("\n开始导入数据...")
        if tang_poems:
            import_tang_poems(conn, tang_poems)
        else:
            print("没有找到唐诗数据文件")
        
        if song_poems:
            import_song_poems(conn, song_poems)
        else:
            print("没有找到宋词数据文件")
        
        # 测试查询
        test_database_queries(conn)
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    finally:
        if conn.is_connected():
            conn.close()
            print("\n数据库连接已关闭")

if __name__ == "__main__":
    main()
