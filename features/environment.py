from behave import fixture, use_fixture
from playwright.sync_api import sync_playwright

@fixture
def browser_context(context):
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)
    context._playwright = pw
    context.browser = browser
    context.page = browser.new_page()
    yield context.page
    context.page.close()
    context.browser.close()
    pw.stop()

def before_scenario(context, scenario):
    use_fixture(browser_context, context)

def after_scenario(context, scenario):
    # cleanup if necessary
    pass
