# MP3 Cutter

![screenshot](/assets/screenshot1.png)

## Features

• Drag-and-drop or browse to open MP3, WAV, OGG, FLAC.  
• Real-time waveform visualization with smooth zoom (mouse wheel).  
• Interactive selection:  
 – Drag triangular markers for start/end.  
 – Or type exact time in HH:mm:ss.zzz fields.  
• Instant preview – play only the selected region.  
• One-click export to MP3 with original bitrate or 192 kbps fallback.  


## Prerequesties

   ```bash
   pip install PyQt5 matplotlib pydub numpy math
   ```

## Quick Start

1. Run the program  
   ```bash
   python .\mp3cutter.py
   ```

2. **Open audio file**  
   • Drag & drop onto the window, or  
   • Click “Load MP3 File…”

3. **Set clip range**  
   • Drag ▼  (start) and ▲ (end) arrows on the waveform, or  
   • Edit the “Start / End” time boxes.

4. **Preview**  
   Click ▶ Play to hear only the selected audio range.

5. **Export clip**  
   Click “Export Clip”, choose a destination, done!


