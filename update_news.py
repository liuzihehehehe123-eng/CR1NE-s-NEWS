import os
import re
import datetime
import google.generativeai as genai

# 配置 Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 检查是否为周六
is_saturday = datetime.datetime.now().weekday() == 5
sections = "今日热点、每周国内、每周国际" if is_saturday else "今日热点"

prompt = f"""
你现在是 CR1NE's NEWS 的主编。请生成{sections}板块的内容。
要求：
1. 每日热点放在 <div id="daily">，国内放在 <div id="domestic">，国际放在 <div id="intl">。
2. 每一条新闻格式：
   - <div class="bg-white rounded-3xl p-6 mb-6 shadow-sm border border-slate-100">
     <h3 class="font-bold text-xl mb-3 text-slate-800 tracking-tight">【中文标题 / English Title】</h3>
     <p class="text-slate-600 mb-4 leading-relaxed">中文摘要（150字）</p>
     <p class="text-slate-400 italic text-sm border-l-4 border-indigo-100 pl-4 leading-loose" onmouseup="quickTranslate(event)">英文报道内容（确保地道专业，适合深度阅读）</p>
   </div>
3. 仅返回 HTML 标签，不带任何 Markdown 标记。
"""

try:
    response = model.generate_content(prompt)
    new_content = response.text
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r'<main id="content".*?>(.*?)</main>'
    replacement = f'<main id="content" class="max-w-4xl mx-auto p-4 mt-2 min-h-[70vh]">{new_content}</main>'
    updated_html = re.sub(pattern, replacement, content, flags=re.DOTALL)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_html)
except Exception as e:
    print(f"Update failed: {e}")
