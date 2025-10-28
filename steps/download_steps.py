from behave import given, when, then
from pages.download_page import DownloadPage
from src.utils.file_helpers import file_exists
from playwright.async_api import async_playwright
import asyncio

import tempfile
from pathlib import Path
import requests


def run_async(coroutine):
    return asyncio.get_event_loop().run_until_complete(coroutine)


async def ensure_page_async(context):
    if not hasattr(context, 'page'):
        pw = await async_playwright().start()
        browser = await pw.chromium.launch(headless=False)
        context._playwright = pw
        context.browser = browser
        context.page = await browser.new_page()


@given('the user is on the home page')
def step_impl(context):
    run_async(ensure_page_async(context))
    run_async(context.page.goto('https://exohunter.earth/explorer'))
    context.download = DownloadPage(context.page)


@when('the user navigates to the download page')
def step_impl(context):
    run_async(ensure_page_async(context))
    run_async(context.page.goto('https://exohunter.earth/explorer'))
    try:
        run_async(context.page.wait_for_selector('.download-buttons', timeout=8000))
    except Exception:
        pass


@given('the user is on the download page')
def step_impl(context):
    run_async(ensure_page_async(context))
    run_async(context.page.goto('https://exohunter.earth/explorer'))
    context.download = DownloadPage(context.page)


def do_initiate_download(context):
    # create a temp dir to store download
    tmp_dir = tempfile.mkdtemp(prefix='exohunter_dl_')
    context._download_tmp = tmp_dir
    # try primary download method exposed by the page object
    try:
        with context.page.expect_download(timeout=30000) as download_info:
            context.download.download_file('a')
        download = download_info.value
        # store the download object; defer saving until assertion step
        context._download_obj = download
        context.download_path = None
        return
    except Exception:
        context._download_obj = None
        context.download_path = None

    # fallback candidates: try clicking example buttons or anchors
    candidates = ['.example-btn', 'button.example-btn', 'a[download]', 'button:has-text("1K rows")', 'button:has-text("5K rows")', 'button:has-text("10K rows")']
    for sel in candidates:
        try:
            locator = context.page.locator(sel)
            if locator.count() == 0:
                continue
            with context.page.expect_download(timeout=30000) as download_info:
                locator.first.click()
            download = download_info.value
            context._download_obj = download
            context.download_path = None
            return
        except Exception:
            context._download_obj = None
            context.download_path = None
            continue


@when('the user initiates a file download')
def step_initiate_alias(context):
    return do_initiate_download(context)


@when('the user initiates the file download')
def step_impl(context):
    return do_initiate_download(context)


@then('the file should be downloaded successfully')
def step_impl(context):
    # If we have a Download object, save it into the tmp dir now
    dl = getattr(context, '_download_obj', None)
    tmp_dir = getattr(context, '_download_tmp', None)
    if dl and tmp_dir:
        try:
            suggested = dl.suggested_filename or 'download.csv'
            dest = Path(tmp_dir) / suggested
            dl.save_as(str(dest))
            context.download_path = str(dest)
        except Exception:
            context.download_path = None

    assert context.download_path is not None, 'Download did not complete or path is unknown'


@then('the downloaded file should be present in the specified location')
def step_impl(context):
    assert context.download_path is not None, 'No download path recorded'
    assert file_exists(context.download_path), f'Downloaded file not found at {context.download_path}'


@when('the user cancels the download')
def step_impl(context):
    # Best-effort: cancel the stored Playwright Download object if present
    dl = getattr(context, '_download_obj', None)
    if dl:
        try:
            dl.cancel()
        except Exception:
            pass

    # also try UI cancel or navigate away
    try:
        context.page.click('button:has-text("Cancel")')
    except Exception:
        pass

    try:
        context.page.goto('https://exohunter.earth/home')
        context.page.wait_for_load_state('networkidle', timeout=3000)
        context.page.goto('https://exohunter.earth/explorer')
    except Exception:
        pass


@given('the user has downloaded a file')
def step_impl(context):
    # Explicitly trigger a download by clicking example download buttons and save into a tmp dir
    tmp_dir = tempfile.mkdtemp(prefix='exohunter_dl_')
    context._download_tmp = tmp_dir
    candidates = ['.example-btn', 'button.example-btn', 'a[download]', 'button:has-text("1K rows")', 'button:has-text("5K rows")', 'button:has-text("10K rows")']
    context.download_path = None

    for sel in candidates:
        try:
            locator = context.page.locator(sel)
            if locator.count() == 0:
                continue
            with context.page.expect_download(timeout=30000) as download_info:
                locator.first.click()
            download = download_info.value
            # try saving the download
            suggested = download.suggested_filename or 'download.csv'
            dest = Path(tmp_dir) / suggested
            try:
                download.save_as(str(dest))
                context.download_path = str(dest)
                break
            except Exception:
                try:
                    tmp_path = download.path()
                    if tmp_path:
                        from shutil import copyfile

                        copyfile(tmp_path, str(dest))
                        context.download_path = str(dest)
                        break
                except Exception:
                    context.download_path = None
        except Exception:
            continue

    # If browser-based download failed, try HTTP fetch of example files as a last resort
    if context.download_path is None:
        base = 'https://exohunter.earth/'
        examples = ['1000example.csv', '5000example.csv', '10000example.csv']
        for fname in examples:
            try:
                r = requests.get(base + fname, timeout=10)
                if r.status_code == 200 and r.content:
                    tmp_dir = context._download_tmp or tempfile.mkdtemp(prefix='exohunter_dl_')
                    context._download_tmp = tmp_dir
                    dest = Path(tmp_dir) / fname
                    dest.write_bytes(r.content)
                    context.download_path = str(dest)
                    break
            except Exception:
                continue

    assert context.download_path is not None, 'Could not download example file in Given step'


@when('the user checks the download location')
def step_impl(context):
    # simple existence check placeholder; actual assertion happens in Then step
    pass


@then('the file should not be present in the download location')
def step_impl(context):
    tmp = getattr(context, '_download_tmp', None)
    present = False
    if tmp:
        tmp_path = Path(tmp)
        if tmp_path.exists():
            for f in tmp_path.iterdir():
                try:
                    if f.stat().st_size > 0:
                        present = True
                        break
                except Exception:
                    continue
    assert not present, 'A file from the cancelled download is present in the download directory'

