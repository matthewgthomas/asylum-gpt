from flask import Flask, render_template, request
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

app = Flask(__name__)

db = SQLDatabase.from_uri("sqlite:///asylum.db")
llm = OpenAI(temperature = 0, openai_api_key="<Your OpenAI API key goes here>")
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']

        # Process the query with GPT-3.5 and LangChain
        result = process_query(query)

        return render_template('index.html', result=result)
    return render_template('index.html')

def process_query(query):
    result = db_chain.run(query)
    return result

if __name__ == '__main__':
    app.run(debug=True)
