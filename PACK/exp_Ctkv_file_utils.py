import os
from pathlib import Path


def get_library_data():
    """Fungsi untuk mengambil dan mengelompokkan data buku dari file MD"""
    # Tentukan direktori yang benar

    directory = Path(__file__).parent.parent / "komik_md"
    library_data = []

    try:
        # Pastikan direktori ada
        if not os.path.exists(directory):
            print(f"Direktori tidak ditemukan: {directory}")
            return [], 0

        # Dapatkan daftar file MD dengan prefix yang benar
        md_files = [
            f
            for f in os.listdir(directory)
            if f.endswith(".md") and f.startswith("DP_KMK_")
        ]
        print(f"File yang ditemukan: {md_files}")  # Debug info

        for filename in md_files:
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()

                    # Dictionary untuk data buku
                    book_data = {
                        "title": "N/A",
                        "author": "N/A",
                        "chapter": "N/A",
                        "platform": "N/A",
                    }

                    # Cari data yang diperlukan
                    for line in lines:
                        line = line.lower().strip()
                        if "original name:" in line:  # Judul
                            book_data["title"] = line.split("original name:")[1].strip()
                        elif "penulis:" in line:  # Penulis
                            book_data["author"] = line.split("penulis:")[1].strip()
                        elif "chapter on read:" in line:  # Chapter
                            book_data["chapter"] = line.split("chapter on read:")[
                                1
                            ].strip()
                        elif "updated-by:" in line:  # Platform
                            book_data["platform"] = line.split("updated-by:")[1].strip()

                    library_data.append(book_data)
                    print(f"Data buku yang ditemukan: {book_data}")  # Debug info

            except Exception as e:
                print(f"Error membaca file {filename}: {str(e)}")
                continue

        print(f"Total buku yang ditemukan: {len(library_data)}")  # Debug info
        return library_data, len(md_files)

    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")
        return [], 0
