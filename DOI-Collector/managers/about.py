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



class About:
    """Handles About information for the application."""

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

    def print_info(self):
        print(f"""
==========================================
 About {self.name} v.{self.version}
==========================================

{self.name} v.{self.version} is an Open Source software designed to help 
researchers and developers collect, manage, and organize DOIs efficiently.

Special thanks to:
- Crossref  
- Wiley  
- Elsevier  
- Springer Nature  
- Taylor & Francis  
- SAGE Publications  
- Oxford University Press  
- Cambridge University Press  
- IEEE (Institute of Electrical and Electronics Engineers)  

for providing free API access that powers this project.

Copyright © 2025 under the Open Source Software License.
This software is distributed under the terms of open source law and may be 
freely used, modified, and shared in accordance with the applicable license.

Developed and Maintained by:
👤 Kevin Keihani  
🏢 Soroush Fanavari Co  

📧 Email: yz.keihani@gmail.com  
🐙 GitHub: https://github.com/keihani  
🔗 LinkedIn: https://linkedin.com/in/keihani  

------------------------------------------
Contributions, feedback, and improvements 
are welcome. Please visit the GitHub 
repository to participate.
==========================================
""")
        input("👉 Press Enter to return to the menu...")

