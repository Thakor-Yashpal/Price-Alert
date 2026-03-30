from app import create_app
from app.services.gold_api import fetch_and_process_gold_price

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        print("🚀 Forcing initial gold price fetch...")
        try:
            fetch_and_process_gold_price()
        except Exception as e:
            print(f"Fetch failed: {e}")
            
    app.run(debug=True, use_reloader=False, threaded=True)