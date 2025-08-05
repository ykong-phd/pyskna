# %%
import os
import sys
import tempfile
import urllib.request
import zipfile
import urllib.request

VFCDM_URL = "https://github.com/ykong-phd/vfcdm-binaries/releases/download/v1.0.0/vfcdm-v1.0.0.zip"
PACKAGE_DIR = os.path.dirname(__file__)  # Path to pyskna/

# Path to libs/ inside the package
INSTALL_DIR = os.path.join(PACKAGE_DIR, "libs")
os.makedirs(INSTALL_DIR, exist_ok=True)

LICENSE_URL = "https://raw.githubusercontent.com/ykong-phd/vfcdm-binaries/refs/heads/main/LICENSE.md"

def fetch_latest_license():
    with urllib.request.urlopen(LICENSE_URL) as response:
        return response.read().decode("utf-8")

def vfcdm_installed():
    return os.path.exists(INSTALL_DIR) and any(
        f.endswith((".dll", ".so", ".dylib")) for f in os.listdir(INSTALL_DIR)
    )

def prompt_license():
    LICENSE_TEXT = fetch_latest_license()
    print("\n=== VFCDM LICENSE AGREEMENT ===")
    print(LICENSE_TEXT)
    print("===============================")
    resp = input("Do you accept the terms? [yes/no]: ").strip().lower()
    return resp == "yes"

def download_and_install():
    print("Downloading VFCDM...")
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "vfcdm.zip")
        urllib.request.urlretrieve(VFCDM_URL, zip_path)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(INSTALL_DIR)
    print(f"VFCDM installed to {INSTALL_DIR}")

def ensure_vfcdm():
    if vfcdm_installed():
        return True
    if not prompt_license():
        print("You must accept the license to install VFCDM.")
        sys.exit(1)
    download_and_install()
    return True

if __name__ == "__main__":
    ensure_vfcdm()
