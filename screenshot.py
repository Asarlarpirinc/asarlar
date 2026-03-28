import asyncio
import os
from playwright.async_api import async_playwright

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "temporary screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def take_screenshots():
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # Desktop
        ctx_desktop = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await ctx_desktop.new_page()
        await page.goto("file:///" + os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html")).replace("\\", "/"))
        await page.wait_for_timeout(1200)
        # Scroll through page to trigger IntersectionObserver animations
        height = await page.evaluate("document.body.scrollHeight")
        step = 600
        pos = 0
        while pos < height:
            await page.evaluate(f"window.scrollTo(0, {pos})")
            await page.wait_for_timeout(120)
            pos += step
        await page.evaluate("window.scrollTo(0, 0)")
        # Force all fade-in elements visible
        await page.evaluate("""
          document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
          document.querySelectorAll('.counter').forEach(el => {
            el.textContent = el.dataset.target + (el.dataset.suffix || '');
          });
        """)
        await page.wait_for_timeout(800)
        path_d = os.path.join(OUTPUT_DIR, "screenshot-1-desktop.png")
        await page.screenshot(path=path_d, full_page=True)
        print(f"Saved: {path_d}")
        await ctx_desktop.close()

        # Mobile
        ctx_mobile = await browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        page_m = await ctx_mobile.new_page()
        await page_m.goto("file:///" + os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html")).replace("\\", "/"))
        await page_m.wait_for_timeout(1200)
        height_m = await page_m.evaluate("document.body.scrollHeight")
        pos_m = 0
        while pos_m < height_m:
            await page_m.evaluate(f"window.scrollTo(0, {pos_m})")
            await page_m.wait_for_timeout(120)
            pos_m += 500
        await page_m.evaluate("window.scrollTo(0, 0)")
        await page_m.evaluate("""
          document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
          document.querySelectorAll('.counter').forEach(el => {
            el.textContent = el.dataset.target + (el.dataset.suffix || '');
          });
        """)
        await page_m.wait_for_timeout(800)
        path_m = os.path.join(OUTPUT_DIR, "screenshot-2-mobile.png")
        await page_m.screenshot(path=path_m, full_page=True)
        print(f"Saved: {path_m}")
        await ctx_mobile.close()

        await browser.close()
        print("Done.")

asyncio.run(take_screenshots())
