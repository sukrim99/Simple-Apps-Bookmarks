import customtkinter as ctk
from tkinter import messagebox
from typing import Dict, Any, Callable
from dataclasses import dataclass

# local import
import PACK as pack

# Konstanta untuk UI
UI_CONSTANTS = {
    "FONTS": {
        "HEADER": ("Helvetica", 24, "bold"),
        "SUBHEADER": ("Helvetica", 20),
        "NORMAL": ("Helvetica", 12),
        "BOLD": ("Helvetica", 13, "bold"),
        "ITALIC": ("Helvetica", 12, "italic"),
    },
    "COLORS": {
        "HEADER_BG": "#00a48e",
        "ROW_BG_1": "#1E272E",
        "ROW_BG_2": "#2D3436",
        "BORDER": "#3498db",
        "SEPARATOR": "#2C3E50",
        "LINK": "#3498db",
    },
    "SIZES": {
        "WINDOW_MIN": (600, 400),
        "LIBRARY_WIDTH": 800,
        "LIBRARY_HEIGHT": 500,
        "BUTTON_HEIGHT": 40,
    }
}

@dataclass
class ColumnConfig:
    """Konfigurasi untuk kolom tabel."""
    text: str
    width: int
    anchor: str
    padx: tuple[int, int]


""" GUI LIBRARY VIEW """


def create_header_label(parent: ctk.CTkFrame, config: Dict[str, Any]) -> ctk.CTkLabel:
    """Membuat label header untuk tabel."""
    header_label_frame = ctk.CTkFrame(parent, fg_color=UI_CONSTANTS["COLORS"]["HEADER_BG"])
    header_label_frame.grid(row=0, column=config["grid_col"], sticky="ew", pady=5)
    
    return ctk.CTkLabel(
        header_label_frame,
        text=config["text"],
        font=UI_CONSTANTS["FONTS"]["BOLD"],
        width=config["width"],
        height=UI_CONSTANTS["SIZES"]["BUTTON_HEIGHT"],
        anchor=config["anchor"],
        fg_color=UI_CONSTANTS["COLORS"]["HEADER_BG"],
    )

def create_data_cell(parent: ctk.CTkFrame, config: Dict[str, Any], content: str, 
                    row_bg: str, handle_click: Callable = None) -> ctk.CTkTextbox:
    """Membuat sel data untuk tabel."""
    text_widget = ctk.CTkTextbox(
        parent,
        font=UI_CONSTANTS["FONTS"]["NORMAL"],
        width=config["width"],
        height=35,
        activate_scrollbars=False,
        fg_color=row_bg,
        wrap="none"
    )
    
    if handle_click:
        text_widget.tag_config("link", 
                             foreground=UI_CONSTANTS["COLORS"]["LINK"], 
                             underline=True)
        text_widget.insert("1.0", content, "link")
        text_widget.tag_bind("link", "<Button-1>", 
                           lambda e: handle_click(content))
        text_widget.configure(cursor="hand2")
    else:
        if config["anchor"] == "center":
            content = content.center(len(content) + 4)
        text_widget.insert("1.0", content)
    
    text_widget.configure(state="disabled")
    return text_widget

