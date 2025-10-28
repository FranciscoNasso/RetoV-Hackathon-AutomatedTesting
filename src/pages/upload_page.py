class UploadPage:
    def __init__(self, page):
        self.page = page
        # Observed input id on /explorer
        self.upload_input_selector = 'input#fileUpload'
        self.submit_button_selector = 'button[type="submit"]'
        self.success_message_selector = '.success-message'

    def upload_file(self, file_path):
        # fileUpload is hidden in the page; use locator set_input_files directly
        self.page.locator(self.upload_input_selector).set_input_files(file_path)
        # If the page requires a submit button click
        self.page.locator(self.submit_button_selector).click()

    def is_upload_successful(self):
        return self.page.locator(self.success_message_selector).is_visible()
