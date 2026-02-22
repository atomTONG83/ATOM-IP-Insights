import json
import os
from datetime import datetime

# 路径配置
WORKSPACE = "/Users/atom1983/.openclaw/workspace"
DATA_FILE = os.path.join(WORKSPACE, "memory/strictly_verified_briefing.json")
HTML_FILE = os.path.join(WORKSPACE, "core/atom_ip_platform/index.html")

def update_platform():
    # 1. 读取数据
    if not os.path.exists(DATA_FILE):
        print("❌ 数据文件不存在")
        return
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 2. 提取最近的 5 条
    # 数据格式：{"date": "2026-02-22", "title_cn": "...", "summary_cn": "...", ...}
    # 假设数据是按日期排序的，或者我们需要排序
    sorted_data = sorted(data, key=lambda x: x.get('date', ''), reverse=True)[:5]
    
    insights_html = ""
    for item in sorted_data:
        date_str = item.get('date', '').replace('-', '.')
        title = item.get('title_cn', '无标题')
        summary = item.get('summary_cn', '')[:60] + "..."
        
        insights_html += f"""
                    <div class="flex items-start">
                        <span class="text-slate-400 text-xs font-mono pt-1 w-24">{date_str}</span>
                        <div class="flex-1 ml-4">
                            <h5 class="font-semibold hover:text-blue-600 cursor-pointer">{title}</h5>
                            <p class="text-xs text-slate-500 mt-1">{summary}</p>
                        </div>
                    </div>"""

    # 3. 注入 HTML
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = "<!-- START_INSIGHTS -->"
    end_marker = "<!-- END_INSIGHTS -->"
    
    if start_marker in content and end_marker in content:
        new_content = content.split(start_marker)[0] + start_marker + insights_html + "\n                    " + end_marker + content.split(end_marker)[1]
        
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ 成功同步 {len(sorted_data)} 条动态到 Atom IP Platform")
    else:
        print("❌ 未找到 HTML 标记位")

if __name__ == "__main__":
    update_platform()
