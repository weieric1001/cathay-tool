import os
import time
from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
UID = os.environ.get("UID")
KEY = os.environ.get("KEY")
time_set = 60*5

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width":800,"height":600})
    page = context.new_page()
    page.goto("https://w3.cathaylife.com.tw/eai/ZPWeb/login.jsp")
    page.locator("#UID").click()
    page.locator("#UID").fill(UID)
    page.locator("#KEY").click()
    page.locator("#KEY").fill(KEY)
    page.get_by_text("登入", exact=True).click()
    print(f'UID：{UID} -> 登入成功', end='\n\n')
    page.get_by_role("link", name="行政資源").click(delay=3000)
    page.get_by_role("link", name="學習與發展").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="國泰學習網").click()
    page1 = page1_info.value
    page1.locator("button").filter(has_text="menu").click(delay=3000)
    page1.get_by_role("link", name="我的學習歷程").click()
    page1.get_by_role("link", name="待修課程").click()
    time.sleep(3)
    list1 = page1.locator("h3.ma-0.pa-0.el-word-break").all_inner_texts()
    print(f'待修課程: {list1}', end='\n\n')

    for i in list1:
        page1.get_by_role("link", name=i, exact=True).click()
        time.sleep(3)
        list2 = page1.locator("a.el-word-break.ng-star-inserted").all_inner_texts()
        list2 = list2[1:]
        print(f'待修單元: {list2}')
        pbar = tqdm(list2, total=len(list2)*time_set)
        for j in list2:
            pbar.set_description(f"{j}")
            try:
                with page1.expect_popup() as page2_info:
                    page1.get_by_role("link", name=j, exact=True).click()
                page2 = page2_info.value
                for t in range(time_set):
                    time.sleep(1)
                    pbar.update(1)
                page2.close()
                # print('-> Finished')
            except Exception as ex:
                print(f' -> {j}: Error ({ex})')
                pass


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
