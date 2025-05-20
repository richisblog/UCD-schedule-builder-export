# 课程表转日历工具

这是一个Django项目，提供将课程表HTML文件转换为ICS日历文件的功能。

## 功能特点

- 用户可以上传课程表HTML文件
- 系统会解析HTML并提取课程信息
- 生成ICS日历文件，包含课程时间、地点、期末考试和重要日期
- 生成的ICS文件可以导入到各种日历应用中，如Google Calendar、Apple Calendar等
- 所有上传的HTML文件都安全存储在独立文件夹中

## 运行环境要求

- Python 3.8+
- Django 3.2+

## 安装步骤

1. 克隆此仓库或下载源代码
2. 进入项目根目录
3. 安装依赖包：
   ```
   pip install django
   ```
4. 执行数据库迁移（虽然本应用不使用数据库，但Django需要）：
   ```
   python manage.py migrate
   ```
5. 启动开发服务器：
   ```
   python manage.py runserver
   ```

## 使用说明

1. 访问 http://127.0.0.1:8000/ 
2. 上传课程表HTML文件
3. 系统会解析文件并生成ICS日历文件
4. 下载生成的ICS文件并导入到您的日历应用

## 文件保存说明

上传的HTML文件将被保存在项目的`uploads/html/`目录中，使用唯一标识符命名，确保您的隐私和数据安全。

## 项目结构

- `calculator/` - 项目配置目录
- `numcalc/` - 主应用目录
  - `views.py` - 视图函数
  - `forms.py` - 表单类
  - `templates/` - 模板文件
  - `final.py` - 课程表HTML解析脚本
- `uploads/html/` - HTML文件存储目录
- `media/` - 媒体文件目录，存放临时文件 