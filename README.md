# DHY 学生教务管理系统

基于 Python Flask 构建的多角色学生教务管理系统，支持学生、教师、管理员三种角色，涵盖课程管理、作业管理、请假审批等核心教务功能。

## 技术栈

- **后端**: Python 3, Flask
- **数据库**: MySQL (mysql-connector-python)
- **模板引擎**: Jinja2
- **前端**: HTML, CSS
- **密码加密**: bcrypt
- **文件处理**: Pillow (头像), openpyxl (Excel 导出), reportlab

## 系统架构

```
├── app.py                  # 应用入口，路由注册
├── db.py                  # MySQL 数据库连接配置
├── login.py               # 登录/注册/密码管理
├── users.py               # 用户信息管理(学生/教师/管理员)
├── courses.py             # 课程管理(选课/成绩/导出)
├── assignments.py          # 作业管理(布置/提交/批改)
├── apply.py               # 申请(学生请假/教师开课)
├── approval.py            # 审批(请假审批/课程审批)
├── migrate_passwords.py   # 密码迁移工具
├── requirements.txt       # Python 依赖
├── sql/                   # 数据库建表脚本
├── templates/             # Jinja2 HTML 模板
│   ├── login/            # 登录/注册/改密
│   ├── index/            # 各角色主页
│   ├── profile/          # 个人信息页
│   ├── edit_profile/     # 编辑信息页
│   ├── courses_management/ # 课程管理
│   ├── assignment/       # 作业管理
│   ├── apply/            # 申请页面
│   ├── approval/         # 审批页面
│   └── admin/            # 管理员后台
└── static/               # 静态资源
    ├── css/              # 样式文件
    ├── images/           # 图片资源
    └── uploads/          # 用户上传(头像/作业)
```

## 角色与功能

### 学生 (Student)
- 注册账号、登录、修改密码
- 查看和编辑个人资料、上传头像
- 浏览可选课程并选课
- 查看已选课程及成绩
- 导出课程成绩为 Excel
- 查看、提交和重新提交作业
- 提交请假申请并查看审批状态

### 教师 (Teacher)
- 查看和编辑个人资料、上传头像
- 申请开设新课程（需管理员审批）
- 查看所授课程及选课学生名单
- 录入和更新学生成绩（平时成绩 40% + 期末成绩 60%），自动计算 GPA
- 发布作业、查看提交情况、批改评分
- 查看课程申请状态

### 管理员 (Admin)
- 查看和编辑个人资料、上传头像
- 审批教师开课申请
- 审批学生请假申请（批准/驳回/销假）
- 查看所有用户列表
- 添加/编辑/删除用户
- 查看和管理课程列表

## 快速开始

### 前置条件

- Python 3.8+
- MySQL 数据库

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/LuvNarcisuss/DHY_students_management_system.git
cd DHY_students_management_system
```

1. **安装依赖**

```bash
pip install -r requirements.txt
```

1. **配置数据库**

在 `db.py` 中修改 MySQL 连接配置：

```python
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'student_management'
}
```

1. **初始化数据库**

执行 `sql/` 目录下的建表脚本创建数据库表：

```bash
mysql -u your_username -p < sql/student_management_users.sql
mysql -u your_username -p < sql/student_management_courses.sql
mysql -u your_username -p < sql/student_management_assignments.sql
mysql -u your_username -p < sql/student_management_student_leave.sql
mysql -u your_username -p < sql/student_management_homework_submissions.sql
mysql -u your_username -p < sql/student_management_student_courses.sql
```

1. **运行应用**

```bash
python app.py
```

访问 `http://localhost:5000` 进入系统。

## 数据库表结构

- **users** — 用户表（学生/教师/管理员）
- **courses** — 课程表（含容量、状态、审批意见）
- **student_courses** — 学生选课记录表（含成绩、绩点）
- **assignments** — 作业表
- **homework_submissions** — 作业提交表
- **student_leave** — 学生请假表（含审批状态）

## 安全特性

- 密码使用 bcrypt 哈希存储
- 登录角色验证，防止跨角色访问
- 基于 session 的登录状态管理
- 请求参数校验（成绩范围、时间合理性等）
- SQL 参数化查询，防止注入
- 各接口均有角色权限校验
- 作业提交权限验证（仅已选课学生可提交）
- 课程管理权限隔离（教师只能操作自己的课程）

## 项目信息

- 作者: [LuvNarcisuss](https://github.com/LuvNarcisuss)
