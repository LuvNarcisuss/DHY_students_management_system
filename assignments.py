from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, send_from_directory, jsonify)
import os
from db import get_db_connection
from login import login_required  # 导入登录保护
import uuid

assignment_bp = Blueprint('assignments', __name__, template_folder='templates/assignment')

# 配置上传文件夹
UPLOAD_FOLDER = 'static/uploads/assignments'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@assignment_bp.route('/teacher/assign_homework/<int:course_id>', methods=['GET', 'POST'])
@login_required
def teacher_assign_homework(course_id):
    if session.get('role') != 'teacher':
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # 验证教师是否有权为该课程创建作业
            cursor.execute('''
                SELECT id FROM courses 
                WHERE id = %s AND teacher_id = %s AND status = '已通过'
            ''', (course_id, session['user_id']))
            if not cursor.fetchone():
                flash('无权为此课程创建作业或课程未通过审批', 'error')
                return redirect(url_for('index'))

            cursor.execute('''
                INSERT INTO assignments (course_id, title, description, due_date)
                VALUES (%s, %s, %s, %s)
            ''', (course_id, title, description, due_date))
            conn.commit()
            flash('作业发布成功', 'success')
            return redirect(url_for('assignments.teacher_view_assignments', course_id=course_id))
        except Exception as e:
            conn.rollback()
            flash(f'发布作业失败: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()

    return render_template('assignment/teacher_assign_homework.html', course_id=course_id)


@assignment_bp.route('/teacher/assignments/<int:course_id>')
@login_required
def teacher_view_assignments(course_id):
    if session.get('role') != 'teacher':
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 验证课程是否属于当前老师且已通过审批
        cursor.execute('''
            SELECT id FROM courses 
            WHERE id = %s AND teacher_id = %s AND status = '已通过'
        ''', (course_id, session['user_id']))
        course = cursor.fetchone()
        if not course:
            flash('无权访问此课程的作业', 'error')
            return redirect(url_for('index'))

        # 获取该课程的所有作业
        cursor.execute('''
            SELECT a.*, COUNT(s.id) AS submission_count
            FROM assignments a
            LEFT JOIN homework_submissions s ON a.id = s.assignment_id
            WHERE a.course_id = %s
            GROUP BY a.id
            ORDER BY a.due_date DESC
        ''', (course_id,))
        assignments = cursor.fetchall()

        return render_template('assignment/teacher_view_assignments.html',
                               assignments=assignments,
                               course_id=course_id)
    finally:
        cursor.close()
        conn.close()


@assignment_bp.route('/teacher/submissions/<int:assignment_id>')
@login_required
def teacher_view_submissions(assignment_id):
    if session.get('role') != 'teacher':
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 验证作业是否属于当前老师的已通过课程
        cursor.execute('''
            SELECT a.id 
            FROM assignments a
            JOIN courses c ON a.course_id = c.id
            WHERE a.id = %s AND c.teacher_id = %s AND c.status = '已通过'
        ''', (assignment_id, session['user_id']))
        assignment = cursor.fetchone()
        if not assignment:
            flash('无权访问此作业的提交', 'error')
            return redirect(url_for('index'))

        # 获取作业信息
        cursor.execute('SELECT * FROM assignments WHERE id = %s', (assignment_id,))
        assignment_info = cursor.fetchone()

        # 获取所有提交
        cursor.execute('''
            SELECT s.*, u.username, u.email
            FROM homework_submissions s
            JOIN users u ON s.student_id = u.id
            WHERE s.assignment_id = %s
            ORDER BY s.submitted_at DESC
        ''', (assignment_id,))
        submissions = cursor.fetchall()

        return render_template('assignment/teacher_view_submissions.html',
                               assignment=assignment_info,
                               submissions=submissions)
    finally:
        cursor.close()
        conn.close()


@assignment_bp.route('/teacher/grade_submission/<int:submission_id>', methods=['POST'])
@login_required
def teacher_grade_submission(submission_id):
    if session.get('role') != 'teacher':
        return jsonify({'success': False, 'message': '无权操作'})

    grade = request.form.get('grade')
    feedback = request.form.get('feedback', '')

    try:
        grade = int(grade) if grade else None
        if grade is not None and (grade <= 0 or grade >= 100):
            raise ValueError('成绩必须在0-100之间')
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)})

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 验证提交是否属于当前老师的已通过课程
        cursor.execute('''
            SELECT s.id 
            FROM homework_submissions s
            JOIN assignments a ON s.assignment_id = a.id
            JOIN courses c ON a.course_id = c.id
            WHERE s.id = %s AND c.teacher_id = %s AND c.status = '已通过'
        ''', (submission_id, session['user_id']))
        if not cursor.fetchone():
            return jsonify({'success': False, 'message': '无权批改此提交'})

        cursor.execute('''
            UPDATE homework_submissions
            SET grade = %s, feedback = %s
            WHERE id = %s
        ''', (grade, feedback, submission_id))
        conn.commit()

        return jsonify({'success': True, 'message': '批改成功'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()


@assignment_bp.route('/student/assignments')
@login_required
def student_view_assignments():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 获取学生已选课程的所有作业（只包括已通过审批的课程）
        cursor.execute('''
            SELECT a.*, c.course_name, 
                   s.id AS submission_id, s.grade, s.feedback,
                   CASE 
                       WHEN s.id IS NULL THEN '未提交'
                       WHEN s.grade IS NULL THEN '已提交'
                       ELSE '已批改'
                   END AS status
            FROM assignments a
            JOIN courses c ON a.course_id = c.id
            JOIN student_courses sc ON c.id = sc.course_id
            LEFT JOIN homework_submissions s ON a.id = s.assignment_id AND s.student_id = %s
            WHERE sc.user_id = %s AND c.status = '已通过'
            ORDER BY a.due_date ASC
        ''', (session['user_id'], session['user_id']))
        assignments = cursor.fetchall()

        return render_template('assignment/student_view_assignments.html', assignments=assignments)
    finally:
        cursor.close()
        conn.close()


@assignment_bp.route('/student/submit_homework/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def student_submit_homework(assignment_id):
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))

    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '')
        file = request.files.get('attachment')

        attachment_path = None
        if file and file.filename:
            # 生成唯一文件名
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            attachment_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(attachment_path)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # 检查学生是否选修了这门课程（课程已通过审批）
            cursor.execute('''
                SELECT sc.user_id 
                FROM student_courses sc
                JOIN courses c ON sc.course_id = c.id
                JOIN assignments a ON c.id = a.course_id
                WHERE a.id = %s AND sc.user_id = %s AND c.status = '已通过'
            ''', (assignment_id, session['user_id']))
            if not cursor.fetchone():
                flash('无权提交此作业', 'error')
                return redirect(url_for('index'))

            # 检查是否已经提交过
            cursor.execute('''
                SELECT id FROM homework_submissions 
                WHERE assignment_id = %s AND student_id = %s
            ''', (assignment_id, session['user_id']))
            existing = cursor.fetchone()

            if existing:
                # 更新现有提交
                cursor.execute('''
                    UPDATE homework_submissions
                    SET submission_text = %s, attachment_path = %s, submitted_at = NOW()
                    WHERE id = %s
                ''', (submission_text, attachment_path, existing[0]))
            else:
                # 创建新提交
                cursor.execute('''
                    INSERT INTO homework_submissions 
                    (assignment_id, student_id, student_name, submission_text, attachment_path)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (assignment_id, session['user_id'], session['username'], submission_text, attachment_path))

            conn.commit()
            flash('作业提交成功', 'success')
            return redirect(url_for('assignments.student_view_assignments'))
        except Exception as e:
            conn.rollback()
            flash(f'提交失败: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()

    # GET请求处理
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 获取作业信息（确保课程已通过审批）
        cursor.execute('''
            SELECT a.*, c.course_name
            FROM assignments a
            JOIN courses c ON a.course_id = c.id
            JOIN student_courses sc ON c.id = sc.course_id
            WHERE a.id = %s AND sc.user_id = %s AND c.status = '已通过'
        ''', (assignment_id, session['user_id']))
        assignment = cursor.fetchone()

        if not assignment:
            flash('无权访问此作业', 'error')
            return redirect(url_for('index'))

        # 检查是否已经提交过
        cursor.execute('''
            SELECT * FROM homework_submissions
            WHERE assignment_id = %s AND student_id = %s
        ''', (assignment_id, session['user_id']))
        submission = cursor.fetchone()

        return render_template('assignment/student_submit_homework.html',
                               assignment=assignment,
                               submission=submission)
    finally:
        cursor.close()
        conn.close()


@assignment_bp.route('/download_submission/<int:submission_id>')
@login_required
def download_submission(submission_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 验证权限
        if session['role'] == 'teacher':
            cursor.execute('''
                SELECT s.attachment_path
                FROM homework_submissions s
                JOIN assignments a ON s.assignment_id = a.id
                JOIN courses c ON a.course_id = c.id
                WHERE s.id = %s AND c.teacher_id = %s AND c.status = '已通过'
            ''', (submission_id, session['user_id']))
        elif session['role'] == 'student':
            cursor.execute('''
                SELECT attachment_path FROM homework_submissions
                WHERE id = %s AND student_id = %s
            ''', (submission_id, session['user_id']))
        else:
            return "无权访问", 403

        submission = cursor.fetchone()
        if not submission or not submission['attachment_path']:
            return "文件不存在", 404

        return send_from_directory(
            os.path.dirname(submission['attachment_path']),
            os.path.basename(submission['attachment_path']),
            as_attachment=True
        )
    finally:
        cursor.close()
        conn.close()
