from flask import Flask, render_template, request, session
from works_manager import load_data
from scraper import scrape_book_content
from summarize import summarize_from_web

app = Flask(__name__, template_folder="../templates")
app.secret_key = "test_secret_key"
data = load_data()

# 選択中の作品
selected_work = {"title": None, "author": None, "url": None}


@app.route("/", methods=["GET", "POST"])
def index():
    global selected_work
    summary = session.get("summary", None)
    search_results = None

    # POSTリクエストの場合
    if request.method == "POST":
        # 作品選択処理
        if request.form.get("selected_work_title"):
            new_title = request.form.get("selected_work_title")
            print("new_title:", new_title)
            print("selected_work:", selected_work["title"])
            if selected_work["title"] != new_title:
                # 別の作品が選択された場合、要約をリセット
                print("Resetting summary for new selection.")
                session.pop("summary", None)
                summary = None
            selected_work["title"] = request.form.get("selected_work_title")
            selected_work["author"] = request.form.get("selected_work_author")
            selected_work["url"] = request.form.get("selected_work_url")

        # 要約機能
        if "summary" in request.form:
            text = scrape_book_content(selected_work["url"])
            print("text:", text[:100])
            try:
                summary = summarize_from_web(text)
                session["summary"] = summary
            except Exception as e:
                print(f"Error summarizing: {e}")
                summary = "要約に失敗しました。"
                session["summary"] = summary
        # 検索機能
        if "search" in request.form:
            search_query = request.form.get("search_query", "").strip()
            if search_query:
                search_results = data[
                    data["作品名"].str.contains(search_query, case=False, na=False)
                ]

    return render_template(
        "index.html",
        summary=summary,
        search_results=search_results,
        selected_work=selected_work,
    )


if __name__ == "__main__":
    app.run(debug=True)
