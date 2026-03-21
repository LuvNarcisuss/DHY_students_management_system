from flask import (Blueprint, render_template, request, redirect, url_for, session)
from db import get_db_connection
from login import login_required

apply_bp = Blueprint('apply', __name__, template_folder='templates/apply')

# 学生请假申请
@apply_bp.route('/student/leave', methods=['GET', 'POST'])
@login_required
def student_leave_apply():
    if session.get('role') != 'student':
        return redirect(url_for('index'))

    if request.method == 'POST':
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        reason = request.form['reason']
        leave_campus = 'leave_campus' in request.form

        # 验证时间合理性
        if start_time >= end_time:
            return render_template('apply/student_leave_apply.html', error='结束时间必须晚于开始时间')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO student_leave 
                (student_id, student_name, start_time, end_time, reason, leave_campus)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (session['user_id'], session['username'], start_time, end_time, reason, leave_campus))
            conn.commit()
            return redirect(url_for('apply.student_leave_status'))
        except Exception as e:
            conn.rollback()
            return render_template('apply/student_leave_apply.html', error='提交失败: ' + str(e))
        finally:
            cursor.close()
            conn.close()

    return render_template('apply/student_leave_apply.html')

# 学生查看请假状态
@apply_bp.route('/student/leave_status')
@login_required
def student_leave_status():
    if session.get('role') != 'student':
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT * FROM student_leave 
        WHERE student_id = %s 
        ORDER BY created_at DESC
    ''', (session['user_id'],))
    leaves = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('apply/student_leave_status.html', leaves=leaves)


# 老师课程申请
@apply_bp.route('/teacher/course_apply', methods=['GET', 'POST'])
@login_required
def teacher_course_apply():
    if session.get('role') != 'teacher':
        return redirect(url_for('index'))

    if request.method == 'POST':
        course_name = request.form['course_name']
        credit = float(request.form['credit'])
        department = request.form['department']
        textbook = request.form['textbook']
        course_type = request.form['course_type']
        capacity = int(request.form.get('capacity', 50))  # 默认容量50

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO courses 
                (course_name, credit, department, teacher_name, textbook, course_type, capacity, status, teacher_id, remaining_capacity)
                VALUES (%s, %s, %s, %s, %s, %s, %s, '待审批', %s, %s)
            ''', (course_name, credit, department, session['username'], textbook, course_type, capacity, session['user_id']), capacity)
            conn.commit()
            return redirect(url_for('apply.teacher_course_status'))
        except Exception as e:
            conn.rollback()
            return render_template('apply/teacher_course_apply.html', error='提交失败: ' + str(e))
        finally:
            cursor.close()
            conn.close()

    return render_template('apply/teacher_course_apply.html')

# 老师查看课程申请状态
@apply_bp.route('/teacher/course_status')
@login_required
def teacher_course_status():
    if session.get('role') != 'teacher':
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT * FROM courses 
        WHERE teacher_name = %s 
        ORDER BY id DESC
    ''', (session['username'],))
    courses = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('apply/teacher_course_status.html', courses=courses)
