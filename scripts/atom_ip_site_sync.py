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
    
    # 提取最近的 10 条
    sorted_data = sorted(data, key=lambda x: x.get('date', ''), reverse=True)[:10]
    
    insights_html = ""
    for item in sorted_data:
        date_str = item.get('date', '').replace('-', '.')
        title = item.get('title', '无标题')
        source = item.get('source', 'Intel')
        category = item.get('category', '专利')
        
        # 优化后的列表项：带分类标签和更清晰的排版
        insights_html += f"""
                    <div class="group border-l-2 border-slate-700 hover:border-blue-500 pl-4 py-2 transition-all">
                        <div class="flex items-center justify-between mb-1">
                            <span class="text-[10px] text-slate-500 font-mono">{date_str}</span>
                            <span class="text-[9px] bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded uppercase tracking-tighter">{category}</span>
                        </div>
                        <h5 class="text-xs font-semibold text-slate-200 group-hover:text-blue-400 transition-colors leading-relaxed cursor-pointer" title="{title}">{title}</h5>
                        <p class="text-[10px] text-slate-500 mt-1 line-clamp-2 italic">来源: {source}</p>
                    </div>"""

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = "<!-- START_INSIGHTS -->"
    end_marker = "<!-- END_INSIGHTS -->"
    
    if start_marker in content and end_marker in content:
        new_content = content.split(start_marker)[0] + start_marker + insights_html + "\n                    " + end_marker + content.split(end_marker)[1]
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ 成功同步 {len(sorted_data)} 条动态")
    else:
        print("❌ 未找到 HTML 标记位")

if __name__ == "__main__":
    update_platform()
