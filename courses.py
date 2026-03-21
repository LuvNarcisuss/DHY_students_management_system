from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, jsonify, send_file)
from datetime import datetime
from openpyxl import Workbook
from io import BytesIO
from db import get_db_connection
from login import login_required

course_bp = Blueprint('courses', __name__, template_folder='templates/courses')

@course_bp.route('/student/select_course', methods=['GET', 'POST'])
@login_required
def student_select_course():
    if session.get('role') != 'student':
        return redirect(url_for('index'))

    if request.method == 'POST':
        selected_courses = request.form.getlist('selected_courses')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # 获取当前学生已选的课程ID
            cursor.execute('''
                SELECT course_id 
                FROM student_courses 
                WHERE user_id = %s
            ''', (session['user_id'],))
            existing_course_ids = [row['course_id'] for row in cursor.fetchall()]

            # 处理新增选课
            for course_id in selected_courses:
                if int(course_id) not in existing_course_ids:
                    # 验证课程状态和剩余容量
                    cursor.execute('''
                        SELECT id, course_name, remaining_capacity 
                        FROM courses 
                        WHERE id = %s AND status = '已通过' AND remaining_capacity > 0
                    ''', (course_id,))
                    course = cursor.fetchone()

                    if not course:
                        return render_template('courses_management/student_select_course.html',
                                               error='课程不可选或已满')

                    # 插入选课记录
                    cursor.execute('''
                        INSERT INTO student_courses 
                        (user_id, student_name, course_id, course_name, status) 
                        VALUES (%s, %s, %s, %s, '已选')
                    ''', (session['user_id'], session['username'],
                          course_id, course['course_name']))

                    # 更新剩余容量
                    cursor.execute('''
                        UPDATE courses
                        SET remaining_capacity = remaining_capacity - 1 
                        WHERE id = %s
                    ''', (course_id,))

            conn.commit()
            return redirect(url_for('courses.student_courses'))
        except Exception as e:
            conn.rollback()
            return render_template('courses_management/student_select_course.html',
                                   error='选课失败: ' + str(e))
        finally:
            cursor.close()
            conn.close()

    # GET请求处理
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 查询状态为"已通过"且有剩余容量的课程
        cursor.execute('''
            SELECT c.*
            FROM courses c
            WHERE c.status = '已通过' AND c.remaining_capacity > 0
            ORDER BY c.course_name
        ''')
        available_courses = cursor.fetchall()

        # 获取学生已选课程ID
        cursor.execute('''
            SELECT course_id 
            FROM student_courses 
            WHERE user_id = %s
        ''', (session['user_id'],))
        selected_course_ids = [row['course_id'] for row in cursor.fetchall()]

        # 标记已选课程
        for course in available_courses:
            course['is_selected'] = course['id'] in selected_course_ids

        return render_template('courses_management/student_select_course.html',
                               courses=available_courses)
    finally:
        cursor.close()
        conn.close()

