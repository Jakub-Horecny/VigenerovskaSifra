class FileManager:

    def __init__(self):
        self.path: str = "files/text1_enc.txt"

    def load_data(self) -> list:
        result: list = []
        with open(self.path, "r") as file:
            while True:
                line = file.readline().strip()
                if not line:
                    break
                result.append(line)
        return result
