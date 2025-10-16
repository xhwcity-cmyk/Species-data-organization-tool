# build.py
import platform
import subprocess
import sys
import os
import shutil
from pathlib import Path

# 全局常量定义
APP_NAME = "SpeciesProcessor"
FINAL_APP_NAME = "物种数据整理工具"


def build_app():
    # 获取当前操作系统
    current_os = platform.system()

    # 主脚本路径
    script_path = "plant_matrix_gui.py"  # 替换为您的脚本文件名

    # 图标路径（可选）
    icon_path = "app_icon.ico" if current_os == "Windows" else "app_icon.icns"

    # PyInstaller 命令
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", APP_NAME,
        "--distpath", "dist",
        "--workpath", "build",
        "--specpath", "build",
        "--clean",
        "--noconfirm"
    ]

    # 添加图标
    if os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])

    # 添加 openpyxl 数据文件（正确格式）
    openpyxl_path = get_openpyxl_path()
    if openpyxl_path:
        # 使用正确的路径分隔符格式
        sep = ";" if current_os == "Windows" else ":"
        data_arg = f"{openpyxl_path}{sep}openpyxl"
        cmd.extend(["--add-data", data_arg])

    # 添加主脚本
    cmd.append(script_path)

    # 打印命令用于调试
    print("执行打包命令:")
    print(" ".join(cmd))

    # 执行打包命令
    try:
        result = subprocess.run(cmd, check=True, stderr=subprocess.STDOUT)
        if result.returncode == 0:
            print(f"\n✅ 打包成功！应用程序位于: dist/{APP_NAME}")

            # 重命名应用程序
            if current_os == "Darwin":
                # macOS 应用
                app_path = Path("dist") / f"{APP_NAME}.app"
                if app_path.exists():
                    final_path = Path("dist") / f"{FINAL_APP_NAME}.app"
                    if final_path.exists():
                        shutil.rmtree(final_path)
                    app_path.rename(final_path)
                    print(f"重命名为: {final_path}")
                    print("在 macOS 上，应用程序是 .app 文件")
                else:
                    print("⚠️ 警告: 未找到生成的 .app 文件")
            elif current_os == "Windows":
                # Windows 应用
                exe_path = Path("dist") / f"{APP_NAME}.exe"
                if exe_path.exists():
                    final_path = Path("dist") / f"{FINAL_APP_NAME}.exe"
                    if final_path.exists():
                        os.remove(final_path)
                    exe_path.rename(final_path)
                    print(f"重命名为: {final_path}")
                    print("在 Windows 上，应用程序是 .exe 文件")
                else:
                    print("⚠️ 警告: 未找到生成的 .exe 文件")
        else:
            print("\n❌ 打包失败")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 打包失败: {e}")
        if hasattr(e, 'output') and e.output:
            try:
                print(f"错误输出: {e.output.decode('utf-8')}")
            except:
                print(f"错误输出: {e.output}")
    except Exception as e:
        print(f"\n❌ 打包过程中发生错误: {str(e)}")
        import traceback
        print(traceback.format_exc())


def get_openpyxl_path():
    """获取 openpyxl 包的安装路径"""
    try:
        import openpyxl
        path = os.path.dirname(openpyxl.__file__)
        print(f"找到 openpyxl 路径: {path}")
        return path
    except ImportError:
        print("警告: 未找到 openpyxl 包")
        # 尝试在常见位置查找
        python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
        possible_paths = [
            f"venv/lib/{python_version}/site-packages/openpyxl",
            f"venv/Lib/site-packages/openpyxl",
            f"Lib/site-packages/openpyxl"
        ]

        for path in possible_paths:
            if os.path.exists(path):
                print(f"找到 openpyxl 路径: {path}")
                return path

        print("未找到 openpyxl 路径，跳过 --add-data 参数")
        return None


def clean_build():
    """清理构建目录"""
    print("清理旧构建文件...")

    # 清理目录
    for dir_name in ["build", "dist"]:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"已清理目录: {dir_name}")
            except Exception as e:
                print(f"清理目录 {dir_name} 失败: {str(e)}")

    # 清理 .spec 文件
    spec_file = f"{APP_NAME}.spec"
    if os.path.exists(spec_file):
        try:
            os.remove(spec_file)
            print(f"已清理文件: {spec_file}")
        except Exception as e:
            print(f"清理文件 {spec_file} 失败: {str(e)}")


if __name__ == "__main__":
    # 清理旧构建
    clean_build()

    # 开始打包
    print("\n开始打包应用程序...")
    build_app()

    # 打包完成提示
    print("\n打包过程完成！")
    if platform.system() == "Darwin":
        app_path = Path("dist") / f"{FINAL_APP_NAME}.app"
        if app_path.exists():
            print(f"macOS 用户: 请将 '{app_path.name}' 文件复制到应用程序文件夹")
        else:
            print("⚠️ 警告: 未找到生成的应用程序文件")
    elif platform.system() == "Windows":
        exe_path = Path("dist") / f"{FINAL_APP_NAME}.exe"
        if exe_path.exists():
            print(f"Windows 用户: 请将 '{exe_path.name}' 文件发送给用户使用")
        else:
            print("⚠️ 警告: 未找到生成的应用程序文件")
    else:
        print("打包完成，请在 dist 目录中查看生成的文件")