@course_bp.route('/student/courses')
@login_required
# 我的课程
def student_courses():
    # 获取学生已选课程
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT c.course_name, c.credit, c.course_type, sc.usual_score, sc.final_score, sc.score, sc.gpa
        FROM student_courses sc
        JOIN courses c ON sc.course_id = c.id
        WHERE sc.user_id = %s
    ''', (session['user_id'],))
    courses = cursor.fetchall()
    #  print(courses)  # 打印查询结果
    cursor.close()
    conn.close()

    return render_template('courses_management/student_courses.html', courses=courses)

# 创建 Excel表单
@course_bp.route('/student/export_courses')
@login_required
def export_courses():
    if session.get('role') != 'student':
        return redirect(url_for('index'))

    # 获取学生课程数据
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT c.course_name, c.credit, c.course_type, 
               sc.usual_score, sc.final_score, sc.score, sc.gpa
        FROM student_courses sc
        JOIN courses c ON sc.course_id = c.id
        WHERE sc.user_id = %s
    ''', (session['user_id'],))
    courses = cursor.fetchall()
    cursor.close()
    conn.close()

    # 创建Excel工作簿
    wb = Workbook()
    ws = wb.active
    ws.title = "我的课程成绩"

    # 添加表头
    headers = ['课程名称', '学分', '课程类型', '平时成绩(40%)', '期末成绩(60%)', '综合成绩', '绩点']
    ws.append(headers)

    # 添加数据行
    for course in courses:
        ws.append([
            course['course_name'],
            course['credit'],
            course['course_type'],
            course['usual_score'],
            course['final_score'],
            course['score'],
            course['gpa']
        ])

    # 设置列宽
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column].width = adjusted_width

    # 创建内存文件对象
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)

    # 生成文件名
    filename = f"{session['username']}_课程成绩_{datetime.now().strftime('%Y%m%d')}.xlsx"

    return send_file(
        excel_file,
        as_attachment=True,
        download_name=filename,
        mimetype='course_bplication/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@course_bp.route('/teacher/my_courses')
@login_required
def teacher_my_courses():
    """获取当前老师所授课程"""
    if session.get('role') != 'teacher':
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # 查询当前老师教授的已通过课程
    cursor.execute('''
        SELECT id, course_name, credit, department, course_type, capacity 
        FROM courses 
        WHERE teacher_name = %s AND status = '已通过'
    ''', (session['username'],))
    courses = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('courses_management/teacher_my_courses.html', courses=courses)


@course_bp.route('/teacher/course_students/<int:course_id>')
@login_required
def teacher_course_students(course_id):
    if session.get('role') != 'teacher':
        return redirect(url_for('index'))

    # 获取排序参数，设置默认值
    sort_by = request.args.get('sort', 'user_id')
    order = request.args.get('order', 'asc')

    # 验证排序字段防止SQL注入
    valid_columns = ['user_id', 'usual_score', 'final_score', 'total_score', 'gpa']
    if sort_by not in valid_columns:
        sort_by = 'user_id'

    # 验证排序方向
    order = 'ASC' if order.lower() == 'asc' else 'DESC'

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 验证课程权限
    cursor.execute('SELECT id FROM courses WHERE id = %s AND teacher_name = %s',
                   (course_id, session['username']))
    if not cursor.fetchone():
        return "无权查看此课程的学生", 403

    # 执行排序查询
    cursor.execute(f'''
        SELECT sc.id, sc.user_id, sc.student_name, 
               sc.usual_score, sc.final_score, 
               sc.usual_score * 0.4 + sc.final_score * 0.6 AS total_score,
               (sc.usual_score * 0.4 + sc.final_score * 0.6) / 10 - 5 AS gpa
        FROM student_courses sc
        WHERE sc.course_id = %s
        ORDER BY {sort_by} {order}
    ''', (course_id,))

    students = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('courses_management/teacher_course_students.html',
                           students=students,
                           course_id=course_id)

@course_bp.route('/teacher/update_scores', methods=['POST'])
@login_required
def teacher_update_scores():
    """更新学生成绩"""
    if session.get('role') != 'teacher':
        return jsonify({'success': False, 'message': '无权操作'})

    data = request.get_json()
    record_id = data.get('record_id')
    usual_score = data.get('usual_score')
    final_score = data.get('final_score')

    # 验证成绩是否为有效百分制整数
    try:
        usual_score = int(usual_score)
        final_score = int(final_score)
        if not (0 <= usual_score <= 100 and 0 <= final_score <= 100):
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': '成绩必须为0-100的整数'})

    # 计算总成绩和GPA
    total_score = usual_score * 0.4 + final_score * 0.6
    gpa = round(total_score / 10 - 5, 1)  # 保留一位小数

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE student_courses 
            SET usual_score = %s, final_score = %s, score = %s, gpa = %s
            WHERE id = %s
        ''', (usual_score, final_score, total_score, gpa, record_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

    return jsonify({
        'success': True,
        'total_score': total_score,
        'gpa': gpa
    })

# 已有课程列表
@course_bp.route('/admin/courses')
@login_required
def course_list():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT * FROM courses 
            WHERE status != '已驳回'
            ORDER BY status DESC, created_at DESC
        ''')
        courses = cursor.fetchall()
        return render_template('courses_management/course_list.html', courses=courses)
    finally:
        cursor.close()
        conn.close()

# 删除课程
@course_bp.route('/admin/delete_course/<int:course_id>', methods=['DELETE'])
@login_required
def delete_course(course_id):
    if session.get('role') != 'admin':
        return jsonify({'success': False, 'message': '无权操作'})

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 先检查是否有学生选课记录
        cursor.execute('SELECT 1 FROM student_courses WHERE course_id = %s', (course_id,))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': '该课程已有学生选课，不能删除'})

        cursor.execute('DELETE FROM courses WHERE id = %s', (course_id,))
        conn.commit()
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
