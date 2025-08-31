import os
import platform
import socket
import requests
from telethon import events, Button
from kyt import *  # pastikan file kyt.py ada dan sudah inisialisasi bot

# =========================
# KONFIG
# =========================
ADMIN_ID = 7559356014   # ganti dengan Telegram ID kamu
DOMAIN = "vvip.kemet-js.store"  # ganti domain kamu

# =========================
# FUNGSI WHITELIST
# =========================
def is_allowed(user_id):
    try:
        with open("whitelist.txt", "r") as f:
            ids = f.read().splitlines()
        return str(user_id) in ids
    except FileNotFoundError:
        return False

def add_id(user_id):
    with open("whitelist.txt", "a") as f:
        f.write(f"{user_id}\n")

def del_id(user_id):
    try:
        with open("whitelist.txt", "r") as f:
            ids = f.read().splitlines()
        if str(user_id) in ids:
            ids.remove(str(user_id))
        with open("whitelist.txt", "w") as f:
            if ids:
                f.write("\n".join(ids) + "\n")
    except FileNotFoundError:
        pass

# =========================
# ADMIN COMMANDS
# =========================
@bot.on(events.NewMessage(pattern=r"/addid(?: (\d+))?"))
async def addid_cmd(event):
    sender = await event.get_sender()
    if sender.id != ADMIN_ID:
        return await event.reply("🚫 Kamu bukan admin!")

    # kalau admin reply pesan user
    if event.is_reply and not event.pattern_match.group(1):
        reply_msg = await event.get_reply_message()
        user = await reply_msg.get_sender()
        user_id = user.id
    else:
        # kalau admin pakai /addid <id>
        user_id = event.pattern_match.group(1)

    if not user_id:
        return await event.reply("⚠️ Format salah!\n\nGunakan:\n`/addid <user_id>` atau reply ke pesan user.")

    add_id(user_id)
    await event.reply(f"✅ User ID `{user_id}` berhasil ditambahkan ke whitelist.")

@bot.on(events.NewMessage(pattern=r"/delid (\d+)"))
async def delid_cmd(event):
    sender = await event.get_sender()
    if sender.id != ADMIN_ID:
        return await event.reply("🚫 Kamu bukan admin!")
    user_id = event.pattern_match.group(1)
    del_id(user_id)
    await event.reply(f"🗑️ User ID `{user_id}` berhasil dihapus dari whitelist.")

@bot.on(events.NewMessage(pattern=r"/listid$"))
async def listid_cmd(event):
    sender = await event.get_sender()
    if sender.id != ADMIN_ID:
        return await event.reply("🚫 Kamu bukan admin!")
    try:
        with open("whitelist.txt","r") as f:
            ids = f.read().splitlines()
        if not ids:
            return await event.reply("⚠️ Whitelist masih kosong.")
        daftar = "\n".join([f"• {i}" for i in ids])
        await event.reply(f"📋 **Daftar User Whitelist:**\n\n{daftar}")
    except FileNotFoundError:
        await event.reply("⚠️ Whitelist file belum ada.")

# =========================
# USER REQUEST AKSES
# =========================
@bot.on(events.NewMessage(pattern=r"/reqakses$"))
async def reqakses_cmd(event):
    sender = await event.get_sender()
    user_id = sender.id
    if is_allowed(user_id):
        return await event.reply("✅ Kamu sudah ada di whitelist, silakan ketik /start lagi.")
    
    await event.reply("📩 Permintaan akses sudah dikirim ke admin. Mohon tunggu persetujuan.")
    await bot.send_message(
        ADMIN_ID,
        f"📥 User {sender.first_name} (`{user_id}`) mengajukan permintaan akses.\n\n"
        f"Balas pesannya dengan `/addid` untuk approve."
    )

