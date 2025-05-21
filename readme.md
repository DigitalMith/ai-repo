# 📸 Smart Batch Image Enhancer

**Version:** `v0.1.0`  
**License:** [MIT](LICENSE)  
**Author:** John Richards

A two-phase image enhancement workflow using Python and AI-powered analysis.
Easily generate lighting-aware suggestions and apply them to session-based photo sets.

---

## 🧠 Overview of Workflow

### Folder Structure
```
Batch_Script/
├── main.py                    # Unified launcher (preview or batch)
├── preview_enhancer.py        # Phase 1: Analyze & recommend settings
├── smart_batch_process.py     # Phase 2: Apply enhancement with config or overrides
├── session_config.json         # Generated config file from analysis
├── requirements.txt            # Minimal reproducible environment dependencies
├── sample_input/               # Selected examples from current lighting conditions
├── input/                      # Actual photos for processing
├── output/                     # Final exported images
├── pool/                       # Archive of all session photos (originals)
└── .gitignore                  # Prevents clutter from cache, output, and IDE files
```

---

## ⚙️ CLI Overrides (Optional)

### Defaults at a Glance
| Setting           | Default     | Description                            |
|------------------|-------------|----------------------------------------|
| Crop             | `no`        | No cropping unless `--crop yes`       |
| Format           | `png`       | Lossless export unless changed        |
| Max Resolution   | None        | Full original resolution unless `--max-dim` is set |
| Config File      | `session_config.json` | Used if present, otherwise fallback to defaults |
| Sharpness        | `1.3`       | Medium sharpening                      |
| Brightness       | `1.05`      | Slightly brighter                      |
| Contrast         | `1.1`       | Slightly boosted contrast              |

### Override with:
```bash
python smart_batch_process.py \
  --crop yes \
  --format jpg \
  --max-dim 2048 \
  --sharpness 1.5 \
  --brightness 1.2 \
  --contrast 1.2
```

Use these flags individually or combined with a config file.

---

## ✅ You’re Ready
Use `main.py` to launch either workflow with a single prompt.
Keep your image sessions clean, session-tuned, and ready to publish.

For enhancements, automation, or GUI integration—just say the word.
