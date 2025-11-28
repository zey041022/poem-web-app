// 等待DOM加载完成
Document.prototype.ready = Document.prototype.ready || function(callback) {
    if (document.readyState !== 'loading') {
        callback();
    } else {
        document.addEventListener('DOMContentLoaded', callback);
    }
};

document.ready(function() {
    // 获取DOM元素
    const userInput = document.getElementById('userInput');
    const generateBtn = document.getElementById('generateBtn');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingStage = document.getElementById('loadingStage');
    const resultSection = document.getElementById('resultSection');
    const poetryTitle = document.getElementById('poetryTitle');
    const poetryContent = document.getElementById('poetryContent');
    const poetryNote = document.getElementById('poetryNote');
    const resultImage = document.getElementById('resultImage');
    const tryAgainBtn = document.getElementById('tryAgainBtn');
    const saveBtn = document.getElementById('saveBtn');
    const savePoetryBtn = document.getElementById('savePoetryBtn');
    
    // 存储当前生成的结果
    let currentGeneration = null;
    
    // 初始状态设置
    let isGenerating = false;
    
    // 初始化应用功能
    console.log('准备初始化应用功能...');
    initializeApp();
    console.log('应用功能初始化完成');
    
    // 加载动画阶段文本
    const stages = [
        '正在构思诗意...',
        '正在挥毫泼墨...',
        '正在渲染意境...',
        '作品即将完成...'
    ];
    
    // 更新加载动画阶段
    function updateLoadingStage(index) {
        if (index < stages.length) {
            loadingStage.textContent = stages[index];
        }
    }
    
    // 显示加载动画
    function showLoading() {
        loadingOverlay.classList.add('active');
        updateLoadingStage(0);
        
        // 模拟进度更新
        let currentStage = 0;
        const stageInterval = setInterval(() => {
            currentStage++;
            if (currentStage < stages.length) {
                updateLoadingStage(currentStage);
            } else {
                clearInterval(stageInterval);
            }
        }, 3000);
    }
    
    // 隐藏加载动画
    function hideLoading() {
        loadingOverlay.classList.remove('active');
    }
    
    // 显示结果
    function showResult(poetryData, imageUrl) {
        // 更新诗词内容
        poetryTitle.textContent = poetryData.title || '无名';
        poetryContent.textContent = poetryData.content || '';
        poetryNote.textContent = poetryData.comment || '';
        
        // 更新图片
        if (imageUrl) {
            resultImage.src = imageUrl;
            resultImage.alt = poetryData.title || '诗词意境图';
        }
        
        // 显示结果区域
        setTimeout(() => {
            resultSection.classList.add('visible');
        }, 100);
    }
    
    // 清空结果
    function clearResult() {
        resultSection.classList.remove('visible');
        poetryTitle.textContent = '';
        poetryContent.textContent = '';
        poetryNote.textContent = '';
        resultImage.src = '';
        resultImage.alt = '';
    }
    
    // 验证输入
    function validateInput() {
        const input = userInput.value.trim();
        if (!input) {
            alert('请输入您想要表达的内容');
            return false;
        }
        if (input.length > 500) {
            alert('输入内容过长，请控制在500字以内');
            return false;
        }
        return true;
    }
    
    // 生成诗词和图片
    async function generatePoetryAndImage() {
        if (!validateInput() || isGenerating) {
            return;
        }
        
        isGenerating = true;
        generateBtn.disabled = true;
        clearResult();
        showLoading();
        
        try {
            // 第一步：生成诗词
            updateLoadingStage(0);
            const poetryResponse = await fetch('/api/generate_poetry', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: userInput.value.trim()
                })
            });
            
            if (!poetryResponse.ok) {
                throw new Error('生成诗词失败');
            }
            
            const poetryData = await poetryResponse.json();
            console.log('生成的诗词:', poetryData);
            
            if (!poetryData.title || !poetryData.content) {
                throw new Error('诗词格式不正确');
            }
            
            // 更新加载状态
            updateLoadingStage(1);
            
            // 第二步：生成图片
            updateLoadingStage(2);
            const imageResponse = await fetch('/api/generate_image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    poetry: poetryData.content
                })
            });
            
            if (!imageResponse.ok) {
                throw new Error('生成图片失败');
            }
            
            const imageData = await imageResponse.json();
            console.log('生成的图片:', imageData);
            
            // 后端已经返回完整的URL路径
            let imageUrl = imageData.image_url || '';
            
            // 更新加载状态
            updateLoadingStage(3);
            
            // 第三步：将诗词题写在图片上
            try {
                updateLoadingStage(3);
                const cardResponse = await fetch('/api/generate_card', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        poetry_title: poetryData.title,
                        poetry_content: poetryData.content,
                        // 不传递注释参数，确保图片中只包含标题和正文
                        image_path: imageUrl
                    })
                });
                
                if (cardResponse.ok) {
                    const cardData = await cardResponse.json();
                    // 如果卡片生成成功，使用带有诗词的卡片图片
                    if (cardData.success && (cardData.card_url || cardData.url)) {
                        imageUrl = cardData.card_url || cardData.url || imageUrl;
                        console.log('诗词卡片生成成功:', imageUrl);
                    }
                }
            } catch (cardError) {
                console.log('生成诗词卡片时出错:', cardError);
                // 即使卡片生成失败，也继续使用原图
            }
            
            // 短暂延迟后显示结果
            setTimeout(() => {
                hideLoading();
                showResult(poetryData, imageUrl);
                isGenerating = false;
                generateBtn.disabled = false;
            }, 1000);
            
        } catch (error) {
            console.error('生成过程中出错:', error);
            hideLoading();
            alert('生成过程中出错: ' + error.message);
            isGenerating = false;
            generateBtn.disabled = false;
        }
    }
    
    // 保存诗词
    async function savePoetry() {
        // 检查是否有生成的诗词
        if (!poetryTitle.textContent || !poetryContent.textContent) {
            alert('没有可保存的诗词');
            return;
        }
        
        try {
            // 显示加载状态
            loadingOverlay.classList.add('active');
            loadingStage.textContent = '正在准备诗词...';
            
            // 构建请求数据
            const poetryData = {
                title: poetryTitle.textContent,
                content: poetryContent.textContent,
                comment: poetryNote.textContent,
                user_input: userInput.value.trim()
            };
            
            // 发送保存请求到后端数据库
            const response = await fetch('/api/save_poetry', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(poetryData)
            });
            
            const result = await response.json();
            
            // 隐藏加载状态
            loadingOverlay.classList.remove('active');
            
            if (result.success) {
                // 同时让用户选择本地保存路径
                // 创建诗词文本内容
                let poetryText = `${poetryData.title}\n\n${poetryData.content}`;
                if (poetryData.comment) {
                    poetryText += `\n\n【注释】${poetryData.comment}`;
                }
                
                // 创建Blob对象
                const blob = new Blob([poetryText], { type: 'text/plain;charset=utf-8' });
                
                // 创建下载链接
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                
                // 生成文件名（从标题中提取，去除特殊字符）
                let filename = poetryData.title.replace(/[《》]/g, '');
                filename = filename.replace(/[^\w\u4e00-\u9fa5]/g, '_') + '_' + new Date().getTime() + '.txt';
                link.download = filename;
                
                // 触发下载
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                // 释放URL对象
                URL.revokeObjectURL(link.href);
                
                alert('诗词已保存到数据库和本地文件！');
            } else {
                alert('保存失败: ' + (result.error || '未知错误'));
            }
        } catch (error) {
            console.error('保存诗词时出错:', error);
            loadingOverlay.classList.remove('active');
            alert('保存过程中出错: ' + error.message);
        }
    }
    
    // 保存图片
    function saveImage() {
        if (resultImage.src) {
            const link = document.createElement('a');
            link.href = resultImage.src;
            link.download = `poetry_image_${new Date().getTime()}.jpg`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            alert('没有可保存的图片');
        }
    }
    
    // 事件监听器
    generateBtn.addEventListener('click', generatePoetryAndImage);
    
    // 回车生成（Ctrl+Enter或Cmd+Enter）
    userInput.addEventListener('keydown', function(event) {
        if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
            generatePoetryAndImage();
        }
    });
    
    // 重新生成按钮
    tryAgainBtn.addEventListener('click', function() {
        clearResult();
        userInput.focus();
    });
    
    // 保存诗词按钮
    if (savePoetryBtn) {
        savePoetryBtn.addEventListener('click', savePoetry);
    }
    
    // 保存图片按钮
    saveBtn.addEventListener('click', saveImage);
    
    // 图片加载错误处理
    resultImage.addEventListener('error', function() {
        this.src = '/static/images/default_image.jpg';
        this.alt = '默认图片';
    });
    
    // 初始焦点
    userInput.focus();
    
    // 添加水墨动画效果
    function animateInkBrush() {
        const decorations = document.querySelectorAll('.background-decoration svg');
        decorations.forEach((decoration, index) => {
            setTimeout(() => {
                decoration.style.opacity = '0.08';
            }, 500 * index);
        });
    }
    
    // 启动水墨动画
    animateInkBrush();
    
    // 窗口滚动效果
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        const bgMountain = document.querySelector('.bg-mountain');
        const bgWater = document.querySelector('.bg-water');
        
        if (bgMountain) {
            bgMountain.style.transform = `translateY(${scrollPosition * 0.1}px)`;
        }
        
        if (bgWater) {
            bgWater.style.transform = `translateY(${scrollPosition * 0.05}px)`;
        }
    });
});

