import os
import pytesseract
from PIL import Image
from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Render 上不需要手動指定 tesseract_cmd，系統會自動辨識路徑（若套件安裝正確）
# 若需手動設定，使用以下方式：
# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Ubuntu 預設路徑

@app.route("/ocr", methods=["POST"])
def ocr():
    if "image" not in request.files:
        return jsonify({"error": "請附上 image 圖片欄位"}), 400

    image_file = request.files["image"]
    npimg = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # 轉灰階 + 二值化（提升辨識準確度）
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    try:
        text = pytesseract.image_to_string(thresh, lang="eng")
        return jsonify({"text": text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "✅ OCR API 運作中，請使用 POST /ocr 上傳圖片"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
