from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import logging
import uuid
from models.poetry_generator import PoetryGenerator
from models.image_generator import ImageGenerator
from history_database import history_db

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 初始化Flask应用
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 配置文件上传
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传文件夹和静态资源文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static/images', exist_ok=True)

# 初始化模型
try:
    poetry_generator = PoetryGenerator()
    image_generator = ImageGenerator()
    logger.info("模型初始化成功")
except Exception as e:
    logger.error(f"模型初始化失败: {str(e)}")
    poetry_generator = None
    image_generator = None

# 首页路由
@app.route('/')
def index():
    """首页路由"""
    logger.info('访问首页')
    return render_template('index.html')

# 生成诗词API
@app.route('/api/generate_poetry', methods=['POST'])
def generate_poetry():
    """生成诗词的API"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': '请求参数错误'}), 400
        
        modern_text = data['text'].strip()
        if not modern_text:
            logger.warning('未提供文本内容')
            return jsonify({'error': '请输入文字内容'}), 400
        
        if not poetry_generator:
            return jsonify({'error': '模型未初始化'}), 500
            
        logger.info(f'接收到诗词生成请求: {modern_text[:50]}...')
        # 生成诗词
        poetry_result = poetry_generator.generate(modern_text)
        
        # 解析结果
        result = parse_poetry_result(poetry_result)
        logger.info(f'诗词生成成功，标题: {result["title"]}')
        
        return jsonify(result)
    except Exception as e:
        logger.error(f'诗词生成失败: {str(e)}')
        return jsonify({'error': f'生成诗词时出错: {str(e)}'}), 500

# 生成图片API
@app.route('/api/generate_image', methods=['POST'])
def generate_image():
    """生成图片的API"""
    try:
        data = request.get_json()
        if not data or 'poetry' not in data:
            return jsonify({'error': '请求参数错误'}), 400
        
        poetry = data['poetry']
        if not poetry_generator:
            return jsonify({'error': '模型未初始化'}), 500
            
        # 处理传入的诗词数据
        if isinstance(poetry, dict):
            # 构造完整诗词文本
            full_poetry = f"《{poetry.get('title', '')}》\n{poetry.get('content', '')}"
            if poetry.get('comment', ''):
                full_poetry += f"\n{poetry['comment']}"
        else:
            full_poetry = str(poetry)
        
        logger.info(f'接收到图片生成请求，诗词: {full_poetry[:50]}...')
        
        try:
            # 生成图片
            image_filename = image_generator.generate(full_poetry)
            
            if image_filename:
                logger.info(f'图片生成成功，文件名: {image_filename}')
                
                # 保存到历史记录
                try:
                    user_input = data.get('user_input', '')
                    history_db.save_history(
                        user_input=user_input,
                        poetry_title=poetry.get('title', '') if isinstance(poetry, dict) else '',
                        poetry_content=poetry.get('content', '') if isinstance(poetry, dict) else poetry,
                        poetry_comment=poetry.get('comment', '') if isinstance(poetry, dict) else '',
                        image_path=f'/uploads/{image_filename}'
                    )
                    logger.info('历史记录保存成功')
                except Exception as hist_error:
                    logger.error(f'保存历史记录失败: {str(hist_error)}')
            
                return jsonify({
                    'image_url': f'/uploads/{image_filename}'
                })
        except Exception as img_error:
            logger.error(f'图片生成过程中出错: {str(img_error)}')
            # 尝试创建默认图片
            try:
                default_image = create_default_image()
                if default_image:
                    filename = f"default_{uuid.uuid4().hex}.jpg"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    default_image.save(filepath)
                    logger.info(f'创建默认图片成功: {filename}')
                    return jsonify({
                        'image_url': f"/uploads/{filename}",
                        'warning': '由于某些原因，使用了默认图片'
                    })
                return jsonify({'error': '图片生成失败'}), 500
            except Exception as default_error:
                logger.error(f'创建默认图片失败: {str(default_error)}')
                return jsonify({'error': '图片生成失败'}), 500
            
    except Exception as e:
        logger.error(f'图片生成请求处理失败: {str(e)}')
        return jsonify({'error': f'生成图片时出错: {str(e)}'}), 500

# 提供上传文件的访问
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """访问上传的文件"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/static/<path:filename>')
def static_file(filename):
    """访问静态文件"""
    return send_from_directory('static', filename)

# 获取历史记录列表API
@app.route('/api/history', methods=['GET'])
def get_history():
    """获取历史记录列表"""
    try:
        # 获取分页参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 50:
            page_size = 10
        
        # 获取历史记录
        offset = (page - 1) * page_size
        records = history_db.get_history(limit=page_size, offset=offset)
        total = history_db.get_total_count()
        
        # 转换为前端友好的格式
        result = {
            'records': records,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        }
        
        return jsonify(result)
    except Exception as e:
        logger.error(f'获取历史记录失败: {str(e)}')
        return jsonify({'error': f'获取历史记录失败: {str(e)}'}), 500

# 获取单条历史记录API
@app.route('/api/history/<int:record_id>', methods=['GET'])
def get_history_record(record_id):
    """获取单条历史记录"""
    try:
        record = history_db.get_history_by_id(record_id)
        if record:
            return jsonify(record)
        else:
            return jsonify({'error': '记录不存在'}), 404
    except Exception as e:
        logger.error(f'获取历史记录失败: {str(e)}')
        return jsonify({'error': f'获取历史记录失败: {str(e)}'}), 500