// 添加水墨装饰SVG
function addInkBrushDecorations() {
    const decorations = `
        <!-- 山景 -->
        <svg class="bg-mountain" viewBox="0 0 1000 300" xmlns="http://www.w3.org/2000/svg">
            <path d="M0,300 L200,100 L400,250 L600,150 L800,200 L1000,100 L1000,300 Z" fill="#000" />
        </svg>
        
        <!-- 水面 -->
        <svg class="bg-water" viewBox="0 0 1000 200" xmlns="http://www.w3.org/2000/svg">
            <path d="M0,200 C200,150 400,180 600,140 C800,100 1000,120 1000,200 Z" fill="#000" />
        </svg>
        
        <!-- 松树 -->
        <svg class="bg-pine" viewBox="0 0 200 400" xmlns="http://www.w3.org/2000/svg">
            <line x1="100" y1="0" x2="100" y2="400" stroke="#000" stroke-width="5" />
            <polygon points="100,50 50,150 150,150" fill="#000" />
            <polygon points="100,100 50,200 150,200" fill="#000" />
            <polygon points="100,150 50,250 150,250" fill="#000" />
            <polygon points="100,200 50,300 150,300" fill="#000" />
        </svg>
        
        <!-- 柳树 -->
        <svg class="bg-willow" viewBox="0 0 200 500" xmlns="http://www.w3.org/2000/svg">
            <line x1="100" y1="0" x2="100" y2="150" stroke="#000" stroke-width="3" />
            <path d="M100,120 C120,150 140,180 130,220" stroke="#000" stroke-width="2" fill="none" />
            <path d="M100,140 C110,170 130,200 120,240" stroke="#000" stroke-width="2" fill="none" />
            <path d="M100,130 C80,160 60,190 70,230" stroke="#000" stroke-width="2" fill="none" />
            <path d="M100,150 C90,180 70,210 80,250" stroke="#000" stroke-width="2" fill="none" />
            <path d="M100,120 C130,160 150,200 140,260" stroke="#000" stroke-width="2" fill="none" />
        </svg>
    `;
    
    const container = document.querySelector('.background-decoration');
    if (container) {
        container.innerHTML = decorations;
    }
}

