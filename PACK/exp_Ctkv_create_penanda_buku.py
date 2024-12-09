import os
from pathlib import Path
import random


def create_book_md(
    title: str,
    author: str,
    year_published: str,
    genre: str,
    last_chapter_read: str,
    reading_platform: str,
    description: str,
    type_choice: str,
    cover_input: str,
) -> str:
    """
    Membuat file markdown penanda buku.

    Args:
        title (str): Judul buku
        author (str): Nama penulis
        year_published (str): Tahun terbit
        genre (str): Genre buku (dipisahkan dengan koma)
        last_chapter_read (str): Chapter terakhir dibaca
        reading_platform (str): Platform membaca
        description (str): Deskripsi buku
        type_choice (str): Tipe buku (manhwa/manhua)
        cover_input (str): URL/path cover buku

    Returns:
        str: Path file yang dibuat

    Raises:
        ValueError: Jika title kosong
        Exception: Jika terjadi kesalahan saat membuat file
    """
    if not title.strip():
        raise ValueError("Judul buku tidak boleh kosong")

    try:
        base_dir = Path(__file__).parent.parent / "library_komik_md"
        base_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "original name": title,
            "cover": format_cover(cover_input),
            "penulis": author,
            "released": year_published,
            "genres": format_genres(genre),
            "type": f"#{type_choice}",
            "chapter on read": last_chapter_read,
            "updated-by": reading_platform
        }

        md_content = ["---"]
        md_content.extend(f"{key}: {value}" for key, value in metadata.items())
        md_content.extend([
            "---\n",
            f"**deskripsi:** {description or 'Silakan isi deskripsi buku di sini.'}\n",
            "Silakan lengkapi keterangan buku di atas."
        ])

        file_path = base_dir / create_safe_filename(title)
        file_path.write_text("\n".join(md_content), encoding="utf-8")

        return str(file_path)

    except Exception as e:
        raise Exception(f"Gagal membuat file markdown: {str(e)}")


def format_cover(cover_input: str) -> str:
    """Format cover link/path untuk markdown."""
    if not cover_input:
        return "No cover"
    if cover_input.startswith(("http://", "https://")):
        return f"![cover]({cover_input})"
    return f"![[{cover_input}]]"


def format_genres(genre: str) -> str:
    """Format genre string menjadi tags."""
    if not genre:
        return ""
    return " ".join(f"#{g.strip()}" for g in genre.split(","))


def create_safe_filename(title: str) -> str:
    """Buat nama file yang aman dengan kode unik."""
    # Bersihkan judul dari karakter tidak aman
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_")).strip()
    # Buat kode unik
    unique_code = f"DP_KMK_{random.randint(0, 9999):04d}"
    return f"{unique_code}_{safe_title}.md"


# Contoh penggunaan
if __name__ == "__main__":
    try:
        file_path = create_book_md(
            title="Contoh Buku",
            author="Penulis Test",
            year_published="2024",
            genre="Fantasy, Action",
            last_chapter_read="10",
            reading_platform="Website Test",
            description="Ini adalah deskripsi buku test",
            type_choice="Novel",
            cover_input="",
        )
        print(f"File berhasil dibuat di: {file_path}")
    except Exception as e:
        print(f"Error: {e}")
