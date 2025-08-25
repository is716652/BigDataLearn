// 全局状态管理
let currentUser = null;
let currentModule = null;
let currentTopic = null;
let modules = [];
let topics = [];
let content = [];
let examData = [];

// DOM 元素引用
const elements = {
  // 导航
  tabLearn: document.getElementById('tab-learn'),
  tabProfile: document.getElementById('tab-profile'),
  tabExam: document.getElementById('tab-exam'),
  tabAdmin: document.getElementById('tab-admin'),
  
  // 页面
  learnPage: document.getElementById('learn-page'),
  profilePage: document.getElementById('profile-page'),
  examPage: document.getElementById('exam-page'),
  adminPage: document.getElementById('admin-page'),
  
  // 学习页面元素
  modulesGrid: document.getElementById('modules-grid'),
  topicsSection: document.getElementById('topics-section'),
  currentModuleTitle: document.getElementById('current-module-title'),
  topicsGrid: document.getElementById('topics'),
  contentSection: document.getElementById('content-section'),
  currentTopicTitle: document.getElementById('current-topic-title'),
  contentCards: document.getElementById('content'),
  aiGenerate: document.getElementById('ai-generate'),
  
  // 认证元素
  loginId: document.getElementById('login-id'),
  loginPw: document.getElementById('login-pw'),
  btnLogin: document.getElementById('btn-login'),
  btnLogout: document.getElementById('btn-logout'),
  loginTip: document.getElementById('login-tip'),
  authBox: document.getElementById('auth-box'),
  profileBox: document.getElementById('profile-box'),
  historyBox: document.getElementById('history-box'),
  me: document.getElementById('me'),
  history: document.getElementById('history'),
  
  // 考试元素
  examSelect: document.getElementById('exam-select'),
  startExam: document.getElementById('start-exam'),
  examForm: document.getElementById('exam-form'),
  examResult: document.getElementById('exam-result'),
  
  // 管理元素
  excelFile: document.getElementById('excel-file'),
  btnImport: document.getElementById('btn-import'),
  importTip: document.getElementById('import-tip')
};

// 页面初始化
document.addEventListener('DOMContentLoaded', function() {
  initializeApp();
});

function initializeApp() {
  setupNavigation();
  loadModules();
  loadExams();
  checkLoginStatus();
  showPage('learn'); // 默认显示学习页面
}

// 导航设置
function setupNavigation() {
  elements.tabLearn.addEventListener('click', () => showPage('learn'));
  elements.tabProfile.addEventListener('click', () => showPage('profile'));
  elements.tabExam.addEventListener('click', () => showPage('exam'));
  elements.tabAdmin.addEventListener('click', () => showPage('admin'));
  
  // 认证事件
  elements.btnLogin.addEventListener('click', login);
  elements.btnLogout.addEventListener('click', logout);
  
  // AI生成事件
  elements.aiGenerate.addEventListener('click', generateAIContent);
  
  // 考试事件
  elements.startExam.addEventListener('click', startExam);
  
  // 管理事件
  elements.btnImport.addEventListener('click', importStudents);
}

// 页面显示控制
function showPage(page) {
  // 隐藏所有页面
  document.querySelectorAll('.page').forEach(p => {
    p.classList.remove('visible');
  });
  
  // 移除所有导航按钮的active状态
  document.querySelectorAll('.nav button').forEach(btn => {
    btn.classList.remove('active');
  });
  
  // 显示目标页面和激活对应按钮
  switch(page) {
    case 'learn':
      elements.learnPage.classList.add('visible');
      elements.tabLearn.classList.add('active');
      break;
    case 'profile':
      elements.profilePage.classList.add('visible');
      elements.tabProfile.classList.add('active');
      break;
    case 'exam':
      elements.examPage.classList.add('visible');
      elements.tabExam.classList.add('active');
      break;
    case 'admin':
      elements.adminPage.classList.add('visible');
      elements.tabAdmin.classList.add('active');
      break;
  }
}

