# KIWI Web Flasher — Setup Guide

## Folder Structure
```
kiwi-flasher/
├── index.html          ← Flasher web page (user opens this URL)
├── manifest.json       ← Firmware manifest (ESP Web Tools reads this)
├── export_bins.py      ← Script to copy bins from Arduino build cache
├── README.md
└── bins/               ← CREATE THIS FOLDER (gitignore தவிர)
    ├── bootloader.bin
    ├── partitions.bin
    ├── boot_app0.bin
    └── firmware.bin
```

---

## Step 1 — Arduino IDE-ல Compile பண்ணுங்க

Arduino IDE 2.x open பண்ணி உங்க KIWI sketch-ஐ **Verify (Ctrl+R)** பண்ணுங்க.
Upload வேண்டாம் — compile மட்டும் போதும்.

Board settings:
```
Board:        ESP32S3 Dev Module
Partition:    (உங்களுக்கு use பண்ற custom partition scheme)
PSRAM:        OPI PSRAM
Flash Mode:   QIO 80MHz
```

---

## Step 2 — Bins Export பண்ணுங்க

```bash
cd kiwi-flasher/
python export_bins.py
```

`bins/` folder-ல 4 files வந்திருக்கணும்:
- `bootloader.bin`
- `partitions.bin`  
- `boot_app0.bin`
- `firmware.bin`

---

## Step 3 — GitHub-ல Host பண்ணுங்க (Free)

```bash
git init
git add .
git commit -m "KIWI flasher v4.0.0"
git remote add origin https://github.com/YOUR_USERNAME/kiwi-flasher.git
git push -u origin main
```

Then:
1. GitHub repo → **Settings** → **Pages**
2. Source: **Deploy from branch** → `main` → `/ (root)`
3. Save பண்ணுங்க

URL கிடைக்கும்: `https://YOUR_USERNAME.github.io/kiwi-flasher/`

---

## Step 4 — User Flash பண்றது (Super Simple)

1. KIWI-ஐ USB cable-ல PC-ல போடுங்க
2. **Google Chrome** open பண்ணுங்க
3. URL type பண்ணுங்க: `https://YOUR_USERNAME.github.io/kiwi-flasher/`
4. **"Flash Firmware"** button click பண்ணுங்க
5. COM port select பண்ணுங்க → **Install** confirm பண்ணுங்க
6. Done! 2 நிமிஷத்தில் flash ஆகிரும் ✅

---

## Firmware Update பண்ண (New Version)

```bash
# Sketch update பண்ணி compile (Ctrl+R)
python export_bins.py          # bins/ update ஆகும்
# manifest.json-ல version bump பண்ணுங்க
git add bins/ manifest.json
git commit -m "KIWI v4.1.0"
git push
```
User அடுத்த முறை URL open பண்ணினா new version flash ஆகும்.

---

## Important Notes

- Chrome / Edge மட்டும் Web Serial support பண்ணும் (Firefox இல்ல)
- HTTPS required — GitHub Pages auto-ஆ HTTPS கொடுக்கும்
- bins/ folder-ல ஒவ்வொரு முறையும் latest compile-ஆன files வேணும்
- `boot_app0.bin` Arduino ESP32 core-ல இருக்கும்:
  `~/.arduino15/packages/esp32/hardware/esp32/*/tools/partitions/boot_app0.bin`
  (export_bins.py auto-ஆ find பண்ணும், இல்லன்னா manually copy பண்ணுங்க)
