import customtkinter as ctk
from tkinter import messagebox

# local import
import PACK as pack


""" GUI LIBRARY VIEW """


def show_library_gui():
    """Fungsi untuk menampilkan GUI library"""
    clear_frame(root_frame)

    # Ambil data buku
    library_data, total_books = pack.get_library_data()

    # Buat frame utama untuk centering
    main_container = ctk.CTkFrame(root_frame, fg_color="transparent")
    main_container.place(relx=0.5, rely=0.5, anchor="center")

    # Label judul
    title_label = ctk.CTkLabel(
        main_container, text="Daftar Buku", font=("Helvetica", 24, "bold")
    )
    title_label.pack(pady=(0, 20))

    # Gunakan ukuran tetap untuk container, bukan relatif terhadap window
    container = ctk.CTkScrollableFrame(
        main_container,
        width=800,  # Ukuran tetap, tidak bergantung pada window
        height=500,  # Ukuran tetap, tidak bergantung pada window
    )
    container.pack(padx=40, pady=20)

    # Definisikan header dan konfigurasi kolom
    headers = {
        "title": {
            "text": "Judul Novel",
            "width": 250,
            "anchor": "w",
            "padx": (20, 10),
        },
        "author": {
            "text": "Penulis",
            "width": 200,
            "anchor": "w",
            "padx": (10, 0)
        },
        "chapter": {
            "text": "Chapter",
            "width": 100,
            "anchor": "center",
            "padx": (10, 10)
        },
        "platform": {
            "text": "Platform",
            "width": 150,
            "anchor": "w",
            "padx": (10, 10)
        },
    }

    # Buat frame untuk header dengan border
    header_frame = ctk.CTkFrame(
        container, 
        fg_color="#00a48e", 
        border_width=2, 
        border_color="#3498db"
    )
    header_frame.grid(
        row=0, 
        column=0, 
        columnspan=len(headers) * 2 - 1, 
        sticky="ew", pady=(0, 5)
    )

    # Tampilkan header dengan separator
    for col, (key, config) in enumerate(headers.items()):
        grid_col = col * 2

        # Frame khusus untuk header label untuk mengatur padding
        header_label_frame = ctk.CTkFrame(header_frame, fg_color="#00a48e")
        header_label_frame.grid(row=0, column=grid_col, sticky="ew", pady=5)

        header_label = ctk.CTkLabel(
            header_label_frame,
            text=config["text"],
            font=("Helvetica", 13, "bold"),
            width=config["width"],
            height=40,
            anchor=config["anchor"],
            fg_color="#00a48e",
        )
        header_label.pack(
            padx=config["padx"], fill="x"
        )  # Gunakan padx dari konfigurasi

        # Tambahkan separator vertikal
        if col < len(headers) - 1:
            separator = ctk.CTkFrame(
                header_frame, width=2, height=40, fg_color="#3498db"
            )
            separator.grid(row=0, column=grid_col + 1, sticky="ns", pady=5)

    # Tampilkan data dengan padding yang sama
    for row, book in enumerate(library_data, start=1):
        row_bg = "#2D3436" if row % 2 == 0 else "#1E272E"
        row_frame = ctk.CTkFrame(
            container, fg_color=row_bg, border_width=1, border_color="#2C3E50"
        )
        row_frame.grid(
            row=row, column=0, columnspan=len(headers) * 2 - 1, sticky="ew", pady=1
        )

        # Mapping data ke kolom
        for col, (key, config) in enumerate(headers.items()):
            grid_col = col * 2

            # Frame untuk data label
            data_label_frame = ctk.CTkFrame(row_frame, fg_color=row_bg)
            data_label_frame.grid(row=0, column=grid_col, sticky="ew")

            # Gunakan CTkTextbox dengan konfigurasi yang disesuaikan
            text_widget = ctk.CTkTextbox(
                data_label_frame,
                font=("Helvetica", 12),
                width=config["width"],
                height=35,
                activate_scrollbars=False,
                fg_color=row_bg,
                wrap="none"
            )
            text_widget.pack(padx=config["padx"], fill="x", expand=True)
            
            # Sesuaikan alignment teks
            content = str(book[key])
            if config["anchor"] == "center":
                # Hitung padding untuk centering
                available_width = config["width"] // 7
                padding = " " * ((available_width - len(content)) // 1)
                text_widget.insert("1.0", f"{padding}{content}")
            else:
                text_widget.insert("1.0", content)
            
            # Konfigurasi tambahan untuk text widget
            text_widget.configure(state="disabled")  # Ubah state menjadi "disabled" agar tidak bisa diedit

            # Tambahkan separator vertikal
            if col < len(headers) - 1:
                separator = ctk.CTkFrame(
                    row_frame, width=2, height=35, fg_color="#2C3E50"
                )
                separator.grid(row=0, column=grid_col + 1, sticky="ns", pady=5)

    # Atur agar kolom responsif
    for i in range(len(headers) * 2 - 1):
        if i % 2 == 0:  # Kolom data
            container.grid_columnconfigure(i, weight=1)
        else:  # Kolom separator
            container.grid_columnconfigure(i, weight=0)

    # Info jumlah buku
    info_text = f"Total Buku: {total_books}"
    ctk.CTkLabel(container, text=info_text, font=("Helvetica", 12, "italic")).grid(
        row=len(library_data) + 2, column=0, columnspan=4, pady=10
    )

    # Tombol kembali di bagian bawah
    ctk.CTkButton(
        main_container, text="Kembali ke Menu Utama", command=show_main_menu, width=200
    ).pack(pady=(20, 0))


""" CLEAR FRAME """


def clear_frame(frame):
    """Hapus semua widget di frame tertentu."""
    for widget in frame.winfo_children():
        widget.destroy()


""" MAIN WINDOWS """
# Atur tema dan mode warna
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Pengelola Penanda Buku")

# Atur ukuran minimum window
root.minsize(600, 400)

# Konfigurasi grid weight untuk responsivitas
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Ubah root_frame ke grid
root_frame = ctk.CTkFrame(root, corner_radius=10)
root_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
root_frame.grid_columnconfigure(0, weight=1)
root_frame.grid_rowconfigure(0, weight=1)

""" GUI MAIN MENU """


def show_main_menu():
    """Menampilkan menu utama."""
    clear_frame(root_frame)

    # Buat frame untuk menu
    menu_frame = ctk.CTkFrame(root_frame)
    menu_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    menu_frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(menu_frame, text="Menu Utama", font=("Helvetica", 24)).grid(
        row=0, pady=20
    )

    ctk.CTkButton(
        menu_frame,
        text="Buat Penanda Buku Baru",
        command=lambda: create_book_gui(root_frame, root),
        height=40,
    ).grid(row=1, pady=10, sticky="ew", padx=40)

    ctk.CTkButton(
        menu_frame,
        text="Perbarui Penanda Buku",
        command=lambda: update_book_gui(root_frame, root),
        height=40,
    ).grid(row=2, pady=10, sticky="ew", padx=40)

    ctk.CTkButton(
        menu_frame, text="Lihat Library", command=show_library_gui, height=40
    ).grid(row=3, pady=10, sticky="ew", padx=40)

    ctk.CTkButton(menu_frame, text="Keluar", command=root.quit, height=40).grid(
        row=4, pady=10, sticky="ew", padx=40
    )


""" GUI CREATE BOOKMARK """


def create_book_gui(frame, root):
    def save_book():
        # Fungsi save_book tetap sama
        title = title_entry.get()
        author = author_entry.get()
        year_published = year_entry.get()
        genre = genre_entry.get()
        last_chapter_read = chapter_entry.get()
        reading_platform = platform_entry.get()
        description = description_text.get("1.0", "end-1c").strip()
        type_choice = type_entry.get()
        cover_input = cover_entry.get()

        try:
            filename = pack.create_book_md(
                title,
                author,
                year_published,
                genre,
                last_chapter_read,
                reading_platform,
                description,
                type_choice,
                cover_input,
            )
            messagebox.showinfo("Success", f"File '{filename}' telah dibuat!")
            show_main_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    clear_frame(frame)

    # Buat scrollable frame
    container = ctk.CTkScrollableFrame(frame)
    container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    # Konfigurasi grid untuk container
    container.grid_columnconfigure(0, weight=1)

    # Judul
    ctk.CTkLabel(container, text="Buat Penanda Buku Baru", font=("Helvetica", 20)).grid(
        row=0, column=0, pady=10
    )

    # Input fields
    fields = [
        ("Judul Buku:", "title_entry"),
        ("Nama Penulis:", "author_entry"),
        ("Tahun Penerbitan:", "year_entry"),
        ("Genre (pisahkan dengan koma):", "genre_entry"),
        ("Chapter Terakhir yang Dibaca:", "chapter_entry"),
        ("Platform Baca:", "platform_entry"),
        ("Type (manhwa/manhua):", "type_entry"),
        ("URL Gambar Cover:", "cover_entry"),
    ]

    for idx, (label_text, var_name) in enumerate(fields, start=1):
        field_frame = ctk.CTkFrame(container)
        field_frame.grid(row=idx, column=0, sticky="ew", pady=5)
        field_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(field_frame, text=label_text, width=200).grid(
            row=0, column=0, padx=5
        )
        entry = ctk.CTkEntry(field_frame)
        entry.grid(row=0, column=1, sticky="ew", padx=5)
        globals()[var_name] = entry

    # Deskripsi text area
    desc_frame = ctk.CTkFrame(container)
    desc_frame.grid(row=len(fields) + 1, column=0, sticky="ew", pady=5)
    desc_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(desc_frame, text="Deskripsi (opsional):", width=200).grid(
        row=0, column=0, padx=5
    )
    description_text = ctk.CTkTextbox(desc_frame, height=100)
    description_text.grid(row=0, column=1, sticky="ew", padx=5)

    # Buttons
    button_frame = ctk.CTkFrame(container)
    button_frame.grid(row=len(fields) + 2, column=0, sticky="ew", pady=20)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkButton(button_frame, text="Simpan Penanda Buku", command=save_book).grid(
        row=0, column=0, padx=5, sticky="ew"
    )
    ctk.CTkButton(button_frame, text="Kembali", command=show_main_menu).grid(
        row=0, column=1, padx=5, sticky="ew"
    )


""" GUI UPDATE BOOKMARK """


def update_book_gui(frame, root):
    def search_file():
        result = pack.search_book_md(filename_entry.get())

        if result["success"]:
            current_content_text.delete("1.0", "end")
            current_content_text.insert("1.0", result["content"])
            messagebox.showinfo("Success", f"File yang ditemukan: {result['filename']}")
        else:
            messagebox.showerror("Error", result["message"])

    def save_changes():
        result = pack.update_book_md(
            filename_entry.get(),
            title_entry.get(),
            author_entry.get(),
            year_entry.get(),
            genre_entry.get(),
            chapter_entry.get(),
            platform_entry.get(),
        )
        messagebox.showinfo("Info", result)
        show_main_menu()

    clear_frame(frame)

    # Buat scrollable frame
    container = ctk.CTkScrollableFrame(frame)
    container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    # Konfigurasi grid untuk container
    container.grid_columnconfigure(0, weight=1)

    # Judul
    ctk.CTkLabel(container, text="Perbarui Penanda Buku", font=("Helvetica", 20)).grid(
        row=0, column=0, pady=10
    )

    # File search section
    search_frame = ctk.CTkFrame(container)
    search_frame.grid(row=1, column=0, sticky="ew", pady=10)
    search_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(search_frame, text="Nama File:", width=150).grid(
        row=0, column=0, padx=5
    )
    filename_entry = ctk.CTkEntry(search_frame)
    filename_entry.grid(row=0, column=1, sticky="ew", padx=5)
    ctk.CTkButton(search_frame, text="Cari File", command=search_file).grid(
        row=0, column=2, padx=5
    )

    # Current content
    content_frame = ctk.CTkFrame(container)
    content_frame.grid(row=2, column=0, sticky="ew", pady=10)
    content_frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(content_frame, text="Isi Saat Ini:").grid(
        row=0, column=0, sticky="w", padx=5
    )
    current_content_text = ctk.CTkTextbox(content_frame, height=150)
    current_content_text.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    # Update fields
    fields = [
        ("Judul Baru (opsional):", "title_entry"),
        ("Nama Penulis Baru (opsional):", "author_entry"),
        ("Tahun Penerbitan Baru (opsional):", "year_entry"),
        ("Genre Baru (opsional):", "genre_entry"),
        ("Chapter Terakhir yang Dibaca (opsional):", "chapter_entry"),
        ("Platform Baca Baru (opsional):", "platform_entry"),
    ]

    for idx, (label_text, var_name) in enumerate(fields, start=3):
        field_frame = ctk.CTkFrame(container)
        field_frame.grid(row=idx, column=0, sticky="ew", pady=5)
        field_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(field_frame, text=label_text, width=200).grid(
            row=0, column=0, padx=5
        )
        entry = ctk.CTkEntry(field_frame)
        entry.grid(row=0, column=1, sticky="ew", padx=5)
        globals()[var_name] = entry

    # Buttons
    button_frame = ctk.CTkFrame(container)
    button_frame.grid(row=len(fields) + 3, column=0, sticky="ew", pady=20)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkButton(button_frame, text="Simpan Perubahan", command=save_changes).grid(
        row=0, column=0, padx=5, sticky="ew"
    )
    ctk.CTkButton(button_frame, text="Kembali", command=show_main_menu).grid(
        row=0, column=1, padx=5, sticky="ew"
    )
