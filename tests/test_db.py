from main import app, db

@app.route('/test-db')
def test_db():
    try:
        db.session.execute('SELECT 1')
        return 'Database connection is working!'
    except Exception as e:
        return f'Database connection failed: {e}'