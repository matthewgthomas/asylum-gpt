from flask import Flask, render_template, request
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

app = Flask(__name__)

# Custom info for the "irregulat migration" table
irreg_table_info = {
    "irregular_migration": """
CREATE TABLE irregular_migration (
	"Date" REAL, 
	"Year" REAL, 
	"Quarter" INTEGER, 
	"Method_of_entry" TEXT, 
	"Nationality" TEXT, 
	"Region" TEXT, 
	"Sex" TEXT, 
	"Age_Group" TEXT, 
	"Number_of_detections" REAL
)
/*
3 rows from irregular_migration table:
Date	Year	Quarter	Method_of_entry	Nationality	Region	Sex	Age_Group	Number_of_detections
17532.0	2018.0	1	Inadequately documented air arrivals	Afghanistan	Asia Central	Female	18-24	4.0
17532.0	2018.0	1	Recorded detections in the UK	Afghanistan	Asia Central	Female	25-39	14.0
17532.0	2018.0	1	Small boat arrivals	Afghanistan	Asia Central	Female	40+	22.0
*/
"""
}

db = SQLDatabase.from_uri("sqlite:///asylum.db", custom_table_info = irreg_table_info)
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
