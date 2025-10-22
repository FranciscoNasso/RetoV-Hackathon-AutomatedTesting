class HomePage:
    def __init__(self, page):
        self.page = page
        self.url = "https://exohunter.earth/home"

    def navigate(self):
        self.page.goto(self.url)

    def get_title(self):
        return self.page.title()

    def click_explore(self):
        # try common selectors for the explore action
        selectors = [
            'a[routerlink="/explorer"]',
            'button[routerlink="/explorer"]',
            'text=Explore',
        ]
        for sel in selectors:
            try:
                locator = self.page.locator(sel)
                if locator.count() > 0:
                    locator.first.click()
                    return
            except Exception:
                continue
        # fallback: click any element containing 'Explore'
        try:
            self.page.click('text=Explore')
        except Exception:
            pass

    def click_download(self):
        self.page.click("text=Download")

    def click_upload(self):
        self.page.click("text=Upload")
