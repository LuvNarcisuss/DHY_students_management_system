from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, current_app)
from datetime import datetime
from werkzeug.utils import secure_filename
from db import get_db_connection
from login import login_required
import os
import bcrypt

user_bp = Blueprint('users', __name__, template_folder='templates/user')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/student/student_profile')
@login_required
# 学生信息
def student_profile():
    if session.get('role') != 'student':
        return redirect(url_for('index'))

    # 获取学生信息
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    student = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('profile/student_profile.html', student=student)

@user_bp.route('/teacher/teacher_profile')
@login_required
# 老师信息
def teacher_profile():
    if session.get('role') != 'teacher':
        return redirect(url_for('index'))

    # 获取老师信息
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    teacher = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('profile/teacher_profile.html', teacher=teacher)

@user_bp.route('/admin/admin_profile')
@login_required
# 管理员信息
def admin_profile():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    # 获取老师信息
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('profile/admin_profile.html', admin=admin)

@user_bp.route('/edit_student_profile')
@login_required
# 修改学生信息
def edit_student_profile():
    if session.get('role') != 'student':
        return redirect(url_for('teacher_index'))

    # 获取当前学生的信息
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    student = cursor.fetchone()
    cursor.close()
    conn.close()

    if not student:
        return "学生信息未找到", 404

    return render_template('edit_profile/edit_student_profile.html', student=student)

@user_bp.route('/edit_teacher_profile')
@login_required
# 修改老师信息
def edit_teacher_profile():
    if session.get('role') != 'teacher':
        return redirect(url_for('index'))

    # 获取当前学生的信息
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    teacher = cursor.fetchone()
    cursor.close()
    conn.close()

    if not teacher:
        return "老师信息未找到", 404

    return render_template('edit_profile/edit_teacher_profile.html', teacher=teacher)

@user_bp.route('/edit_admin_profile')
@login_required
# 修改管理员信息
def edit_admin_profile():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    # 获取当前管理员的信息
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()

    if not admin:
        return "管理员信息未找到", 404

    return render_template('edit_profile/edit_admin_profile.html', admin=admin)

@user_bp.route('/update_teacher_profile', methods=['POST'])
@login_required
# 更新老师信息
def update_teacher_profile():
    if session.get('role') != 'teacher':
        return redirect(url_for('index'))

    # 获取表单数据
    username = request.form['username']
    gender = request.form['gender']
    birthdate = request.form['birthdate']
    department = request.form['department']
    title = request.form['title']
    phone = request.form['phone']
    email = request.form['email']
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if 'avatar' in request.files:
        avatar_file = request.files['avatar']
        if avatar_file.filename != '':
            # 确保上传的是图片
            if avatar_file and allowed_file(avatar_file.filename):
                filename = secure_filename(f"{session['user_id']}_{avatar_file.filename}")
                # avatar_path = os.path.join(user_bp.config['UPLOAD_FOLDER'], filename)
                avatar_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                avatar_file.save(avatar_path)
                avatar_url = f"/static/uploads/avatars/{filename}"

                # 更新数据库中的头像路径
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                               UPDATE users
                               SET avatar = %s
                               WHERE id = %s
                               ''', (avatar_url, session['user_id']))
                conn.commit()
                cursor.close()
                conn.close()

    # 更新数据库
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET username = %s, gender = %s, birthdate = %s, department = %s, title = %s, phone = %s, email = %s, created_at = %s 
        WHERE id = %s
    ''', (username, gender, birthdate, department, title, phone, email, created_at, session['user_id']))
    conn.commit()
    cursor.close()
    conn.close()

    session.update({
        'username': username,
        'gender': gender,
        'birthdate': birthdate,
        'department': department,
        'title': title,
        'phone': phone,
        'email': email,
        'avatar': avatar_url  # 无论是否上传新头像都会更新
    })

    return redirect(url_for('users.teacher_profile'))

@user_bp.route('/update_admin_profile', methods=['POST'])
@login_required
# 更新管理员信息
def update_admin_profile():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    # 获取表单数据
    username = request.form['username']
    gender = request.form['gender']
    birthdate = request.form['birthdate']
    department = request.form['department']
    title = request.form['title']
    phone = request.form['phone']
    email = request.form['email']
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if 'avatar' in request.files:
        avatar_file = request.files['avatar']
        if avatar_file.filename != '':
            # 确保上传的是图片
            if avatar_file and allowed_file(avatar_file.filename):
                filename = secure_filename(f"{session['user_id']}_{avatar_file.filename}")
                avatar_path = os.path.join(user_bp.config['UPLOAD_FOLDER'], filename)
                avatar_file.save(avatar_path)
                avatar_url = f"/static/uploads/avatars/{filename}"

                # 更新数据库中的头像路径
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                               UPDATE users
                               SET avatar = %s
                               WHERE id = %s
                               ''', (avatar_url, session['user_id']))
                conn.commit()
                cursor.close()
                conn.close()

    # 更新数据库
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET username = %s, gender = %s, birthdate = %s, department = %s, title = %s, phone = %s, email = %s, created_at = %s 
        WHERE id = %s
    ''', (username, gender, birthdate, department, title, phone, email, created_at, session['user_id']))
    conn.commit()
    cursor.close()
    conn.close()

    session.update({
        'username': username,
        'gender': gender,
        'birthdate': birthdate,
        'department': department,
        'title': title,
        'phone': phone,
        'email': email,
        'avatar': avatar_url  # 无论是否上传新头像都会更新
    })

    return redirect(url_for('users.admin_profile'))

