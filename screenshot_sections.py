import asyncio, os
from playwright.async_api import async_playwright

OUT = os.path.join(os.path.dirname(__file__), "temporary screenshots")
os.makedirs(OUT, exist_ok=True)

HTML = "file:///" + os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html")).replace("\\", "/")

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await ctx.new_page()
        await page.goto(HTML)
        await page.wait_for_timeout(1200)
        # Force all visible
        await page.evaluate("""
          document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
          document.querySelectorAll('.counter').forEach(el => {
            el.textContent = el.dataset.target + (el.dataset.suffix || '');
          });
        """)
        await page.wait_for_timeout(500)

        total_height = await page.evaluate("document.body.scrollHeight")
        sections = ["hero", "kurumsal", "stats", "urunler", "ges", "sertifika", "iletisim", "footer"]
        step = total_height // len(sections)

        force_js = """
          document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
          document.querySelectorAll('.counter').forEach(el => {
            el.textContent = el.dataset.target + (el.dataset.suffix || '');
          });
        """
        for i, name in enumerate(sections):
            y = i * step
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(2100)  # animation duration is 1800ms
            await page.evaluate(force_js)
            await page.wait_for_timeout(100)
            path = os.path.join(OUT, f"section-{name}.png")
            await page.screenshot(path=path)
            print(f"Saved: {path}")

        await browser.close()

asyncio.run(run())
