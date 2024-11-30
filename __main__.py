

# local import
import PACK as pack


def main():
    """Fungsi utama untuk menjalankan aplikasi."""
    try:
        # Tampilkan menu utama
        pack.show_main_menu()

        # Jalankan aplikasi
        pack.root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()



