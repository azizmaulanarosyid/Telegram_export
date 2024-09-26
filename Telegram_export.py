import os
import pandas as pd
from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel
from datetime import datetime, time as dt_time, timedelta
import pytz
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import asyncio

# Masukkan informasi API Anda
api_id = '#####'  # Ganti dengan api_id yang Anda dapatkan
api_hash = '#####'  # Ganti dengan api_hash yang Anda dapatkan
phone = '+628#####'  # Ganti dengan nomor telepon Anda dalam format internasional

# Fungsi untuk mengekspor pesan ke file Excel
def export_messages_to_excel(messages, filename):
    # Tambahkan kolom-kolom yang diinginkan
    columns = ['No.', 'Date Time', 'Subject', 'Detail', 'Category', 'Hostname', 'Problem', 'Action', 'Note']
    df = pd.DataFrame(messages, columns=columns)
    
    # Mengurutkan berdasarkan Date Time dan menambahkan nomor urut
    df.sort_values(by='Date Time', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.index += 1  # Menambahkan nomor urut dimulai dari 1
    df['No.'] = df.index

    # Simpan DataFrame ke file Excel
    df.to_excel(filename, index=False)

# Fungsi untuk memeriksa apakah pesan berada dalam periode waktu yang ditentukan
def is_in_time_period(dt, start_time, end_time):
    return start_time <= dt.time() <= end_time

# Fungsi untuk menghasilkan nama file yang unik
def generate_filename(base_name, extension):
    if not os.path.exists(f"{base_name}.{extension}"):
        return f"{base_name}.{extension}"
    counter = 1
    while True:
        filename = f"{base_name} {counter:04d}.{extension}"
        if not os.path.exists(filename):
            return filename
        counter += 1

# Fungsi untuk memproses batch pesan
async def process_message_batch(client, entity, offset_id, start_time, end_time, date):
    messages = []
    async for message in client.iter_messages(entity, offset_id=offset_id, limit=1000):
        if message.text:
            message_date = message.date.astimezone(pytz.timezone('Asia/Jakarta')).replace(tzinfo=None)
            if date == message_date.date() and is_in_time_period(message_date, start_time, end_time):
                # Parse message
                detail = message.text
                subject = parse_subject(detail)
                category = 'Alert' if 'Alert' in detail else 'Recovery'
                hostname = parse_hostname(detail)
                problem = subject
                action = 'Log Perangkat UP' if category == 'Recovery' else 'Perangkat UP sebelum SLA'
                note = ''
                
                messages.append([None, message_date, subject, detail, category, hostname, problem, action, note])
    return messages

# Fungsi untuk parse subject dari detail pesan
def parse_subject(detail):
    if "Status" in detail:
        return detail.split("Status:")[1].split('\n')[0].strip()
    return ''

# Fungsi untuk parse hostname dari detail pesan
def parse_hostname(detail):
    if "Hostname" in detail:
        return detail.split("Hostname:")[1].split('\n')[0].strip()
    return ''

# Fungsi utama untuk mengekspor pesan dari grup Telegram
async def export_telegram_messages(group_name, date, time_choice):
    if time_choice == 1:
        start_time, end_time, period_label = dt_time(8, 1), dt_time(16, 30), '08.01-16.30'
    elif time_choice == 2:
        start_time, end_time, period_label = dt_time(16, 31), dt_time(23, 59, 59), '16.31-00.00'
    elif time_choice == 3:
        start_time, end_time, period_label = dt_time(0, 1), dt_time(8, 0), '00.01-08.00'
    else:
        messagebox.showerror("Error", "Pilihan tidak valid.")
        return

    client = TelegramClient(phone, api_id, api_hash)
    await client.start()

    try:
        entity = None
        async for dialog in client.iter_dialogs():
            if dialog.name == group_name:
                entity = dialog.entity
                break

        if entity is None:
            messagebox.showerror("Error", f'Group dengan nama "{group_name}" tidak ditemukan.')
            return

        offset_id = 0
        messages = []
        while True:
            batch = await process_message_batch(client, entity, offset_id, start_time, end_time, date)
            if not batch:
                break
            messages.extend(batch)
            offset_id = batch[-1][1].timestamp()  # Update offset_id berdasarkan timestamp pesan terakhir
            if len(batch) < 1000:  # Kurang dari 1000 pesan berarti tidak ada lagi pesan yang tersisa
                break

        base_filename = f"Hasil Log GDN {date} {period_label}"
        filename = generate_filename(base_filename, 'xlsx')
        export_messages_to_excel(messages, filename)

        messagebox.showinfo("Success", f'Selamat ya, Pesan berhasil diekspor ke file: {filename}')
    except Exception as e:
        messagebox.showerror("Error", f'Duh, Error lagi deh. An error occurred: {e}')
    finally:
        await client.disconnect()

# Fungsi untuk menangani klik tombol Ekspor
def on_export_button_click():
    group_name = group_name_entry.get()
    date = date_entry.get_date()
    time_choice = time_choice_var.get()

    if not group_name or not date or not time_choice:
        messagebox.showerror("Error", "Semua field harus diisi.")
        return

    asyncio.run(export_telegram_messages(group_name, date, time_choice))

# GUI setup
root = tk.Tk()
root.title("Telegram Message Exporter")

# Label dan Entry untuk nama grup
tk.Label(root, text="Nama Grup:", anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky='w')
group_name_entry = tk.Entry(root, width=30)
group_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# Label dan DateEntry untuk tanggal
tk.Label(root, text="Tanggal:", anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky='w')
date_entry = DateEntry(root, width=30, background='darkblue', foreground='white', borderwidth=2)
date_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

# Label untuk memilih periode waktu
tk.Label(root, text="Jam Piket:", anchor="w").grid(row=2, column=0, padx=10, pady=10, sticky='w')
time_choice_var = tk.IntVar()
time_choices = [("08.01 s/d 16.30", 1), ("16.31 s/d 00.00", 2), ("00.01 s/d 08.00", 3)]
for i, (text, value) in enumerate(time_choices):
    tk.Radiobutton(root, text=text, variable=time_choice_var, value=value, anchor="w").grid(row=2+i, column=1, padx=10, pady=5, sticky='w')

# Fungsi untuk membuat tombol dengan border lebih tebal dan bayangan
def create_styled_button(master, text, command):
    button = tk.Button(master, text=text, command=command, relief="raised", bd=4)
    button.grid(row=5, column=1, pady=20, sticky='w')
    return button

# Tombol Ekspor dengan gaya yang ditingkatkan
export_button = create_styled_button(root, "Ekspor", on_export_button_click)

root.mainloop()
