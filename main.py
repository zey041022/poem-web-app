import os
import json
import subprocess
import time
import sys

def check_dependencies():
    """检查必要的依赖库"""
    print("检查必要的依赖库...")
    required_libraries = ['requests', 'beautifulsoup4', 'lxml']
    
    missing_libraries = []
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            missing_libraries.append(lib)
    
    if missing_libraries:
        print(f"缺少以下必要的库: {', '.join(missing_libraries)}")
        print("正在安装缺失的库...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_libraries])
            print("库安装成功！")
        except Exception as e:
            print(f"安装库时出错: {e}")
            return False
    else:
        print("所有必要的库已安装。")
    
    return True

def run_script(script_name, description):
    """运行指定的Python脚本"""
    print(f"\n===== {description} =====")
    try:
        start_time = time.time()
        result = subprocess.run([sys.executable, script_name], 
                               cwd=os.getcwd(), 
                               capture_output=True, 
                               text=True)
        
        # 打印输出
        print(result.stdout)
        if result.stderr:
            print(f"警告 (stderr): {result.stderr}")
        
        end_time = time.time()
        print(f"{description}完成，耗时: {end_time - start_time:.2f}秒")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"运行{script_name}时出错: {e}")
        return False

def validate_data(file_path, expected_count):
    """验证爬取的数据是否符合要求"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查数据量
        if len(data) < expected_count:
            print(f"警告: {file_path} 中只有{len(data)}条数据，少于预期的{expected_count}条")
            return False
        
        # 检查数据完整性
        required_fields = ['title', 'author', 'content', 'genre']
        for i, item in enumerate(data):
            missing_fields = [field for field in required_fields if field not in item]
            if missing_fields:
                print(f"警告: 第{i+1}条数据缺少字段: {', '.join(missing_fields)}")
                return False
            
            # 检查内容是否为空
            if not item['content'].strip():
                print(f"警告: 第{i+1}条数据内容为空")
                return False
        
        print(f"{file_path} 数据验证通过！共{len(data)}条有效数据")
        return True
        
    except Exception as e:
        print(f"验证{file_path}时出错: {e}")
        return False

def validate_analysis_results(file_path):
    """验证分析结果数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查分析字段
        for i, item in enumerate(data):
            if 'imagery' not in item:
                print(f"警告: 第{i+1}条数据缺少意象分析")
                return False
            if 'main_emotions' not in item:
                print(f"警告: 第{i+1}条数据缺少情感分析")
                return False
        
        print(f"{file_path} 分析结果验证通过！")
        return True
        
    except Exception as e:
        print(f"验证{file_path}分析结果时出错: {e}")
        return False

def generate_report():
    """生成最终的数据分析报告"""
    print("\n===== 生成数据分析报告 =====")
    
    report = {
        'project': '古诗文爬取与分析',
        'date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'summary': {},
        'statistics': {}
    }
    
    # 读取唐诗和宋词的完整分析结果
    try:
        # 读取唐诗分析结果
        with open('tang_poems_complete_analysis.json', 'r', encoding='utf-8') as f:
            tang_data = json.load(f)
        report['summary']['tang_poems'] = len(tang_data)
        
        # 读取宋词分析结果
        with open('song_poems_complete_analysis.json', 'r', encoding='utf-8') as f:
            song_data = json.load(f)
        report['summary']['song_poems'] = len(song_data)
        
        # 读取统计数据
        if os.path.exists('imagery_statistics.json'):
            with open('imagery_statistics.json', 'r', encoding='utf-8') as f:
                report['statistics']['imagery'] = json.load(f)
        
        if os.path.exists('emotion_statistics.json'):
            with open('emotion_statistics.json', 'r', encoding='utf-8') as f:
                report['statistics']['emotion'] = json.load(f)
        
        # 保存报告
        with open('analysis_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("分析报告生成成功！")
        print(f"总爬取唐诗: {len(tang_data)}首")
        print(f"总爬取宋词: {len(song_data)}首")
        print(f"报告已保存到: analysis_report.json")
        
        return True
        
    except Exception as e:
        print(f"生成报告时出错: {e}")
        return False

def main():
    """主函数"""
    print("===== 古诗文爬取与分析系统 =====\n")
    
    # 1. 检查依赖
    if not check_dependencies():
        print("依赖检查失败，程序终止。")
        return
    
    # 2. 爬取唐诗
    if not os.path.exists('tang_poems.json'):
        if not run_script('crawl_tang_poetry.py', '爬取唐诗'):
            print("唐诗爬取失败，程序终止。")
            return
    else:
        print("唐诗数据文件已存在，跳过爬取步骤。")
    
    # 3. 爬取宋词
    if not os.path.exists('song_poems.json'):
        if not run_script('crawl_song_poetry.py', '爬取宋词'):
            print("宋词爬取失败，程序终止。")
            return
    else:
        print("宋词数据文件已存在，跳过爬取步骤。")
    
    # 4. 验证爬取的数据
    print("\n===== 验证爬取的数据 =====")
    if not validate_data('tang_poems.json', 100):
        print("唐诗数据验证失败，请重新爬取。")
    
    if not validate_data('song_poems.json', 100):
        print("宋词数据验证失败，请重新爬取。")
    
    # 5. 分析意象
    if not os.path.exists('tang_poems_with_imagery.json') or not os.path.exists('song_poems_with_imagery.json'):
        if not run_script('analyze_imagery.py', '分析诗词意象'):
            print("意象分析失败，程序终止。")
            return
    else:
        print("意象分析结果已存在，跳过分析步骤。")
    
    # 6. 分析情感
    if not os.path.exists('tang_poems_with_emotion.json') or not os.path.exists('song_poems_with_emotion.json'):
        if not run_script('analyze_emotion.py', '分析诗词情感'):
            print("情感分析失败，程序终止。")
            return
    else:
        print("情感分析结果已存在，跳过分析步骤。")
    
    # 7. 验证分析结果
    print("\n===== 验证分析结果 =====")
    if os.path.exists('tang_poems_complete_analysis.json'):
        validate_analysis_results('tang_poems_complete_analysis.json')
    
    if os.path.exists('song_poems_complete_analysis.json'):
        validate_analysis_results('song_poems_complete_analysis.json')
    
    # 8. 生成最终报告
    generate_report()
    
    print("\n===== 任务完成 =====")
    print("所有功能已成功执行！")
    print("\n生成的文件列表:")
    important_files = [
        'tang_poems.json', 'song_poems.json',
        'tang_poems_complete_analysis.json', 'song_poems_complete_analysis.json',
        'analysis_report.json'
    ]
    
    for file in important_files:
        if os.path.exists(file):
            print(f"- {file}")
        else:
            print(f"- {file} [未生成]")

if __name__ == '__main__':
    main()