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
from managers import AppController

if __name__ == "__main__":
    dois_file = os.path.join("data", "dois.txt")
    snapshots_file = os.path.join("data", "paper_snapshots.txt")

    app = AppController(dois_file, snapshots_file)
    app.run_menu()