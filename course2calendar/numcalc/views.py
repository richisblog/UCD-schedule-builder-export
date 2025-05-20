import os
import subprocess
import shutil
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
import uuid

from .forms import HTMLFileForm


def upload_html(request):
    """处理HTML文件上传并生成日历文件"""
    if request.method == 'POST':
        form = HTMLFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 获取上传的文件
            html_file = request.FILES['file']
            
            try:
                # 确保媒体目录和上传目录存在
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                os.makedirs(settings.HTML_UPLOAD_DIR, exist_ok=True)
                
                # 生成唯一文件名，保存用户上传的HTML
                unique_id = str(uuid.uuid4())
                original_filename = html_file.name
                filename_base, filename_ext = os.path.splitext(original_filename)
                safe_filename = f"{unique_id}{filename_ext}"
                
                # 保存原始HTML到上传目录
                html_file_path = os.path.join(settings.HTML_UPLOAD_DIR, safe_filename)
                with open(html_file_path, 'wb') as f:
                    for chunk in html_file.chunks():
                        f.write(chunk)
                
                # 创建工作文件的临时副本
                temp_html_path = os.path.join(settings.MEDIA_ROOT, 'cindy.html')
                shutil.copy2(html_file_path, temp_html_path)
                
                # 复制final.py到媒体目录
                final_script_path = os.path.join(os.path.dirname(__file__), 'final.py')
                temp_script_path = os.path.join(settings.MEDIA_ROOT, 'final.py')
                
                with open(final_script_path, 'r', encoding='utf-8') as src_file:
                    with open(temp_script_path, 'w', encoding='utf-8') as dst_file:
                        dst_file.write(src_file.read())
                
                # 执行脚本生成ICS文件
                os.chdir(settings.MEDIA_ROOT)
                subprocess.run(['python', 'final.py'], check=True)
                
                # 获取生成的ICS文件
                ics_file_path = temp_html_path + '.ics'
                
                # 检查文件是否生成
                if not os.path.exists(ics_file_path):
                    messages.error(request, '生成日历文件失败')
                    return redirect('upload_html')
                
                # 生成有意义的输出文件名
                output_filename = f"{filename_base}_calendar.ics"
                
                # 读取ICS文件并返回给用户
                with open(ics_file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='text/calendar')
                    response['Content-Disposition'] = f'attachment; filename="{output_filename}"'
                    
                    # 清理临时文件
                    try:
                        os.remove(temp_html_path)
                        os.remove(ics_file_path)
                        os.remove(temp_script_path)
                    except:
                        pass
                    
                    return response
                
            except Exception as e:
                messages.error(request, f'处理文件时出错: {str(e)}')
                return redirect('upload_html')
    else:
        form = HTMLFileForm()
    
    return render(request, 'numcalc/upload_html.html', {'form': form})


def home(request):
    """主页视图"""
    return redirect('upload_html')
