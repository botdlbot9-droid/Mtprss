import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess
from urllib.parse import quote

# Import your existing modules
from vars import API_ID, API_HASH, BOT_TOKEN, WEBHOOK, PORT
from aiohttp import ClientSession, web
from pyromod import listen
from subprocess import getstatusoutput
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from style import Ashu

# ========== CUSTOM DOWNLOAD FUNCTION (NO PROGRESS BAR ERRORS) ==========
async def download_video_direct(url, output_path, quality=None):
    """Download video using yt-dlp with quiet mode. Returns output path."""
    os.makedirs("downloads", exist_ok=True)
    if quality and "youtu" in url:
        fmt = f"b[height<={quality}][ext=mp4]/bv[height<={quality}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
    elif quality:
        fmt = f"b[height<={quality}]/bv[height<={quality}]+ba/b/bv+ba"
    else:
        fmt = "best"
    
    cmd = [
        "yt-dlp",
        "--quiet", "--no-progress",
        "-f", fmt,
        "-o", output_path,
        url
    ]
    
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    _, stderr = await process.communicate()
    
    if process.returncode != 0:
        raise Exception(f"yt-dlp error: {stderr.decode()}")
    
    # Check if file exists
    if os.path.exists(output_path):
        return output_path
    # Sometimes yt-dlp adds extension
    if not output_path.endswith('.mp4') and os.path.exists(output_path + '.mp4'):
        return output_path + '.mp4'
    raise Exception("Downloaded file not found")

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ========== WEBHOOK ROUTES ==========
routes = web.RouteTableDef()
@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("https://github.com/AshutoshGoswami24")
async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

# ========== BOT COMMANDS ==========
@bot.on_message(filters.command(["start"]))
async def start_cmd(bot: Client, m: Message):
    await m.reply_text(
        Ashu.START_TEXT,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✜ ᴀsʜᴜᴛᴏsʜ ɢᴏsᴡᴀᴍɪ 𝟸𝟺 ✜", url="https://t.me/AshutoshGoswami24")],
            [InlineKeyboardButton("🦋 𝐅𝐨𝐥𝐥𝐨𝐰 𝐌𝐞 🦋", url="https://t.me/AshuSupport")]
        ])
    )

