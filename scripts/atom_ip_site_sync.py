import json
import os
from datetime import datetime

# 路径配置
WORKSPACE = "/Users/atom1983/.openclaw/workspace"
DATA_FILE = os.path.join(WORKSPACE, "memory/strictly_verified_briefing.json")
HTML_FILE = os.path.join(WORKSPACE, "core/atom_ip_platform/index.html")

def update_platform():
    if not os.path.exists(DATA_FILE):
        print("❌ 数据文件不存在")
        return
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取最近的 15 条（增加展示数量，覆盖更多日期）
    sorted_data = sorted(data, key=lambda x: x.get('date', ''), reverse=True)[:15]
    
    insights_html = ""
    for item in sorted_data:
        date_str = item.get('date', '').replace('-', '.')
        title = item.get('title', '无标题')
        source = item.get('source', 'Intel')
        category = item.get('category', '专利')
        
        # 修复配色：text-slate-900 (深黑) 确保在 bg-slate-100 上清晰
        insights_html += f"""
                    <div class="group border-l-2 border-slate-300 hover:border-blue-600 pl-5 py-3 transition-all bg-white/50 rounded-r-lg mb-2">
                        <div class="flex items-center justify-between mb-1.5">
                            <span class="text-[10px] text-slate-500 font-bold font-mono tracking-tighter">{date_str}</span>
                            <span class="text-[9px] bg-blue-100 text-blue-700 px-2 py-0.5 rounded font-bold uppercase">{category}</span>
                        </div>
                        <h5 class="text-[13px] font-bold text-slate-900 group-hover:text-blue-600 transition-colors leading-snug cursor-pointer" title="{title}">{title}</h5>
                        <p class="text-[11px] text-slate-500 mt-2 line-clamp-2 italic font-medium">来源: {source}</p>
                    </div>"""

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = "<!-- START_INSIGHTS -->"
    end_marker = "<!-- END_INSIGHTS -->"
    
    if start_marker in content and end_marker in content:
        new_content = content.split(start_marker)[0] + start_marker + insights_html + "\n                    " + end_marker + content.split(end_marker)[1]
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ 成功同步 {len(sorted_data)} 条动态 (已修复配色与可读性)")
    else:
        print("❌ 未找到 HTML 标记位")

if __name__ == "__main__":
    update_platform()
