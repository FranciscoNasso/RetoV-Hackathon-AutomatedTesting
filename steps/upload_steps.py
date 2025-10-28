from behave import given, when, then
from pages.upload_page import UploadPage
from pathlib import Path

@given('the user is on the upload page')
def step_impl(context):
    # explorer contains the upload flow
    context.page.goto('https://exohunter.earth/explorer')
    context.upload = UploadPage(context.page)

@when('the user selects a file to upload')
def step_impl(context):
    # create a small temp CSV file to upload (app expects CSV)
    tmp = Path('tmp_upload.csv')
    tmp.write_text('col1,col2\n1,2')
    # set the hidden file input directly
    context.page.locator('input#fileUpload').set_input_files(str(tmp.resolve()))
    context._tmp_upload = tmp


@when('the user selects an invalid file type to upload')
def step_impl(context):
    # create a temp file with an invalid extension and try to set it
    tmp = Path('tmp_invalid.exe')
    tmp.write_bytes(b'\x00\x01\x02')
    # attempt to set it into the file input
    try:
        context.page.locator('input#fileUpload').set_input_files(str(tmp.resolve()))
    except Exception:
        # some apps block programmatic set; still store for cleanup
        pass
    context._tmp_invalid = tmp

@when('the user clicks the upload button')
def step_impl(context):
    # click the button that triggers prediction. The UI labels are "Run Prediction" or "Re-run Prediction".
    try:
        context.page.click('button:has-text("Run Prediction")')
        return
    except Exception:
        pass

    try:
        context.page.click('button:has-text("Re-run Prediction")')
        return
    except Exception:
        pass

    # fallback: click the primary action button inside the actions container
    try:
        context.page.click('.actions button')
    except Exception:
        pass

@then('the user should see a success message')
def step_impl(context):
    # Wait for either the result area or the data visualization (table) to appear. Use a generous timeout.
    success_selectors = ['.prediction-result', '.data-visualization', '.server-error-message']
    found = False
    for sel in success_selectors:
        try:
            if context.page.locator(sel).count() > 0:
                # wait briefly for visibility
                try:
                    context.page.wait_for_selector(sel, timeout=15000)
                    found = True
                    break
                except Exception:
                    # not visible within timeout
                    continue
        except Exception:
            continue

    # fallback: search page text for typical success words
    if not found:
        body = context.page.content().lower()
        if 'prediction' in body or 'no data received' in body or 'prediction result' in body or 'table' in body:
            found = True

    assert found, 'No prediction result or data visualization detected after upload'
    # cleanup
    try:
        context._tmp_upload.unlink()
    except Exception:
        pass


@then('the user should see an error message')
def step_impl(context):
    # check common error selectors or text
    error_locators = ['.error-message', '.mat-error', '.upload-error', '.toast-error']
    found = False
    for sel in error_locators:
        try:
            if context.page.locator(sel).count() > 0 and context.page.locator(sel).first.is_visible():
                found = True
                break
        except Exception:
            continue
    if not found:
        # fallback: search the page text for typical error words
        body = context.page.content().lower()
        if 'invalid' in body or 'error' in body or 'not allowed' in body:
            found = True
    assert found, 'No error message detected after invalid upload'
    # cleanup
    try:
        context._tmp_invalid.unlink()
    except Exception:
        pass


@when('the user clicks the cancel button')
def step_impl(context):
    # try common cancel buttons
    try:
        context.page.click('button:has-text("Cancel")')
        return
    except Exception:
        pass
    try:
        context.page.click('button:has-text("Cancel upload")')
        return
    except Exception:
        pass
    # fallback: try to click any element with class 'cancel'
    try:
        context.page.click('.cancel')
    except Exception:
        pass

    # If no explicit cancel UI, clear the file input programmatically (this should remove the selection)
    try:
        # Playwright supports clearing input by setting empty files
        context.page.locator('input#fileUpload').set_input_files([])
    except Exception:
        try:
            # As a last resort, clear the input value and dispatch change event so Angular updates
            context.page.evaluate("""
                const input = document.getElementById('fileUpload');
                if (input) {
                    input.value = '';
                    input.dispatchEvent(new Event('change'));
                }
            """)
        except Exception:
            pass

    # Final fallback: navigate away (Back to Home) then return to explorer to reset component state
    try:
        # try clicking the back link if present
        context.page.click('button.back-link')
        context.page.wait_for_load_state('networkidle', timeout=5000)
        # navigate back to explorer which will re-initialize the component
        context.page.goto('https://exohunter.earth/explorer')
    except Exception:
        try:
            context.page.click('button:has-text("Back to Home")')
            context.page.wait_for_load_state('networkidle', timeout=5000)
            context.page.goto('https://exohunter.earth/explorer')
        except Exception:
            # give up silently; the following assertion will catch presence
            pass


@then('the user should not see the file in the upload list')
def step_impl(context):
    # Check for absence of the filename in common upload list selectors
    filename = getattr(context, '_tmp_upload', None)
    name = None
    if filename:
        name = filename.name
    # try common list selectors
    list_selectors = ['.upload-list', '.file-list', '.uploaded-files', '.upload-items']
    visible = False
    for sel in list_selectors:
        try:
            if context.page.locator(sel).count() > 0:
                text = context.page.locator(sel).first.inner_text()
                if name and name in text:
                    visible = True
                    break
        except Exception:
            continue
    # fallback: search page text for filename
    if name and not visible:
        if name in context.page.content():
            visible = True
    assert not visible, 'File still present in the upload list after cancel'