# =========================
# START MENU
# =========================
@bot.on(events.NewMessage(pattern=r"(?:\.start|/start)$"))
@bot.on(events.CallbackQuery(data=b'start'))
async def start(event):
    sender = await event.get_sender()
    user_id = sender.id
    firstname = sender.first_name or "Tidak ada"
    username = f"@{sender.username}" if sender.username else "Tidak ada"

    if not is_allowed(user_id):
        await event.reply("🚫 Akses ditolak!\n\n⚠️ Hubungi admin untuk mendapatkan izin akses (pakai /reqakses).")
        await bot.send_message(ADMIN_ID, f"⚠️ User {sender.first_name} ({user_id}) mencoba akses tanpa izin.")
        return

    banner = "https://files.catbox.moe/vl2fdm.jpeg"

    # Fungsi hitung baris akun
    def count_lines(filepath):
        try:
            with open(filepath, "r") as f:
                return sum(1 for line in f if "###" in line)
        except FileNotFoundError:
            return 0

    # =========================
    # ADMIN
    # =========================
    if user_id == ADMIN_ID:
        inline = [
            [Button.inline("PANEL CREATE ACCOUNT","menu")],
            [Button.url("💬 PRIVATE MESSAGE", "https://t.me/newbie_store24")],
            [Button.url("🛒 ORDER SCRIPT", "https://whatsapp.nevpn.site")]
        ]

        ssh = count_lines("/etc/ssh/.ssh.db")
        vms = count_lines("/etc/vmess/.vmess.db")
        vls = count_lines("/etc/vless/.vless.db")
        trj = count_lines("/etc/trojan/.trojan.db")

        namaos = platform.platform()
        try:
            with open("/etc/xray/city", "r") as f:
                city = f.read().strip()
        except FileNotFoundError:
            city = "Unknown"

        try:
            ipsaya = requests.get("https://ipv4.icanhazip.com").text.strip()
        except:
            ipsaya = socket.gethostbyname(socket.gethostname())

        msg = f"""
╔════════════════════════╗
       👑 **OWNER PANEL**
╚════════════════════════╝

🆔 **ID**       : `{user_id}`
👤 **Name**     : {firstname}
📛 **Username** : @{username if username else '-'}

💻 **SERVER INFO**
🖥️ OS       : `{namaos.strip()}`
🌍 CITY     : `{city.strip()}`
🌐 DOMAIN   : `{DOMAIN}`
📡 IP VPS   : `{ipsaya.strip()}`

📊 **JUMLAH AKUN**
🔑 SSH      : {ssh}
⚡ VMESS    : {vms}
✨ VLESS    : {vls}
🔒 TROJAN   : {trj}

━━━━━━━━━━━━━━━━━━━━━━━
🚀 Powered by **KJS-STORE™**
━━━━━━━━━━━━━━━━━━━━━━━
"""

        await bot.send_file(event.chat_id, banner)
        await event.respond(msg, buttons=inline, link_preview=False)

    # =========================
    # USER BIASA
    # =========================
    else:
        inline = [
            [Button.inline("PANEL CREATE ACCOUNT","menu")],
            [Button.url("💬 HUBUNGI ADMIN", "https://t.me/newbie_store24"),
             Button.url("🛒 ORDER SCRIPT", "https://whatsapp.nevpn.site")]
        ]

        msg = f"""
╔════════════════════════╗
       👤 **USER PANEL**
╚════════════════════════╝

🔑 ID       : `{user_id}`
👤 Name     : {firstname}
📛 Username : @{username if username else '-'}

📌 **PEMBERITAHUAN**
⚠️ Gunakan panel ini dengan bijak.  
⚠️ Dilarang menyalahgunakan akun.  
⚠️ Hubungi admin jika membutuhkan bantuan.  

━━━━━━━━━━━━━━━━━━━━━━━
🚀 Powered by **KJS-STORE™**
━━━━━━━━━━━━━━━━━━━━━━━
"""
        await bot.send_file(event.chat_id, banner)
        await event.respond(msg, buttons=inline, link_preview=False)