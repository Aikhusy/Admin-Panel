from Conn import connect_db
from tkinter import messagebox
from Encrypt import encrypt_password
from Validation import validate_ip
from datetime import datetime
from JsonConfig import get_json_config

passfrase = get_json_config('config.json')
passfrase = passfrase['Encrypt_Phrase']
# Fungsi untuk menyimpan data tbl_r_firewall_login
def save_firewall_login(fk_m_firewall, fw_ip_address, fw_username, fw_password, fw_expert_password):
    if not validate_ip(fw_ip_address):
        messagebox.showerror("Invalid IP", "Format IP Address tidak valid!")
        return

    # Mengenkripsi password sebelum disimpan
    fw_password_encrypted = encrypt_password(fw_password,passfrase)
    fw_expert_password_encrypted = encrypt_password(fw_expert_password,passfrase)

    if fk_m_firewall and fw_ip_address and fw_username and fw_password and fw_expert_password:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tbl_r_firewall_login (fk_m_firewall, fw_ip_address, fw_username, fw_password, fw_expert_password) VALUES (?, ?, ?, ?, ?)", 
                           (fk_m_firewall, fw_ip_address, fw_username, fw_password_encrypted, fw_expert_password_encrypted))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Firewall login berhasil disimpan!")
    else:
        messagebox.showwarning("Input Error", "Semua kolom harus diisi.")

# Fungsi untuk mengambil data firewall ID dan mengisi dropdown (combobox)
def load_firewall_ids():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, fw_name FROM tbl_m_firewall WHERE deleted_at IS NULL")
        firewalls = cursor.fetchall()
        conn.close()
        return firewalls
    return []

# Fungsi untuk menyimpan data ke tbl_m_firewall
def save_firewall(fw_name, fw_location, fw_site, fk_fw_pair):
    if fw_name and fw_location and fw_site and fk_fw_pair:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tbl_m_firewall (fw_name, fw_location, fw_site, fk_fw_pair) VALUES (?, ?, ?, ?)", 
                           (fw_name, fw_location, fw_site, fk_fw_pair))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Firewall berhasil ditambahkan!")
    else:
        messagebox.showwarning("Input Error", "Semua kolom harus diisi.")

# Fungsi untuk mengambil dan menampilkan data dari tabel tbl_m_firewall
def load_firewall_data():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, fw_name, fw_location, fw_site, fk_fw_pair FROM tbl_m_firewall WHERE deleted_at IS NULL")
        rows = cursor.fetchall()
        conn.close()
        return [(str(row[0]), row[1], row[2], row[3]) for row in rows]
    return []

def delete_firewall(fw_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            current_time = datetime.now()
            cursor.execute("UPDATE tbl_m_firewall SET deleted_at = ? WHERE id = ?", (current_time, fw_id))
            
            conn.commit()

            cursor.execute("update tbl_r_firewall_login SET deleted_at = ? WHERE fk_m_firewall = ?",(current_time, fw_id))
            cursor.execute("update tbl_t_firewall_capacity_optimisation SET deleted_at = ? WHERE fk_m_firewall = ?",(current_time, fw_id))
            cursor.execute("update tbl_t_firewall_clusterxl SET deleted_at = ? WHERE fk_m_firewall = ?",(current_time, fw_id))
            cursor.execute("update tbl_t_firewall_cpu SET deleted_at = ? WHERE fk_m_firewall = ?",(current_time, fw_id))
            cursor.execute("update tbl_t_firewall_current_status SET deleted_at = ? WHERE fk_m_firewall = ?",(current_time, fw_id))
            cursor.execute("update tbl_t_firewall_diskspace SET deleted_at = ? WHERE fk_m_firewall = ?",(current_time, fw_id))
            cursor.execute("update tbl_t_firewall_failed_memory SET deleted_at = ? WHERE fk_m_firewall = ?",(current_time, fw_id))
            cursor.execute("update tbl_t_firewall_hotfix SET deleted_at = ? WHERE fk_m_firewall = ?",(current_time, fw_id))
            cursor.execute("update tbl_t_firewall_license SET deleted_at = ? WHERE fk_m_firewall = ?",(current_time, fw_id))
            cursor.execute("update tbl_t_firewall_memory SET deleted_at = ? WHERE fk_m_firewall = ?",(current_time, fw_id))
            cursor.execute("update tbl_t_firewall_raid SET deleted_at = ? WHERE fk_m_firewall = ?",(current_time, fw_id))
            cursor.execute("update tbl_t_firewall_rxtx SET deleted_at = ? WHERE fk_m_firewall = ?",(current_time, fw_id))
            cursor.execute("update tbl_t_firewall_uptime SET deleted_at = ? WHERE fk_m_firewall = ?",(current_time, fw_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Firewall berhasil dihapus!")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error saat menghapus firewall: {e}")
    else:
        messagebox.showerror("Database Error", "Koneksi ke database gagal.")

def load_firewall_login_data():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tbl_r_firewall_login.id,tbl_m_firewall.fw_name, tbl_r_firewall_login.fw_ip_address, 
                   tbl_r_firewall_login.fw_username 
            FROM tbl_r_firewall_login 
            JOIN tbl_m_firewall ON tbl_r_firewall_login.fk_m_firewall = tbl_m_firewall.id 
            WHERE tbl_r_firewall_login.deleted_at IS NULL
        """)
        rows = cursor.fetchall()
        conn.close()
        return [(str(row[0]), row[1], row[2],row[3]) for row in rows]
    return []

def delete_firewall_login(fw_id):

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            current_time = datetime.now()
            cursor.execute("UPDATE tbl_r_firewall_login SET deleted_at = ? WHERE id = ?", (current_time, fw_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Firewall berhasil dihapus!")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error saat menghapus firewall: {e}")
    else:
        messagebox.showerror("Database Error", "Koneksi ke database gagal.")