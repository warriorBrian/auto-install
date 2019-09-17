#!/usr/bin/python
#-*- coding:UTF-8 -*-
import subprocess
import os
import commands
import time
import signal
import platform

#==============================
# System Required: Centos6+/Debian && Centos7/Debian
# Description: Install package
# Version: 0.1.0
# Author: Brian Lee
#==============================

# 获取项目根目录
def getRootPath():
    rootPath = os.path.dirname(os.path.abspath(__file__))
    return rootPath

# 输出颜色函数
def inred(s):

    return"%s\033[31m%s%s[0m"%(chr(27), s, chr(27))

def ingreen(s):

    return"%s[\033[32m%s%s[0m"%(chr(27), s, chr(27))

def inyellow(s):
    return"%s[\033[33m%s%s[0m"%(chr(27), s, chr(27))

def inblue(s):

    return"%s[\033[34m%s%s[0m"%(chr(27), s, chr(27))

def inpouple(s):

    return"%s[\033[35m%s%s[0m"%(chr(27), s, chr(27))

# 捕获ctrl + c 终止程序
def signal_handler(signal,frame):
    print(inred('\n程序终止，退出脚本'))
    exit(0)
 
signal.signal(signal.SIGINT,signal_handler)

# **************************************************************
# 检查是否安装wget

def checkWget():
    print(inblue('检查wget安装情况...'))
    (wget, output) = commands.getstatusoutput('wget --help')
    if wget != 0:
        subprocess.call(['yum', 'install', 'wget', '-y'], shell=False)
    else:
        print(inblue('wget存在,继续执行安装'))

# **************************************************************
# 卸载node版本 && 更换版本
def replaceNode():
    while(True):
        uninstall = raw_input(inyellow('是否卸载当前版本Node,请输入[y/n]:'))
        if (uninstall == 'y'):
            checkNodeExist()
            time.sleep(0.5)
            break
        elif uninstall == 'n':
            break
        else:
            print(inred('输入错误，重新输入'))
# 检查是否安装node
def checkNode():
    print(inblue('检查Node环境...'))
    time.sleep(1)
    (node, nodeOutput) = commands.getstatusoutput('node -v')
    if node != 0:
        print(inred('node环境未安装，开始安装'))
        # 检查wget是否存在
        checkWget()
        time.sleep(1)
        plat = UsePlatform()
        if plat == 1:
            print(inred('下载msi包，手动安装程序：') + "https://npm.taobao.org/mirrors/node/v10.16.2/node-v10.16.2-x64.msi")
        elif plat == 2:
            # linux环境，执行安装Node
            installNode()
        elif plat == 3:
            print(inred('下载pkg包，手动安装程序：') + "https://npm.taobao.org/mirrors/node/v10.16.2/node-v10.16.2.pkg")
    else:
        print('Node Version:' + ingreen(nodeOutput))

def checkCnpm():
    while(True):
        cnpm = raw_input(inyellow('是否安装cnpm? 请输入[y/n]:'))
        if cnpm == 'y':
            # npm install -g cnpm --registry=https://registry.npm.taobao.org
            subprocess.call(['npm', 'install', '-g', 'cnpm', '--registry=https://registry.npm.taobao.org'], shell=False)
            (cnpmCode, cnpmOutput) = commands.getstatusoutput('cnpm -v')
            if cnpmCode == 0:
                print(inblue('cnpm安装成功'))
                print(cnpmOutput)
            else:
                print(inred('安装失败，尝试写入变量添加alias参数'))
                time.sleep(1)
                subprocess.call('alias cnpm="npm --registry=https://registry.npm.taobao.org --cache=$HOME/.npm/.cache/cnpm --disturl=https://npm.taobao.org/dist --userconfig=$HOME/.cnpmrc"', shell=True)
                time.sleep(0.5)
                print(cnpmOutput)
            break
        elif cnpm == 'n':
            break
        else:
            print(inred('输入错误，重新输入'))
