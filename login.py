from flask import Blueprint, render_template, request, session, redirect, url_for
from datetime import datetime
from db import get_db_connection
from functools import wraps
import bcrypt  # 导入密码哈希库

# 创建蓝图
login_bp = Blueprint('login', __name__, url_prefix='/auth')


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            # 获取表单数据
            username = request.form['username']
            password = request.form['password'].encode('utf-8')  # 将密码转为bytes类型
            selected_role = request.form['role']

            # 连接数据库验证用户
            conn = get_db_connection()
            if not conn:
                return render_template('login/login.html', error='数据库连接失败')

            cursor = conn.cursor(dictionary=True)
            # 只根据用户名查询用户(不验证密码)
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                # 验证密码哈希和角色
                stored_password = user['password'].encode('utf-8')  # 获取数据库存储的哈希密码
                if (bcrypt.checkpw(password, stored_password) and
                        user['role'] == selected_role):

                    # 设置会话变量
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['gender'] = user['gender']
                    session['role'] = user['role']
                    session['avatar'] = user['avatar']

                    # 根据角色跳转不同页面
                    if user['role'] == 'teacher':
                        return redirect(url_for('teacher_index'))
                    elif user['role'] == 'student':
                        return redirect(url_for('student_index'))
                    elif user['role'] == 'admin':
                        return redirect(url_for('admin_index'))
                else:
                    # 不明确提示具体错误(安全考虑)
                    return render_template('login/login.html', error='用户名或密码错误或角色不正确')
            else:
                return render_template('login/login.html', error='用户名或密码错误或角色不正确')

        return render_template('login/login.html')
    except Exception as e:
        print(f"登录失败: {e}")
        return render_template('login/login.html', error='登录失败，请稍后重试')


@login_bp.route('/logout')
def logout():
    # 清除所有会话信息
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('gender', None)
    session.pop('role', None)
    session.pop('avatar', None)
    return redirect(url_for('login.login'))


# 登录保护
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)

    return decorated_function


@login_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        # 获取表单数据
        current_password = request.form['current_password'].encode('utf-8')
        new_password = request.form['new_password'].encode('utf-8')
        confirm_password = request.form['confirm_password']

        # 验证当前密码
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # 获取存储的密码哈希
        cursor.execute('SELECT password FROM users WHERE id = %s', (session['user_id'],))
        user = cursor.fetchone()

        # 验证当前密码是否正确
        if not user or not bcrypt.checkpw(current_password, user['password'].encode('utf-8')):
            cursor.close()
            conn.close()
            return render_template('login/change_password.html', error='当前密码错误')

        # 验证新密码是否一致
        if new_password.decode('utf-8') != confirm_password:
            cursor.close()
            conn.close()
            return render_template('login/change_password.html', error='新密码和确认密码不一致')

        # 对新密码进行哈希处理
        hashed_new_password = bcrypt.hashpw(new_password, bcrypt.gensalt())

        # 更新密码
        cursor.execute('UPDATE users SET password = %s WHERE id = %s',
                       (hashed_new_password.decode('utf-8'), session['user_id']))
        conn.commit()

        # 获取用户角色
        cursor.execute('SELECT role FROM users WHERE id = %s', (session['user_id'],))
        user_role = cursor.fetchone()['role']
        cursor.close()
        conn.close()

        # 根据角色返回不同页面
        if user_role == 'student':
            return render_template('index/student_index.html', success='密码修改成功')
        elif user_role == 'teacher':
            return render_template('index/teacher_index.html', success='密码修改成功')
        elif user_role == 'admin':
            return render_template('index/admin_index.html', success='密码修改成功')

    return render_template('login/change_password.html')


@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form['username']
        password = request.form['password'].encode('utf-8')  # 转为bytes类型
        gender = request.form['gender']
        birthdate = request.form['birthdate']
        phone = request.form['phone']
        email = request.form['email']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 根据性别设置默认头像
        default_avatar = '/static/images/男生.png' if gender == '男' else '/static/images/女生.png'

        # 对密码进行哈希处理
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # 插入新用户到数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, password, role, gender, birthdate, phone, email, created_at, avatar) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (username, hashed_password.decode('utf-8'), 'student', gender, birthdate, phone, email, created_at,
             default_avatar)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login.login'))

    return render_template('login/register.html')