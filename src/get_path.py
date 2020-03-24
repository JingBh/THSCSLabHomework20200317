from os.path import realpath


def get_path(path):
    """将相对于项目根目录的路径转换为绝对路径"""
    return realpath(__file__ + "/../../" + path)
