# DOI-Collector v.25
# SPDX-License-Identifier: MIT
#
# Author: Kevin Keihani
# Company: Soroush Fanavari Co
# Contact: yz.keihani@gmail.com
# GitHub:  https://github.com/keihani
# LinkedIn: https://linkedin.com/in/keihani
#
# This file is part of DOI-Collector v.25, an open source project.

import os
import stat
import platform
import subprocess


class FileManager:
    """Handles file operations and permissions."""

    @staticmethod
    def set_writable(file_path):
        """Remove read-only attribute (make file writable)."""
        if not os.path.exists(file_path):
            return
        if platform.system() == "Windows":
            subprocess.call(["attrib", "-R", file_path])
        else:  # Linux/macOS
            os.chmod(file_path, stat.S_IWRITE | stat.S_IREAD)

    @staticmethod
    def set_readonly(file_path):
        """Set read-only attribute."""
        if not os.path.exists(file_path):
            return
        if platform.system() == "Windows":
            subprocess.call(["attrib", "+R", file_path])
        else:  # Linux/macOS
            os.chmod(file_path, stat.S_IREAD)

    @staticmethod
    def count_dois(dois_file):
        """Count how many DOIs are stored (excluding the project name line)."""
        try:
            with open(dois_file, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                return len(lines) - 1 if lines else 0
        except FileNotFoundError:
            return 0

    @staticmethod
    def ensure_project_name(dois_file, snapshots_file):
        """Ensure both files exist and start with 'project name:'."""

        def check_or_set_project(file_path, project_name=None):
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                if not project_name:
                    project_name = input("Enter project name: ").strip()
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"project name: {project_name}\n")
                return project_name

            with open(file_path, "r+", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if not first_line.lower().startswith("project name:"):
                    if not project_name:
                        project_name = input("Enter project name: ").strip()
                    rest = f.read()
                    f.seek(0)
                    f.write(f"project name: {project_name}\n")
                    f.write(rest)
            return project_name

        project_name = check_or_set_project(dois_file)
        check_or_set_project(snapshots_file, project_name)

    @staticmethod
    def read_file(file_path):
        """Read and return file content as string (or None if not found/empty)."""
        if not os.path.isfile(file_path):
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        return content if content else None

    @staticmethod
    def write_file(file_path, content):
        """Write string content to file (overwrite)."""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def append_file(file_path, content):
        """Append string content to a file (creates it if not exists)."""
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)
# ...existing code...

    @staticmethod
    def is_admin():
        """Check if the script is running with administrator/root privileges."""
        try:
            if platform.system() == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except Exception:
            return False

    @staticmethod
    def request_admin():
        """Request administrator/root privileges to rerun the script if not already elevated."""
        if FileManager.is_admin():
            return True
        print("⚠️ Administrator privileges are required. Attempting to elevate...")
        try:
            if platform.system() == "Windows":
                import sys
                ctypes = __import__('ctypes')
                params = ' '.join([f'"{arg}"' for arg in sys.argv])
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, params, None, 1)
                return False
            else:
                import sys
                os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
        except Exception as e:
            print(f"❌ Failed to elevate privileges: {e}")
            return False
        
    @staticmethod
    def maximize_console():
        """Maximize the console window (works in .exe too)."""
        if platform.system() == "Windows":
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                user32 = ctypes.windll.user32
                hWnd = kernel32.GetConsoleWindow()
                if hWnd:
                    SW_RESTORE = 9
                    SW_MAXIMIZE = 3
                    user32.ShowWindow(hWnd, SW_RESTORE)   # ensure visible
                    user32.ShowWindow(hWnd, SW_MAXIMIZE)  # maximize
                else:
                    print("⚠️ No console window found.")
            except Exception as e:
                print(f"⚠️ Failed to maximize console: {e}")

    @staticmethod
    def clear_screen():
        """Clear console screen (cross-platform)."""
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")