# **************************************************************
# 安装Node环境
def installNode():
    node_str = raw_input(inyellow('输入Node版本号(例如: 10.16.0)：'))
    # 检查Node文件环境
    checkNodeExist()
    time.sleep(1)
    subprocess.call(['wget', '-P', '/usr/', 'https://nodejs.org/dist/v'+node_str+'/node-v'+node_str+'-linux-x64.tar.gz'], shell=False)
    subprocess.call(['tar', '-zxvf', '/usr/node-v'+node_str+'-linux-x64.tar.gz', '-C', '/usr'], shell=False)
    subprocess.call(['mv', '/usr/node-v'+node_str+'-linux-x64', '/usr/node'], shell=False)
    subprocess.call(['sudo', 'ln', '-s', '/usr/node/bin/node', '/usr/local/bin/node'], shell=False)
    subprocess.call(['sudo', 'ln', '-s', '/usr/node/bin/npm', '/usr/local/bin/npm'], shell=False)
    print(inblue('写入环境变量...'))
    time.sleep(0.5)
    subprocess.call('echo -e "export PATH=$(npm prefix -g)/bin:$PATH" >> ~/.bashrc && source ~/.bashrc', shell=True)
    time.sleep(0.5)
    subprocess.call(['rm','-rf', '/usr/node-v'+node_str+'-linux-x64.tar.gz'], shell=False)
    # 重新检查Node环境是否安装成功
    checkNode()
    time.sleep(0.5)
    # 检查是否安装cnpm
    checkCnpm()

# 检查Node环境文件夹是否重复
def checkNodeExist():
    packagePath = '/usr/local/bin/'
    print(inblue('删除node压缩包及安装包...'))
    time.sleep(0.5)
    subprocess.call(['rm', '-rf', '/usr/node'], shell=False)
    (Nodestatus, findNodeOutput) = commands.getstatusoutput('find '+packagePath+' -name node')
    if (Nodestatus == 0 and len(findNodeOutput) != 0):
        print(inblue('删除node软链接,重新创建...'))
        time.sleep(0.5)
        subprocess.call(['rm', '-rf',''+packagePath+'npm'], shell=False)
        subprocess.call(['rm', '-rf',''+packagePath+'node'], shell=False)
    print(inblue('环境清空完毕'))
# **************************************************************
# 检测操作系统，环境安装
def UsePlatform():
  sysstr = platform.system()
  if(sysstr =="Windows"):
      return 1
  elif(sysstr == "Linux"):
      return 2
  elif(sysstr == "Darwin"):
      return 3
  else:
      print(inred('检测系统非Linux环境，暂不支持，退出程序'))
      exit(0)

# **************************************************************
# 安装Nginx
def installNginx():
    plat = UsePlatform()
    if plat == 2:
        (NginxStatus, NginxOutput) = commands.getstatusoutput('nginx -v')
        (NginxSystemStatus, NginxSystemOutput) = commands.getstatusoutput('systemctl status nginx.service')
        if NginxStatus == 0:
            # 已经安装nginx
            print('已经安装nginx')
        else:
            # 安装nginx
            subprocess.call(['yum', 'install', 'nginx', '-y'], shell=False)
            if NginxSystemStatus == 768:
                print(inblue('程序没有运行，正在唤醒nginx程序运行...'))
                subprocess.call(['systemctl', 'start', 'nginx'], shell=False)
            elif NginxSystemStatus == 0:
                print('安装目录为' + ingreen('/etc/nginx'))
                time.sleep(1)
                print(ingreen('程序运行，显示状态:'))
                print(NginxSystemOutput)
    else:
        print(inred('Nginx其他平台安装请相关查阅资料，暂不支持自动安装'))

