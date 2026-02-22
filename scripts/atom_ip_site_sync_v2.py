import json
import os
from datetime import datetime
from collections import defaultdict

# 路径配置
WORKSPACE = "/Users/atom1983/.openclaw/workspace"
DATA_FILE = os.path.join(WORKSPACE, "memory/daily_briefing_history.json")
HTML_FILE = os.path.join(WORKSPACE, "core/atom_ip_platform/index.html")

def update_platform():
    if not os.path.exists(DATA_FILE):
        print("❌ 历史数据库不存在")
        return
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        history_data = json.load(f)
        data = history_data.get("history", [])
    
    # 按日期分组
    date_groups = defaultdict(list)
    for item in data:
        date = item.get('date', '无日期')
        date_groups[date].append(item)
    
    # 按日期倒序排序
    sorted_dates = sorted(date_groups.keys(), reverse=True)
    
    insights_html = ""
    
    # 为每个日期创建外层折叠面板
    for date in sorted_dates:
        date_str = date.replace('-', '.')
        items = date_groups[date]
        
        # 外层日期折叠面板
        insights_html += f"""
                    <!-- 日期分组: {date} -->
                    <details class="group mb-6 bg-white/80 rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                        <summary class="list-none cursor-pointer bg-gradient-to-r from-slate-50 to-slate-100 hover:from-blue-50 hover:to-blue-100 p-5 transition-all">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center space-x-3">
                                    <div class="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center">
                                        <span class="text-sm font-bold">{date.split('-')[2]}</span>
                                    </div>
                                    <div>
                                        <h4 class="font-bold text-slate-900 group-open:text-blue-700 transition-colors">
                                            欧洲知产日报 {date_str}
                                            <span class="ml-2 text-xs bg-blue-600 text-white px-2 py-0.5 rounded-full">{len(items)}条动态</span>
                                        </h4>
                                        <p class="text-xs text-slate-500 mt-1">
                                            {get_month_name(date.split('-')[1])} {date.split('-')[0]}, 第{get_week_number(date)}周
                                        </p>
                                    </div>
                                </div>
                                <div class="text-slate-400 group-open:rotate-180 transition-transform">
                                    <i class="fa-solid fa-chevron-down"></i>
                                </div>
                            </div>
                        </summary>
                        <div class="p-4 pt-2 space-y-4 max-h-[600px] overflow-y-auto custom-scrollbar">
                """
        
        # 内层动态列表 - 使用简单列表，避免嵌套折叠
        for i, item in enumerate(items, 1):
            title = item.get('title', '无标题')
            source = item.get('source', 'Intel')
            category = item.get('category', '专利')
            point = item.get('point', '')
            insight = item.get('insight', '')
            
            # 动态卡片，无嵌套折叠
            insights_html += f"""
                            <div class="bg-white rounded-lg border border-slate-200 p-4 hover:border-blue-300 transition-colors">
                                <div class="flex items-center justify-between mb-2">
                                    <span class="text-[10px] font-bold bg-slate-100 text-slate-700 px-2 py-0.5 rounded-full uppercase">{category}</span>
                                    <span class="text-[10px] text-slate-400">#{i}</span>
                                </div>
                                <h5 class="text-[13px] font-bold text-slate-900 mb-2 leading-tight">{title}</h5>
                                <div class="text-[11px] text-slate-600 space-y-1.5">
                                    <p><strong class="text-slate-800">摘要:</strong> {point}</p>
                                    <p><strong class="text-blue-700">洞察:</strong> {insight}</p>
                                </div>
                                <div class="mt-3 flex justify-between items-center">
                                    <span class="text-[10px] text-slate-400 italic">来源: {source}</span>
                                    <a href="{item.get('url', '#')}" target="_blank" class="text-[10px] text-blue-600 hover:text-blue-800 font-bold flex items-center">
                                        原文链接 <i class="fa-solid fa-external-link-alt ml-1 text-[8px]"></i>
                                    </a>
                                </div>
                            </div>
                """
        
        # 关闭日期面板
        insights_html += """
                        </div>
                    </details>
                """
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = "<!-- START_INSIGHTS -->"
    end_marker = "<!-- END_INSIGHTS -->"
    
    if start_marker in content and end_marker in content:
        new_content = content.split(start_marker)[0] + start_marker + insights_html + "\n                    " + end_marker + content.split(end_marker)[1]
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ 成功同步 {len(data)} 条动态，按 {len(sorted_dates)} 个日期分组折叠显示")
    else:
        print("❌ 未找到 HTML 标记位")

def get_month_name(month_num):
    """获取月份名称"""
    months = ['', '一月', '二月', '三月', '四月', '五月', '六月', 
              '七月', '八月', '九月', '十月', '十一月', '十二月']
    try:
        return months[int(month_num)]
    except:
        return month_num

def get_week_number(date_str):
    """计算是一年中的第几周（简化版）"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        week_num = date_obj.isocalendar()[1]
        return week_num
    except:
        return ""

if __name__ == "__main__":
    update_platform()