# 保存诗词API
@app.route('/api/save_poetry', methods=['POST'])
def save_poetry():
    """保存诗词的API"""
    try:
        data = request.get_json()
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': '请求参数错误'}), 400
        
        # 提取诗词数据
        poetry_title = data['title'].strip()
        poetry_content = data['content'].strip()
        poetry_comment = data.get('comment', '').strip()
        user_input = data.get('user_input', '')
        
        # 为没有图片的诗词提供默认图片路径
        default_image_path = '/static/images/default_image.jpg'
        
        # 保存到数据库
        history_id = history_db.save_history(
            user_input=user_input,
            poetry_title=poetry_title,
            poetry_content=poetry_content,
            poetry_comment=poetry_comment,
            image_path=default_image_path
        )
        
        logger.info(f'诗词保存成功，标题: {poetry_title}，ID: {history_id}')
        return jsonify({
            'success': True,
            'message': '诗词保存成功',
            'id': history_id
        })
    except Exception as e:
        logger.error(f'保存诗词失败: {str(e)}')
        return jsonify({'error': f'保存诗词时出错: {str(e)}'}), 500

# 删除历史记录API
@app.route('/api/history/<int:record_id>', methods=['DELETE'])
def delete_history_record(record_id):
    """删除历史记录"""
    try:
        # 获取记录以获取图片路径
        record = history_db.get_record_by_id(record_id)
        if not record:
            return jsonify({'error': '记录不存在'}), 404
        
        # 删除数据库记录
        success = history_db.delete_record(record_id)
        if success:
            # 删除对应的图片文件
            if 'image_path' in record and record['image_path']:
                image_file = record['image_path'].replace('/uploads/', '')
                image_full_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file)
                if os.path.exists(image_full_path):
                    try:
                        os.remove(image_full_path)
                        logger.info(f'删除图片文件成功: {image_full_path}')
                    except Exception as img_error:
                        logger.error(f'删除图片文件失败: {str(img_error)}')
            
            return jsonify({'message': '删除成功'})
        else:
            return jsonify({'error': '删除失败'}), 500
    except Exception as e:
        logger.error(f'删除历史记录失败: {str(e)}')
        return jsonify({'error': f'删除历史记录失败: {str(e)}'}), 500

# 注意：诗词卡片生成功能已移除，只保留意境图生成功能

def parse_poetry_result(poetry_text):
    """
    解析诗词生成结果，提取标题、正文和注释
    """
    lines = poetry_text.strip().split('\n')
    result = {
        'title': '',
        'content': '',
        'comment': ''
    }
    
    # 提取标题
    if lines and lines[0].startswith('《') and '》' in lines[0]:
        result['title'] = lines[0].strip()
        content_lines = lines[1:]
    else:
        # 如果没有标准标题格式，尝试查找第一行作为标题
        if lines:
            result['title'] = f'《{lines[0]}》'
            content_lines = lines[1:]
        else:
            content_lines = []
    
    # 查找注释位置
    note_index = -1
    for i, line in enumerate(content_lines):
        if line.startswith('【注释】') or line.startswith('注释：'):
            note_index = i
            break
    
    # 提取正文和注释
    if note_index >= 0:
        result['content'] = '\n'.join(content_lines[:note_index]).strip()
        result['comment'] = content_lines[note_index].replace('【注释】', '').replace('注释：', '').strip()
    else:
        result['content'] = '\n'.join(content_lines).strip()
    
    # 如果标题还是空的，设置默认标题
    if not result['title'] or result['title'] == '《》':
        result['title'] = '《无名》'
    
    result['full_text'] = poetry_text
    return result

# 创建默认图片
from PIL import Image, ImageDraw, ImageFont
def create_default_image():
    """创建默认图片"""
    try:
        # 创建一个简单的水墨画风格图片
        img = Image.new('RGB', (1024, 768), color='#f5f5f5')
        draw = ImageDraw.Draw(img)
        
        # 添加简单的水墨效果 - 山水轮廓
        draw.ellipse([(200, 400), (800, 700)], fill='#e0e0e0')
        draw.ellipse([(300, 500), (700, 650)], fill='#d0d0d0')
        
        # 添加简单的水墨风格文字
        try:
            # 尝试使用系统字体
            font_path = "C:\\Windows\\Fonts\\simhei.ttf"  # Windows系统字体
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 36)
                draw.text((512, 384), "水墨意境", font=font, fill='#333333', anchor='mm')
            else:
                # 尝试其他可能的字体路径
                try:
                    font = ImageFont.truetype("simhei.ttf", 36)
                    draw.text((512, 384), "水墨意境", font=font, fill='#333333', anchor='mm')
                except:
                    draw.text((512, 384), "水墨意境", fill='#333333')
        except Exception as e:
            logger.warning(f"无法加载字体: {str(e)}")
            draw.text((512, 384), "水墨意境", fill='#333333')
        
        # 保存图片到static/images目录
        default_image_path = os.path.join('static', 'images', 'default_image.jpg')
        img.save(default_image_path)
        logger.info('已创建并保存默认图片')
        return img
    except Exception as e:
        logger.error(f'创建默认图片失败: {str(e)}')
        return None

if __name__ == '__main__':
    # 创建默认图片
    create_default_image()
    
    # 启动Flask应用
    logger.info('启动Flask应用，端口5000')
    app.run(debug=True, port=5000, host='0.0.0.0')
