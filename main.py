from scanner import load_signatures, scan_folder, quarantine_file
from report import save_report, print_summary

TARGET_DIR = r"C:\Users\shado\OneDrive\Documents\VSC"
SIGNATURES_PATH = r"C:\Users\shado\OneDrive\Documents\VSC\signatures.json"
QUARANTINE_DIR = r"C:\Users\shado\OneDrive\Documents\VSC\quarantine"
REPORT_PATH = r"C:\Users\shado\OneDrive\Documents\VSC\report.json"

def main():
    signatures = load_signatures(SIGNATURES_PATH)
    results = scan_folder(TARGET_DIR, signatures)

    print_summary(results)

    for result in results:
        print(result["file"], result["hash"], result["status"])
        if result["status"] == "infected":
            print(f"[ALERT] {result['file']} matched {result['signature']['name']}")
            quarantined_path = quarantine_file(result["file"], QUARANTINE_DIR)
            print(f"Quarantined to: {quarantined_path}")

    save_report(results, REPORT_PATH)
    print(f"Scan complete. Report saved to {REPORT_PATH}")

if __name__ == "__main__":
    main()