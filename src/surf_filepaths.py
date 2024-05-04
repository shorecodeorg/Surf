#kevin fink
#kevin@shorecode.org
#Sun Apr 28 06:40:48 PM +07 2024
#kevin fink
#kevin@shorecode.org
#Fri Mar  8 02:06:54 PM +07 2024
#.py

import os
import platform
from dataclasses import dataclass

@dataclass
class Files:
    current_platform = platform.system()
    filepaths = ['logging/surf.log', 'data/images/sc.png', 'surf_main.py',
                 'not used', 'data/images/close.png']
    win_filepaths = list()
    for f in filepaths:
        f = f.replace('/', '\\')
        f = os.path.dirname(os.path.abspath(__file__)) + '\\' + f
        win_filepaths.append(f)
    for f in filepaths:
        idx = filepaths.index(f)
        f = os.path.dirname(os.path.abspath(__file__)) + '/' + f
        filepaths.pop(idx)
        filepaths.insert(idx, f)

    def get_files_list(self) -> list:
        if self.current_platform == 'Windows':
            return self.win_filepaths
        else:
            return self.filepaths
        
    def get_file_by_index(self, idx: int) ->list:
        if self.current_platform == 'Windows':
            return self.win_filepaths[idx]
        else:
            return self.filepaths[idx]
