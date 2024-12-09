import sys
import PACK as pack

def main():
    """Fungsi utama untuk menjalankan aplikasi penanda buku."""
    try:
        # Tampilkan menu utama
        pack.show_main_menu()
        pack.root.mainloop()
    except KeyboardInterrupt:
        print("\nAplikasi dihentikan oleh pengguna")
        sys.exit(0)
    except Exception as e:
        print(f"Terjadi kesalahan fatal: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()



