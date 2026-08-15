# URL Shortener

This is a small Django project that changes a long web address into a short link. It also counts how many times each short link is opened.

## Run the full project with CMD (Windows)

1. Install Python 3 if it is not already installed.
2. Open **Command Prompt** in this project folder.
3. Run this command:

```cmd
run_project.bat
```

If Command Prompt is open in a different folder, first go to the project folder:

```cmd
cd /d "C:\Users\abc\Desktop\Learning\projects\url"
run_project.bat
```

4. Wait for the server to start, then open http://127.0.0.1:8000/ in your browser.

You can also start the project by double-clicking `run_project.bat`.

`run_project.bat` runs the full setup automatically:

- creates a `.venv` virtual environment;
- activates the environment;
- installs the required packages;
- creates `.env` from `.env.example` when needed;
- updates the database; and
- starts the Django server.

To stop the server, press `Ctrl + C` in the command window.

## Use the website

Paste a long URL on the home page and click **Shorten**. Open the new short link to visit the original page. The page also provides a link to its click data.

## API (optional)

Create a short link:

```http
POST /api/links/
Content-Type: application/json

{"original_url": "https://example.com/a-long-page"}
```

View one link:

```text
GET /api/links/{code}/
```

View its click data:

```text
GET /api/links/{code}/analytics/
```

## Database

The project uses a local SQLite database by default, so no database setup is required. To use PostgreSQL instead, add this line to `.env` and change it to match your database:

```text
DATABASE_URL=postgresql://username:password@localhost:5432/url_shortener
```
