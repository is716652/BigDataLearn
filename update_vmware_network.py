#!/usr/bin/env python3
import sqlite3
import json
import os

# 使用正确的数据库路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'DB')
DB_PATH = os.path.join(DB_DIR, 'app.db')

print(f"更新VMware网络配置主题: {DB_PATH}")

# 更新后的网络配置主题内容
updated_network_content = {
    'title': 'VMware网络模式详解与配置实战',
    'theory': '''VMware提供三种主要的网络连接模式，每种模式都有其独特的特点和适用场景。正确理解和配置网络模式是虚拟机与外界通信的关键。\n\n## 三种网络模式对比\n\n### 1. 桥接模式 (Bridged)\n**工作原理：**\n• 虚拟机直接连接到物理网络\n• 虚拟机获得与宿主机同网段的IP地址\n• 虚拟机在网络中表现为独立的物理设备\n\n**特点：**\n✅ 虚拟机可以直接访问局域网内其他设备\n✅ 局域网内其他设备可以直接访问虚拟机\n✅ 网络性能最佳，延迟最低\n❌ 需要额外的IP地址资源\n❌ 受网络管理员权限限制\n❌ 移动设备时需要重新配置\n\n**适用场景：**\n• 服务器虚拟化环境\n• 需要对外提供服务的虚拟机\n• 局域网内设备需要直接访问虚拟机\n\n### 2. NAT模式 (Network Address Translation)\n**工作原理：**\n• 虚拟机通过宿主机的网络地址转换访问外网\n• 虚拟机使用私有IP地址段（如192.168.x.x）\n• 宿主机充当路由器和防火墙角色\n\n**特点：**\n✅ 不需要额外的公网IP地址\n✅ 虚拟机受宿主机防火墙保护\n✅ 便于移动和迁移\n✅ 可以通过端口映射提供服务\n❌ 局域网设备无法直接访问虚拟机\n❌ 网络性能略低于桥接模式\n❌ 配置相对复杂\n\n**适用场景：**\n• 开发和测试环境\n• 个人学习和实验\n• 需要网络隔离的环境\n• 笔记本电脑上的虚拟机\n\n### 3. 仅主机模式 (Host-Only)\n**工作原理：**\n• 创建一个仅在宿主机和虚拟机之间的私有网络\n• 虚拟机无法访问外部网络\n• 只能与宿主机和同一Host-Only网络的虚拟机通信\n\n**特点：**\n✅ 完全隔离的安全环境\n✅ 不受外网环境影响\n✅ 适合搭建内部集群\n❌ 无法访问互联网\n❌ 无法与局域网其他设备通信\n❌ 功能受限\n\n**适用场景：**\n• 安全测试环境\n• 内部集群搭建\n• 离线开发环境\n• 恶意软件分析\n\n## 网络模式选择指南\n\n| 需求场景 | 推荐模式 | 原因 |\n|---------|---------|------|\n| Web服务器部署 | 桥接模式 | 需要外部直接访问 |\n| 开发测试环境 | NAT模式 | 平衡安全性和便利性 |\n| 大数据集群学习 | NAT模式 | 端口映射访问Web界面 |\n| 安全研究 | 仅主机模式 | 完全隔离环境 |\n| 多虚拟机集群 | 仅主机模式 | 内部通信，外部隔离 |''',
    'code': '''# VMware网络模式配置命令和脚本\n\n# 1. 查看和配置虚拟网络\n# 在VMware中：编辑 -> 虚拟网络编辑器\n\n# 2. 桥接模式配置\n# .vmx配置文件示例\nethernet0.present = "TRUE"\nethernet0.connectionType = "bridged"\nethernet0.virtualDev = "e1000"\nethernet0.wakeOnPcktRcv = "FALSE"\nethernet0.addressType = "generated"\n\n# Linux虚拟机桥接模式网络配置\n# Ubuntu Netplan配置 (/etc/netplan/01-netcfg.yaml)\nnetwork:\n  version: 2\n  ethernets:\n    ens33:\n      dhcp4: true  # 或配置静态IP\n      # addresses: [192.168.1.100/24]\n      # gateway4: 192.168.1.1\n      # nameservers:\n      #   addresses: [8.8.8.8, 8.8.4.4]\n\n# 3. NAT模式配置\n# .vmx配置文件示例\nethernet0.present = "TRUE"\nethernet0.connectionType = "nat"\nethernet0.virtualDev = "e1000"\nethernet0.wakeOnPcktRcv = "FALSE"\nethernet0.addressType = "generated"\n\n# NAT端口映射配置示例\n# 虚拟网络编辑器 -> VMnet8 -> NAT设置 -> 端口转发\n# 格式：主机端口 -> 虚拟机IP:端口\n\n# 常用端口映射配置\n# SSH访问\n2222 -> 192.168.100.128:22\n\n# Web服务\n8080 -> 192.168.100.128:80\n8443 -> 192.168.100.128:443\n\n# 大数据服务端口\n9870 -> 192.168.100.128:9870  # Hadoop NameNode\n8088 -> 192.168.100.128:8088  # YARN ResourceManager\n4040 -> 192.168.100.128:4040  # Spark Web UI\n8080 -> 192.168.100.128:8080  # Spark Master\n\n# 数据库服务\n3306 -> 192.168.100.128:3306  # MySQL\n5432 -> 192.168.100.128:5432  # PostgreSQL\n27017 -> 192.168.100.128:27017 # MongoDB\n\n# 4. 仅主机模式配置\n# .vmx配置文件示例\nethernet0.present = "TRUE"\nethernet0.connectionType = "hostonly"\nethernet0.virtualDev = "e1000"\nethernet0.wakeOnPcktRcv = "FALSE"\nethernet0.addressType = "generated"\n\n# Host-Only网络配置\n# 虚拟网络编辑器 -> VMnet1 -> 主机虚拟适配器设置\n# 子网IP: 192.168.56.0\n# 子网掩码: 255.255.255.0\n\n# 5. 网络诊断脚本\n#!/bin/bash\n# 网络连接测试脚本\n\necho "=== VMware虚拟机网络诊断 ==="\necho "时间: $(date)"\necho\n\n# 1. 网络接口信息\necho "1. 网络接口信息:"\nip addr show | grep -E "^[0-9]+:|inet "\necho\n\n# 2. 路由表\necho "2. 路由表:"\nip route show\necho\n\n# 3. DNS配置\necho "3. DNS配置:"\ncat /etc/resolv.conf\necho\n\n# 4. 连通性测试\necho "4. 连通性测试:"\necho "测试网关连通性:"\nping -c 3 $(ip route | grep default | awk '{print $3}') 2>/dev/null\necho\necho "测试外网连通性:"\nping -c 3 8.8.8.8 2>/dev/null\necho\necho "测试域名解析:"\nnslookup google.com 2>/dev/null\n\n# 5. 端口监听\necho "5. 端口监听状态:"\nss -tulpn | head -10\n\n# 6. 网络模式识别\necho "6. 网络模式识别:"\nGATEWAY=$(ip route | grep default | awk '{print $3}')\nif [[ $GATEWAY == 192.168.* ]]; then\n    if [[ $GATEWAY == *.2 ]]; then\n        echo "检测到NAT模式 (网关: $GATEWAY)"\n    else\n        echo "检测到桥接模式 (网关: $GATEWAY)"\n    fi\nelif [[ $GATEWAY == 192.168.56.* ]]; then\n    echo "检测到仅主机模式 (网关: $GATEWAY)"\nelse\n    echo "未知网络模式 (网关: $GATEWAY)"\nfi\n\n# 7. VMware Tools网络状态\necho "7. VMware Tools网络状态:"\nvmware-toolbox-cmd stat sessionid 2>/dev/null || echo "VMware Tools未安装或未运行"\n\necho "\n=== 诊断完成 ==="''',
    'case': '''## 实战案例：大数据学习环境网络配置\n\n### 案例1：单机开发环境（NAT模式）\n\n**场景：** 在笔记本上搭建Hadoop学习环境\n\n**需求分析：**\n- 需要访问外网下载软件包\n- 通过浏览器访问Hadoop Web界面\n- 便于携带和迁移\n- 不影响宿主机网络\n\n**配置方案：**\n\n1. **虚拟机网络设置**\n   ```\n   网络模式：NAT\n   虚拟网络：VMnet8\n   子网：192.168.100.0/24\n   网关：192.168.100.2\n   DHCP：启用\n   ```\n\n2. **端口映射配置**\n   ```\n   # Hadoop服务端口映射\n   主机端口 -> 虚拟机端口\n   9870 -> 192.168.100.128:9870   # NameNode Web UI\n   8088 -> 192.168.100.128:8088   # ResourceManager Web UI\n   19888 -> 192.168.100.128:19888 # JobHistory Server\n   \n   # 开发工具端口\n   8080 -> 192.168.100.128:8080   # Tomcat\n   3000 -> 192.168.100.128:3000   # Node.js开发服务器\n   8888 -> 192.168.100.128:8888   # Jupyter Notebook\n   \n   # 远程访问\n   2222 -> 192.168.100.128:22     # SSH\n   5901 -> 192.168.100.128:5901   # VNC\n   ```\n\n3. **虚拟机网络配置**\n   ```bash\n   # 配置静态IP（可选）\n   sudo nano /etc/netplan/01-netcfg.yaml\n   \n   network:\n     version: 2\n     ethernets:\n       ens33:\n         addresses: [192.168.100.128/24]\n         gateway4: 192.168.100.2\n         nameservers:\n           addresses: [8.8.8.8, 8.8.4.4]\n   \n   sudo netplan apply\n   ```\n\n4. **验证配置**\n   ```bash\n   # 在宿主机浏览器中访问\n   http://localhost:9870    # Hadoop NameNode\n   http://localhost:8088    # YARN ResourceManager\n   \n   # SSH连接\n   ssh -p 2222 hadoop@localhost\n   ```\n\n### 案例2：多节点集群环境（仅主机模式）\n\n**场景：** 搭建3节点Hadoop集群进行分布式计算学习\n\n**需求分析：**\n- 节点间需要相互通信\n- 模拟真实集群网络环境\n- 与外网隔离确保安全\n- 统一的网络配置\n\n**配置方案：**\n\n1. **虚拟网络规划**\n   ```\n   网络模式：仅主机模式\n   虚拟网络：VMnet1\n   子网：192.168.56.0/24\n   \n   节点IP分配：\n   - hadoop-master: 192.168.56.101\n   - hadoop-worker1: 192.168.56.102\n   - hadoop-worker2: 192.168.56.103\n   ```\n\n2. **虚拟机配置**\n   ```\n   # 每个虚拟机的.vmx文件\n   ethernet0.present = "TRUE"\n   ethernet0.connectionType = "hostonly"\n   ethernet0.virtualDev = "e1000"\n   ethernet0.addressType = "static"\n   ```\n\n3. **网络配置脚本**\n   ```bash\n   #!/bin/bash\n   # setup_cluster_network.sh\n   \n   # 配置主机名和IP映射\n   cat >> /etc/hosts << EOF\n   192.168.56.101 hadoop-master\n   192.168.56.102 hadoop-worker1\n   192.168.56.103 hadoop-worker2\n   EOF\n   \n   # 配置静态IP（根据节点调整IP地址）\n   cat > /etc/netplan/01-netcfg.yaml << EOF\n   network:\n     version: 2\n     ethernets:\n       ens33:\n         addresses: [192.168.56.101/24]  # 根据节点修改\n         nameservers:\n           addresses: [192.168.56.1]\n   EOF\n   \n   netplan apply\n   \n   # 配置SSH免密登录\n   ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa\n   # 将公钥复制到其他节点\n   ```\n\n4. **集群连通性测试**\n   ```bash\n   #!/bin/bash\n   # test_cluster_network.sh\n   \n   NODES=("hadoop-master" "hadoop-worker1" "hadoop-worker2")\n   \n   echo "测试集群节点连通性..."\n   for node in "${NODES[@]}"; do\n       echo "测试连接到 $node:"\n       ping -c 3 $node\n       echo "SSH连接测试:"\n       ssh -o ConnectTimeout=5 $node "hostname && date"\n       echo "---"\n   done\n   ```\n\n### 案例3：生产环境模拟（桥接模式）\n\n**场景：** 模拟企业级大数据平台部署\n\n**需求分析：**\n- 需要对外提供服务\n- 局域网内其他设备需要访问\n- 模拟真实生产环境\n- 高性能网络需求\n\n**配置方案：**\n\n1. **网络规划**\n   ```\n   网络模式：桥接模式\n   物理网络：192.168.1.0/24\n   \n   服务器IP分配：\n   - bigdata-master: 192.168.1.201\n   - bigdata-worker1: 192.168.1.202\n   - bigdata-worker2: 192.168.1.203\n   - bigdata-edge: 192.168.1.204\n   ```\n\n2. **高可用配置**\n   ```bash\n   # 配置网络绑定（双网卡）\n   cat > /etc/netplan/01-netcfg.yaml << EOF\n   network:\n     version: 2\n     ethernets:\n       ens33:\n         dhcp4: false\n       ens34:\n         dhcp4: false\n     bonds:\n       bond0:\n         interfaces: [ens33, ens34]\n         addresses: [192.168.1.201/24]\n         gateway4: 192.168.1.1\n         nameservers:\n           addresses: [8.8.8.8, 8.8.4.4]\n         parameters:\n           mode: active-backup\n           primary: ens33\n   EOF\n   ```\n\n3. **防火墙配置**\n   ```bash\n   # 配置防火墙规则\n   ufw enable\n   \n   # Hadoop端口\n   ufw allow 9870    # NameNode Web UI\n   ufw allow 8088    # ResourceManager Web UI\n   ufw allow 9000    # NameNode IPC\n   \n   # Spark端口\n   ufw allow 8080    # Spark Master Web UI\n   ufw allow 4040    # Spark Application Web UI\n   \n   # 集群内部通信\n   ufw allow from 192.168.1.0/24\n   ```\n\n4. **负载均衡配置**\n   ```bash\n   # 使用Nginx做负载均衡\n   cat > /etc/nginx/sites-available/bigdata << EOF\n   upstream hadoop_namenodes {\n       server 192.168.1.201:9870;\n       server 192.168.1.202:9870 backup;\n   }\n   \n   server {\n       listen 80;\n       server_name bigdata.company.com;\n       \n       location / {\n           proxy_pass http://hadoop_namenodes;\n           proxy_set_header Host \$host;\n           proxy_set_header X-Real-IP \$remote_addr;\n       }\n   }\n   EOF\n   ```\n\n### 网络模式切换指南\n\n**开发阶段 → 测试阶段：**\n```\nNAT模式 → 仅主机模式\n优势：隔离测试环境，避免外部干扰\n注意：需要重新配置IP地址和主机名解析\n```\n\n**测试阶段 → 生产阶段：**\n```\n仅主机模式 → 桥接模式\n优势：真实网络环境，对外提供服务\n注意：需要申请IP地址，配置防火墙规则\n```\n\n**故障排查步骤：**\n1. 检查虚拟机网络适配器设置\n2. 验证IP地址配置\n3. 测试网关连通性\n4. 检查防火墙规则\n5. 验证DNS解析\n6. 测试端口映射（NAT模式）'''
}