# 卸载Nginx
def continueRemoveNginx():
    (NginxStatus, NginxOutput) = commands.getstatusoutput('nginx -v')
    (NginxSystemStatus, NginxSystemOutput) = commands.getstatusoutput('systemctl status nginx.service')
    (NginxPackageStatus, NginxPackageOutput) = commands.getstatusoutput('rpm -qa | grep nginx')
    if NginxStatus == 0:
        subprocess.call(['systemctl', 'stop', 'nginx.service'], shell=False)
        time.sleep(0.5)
        if NginxSystemStatus == 768:
            print(ingreen('停止后台任务成功，执行卸载程序...'))
            time.sleep(1)
            subprocess.call(['yum', 'remove', 'nginx', '-y'], shell=False)
            print(inblue('擦除依赖包...'))
            time.sleep(0.5)
            subprocess.call('rpm -e --nodeps `rpm -qa | grep nginx`', shell=True)
            time.sleep(1)
            print(ingreen('依赖包清空完毕'))   
        else:
            print(inblue('卸载Nginx脚本执行中...'))
            time.sleep(0.5)
            subprocess.call(['yum', 'remove', 'nginx', '-y'], shell=False)
            print(inblue('擦除依赖包...'))
            time.sleep(0.5)
            subprocess.call('rpm -e --nodeps `rpm -qa | grep nginx`', shell=True)
    else:
        print(ingreen('检测已经被卸载完毕'))

# 卸载Nginx确认
def removeNginx():
    while(True):
        uninstall = raw_input(inyellow('是否卸载当前版本Nginx,'+inred('(可能会导致配置丢失或者正在运行程序停止！)')+inyellow('请输入[y/n]:')))
        if (uninstall == 'y'):
            continueRemoveNginx()
            time.sleep(0.5)
            break
        elif uninstall == 'n':
            break
        else:
            print(inred('输入错误，重新输入'))
# **************************************************************
# 安装Mongodb && 卸载mongodb
def removeMongo():
    while(True):
        uninstall = raw_input(inyellow('是否卸载当前版本MongoDB,'+inred('(可能会导致数据丢失或者正在运行程序停止！)')+inyellow('请输入[y/n]:')))
        if (uninstall == 'y'):
            checkMongo()
            break
        elif uninstall == 'n':
            break
        else:
            print(inred('输入错误，重新输入'))

def continueInstallMongo():
    (MongoStatus, MongoOutput) = commands.getstatusoutput('mongo --version')
    if MongoStatus == 0:
        print(inred('检测MongoDB存在，请先执行6，卸载MongoDB'))
    else:
        while(True):
            print(inyellow('输入3对应版本 Version:3.6, 输入4对应版本 Version:4.0.1'))
            install = raw_input('输入MongoDB版本[3/4]：')
            if install in ['3', '4']:
                executeInstallMongo(install)
                break
            else:
                print(inred('输入错误，请重新输入'))

def executeInstallMongo(version):
    subprocess.call('rm -f /etc/yum.repos.d/mongodb-org-*', shell=True)
    time.sleep(1)
    # 检查是否安装wget
    checkWget()
    time.sleep(1)
    print(inblue('拉取repo镜像源...'))
    time.sleep(1)
    if version == '3':
        subprocess.call('wget http://images.brianlee.cn/mongodb-org-3.6.repo -P /etc/yum.repos.d/', shell=True)
    elif version == '4':
        subprocess.call('wget http://images.brianlee.cn/mongodb-org-4.0.repo -P /etc/yum.repos.d/', shell=True)
    else:
        pass
    #subprocess.call(['wget', 'http://images.brianlee.cn/mongodb-org-'+version+'.0.repo', '&&', 'mv', 'mongodb-org-'+version+'.0.repo', '/etc/yum.repo.d/'], shell=False)
    print(inblue('执行安装MongoDB...'))
    time.sleep(1)
    subprocess.call(['yum', 'install', 'mongodb-org', '-y'], shell=False)
    print(inblue('开启后台程序'))
    subprocess.call(['systemctl', 'stop', 'mongod.service'], shell=False)
    time.sleep(1)
    subprocess.call(['systemctl', 'start', 'mongod.service'], shell=False)
    time.sleep(2)
    (MongoExtStatus, MongoExtOutput) = commands.getstatusoutput('mongo --version')
    #print(inblue('安装状态码:') + MongoExtStatus)
    if MongoExtStatus == 0:
        print(ingreen('安装成功，打印版本信息：'))
        print(MongoExtOutput)
        time.sleep(1)
        print(inblue('输出后台运行状态:'))
        time.sleep(0.5)
        subprocess.call(['systemctl', 'status', 'mongod.service'], shell=False)
    else:
        print(inred('安装失败，需要手动解决错误'))
        #subprocess.call(['systemctl', '--failed'], shell=False)
        subprocess.call(['systemctl', 'status', 'mongod.service'], shell=False)

