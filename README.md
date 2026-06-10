<div align="center">
  <h1>⚡ LogicFlow v2.0</h1>
  <p><strong>Modern Logic Circuit Generator</strong></p>
</div>

LogicFlow is a completely revamped, modern logic circuit drawing software designed to offer a professional and streamlined UX/UI experience. Simply type your logic expression or use the built-in smart keypad, and LogicFlow will instantly draw the corresponding logic circuit diagram in real-time!

## ✨ Features

- **Modern UI:** A sleek, eye-friendly, and responsive interface built with CustomTkinter.
- **Calculator-style Keypad:** No need to type equations manually! Use the smart keypad featuring variables (A-F) and logic gates (AND, OR, NOT, XOR, NAND, NOR, XNOR) to easily build your logic equations with simple clicks.
- **Live Step-by-Step Preview:** Your logic circuit is drawn and updated in real-time as you type or press buttons. Our smart system ignores temporary syntax errors while typing to ensure an uninterrupted experience.
- **Smart Input & Processing:** Full support for Copy/Paste functionality for long and complex multi-line equations, alongside automatic case-insensitivity recognition for logic gates.
- **Quick Export:** Conveniently save and export your generated circuit diagram as a high-resolution PNG image for easy sharing and integration into documents.

## 🚀 Download & Installation

LogicFlow is available as a standalone executable (`.exe`) file, ready for direct download and immediate use without the need for any pre-installation, Python environment, or setup!

👉 **[Download the Latest Release here](https://github.com/badawika-tech/gateFlow/releases/**

### Download Older Versions
To download previous versions or explore all available releases, please visit the **[Releases](https://github.com/badawika-tech/gateFlow/releases)** section.

## 🛠️ Development & Building from Source

If you'd like to build the executable yourself or run the app from its source code:

### Prerequisites

Ensure you have Python 3.12+ installed, along with the necessary libraries.

```bash
git clone https://github.com/badawika-tech/gateFlow.git
cd gateFlow
pip install -r requirements.txt
```

### Running the Source

```bash
python final_draw_gates.py
```

### Building the Executable

We use `PyInstaller` to build the standalone executable. A `.spec` file is already provided:

```bash
pyinstaller final_draw_gates.spec
```

The compiled `.exe` file will be located in the `dist` folder.

## 👨‍💻 Credits

**Programming & Design by:** Sima for Digital Solutions - Ahmed Elbadawi

---
*Tags: #LogicFlow #DigitalDesign #LogicGates #Python #CustomTkinter #SoftwareDevelopment #SimaDigitalSolutions #Engineering #ComputerScience #Tech*
