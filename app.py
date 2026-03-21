from flask import (Flask, render_template, redirect, url_for, session)
from login import login_bp, login_required
from assignments import assignment_bp
from users import user_bp
from courses import course_bp
from apply import apply_bp
from approval import approval_bp
import os

app = Flask(__name__)
app.debug = True
app.secret_key = '123456'

# 配置文件上传
UPLOAD_FOLDER = 'static/uploads/avatars'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_AVATAR_SIZE'] = 2 * 1024 * 1024
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.register_blueprint(login_bp)  # 注册登录蓝图
app.register_blueprint(assignment_bp, url_prefix='/assignments') # 注册作业蓝图
app.register_blueprint(user_bp, url_prefix='/users') # 注册用户蓝图
app.register_blueprint(course_bp, url_prefix='/courses') # 注册课程蓝图
app.register_blueprint(apply_bp, url_prefix='/apply')
app.register_blueprint(approval_bp, url_prefix='/approval')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))  # 未登录则跳转到登录页面

    # 根据用户角色跳转到不同主页
    if session.get('role') == 'teacher':
        return redirect(url_for('teacher_index'))  # 老师主页
    elif session.get('role') == 'student':
        return redirect(url_for('student_index'))  # 学生主页
    elif session.get('role') == 'admin':
        return redirect(url_for('admin_index'))  # 管理员主页
    else:
        return redirect(url_for('login.login'))  # 如果角色未知，跳转到登录页面

@app.route('/teacher')
@login_required
# 老师主页
def teacher_index():
    return render_template('index/teacher_index.html')

@app.route('/student')
@login_required
# 学生主页
def student_index():
    return render_template('index/student_index.html')

@app.route('/admin')
@login_required
# 管理员主页
def admin_index():
    return render_template('index/admin_index.html')

@app.route('/heart')
def heart():
    return render_template('heart.html')

if __name__ == '__main__' :
    # 运行应用，监听所有网络接口的 5000 端口
    app.run(host='0.0.0.0', port=5000, debug=True)