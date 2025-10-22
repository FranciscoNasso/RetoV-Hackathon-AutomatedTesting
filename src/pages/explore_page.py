class ExplorePage:
    def __init__(self, page):
        self.page = page

    def navigate_to_page(self, page_name):
        self.page.click(f'nav >> text={page_name}')

    def get_page_title(self):
        return self.page.title()

    def explore_feature(self, feature_name):
        self.page.click(f'button >> text={feature_name}')

    def is_feature_visible(self, feature_name):
        return self.page.is_visible(f'button >> text={feature_name}')
