"""
Exile UI Vietnamese Language Installer
Tự động cài đặt gói tiếng Việt cho Exile UI
"""

import os
import shutil
import subprocess
import tempfile
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


def show_error_and_open_repo():
    """Hiển thị thông báo lỗi và mở repo Exile UI"""
    root = tk.Tk()
    root.withdraw()

    result = messagebox.showinfo(
        "Thiếu Exile UI",
        "Vui lòng bấm vào nút OK tải về Exile UI, sau đó khởi chạy lại từ thư mục gốc của Exile UI"
    )
    webbrowser.open("https://github.com/Lailloken/Exile-UI")
    root.destroy()
    return False


def show_success():
    """Hiển thị thông báo thành công"""
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Thành công", "THÀNH CÔNG. Đã có lvling tiếng việt!")
    root.destroy()


def clone_repo(temp_dir):
    """Clone repo exile_ui_vi vào thư mục tạm"""
    repo_url = "https://github.com/chunn112/exile_ui_vi"

    try:
        print("Đang tải xuống gói tiếng Việt...")
        subprocess.run(
            ["git", "clone", repo_url, temp_dir],
            check=True,
            capture_output=True,
            text=True
        )
        print("✓ Tải xuống thành công")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Lỗi khi clone repo: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("✗ Lỗi: Git chưa được cài đặt. Vui lòng cài đặt Git trước.")
        return False


def check_data_folder():
    """Kiểm tra xem thư mục /data có tồn tại không"""
    current_dir = Path.cwd()
    data_dir = current_dir / "data"

    if not data_dir.exists():
        print("✗ Không tìm thấy thư mục /data")
        return False

    print(f"✓ Tìm thấy thư mục /data tại: {data_dir}")
    return True


def copy_leveltracker_guide(temp_dir):
    """Copy file leveltracker guide vào /data/english"""
    source_file = Path(temp_dir) / "vi" / "[leveltracker] default guide.json"
    dest_dir = Path.cwd() / "data" / "english"
    dest_file = dest_dir / "[leveltracker] default guide.json"

    try:
        dest_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy2(source_file, dest_file)
        print(f"✓ Đã copy leveltracker guide vào {dest_file}")
        return True
    except FileNotFoundError as e:
        print(f"✗ Lỗi: Không tìm thấy file {source_file}")
        return False
    except Exception as e:
        print(f"✗ Lỗi khi copy leveltracker guide: {e}")
        return False


def copy_font(temp_dir):
    """Copy font NotoSans-Regular.ttf vào /data"""
    source_file = Path(temp_dir) / "NotoSans-Regular.ttf"
    dest_dir = Path.cwd() / "data"
    dest_file = dest_dir / "NotoSans-Regular.ttf"

    try:
        shutil.copy2(source_file, dest_file)
        print(f"✓ Đã copy font vào {dest_file}")
        return True
    except FileNotFoundError:
        print(f"✗ Lỗi: Không tìm thấy file {source_file}")
        return False
    except Exception as e:
        print(f"✗ Lỗi khi copy font: {e}")
        return False


def modify_ahk_file():
    """Sửa file Exile Ui.ahk để sử dụng font tiếng Việt"""
    ahk_file = Path.cwd() / "Exile Ui.ahk"

    if not ahk_file.exists():
        print(f"✗ Không tìm thấy file {ahk_file}")
        return False

    try:
        with open(ahk_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original = 'alt_font : "Fontin-SmallCaps.ttf"'
        replacement = 'alt_font := "NotoSans-Regular.ttf"'

        if original in content:
            content = content.replace(original, replacement)
            print(f"✓ Tìm thấy và sửa: {original}")
        else:
            print("⚠ Không tìm thấy pattern chính xác, đang thử các pattern khác...")

            import re
            pattern = r'vars\.system\.font\s*:=\s*"[^"]*"'
            matches = re.findall(pattern, content)

            if matches:
                print(f"  Tìm thấy: {matches[0]}")
                content = re.sub(pattern, replacement, content)
                print(f"✓ Đã sửa thành: {replacement}")
            else:
                print("✗ Không tìm thấy dòng vars.system.font trong file")
                return False

        with open(ahk_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Đã cập nhật file {ahk_file}")
        return True

    except Exception as e:
        print(f"✗ Lỗi khi sửa file AHK: {e}")
        return False


def cleanup_temp_dir(temp_dir):
    """Xóa thư mục tạm đã clone"""
    import stat

    def handle_remove_readonly(func, path, _exc):
        """Xử lý file readonly/locked trên Windows"""

        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception:
            pass

    try:
        shutil.rmtree(temp_dir, onerror=handle_remove_readonly)
        print("✓ Đã xóa thư mục tạm")
        return True
    except Exception as e:
        print(f"⚠ Cảnh báo: Không thể xóa thư mục tạm {temp_dir}: {e}")
        print("  (Bạn có thể xóa thủ công sau)")
        return False


def main():
    """Hàm chính của installer"""
    print("=" * 60)
    print("Exile UI - Vietnamese Language Installer")
    print("=" * 60)
    print()

    if not check_data_folder():
        show_error_and_open_repo()
        return

    temp_dir = tempfile.mkdtemp(prefix="exile_ui_vi_")
    print(f"Thư mục tạm: {temp_dir}")
    print()

    try:

        if not clone_repo(temp_dir):
            print("Cài đặt thất bại!")
            return
        print()

        if not copy_leveltracker_guide(temp_dir):
            print("Cài đặt thất bại!")
            return

        if not copy_font(temp_dir):
            print("Cài đặt thất bại!")
            return

        if not modify_ahk_file():
            print("Cài đặt thất bại!")
            return

        print()
        print("=" * 60)

        cleanup_temp_dir(temp_dir)

        show_success()

    except Exception as e:
        print(f"✗ Lỗi không mong đợi: {e}")
        cleanup_temp_dir(temp_dir)


if __name__ == "__main__":
    main()
