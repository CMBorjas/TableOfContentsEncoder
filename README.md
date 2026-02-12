# TableOfContentsEncoder

A utility for generating and encoding Table of Contents (TOC) into mnemonic memory palaces. This project analyzes TOC topics and creates cognitive correlations based on **randomized absurd imagery** and **dual-scent Proustian anchors**.

## Features

* **TOC Analysis:** Automatically scans documents to generate structured hierarchies.
* **Mnemonic Encoding:** Maps chapters to specific "Loci" (locations) and "Actors" (subjects).
* **Dual-Scent Anchoring:** Generates a **Positive Scent** (Success/Methodology) and a **Bad Scent** (Problem/Trouble) for synesthetic memory retention.
* **Flashcard Export:** Formats output for seamless integration with **Anki**, **Quizlet**, and other spaced-repetition software.

## Installation

```bash
git clone https://github.com/CMBorjas/TableOfContentsEncoder.git
cd TableOfContentsEncoder
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

```

## Usage (Terminal Mode)

```bash
python toc_encoder.py input_file.md --mnemonic

```

---

## Enterprise-Level Optimization Roadmap

To transition this from a script to a professional-grade GUI application, the following techniques are being implemented:

### 1. The Method of Loci Engine (Mnemonic Logic)

We utilize a **Synesthetic Mapping** technique. For example:

* **Target:** *Chapter 24: Network Troubleshooting Methodology*
* **Locus:** A 24-Hour Diner (Numerical anchor).
* **Actor:** A Neon Spider (Network subject).
* **Positive Scent (+):** Eucalyptus & Ozone (The smell of a working system).
* **Bad Scent (-):** Scorched Hair (The smell of a technical failure).

### 2. Decoupled Architecture (TUI to GUI)

To ensure the program scales, we are moving toward a **Model-View-Controller (MVC)** pattern:

* **Core Logic:** The encoding and imagery generation is handled by a standalone Python API.
* **Current Interface:** A **TUI (Terminal User Interface)** using `Click` or `Textual` for high-performance CLI interaction.
* **Future Interface:** A **Gradio** or **Streamlit** wrapper to provide a web-accessible GUI for non-technical users.

### 3. Asynchronous Processing

Enterprise applications must handle large documents without freezing. We use `asyncio` to allow the TOC scanning and imagery generation to run in parallel, ensuring the UI remains responsive during heavy computation.

### 4. Database Persistence

Switching from flat-file JSON to a vector-based or relational database (like `Qdrant` or `SQLite`) to store user-specific memory palaces, allowing for long-term study tracking and data persistence.

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/ScaleToGUI`)
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

MIT License - See [LICENSE](https://www.google.com/search?q=LICENSE) for details.


Old:
# TableOfContentsEncoder

A utility for generating and encoding table of contents (TOC) for documents or files. This project takes the Table of contents analysizes the topics and creates correlations based on randomized absurd imagery, as well Proust scents tied directly form the TOC.

## Features

- Automatically scans documents to generate a structured TOC
- Encodes TOC in various formats (JSON, Markdown, etc.)
- Easy integration with existing documentation workflows

## Installation

```bash
git clone https://github.com/yourusername/TableOfContentsEncoder.git
cd TableOfContentsEncoder
# Install dependencies if applicable
```

## Usage

```bash
python toc_encoder.py input_file.md
```

- Replace `input_file.md` with your target document.

## Configuration

- Customize encoding formats and output options in the configuration file or via command-line arguments.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, open an issue on the repository.
