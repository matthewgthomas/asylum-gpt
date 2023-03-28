from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openai

# Replace with your OpenAI API key
openai.api_key = "your_openai_api_key_here"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database_file.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define your database models here
# For example:
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     ...

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        # Process the query with GPT-4 and SQLite
        result = process_query(query)
        return render_template('index.html', result=result)
    return render_template('index.html')

def get_database_schema():
    result = db.session.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in result.fetchall()]

    schema = []
    for table in tables:
        result = db.session.execute(f"PRAGMA table_info({table});")
        fields = [column[1] for column in result.fetchall()]
        schema.append(f"{table} ({', '.join(fields)})")

    return ', '.join(schema)

def process_query(query):
    database_schema = get_database_schema()
    prompt = f"Given a SQLite database with the following tables: {database_schema}, process the following natural language query: '{query}'."
    response = openai.Completion.create(
        engine="text-davinci-002",  # GPT-4 should be available as an engine
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    sql_query = response.choices[0].text.strip()
    result = execute_sql(sql_query)
    return result

def execute_sql(sql_query):
    try:
        result = db.session.execute(sql_query)
        return result.fetchall()
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
