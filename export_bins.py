#!/usr/bin/env python3
"""
KIWI Firmware - Arduino IDE Build Export Script
================================================
Arduino IDE la compile ஆன .bin files-ஐ
kiwi-flasher/bins/ folder-க்கு copy பண்ணும்.

Usage:
  python export_bins.py

Requirements:
  - Arduino IDE 2.x use பண்ணியிருக்கணும்
  - Once "Verify" (compile) பண்ணியிருக்கணும்
"""

import os, sys, shutil, glob, platform, subprocess
from pathlib import Path

# ─── Config ──────────────────────────────────────────────────────────────────
BOARD_FQBN   = "esp32:esp32:esp32s3"         # Board Manager board FQBN
OUTPUT_DIR   = Path(__file__).parent / "bins"  # Output: kiwi-flasher/bins/

# Arduino IDE 2.x temp build cache location (change if needed)
if platform.system() == "Windows":
    BUILD_CACHE_ROOT = Path(os.environ.get("TEMP", "C:/Users/Public/Temp")) / "arduino"
elif platform.system() == "Darwin":
    BUILD_CACHE_ROOT = Path.home() / "Library/Caches/arduino/sketches"
else:
    BUILD_CACHE_ROOT = Path.home() / ".cache/arduino/sketches"

# Files we need (name → flash offset in decimal)
REQUIRED_BINS = {
    "bootloader.bin" : 0x0000,      # 0
    "partitions.bin" : 0x8000,      # 32768
    "boot_app0.bin"  : 0xE000,      # 57344
    # firmware.bin name varies — matched by *.ino.bin pattern below
}

# ─── Helpers ─────────────────────────────────────────────────────────────────
def find_latest_build_dir():
    """Find the most recently modified sketch build folder."""
    candidates = list(BUILD_CACHE_ROOT.glob("**/bootloader.bin"))
    if not candidates:
        return None
    # Sort by mtime, pick newest
    latest = max(candidates, key=lambda p: p.stat().st_mtime)
    return latest.parent

def copy_with_verify(src: Path, dst: Path, label: str):
    if not src.exists():
        print(f"  [ERROR] {label} not found: {src}")
        return False
    shutil.copy2(src, dst)
    size_kb = src.stat().st_size / 1024
    print(f"  [OK] {label:<20}  {size_kb:6.1f} KB  →  {dst.name}")
    return True

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  KIWI Firmware Bin Exporter")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    build_dir = find_latest_build_dir()
    if not build_dir:
        print(f"\n[ERROR] Arduino build cache not found under:\n  {BUILD_CACHE_ROOT}")
        print("\nFix: Arduino IDE la sketch-ஐ ஒரு முறை Verify (Ctrl+R) பண்ணுங்க.")
        sys.exit(1)

    print(f"\nBuild dir found:\n  {build_dir}\n")
    print("Copying bins:")

    ok = True

    # bootloader, partitions, boot_app0
    for fname in ("bootloader.bin", "partitions.bin", "boot_app0.bin"):
        src = build_dir / fname
        ok &= copy_with_verify(src, OUTPUT_DIR / fname, fname)

    # firmware.bin — Arduino IDE names it <SketchName>.ino.bin
    fw_candidates = list(build_dir.glob("*.ino.bin"))
    if fw_candidates:
        # Pick the newest if multiple
        fw_src = max(fw_candidates, key=lambda p: p.stat().st_mtime)
        ok &= copy_with_verify(fw_src, OUTPUT_DIR / "firmware.bin", "firmware.bin")
    else:
        # fallback: sometimes just .bin in root
        fw_candidates2 = [
            f for f in build_dir.glob("*.bin")
            if f.name not in ("bootloader.bin", "partitions.bin", "boot_app0.bin")
        ]
        if fw_candidates2:
            fw_src = max(fw_candidates2, key=lambda p: p.stat().st_mtime)
            ok &= copy_with_verify(fw_src, OUTPUT_DIR / "firmware.bin", "firmware.bin")
        else:
            print("  [ERROR] firmware.bin not found!")
            ok = False

    print()
    if ok:
        print("✅  All bins exported successfully!")
        print(f"   Folder: {OUTPUT_DIR.resolve()}")
        print("\nNext step:")
        print("  1. bins/ folder-ஐ kiwi-flasher/ உள்ளே வையுங்க")
        print("  2. GitHub repo-வுக்கு push பண்ணுங்க")
        print("  3. GitHub Pages enable பண்ணுங்க (Settings → Pages → main branch)")
        print("  4. URL share பண்ணுங்க → User chrome open பண்ணி flash!")
    else:
        print("❌  Some bins missing. Errors above பாருங்க.")
        sys.exit(1)

if __name__ == "__main__":
    main()