try:
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("开始更新VMware网络配置主题...")
    
    # 1. 查找VMware模块中的网络配置主题
    cursor.execute('''
        SELECT t.id, t.title, c.id as content_id
        FROM topics t
        JOIN modules m ON t.module_id = m.id
        LEFT JOIN contents c ON t.id = c.topic_id
        WHERE m.title = 'VMware虚拟化环境搭建' AND t.title LIKE '%网络配置%'
    ''')
    
    result = cursor.fetchone()
    
    if not result:
        print("未找到VMware网络配置主题")
        conn.close()
        exit(1)
    
    topic_id, old_title, content_id = result
    print(f"找到网络配置主题: ID={topic_id}, 标题={old_title}")
    
    # 2. 更新主题标题
    new_title = updated_network_content['title']
    cursor.execute('UPDATE topics SET title = ? WHERE id = ?', (new_title, topic_id))
    print(f"更新主题标题: {old_title} -> {new_title}")
    
    # 3. 准备新的内容数据
    content_data = {
        'title': new_title,
        'theory': updated_network_content['theory'],
        'code': updated_network_content['code'],
        'case': updated_network_content['case'],
        'exercises': [
            "练习1：在VMware中分别配置桥接、NAT、仅主机三种网络模式，并测试连通性",
            "练习2：为NAT模式的虚拟机配置端口映射，实现外部访问Web服务",
            "练习3：搭建3节点仅主机模式集群，配置节点间SSH免密登录",
            "练习4：比较三种网络模式的性能差异，使用iperf3进行网络性能测试",
            "练习5：设计一个混合网络方案，同时使用多种网络模式满足不同需求"
        ],
        'images': [
            'https://images.unsplash.com/photo-1558494949-ef010cbdcc31',  # 网络拓扑图
            'https://images.unsplash.com/photo-1544197150-b99a580bb7a8',  # 网络配置
            'https://images.unsplash.com/photo-1518779578993-ec3579fee39f',  # 服务器网络
            'https://images.unsplash.com/photo-1519389950473-47ba0277781c',  # 数据中心
            'https://images.unsplash.com/photo-1551288049-bebda4e38f71'   # 网络监控
        ]
    }
    
    # 4. 更新内容数据
    if content_id:
        cursor.execute('''
            UPDATE contents SET data = ? WHERE id = ?
        ''', (json.dumps(content_data, ensure_ascii=False), content_id))
        print("更新现有内容数据")
    else:
        cursor.execute('''
            INSERT INTO contents (topic_id, data) VALUES (?, ?)
        ''', (topic_id, json.dumps(content_data, ensure_ascii=False)))
        print("插入新的内容数据")
    
    conn.commit()
    
    # 5. 验证更新结果
    print("\n验证更新结果:")
    cursor.execute('''
        SELECT t.title, c.data
        FROM topics t
        JOIN contents c ON t.id = c.topic_id
        WHERE t.id = ?
    ''', (topic_id,))
    
    result = cursor.fetchone()
    if result:
        title, data_json = result
        data = json.loads(data_json)
        print(f"主题标题: {title}")
        print(f"理论内容长度: {len(data['theory'])} 字符")
        print(f"代码示例长度: {len(data['code'])} 字符")
        print(f"案例内容长度: {len(data['case'])} 字符")
        print(f"练习题目数量: {len(data['exercises'])}")
        print(f"配图数量: {len(data['images'])}")
    
    conn.close()
    print("\nVMware网络配置主题更新成功！")
    print("\n新增内容包括:")
    print("- 桥接、NAT、仅主机三种模式的详细对比")
    print("- 每种模式的工作原理和适用场景")
    print("- 网络模式选择指南表格")
    print("- 三个完整的实战案例")
    print("- 网络诊断和故障排查脚本")
    print("- 丰富的配置示例和最佳实践")
    
except Exception as e:
    print(f"错误: {e}")
    if 'conn' in locals():
        conn.rollback()
        conn.close()