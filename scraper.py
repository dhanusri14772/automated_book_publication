import asyncio
from playwright.async_api import async_playwright
import os

async def scrape_chapter(url, output_dir="data", screenshot_dir="screenshots"):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        await page.wait_for_selector("#mw-content-text")

        content = await page.inner_text("#mw-content-text")

        filename = "chapter_1.txt" 

        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            f.write(content)

        screenshot_path = os.path.join(screenshot_dir, filename.replace(".txt", ".png"))
        await page.screenshot(path=screenshot_path, full_page=True)

        await browser.close()

        print(f"[+] Scraped and saved: {filename}")
        print(f"[+] Screenshot saved to: {screenshot_path}")
        
        return os.path.join(output_dir, filename)  

if __name__ == "__main__":
    test_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    asyncio.run(scrape_chapter(test_url))