@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("♦ 𝐒𝐭𝐨𝐩𝐩𝐞𝐭 ♦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["upload"]))
async def upload_handler(bot: Client, m: Message):
    editable = await m.reply_text('sᴇɴᴅ ᴍᴇ .ᴛxᴛ ғɪʟᴇ  ⏍')
    input_msg = await bot.listen(editable.chat.id)
    x = await input_msg.download()
    await input_msg.delete(True)

    try:
        with open(x, "r") as f:
            content = f.read()
        links = []
        for line in content.split("\n"):
            if line.strip():
                parts = line.split("://", 1)
                if len(parts) == 2:
                    links.append(parts)
        os.remove(x)
    except Exception:
        await m.reply_text("∝ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐢𝐥𝐞 𝐢𝐧𝐩𝐮𝐭.")
        if os.path.exists(x):
            os.remove(x)
        return

    await editable.edit(f"ɪɴ ᴛxᴛ ғɪʟᴇ ᴛɪᴛʟᴇ ʟɪɴᴋ 🔗 **{len(links)}**\n\nsᴇɴᴅ ғʀᴏᴍ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ɪɴɪᴛᴀʟ ɪs `1`")
    input0 = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("∝ 𝐍𝐨𝐰 𝐏𝐥𝐞𝐚𝐬𝐞 𝐒𝐞𝐧𝐝 𝐌𝐞 𝐘𝐨𝐮𝐫 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞")
    input1 = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)

    await editable.edit(Ashu.Q1_TEXT)
    input2 = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)

    # Resolution mapping
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080"
        else:
            res = "UN"
    except:
        res = "UN"

    await editable.edit(Ashu.C1_TEXT)
    input3 = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    MR = "️ ⁪⁬⁮⁮⁮" if raw_text3 == 'Robin' else raw_text3

    # Token for PW/ClassPlus
    await editable.edit("**Enter Your PW/Classplus Working Token\n\nOtherwise Send No**")
    input4 = await bot.listen(editable.chat.id)
    working_token = input4.text
    await input4.delete(True)

    await editable.edit(Ashu.T1_TEXT)
    input6 = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = raw_text6
    if thumb.startswith("http"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = "no"

    count = int(raw_text) if len(links) > 1 else 1

    # ========== MAIN LOOP ==========
    for i in range(count - 1, len(links)):
        title = links[i][0]
        url = "https://" + links[i][1]

        # Skip invalid links
        if not url.startswith(('http://','https://')) or 't.me/' in url:
            await m.reply_text(f"⚠️ Skipping invalid link: {title}")
            continue

        # ---------- Visionias ----------
        if "visionias" in url:
            async with ClientSession() as session:
                async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
                    text = await resp.text()
                    match = re.search(r"(https://.*?playlist.m3u8.*?)\"", text)
                    if match:
                        url = match.group(1)

        # ---------- ClassPlus (working) ----------
        elif any(x in url for x in ["classplusapp", "testbook.com", "classplusapp.com/drm", "media-cdn.classplusapp.com/drm"]):
            if working_token.lower() == "no":
                await m.reply_text(f"⚠️ Token required, skipping: {title}")
                continue
            if '&contentHashIdl=' not in url:
                await m.reply_text(f"❌ Invalid ClassPlus URL (missing contentHashIdl): {url[:100]}")
                continue
            base_url, contentId = url.split('&contentHashIdl=', 1)
            headers = {
                'host': 'api.classplusapp.com',
                'x-access-token': working_token,
                'accept-language': 'EN',
                'api-version': '18',
                'app-version': '1.4.73.2',
                'build-number': '35',
                'content-type': 'application/json',
                'device-details': 'Xiaomi_Redmi 7_SDK-32',
                'device-id': 'c28d3cb16bbdac01',
                'region': 'IN',
                'user-agent': 'Mobile-Android',
            }
            params = {'contentId': contentId, 'offlineDownload': "false"}
            try:
                resp = requests.get("https://api.classplusapp.com/cams/uploader/video/jw-signed-url", params=params, headers=headers).json()
                if 'error' in resp or 'Error' in resp:
                    await m.reply_text(f"❌ ClassPlus API error: {resp.get('error', resp.get('Error', 'Invalid token'))}")
                    continue
                if "testbook.com" in url or "classplusapp.com/drm" in url or "media-cdn.classplusapp.com/drm" in url:
                    url = resp['drmUrls']['manifestUrl']
                else:
                    url = resp["url"]
            except Exception as e:
                await m.reply_text(f"❌ ClassPlus API exception: {e}")
                continue

        # ---------- PW (PhysicsWallah) - NO MODIFICATION, JUST WRAP ----------
        elif "childId" in url and "parentId" in url:
            if working_token.lower() == "no":
                await m.reply_text(f"⚠️ PW token required, skipping: {title}")
                continue
            encoded_url = quote(url, safe='')
            url = f"https://anonymouspwplayer-907e62cf4891.herokuapp.com/pw?url={encoded_url}&token={working_token}"

        # ---------- No extra conversion for .mpd ----------
        # (We removed the /master.mpd block)

        # ---------- Prepare filename and caption ----------
        name1 = title.replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
        name = f'{str(count).zfill(3)}) {name1[:60]}'
        safe_name = name.replace(" ", "_").replace(")", "").replace("(", "")
        output_path = f"downloads/{safe_name}.mp4"

        cc = f'**[ 🎥 ] Vid_ID:** {str(count).zfill(3)}. {name1}{MR}\n✉️ 𝐁𝐚𝐭𝐜𝐡 » **{raw_text0}**'
        cc1 = f'**[ 📁 ] Pdf_ID:** {str(count).zfill(3)}. {name1}{MR}.pdf \n✉️ 𝐁𝐚𝐭𝐜𝐡 » **{raw_text0}**'

        # ---------- Download ----------
        try:
            if "drive.google.com" in url or "drive" in url:
                # If you have helper.download, you can use it; otherwise skip
                await m.reply_text(f"⚠️ Drive links not supported in this version. Skipping.")
                count += 1
                continue
            elif ".pdf" in url.lower():
                pdf_cmd = f'yt-dlp --quiet --no-progress -o "downloads/{safe_name}.pdf" "{url}"'
                subprocess.run(pdf_cmd, shell=True, check=True)
                await bot.send_document(m.chat.id, f"downloads/{safe_name}.pdf", caption=cc1)
                os.remove(f"downloads/{safe_name}.pdf")
                count += 1
            else:
                prog = await m.reply_text(f"❊⟱ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 ⟱❊ »\n\n📝 𝐍𝐚𝐦𝐞 » `{name}`\n⌨ 𝐐𝐮𝐥𝐢𝐭𝐲 » {raw_text2}\n\n**🔗 𝐔𝐑𝐋 »** `{url[:100]}...`")
                filename = await download_video_direct(url, output_path, raw_text2)
                await prog.delete()
                if thumb != "no":
                    await bot.send_video(m.chat.id, filename, caption=cc, thumb=thumb)
                else:
                    await bot.send_video(m.chat.id, filename, caption=cc)
                os.remove(filename)
                count += 1
                time.sleep(1)
        except Exception as e:
            await m.reply_text(f"⌘ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n{str(e)}\n⌘ 𝐍𝐚𝐦𝐞 » {name}\n⌘ 𝐋𝐢𝐧𝐤 » {url}")
            continue

    await m.reply_text("✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐨𝐧𝐞")

# ========== WEBHOOK AND MAIN ==========
async def main():
    if WEBHOOK:
        app = await web_server()
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

async def start_bot():
    await bot.start()
    print("Bot started ✅")

async def start_web():
    await main()

if __name__ == "__main__":
    print("Bot starting...")
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(start_bot())
        if WEBHOOK:
            loop.create_task(start_web())
        loop.run_forever()
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        loop.stop()
