
# 简化版image_card_generator.py（仅修复字体问题）
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
        """查找合适的字体文件，支持Windows和Linux系统"""
        # Windows系统字体路径
        windows_font_paths = [
            os.path.join('C:\Windows\Fonts', f'{font_name}.ttf'),
            os.path.join('C:\Windows\Fonts', f'{font_name}.ttc'),
        ]
        
        # Linux系统字体路径
        linux_font_paths = [
            os.path.join('/usr/share/fonts', f'{font_name}.ttf'),
            os.path.join('/usr/share/fonts/truetype', f'{font_name}.ttf'),
            os.path.join('/usr/share/fonts/truetype/dejavu', 'DejaVuSans.ttf'),
            os.path.join('/usr/share/fonts/truetype/noto', 'NotoSansCJK.ttc'),
            os.path.join('/usr/share/fonts/truetype/noto-cjk', 'NotoSansCJK.ttc'),
            os.path.join('/usr/share/fonts/truetype/wqy', 'wqy-microhei.ttc'),
        ]
        
        # 检查Windows字体
        for path in windows_font_paths:
            if os.path.exists(path):
                return path
        
        # 检查Linux字体
        for path in linux_font_paths:
            if os.path.exists(path):
                return path
        
        # 尝试其他常见字体
        common_fonts = ['simhei', 'simsun', 'microsoft yahei', 'simkai', 'dejavu sans', 'noto sans']
        for font in common_fonts:
            # Windows路径
            for ext in ['.ttf', '.ttc']:
                path = os.path.join('C:\Windows\Fonts', font + ext)
                if os.path.exists(path):
                    return path
            # Linux路径变体
            font_lower = font.replace(' ', '')
            for ext in ['.ttf', '.ttc']:
                linux_paths = [
                    os.path.join('/usr/share/fonts/truetype', font_lower + ext),
                    os.path.join('/usr/share/fonts', font_lower + ext),
                ]
                for linux_path in linux_paths:
                    if os.path.exists(linux_path):
                        return linux_path
        
        # 如果找不到任何字体，返回None，让PIL使用默认字体
        logger.warning('未找到合适的字体文件，将使用PIL默认字体')
        return None
    
    # 其余方法保持不变...
