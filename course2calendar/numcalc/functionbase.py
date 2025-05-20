from datetime import datetime
from bs4 import BeautifulSoup
import re

def extract_student_info(content):
    soup = BeautifulSoup(content, 'html.parser')
        # 查找包含学生信息的div标签
    student_info_div = soup.find('div', id='student_name_id')
    if student_info_div:
            # 获取div标签内的文本内容
        student_info_text = student_info_div.get_text(strip=True)

            # 使用正则表达式提取姓名和学号
            # 这个正则表达式假设姓名和学号由 " - " 分隔
        match = re.match(r'^(.*?) - (\d+)$', student_info_text)
        if match:
            name = match.group(1).strip()
            student_id = match.group(2).strip()
            return name, student_id

def extract_term_code_from_input(html_content):
    """
    从 HTML 中提取 <input name="termCode" value="..."> 的值
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    tag = soup.find('input', {'name': 'termCode'})
    if tag and tag.has_attr('value'):
        return tag['value']
    return "UNKNOWN"

def find_string_between(a, b, c):
    start_b = a.find(b)
    if start_b == -1:
      return ""  # 如果没有找到 b，返回空字符串

    # 计算 b 结束后的位置
    start_substring = start_b + len(b)

    # 从 b 结束后的位置开始查找 c
    start_c = a.find(c, start_substring)
    if start_c == -1:
      return ""  # 如果在 b 之后没有找到 c，返回空字符串

    # 提取并返回 b 和 c 之间的子字符串
    return a[start_substring:start_c]

def find_registered_waitlisted_course_id(text):
    in_courses=[]
    for line in text.splitlines():
        if (find_string_between(line,'CourseDetails.t','.REGISTRATION_STATUS = "Registered"')) != "":
            in_courses.append(find_string_between(line, 'CourseDetails.t', '.REGISTRATION_STATUS = "Registered"'))
        elif find_string_between(line,'CourseDetails.t','.REGISTRATION_STATUS = "Waitlisted"') != "":
            in_courses.append(find_string_between(line, 'CourseDetails.t', '.REGISTRATION_STATUS = "Waitlisted"'))
    return in_courses

def find_crn(text):
    return find_string_between(text, "\"CRN\":\"", "\"")

def find_course_name(text):
    return find_string_between(text, "\"TITLE\":\"", "\"")

def find_subject_code(text):
    return find_string_between(text, "\"SUBJECT_CODE\":\"", "\"")

def find_course_number(text):
    return find_string_between(text, "\"COURSE_NUMBER\":\"", "\"")

def find_section_number(text):
    return find_string_between(text, "\"SECTION_NUMBER\":\"", "\"")

def find_final(text):
    orgtime = find_string_between(text, "\"FINAL_EXAM_STARTDATE\":", "\n")
    if orgtime == "null":
        return "null"
    yr=find_string_between(orgtime, "(", ",")
    mth=find_string_between(orgtime, "("+yr+",", ",")
    dy=find_string_between(orgtime, "("+yr+","+mth+",", ",")
    hour=find_string_between(orgtime, "("+yr+","+mth+","+dy+",", ",")
    mnt=find_string_between(orgtime, "("+yr+","+mth+","+dy+","+hour+",", ",")
    finaltime=datetime(int(yr),int(mth)+1,int(dy),int(hour),int(mnt),0)
    return finaltime.strftime("%Y-%m-%d %H:%M:%S")

def find_units(text):
    return find_string_between(text, "\"UNITS\":\"", "\"")

def find_meeting_times(text):
    org_meeting = find_string_between(text, "\"MEETINGS\":[", "]")
    meeting_number=org_meeting.count("{")
    return meeting_number

def  find_meetings(text):
    org_meeting = find_string_between(text, "\"MEETINGS\":", "]")
    return org_meeting


def insert_registered_or_waitlisted_blocks(html_text):
    """
    提取 CourseDetails.tXXXX = {...}; 的 JS 块中，状态为 Registered 或 Waitlist 的那些块
    :param html_text: 原始 HTML 内容
    :return: list[str]，符合条件的 script 块代码
    """
    pattern = r'CourseDetails\.(t\d+)\s*=\s*{.*?};'
    matches = re.finditer(pattern, html_text, re.DOTALL)
    student_name,student_id = extract_student_info(html_text)
    termid=extract_term_code_from_input(html_text)
    print(student_name)
    print(student_id)
    parsed_course = []
    for match in matches:
        js_code = match.group(0)
       # print(js_code)
        if re.search(r'REGISTRATION_STATUS"\s*:\s*"?(Registered|Waitlist)"?', js_code):
            this_course=js_code
            parsed_course.append(this_course)
            readd=find_meeting_times(this_course)
            #print(readd)
            for i in range(0,readd):
                print("执行",i,"次")
                print("-----------------------------------------------------------------------------------------")

    return {
        "student_name": student_name,
        "student_id": student_id,
        "semester": termid,
        "courses": find_registered_waitlisted_course_id(html_text)
    }

