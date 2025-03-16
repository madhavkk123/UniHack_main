from flask import Flask, request, jsonify
import read_data
import scrape
import subject_page
import mongo_script

app = Flask(__name__)

@app.route("/notes", methods=["GET"])
def get_notes():
    """
    Returns the notes stored in the JSON file (studocu_data.json)
    using the read_data.read_json_file() function.
    """
    data = read_data.read_json_file()
    if data is None:
        return jsonify({"error": "Notes not found."}), 404
    return jsonify(data)

@app.route("/scrape", methods=["GET"])
def scrape_page():
    """
    Scrapes a Studocu page given a URL.
    URL should be provided as a query parameter, e.g.:
    /scrape?url=https://www.studocu.com/en-au/document/...
    """
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter."}), 400
    data = scrape.scrape_studocu(url)
    if not data:
        return jsonify({"error": "Scraping failed."}), 500
    return jsonify(data)

@app.route("/subject", methods=["GET"])
def get_subject():
    """
    Retrieves the top subject page URLs based on a user query.
    The query should be provided as a query parameter, e.g.:
    /subject?query=principles of finance uni melb
    """
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' parameter."}), 400
    urls = subject_page.get_subject_page_url(query)
    if urls is None:
        return jsonify({"error": "No subject page URLs found."}), 404
    return jsonify({"urls": urls})

@app.route("/mongo", methods=["POST"])
def insert_data_to_mongo():
    """
    Inserts data from a JSON file into MongoDB.
    Expects a JSON payload with optional keys:
      - json_file_path (default "studocu_data.json")
      - db_name (default "Database_unihack")
      - collection_name (default "query_responses")
    """
    payload = request.get_json()
    json_file_path = payload.get("json_file_path", "studocu_data.json")
    db_name = payload.get("db_name", "Database_unihack")
    collection_name = payload.get("collection_name", "query_responses")
    try:
        mongo_script.insert_json_to_mongodb(json_file_path, db_name, collection_name)
        return jsonify({"message": "Data inserted successfully into MongoDB."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ask", methods=["POST"])
def ask_question():
    """
    Uses the study assistant functionality.
    Expects a JSON payload with:
      - question: the student's question.
      - conversation_history (optional): list of previous exchanges.
    
    The function uses the JSON data from studocu_data.json as context.
    """
    payload = request.get_json()
    question = payload.get("question")
    conversation_history = payload.get("conversation_history", [])
    if not question:
        return jsonify({"error": "Missing 'question' parameter."}), 400
    context = read_data.read_json_file()
    answer = read_data.askQuestion(context, question, conversation_history)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
