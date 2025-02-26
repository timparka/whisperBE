from flask import Blueprint, request, jsonify
from services.merge_service import process_and_merge_urls

video_bp = Blueprint('video', __name__)

@video_bp.route("/postURLs", methods=["POST"])
def post_urls():
    try:
        print("Received request on /postURLs")
        data = request.json
        chunk_urls = data.get("urls", [])
        
        print("Received URLs:", chunk_urls)

        if not chunk_urls:
            return jsonify({"error": "No URLs provided"}), 400

        output_file = "merged_video.mp4"
        message = process_and_merge_urls(chunk_urls, output_file)

        return jsonify({"message": message, "output_file": output_file}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
