import requests
import time
import json
import os
import uuid
from PIL import Image
from io import BytesIO

class ImageGenerator:
    def __init__(self):
        self.base_url = 'https://api-inference.modelscope.cn/'
        self.api_key = "ms-fc15f851-c877-4691-b208-e6bbd8d13e25"  # ModelScope Token
        self.common_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.upload_folder = 'uploads'
        
        # 确保上传文件夹存在
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
    
    def generate_prompt(self, poetry_text):
        """
        根据诗词内容生成适合文生图的提示词
        参数:
            poetry_text: 诗词内容
        返回:
            适合文生图的提示词
        """
        # 分析诗词中的主要意象
        imagery_keywords = []
        scene_elements = []
        mood_elements = []
        
        # 常见诗词意象及其英文对应（更全面的映射）
        imagery_mapping = {
            # 自然景观
            '山': 'mountain', '峰': 'peak', '岭': 'ridge', '峦': 'mountain range',
            '水': 'water', '江': 'river', '湖': 'lake', '海': 'sea', '河': 'river',
            '溪': 'stream', '泉': 'spring', '瀑': 'waterfall', '潭': 'pond',
            '月': 'moon', '明': 'bright moon', '日': 'sun', '阳': 'sun',
            '云': 'cloud', '霞': 'sunset glow', '雾': 'mist', '烟': 'smoke',
            '风': 'wind', '雨': 'rain', '雪': 'snow', '霜': 'frost',
            
            # 季节与植物
            '春': 'spring', '夏': 'summer', '秋': 'autumn', '冬': 'winter',
            '花': 'flower', '草': 'grass', '树': 'tree', '林': 'forest',
            '松': 'pine tree', '竹': 'bamboo', '柳': 'willow', '梅': 'plum blossom',
            '菊': 'chrysanthemum', '荷': 'lotus', '桃': 'peach blossom', '梨': 'pear blossom',
            '桂': 'osmanthus', '兰': 'orchid',
            
            # 动物
            '鸟': 'bird', '雁': 'wild goose', '鹤': 'crane', '鹭': 'heron',
            '鱼': 'fish', '马': 'horse', '猿': 'monkey', '鹿': 'deer',
            
            # 人造景观
            '舟': 'boat', '桥': 'bridge', '亭': 'pavilion', '阁': 'pavilion',
            '寺': 'temple', '庙': 'temple', '楼': 'tower', '台': 'platform',
            '院': 'courtyard', '园': 'garden', '门': 'gate', '窗': 'window',
            
            # 人物与物品
            '人': 'person', '客': 'traveler', '僧': 'monk', '隐者': 'hermit',
            '酒': 'wine', '剑': 'sword', '琴': 'guqin', '书': 'book',
            '棋': 'chess', '笔': 'brush', '墨': 'ink', '纸': 'paper',
            '茶': 'tea', '灯': 'lantern',
            
            # 情感相关词汇
            '愁': 'sorrow', '思': 'longing', '忆': 'memory', '念': 'missing',
            '归': 'returning', '别': 'parting', '望': 'looking', '盼': 'hoping',
            '静': 'tranquil', '闲': 'leisurely', '幽': 'secluded', '远': 'distant',
            '孤': 'lonely', '独': 'alone', '寂': 'silent', '寞': 'lonely'
        }
        
        # 季节特征词汇
        season_markers = {
            '春': ['桃', '梨', '柳', '燕', '绿'],
            '夏': ['荷', '蝉', '热', '浓', '茂'],
            '秋': ['菊', '枫', '落', '黄', '凉'],
            '冬': ['梅', '雪', '寒', '冰', '霜']
        }
        
        # 情感氛围词汇
        mood_markers = {
            '宁静': ['静', '闲', '幽', '寂', '寞'],
            '忧伤': ['愁', '思', '忆', '念', '别'],
            '壮阔': ['山', '海', '江', '河', '峰'],
            '悠远': ['远', '望', '归', '云', '霞'],
            '闲适': ['茶', '酒', '棋', '书', '琴']
        }
        
        # 提取意象关键词
        for chinese, english in imagery_mapping.items():
            if chinese in poetry_text:
                imagery_keywords.append(english)
                
                # 检查是否为场景元素
                if chinese in ['山', '水', '江', '湖', '海', '河', '溪', '泉', '瀑', '潭',
                              '月', '日', '云', '雾', '烟', '风', '雨', '雪',
                              '春', '夏', '秋', '冬', '花', '草', '树', '林',
                              '松', '竹', '柳', '梅', '菊', '荷']:
                    scene_elements.append(english)
        
        # 确定季节
        season = None
        for s, markers in season_markers.items():
            if any(m in poetry_text for m in markers):
                season = s
                break
        
        # 确定情感氛围
        mood = None
        for m, markers in mood_markers.items():
            if any(mm in poetry_text for mm in markers):
                mood = m
                break
        
        # 构建基础提示词
        base_prompt = "traditional Chinese ink painting, ink wash style, "
        
        # 添加季节描述
        if season:
            season_vocab = {
                '春': 'spring landscape, soft green tones, blooming flowers',
                '夏': 'summer scenery, lush vegetation, vibrant greens',
                '秋': 'autumn scene, golden leaves, clear sky',
                '冬': 'winter landscape, snow-covered, serene'
            }
            base_prompt += season_vocab[season] + ", "
        
        # 添加场景元素
        if scene_elements:
            scene_desc = ", ".join(list(set(scene_elements)))  # 去重
            base_prompt += f"featuring {scene_desc}, "
        
        # 添加情感氛围
        if mood:
            mood_vocab = {
                '宁静': 'serene, peaceful atmosphere, minimalist',
                '忧伤': 'melancholic mood, misty, subtle colors',
                '壮阔': 'grand scenery, vast perspective, majestic',
                '悠远': 'distant view, hazy mountains, contemplative',
                '闲适': 'leisurely scene, simple life, elegant'
            }
            base_prompt += mood_vocab[mood] + ", "
        
        # 添加艺术风格描述
        base_prompt += "elegant brush strokes, minimalist composition, poetic atmosphere, high detail, masterpiece, traditional Chinese aesthetics"
        
        return base_prompt
    
    def generate(self, poetry_text, max_task_retries=3, max_polling_retries=40):
        """
        根据诗词生成图片
        参数:
            poetry_text: 诗词内容
            max_task_retries: 任务创建最大重试次数
            max_polling_retries: 状态轮询最大重试次数
        返回:
            保存的图片文件名
        """
        task_retry_count = 0
        
        while task_retry_count <= max_task_retries:
            try:
                # 生成提示词
                prompt = self.generate_prompt(poetry_text)
                print(f"生成的提示词: {prompt}")
                
                # 发起异步图片生成请求
                response = requests.post(
                    f"{self.base_url}v1/images/generations",
                    headers={**self.common_headers, "X-ModelScope-Async-Mode": "true"},
                    data=json.dumps({
                        "model": "Qwen/Qwen-Image",
                        "prompt": prompt,
                        "width": 1024,  # 设置合适的图片尺寸
                        "height": 768,
                        "steps": 50,    # 增加生成步骤以提高质量
                        "guidance_scale": 7.5  # 控制提示词的影响力
                    }, ensure_ascii=False).encode('utf-8')
                )
                
                response.raise_for_status()
                task_data = response.json()
                
                # 检查任务ID是否存在
                if "task_id" not in task_data:
                    raise Exception(f"任务创建失败，响应中没有task_id: {task_data}")
                
                task_id = task_data["task_id"]
                print(f"图片生成任务ID: {task_id}")
                
                # 轮询任务状态
                polling_retry_count = 0
                
                while polling_retry_count < max_polling_retries:
                    try:
                        result = requests.get(
                            f"{self.base_url}v1/tasks/{task_id}",
                            headers={**self.common_headers, "X-ModelScope-Task-Type": "image_generation"},
                            timeout=30  # 设置超时时间
                        )
                        
                        result.raise_for_status()
                        data = result.json()
                        
                        # 检查响应状态
                        if data["task_status"] == "SUCCEED":
                            # 获取图片
                            if "output_images" not in data or not data["output_images"]:
                                raise Exception("任务成功但未返回图片URL")
                            
                            image_url = data["output_images"][0]
                            print(f"图片生成成功，URL: {image_url}")
                            
                            # 获取图片内容
                            image_response = requests.get(image_url, timeout=60)
                            image_response.raise_for_status()
                            
                            # 保存图片
                            try:
                                image = Image.open(BytesIO(image_response.content))
                                unique_filename = f"poetry_image_{uuid.uuid4().hex[:8]}.jpg"
                                image_path = os.path.join(self.upload_folder, unique_filename)
                                
                                # 确保图片质量
                                image.save(image_path, 'JPEG', quality=95)
                                print(f"图片已保存: {image_path}")
                                return unique_filename
                            except Exception as img_error:
                                print(f"处理图片时出错: {img_error}")
                                raise Exception(f"图片处理失败: {str(img_error)}")
                                
                        elif data["task_status"] == "FAILED":
                            error_msg = data.get("error_msg", "图片生成失败")
                            raise Exception(f"图片生成失败: {error_msg}")
                        elif data["task_status"] == "CANCELLED":
                            raise Exception("图片生成任务已取消")
                        
                        # 等待后重试，使用指数退避策略
                        wait_time = min(2 + (polling_retry_count * 0.5), 15)  # 最大等待15秒
                        print(f"任务状态: {data['task_status']}，等待{wait_time:.1f}秒后重试...")
                        time.sleep(wait_time)
                        polling_retry_count += 1
                        
                    except requests.Timeout:
                        print("请求超时，重试...")
                        polling_retry_count += 1
                        time.sleep(5)
                    except Exception as poll_error:
                        print(f"轮询任务状态时出错: {poll_error}")
                        raise
                
                raise Exception("图片生成超时")
                
            except Exception as e:
                task_retry_count += 1
                error_msg = str(e)
                print(f"生成图片时出错: {error_msg}，第{task_retry_count}次重试...")
                
                # 如果是特定错误类型，可能不需要重试
                if "invalid api key" in error_msg.lower() or "authentication failed" in error_msg.lower():
                    print("API密钥无效，停止重试")
                    break
                
                if task_retry_count <= max_task_retries:
                    print("等待3秒后重试...")
                    time.sleep(3)
        
        # 所有重试都失败，返回默认图片
        print("所有重试都失败，返回默认图片")
        return self._get_default_image()
    
    def _get_default_image(self):
        """
        获取或创建默认图片
        返回:
            默认图片文件名
        """
        default_image = "default_poetry_image.jpg"
        default_path = os.path.join(self.upload_folder, default_image)
        
        if not os.path.exists(default_path):
            try:
                # 创建一个简单的默认水墨画风格图片
                from PIL import ImageDraw
                img = Image.new('RGB', (1024, 768), color='white')
                draw = ImageDraw.Draw(img)
                
                # 绘制简单的山水轮廓
                draw.rectangle([(0, 500), (1024, 768)], fill='#E8E8E8')  # 底色
                
                # 简单的山轮廓
                draw.polygon([(0, 500), (512, 200), (1024, 500)], fill='#CCCCCC')
                
                # 简单的水波纹
                for i in range(5):
                    y = 550 + i * 30
                    draw.line([(0, y), (1024, y)], fill='#AAAAAA', width=1)
                
                img.save(default_path, 'JPEG', quality=85)
                print(f"已创建默认图片: {default_path}")
            except Exception as e:
                print(f"创建默认图片失败: {e}")
        
        return default_image

# 测试代码（可选）
if __name__ == "__main__":
    generator = ImageGenerator()
    test_poetry = "《山居秋暝》\n空山新雨后，天气晚来秋。\n明月松间照，清泉石上流。\n竹喧归浣女，莲动下渔舟。\n随意春芳歇，王孙自可留。"
    image_file = generator.generate(test_poetry)
    print(f"生成的图片保存在: {image_file}")
