class InvalidArgumentException(Exception):
    def __init__(self):
        self.message = ("Please enter the site link as an argument. "
                        "Example usage: 'python resources/main.py https://www.example.com'")
        super().__init__(self.message)


class InvalidURLException(Exception):
    def __init__(self):
        self.message = "You entered an invalid URL, please check it and enter it again. valid url template: https://www.example.com"
        super().__init__(self.message)
