class HomePage:
    def __init__(self, page):
        self.page = page
        self.url = "https://exohunter.earth/home"

    def navigate(self):
        self.page.goto(self.url)

    def get_title(self):
        return self.page.title()

    def click_explore(self):
        # Use the correct selector for the explore action
        self.page.locator('a[routerlink="/explorer"]').first.click()

    def click_download(self):
        self.page.click("text=Download")

    def click_upload(self):
        self.page.click("text=Upload")
