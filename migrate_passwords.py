from db import get_db_connection
import bcrypt
import sys

def migrate_passwords():
    # 将数据库中所有用户的明文密码加密为bcrypt哈希密码
    try:
        # 获取数据库连接
        conn = get_db_connection()
        if not conn:
            print("数据库连接失败")
            return False

        cursor = conn.cursor(dictionary=True)

        # 查询所有用户
        cursor.execute('SELECT id, username, password FROM users')
        users = cursor.fetchall()

        if not users:
            print("没有找到需要加密的用户")
            return True

        print(f"找到 {len(users)} 个需要检查的用户")
        migrated_count = 0

        # 遍历每个用户
        for user in users:
            user_id = user['id']
            current_password = user['password']

            # 检查密码是否已经是哈希格式(bcrypt哈希以$2a$, $2b$或$2y$开头)
            if current_password.startswith(('$2a$', '$2b$', '$2y$')):
                print(f"用户 {user['username']} 的密码已经是哈希格式，跳过")
                continue

            # 对明文密码进行哈希处理
            try:
                hashed_password = bcrypt.hashpw(current_password.encode('utf-8'), bcrypt.gensalt())
                hashed_password_str = hashed_password.decode('utf-8')

                # 更新数据库
                update_cursor = conn.cursor()
                update_cursor.execute(
                    'UPDATE users SET password = %s WHERE id = %s',
                    (hashed_password_str, user_id)
                )
                conn.commit()
                update_cursor.close()

                migrated_count += 1
                print(f"已加密用户 {user['username']} 的密码")

            except Exception as e:
                print(f"加密用户 {user['username']} 时出错: {str(e)}")
                conn.rollback()
                continue

        # 完成统计
        print(f"\n加密完成！共处理了 {migrated_count}/{len(users)} 个用户")
        return True

    except Exception as e:
        print(f"加密过程中发生错误: {str(e)}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":

    # 确认操作
    confirm = input("确定要继续吗？(yes/no): ").strip().lower()
    if confirm != 'yes':
        print("操作已取消")
        sys.exit(0)

    # 执行加密
    success = migrate_passwords()

    if success:
        print("密码加密成功完成！")
        sys.exit(0)
    else:
        print("密码加密失败，请检查错误信息")
        sys.exit(1)