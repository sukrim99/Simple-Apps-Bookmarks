import os
import difflib
from pathlib import Path

""" OPRATION UPDATE BOOKMARK """


def search_book_md(filename):
    """Fungsi untuk mencari dan membaca konten file"""
    # directory = r"E:\Obsidian Belajar\LEARNING_(LITERATUR-NOTE)\TEKNOLOGI\PYTHON\CODE\penanda_buku_md\CTK_version\exp_CTK\komik_md"
    directory = Path(__file__).parent.parent / "komik_md"
    try:
        # Dapatkan daftar file dengan path lengkap
        md_files = [f for f in os.listdir(directory) if f.endswith(".md")]

        # Hilangkan ekstensi .md untuk pencocokan
        filename_clean = filename.lower().replace(".md", "")
        md_files_clean = [f.lower().replace(".md", "") for f in md_files]

        # Cari kecocokan
        close_matches = difflib.get_close_matches(
            filename_clean, md_files_clean, n=1, cutoff=0.3
        )

        if close_matches:
            # Temukan file asli yang cocok
            matched_index = md_files_clean.index(close_matches[0])
            matched_filename = md_files[matched_index]
            # Buat path lengkap
            full_path = os.path.join(directory, matched_filename)

            # Baca konten file
            with open(full_path, "r", encoding="utf-8") as file:
                content = file.read()

            return {"success": True, "filename": matched_filename, "content": content}
        else:
            return {
                "success": False,
                "message": f"File tidak ditemukan. File yang tersedia: {', '.join(md_files)}",
            }

    except Exception as e:
        return {"success": False, "message": f"Terjadi kesalahan: {str(e)}"}


def update_book_md(
    filename, title, author, year_published, genre, last_chapter_read, reading_platform
):
    """Fungsi untuk memperbarui konten file"""
    # directory = r"E:\Obsidian Belajar\LEARNING_(LITERATUR-NOTE)\TEKNOLOGI\PYTHON\CODE\penanda_buku_md\CTK_version\exp_CTK\komik_md"
    directory = Path(__file__).parent.parent / "komik_md"
    try:
        # Pastikan direktori ada
        if not os.path.exists(directory):
            return f"Direktori tidak ditemukan: {directory}"

        # Dapatkan daftar file dengan path lengkap
        md_files = [f for f in os.listdir(directory) if f.endswith(".md")]

        # Hilangkan ekstensi .md untuk pencocokan
        filename_clean = filename.lower().replace(".md", "")
        md_files_clean = [f.lower().replace(".md", "") for f in md_files]

        # Cari kecocokan
        close_matches = difflib.get_close_matches(
            filename_clean, md_files_clean, n=1, cutoff=0.3
        )

        if close_matches:
            matched_index = md_files_clean.index(close_matches[0])
            matched_filename = md_files[matched_index]
            full_path = os.path.join(directory, matched_filename)
        else:
            return f"File tidak ditemukan. File yang tersedia: {', '.join(md_files)}"

        # Baca konten file yang ada
        with open(full_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        # Update konten file
        if title and title.strip():  # Cek jika title tidak kosong
            # Update original name di konten
            lines[1] = f"original name: {title}\n"
            
            # Buat nama file baru
            new_filename = f"DP_KMK_{title}.md"
            new_full_path = os.path.join(directory, new_filename)
            
            # Tutup file sebelum merename
            with open(full_path, "w", encoding="utf-8") as file:
                file.writelines(lines)
                
            try:
                # Rename file
                os.rename(full_path, new_full_path)
                full_path = new_full_path  # Update path untuk operasi selanjutnya
            except Exception as e:
                return f"Gagal mengubah nama file: {str(e)}"
        
        if author and author.strip():  # Cek jika author tidak kosong
            lines[2] = f"penulis: {author}\n"

        if year_published and year_published.strip():  # Cek jika year tidak kosong
            lines[3] = f"released: {year_published}\n"

        if genre and genre.strip():  # Cek jika genre tidak kosong
            genre_tags = " ".join([f"#{g.strip()}" for g in genre.split(",")])
            lines[4] = f"genres: {genre_tags}\n"

        if (
            last_chapter_read and last_chapter_read.strip()
        ):  # Cek jika chapter tidak kosong
            lines[6] = f"chapter on read: {last_chapter_read}\n"

        if (
            reading_platform and reading_platform.strip()
        ):  # Cek jika platform tidak kosong
            lines[7] = f"updated-by: {reading_platform}\n"

        # Tulis kembali file dengan konten yang diupdate
        with open(full_path, "w", encoding="utf-8") as file:
            file.writelines(lines)

        return f"File '{matched_filename}' telah diperbarui!"

    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"