// 加载学习模块
async function loadModules() {
  try {
    // 添加时间戳参数防止缓存
    const timestamp = new Date().getTime();
    const response = await fetch(`http://localhost:90/api/modules?_t=${timestamp}`);
    modules = await response.json();
    renderModules();
  } catch (error) {
    console.error('加载模块失败:', error);
  }
}

// 渲染模块卡片
function renderModules() {
  elements.modulesGrid.innerHTML = modules.map(module => `
    <div class="module-card" data-module-id="${module.id}" onclick="selectModule(${module.id})">
      <h3>${module.title}</h3>
      <p>${module.description || '探索这个模块的核心概念和实践应用'}</p>
      <div class="module-meta">
        <span>📚 ${module.topics?.length || 5} 个知识点</span>
        <span>⏱️ 预计 ${Math.ceil((module.topics?.length || 5) * 15)} 分钟</span>
      </div>
    </div>
  `).join('');
}

// 选择模块
function selectModule(moduleId) {
  // 更新选中状态
  document.querySelectorAll('.module-card').forEach(card => {
    card.classList.remove('selected');
  });
  document.querySelector(`[data-module-id="${moduleId}"]`).classList.add('selected');
  
  currentModule = modules.find(m => m.id === moduleId);
  
  // 显示知识点区域
  elements.currentModuleTitle.textContent = currentModule.title;
  elements.topicsSection.style.display = 'block';
  
  // 加载该模块的知识点
  loadTopics(moduleId);
  
  // 隐藏内容区域
  elements.contentSection.style.display = 'none';
}

// 加载知识点
async function loadTopics(moduleId) {
  try {
    // 添加时间戳参数防止缓存
    const timestamp = new Date().getTime();
    const response = await fetch(`http://localhost:90/api/modules/${moduleId}/topics?_t=${timestamp}`);
    topics = await response.json();
    renderTopics();
  } catch (error) {
    console.error('加载知识点失败:', error);
  }
}

// 渲染知识点
function renderTopics() {
  elements.topicsGrid.innerHTML = topics.map(topic => `
    <div class="topic-card" data-topic-id="${topic.id}" onclick="selectTopic(${topic.id})">
      <h4>${topic.title}</h4>
      <p>${topic.description || '深入了解这个重要概念'}</p>
    </div>
  `).join('');
}

// 选择知识点
function selectTopic(topicId) {
  // 更新选中状态
  document.querySelectorAll('.topic-card').forEach(card => {
    card.classList.remove('selected');
  });
  document.querySelector(`[data-topic-id="${topicId}"]`).classList.add('selected');
  
  currentTopic = topics.find(t => t.id === topicId);
  
  // 显示内容区域
  elements.currentTopicTitle.textContent = currentTopic.title;
  elements.contentSection.style.display = 'block';
  
  // 加载内容
  loadContent(topicId);
  
  // 启用AI生成按钮（仅管理员）
  if (currentUser && currentUser.role === 'admin') {
    elements.aiGenerate.disabled = false;
  }
}

// 加载学习内容
async function loadContent(topicId) {
  try {
    const response = await fetch(`http://localhost:90/api/topics/${topicId}/content`);
    content = await response.json();
    renderContent();
  } catch (error) {
    console.error('加载内容失败:', error);
  }
}

