import argparse
import os
from importlib import import_module
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main() -> None:
    parser = argparse.ArgumentParser(description="Check the Picky Agent environment.")
    parser.add_argument("--robot", action="store_true", help="Also check LeRobot and device dependencies.")
    args = parser.parse_args()

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        parser.error("Set GEMINI_API_KEY in the project .env or in your shell.")

    model = os.environ.get("GEMINI_MODEL", "").strip() or "gemini-robotics-er-2-preview"
    with genai.Client(api_key=api_key, http_options=types.HttpOptions(api_version="v1beta")):
        print(f"Gemini client configured for {model}.")

    if args.robot:
        for module in ("lerobot.robots.so_follower", "cv2", "rustypot", "serial"):
            import_module(module)
        print("LeRobot, camera, and serial dependencies loaded.")


if __name__ == "__main__":
    main()
