from flask import Flask, jsonify
import database

app = Flask(__name__)

@app.route('/debug')
def debug():
    try:
        conn = database.get_connection()
        c = conn.cursor()
        c.execute('SELECT count(*) FROM businesses')
        res = c.fetchone()
        conn.close()
        # Handle simple tuple result from sqlite3.Row if needed, or index 0
        val = res[0] if res else 0
        return jsonify({'count': val})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("Starting debug server...")
    app.run(port=8001)
