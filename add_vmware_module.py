#!/usr/bin/env python3
import sqlite3
import json
import os

# 使用正确的数据库路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'DB')
DB_PATH = os.path.join(DB_DIR, 'app.db')

print(f"添加VMware模块到数据库: {DB_PATH}")

# VMware模块的详细内容
vmware_content = {
    1: {
        'title': 'VMware Workstation安装与基础配置',
        'theory': '''VMware Workstation是业界领先的桌面虚拟化软件，允许在单台物理机上运行多个操作系统。\n\n**核心概念：**\n• 虚拟化技术：通过软件模拟硬件环境\n• 宿主机(Host)：运行VMware的物理计算机\n• 虚拟机(Guest)：在VMware中创建的虚拟计算机\n• 快照(Snapshot)：保存虚拟机某一时刻的完整状态\n\n**系统要求：**\n• CPU：支持64位的Intel或AMD处理器\n• 内存：至少4GB RAM（推荐8GB以上）\n• 硬盘：至少1.5GB可用空间用于安装\n• 操作系统：Windows 10/11, Linux等\n\n**版本选择：**\n• VMware Workstation Pro：功能完整，适合专业用户\n• VMware Workstation Player：免费版本，功能有限\n• VMware vSphere：企业级服务器虚拟化解决方案''',
        'code': '''# VMware安装后的基本配置检查\n\n# 1. 检查虚拟化支持\n# 在Windows命令提示符中运行：\nsysteminfo | findstr /i "hyper-v"\n\n# 2. BIOS设置检查\n# 确保以下选项已启用：\n# - Intel VT-x 或 AMD-V\n# - Intel VT-d 或 AMD IOMMU\n\n# 3. VMware服务状态检查\n# 在服务管理器中确认以下服务正在运行：\n# - VMware Authorization Service\n# - VMware DHCP Service\n# - VMware NAT Service\n\n# 4. 网络适配器检查\n# VMware会创建虚拟网络适配器：\n# - VMware Network Adapter VMnet1 (Host-only)\n# - VMware Network Adapter VMnet8 (NAT)''',
        'case': '''**案例：为大数据学习环境安装VMware**\n\n**场景：** 在Windows 11上安装VMware Workstation Pro 17\n\n**步骤：**\n1. **下载安装包**\n   - 访问VMware官网下载最新版本\n   - 选择适合的版本（Pro或Player）\n\n2. **安装过程**\n   - 右键以管理员身份运行安装程序\n   - 接受许可协议\n   - 选择安装路径（建议默认）\n   - 配置更新设置\n\n3. **许可证激活**\n   - 输入购买的许可证密钥\n   - 或选择试用版本（30天）\n\n4. **首次启动配置**\n   - 配置客户体验改进计划\n   - 设置软件更新选项\n   - 完成初始化设置\n\n**验证安装：**\n- 启动VMware Workstation\n- 检查"帮助" -> "关于"中的版本信息\n- 确认虚拟网络编辑器可以正常打开'''
    },
    2: {
        'title': '虚拟机创建与操作系统安装',
        'theory': '''创建虚拟机是使用VMware的第一步，需要合理配置硬件资源和选择合适的操作系统。\n\n**虚拟机硬件配置：**\n• CPU：根据需求分配核心数（建议不超过物理核心的50%）\n• 内存：Linux最少2GB，Windows最少4GB\n• 硬盘：动态分配vs固定大小，SCSI vs IDE\n• 网络：NAT、桥接、仅主机等模式\n\n**操作系统选择：**\n• Ubuntu 20.04/22.04 LTS：适合大数据开发\n• CentOS 7/8：企业级服务器环境\n• Windows Server：混合环境需求\n\n**安装方式：**\n• 简易安装：VMware自动化安装过程\n• 典型安装：手动控制安装步骤\n• 自定义安装：完全自定义硬件配置''',
        'code': '''# 虚拟机创建的关键配置参数\n\n# 1. 虚拟机配置文件(.vmx)示例\n# 位置：虚拟机文件夹/虚拟机名.vmx\n\n# 基本配置\nconfig.version = "8"\nvirtualHW.version = "19"\nmemSize = "4096"  # 内存大小(MB)\nnumvcpus = "2"    # CPU核心数\n\n# 硬盘配置\nscsi0.present = "TRUE"\nscsi0.virtualDev = "lsilogic"\nscsi0:0.present = "TRUE"\nscsi0:0.fileName = "Ubuntu.vmdk"\nscsi0:0.deviceType = "scsi-hardDisk"\n\n# 网络配置\nethernet0.present = "TRUE"\nethernet0.connectionType = "nat"\nethernet0.virtualDev = "e1000"\n\n# 2. VMware命令行工具\n# vmrun命令示例（需要VIX API）\nvmrun -T ws start "path/to/vm.vmx"\nvmrun -T ws stop "path/to/vm.vmx"\nvmrun -T ws suspend "path/to/vm.vmx"''',
        'case': '''**案例：创建Ubuntu 22.04虚拟机**\n\n**准备工作：**\n1. 下载Ubuntu 22.04 LTS ISO镜像\n2. 确保宿主机有足够的资源\n\n**创建步骤：**\n1. **新建虚拟机向导**\n   - 文件 -> 新建虚拟机\n   - 选择"典型"配置\n   - 选择"稍后安装操作系统"\n\n2. **操作系统配置**\n   - 客户机操作系统：Linux\n   - 版本：Ubuntu 64位\n   - 虚拟机名称：Ubuntu-BigData\n\n3. **硬件配置**\n   - 磁盘大小：40GB（动态分配）\n   - 内存：4GB\n   - 处理器：2核心\n\n4. **安装Ubuntu**\n   - 编辑虚拟机设置\n   - CD/DVD：使用ISO镜像文件\n   - 启动虚拟机开始安装\n\n**安装后配置：**\n- 安装VMware Tools提升性能\n- 配置网络和SSH访问\n- 创建快照保存初始状态'''
    },
    3: {
        'title': '网络配置与端口映射设置',
        'theory': '''VMware提供多种网络模式，每种模式适用于不同的使用场景。正确配置网络是虚拟机与外界通信的关键。\n\n**网络模式详解：**\n• **NAT模式**：虚拟机通过宿主机访问网络，有独立IP段\n• **桥接模式**：虚拟机直接连接物理网络，获得与宿主机同网段IP\n• **仅主机模式**：虚拟机只能与宿主机通信，完全隔离\n• **自定义模式**：使用特定的虚拟网络适配器\n\n**端口映射原理：**\n• 将宿主机端口映射到虚拟机端口\n• 实现外部网络访问虚拟机服务\n• 常用于Web服务、SSH、数据库等\n\n**网络故障排查：**\n• ping测试连通性\n• 检查防火墙设置\n• 验证IP地址分配\n• 确认路由表配置''',
        'code': '''# VMware网络配置命令和脚本\n\n# 1. 查看虚拟网络配置\n# 在VMware中：编辑 -> 虚拟网络编辑器\n\n# 2. NAT端口映射配置\n# 虚拟网络编辑器 -> 选择VMnet8 -> NAT设置 -> 端口转发\n\n# 示例端口映射配置：\n# 主机端口 -> 虚拟机IP:端口\n# 2222 -> 192.168.100.128:22    (SSH)\n# 8080 -> 192.168.100.128:80    (HTTP)\n# 3306 -> 192.168.100.128:3306  (MySQL)\n# 9000 -> 192.168.100.128:9000  (Hadoop)\n\n# 3. Linux虚拟机网络配置\n# 查看网络接口\nip addr show\nifconfig\n\n# 配置静态IP（Ubuntu）\nsudo nano /etc/netplan/01-netcfg.yaml\n# 内容示例：\nnetwork:\n  version: 2\n  ethernets:\n    ens33:\n      dhcp4: false\n      addresses: [192.168.100.100/24]\n      gateway4: 192.168.100.2\n      nameservers:\n        addresses: [8.8.8.8, 8.8.4.4]\n\n# 应用配置\nsudo netplan apply\n\n# 4. 防火墙配置\n# Ubuntu防火墙\nsudo ufw enable\nsudo ufw allow 22    # SSH\nsudo ufw allow 80    # HTTP\nsudo ufw allow 8080  # 自定义端口''',
        'case': '''**案例：配置大数据集群网络环境**\n\n**需求：** 搭建3节点Hadoop集群，需要相互通信\n\n**网络规划：**\n- 使用NAT模式保证外网访问\n- 配置端口映射访问集群服务\n- 设置静态IP确保节点间通信\n\n**实施步骤：**\n\n1. **虚拟网络配置**\n   - 打开虚拟网络编辑器\n   - 选择VMnet8（NAT模式）\n   - 设置子网IP：192.168.100.0/24\n   - 网关：192.168.100.2\n\n2. **端口映射设置**\n   ```\n   # Hadoop集群端口映射\n   主机端口 -> 虚拟机端口\n   9870 -> 192.168.100.101:9870  # NameNode Web UI\n   8088 -> 192.168.100.101:8088  # ResourceManager Web UI\n   19888 -> 192.168.100.101:19888 # JobHistory Server\n   2201 -> 192.168.100.101:22    # SSH to master\n   2202 -> 192.168.100.102:22    # SSH to worker1\n   2203 -> 192.168.100.103:22    # SSH to worker2\n   ```\n\n3. **虚拟机IP配置**\n   - Master节点：192.168.100.101\n   - Worker1节点：192.168.100.102\n   - Worker2节点：192.168.100.103\n\n4. **连通性测试**\n   ```bash\n   # 在宿主机测试\n   ping 192.168.100.101\n   ssh -p 2201 hadoop@localhost\n   \n   # 访问Web界面\n   http://localhost:9870  # NameNode\n   http://localhost:8088  # ResourceManager\n   ```'''
    },
    4: {
        'title': '快照管理与虚拟机克隆',
        'theory': '''快照和克隆是VMware的重要功能，用于备份、恢复和快速部署虚拟机环境。\n\n**快照功能：**\n• 保存虚拟机的完整状态（内存、设置、磁盘）\n• 支持多个快照点，形成快照树\n• 可以快速回滚到任意快照状态\n• 适用于测试、开发、培训环境\n\n**快照类型：**\n• 内存快照：包含虚拟机内存状态\n• 静默快照：不包含内存，虚拟机需关机\n• 自动快照：定时自动创建\n\n**克隆技术：**\n• 完整克隆：创建独立的虚拟机副本\n• 链接克隆：基于快照创建，节省磁盘空间\n• 模板克隆：基于预配置的虚拟机模板\n\n**最佳实践：**\n• 定期清理旧快照避免磁盘空间不足\n• 重要节点创建快照（如系统安装后、软件配置后）\n• 使用描述性名称标识快照用途''',
        'code': '''# 快照和克隆相关的VMware操作\n\n# 1. 快照管理命令（vmrun工具）\n# 创建快照\nvmrun -T ws snapshot "path/to/vm.vmx" "snapshot_name"\n\n# 恢复到快照\nvmrun -T ws revertToSnapshot "path/to/vm.vmx" "snapshot_name"\n\n# 删除快照\nvmrun -T ws deleteSnapshot "path/to/vm.vmx" "snapshot_name"\n\n# 列出所有快照\nvmrun -T ws listSnapshots "path/to/vm.vmx"\n\n# 2. 克隆虚拟机\n# 完整克隆（通过GUI操作）\n# 右键虚拟机 -> 管理 -> 克隆\n\n# 3. 批量快照脚本示例\n#!/bin/bash\n# 为多个虚拟机创建快照\n\nVM_LIST=(\n    "/path/to/hadoop-master.vmx"\n    "/path/to/hadoop-worker1.vmx"\n    "/path/to/hadoop-worker2.vmx"\n)\n\nSNAPSHOT_NAME="cluster-configured-$(date +%Y%m%d)"\n\nfor vm in "${VM_LIST[@]}"; do\n    echo "Creating snapshot for $vm"\n    vmrun -T ws snapshot "$vm" "$SNAPSHOT_NAME"\ndone\n\n# 4. 虚拟机配置备份\n# 备份.vmx配置文件\ncp /path/to/vm.vmx /backup/vm-$(date +%Y%m%d).vmx\n\n# 5. 磁盘空间监控\n# 检查快照占用空间\ndu -sh /path/to/vm-folder/\nls -la *.vmdk''',
        'case': '''**案例：大数据集群环境的快照管理策略**\n\n**场景：** 管理3节点Hadoop集群的开发和测试环境\n\n**快照策略：**\n\n1. **基础环境快照**\n   - 快照名："01-os-installed"\n   - 时机：操作系统安装完成后\n   - 用途：快速重建干净系统\n\n2. **软件安装快照**\n   - 快照名："02-java-hadoop-installed"\n   - 时机：Java和Hadoop安装配置完成\n   - 用途：跳过软件安装步骤\n\n3. **集群配置快照**\n   - 快照名："03-cluster-configured"\n   - 时机：集群配置完成，服务正常启动\n   - 用途：快速恢复可用集群\n\n4. **数据导入快照**\n   - 快照名："04-sample-data-loaded"\n   - 时机：示例数据导入完成\n   - 用途：快速开始数据分析实验\n\n**克隆应用：**\n\n1. **开发环境克隆**\n   ```\n   基础虚拟机：hadoop-template\n   克隆目标：\n   - hadoop-dev1（开发者A）\n   - hadoop-dev2（开发者B）\n   - hadoop-test（测试环境）\n   ```\n\n2. **培训环境部署**\n   - 基于"03-cluster-configured"快照\n   - 快速为每个学员创建独立环境\n   - 统一的起始状态确保实验一致性\n\n**维护操作：**\n```bash\n# 每周清理超过30天的快照\nfind /vm-storage -name "*.vmsd" -mtime +30\n\n# 监控磁盘使用\ndf -h /vm-storage\n\n# 压缩虚拟磁盘\nvmware-vdiskmanager -k disk.vmdk\n```'''
    },
    5: {
        'title': 'VMware Tools安装与性能优化',
        'theory': '''VMware Tools是增强虚拟机性能和功能的重要组件，提供更好的图形性能、文件共享、时间同步等功能。\n\n**VMware Tools功能：**\n• 改善图形性能和分辨率支持\n• 实现宿主机与虚拟机间的文件拖拽\n• 提供共享文件夹功能\n• 优化网络和磁盘I/O性能\n• 实现时间同步\n• 支持虚拟机的优雅关机\n\n**性能优化策略：**\n• 合理分配CPU和内存资源\n• 启用硬件加速功能\n• 优化磁盘I/O设置\n• 配置适当的网络适配器类型\n• 禁用不必要的设备和服务\n\n**监控指标：**\n• CPU使用率和等待时间\n• 内存使用和交换\n• 磁盘I/O吞吐量\n• 网络带宽利用率\n\n**故障排查：**\n• 性能问题诊断\n• 资源瓶颈识别\n• 配置优化建议''',
        'code': '''# VMware Tools安装和性能优化配置\n\n# 1. Linux系统VMware Tools安装\n# 方法1：使用发行版包管理器（推荐）\n# Ubuntu/Debian\nsudo apt update\nsudo apt install open-vm-tools open-vm-tools-desktop\n\n# CentOS/RHEL\nsudo yum install open-vm-tools open-vm-tools-desktop\n# 或者\nsudo dnf install open-vm-tools open-vm-tools-desktop\n\n# 方法2：手动安装VMware Tools\n# 在VMware菜单：虚拟机 -> 安装VMware Tools\n# 挂载ISO并安装\nsudo mkdir /mnt/cdrom\nsudo mount /dev/cdrom /mnt/cdrom\ncp /mnt/cdrom/VMwareTools-*.tar.gz /tmp/\ncd /tmp\ntar -xzf VMwareTools-*.tar.gz\ncd vmware-tools-distrib\nsudo ./vmware-install.pl\n\n# 2. 性能监控脚本\n#!/bin/bash\n# 虚拟机性能监控\n\necho "=== VMware虚拟机性能报告 ==="\necho "时间: $(date)"\necho\n\n# CPU信息\necho "CPU使用率:"\ntop -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1\n\n# 内存信息\necho "内存使用情况:"\nfree -h\n\n# 磁盘I/O\necho "磁盘使用情况:"\ndf -h\n\n# 网络统计\necho "网络接口统计:"\ncat /proc/net/dev | grep eth0\n\n# VMware Tools状态\necho "VMware Tools状态:"\nvmware-toolbox-cmd stat sessionid 2>/dev/null || echo "未安装或未运行"\n\n# 3. 虚拟机配置优化\n# .vmx文件优化参数\n\n# 内存优化\nsched.mem.pshare.enable = "FALSE"\nprefvmx.useRecommendedLockedMemSize = "TRUE"\nmemsize = "4096"\n\n# CPU优化\nnumvcpus = "2"\ncpuid.coresPerSocket = "2"\n\n# 磁盘优化\nscsi0.virtualDev = "pvscsi"  # 使用半虚拟化SCSI\ndisk.EnableUUID = "TRUE"\n\n# 网络优化\nethernet0.virtualDev = "vmxnet3"  # 使用VMXNet3适配器\n\n# 图形优化\nsvga.autodetect = "TRUE"\nsvga.vramSize = "134217728"  # 128MB显存\n\n# 4. 共享文件夹配置\n# 启用共享文件夹\nsharedFolder0.present = "TRUE"\nsharedFolder0.enabled = "TRUE"\nsharedFolder0.readAccess = "TRUE"\nsharedFolder0.writeAccess = "TRUE"\nsharedFolder0.hostPath = "C:\\SharedData"\nsharedFolder0.guestName = "shared"\nsharedFolder0.expiration = "never"\n\n# Linux中挂载共享文件夹\nsudo mkdir /mnt/shared\nsudo mount -t vmhgfs-fuse .host:/shared /mnt/shared -o allow_other\n\n# 开机自动挂载\necho ".host:/shared /mnt/shared vmhgfs-fuse allow_other 0 0" | sudo tee -a /etc/fstab''',
        'case': '''**案例：优化大数据处理虚拟机性能**\n\n**场景：** 在VMware中运行Spark数据处理任务，需要优化性能\n\n**硬件配置优化：**\n\n1. **CPU配置**\n   - 分配4个vCPU（物理机8核）\n   - 启用虚拟化引擎中的"虚拟化Intel VT-x/EPT"\n   - 设置CPU亲和性避免资源竞争\n\n2. **内存配置**\n   - 分配8GB内存（物理机16GB）\n   - 禁用内存页面共享提高性能\n   - 预留内存避免交换\n\n3. **存储优化**\n   - 使用SSD存储虚拟机文件\n   - 选择PVSCSI适配器\n   - 预分配磁盘空间\n   - 禁用磁盘碎片整理\n\n**软件配置优化：**\n\n1. **操作系统调优**\n   ```bash\n   # 调整虚拟内存\n   echo 'vm.swappiness=10' >> /etc/sysctl.conf\n   \n   # 优化网络参数\n   echo 'net.core.rmem_max = 134217728' >> /etc/sysctl.conf\n   echo 'net.core.wmem_max = 134217728' >> /etc/sysctl.conf\n   \n   # 应用配置\n   sysctl -p\n   ```\n\n2. **Spark配置优化**\n   ```bash\n   # spark-defaults.conf\n   spark.executor.memory=2g\n   spark.executor.cores=2\n   spark.sql.adaptive.enabled=true\n   spark.sql.adaptive.coalescePartitions.enabled=true\n   ```\n\n**监控和调优：**\n\n1. **性能基线测试**\n   ```bash\n   # CPU基准测试\n   sysbench cpu --cpu-max-prime=20000 run\n   \n   # 内存测试\n   sysbench memory --memory-total-size=10G run\n   \n   # 磁盘I/O测试\n   dd if=/dev/zero of=testfile bs=1G count=1 oflag=direct\n   ```\n\n2. **实时监控**\n   - 使用htop监控CPU和内存\n   - 使用iotop监控磁盘I/O\n   - 使用nethogs监控网络使用\n\n**结果验证：**\n- Spark作业执行时间减少30%\n- 系统响应性显著提升\n- 资源利用率更加均衡\n\n**维护建议：**\n- 定期清理临时文件\n- 监控虚拟机资源使用趋势\n- 根据工作负载调整资源分配'''
    }
}

