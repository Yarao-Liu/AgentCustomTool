#!/usr/bin/env python3
"""
Python 打包脚本
提供两种打包方式供用户选择
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_step(step, message):
    """打印步骤信息"""
    print(f"\n{'='*50}")
    print(f"[{step}] {message}")
    print('='*50)

def clean_build_files():
    """清理构建文件"""
    print_step("1/4", "清理构建文件")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name, ignore_errors=True)
            print(f"✓ 删除目录: {dir_name}")
    
    # 清理spec文件
    for spec_file in Path('.').glob('*.spec'):
        try:
            spec_file.unlink()
            print(f"✓ 删除文件: {spec_file}")
        except:
            pass

def check_dependencies():
    """检查项目文件"""
    print_step("2/4", "检查项目文件")
    
    required_files = ['main.py', 'config.py', 'config.ini']
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"× {file} 不存在")
            return False
    return True

def try_cx_freeze():
    """使用cx_Freeze打包"""
    print_step("3/4", "使用 cx_Freeze 打包")
    
    try:
        # 安装cx_Freeze
        print("安装 cx_Freeze...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'cx_Freeze'], 
                      check=True, capture_output=True)
        
        # 创建setup.py
        setup_content = '''
from cx_Freeze import setup, Executable
import sys

packages = ["fastapi", "uvicorn", "pydantic", "starlette", "configparser"]
include_files = [("config.ini", "config.ini"), ("module/", "module/")]

build_exe_options = {
    "packages": packages,
    "include_files": include_files,
    "excludes": ["matplotlib", "numpy", "pandas", "tkinter"],
}

executables = [Executable("main.py", base=None, target_name="MindmapFileService.exe")]

setup(
    name="MindmapFileService",
    version="1.0.0",
    options={"build_exe": build_exe_options},
    executables=executables
)
'''
        
        with open('setup.py', 'w', encoding='utf-8') as f:
            f.write(setup_content)
        
        # 构建
        result = subprocess.run([sys.executable, 'setup.py', 'build'], 
                               capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # 查找生成的exe
            build_dir = Path('build')
            for exe_file in build_dir.rglob('MindmapFileService.exe'):
                print(f"✓ cx_Freeze 构建成功!")
                print(f"✓ 文件位置: {exe_file.absolute()}")
                return True
            
        print(f"× cx_Freeze 失败: {result.stderr}")
        return False
        
    except Exception as e:
        print(f"× cx_Freeze 失败: {str(e)}")
        return False

def try_pyinstaller():
    """使用PyInstaller打包"""
    print_step("3/4", "使用 PyInstaller 打包")
    
    try:
        # 安装PyInstaller
        print("安装 PyInstaller...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], 
                      check=True, capture_output=True)
        
        # PyInstaller命令
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            '--console', 
            '--name=MindmapFileService',
            '--add-data=config.ini;.',
            '--add-data=module;module',
            '--noconfirm',
            'main.py'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        exe_path = Path('dist/MindmapFileService.exe')
        if exe_path.exists():
            print(f"✓ PyInstaller 构建成功!")
            print(f"✓ 文件位置: {exe_path.absolute()}")
            return True
        else:
            print(f"× PyInstaller 失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"× PyInstaller 失败: {str(e)}")
        return False

def try_nuitka():
    """使用Nuitka打包"""
    print_step("3/4", "使用 Nuitka 打包")
    
    try:
        # 安装Nuitka
        print("安装 Nuitka...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'nuitka'], 
                      check=True, capture_output=True)
        
        # Nuitka命令
        cmd = [
            sys.executable, '-m', 'nuitka',
            '--onefile',
            '--standalone',
            '--include-package=fastapi',
            '--include-package=uvicorn', 
            '--include-data-dir=module=module',
            '--include-data-file=config.ini=config.ini',
            '--output-filename=MindmapFileService.exe',
            '--output-dir=dist',
            'main.py'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        exe_path = Path('dist/MindmapFileService.exe')
        if exe_path.exists():
            print(f"✓ Nuitka 构建成功!")
            print(f"✓ 文件位置: {exe_path.absolute()}")
            return True
        else:
            print(f"× Nuitka 失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"× Nuitka 失败: {str(e)}")
        return False

def verify_and_finalize():
    """验证并完成"""
    print_step("4/4", "完成打包")
    
    # 查找任何生成的exe文件
    exe_files = []
    for pattern in ['dist/*.exe', 'build/**/*.exe']:
        exe_files.extend(Path('.').glob(pattern))
    
    if exe_files:
        print("✓ 找到以下exe文件:")
        for exe_file in exe_files:
            size_mb = exe_file.stat().st_size / (1024*1024)
            print(f"  - {exe_file}: {size_mb:.1f} MB")
        
        print("\n" + "="*50)
        print("打包完成！")
        print("="*50)
        print("使用说明:")
        print("1. 确保已安装 Node.js 和 markmap-cli")
        print("2. 运行: npm install -g markmap-cli")
        print("3. 双击exe运行")
        return True
    else:
        print("× 打包失败")
        return False

def show_menu():
    """显示菜单"""
    print("\n" + "="*50)
    print("Python 打包工具")
    print("="*50)
    print("请选择打包方式:")
    print("1. cx_Freeze (推荐，包含依赖文件)")
    print("2. PyInstaller (单文件打包)")
    print("3. Nuitka (高性能编译打包)")
    print("="*50)

def main():
    """主函数"""
    print("Python 打包脚本")
    
    try:
        # 1. 清理文件
        clean_build_files()
        
        # 2. 检查依赖
        if not check_dependencies():
            print("× 项目文件检查失败")
            return False
        
        # 3. 显示菜单并获取用户选择
        while True:
            show_menu()
            choice = input("请输入选择 (1, 2 或 3): ").strip()
            
            if choice == '1':
                success = try_cx_freeze()
                break
            elif choice == '2':
                success = try_pyinstaller()
                break
            elif choice == '3':
                success = try_nuitka()
                break
            else:
                print("× 无效选择，请输入 1, 2 或 3")
                continue
        
        if success:
            verify_and_finalize()
            return True
        else:
            print("\n× 打包失败！")
            print("建议：")
            print("1. 尝试在 Python 3.9 环境中运行")
            print("2. 使用虚拟环境隔离依赖")
            print("3. 手动运行: python main.py")
            return False
        
    except KeyboardInterrupt:
        print("\n× 用户中断操作")
        return False
    except Exception as e:
        print(f"\n× 意外错误: {str(e)}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists('setup.py'):
            os.remove('setup.py')

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n构建失败！")
    input("按任意键退出...") 