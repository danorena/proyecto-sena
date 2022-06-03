import sys

sys.path.append('../../')
def unEnroll(id,ficha):
    import os
    from controller.path import path
    exc = path() + f'model'
    os.chdir(exc)
    os.system(f'python unenroll.py --id {id} --conf datasets/attendance_system_dataset/{ficha}/config/config.json')