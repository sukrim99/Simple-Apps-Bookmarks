import os
import difflib
from pathlib import Path

""" OPRATION UPDATE BOOKMARK """


def search_book_md(filename: str) -> dict:
    """
    Mencari dan membaca konten file markdown.

    Args:
        filename (str): Nama file yang dicari

    Returns:
        dict: {
            'success': bool,
            'filename': str | None,
            'content': str | None,
            'message': str | None
        }
    """
    directory = Path(__file__).parent.parent / "library_komik_md"
    
    try:
        md_files = list(directory.glob("*.md"))
        if not md_files:
            return {
                "success": False,
                "message": "Tidak ada file markdown yang ditemukan"
            }

        # Persiapkan nama file untuk pencarian
        filename_clean = filename.lower().replace(".md", "")
        md_files_clean = [f.stem.lower() for f in md_files]

        # Cari file yang paling cocok
        matches = difflib.get_close_matches(
            filename_clean, 
            md_files_clean,
            n=1,
            cutoff=0.3
        )

        if not matches:
            return {
                "success": False,
                "message": f"File tidak ditemukan. Tersedia: {', '.join(f.name for f in md_files)}"
            }

        # Ambil file yang cocok
        matched_file = md_files[md_files_clean.index(matches[0])]
        content = matched_file.read_text(encoding="utf-8")

        return {
            "success": True,
            "filename": matched_file.name,
            "content": content
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Terjadi kesalahan: {str(e)}"
        }


def update_book_md(
    filename, title, author, year_published, genre, last_chapter_read, reading_platform
):
    """
    Fungsi untuk memperbarui konten file.
    
    Args:
        filename (str): Nama file yang akan diupdate
        title (str): Judul buku baru
        author (str): Penulis baru
        year_published (str): Tahun terbit baru
        genre (str): Genre baru (dipisahkan dengan koma)
        last_chapter_read (str): Chapter terakhir baru
        reading_platform (str): Platform baru
    """
    directory = Path(__file__).parent.parent / "library_komik_md"
    try:
        # Pastikan direktori ada
        if not directory.exists():
            return f"Direktori tidak ditemukan: {directory}"

        # Dapatkan daftar file dengan path lengkap
        md_files = [f for f in os.listdir(directory) if f.endswith(".md")]
        filename_clean = filename.lower().replace(".md", "")
        md_files_clean = [f.lower().replace(".md", "") for f in md_files]

        # Cari kecocokan
        close_matches = difflib.get_close_matches(
            filename_clean, md_files_clean, n=1, cutoff=0.3
        )

        if not close_matches:
            return f"File tidak ditemukan. File yang tersedia: {', '.join(md_files)}"

        matched_index = md_files_clean.index(close_matches[0])
        matched_filename = md_files[matched_index]
        full_path = os.path.join(directory, matched_filename)

        # Baca konten file yang ada dan parse metadata
        with open(full_path, "r", encoding="utf-8") as file:
            content = file.read()
            
        # Pisahkan metadata dan konten
        parts = content.split("---", 2)
        if len(parts) < 3:
            return "Format file tidak valid"
            
        metadata_lines = parts[1].strip().split('\n')
        metadata = {}
        
        # Parse metadata yang ada
        for line in metadata_lines:
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        
        # Update metadata dengan nilai baru jika ada
        if title and title.strip():
            metadata["original name"] = title
        if author and author.strip():
            metadata["penulis"] = author
        if year_published and year_published.strip():
            metadata["released"] = year_published
        if genre and genre.strip():
            # Format genre baru dengan # dan hapus duplikasi
            genres = [g.strip() for g in genre.split(',')]
            unique_genres = list(dict.fromkeys(genres))  # Hapus duplikasi
            metadata["genres"] = ' '.join(f"#{g}" for g in unique_genres)
        if last_chapter_read and last_chapter_read.strip():
            metadata["chapter on read"] = last_chapter_read
        if reading_platform and reading_platform.strip():
            metadata["updated-by"] = reading_platform

        # Buat konten file baru
        new_content = ["---"]
        for key, value in metadata.items():
            new_content.append(f"{key}: {value}")
        new_content.append("---")
        if len(parts) > 2:
            new_content.append(parts[2].strip())
        
        # Tulis kembali file
        with open(full_path, "w", encoding="utf-8") as file:
            file.write('\n'.join(new_content))

        # Jika judul diubah, rename file
        if title and title.strip():
            new_filename = f"DP_KMK_{title}.md"
            new_full_path = os.path.join(directory, new_filename)
            if full_path != new_full_path:
                try:
                    os.rename(full_path, new_full_path)
                except Exception as e:
                    return f"File diupdate tapi gagal mengubah nama: {str(e)}"

        return f"File '{matched_filename}' telah diperbarui!"

    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"
