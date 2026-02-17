import argparse
import json
from parser import parse_pdf


def main():
    parser = argparse.ArgumentParser(description="PDF invoice -> JSON extractor")
    parser.add_argument("pdf_path", help="Path to input PDF")
    parser.add_argument(
        "-o", "--output", help="Path to output JSON file (default: stdout)"
    )
    args = parser.parse_args()

    data = parse_pdf(args.pdf_path)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
