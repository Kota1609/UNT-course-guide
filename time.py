import asyncio
import json
from playwright.async_api import async_playwright

# Paste your cookies JSON here as a raw string.
cookie_json_str = r'''
[
  {
    "domain": ".unt.edu",
    "expirationDate": 1774991276,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_clck",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "16nxvyy%7C2%7Cfuo%7C0%7C1902",
    "id": 1
  },
  {
    "domain": ".unt.edu",
    "expirationDate": 1778015275.781525,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.1.1978387267.1741895987",
    "id": 2
  },
  {
    "domain": ".unt.edu",
    "expirationDate": 1778015357.591055,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga_33TTT716N7",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GS1.1.1743455275.9.0.1743455357.60.0.0",
    "id": 3
  },
  {
    "domain": ".unt.edu",
    "expirationDate": 1777134183.520824,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga_7F0QY2CKEC",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GS1.1.1742574135.2.1.1742574183.0.0.0",
    "id": 4
  },
  {
    "domain": ".unt.edu",
    "expirationDate": 1777737319.634848,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga_G0SYP4K3L7",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GS1.1.1743177177.10.1.1743177319.43.0.0",
    "id": 5
  },
  {
    "domain": ".unt.edu",
    "expirationDate": 1776455987.263625,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga_L43QLTR42Q",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GS1.1.1741895987.1.0.1741895987.0.0.0",
    "id": 6
  },
  {
    "domain": ".unt.edu",
    "expirationDate": 1777737174.398573,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga_RYXSNRFSV9",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GS1.1.1743177172.10.0.1743177174.0.0.0",
    "id": 7
  },
  {
    "domain": ".unt.edu",
    "expirationDate": 1778015357.576247,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga_VFVM0814BD",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GS1.1.1743455263.3.0.1743455357.0.0.0",
    "id": 8
  },
  {
    "domain": ".unt.edu",
    "expirationDate": 1776455987.579627,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga_XQ61LLKTHQ",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GS1.1.1741895987.1.0.1741895987.0.0.0",
    "id": 9
  },
  {
    "domain": ".unt.edu",
    "expirationDate": 1749671987,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_gcl_au",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1.1.1748274845.1741895987",
    "id": 10
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "ExpirePage",
    "path": "/",
    "sameSite": "strict",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "https://my.unt.edu/psp/ps/",
    "id": 11
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "FSPD-PORTAL-PSJSESSIONID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "R_r4FSze3XFCg6EPA-VQE5rIyIfrxWq1!165646837",
    "id": 12
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "gbpa_campususer",
    "path": "/",
    "sameSite": "strict",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "NT",
    "id": 13
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "gbpa_usersiteid",
    "path": "/",
    "sameSite": "strict",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "NT752",
    "id": 14
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "hrpd",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "rd671o00000000000000000000ffff0a9c443ao7103",
    "id": 15
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "HRPD-PORTAL-PSJSESSIONID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "O8v4FSzMYk8CesE-D0ALEOlWB3lg3HPF!-2049352079",
    "id": 16
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "myfs",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "rd671o00000000000000000000ffff0a9c442do7101",
    "id": 17
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "myhr",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "rd671o00000000000000000000ffff0a9c4438o7101",
    "id": 18
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "myunt",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "rd671o00000000000000000000ffff0a9c4410o7101",
    "id": 19
  },
  {
    "domain": ".unt.edu",
    "expirationDate": 1776455987.633544,
    "hostOnly": false,
    "httpOnly": false,
    "name": "nmstat",
    "path": "/",
    "sameSite": "lax",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "b4140d07-12e4-f1a4-a1cd-ed609cc73a5b",
    "id": 20
  },
  {
    "domain": ".unt.edu",
    "expirationDate": 1778183760.165639,
    "hostOnly": false,
    "httpOnly": false,
    "name": "PS_DEVICEFEATURES",
    "path": "/",
    "sameSite": "strict",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "width:3440 height:1440 pixelratio:0.8999999761581421 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0",
    "id": 21
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "PS_LASTSITE",
    "path": "/",
    "sameSite": "strict",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "https://my.unt.edu/psc/ps_24/",
    "id": 22
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": false,
    "name": "PS_LOGINLIST",
    "path": "/",
    "sameSite": "strict",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "https://my.unt.edu/ps",
    "id": 23
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "PS_TOKEN",
    "path": "/",
    "sameSite": "strict",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "ogAAAAQDAgEBAAAAvAIAAAAAAAAsAAAABABTaGRyAk4Aawg4AC4AMQAwABT6mXyA7P9MuXjERIa/CuWShc1i/mIAAAAFAFNkYXRhVnicHYnBDkAwEAWnJQ4O/kRDW+Iu1ZtIcPYBftHHeekeZnZ2X6CurDHyZynTZm4SJxdNYifTHapN/bBqi54Bz0Qvx0IvjqITZzHo5vTz6kUO8ANazAse",
    "id": 24
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": false,
    "name": "PS_TOKENEXPIRE",
    "path": "/",
    "sameSite": "strict",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "2_Apr_2025_22:16:39_GMT",
    "id": 25
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "PS_TokenSite",
    "path": "/",
    "sameSite": "strict",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "https://my.unt.edu/psc/ps_24/?SELFSRV-LSPD-PORTAL-PSJSESSIONID",
    "id": 26
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": false,
    "name": "psback",
    "path": "/",
    "sameSite": "strict",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "%22%22url%22%3A%22https%3A%2F%2Fmy.unt.edu%2Fpsc%2Fps_26%2FEMPLOYEE%2FSA%2Fc%2FSSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL%3Fpage%3DSSR_CLSRCH_ES_FL%22%20%22label%22%3A%22Class%20Search%20Results%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%221%22%20%22refurl%22%3A%22https%3A%2F%2Fmy.unt.edu%2Fpsc%2Fps_26%2FEMPLOYEE%2FSA%22%22",
    "id": 27
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": false,
    "name": "resolution",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "3440",
    "id": 28
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "SELFSRV-LSPD-PORTAL-PSJSESSIONID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "zTf4k86GlVAJww_f5klVPppnR-MqSL8j!-1476482429",
    "id": 29
  },
  {
    "domain": ".unt.edu",
    "hostOnly": false,
    "httpOnly": true,
    "name": "SignOnDefault",
    "path": "/",
    "sameSite": "strict",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "",
    "id": 30
  },
  {
    "domain": "my.unt.edu",
    "hostOnly": true,
    "httpOnly": false,
    "name": "ps_theme",
    "path": "/",
    "sameSite": "strict",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "node:SA portal:EMPLOYEE theme_id:NT_DEFAULT_THEME_FLUID_860 css:NT_DEFAULT_THEME_FLUID_860 accessibility:N macroset:NT_DEFAULT_MACROSET_860 formfactor:3 piamode:2",
    "id": 31
  }
]
'''

