import os
import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)

# 初始化 Textract 用戶端
textract = boto3.client(
    'textract',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="ap-northeast-1"
)

@app.route("/ocr", methods=["POST"])
def ocr():
    if "image" not in request.files:
        return jsonify({"error": "請附上 image 圖片欄位"}), 400

    image_file = request.files["image"]
    image_bytes = image_file.read()

    try:
        response = textract.detect_document_text(Document={"Bytes": image_bytes})
        lines = [block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"]
        return jsonify({"lines": lines})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
