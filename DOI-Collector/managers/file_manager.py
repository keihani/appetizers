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
