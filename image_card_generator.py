# 注意：此模块已不再被使用
# 由于需求变更，诗词卡片生成功能已被移除，只保留意境图生成功能

# 为了向后兼容性，保留此文件但不再导入使用
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import logging
import uuid

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageCardGenerator:
    """诗词卡片生成器，用于将诗词与图片合成精美卡片"""
    
    def __init__(self):
        self.card_width = 1080
        self.card_height = 1350
        self.padding = 60
        self.font_size_title = 36
        self.font_size_content = 28
        self.font_size_comment = 24
        self.line_spacing = 1.5
        self.border_width = 10
        self.border_color = '#ffffff'
        
    def find_font(self, font_name='simhei'):
        """查找合适的字体文件"""
        # Windows系统字体路径
        windows_font_paths = [
            os.path.join('C:\Windows\Fonts', f'{font_name}.ttf'),
            os.path.join('C:\Windows\Fonts', f'{font_name}.ttc'),
        ]
        
        # 检查Windows字体
        for path in windows_font_paths:
            if os.path.exists(path):
                return path
        
        # 尝试其他常见字体
        common_fonts = ['simhei', 'simsun', 'microsoft yahei', 'simkai']
        for font in common_fonts:
            for ext in ['.ttf', '.ttc']:
                path = os.path.join('C:\Windows\Fonts', font + ext)
                if os.path.exists(path):
                    return path
        
        return None
    
    def generate_card(self, image_path, poetry_title, poetry_content, poetry_comment='', output_folder='uploads'):
        """
        生成诗词卡片
        
        Args:
            image_path: 原始图片路径（相对于应用根目录）
            poetry_title: 诗词标题
            poetry_content: 诗词内容
            poetry_comment: 诗词注释（可选）
            output_folder: 输出文件夹
            
        Returns:
            生成的卡片图片文件名
        """
        try:
            # 确保输出文件夹存在
            os.makedirs(output_folder, exist_ok=True)
            
            # 打开原始图片
            full_image_path = os.path.join(os.getcwd(), image_path.lstrip('/'))
            if not os.path.exists(full_image_path):
                logger.error(f'图片文件不存在: {full_image_path}')
                return None
            
            original_img = Image.open(full_image_path).convert('RGB')
            
            # 创建卡片背景
            card = Image.new('RGB', (self.card_width, self.card_height), color='#f5f5f5')
            draw = ImageDraw.Draw(card)
            
            # 计算图片区域
            img_width = self.card_width - 2 * self.padding
            img_height = int(img_width * 0.75)  # 4:3比例
            img_y = self.padding
            
            # 调整原始图片大小并居中
            original_img = self.resize_and_crop(original_img, img_width, img_height)
            card.paste(original_img, (self.padding, img_y))
            
            # 添加装饰边框
            draw.rectangle([(self.padding - self.border_width, img_y - self.border_width),
                           (self.card_width - self.padding + self.border_width,
                            img_y + img_height + self.border_width)],
                          outline=self.border_color, width=self.border_width)
            
            # 获取字体
            font_path = self.find_font()
            
            # 绘制诗词标题
            if poetry_title:
                title_y = img_y + img_height + self.padding
                if font_path:
                    try:
                        font = ImageFont.truetype(font_path, self.font_size_title)
                        draw.text((self.card_width // 2, title_y), poetry_title,
                                 font=font, fill='#333333', anchor='mt', align='center')
                    except Exception as e:
                        logger.warning(f'使用字体失败，使用默认字体: {str(e)}')
                        draw.text((self.card_width // 2, title_y), poetry_title,
                                 fill='#333333', anchor='mt', align='center')
                else:
                    draw.text((self.card_width // 2, title_y), poetry_title,
                             fill='#333333', anchor='mt', align='center')
                
                content_y = title_y + self.font_size_title * 1.5
            else:
                content_y = img_y + img_height + self.padding
            
            # 绘制诗词内容（支持多行）
            if poetry_content:
                if font_path:
                    try:
                        content_font = ImageFont.truetype(font_path, self.font_size_content)
                    except:
                        content_font = None
                else:
                    content_font = None
                
                lines = poetry_content.split('\n')
                for line in lines:
                    if content_font:
                        draw.text((self.card_width // 2, content_y), line,
                                 font=content_font, fill='#333333', anchor='mt', align='center')
                    else:
                        draw.text((self.card_width // 2, content_y), line,
                                 fill='#333333', anchor='mt', align='center')
                    content_y += int(self.font_size_content * self.line_spacing)
            
            # 绘制诗词注释
            if poetry_comment:
                # 添加注释前的分隔线
                line_y = content_y + self.padding // 2
                draw.line([(self.padding * 2, line_y),
                           (self.card_width - self.padding * 2, line_y)],
                          fill='#999999', width=1)
                
                comment_y = line_y + self.padding // 2
                if font_path:
                    try:
                        comment_font = ImageFont.truetype(font_path, self.font_size_comment)
                    except:
                        comment_font = None
                else:
                    comment_font = None
                
                # 注释内容
                if comment_font:
                    draw.text((self.card_width // 2, comment_y), f'注释：{poetry_comment}',
                             font=comment_font, fill='#666666', anchor='mt', align='center')
                else:
                    draw.text((self.card_width // 2, comment_y), f'注释：{poetry_comment}',
                             fill='#666666', anchor='mt', align='center')
            
            # 添加水印或装饰元素
            self.add_decoration(card, draw)
            
            # 保存生成的卡片
            output_filename = f'card_{uuid.uuid4().hex}.jpg'
            output_path = os.path.join(output_folder, output_filename)
            card.save(output_path, quality=95)
            
            logger.info(f'诗词卡片生成成功: {output_filename}')
            return output_filename
            
        except Exception as e:
            logger.error(f'生成诗词卡片失败: {str(e)}')
            return None
    
    def resize_and_crop(self, image, target_width, target_height):
        """调整图片大小并裁剪以适应目标尺寸"""
        # 计算缩放比例
        img_ratio = image.width / image.height
        target_ratio = target_width / target_height
        
        # 根据比例调整图片大小
        if img_ratio > target_ratio:
            # 图片更宽，按高度缩放
            new_height = target_height
            new_width = int(new_height * img_ratio)
            resized = image.resize((new_width, new_height), Image.LANCZOS)
            # 裁剪宽度
            left = (new_width - target_width) // 2
            right = left + target_width
            return resized.crop((left, 0, right, target_height))
        else:
            # 图片更高或等比例，按宽度缩放
            new_width = target_width
            new_height = int(new_width / img_ratio)
            resized = image.resize((new_width, new_height), Image.LANCZOS)
            # 裁剪高度
            top = (new_height - target_height) // 2
            bottom = top + target_height
            return resized.crop((0, top, target_width, bottom))
    
    def add_decoration(self, card, draw):
        """添加装饰元素"""
        # 添加角落装饰
        corner_size = 30
        corner_width = 2
        color = '#999999'
        
        # 左上角
        draw.line([(self.padding, self.padding),
                   (self.padding + corner_size, self.padding)],
                  fill=color, width=corner_width)
        draw.line([(self.padding, self.padding),
                   (self.padding, self.padding + corner_size)],
                  fill=color, width=corner_width)
        
        # 右上角
        draw.line([(self.card_width - self.padding, self.padding),
                   (self.card_width - self.padding - corner_size, self.padding)],
                  fill=color, width=corner_width)
        draw.line([(self.card_width - self.padding, self.padding),
                   (self.card_width - self.padding, self.padding + corner_size)],
                  fill=color, width=corner_width)
        
        # 左下角
        draw.line([(self.padding, self.card_height - self.padding),
                   (self.padding + corner_size, self.card_height - self.padding)],
                  fill=color, width=corner_width)
        draw.line([(self.padding, self.card_height - self.padding),
                   (self.padding, self.card_height - self.padding - corner_size)],
                  fill=color, width=corner_width)
        
        # 右下角
        draw.line([(self.card_width - self.padding, self.card_height - self.padding),
                   (self.card_width - self.padding - corner_size, self.card_height - self.padding)],
                  fill=color, width=corner_width)
        draw.line([(self.card_width - self.padding, self.card_height - self.padding),
                   (self.card_width - self.padding, self.card_height - self.padding - corner_size)],
                  fill=color, width=corner_width)

# 创建全局实例
card_generator = ImageCardGenerator()

# 测试函数（可选）
def test_card_generation():
    """测试卡片生成功能"""
    test_image = "uploads/default_test.jpg"
    if os.path.exists(test_image):
        result = card_generator.generate_card(
            test_image,
            "《测试标题》",
            "春眠不觉晓，处处闻啼鸟。\n夜来风雨声，花落知多少。",
            "这是一首测试注释"
        )
        print(f"测试结果: {result}")

if __name__ == "__main__":
    test_card_generation()