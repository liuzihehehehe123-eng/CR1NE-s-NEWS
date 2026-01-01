import os
import re
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = """
作为 CR1NE's NEWS 主编，生成今日热点。
格式要求：
<div id="daily" class="news-section active">
    <div class="bg-white rounded-3xl p-6 mb-6 shadow-sm border border-slate-100">
        <h3 class="font-bold text-xl mb-3 text-slate-800">【标题 / Title】</h3>
        <p class="text-slate-600 mb-4">中文摘要</p>
        <p class="text-slate-400 italic text-sm border-l-4 border-indigo-100 pl-4" onmouseup="quickTranslate(event)">English description here.</p>
    </div>
</div>
<div id="domestic" class="news-section"></div>
<div id="intl" class="news-section"></div>
"""

try:
    response = model.generate_content(prompt)
    new_html = response.text.replace("```html", "").replace("```", "").strip()
    
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 这里的 ID 必须匹配 index.html 里的 main id="content"
    pattern = r'(<main id="content".*?>)(.*?)(</main>)'
    replacement = rf'\1\n{new_html}\n\3'
    updated_html = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_html)
    print("Update successful")
except Exception as e:
    print(f"Error: {e}")