// 渲染学习内容
function renderContent() {
  if (!content || Object.keys(content).length === 0) {
    elements.contentCards.innerHTML = `
      <div class="content-card">
        <h4>📖 开始学习</h4>
        <p>这个知识点的详细内容正在准备中。${currentUser && currentUser.role === 'admin' ? '管理员可以点击"AI扩写内容"来生成学习材料。' : ''}</p>
      </div>
    `;
    return;
  }
  
  // 格式化文本内容，将换行符转换为HTML
  function formatContent(text) {
    if (!text) return text;
    return text
      .replace(/\n\n/g, '</p><p>')  // 双换行转换为段落
      .replace(/\n/g, '<br>')       // 单换行转换为换行标签
      .replace(/^/, '<p>')          // 开头添加段落标签
      .replace(/$/, '</p>');        // 结尾添加段落标签
  }
  
  // 处理练习题数据（可能是数组或字符串）
  function formatExercises(exercises) {
    if (!exercises) return '<p>练习题正在准备中...</p>';
    if (Array.isArray(exercises)) {
      return exercises.map((ex, index) => `<p><strong>${index + 1}. </strong>${ex}</p>`).join('');
    }
    return formatContent(exercises);
  }
  
  // 将content对象转换为数组格式进行渲染
  const contentSections = [
    { title: '📚 理论知识', content: formatContent(content.theory) || '<p>理论内容正在准备中...</p>' },
    { title: '💻 代码示例', content: content.code ? `<pre><code>${content.code}</code></pre>` : '<p>代码示例正在准备中...</p>' },
    { title: '🔍 案例分析', content: formatContent(content.case) || '<p>案例分析正在准备中...</p>' },
    { title: '✏️ 练习题', content: formatExercises(content.exercises || content.exercise) }
  ];
  
  elements.contentCards.innerHTML = contentSections.map(item => `
    <div class="content-card">
      <h4>${item.title}</h4>
      <div class="content-body">${item.content}</div>
    </div>
  `).join('');
}

