import os
from pathlib import Path


def get_library_data() -> tuple[list[dict], int]:
    """
    Fungsi untuk mengambil dan mengelompokkan data buku dari file MD.

    Returns:
        tuple: (list data buku, jumlah total buku)
    """
    directory = Path(__file__).parent.parent / "library_komik_md"
    library_data = []

    try:
        # Debug print
        print(f"Mencari file di direktori: {directory}")
        
        if not directory.exists():
            print(f"Direktori tidak ditemukan: {directory}")
            return [], 0

        # Dapatkan daftar file MD dengan prefix yang benar
        md_files = [f for f in directory.iterdir() if f.name.startswith("DP_KMK_") and f.suffix == '.md']
        print(f"File yang ditemukan: {[f.name for f in md_files]}")  # Debug print

        for file_path in md_files:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.readlines()
                
                book_data = {
                    "title": "N/A",
                    "author": "N/A",
                    "chapter": "N/A",
                    "platform": "N/A"
                }

                for line in content:
                    line = line.lower().strip()
                    if "original name:" in line:
                        book_data["title"] = line.split("original name:")[1].strip()
                    elif "penulis:" in line:
                        book_data["author"] = line.split("penulis:")[1].strip()
                    elif "chapter on read:" in line:
                        book_data["chapter"] = line.split("chapter on read:")[1].strip()
                    elif "updated-by:" in line:
                        book_data["platform"] = line.split("updated-by:")[1].strip()

                print(f"Data buku yang dibaca: {book_data}")  # Debug print
                library_data.append(book_data)

            except Exception as e:
                print(f"Error membaca file {file_path.name}: {str(e)}")
                continue

        print(f"Total data yang dikumpulkan: {len(library_data)}")  # Debug print
        return library_data, len(md_files)

    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")
        return [], 0

def extract_metadata(content: str, key: str) -> str:
    """Ekstrak metadata dari konten file."""
    try:
        for line in content.split('\n'):
            if f"{key}:" in line:
                return line.split(f"{key}:")[1].strip()
    except:
        pass
    return "N/A"