try:
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("开始添加VMware使用指南模块...")
    
    # 1. 调整现有模块的顺序（将所有模块的ord+1）
    print("调整现有模块顺序...")
    cursor.execute('UPDATE modules SET ord = ord + 1')
    
    # 2. 插入VMware模块（ord=1，排在最前面）
    vmware_module_title = 'VMware虚拟化环境搭建'
    vmware_module_desc = 'VMware Workstation安装配置、虚拟机创建、网络设置、端口映射与性能优化'
    
    cursor.execute('''
        INSERT INTO modules (title, description, ord) 
        VALUES (?, ?, ?)
    ''', (vmware_module_title, vmware_module_desc, 1))
    
    vmware_module_id = cursor.lastrowid
    print(f"VMware模块已创建，ID: {vmware_module_id}")
    
    # 3. 为VMware模块创建5个主题
    for topic_ord in range(1, 6):
        content = vmware_content[topic_ord]
        topic_title = content['title']
        
        # 插入主题
        cursor.execute('''
            INSERT INTO topics (module_id, title, ord) 
            VALUES (?, ?, ?)
        ''', (vmware_module_id, topic_title, topic_ord))
        
        topic_id = cursor.lastrowid
        
        # 准备内容数据
        content_data = {
            'title': topic_title,
            'theory': content['theory'],
            'code': content['code'],
            'case': content['case'],
            'exercises': [
                f"练习1：根据{topic_title}的内容，完成相关的实践操作",
                f"练习2：总结{topic_title}中的关键配置参数和最佳实践",
                f"练习3：设计一个基于{topic_title}的实际应用场景"
            ],
            'images': [
                'https://images.unsplash.com/photo-1518779578993-ec3579fee39f',
                'https://images.unsplash.com/photo-1519389950473-47ba0277781c'
            ]
        }
        
        # 插入内容
        cursor.execute('''
            INSERT INTO contents (topic_id, data) 
            VALUES (?, ?)
        ''', (topic_id, json.dumps(content_data, ensure_ascii=False)))
        
        print(f"  主题 {topic_ord}: {topic_title} 已创建")
    
    conn.commit()
    
    # 4. 验证结果
    print("\n验证模块顺序:")
    cursor.execute('SELECT id, title, ord FROM modules ORDER BY ord')
    modules = cursor.fetchall()
    
    for module in modules:
        module_id, title, ord_num = module
        print(f"  {ord_num}. {title} (ID: {module_id})")
    
    print("\n验证VMware模块主题:")
    cursor.execute('''
        SELECT t.id, t.title, t.ord 
        FROM topics t 
        WHERE t.module_id = ? 
        ORDER BY t.ord
    ''', (vmware_module_id,))
    
    topics = cursor.fetchall()
    for topic in topics:
        topic_id, title, ord_num = topic
        print(f"  {ord_num}. {title} (ID: {topic_id})")
    
    conn.close()
    print("\nVMware模块添加成功！")
    
except Exception as e:
    print(f"错误: {e}")
    if 'conn' in locals():
        conn.rollback()
        conn.close()