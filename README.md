# Course2Calendar - 课程表转日历工具

这是一个简洁的Django应用，帮助学生轻松地将课程表HTML文件转换为标准ICS日历文件。

## 功能特点

- 用户可以上传课程表HTML文件
- 系统会解析HTML并提取课程信息
- 生成ICS日历文件，包含课程时间、地点、期末考试和重要日期
- 生成的ICS文件可以导入到各种日历应用中，如Google Calendar、Apple Calendar等
- 上传的HTML文件使用学生姓名和学号进行加密命名，确保隐私安全

## 运行环境要求

- Python 3.8+
- Django 3.2+
- cryptography库

## 安装步骤

1. 克隆此仓库或下载源代码
2. 进入项目根目录
3. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```
4. 执行数据库迁移：
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

## 文件加密说明

系统从上传的HTML文件中提取学生姓名和学号信息，并使用这些信息创建加密文件名：

1. 提取格式: `student_name|student_id`
2. 使用Fernet对称加密算法加密
3. 加密后转换为URL安全的Base64编码
4. 保存到uploads/html/目录

## 文件名解密工具

管理员可以使用文件名解密工具还原学生信息：

1. 访问 http://127.0.0.1:8000/decrypt-tool/
2. 输入加密的文件名
3. 系统会解密并显示对应的学生姓名和学号
4. 工具还提供已上传文件列表，方便管理

## 加密解密原理

1. **加密流程**:
   - 合并学生姓名和学号为一个字符串 (`student_name|student_id`)
   - 使用Fernet对称加密进行加密
   - 使用URL安全的Base64编码转换为文件安全的字符串

2. **解密流程**:
   - 将文件名通过Base64解码
   - 使用相同的Fernet密钥解密
   - 分离学生姓名和学号

3. **密钥管理**:
   - 密钥自动生成并保存在 `main/secret.key` 文件中
   - 系统会自动检测密钥文件并使用相同的密钥

## 项目结构

- `calculator/` - 项目配置目录
- `main/` - 工具函数目录
  - `functionbase.py` - 学生信息提取和加密解密功能
- `numcalc/` - 主应用目录
  - `views.py` - 视图函数
  - `forms.py` - 表单类
  - `templates/` - 模板文件
  - `final.py` - 课程表HTML解析脚本
- `uploads/html/` - HTML文件加密存储目录
- `media/` - 媒体文件目录，存放临时文件 