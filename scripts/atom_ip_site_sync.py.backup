import json
import os
from datetime import datetime

# 路径配置
WORKSPACE = "/Users/atom1983/.openclaw/workspace"
# 统一使用 history 作为数据源，确保回溯完整性
DATA_FILE = os.path.join(WORKSPACE, "memory/daily_briefing_history.json")
HTML_FILE = os.path.join(WORKSPACE, "core/atom_ip_platform/index.html")

def update_platform():
    if not os.path.exists(DATA_FILE):
        print("❌ 历史数据库不存在")
        return
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        history_data = json.load(f)
        data = history_data.get("history", [])
    
    # 提取最近的 15 条，按日期倒序
    sorted_data = sorted(data, key=lambda x: x.get('date', ''), reverse=True)[:15]
    
    insights_html = ""
    for i, item in enumerate(sorted_data):
        date_str = item.get('date', '').replace('-', '.')
        title = item.get('title', '无标题')
        source = item.get('source', 'Intel')
        category = item.get('category', '专利')
        point = item.get('point', '')
        insight = item.get('insight', '')
        
        # 使用 HTML <details> 实现原生折叠，无需复杂 JS，更稳定
        # 优化配色：深色文字 (slate-900) 确保高对比度
        insights_html += f"""
                    <details class="group border-l-2 border-slate-300 hover:border-blue-600 pl-4 py-3 transition-all bg-white/50 rounded-r-lg mb-3">
                        <summary class="list-none cursor-pointer">
                            <div class="flex items-center justify-between mb-1.5">
                                <span class="text-[10px] text-slate-500 font-bold font-mono">{date_str}</span>
                                <span class="text-[9px] bg-blue-100 text-blue-700 px-2 py-0.5 rounded font-bold uppercase">{category}</span>
                            </div>
                            <h5 class="text-[13px] font-bold text-slate-900 group-open:text-blue-600 transition-colors leading-snug pr-4 relative">
                                {title}
                                <i class="fa-solid fa-chevron-down absolute right-0 top-1 text-[10px] transition-transform group-open:rotate-180"></i>
                            </h5>
                        </summary>
                        <div class="mt-3 text-[11px] text-slate-600 leading-relaxed border-t border-slate-200/50 pt-3 space-y-2">
                            <p><strong class="text-slate-800">摘要:</strong> {point}</p>
                            <p><strong class="text-blue-700">洞察:</strong> {insight}</p>
                            <p class="text-[10px] text-slate-400 italic mt-2">来源: {source}</p>
                        </div>
                    </details>"""

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = "<!-- START_INSIGHTS -->"
    end_marker = "<!-- END_INSIGHTS -->"
    
    if start_marker in content and end_marker in content:
        new_content = content.split(start_marker)[0] + start_marker + insights_html + "\n                    " + end_marker + content.split(end_marker)[1]
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ 成功同步 {len(sorted_data)} 条动态 (已启用折叠显示与对比度修复)")
    else:
        print("❌ 未找到 HTML 标记位")

if __name__ == "__main__":
    update_platform()
