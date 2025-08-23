import os
from managers import AppController

if __name__ == "__main__":
    dois_file = os.path.join("data", "dois.txt")
    snapshots_file = os.path.join("data", "paper_snapshots.txt")

    app = AppController(dois_file, snapshots_file)
    app.run_menu()