class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate_to(self, url):
        self.page.goto(url)

    def get_title(self):
        return self.page.title()

    def is_visible(self, selector):
        return self.page.is_visible(selector)

    def click(self, selector):
        self.page.click(selector)

    def fill(self, selector, value):
        self.page.fill(selector, value)

    def upload_file(self, selector, file_path):
        self.page.set_input_files(selector, file_path)

    def download_file(self, selector):
        self.page.click(selector)  # Assuming this initiates a download

    def wait_for_download(self, download):
        return download.path()  # Wait for the download to complete