def show_library_gui():
    """Menampilkan GUI library dengan data buku."""
    clear_frame(root_frame)
    
    library_data, total_books = pack.get_library_data()
    print(f"Data yang diterima: {library_data}")
    
    # Container utama dengan centering
    main_container = ctk.CTkFrame(root_frame, fg_color="transparent")
    main_container.place(relx=0.5, rely=0.5, anchor="center")
    
    # Header
    ctk.CTkLabel(
        main_container, 
        text="Daftar Buku", 
        font=UI_CONSTANTS["FONTS"]["HEADER"]
    ).pack(pady=(0, 20))
    
    # Tabel container dengan ukuran tetap dan scrollbar minimal
    table_container = ctk.CTkScrollableFrame(
        main_container,
        width=UI_CONSTANTS["SIZES"]["LIBRARY_WIDTH"],
        height=UI_CONSTANTS["SIZES"]["LIBRARY_HEIGHT"],
        fg_color="transparent",
        scrollbar_button_color="#2B2B2B",        # Warna gelap yang hampir tidak terlihat
        scrollbar_button_hover_color="#3B3B3B",  # Sedikit lebih terang saat hover
        scrollbar_fg_color="#2B2B2B"             # Sama dengan button color
    )
    table_container.pack(padx=10, pady=10)
    
    # Bind mouse wheel untuk scroll yang lebih smooth
    def _on_mousewheel(event):
        table_container._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    table_container.bind_all("<MouseWheel>", _on_mousewheel)
    
    # Konfigurasi kolom
    column_widths = [250, 200, 100, 150]  # Lebar untuk setiap kolom
    headers = ["Judul Novel", "Penulis", "Chapter", "Platform"]
    
    # Header row dengan frame
    header_frame = ctk.CTkFrame(
        table_container,
        fg_color=UI_CONSTANTS["COLORS"]["HEADER_BG"],
        border_width=1,
        border_color=UI_CONSTANTS["COLORS"]["BORDER"]
    )
    header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5), padx=5)
    header_frame.grid_columnconfigure((0,1,2,3), weight=1)
    
    # Header labels
    for col, (header, width) in enumerate(zip(headers, column_widths)):
        header_cell = ctk.CTkFrame(
            header_frame,
            fg_color=UI_CONSTANTS["COLORS"]["HEADER_BG"]
        )
        header_cell.grid(row=0, column=col, sticky="ew", padx=1)
        header_cell.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            header_cell,
            text=header,
            font=UI_CONSTANTS["FONTS"]["BOLD"],
            width=width,
            height=35,
            fg_color=UI_CONSTANTS["COLORS"]["HEADER_BG"]
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    # Data rows
    for row, book in enumerate(library_data, start=1):
        row_frame = ctk.CTkFrame(
            table_container,
            fg_color=UI_CONSTANTS["COLORS"]["ROW_BG_2" if row % 2 == 0 else "ROW_BG_1"],
            border_width=1,
            border_color=UI_CONSTANTS["COLORS"]["SEPARATOR"]
        )
        row_frame.grid(row=row, column=0, sticky="ew", pady=1, padx=5)
        row_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        # Kolom data
        data = [book["title"], book["author"], book["chapter"], book["platform"]]
        
        for col, (content, width) in enumerate(zip(data, column_widths)):
            cell_frame = ctk.CTkFrame(
                row_frame,
                fg_color=row_frame.cget("fg_color")
            )
            cell_frame.grid(row=0, column=col, sticky="ew", padx=1)
            cell_frame.grid_columnconfigure(0, weight=1)
            
            if col == 0:  # Kolom judul dengan link
                label = ctk.CTkLabel(
                    cell_frame,
                    text=content,
                    font=UI_CONSTANTS["FONTS"]["NORMAL"],
                    width=width,
                    height=35,
                    cursor="hand2",
                    text_color=UI_CONSTANTS["COLORS"]["LINK"],
                    fg_color=cell_frame.cget("fg_color")
                )
                label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
                label.bind("<Button-1>", lambda e, title=content: handle_title_click(title, root))
            else:
                ctk.CTkLabel(
                    cell_frame,
                    text=content,
                    font=UI_CONSTANTS["FONTS"]["NORMAL"],
                    width=width,
                    height=35,
                    fg_color=cell_frame.cget("fg_color")
                ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    # Info total buku
    ctk.CTkLabel(
        main_container, 
        text=f"Total Buku: {total_books}",
        font=UI_CONSTANTS["FONTS"]["ITALIC"]
    ).pack(pady=10)
    
    # Tombol kembali
    ctk.CTkButton(
        main_container,
        text="Kembali ke Menu Utama",
        command=show_main_menu,
        width=200
    ).pack(pady=10)

    # Unbind mousewheel when window is destroyed
    def _on_destroy(event):
        table_container.unbind_all("<MouseWheel>")
    root_frame.bind("<Destroy>", _on_destroy)


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

    # Tambahkan referensi ke root untuk akses global
    root.current_filename_entry = filename_entry
    root.current_content_textbox = current_content_text

def setup_library_table(container: ctk.CTkScrollableFrame, library_data: list):
    """Setup tabel untuk menampilkan data library."""
    if not library_data:
        # Tampilkan pesan jika tidak ada data
        ctk.CTkLabel(
            container,
            text="Tidak ada data buku yang tersedia",
            font=UI_CONSTANTS["FONTS"]["ITALIC"]
        ).grid(row=0, column=0, pady=20)
        return

    headers = {
        "title": ColumnConfig("Judul Novel", 250, "w", (20, 10)),
        "author": ColumnConfig("Penulis", 200, "w", (10, 0)),
        "chapter": ColumnConfig("Chapter", 100, "center", (10, 10)),
        "platform": ColumnConfig("Platform", 150, "w", (10, 10))
    }
    
    # Buat header
    header_frame = create_table_header(container, headers)
    
    # Buat baris data
    for row, book in enumerate(library_data, start=1):
        create_table_row(container, headers, book, row)
        
    # Setup kolom responsif
    setup_responsive_columns(container, len(headers))

def create_table_header(container: ctk.CTkScrollableFrame, 
                       headers: Dict[str, ColumnConfig]) -> ctk.CTkFrame:
    """Membuat header tabel."""
    header_frame = ctk.CTkFrame(
        container,
        fg_color=UI_CONSTANTS["COLORS"]["HEADER_BG"],
        border_width=2,
        border_color=UI_CONSTANTS["COLORS"]["BORDER"]
    )
    header_frame.grid(
        row=0,
        column=0,
        columnspan=len(headers) * 2 - 1,
        sticky="ew",
        pady=(0, 5)
    )
    
    for col, (_, config) in enumerate(headers.items()):
        grid_col = col * 2
        
        header_label = create_header_label(header_frame, {
            "grid_col": grid_col,
            "text": config.text,
            "width": config.width,
            "anchor": config.anchor
        })
        header_label.pack(padx=config.padx, fill="x")
        
        if col < len(headers) - 1:
            create_separator(header_frame, grid_col + 1)
            
    return header_frame

def create_table_row(container: ctk.CTkScrollableFrame, 
                    headers: Dict[str, ColumnConfig],
                    book: Dict[str, str], row: int):
    """Membuat baris data untuk tabel."""
    row_bg = UI_CONSTANTS["COLORS"]["ROW_BG_2" if row % 2 == 0 else "ROW_BG_1"]
    
    row_frame = ctk.CTkFrame(
        container,
        fg_color=row_bg,
        border_width=1,
        border_color=UI_CONSTANTS["COLORS"]["SEPARATOR"]
    )
    row_frame.grid(
        row=row,
        column=0,
        columnspan=len(headers) * 2 - 1,
        sticky="ew",
        pady=1
    )
    
    for col, (key, config) in enumerate(headers.items()):
        grid_col = col * 2
        content = str(book[key])
        
        if key == "title":
            create_data_cell(
                row_frame, 
                {"grid_col": grid_col, "width": config.width, "anchor": config.anchor},
                content,
                row_bg,
                lambda title: handle_title_click(title, root)
            )
        else:
            create_data_cell(
                row_frame,
                {"grid_col": grid_col, "width": config.width, "anchor": config.anchor},
                content,
                row_bg
            )
        
        if col < len(headers) - 1:
            create_separator(row_frame, grid_col + 1)

def create_separator(parent: ctk.CTkFrame, grid_col: int):
    """Membuat separator vertikal."""
    separator = ctk.CTkFrame(
        parent,
        width=2,
        height=35,
        fg_color=UI_CONSTANTS["COLORS"]["SEPARATOR"]
    )
    separator.grid(row=0, column=grid_col, sticky="ns", pady=5)

def setup_responsive_columns(container: ctk.CTkScrollableFrame, num_headers: int):
    """Setup kolom responsif."""
    for i in range(num_headers * 2 - 1):
        container.grid_columnconfigure(i, weight=1 if i % 2 == 0 else 0)

def handle_title_click(title: str, root: ctk.CTk):
    """Menangani klik pada judul buku."""
    filename = f"DP_KMK_{title}.md"
    update_book_gui(root_frame, root)
    
    def delayed_fill():
        if hasattr(root, 'current_filename_entry') and \
           hasattr(root, 'current_content_textbox'):
            root.current_filename_entry.delete(0, 'end')
            root.current_filename_entry.insert(0, filename)
            
            result = pack.search_book_md(filename)
            if result["success"]:
                root.current_content_textbox.delete("1.0", "end")
                root.current_content_textbox.insert("1.0", result["content"])
    
    root.after(100, delayed_fill)
