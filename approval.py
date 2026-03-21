from flask import (Blueprint, render_template, request, redirect, url_for,
                   jsonify, session)
from db import get_db_connection
from login import login_required

approval_bp = Blueprint('approval', __name__, template_folder='templates/approval')

# 管理员审核请假
@approval_bp.route('/admin/leave_approval')
@login_required
def admin_leave_approval():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT lr.*, u.department, u.classname 
        FROM student_leave lr
        JOIN users u ON lr.student_id = u.id
        WHERE lr.status = '待通过' OR lr.status = '待销假'
        ORDER BY lr.created_at
    ''')
    leaves = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('approval/admin_leave_approval.html', leaves=leaves)

# 管理员处理请假申请
@approval_bp.route('/admin/approve_leave/<int:leave_id>', methods=['POST'])
@login_required
def admin_approve_leave(leave_id):
    """批准请假，状态改为待销假"""
    if session.get('role') != 'admin':
        return jsonify({'success': False, 'message': '无权操作'}), 403

    try:
        # 获取请求数据
        data = request.get_json() if request.is_json else request.form
        comment = data.get('comment', '')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 先检查请假记录是否存在且状态正确
        cursor.execute('''
                       SELECT id, status
                       FROM student_leave
                       WHERE id = %s
                         AND status = '待通过'
                       ''', (leave_id,))
        leave = cursor.fetchone()

        if not leave:
            return jsonify({
                'success': False,
                'message': '请假记录不存在或状态已变更'
            }), 400

        # 更新状态
        cursor.execute('''
                       UPDATE student_leave
                       SET status        = '待销假',
                           admin_comment = %s
                       WHERE id = %s
                       ''', (comment, leave_id))

        conn.commit()
        return jsonify({
            'success': True,
            'message': '已批准，等待销假',
            'new_status': '待销假'
        })

    except Exception as e:
        conn.rollback()
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
        }), 500

    finally:
        cursor and cursor.close()
        conn and conn.close()


@approval_bp.route('/admin/reject_leave/<int:leave_id>', methods=['POST'])
@login_required
def admin_reject_leave(leave_id):
    """驳回请假申请"""
    if session.get('role') != 'admin':
        return jsonify({'success': False, 'message': '无权操作'}), 403

    try:
        # 获取请求数据
        data = request.get_json() if request.is_json else request.form
        comment = data.get('comment', '')

        if not comment:
            return jsonify({
                'success': False,
                'message': '请填写驳回原因'
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 先检查请假记录是否存在且状态正确
        cursor.execute('''
                       SELECT id, status
                       FROM student_leave
                       WHERE id = %s
                         AND status = '待通过'
                       ''', (leave_id,))
        leave = cursor.fetchone()

        if not leave:
            return jsonify({
                'success': False,
                'message': '请假记录不存在或状态已变更'
            }), 400

        # 更新状态
        cursor.execute('''
                       UPDATE student_leave
                       SET status        = '已驳回',
                           admin_comment = %s
                       WHERE id = %s
                       ''', (comment, leave_id))

        conn.commit()
        return jsonify({
            'success': True,
            'message': '已驳回请假申请',
            'new_status': '已驳回'
        })

    except Exception as e:
        conn.rollback()
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
        }), 500

    finally:
        cursor and cursor.close()
        conn and conn.close()

@approval_bp.route('/admin/complete_leave/<int:leave_id>', methods=['POST'])
@login_required
def admin_complete_leave(leave_id):
    """完成销假，状态改为已销假"""
    if session.get('role') != 'admin':
        return jsonify({'success': False, 'message': '无权操作'})

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE student_leave 
            SET status = '已销假'
            WHERE id = %s AND status = '待销假'
        ''', (leave_id,))
        conn.commit()
        return jsonify({'success': True, 'message': '销假完成'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()



# 管理员审核课程
@approval_bp.route('/admin/course_approval')
@login_required
def admin_course_approval():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT * FROM courses 
        WHERE status = '待审批'
        ORDER BY id
    ''')
    courses = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('approval/admin_course_approval.html', courses=courses)


# 管理员处理课程申请
@approval_bp.route('/admin/approve_course/<int:course_id>', methods=['POST'])
@login_required
def admin_approve_course(course_id):
    if session.get('role') != 'admin':
        return jsonify({'success': False, 'message': '无权操作'}), 403

    try:
        # 获取请求数据
        data = request.get_json() if request.is_json else request.form
        action = data.get('action')
        comment = data.get('comment', '')

        if action not in ['批准', '驳回']:
            return jsonify({'success': False, 'message': '无效操作'}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 检查课程状态
        cursor.execute('SELECT status FROM courses WHERE id = %s', (course_id,))
        course = cursor.fetchone()

        if not course:
            return jsonify({'success': False, 'message': '课程不存在'}), 404
        if course['status'] != '待审批':
            return jsonify({
                'success': False,
                'message': f'课程当前状态为{course["status"]}，无法操作'
            }), 400

        # 更新状态
        new_status = '已通过' if action == '批准' else '已驳回'
        cursor.execute('''
                       UPDATE courses
                       SET status        = %s,
                           admin_comment = %s
                       WHERE id = %s
                       ''', (new_status, comment, course_id))

        conn.commit()
        return jsonify({
            'success': True,
            'message': f'课程已{action}',
            'new_status': new_status
        })

    except Exception as e:
        conn.rollback()
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
        }), 500

    finally:
        cursor and cursor.close()
        conn and conn.close()