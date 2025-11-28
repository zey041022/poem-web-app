from openai import OpenAI
import time
import re

class PoetryGenerator:
    def __init__(self):
        # 初始化OpenAI客户端，连接到ModelScope API
        self.client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1',
            api_key='ms-fc15f851-c877-4691-b208-e6bbd8d13e25',  # ModelScope Token
        )
        
        # 系统提示词
        self.system_prompt = """
        你是一位才华横溢且精通中国古典诗词的AI诗人。你的任务是根据用户提供的现代汉语描述，创作一首符合古典诗词格律和意境的诗或词。
        【要求】
        1. 深刻理解用户描述的**核心情感与场景**。
        2. 严格按照指定体裁（如无指定，则随机选择唐诗或宋词风格）的格律创作，注意平仄、对仗和押韵。
        3. 灵活运用古典意象（如明月、杨柳、孤舟、浊酒等）来表达情感，避免使用现代词汇。
        4. 输出格式为纯文本，第一行为诗/词标题，第二行开始为正文，最后以"【注释】"开头，用现代文简要解释诗的意境。
        【示例】
        用户输入：今天好累，不想上班。
        输出：
        《倦勤》
        朝霞未染已披衣，案牍劳形力渐微。
        愿化闲云归野壑，不随车马逐尘飞。
        【注释】此诗以朝霞未出便已起床的辛劳开篇，描绘了公务繁忙、身心疲惫的状态。后两句直抒胸臆，表达了渴望摆脱俗务、归隐自然的闲适愿望。
        """
    
    def generate(self, modern_text, max_retries=3):
        """
        根据现代文生成古诗词
        参数:
            modern_text: 用户输入的现代文
            max_retries: 最大重试次数
        返回:
            生成的古诗词文本
        """
        retry_count = 0
        last_error = None
        
        while retry_count <= max_retries:
            try:
                # 构建消息
                messages = [
                    {
                        'role': 'system',
                        'content': self.system_prompt
                    },
                    {
                        'role': 'user',
                        'content': modern_text
                    }
                ]
                
                # 调用模型
                response = self.client.chat.completions.create(
                    model='deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
                    messages=messages,
                    stream=True,
                    temperature=0.7,  # 控制生成多样性
                    max_tokens=1024  # 设置最大生成长度
                )
                
                # 处理流式响应
                full_response = ""
                reasoning_content = ""
                
                for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                    elif chunk.choices and hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
                        reasoning_content += chunk.choices[0].delta.reasoning_content
                
                # 验证生成结果格式
                if self._validate_poetry_format(full_response):
                    return full_response
                else:
                    # 格式不正确，尝试修正
                    corrected_response = self._correct_poetry_format(full_response)
                    if self._validate_poetry_format(corrected_response):
                        return corrected_response
                    
                    # 如果修正后仍不正确，重试
                    retry_count += 1
                    last_error = "生成的诗词格式不正确"
                    if retry_count <= max_retries:
                        print(f"重试生成诗词，第{retry_count}次...")
                        time.sleep(1)  # 等待1秒后重试
                    continue
                    
            except Exception as e:
                retry_count += 1
                last_error = str(e)
                print(f"生成诗词时出错: {e}，第{retry_count}次重试...")
                if retry_count <= max_retries:
                    time.sleep(2)  # 等待2秒后重试
        
        # 所有重试都失败
        print(f"所有重试都失败，最后错误: {last_error}")
        return f"《生成失败》\n生成诗词时遇到问题，请稍后重试。\n【注释】{last_error}，请检查网络连接或稍后再试。"
    
    def _validate_poetry_format(self, text):
        """
        验证诗词格式是否正确
        参数:
            text: 生成的诗词文本
        返回:
            是否格式正确
        """
        # 检查是否包含标题、正文和注释
        has_title = '《' in text and '》' in text
        has_comment = '【注释】' in text
        
        # 检查正文部分是否存在
        title_match = re.search(r'《.*?》', text)
        if title_match:
            title_end = title_match.end()
            comment_match = text.find('【注释】', title_end)
            has_content = comment_match > title_end
        else:
            has_content = False
        
        return has_title and has_content and has_comment
    
    def _correct_poetry_format(self, text):
        """
        尝试修正诗词格式
        参数:
            text: 生成的诗词文本
        返回:
            修正后的诗词文本
        """
        # 如果没有标题，添加默认标题
        if '《' not in text or '》' not in text:
            text = "《无题》\n" + text
        
        # 如果没有注释，添加默认注释
        if '【注释】' not in text:
            text += "\n【注释】根据您的描述生成的诗词。"
        
        return text

# 测试代码（可选）
if __name__ == "__main__":
    generator = PoetryGenerator()
    result = generator.generate("今天天气真好，阳光明媚，心情也跟着开朗起来")
    print(result)
