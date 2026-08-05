import json

def save_report(results, output_file="report.json"):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

def print_summary(results):
    infected = sum(1 for r in results if r["status"] == "infected")
    clean = sum(1 for r in results if r["status"] == "clean")
    errors = sum(1 for r in results if r["status"] == "error")

    print(f"Clean: {clean}")
    print(f"Infected: {infected}")
    print(f"Errors: {errors}")