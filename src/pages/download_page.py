class DownloadPage:
    def __init__(self, page):
        self.page = page

    def navigate_to_download_section(self):
        # The site exposes download buttons on explorer; navigate to explorer then find downloads
        self.page.goto("https://exohunter.earth/explorer")

    def download_file(self, file_link_selector):
        # Use the correct selector for the download action
        btn = self.page.locator('button:has-text("rows")')
        if btn.count() > 0:
            btn.first.click()
        else:
            self.page.click(file_link_selector)

    def verify_file_downloaded(self, file_name):
        # Logic to verify if the file has been downloaded
        pass
