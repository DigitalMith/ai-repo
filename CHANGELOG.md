# 📦 Changelog

All notable changes to this project will be documented in this file.

---

## [v0.1.0] - Beta Preview
**Released:** _Planned for May 2025_

### 🚀 Initial Features
- Session-based workflow using `/pool`, `/sample_input`, `/input`, `/output`
- `preview_enhancer.py` analyzes sharpness, brightness, and contrast across sample images
- Auto-generates `session_config.json` based on image metrics
- `smart_batch_process.py` applies enhancements with:
  - Face-aware crop (toggleable)
  - Brightness, contrast, sharpness adjustment
  - Aspect-preserving resize
  - Export as PNG or JPG
- `main.py` launcher with basic CLI menu

### 🧪 Status
- Internal use only (beta/testing)
- No GUI
- Not yet performance-profiled or validated across wide hardware/photo types

---

## [v1.0.0] - Public Stable (coming soon)
**Planned:** After GUI implementation and field testing

### 🗓 Roadmap
- Full GUI with folder picker, preview toggle, batch control
- Side-by-side composite export
- Preset manager for Facebook/Instagram/Print
- Watch mode for `/input` folder
- Platform-agnostic bundling (Windows/macOS/Linux)

---

_This file uses [Semantic Versioning](https://semver.org)_
