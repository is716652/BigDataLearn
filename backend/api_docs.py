from flask import Flask
from flask_restx import Api, Resource, fields, Namespace
from flask_cors import CORS
import json

# 创建API文档应用
def create_api_docs_app():
    app = Flask(__name__)
    CORS(app)
    
    # 配置API文档
    api = Api(
        app,
        version='1.0',
        title='大数据学习平台 API',
        description='提供学习模块、考试系统、用户管理等功能的RESTful API接口',
        doc='/docs/',
        prefix='/api'
    )
    
    # 定义命名空间
    modules_ns = Namespace('modules', description='学习模块相关接口')
    exams_ns = Namespace('exams', description='考试系统相关接口')
    auth_ns = Namespace('auth', description='用户认证相关接口')
    admin_ns = Namespace('admin', description='管理员功能接口')
    
    api.add_namespace(modules_ns)
    api.add_namespace(exams_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(admin_ns)
    
    # 定义数据模型
    module_model = api.model('Module', {
        'id': fields.Integer(required=True, description='模块ID'),
        'title': fields.String(required=True, description='模块标题'),
        'description': fields.String(description='模块描述'),
        'ord': fields.Integer(description='排序号')
    })
    
    topic_model = api.model('Topic', {
        'id': fields.Integer(required=True, description='主题ID'),
        'title': fields.String(required=True, description='主题标题'),
        'ord': fields.Integer(description='排序号')
    })
    
    content_model = api.model('Content', {
        'title': fields.String(description='内容标题'),
        'theory': fields.String(description='理论知识'),
        'code': fields.String(description='代码示例'),
        'case': fields.String(description='案例分析'),
        'exercise': fields.String(description='练习题目'),
        'images': fields.List(fields.String, description='相关图片')
    })
    
    exam_model = api.model('Exam', {
        'id': fields.Integer(required=True, description='考试ID'),
        'name': fields.String(required=True, description='考试名称')
    })
    
    question_model = api.model('Question', {
        'id': fields.Integer(required=True, description='题目ID'),
        'type': fields.String(required=True, description='题目类型', enum=['mcq', 'tf', 'fill', 'short']),
        'prompt': fields.String(required=True, description='题目内容'),
        'options': fields.List(fields.String, description='选项（选择题）'),
        'score': fields.Integer(required=True, description='分值'),
        'ord': fields.Integer(description='排序号')
    })
    
    user_model = api.model('User', {
        'id': fields.Integer(required=True, description='用户ID'),
        'name': fields.String(required=True, description='姓名'),
        'username': fields.String(description='用户名'),
        'student_id': fields.String(description='学号'),
        'role': fields.String(required=True, description='角色', enum=['student', 'admin'])
    })
    
    login_model = api.model('Login', {
        'student_id': fields.String(description='学号'),
        'username': fields.String(description='用户名'),
        'password': fields.String(required=True, description='密码')
    })
    
    register_model = api.model('Register', {
        'student_id': fields.String(required=True, description='学号'),
        'name': fields.String(required=True, description='姓名'),
        'password': fields.String(description='密码（默认123456）')
    })
    
    # 学习模块接口文档
    @modules_ns.route('')
    class ModuleList(Resource):
        @modules_ns.doc('list_modules')
        @modules_ns.marshal_list_with(module_model)
        def get(self):
            """获取所有学习模块"""
            return []
    
    @modules_ns.route('/<int:mid>/topics')
    class TopicList(Resource):
        @modules_ns.doc('list_topics')
        @modules_ns.marshal_list_with(topic_model)
        def get(self, mid):
            """获取指定模块的所有主题"""
            return []
    
    @modules_ns.route('/topics/<int:tid>/content')
    class TopicContent(Resource):
        @modules_ns.doc('get_content')
        @modules_ns.marshal_with(content_model)
        def get(self, tid):
            """获取指定主题的学习内容"""
            return {}
    
    # 考试系统接口文档
    @exams_ns.route('')
    class ExamList(Resource):
        @exams_ns.doc('list_exams')
        @exams_ns.marshal_list_with(exam_model)
        def get(self):
            """获取所有考试"""
            return []
    
    @exams_ns.route('/<int:eid>')
    class ExamDetail(Resource):
        @exams_ns.doc('get_exam')
        @exams_ns.marshal_list_with(question_model)
        def get(self, eid):
            """获取考试详情（题目列表）"""
            return []
    
    @exams_ns.route('/<int:eid>/submit')
    class ExamSubmit(Resource):
        @exams_ns.doc('submit_exam')
        @exams_ns.expect(api.model('ExamAnswers', {
            'answers': fields.Raw(required=True, description='答案字典 {题目ID: 答案}')
        }))
        def post(self, eid):
            """提交考试答案"""
            return {
                'score': 85,
                'total': 100,
                'rate': 85.0,
                'detail': [],
                'wrong_qids': [],
                'suggestions': []
            }
    
    # 用户认证接口文档
    @auth_ns.route('/login')
    class Login(Resource):
        @auth_ns.doc('user_login')
        @auth_ns.expect(login_model)
        def post(self):
            """用户登录"""
            return {
                'token': 'jwt_token_here',
                'user': {
                    'id': 1,
                    'name': '张三',
                    'username': 'zhangsan',
                    'student_id': '2021001',
                    'role': 'student'
                }
            }
    
    @auth_ns.route('/register')
    class Register(Resource):
        @auth_ns.doc('user_register')
        @auth_ns.expect(register_model)
        def post(self):
            """用户注册"""
            return {'ok': True}
    
    @auth_ns.route('/me')
    class UserProfile(Resource):
        @auth_ns.doc('get_profile')
        @auth_ns.marshal_with(user_model)
        @auth_ns.doc(security='Bearer')
        def get(self):
            """获取当前用户信息（需要认证）"""
            return {}
    
    # 管理员接口文档
    @admin_ns.route('/import_students')
    class ImportStudents(Resource):
        @admin_ns.doc('import_students')
        @admin_ns.doc(security='Bearer')
        @admin_ns.expect(api.parser().add_argument('file', location='files', type='file', required=True, help='Excel文件'))
        def post(self):
            """批量导入学生信息（Excel文件）"""
            return {
                'ok': True,
                'imported': 50
            }
    
    # 添加安全定义
    api.authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Token格式: Bearer <token>'
        }
    }
    
    # 添加主页重定向
    @app.route('/')
    def index():
        return '<h1>大数据学习平台 API 文档</h1><p><a href="/docs/">查看 API 文档</a></p>'
    
    return app

if __name__ == '__main__':
    app = create_api_docs_app()
    app.run(host='0.0.0.0', port=91, debug=True)