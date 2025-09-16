from managers.doi_manager import DOIManager
from managers.file_manager import FileManager
from managers.internet_manager import InternetManager
from managers.about import About

class AppController:
    """Runs the CLI and handles user choices."""

    def __init__(self, dois_file, snapshots_file):
        self.dois_file = dois_file
        self.snapshots_file = snapshots_file
        self.doi_manager = DOIManager(dois_file, snapshots_file)

    def run_menu(self):
        InternetManager.wait_for_internet()

        FileManager.set_writable(self.dois_file)
        FileManager.set_writable(self.snapshots_file)

        FileManager.ensure_project_name(self.dois_file, self.snapshots_file)

        print(f"📊 Starting with {FileManager.count_dois(self.dois_file)} DOIs stored.\n")

        while True:
            # --- Show project name + DOI count each time we return ---
            content = FileManager.read_file(self.dois_file)
            project_name = "Unknown Project"
            if content:
                first_line = content.splitlines()[0]
                if first_line.lower().startswith("project name:"):
                    project_name = first_line.split(":", 1)[1].strip()

            total_dois = FileManager.count_dois(self.dois_file)
            print(f"\n📂 Project: {project_name} | 📊 DOIs stored: {total_dois}")

            print("\n📌 Please choose an option:")
            print("[1] - Add single DOI to the Library")
            print("[2] - Add batch DOIs")
            print("[3] - Find Automatic DOIs by Keywords")
            print("[4] - Add batch file to the Library")
            print("[5] - About")
            print("[6] - Exit")

            choice = input("👉 Enter your choice (1-6): ").strip()

            if choice == "1":
                print("🔖 Add single DOI")
                try:
                    while True:
                        InternetManager.wait_for_internet()
                        self.doi_manager.add_doi()
                        again = input("Do you want to add another DOI? (y/n): ").strip().lower()
                        if again != "y":
                            break
                finally:
                    FileManager.set_readonly(self.dois_file)
                    FileManager.set_readonly(self.snapshots_file)
                    print("🔒 Files set to read-only. Returning to menu...")

            elif choice == "2":
                print("📂 batch DOIs")
                self.doi_manager.batch_input_menu()

            elif choice == "3":
                print("🤖 Find Automatic")
                self.doi_manager.auto_lookup()

            elif choice == "4":
                print("📑 Add batch file to the Library")
                self.doi_manager.process_batch_file()

            elif choice == "5":
                print("ℹ️ About")
                about = About("DOI-Collector", "25.0")
                about.print_info()

            elif choice == "6":
                print("👋 Exiting program...")
                FileManager.set_readonly(self.dois_file)
                FileManager.set_readonly(self.snapshots_file)
                break

            else:
                print("⚠️ Invalid choice. Please select 1–5.")
