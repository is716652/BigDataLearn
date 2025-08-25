#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import json
import os

def regenerate_shell_content():
    """重新生成Shell脚本模块的学习内容"""
    # 确保在backend目录下运行
    if not os.path.exists('bigdata_learning.db'):
        os.chdir('backend')
    
    conn = sqlite3.connect('bigdata_learning.db')
    cursor = conn.cursor()
    
    try:
        # 获取Shell脚本模块的topic IDs
        print("获取Shell脚本模块的主题...")
        cursor.execute("SELECT id, ord FROM topics WHERE module_id = 2 ORDER BY ord")
        topics = cursor.fetchall()
        
        if not topics:
            print("未找到Shell脚本模块的主题")
            return
        
        # 删除Shell脚本模块的旧内容
        print("删除Shell脚本模块的旧内容...")
        cursor.execute("DELETE FROM contents WHERE topic_id IN (SELECT id FROM topics WHERE module_id = 2)")
        
        # Shell脚本模块的新内容定义
        shell_contents = [
            {
                'title': 'Shell脚本入门与环境配置',
                'theory': '''Shell脚本是Linux系统管理和自动化的重要工具。Shell作为命令行解释器，可以执行系统命令、处理文件和管理进程。常见的Shell包括bash、zsh、csh等，其中bash是最广泛使用的。\n\n**Shell脚本特点：**\n• 解释执行，无需编译\n• 语法简单，易于学习\n• 与系统命令紧密集成\n• 适合自动化任务\n\n**脚本基础：**\n• 脚本文件以#!/bin/bash开头（Shebang）\n• 文件需要执行权限：chmod +x script.sh\n• 执行方式：./script.sh 或 bash script.sh''',
                'code': '''#!/bin/bash\n# 第一个Shell脚本\necho "Hello, Shell World!"\n\n# 检查Shell类型\necho "当前Shell: $SHELL"\necho "Shell版本: $BASH_VERSION"\n\n# 脚本信息\necho "脚本名称: $0"\necho "执行时间: $(date)"\necho "当前用户: $USER"\necho "工作目录: $PWD"\n\n# 设置执行权限并运行\n# chmod +x hello.sh\n# ./hello.sh''',
                'case': '''**案例：系统信息收集脚本**\n\n创建一个收集系统基本信息的脚本：\n\n```bash\n#!/bin/bash\n# 文件名：system_info.sh\n\necho "=== 系统信息收集 ==="\necho "主机名: $(hostname)"\necho "操作系统: $(uname -s)"\necho "内核版本: $(uname -r)"\necho "系统架构: $(uname -m)"\necho "运行时间: $(uptime)"\necho "当前时间: $(date)"\necho "磁盘使用: $(df -h / | tail -1)"\necho "内存使用: $(free -h | grep Mem)"\n```\n\n**应用场景：**\n• 系统监控脚本\n• 环境检查工具\n• 自动化部署脚本''',
                'exercises': [
                    "理论练习：解释Shell脚本的Shebang行的作用，并说明#!/bin/bash和#!/bin/sh的区别。",
                    "实践练习：创建一个Shell脚本，显示当前系统的基本信息（用户名、主机名、当前时间、工作目录）。",
                    "扩展练习：编写一个脚本检查系统中是否安装了指定的软件包（如git、vim、python3），并输出检查结果。"
                ]
            },
            {
                'title': '变量定义与使用技巧',
                'theory': '''Shell变量是存储数据的容器，分为环境变量和用户自定义变量。变量赋值时等号两边不能有空格，使用时需要加$符号。\n\n**变量类型：**\n• 字符串变量：name="value"\n• 数值变量：count=10\n• 数组变量：arr=(a b c)\n• 只读变量：readonly PI=3.14\n\n**变量作用域：**\n• 局部变量：仅在当前Shell中有效\n• 环境变量：可被子进程继承\n• 全局变量：export导出的变量\n\n**特殊变量：**\n• $0：脚本名称\n• $1-$9：位置参数\n• $#：参数个数\n• $@：所有参数\n• $?：上一命令退出状态''',
                'code': '''#!/bin/bash\n# 变量定义与使用\n\n# 基本变量\nname="张三"\nage=25\npath="/home/user"\n\n# 变量使用\necho "姓名: $name"\necho "年龄: ${age}岁"\necho "路径: $path"\n\n# 命令替换\ncurrent_date=$(date +"%Y-%m-%d")\nfile_count=`ls | wc -l`\necho "当前日期: $current_date"\necho "文件数量: $file_count"\n\n# 数组变量\nfruits=("苹果" "香蕉" "橙子")\necho "第一个水果: ${fruits[0]}"\necho "所有水果: ${fruits[@]}"\necho "数组长度: ${#fruits[@]}"\n\n# 只读变量\nreadonly PI=3.14159\necho "圆周率: $PI"\n\n# 删除变量\nunset name\necho "删除后的name: $name"''',
                'case': '''**案例：配置文件管理脚本**\n\n创建一个管理应用配置的脚本：\n\n```bash\n#!/bin/bash\n# 文件名：config_manager.sh\n\n# 配置变量\nAPP_NAME="BigDataApp"\nAPP_VERSION="1.0.0"\nCONFIG_DIR="/etc/bigdata"\nLOG_DIR="/var/log/bigdata"\nDATA_DIR="/data/bigdata"\n\n# 数据库配置\nDB_HOST="localhost"\nDB_PORT=3306\nDB_NAME="bigdata_db"\nDB_USER="admin"\n\n# 创建配置文件\ncreate_config() {\n    echo "# $APP_NAME 配置文件" > "$CONFIG_DIR/app.conf"\n    echo "app.name=$APP_NAME" >> "$CONFIG_DIR/app.conf"\n    echo "app.version=$APP_VERSION" >> "$CONFIG_DIR/app.conf"\n    echo "db.host=$DB_HOST" >> "$CONFIG_DIR/app.conf"\n    echo "db.port=$DB_PORT" >> "$CONFIG_DIR/app.conf"\n    echo "配置文件已创建: $CONFIG_DIR/app.conf"\n}\n\n# 显示配置\nshow_config() {\n    echo "=== 应用配置 ==="\n    echo "应用名称: $APP_NAME"\n    echo "版本号: $APP_VERSION"\n    echo "配置目录: $CONFIG_DIR"\n    echo "日志目录: $LOG_DIR"\n    echo "数据目录: $DATA_DIR"\n}\n\n# 主程序\ncase $1 in\n    "create")\n        create_config\n        ;;\n    "show")\n        show_config\n        ;;\n    *)\n        echo "用法: $0 {create|show}"\n        ;;\nesac\n```''',
                'exercises': [
                    "理论练习：说明Shell变量赋值时为什么等号两边不能有空格，以及$var和${var}的使用场景区别。",
                    "实践练习：编写脚本接收用户输入的姓名和年龄，然后输出格式化的个人信息。",
                    "扩展练习：创建一个脚本使用数组存储多个文件路径，然后遍历检查每个文件是否存在。"
                ]
            },
            {
                'title': '条件判断与分支控制',
                'theory': '''Shell提供if-then-else条件判断结构，支持数值比较、字符串比较和文件测试。test命令或[]用于条件测试，&&和||用于逻辑运算。\n\n**比较操作符：**\n• 数值比较：-eq(等于)、-ne(不等于)、-gt(大于)、-lt(小于)\n• 字符串比较：=(等于)、!=(不等于)、-z(为空)、-n(非空)\n• 文件测试：-f(文件)、-d(目录)、-e(存在)、-r(可读)\n\n**逻辑操作符：**\n• &&：逻辑与\n• ||：逻辑或\n• !：逻辑非\n\n**case语句：**\n• 多分支选择结构\n• 支持模式匹配\n• 比多个if-elif更简洁''',
                'code': '''#!/bin/bash\n# 条件判断示例\n\n# 数值比较\nnum=10\nif [ $num -gt 5 ]; then\n    echo "数字大于5"\nelif [ $num -eq 5 ]; then\n    echo "数字等于5"\nelse\n    echo "数字小于5"\nfi\n\n# 字符串比较\nuser="admin"\nif [ "$user" = "admin" ]; then\n    echo "管理员用户"\nelse\n    echo "普通用户"\nfi\n\n# 文件测试\nfile="/etc/passwd"\nif [ -f "$file" ]; then\n    echo "文件存在"\n    if [ -r "$file" ]; then\n        echo "文件可读"\n    fi\nfi\n\n# case语句\necho "请选择操作: (start|stop|restart|status)"\nread action\ncase $action in\n    "start")\n        echo "启动服务..."\n        ;;\n    "stop")\n        echo "停止服务..."\n        ;;\n    "restart")\n        echo "重启服务..."\n        ;;\n    "status")\n        echo "查看状态..."\n        ;;\n    *)\n        echo "无效操作"\n        ;;\nesac''',
                'case': '''**案例：服务状态检查脚本**\n\n创建一个检查系统服务状态的脚本：\n\n```bash\n#!/bin/bash\n# 文件名：service_check.sh\n\n# 检查服务状态\ncheck_service() {\n    local service_name=$1\n    \n    if systemctl is-active --quiet "$service_name"; then\n        echo "✓ $service_name 服务正在运行"\n        return 0\n    else\n        echo "✗ $service_name 服务未运行"\n        return 1\n    fi\n}\n\n# 检查端口\ncheck_port() {\n    local port=$1\n    \n    if netstat -tuln | grep -q ":$port "; then\n        echo "✓ 端口 $port 正在监听"\n        return 0\n    else\n        echo "✗ 端口 $port 未监听"\n        return 1\n    fi\n}\n\n# 主检查逻辑\necho "=== 系统服务检查 ==="\n\n# 检查关键服务\nservices=("nginx" "mysql" "redis")\nfor service in "${services[@]}"; do\n    check_service "$service"\ndone\n\necho "\n=== 端口检查 ==="\n\n# 检查关键端口\nports=(80 443 3306 6379)\nfor port in "${ports[@]}"; do\n    check_port "$port"\ndone\n\n# 磁盘空间检查\necho "\n=== 磁盘空间检查 ==="\ndisk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')\nif [ "$disk_usage" -gt 80 ]; then\n    echo "⚠ 磁盘使用率过高: ${disk_usage}%"\nelse\n    echo "✓ 磁盘使用率正常: ${disk_usage}%"\nfi\n```''',
                'exercises': [
                    "理论练习：解释Shell中[ ]和[[ ]]的区别，以及什么时候使用test命令。",
                    "实践练习：编写脚本判断用户输入的数字是正数、负数还是零，并给出相应提示。",
                    "扩展练习：创建一个文件管理脚本，根据用户选择执行不同操作（创建、删除、查看、备份文件）。"
                ]
            },
            {
                'title': '循环结构与流程控制',
                'theory': '''Shell支持for、while、until三种循环结构。for循环适合遍历列表，while循环适合条件循环，until循环在条件为假时执行。\n\n**for循环类型：**\n• 列表遍历：for item in list\n• 数值范围：for i in {1..10}\n• C风格：for ((i=0; i<10; i++))\n• 文件遍历：for file in *.txt\n\n**while循环：**\n• 条件为真时执行\n• 适合不确定次数的循环\n• 常用于读取文件\n\n**until循环：**\n• 条件为假时执行\n• 与while相反\n\n**流程控制：**\n• break：跳出循环\n• continue：跳过当前迭代\n• exit：退出脚本''',
                'code': '''#!/bin/bash\n# 循环结构示例\n\n# for循环 - 数值范围\necho "=== 数值循环 ==="\nfor i in {1..5}; do\n    echo "数字: $i"\ndone\n\n# for循环 - 列表遍历\necho "\n=== 列表遍历 ==="\nfruits=("苹果" "香蕉" "橙子")\nfor fruit in "${fruits[@]}"; do\n    echo "水果: $fruit"\ndone\n\n# for循环 - 文件遍历\necho "\n=== 文件遍历 ==="\nfor file in *.txt; do\n    if [ -f "$file" ]; then\n        echo "处理文件: $file"\n        wc -l "$file"\n    fi\ndone\n\n# while循环\necho "\n=== while循环 ==="\ncount=1\nwhile [ $count -le 3 ]; do\n    echo "计数: $count"\n    count=$((count + 1))\ndone\n\n# 读取文件\necho "\n=== 读取文件 ==="\nwhile IFS= read -r line; do\n    echo "行内容: $line"\ndone < "/etc/passwd" | head -5\n\n# until循环\necho "\n=== until循环 ==="\nnum=1\nuntil [ $num -gt 3 ]; do\n    echo "Until: $num"\n    num=$((num + 1))\ndone''',
                'case': '''**案例：批量文件处理脚本**\n\n创建一个批量处理日志文件的脚本：\n\n```bash\n#!/bin/bash\n# 文件名：batch_process.sh\n\n# 配置\nLOG_DIR="/var/log/app"\nARCHIVE_DIR="/var/log/archive"\nMAX_SIZE=100M  # 100MB\nDAYS_OLD=7\n\n# 创建归档目录\nmkdir -p "$ARCHIVE_DIR"\n\n# 处理大文件\necho "=== 处理大文件 ==="\nfor logfile in "$LOG_DIR"/*.log; do\n    if [ -f "$logfile" ]; then\n        # 检查文件大小\n        size=$(stat -f%z "$logfile" 2>/dev/null || stat -c%s "$logfile")\n        size_mb=$((size / 1024 / 1024))\n        \n        if [ $size_mb -gt 100 ]; then\n            echo "处理大文件: $logfile (${size_mb}MB)"\n            \n            # 压缩并移动\n            gzip "$logfile"\n            mv "${logfile}.gz" "$ARCHIVE_DIR/"\n            echo "已归档: ${logfile}.gz"\n        fi\n    fi\ndone\n\n# 清理旧文件\necho "\n=== 清理旧文件 ==="\nfind "$ARCHIVE_DIR" -name "*.gz" -mtime +$DAYS_OLD -type f | while read -r oldfile; do\n    echo "删除旧文件: $oldfile"\n    rm "$oldfile"\ndone\n\n# 统计处理结果\necho "\n=== 处理统计 ==="\nactive_logs=$(find "$LOG_DIR" -name "*.log" | wc -l)\narchived_logs=$(find "$ARCHIVE_DIR" -name "*.gz" | wc -l)\necho "活跃日志文件: $active_logs"\necho "归档日志文件: $archived_logs"\n\n# 磁盘使用情况\necho "\n=== 磁盘使用 ==="\ndu -sh "$LOG_DIR" "$ARCHIVE_DIR"\n```''',
                'exercises': [
                    "理论练习：比较for、while、until三种循环的适用场景，并说明break和continue的区别。",
                    "实践练习：编写脚本使用for循环计算1到100的和，并用while循环实现相同功能。",
                    "扩展练习：创建一个脚本遍历指定目录下的所有.txt文件，统计每个文件的行数和总行数。"
                ]
            },
            {
                'title': '函数定义与模块化编程',
                'theory': '''Shell函数是可重用的代码块，提高脚本的模块化和可维护性。函数可以接收参数，通过$1、$2等访问参数，$#获取参数个数，$@获取所有参数。\n\n**函数特点：**\n• 代码重用，减少重复\n• 模块化设计，便于维护\n• 参数传递，灵活调用\n• 返回值，状态反馈\n\n**函数语法：**\n• 定义：function_name() { commands; }\n• 调用：function_name arg1 arg2\n• 局部变量：local var=value\n• 返回值：return 0-255\n\n**最佳实践：**\n• 函数名要有意义\n• 使用局部变量\n• 错误处理\n• 文档注释''',
                'code': '''#!/bin/bash\n# 函数定义与使用\n\n# 简单函数\ngreet() {\n    echo "Hello, $1!"\n}\n\n# 带参数检查的函数\ncheck_file() {\n    local filename=$1\n    \n    if [ $# -eq 0 ]; then\n        echo "错误: 请提供文件名"\n        return 1\n    fi\n    \n    if [ -f "$filename" ]; then\n        echo "文件 $filename 存在"\n        return 0\n    else\n        echo "文件 $filename 不存在"\n        return 1\n    fi\n}\n\n# 计算函数\ncalculate() {\n    local num1=$1\n    local num2=$2\n    local operation=$3\n    \n    case $operation in\n        "+")\n            echo $((num1 + num2))\n            ;;\n        "-")\n            echo $((num1 - num2))\n            ;;\n        "*")\n            echo $((num1 * num2))\n            ;;\n        "/")\n            if [ $num2 -ne 0 ]; then\n                echo $((num1 / num2))\n            else\n                echo "错误: 除数不能为0"\n                return 1\n            fi\n            ;;\n        *)\n            echo "错误: 不支持的操作"\n            return 1\n            ;;\n    esac\n}\n\n# 函数调用\ngreet "世界"\ncheck_file "/etc/passwd"\nresult=$(calculate 10 5 "+")\necho "计算结果: $result"''',
                'case': '''**案例：系统管理工具库**\n\n创建一个可重用的系统管理函数库：\n\n```bash\n#!/bin/bash\n# 文件名：syslib.sh - 系统管理函数库\n\n# 日志函数\nlog_info() {\n    echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1"\n}\n\nlog_error() {\n    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >&2\n}\n\n# 服务管理函数\nstart_service() {\n    local service_name=$1\n    \n    if [ -z "$service_name" ]; then\n        log_error "服务名不能为空"\n        return 1\n    fi\n    \n    log_info "启动服务: $service_name"\n    if systemctl start "$service_name"; then\n        log_info "服务 $service_name 启动成功"\n        return 0\n    else\n        log_error "服务 $service_name 启动失败"\n        return 1\n    fi\n}\n\n# 备份函数\nbackup_directory() {\n    local source_dir=$1\n    local backup_dir=$2\n    local timestamp=$(date +"%Y%m%d_%H%M%S")\n    \n    if [ ! -d "$source_dir" ]; then\n        log_error "源目录不存在: $source_dir"\n        return 1\n    fi\n    \n    mkdir -p "$backup_dir"\n    local backup_file="$backup_dir/backup_${timestamp}.tar.gz"\n    \n    log_info "开始备份: $source_dir -> $backup_file"\n    if tar -czf "$backup_file" -C "$(dirname "$source_dir")" "$(basename "$source_dir")"; then\n        log_info "备份完成: $backup_file"\n        return 0\n    else\n        log_error "备份失败"\n        return 1\n    fi\n}\n\n# 磁盘空间检查\ncheck_disk_space() {\n    local path=${1:-"/"}\n    local threshold=${2:-80}\n    \n    local usage=$(df "$path" | tail -1 | awk '{print $5}' | sed 's/%//')\n    \n    if [ "$usage" -gt "$threshold" ]; then\n        log_error "磁盘空间不足: $path 使用率 ${usage}% (阈值: ${threshold}%)"\n        return 1\n    else\n        log_info "磁盘空间正常: $path 使用率 ${usage}%"\n        return 0\n    fi\n}\n\n# 使用示例\n# source syslib.sh\n# start_service "nginx"\n# backup_directory "/etc" "/backup"\n# check_disk_space "/" 90\n```''',
                'exercises': [
                    "理论练习：解释Shell函数中局部变量和全局变量的区别，以及return和exit的不同用法。",
                    "实践练习：编写一个包含多个数学运算函数的脚本（加、减、乘、除），并创建主函数调用它们。",
                    "扩展练习：设计一个文件操作函数库，包含创建、删除、复制、移动文件的函数，并添加错误处理。"
                ]
            }
        ]
        
        # 插入新的内容
        print("插入Shell脚本模块的新内容...")
        for i, content in enumerate(shell_contents):
            if i >= len(topics):
                print(f"警告: 内容数量超过主题数量")
                break
                
            topic_id = topics[i][0]
            data = {
                'theory': content['theory'],
                'code': content['code'],
                'case': content['case'],
                'exercises': content['exercises']
            }
            
            cursor.execute("""
                INSERT INTO contents (topic_id, data)
                VALUES (?, ?)
            """, (topic_id, json.dumps(data, ensure_ascii=False)))
            
            print(f"已插入知识点 {i+1}: {content['title']}")
        
        conn.commit()
        print("\nShell脚本模块内容重新生成完成！")
        
        # 验证结果
        cursor.execute("""
            SELECT t.ord, t.title 
            FROM topics t 
            JOIN contents c ON t.id = c.topic_id 
            WHERE t.module_id = 2 
            ORDER BY t.ord
        """)
        results = cursor.fetchall()
        print("\n=== 验证结果 ===")
        for ord_num, title in results:
            print(f"知识点 {ord_num}: {title}")
            
    except Exception as e:
        print(f"错误: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    regenerate_shell_content()