async def main():
    # Load cookies from JSON string.
    cookie_list = json.loads(cookie_json_str)
    # Build cookies for Playwright.
    cookies = []
    for cookie in cookie_list:
        cookies.append({
            "name": cookie["name"],
            "value": cookie["value"],
            "domain": cookie["domain"],
            "path": cookie["path"]
        })

    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        print("Adding cookies...")
        await context.add_cookies(cookies)
        print("Cookies added.")
        
        print("Creating new page...")
        page = await context.new_page()
        search_url = (
            "https://my.unt.edu/psc/ps_24/EMPLOYEE/SA/c/SSR_STUDENT_FL."
            "SSR_CLSRCH_ES_FL.GBL?Page=SSR_CLSRCH_ES_FL&SEARCH_GROUP=SSR_CLASS_SEARCH_LFF"
            "&SEARCH_TEXT=csce%205&ES_INST=NT752&ES_STRM=1251&ES_ADV=N&INVOKE_SEARCHAGAIN=PTSF_GBLSRCH_FLUID"
        )
        print("Navigating to search URL...")
        await page.goto(search_url)
        
        print("Waiting for network idle...")
        await page.wait_for_load_state("networkidle")
        
        try:
            print("Waiting for course elements...")
            await page.wait_for_selector("div.ps-list-item", timeout=15000)
            print("Course elements found.")
        except Exception as e:
            print("Course elements not found:", e)
        
        content = await page.content()
        print("Page content fetched (first 1000 characters):")
        print(content[:1000])
        
        courses = await page.query_selector_all("div.ps-list-item")
        print("Found", len(courses), "course elements.")
        
        await browser.close()

asyncio.run(main())