# 检查及卸载mongodb
def checkMongo():
    (MongoSystemStatus, MongoSystemOutput) = commands.getstatusoutput('systemctl status mongod.service')
    subprocess.call(['systemctl', 'stop', 'mongod.service'], shell=False)
    print(inblue('停止后台任务成功，执行卸载程序...'))
    time.sleep(1)
    subprocess.call(['yum', 'remove', 'mongodb-org', '-y'],shell=False)
    print(inblue('擦除依赖包...'))
    time.sleep(0.5)
    print(inblue('擦除数据库文件...'))
    time.sleep(0.5)
    subprocess.call(['rm', '-rf', '/data/db'], shell=False)
    print(inblue('擦除日志文件防止冲突...'))
    time.sleep(0.5)
    subprocess.call(['rm', '-rf', '/var/log/mongodb'], shell=False)
    print(inblue('擦除所有rpm包'))
    time.sleep(1)
    subprocess.call('rpm -e --nodeps `rpm -qa | grep mongodb`', shell=True)
    time.sleep(1)
    print(ingreen('依赖包清空完毕'))
# **************************************************************
# 安装mysql
def installMysql():
    print(inblue('检查依赖包状态...'))
    time.sleep(1)
    subprocess.call('rpm -qa | grep mysql',shell=True)
    time.sleep(1)
    print(inblue('删除Mysql依赖包...'))
    subprocess.call('rpm -e --nodeps `rpm -qa | grep mysql`', shell=True)
    time.sleep(1)
    # 检查是否安装wget
    checkWget()
    print(inblue('删除无用安装包'))
    time.sleep(0.5)
    subprocess.call('rm -rf /usr/mysql-community-release-el7-5.noarch.rpm', shell=True)
    subprocess.call(['wget', 'http://mirrors.ustc.edu.cn/mysql-repo/mysql-community-release-el7-5.noarch.rpm', '-P', '/usr/'], shell=False)
    print(inblue('执行安装mysql...'))
    subprocess.call('rpm -ivh /usr/mysql-community-release-el7-5.noarch.rpm', shell=True)
    print(inblue('执行yum更新程序，请稍后...'))
    time.sleep(1)
    subprocess.call(['yum', 'update', '-y'], shell=False)
    time.sleep(1)
    print(inblue('安装mysql中...'))
    subprocess.call(['yum', 'install', 'mysql-server', '-y'], shell=False)
    print(inblue('设置文件夹权限...'))
    time.sleep(1)
    subprocess.call('chown mysql:mysql -R /var/lib/mysql', shell=True)
    print(inblue('初始化MySQL中...'))
    subprocess.call(['mysqld', '--initialize'], shell=False)
    print(inblue('启动MySQL中...'))
    time.sleep(1)
    subprocess.call(['systemctl', 'start', 'mysqld'], shell=False)
    print(inblue('返回MySQL运行状态'))
    time.sleep(0.5)
    subprocess.call(['systemctl', 'status', 'mysqld'], shell=False)
    print(inblue('删除无用安装包'))
    time.sleep(0.5)
    subprocess.call('rm -rf /usr/mysql-community-release-el7-5.noarch.rpm', shell=True)
    print(inblue('返回MySQL版本信息'))
    time.sleep(0.5)
    subprocess.call(['mysqladmin', '--version'],shell=False)

# 卸载mysql
def askRemoveMysql():
    while(True):
        uninstall = raw_input(inyellow('是否卸载当前版本MySQL,'+inred('(可能会导致数据丢失或者正在运行程序停止！)')+inyellow('请输入[y/n]:')))
        if (uninstall == 'y'):
            removeMysql()
            break
        elif uninstall == 'n':
            break
        else:
            print(inred('输入错误，重新输入'))