@user_bp.route('/update_student_profile', methods=['POST'])
@login_required
# 更新学生信息
def update_student_profile():
    if session.get('role') != 'student':
        return redirect(url_for('teacher_index'))

    # 获取表单数据
    username = request.form['username']
    gender = request.form['gender']
    birthdate = request.form['birthdate']
    department = request.form['department']
    major = request.form['major']
    grade = request.form['grade']
    classname = request.form['classname']
    phone = request.form['phone']
    email = request.form['email']
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    avatar_url = session.get('avatar', '/static/images/default_avatar.png')

    if 'avatar' in request.files:
        avatar_file = request.files['avatar']
        if avatar_file.filename != '':
            # 确保上传的是图片
            if avatar_file and allowed_file(avatar_file.filename):
                filename = secure_filename(f"{session['user_id']}_{avatar_file.filename}")
                avatar_path = os.path.join(user_bp.config['UPLOAD_FOLDER'], filename)
                avatar_file.save(avatar_path)
                avatar_url = f"/static/uploads/avatars/{filename}"

                # 更新数据库中的头像路径
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                               UPDATE users
                               SET avatar = %s
                               WHERE id = %s
                               ''', (avatar_url, session['user_id']))
                conn.commit()
                cursor.close()
                conn.close()

    # 更新数据库
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET username = %s, gender = %s, birthdate = %s, department = %s, major = %s, grade = %s, classname = %s, phone = %s, email = %s, created_at = %s
        WHERE id = %s
    ''', (username, gender, birthdate, department, major, grade, classname, phone, email, created_at, session['user_id']))
    conn.commit()
    cursor.close()
    conn.close()

    session.update({
        'username': username,
        'gender': gender,
        'birthdate': birthdate,
        'department': department,
        'major': major,
        'grade': grade,
        'classname': classname,
        'phone': phone,
        'email': email,
        'avatar': avatar_url  # 无论是否上传新头像都会更新
    })

    return redirect(url_for('users.student_profile'))

@user_bp.route('/add_student', methods=['GET', 'POST'])
@login_required
# 添加学生
def add_student():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form['username']
        gender = request.form['gender']
        birthdate = request.form['birthdate']
        department = request.form['department']
        major = request.form['major']
        grade = request.form['grade']
        classname = request.form['classname']
        phone = request.form['phone']
        email = request.form['email']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        password = '123456'.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # 插入数据到数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, password, role, gender, birthdate, department, major, grade, classname, phone, email, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (username, hashed_password.decode('utf-8'), 'student', gender, birthdate, department, major, grade, classname, phone, email, created_at)
        )
        conn.commit()
        cursor.close()
        conn.close()

        # 跳转到查看学生页面
        return redirect(url_for('users.view_users'))

    return render_template('admin/add_student.html')

@user_bp.route('/view_users')
@login_required
def view_users():
    # 从数据库获取所有用户
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin/view_users.html', users=users)

@user_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    # 查找用户
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return "用户未找到", 404

    if request.method == 'POST':
        # 获取表单数据
        new_username = request.form['username']
        gender = request.form['gender']
        birthdate = request.form['birthdate']
        department = request.form['department']
        major = request.form['major']
        grade = request.form['grade']
        classname = request.form['classname']
        phone = request.form['phone']
        email = request.form['email']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 检查用户名是否已被其他用户使用
        cursor.execute('SELECT id FROM users WHERE username = %s AND id != %s',
                       (new_username, user_id))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return render_template('edit_profile/edit_user.html',
                                   user=user,
                                   error='用户名已被其他用户使用')

        try:
            # 更新用户信息
            cursor.execute('''
                UPDATE users
                SET username = %s, gender = %s, birthdate = %s, 
                    department = %s, major = %s, grade = %s, 
                    classname = %s, phone = %s, email = %s, 
                    created_at = %s
                WHERE id = %s
            ''', (new_username, gender, birthdate, department,
                  major, grade, classname, phone, email,
                  created_at, user_id))
            conn.commit()

            return redirect(url_for('view_users'))
        except Exception as e:
            conn.rollback()
            return render_template('edit_profile/edit_user.html',
                                   user=user,
                                   error=f'更新失败: {str(e)}')
        finally:
            cursor.close()
            conn.close()

    # GET请求处理
    cursor.close()
    conn.close()
    return render_template('edit_profile/edit_user.html', user=user)

@user_bp.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('users.view_users'))
