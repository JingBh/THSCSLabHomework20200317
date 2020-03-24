from get_path import get_path


class Progress:

    def __init__(self, path="database/progress.dat"):
        self.path = get_path(path)
        try:
            handler = open(self.path, "r")
            self.progress = float(handler.read())
            handler.close()
        except Exception:
            self.progress = 0

    def set(self, number):
        self.progress = float(number)
        handler = open(self.path, "w")
        handler.write(str(self.progress))
        handler.close()

    def get(self):
        return self.progress

    def clear(self):
        self.set(0)