def removeMysql():
    print(inblue('停止MySQL后台运行'))
    time.sleep(0.5)
    subprocess.call(['systemctl', 'stop', 'mysqld'], shell=False)
    print(inblue('清理所有安装包环境'))
    time.sleep(1)
    subprocess.call('rpm -e --nodeps `rpm -qa | grep mysql`', shell=True)
    (mysqlExtStatus, mysqlExtOutput) = commands.getstatusoutput('mysqladmin --version')
    if mysqlExtStatus != 0:
        print(ingreen('清理成功'))
    else:
        print(inred('清理失败'))
        print(mysqlExtOutput)
# **************************************************************
# 更换源
def replaceSource():
    # 检查是否安装wget
    checkWget()
    print(inblue('执行备份源...'))
    subprocess.call('rm -rf /etc/yum.repos.d/CentOS-Base.repo.backup', shell=True)
    time.sleep(1)
    subprocess.call('mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup', shell=True)
    print(inblue('覆盖base源'))
    time.sleep(1)
    subprocess.call('wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo', shell=True)
    print(inblue('生成缓存...'))
    time.sleep(1)
    subprocess.call('yum clean all && yum makecache', shell=True)
    print(inblue('yum更新'))
    time.sleep(1)
    subprocess.call(['yum', 'update', '-y'], shell=False)

# **************************************************************
# 显示所有程序安装状态
def checkStatus():
    (NginxStatus, NginxOutput) = commands.getstatusoutput('nginx -v')
    (node, nodeOutput) = commands.getstatusoutput('node -v')
    nodeVersion = inred('未安装') if node != 0 else ingreen(nodeOutput)
    NginxVersion = inred('未安装') if NginxStatus != 0 else ingreen(NginxOutput)
    print('Node版本为：' + nodeVersion)
    print('Nginx版本为：' + NginxVersion)
# 显示菜单项
def show_menu():
    print((ingreen('*') * 20)+'一键自动安装程序'+(ingreen('*') * 20))
    print('Github: ' + inblue('https://github.com/warriorBrian/auto-install'))
    print('\n')
    print(ingreen('1.') + '安装NodeJs环境')
    print(ingreen('2.') + '安装Nginx')
    print(ingreen('3.') + '安装MongoDB 3 / 4版本')
    print(ingreen('4.') + '安装MySQL程序')
    print(ingreen('5.') + 'yum更换阿里源')
    print('')
    print(ingreen('6.') + '卸载NodeJs环境')
    print(ingreen('7.') + '卸载Nginx')
    print(ingreen('8.') + '卸载MongoDB')
    print(ingreen('9.') + '卸载MySQL程序')
    print('\n')
    print(ingreen('0.') + '退出安装程序')
    # 显示安装信息开始
    print('\n')
    print('-' * 56)
    checkStatus()
    print('-' * 56)
    # 显示安装信息结束
    print(ingreen('*') * 56)

while True:
    # 显示操作菜单
    show_menu()
    time.sleep(0.5)
    action_str = raw_input('请选择希望执行的操作：')
    if action_str in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        time.sleep(0.5)
        subprocess.call(['clear'], shell=False)
        if (action_str == '1'):
            # 安装node
            checkNode()
        elif (action_str == '2'):
            # 安装nginx
            installNginx()
        elif (action_str == '3'):
            # 安装mongo
            continueInstallMongo()
        elif (action_str == '4'):
            # 安装mysql
            installMysql()
        elif (action_str == '5'):
            # 更换阿里源
            replaceSource()
        elif (action_str == '6'):
            # 卸载node
            replaceNode()
        elif (action_str == '7'):
            # 卸载nginx
            removeNginx()
        elif (action_str == '8'):
            # 卸载mongo
            removeMongo()
        elif (action_str == '9'):
            # 卸载mysql
            askRemoveMysql()
    elif action_str == '0':
        exit(0)
    else:
        time.sleep(0.5)
        subprocess.call(['clear'], shell=False)
        print(inred('输入错误,请重新选择'))

# **************************************************************