// 移除了历史记录和生成卡片功能相关变量

// 切换创作/历史记录标签
function setupTabNavigation() {
    const createTab = document.getElementById('create-tab');
    const createSection = document.getElementById('create-section');
    
    if (createTab && createSection) {
        // 确保创作标签始终处于激活状态
        createTab.classList.add('active');
        createSection.style.display = 'block';
    }
}

// 移除了历史记录和生成卡片功能相关函数



// 初始化所有功能
function initializeApp() {
    console.log('initializeApp函数开始执行...');
    
    // 更新generatePoetryAndImage函数以保存当前生成结果
    const originalGeneratePoetryAndImage = window.generatePoetryAndImage;
    console.log('检查原始generatePoetryAndImage函数:', typeof originalGeneratePoetryAndImage === 'function');
    
    if (typeof originalGeneratePoetryAndImage === 'function') {
        window.generatePoetryAndImage = async function() {
            // 调用原始函数并等待完成
            await originalGeneratePoetryAndImage.call(this);
            
            // 获取当前生成结果
            const poetryTitle = document.getElementById('poetryTitle');
            const poetryContent = document.getElementById('poetryContent');
            const poetryNote = document.getElementById('poetryNote');
            const resultImage = document.getElementById('resultImage');
            
            if (poetryTitle && poetryContent && resultImage) {
                currentGeneration = {
                    title: poetryTitle.textContent,
                    content: poetryContent.textContent,
                    comment: poetryNote ? poetryNote.textContent : '',
                    image_url: resultImage.src
                };
            }
        };
    }
    
    // 设置功能
    console.log('开始设置导航标签功能...');
    setupTabNavigation();
    console.log('导航标签功能设置完成');
    
    console.log('initializeApp函数执行完成');
}

// 页面加载完成后初始化应用
window.addEventListener('load', function() {
    addInkBrushDecorations();
});