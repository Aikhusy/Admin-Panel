import tkinter as tk
from tkinter import messagebox, ttk
from firewall import save_firewall_login, load_firewall_ids, save_firewall, load_firewall_data, delete_firewall

def refresh_firewall_dropdown():
    firewalls = load_firewall_ids()
    fk_m_firewall_combobox['values'] = [f"{str(fw[0]).strip('(),')} - {fw[1]}" for fw in firewalls]

# Fungsi untuk load data firewall ke dalam Treeview
def refresh_firewall_table():
    rows = load_firewall_data()

    # Hapus data lama dari Treeview
    for item in firewall_treeview.get_children():
        firewall_treeview.delete(item)

    # Masukkan data baru ke dalam Treeview
    for row in rows:
        firewall_treeview.insert("", tk.END, values=row)

# Fungsi untuk menyimpan data login firewall
def save_firewall_login_action():
    fk_m_firewall = fk_m_firewall_combobox.get().split(' ')[0]  # Ambil hanya ID firewall
    fw_ip_address = fw_ip_address_entry.get()
    fw_username = fw_username_entry.get()
    fw_password = fw_password_entry.get()
    fw_expert_password = fw_expert_password_entry.get()

    save_firewall_login(fk_m_firewall, fw_ip_address, fw_username, fw_password, fw_expert_password)
    refresh_firewall_dropdown()  # Refresh dropdown setelah menyimpan

# Fungsi untuk menyimpan data firewall
def save_firewall_action():
    fw_name = fw_name_entry.get()
    fw_location = fw_location_entry.get()
    fw_site = fw_site_entry.get()
    fk_fw_pair = fk_fw_pair_entry.get()

    save_firewall(fw_name, fw_location, fw_site, fk_fw_pair)
    refresh_firewall_table()  # Refresh tabel setelah menyimpan
    refresh_firewall_dropdown()  # Refresh dropdown setelah menyimpan

# Fungsi untuk menghapus firewall
def delete_firewall_action():
    selected_item = firewall_treeview.selection()  # Mendapatkan item yang dipilih
    if selected_item:
        item_values = firewall_treeview.item(selected_item, 'values')
        fw_id = item_values[0]  # Mengambil ID dari item yang dipilih

        confirm = messagebox.askyesno("Confirm Delete", "Apakah Anda yakin ingin menghapus firewall ini?")
        if confirm:
            delete_firewall(fw_id)
            refresh_firewall_table()  # Refresh data setelah penghapusan
    else:
        messagebox.showwarning("No Selection", "Pilih firewall yang ingin dihapus.")

# Fungsi untuk clear data pada panel login firewall
def clear_fw_login_panel():
    fk_m_firewall_combobox.set("")
    fw_ip_address_entry.delete(0, tk.END)
    fw_username_entry.delete(0, tk.END)
    fw_password_entry.delete(0, tk.END)
    fw_expert_password_entry.delete(0, tk.END)

# Fungsi untuk clear data pada panel tambah firewall
def clear_fw_panel():
    fw_name_entry.delete(0, tk.END)
    fw_location_entry.delete(0, tk.END)
    fw_site_entry.delete(0, tk.END)
    fk_fw_pair_entry.delete(0, tk.END)

# Membuat GUI utama
root = tk.Tk()
root.title("Firewall Management")
root.geometry("800x700")

# Frame utama untuk canvas dan scrollbar
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Canvas widget
canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill="both", expand=True)

# Scrollbar widget
scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")

# Frame yang akan di-scroll
content_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Fungsi untuk update scrollbar
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

content_frame.bind("<Configure>", on_frame_configure)

# Panel untuk tbl_r_firewall_login
fw_login_panel = tk.LabelFrame(content_frame, text="Firewall Login Management", padx=10, pady=10)
fw_login_panel.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Dropdown untuk memilih Firewall ID
tk.Label(fw_login_panel, text="Firewall").grid(row=0, column=0)

# Ambil firewall IDs dari tabel tbl_m_firewall
firewalls = load_firewall_ids()

# Buat Combobox dengan pilihan firewall IDs
fk_m_firewall_combobox = ttk.Combobox(fw_login_panel, state="readonly")
fk_m_firewall_combobox['values'] = [f"{fw[0]} - {fw[1]}" for fw in firewalls]
fk_m_firewall_combobox.grid(row=0, column=1)

tk.Label(fw_login_panel, text="IP Address").grid(row=1, column=0)
fw_ip_address_entry = tk.Entry(fw_login_panel)
fw_ip_address_entry.grid(row=1, column=1)

tk.Label(fw_login_panel, text="Username").grid(row=2, column=0)
fw_username_entry = tk.Entry(fw_login_panel)
fw_username_entry.grid(row=2, column=1)

tk.Label(fw_login_panel, text="Password").grid(row=3, column=0)
fw_password_entry = tk.Entry(fw_login_panel, show='*')
fw_password_entry.grid(row=3, column=1)

tk.Label(fw_login_panel, text="Expert Password").grid(row=4, column=0)
fw_expert_password_entry = tk.Entry(fw_login_panel, show='*')
fw_expert_password_entry.grid(row=4, column=1)

# Tombol Save dan Clear pada satu baris
button_frame = tk.Frame(fw_login_panel)
button_frame.grid(row=5, column=0, columnspan=2, pady=10)

tk.Button(button_frame, text="Save Firewall Login", command=save_firewall_login_action).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Clear", command=clear_fw_login_panel).pack(side=tk.LEFT, padx=5)

# Panel untuk tbl_m_firewall (Tambah Firewall)
fw_panel = tk.LabelFrame(content_frame, text="Add New Firewall", padx=10, pady=10)
fw_panel.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

tk.Label(fw_panel, text="Firewall Name").grid(row=0, column=0)
fw_name_entry = tk.Entry(fw_panel)
fw_name_entry.grid(row=0, column=1)

tk.Label(fw_panel, text="Firewall Location").grid(row=1, column=0)
fw_location_entry = tk.Entry(fw_panel)
fw_location_entry.grid(row=1, column=1)

tk.Label(fw_panel, text="Firewall Site").grid(row=2, column=0)
fw_site_entry = tk.Entry(fw_panel)
fw_site_entry.grid(row=2, column=1)

tk.Label(fw_panel, text="Firewall Pair ID").grid(row=3, column=0)
fk_fw_pair_entry = tk.Entry(fw_panel)
fk_fw_pair_entry.grid(row=3, column=1)

# Tombol Save dan Clear pada satu baris
button_frame_fw = tk.Frame(fw_panel)
button_frame_fw.grid(row=4, column=0, columnspan=2, pady=10)

tk.Button(button_frame_fw, text="Save Firewall", command=save_firewall_action).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame_fw, text="Clear", command=clear_fw_panel).pack(side=tk.LEFT, padx=5)

# Panel untuk menampilkan data Firewall (tbl_m_firewall)
firewall_data_panel = tk.LabelFrame(content_frame, text="Firewall Data", padx=10, pady=10)
firewall_data_panel.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

columns = ("id", "Name", "Location", "Site", "Pair ID")
firewall_treeview = ttk.Treeview(firewall_data_panel, columns=columns, show="headings")
for col in columns:
    firewall_treeview.heading(col, text=col)
firewall_treeview.pack(fill="both", expand="yes")

# Tombol Hapus
tk.Button(firewall_data_panel, text="Delete Firewall", command=delete_firewall_action).pack(pady=10)

# Refresh data awal
refresh_firewall_table()

root.mainloop()