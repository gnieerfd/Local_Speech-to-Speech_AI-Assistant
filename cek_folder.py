import os

# Cek struktur folder secara otomatis
path_modules = os.path.join(os.getcwd(), "modules")
init_file = os.path.join(path_modules, "__init__.py")

print(f"DEBUG: Lokasi lo sekarang -> {os.getcwd()}")
print(f"DEBUG: Folder 'modules' ada? -> {os.path.exists(path_modules)}")
print(f"DEBUG: File '__init__.py' ada? -> {os.path.exists(init_file)}")

if not os.path.exists(path_modules):
    print("FIX: Rename folder 'src' lo jadi 'modules'!")
if not os.path.exists(init_file):
    print("FIX: Buat file kosong bernama '__init__.py' di dalam folder 'modules'!")