// AI生成内容（仅管理员，一次性生成）
async function generateAIContent() {
  if (!currentUser || currentUser.role !== 'admin') {
    showTip(elements.loginTip, '只有管理员可以生成AI内容', 'error');
    return;
  }
  
  if (!currentTopic) {
    showTip(elements.loginTip, '请先选择一个知识点', 'error');
    return;
  }
  
  elements.aiGenerate.disabled = true;
  elements.aiGenerate.textContent = '🔄 生成中...';
  
  try {
    const response = await fetch(`http://localhost:90/api/generate/topic/${currentTopic.id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        topic_id: currentTopic.id,
        topic_name: currentTopic.title,
        module_name: currentModule.title
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      // 重新加载内容以显示生成的内容
      await loadContent(currentTopic.id);
      showTip(elements.loginTip, '✨ AI内容生成成功！内容已保存，刷新页面不会重新生成。', 'success');
    } else {
      showTip(elements.loginTip, result.error || 'AI生成失败', 'error');
    }
  } catch (error) {
    console.error('AI生成错误:', error);
    showTip(elements.loginTip, '网络错误，请稍后重试', 'error');
  } finally {
    elements.aiGenerate.disabled = false;
    elements.aiGenerate.textContent = '✨ AI扩写内容';
  }
}

// 用户认证
async function login() {
  const id = elements.loginId.value.trim();
  const password = elements.loginPw.value.trim();
  
  if (!id || !password) {
    showTip(elements.loginTip, '请输入用户名和密码', 'error');
    return;
  }
  
  try {
    const response = await fetch('http://localhost:90/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: id, password })
    });
    
    const result = await response.json();
    
    if (result.success) {
      currentUser = result.user;
      updateAuthUI();
      loadUserHistory();
      showTip(elements.loginTip, `欢迎，${currentUser.name}！`, 'success');
    } else {
      showTip(elements.loginTip, result.error || '登录失败', 'error');
    }
  } catch (error) {
    console.error('登录错误:', error);
    showTip(elements.loginTip, '网络错误，请稍后重试', 'error');
  }
}

function logout() {
  currentUser = null;
  updateAuthUI();
  showTip(elements.loginTip, '已退出登录', 'info');
}

function checkLoginStatus() {
  // 这里可以检查本地存储或cookie中的登录状态
  updateAuthUI();
}

function updateAuthUI() {
  if (currentUser) {
    elements.btnLogin.style.display = 'none';
    elements.btnLogout.style.display = 'inline-block';
    elements.profileBox.style.display = 'block';
    elements.historyBox.style.display = 'block';
    elements.me.innerHTML = `
      <p><strong>姓名：</strong>${currentUser.name}</p>
      <p><strong>角色：</strong>${currentUser.role === 'admin' ? '管理员' : '学生'}</p>
      <p><strong>学号：</strong>${currentUser.username}</p>
    `;
    
    // 显示管理员标签页
    if (currentUser.role === 'admin') {
      elements.tabAdmin.style.display = 'inline-block';
    }
  } else {
    elements.btnLogin.style.display = 'inline-block';
    elements.btnLogout.style.display = 'none';
    elements.profileBox.style.display = 'none';
    elements.historyBox.style.display = 'none';
    elements.tabAdmin.style.display = 'none';
    elements.me.innerHTML = '';
    elements.history.innerHTML = '';
  }
}

// 加载用户历史记录
async function loadUserHistory() {
  if (!currentUser) return;
  
  try {
    const response = await fetch(`http://localhost:90/api/my/scores`);
    const history = await response.json();
    
    if (history.length === 0) {
      elements.history.innerHTML = '<p>暂无学习记录</p>';
      return;
    }
    
    elements.history.innerHTML = history.map(record => `
      <div class="history-item">
        <h4>${record.exam_name}</h4>
        <p>得分：${record.score}/${record.total} (${Math.round(record.score/record.total*100)}%)</p>
        <p>时间：${new Date(record.timestamp).toLocaleString()}</p>
      </div>
    `).join('');
  } catch (error) {
    console.error('加载历史记录失败:', error);
  }
}

// 考试功能
async function loadExams() {
  try {
    const response = await fetch('http://localhost:90/api/exams');
    examData = await response.json();
    
    elements.examSelect.innerHTML = examData.map(exam => 
      `<option value="${exam.id}">${exam.name}</option>`
    ).join('');
  } catch (error) {
    console.error('加载考试失败:', error);
  }
}

function startExam() {
  if (!currentUser) {
    showTip(elements.loginTip, '请先登录后再参加考试', 'error');
    showPage('profile');
    return;
  }
  
  const examId = elements.examSelect.value;
  const exam = examData.find(e => e.id == examId);
  
  if (!exam) return;
  
  elements.examForm.innerHTML = exam.questions.map((q, i) => `
    <div class="q">
      <h4>${i + 1}. ${q.question}</h4>
      ${q.type === 'choice' ? 
        q.options.map((opt, j) => `
          <label><input type="radio" name="q${i}" value="${j}"> ${opt}</label>
        `).join('') :
        `<input type="text" name="q${i}" placeholder="请输入答案">`
      }
    </div>
  `).join('') + `<button type="submit" class="btn primary">提交答案</button>`;
  
  elements.examForm.onsubmit = (e) => submitExam(e, exam);
}

async function submitExam(event, exam) {
  event.preventDefault();
  
  const formData = new FormData(event.target);
  const answers = [];
  
  for (let i = 0; i < exam.questions.length; i++) {
    answers.push(formData.get(`q${i}`) || '');
  }
  
  try {
    const response = await fetch(`http://localhost:90/api/exams/${exam.id}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        exam_id: exam.id,
        username: currentUser.username,
        answers
      })
    });
    
    const result = await response.json();
    
    elements.examResult.innerHTML = `
      <h3>考试结果</h3>
      <p>得分：${result.score}/${result.total} (${Math.round(result.score/result.total*100)}%)</p>
      <p>用时：${new Date().toLocaleString()}</p>
    `;
    
    // 刷新历史记录
    loadUserHistory();
  } catch (error) {
    console.error('提交考试失败:', error);
    showTip(elements.loginTip, '提交失败，请稍后重试', 'error');
  }
}

// 管理功能
async function importStudents() {
  const file = elements.excelFile.files[0];
  if (!file) {
    showTip(elements.importTip, '请选择Excel文件', 'error');
    return;
  }
  
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await fetch('http://localhost:90/api/admin/import_students', {
      method: 'POST',
      body: formData
    });
    
    const result = await response.json();
    
    if (result.success) {
      showTip(elements.importTip, `成功导入 ${result.count} 名学生`, 'success');
      elements.excelFile.value = '';
    } else {
      showTip(elements.importTip, result.error || '导入失败', 'error');
    }
  } catch (error) {
    console.error('导入失败:', error);
    showTip(elements.importTip, '网络错误，请稍后重试', 'error');
  }
}

// 工具函数
function showTip(element, message, type = 'info') {
  element.textContent = message;
  element.className = `tip ${type}`;
  setTimeout(() => {
    element.textContent = '';
    element.className = 'tip';
  }, 3000);
}