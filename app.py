from flask import Flask, request, Response, render_template
from urllib.parse import urlparse
import requests

app = Flask(__name__)

# سيشن واحدة بتتشارك الاتصالات (connection pooling) بدل ما كل ريكوست
# يعمل اتصال TCP/TLS جديد من الصفر مع سيرفر اللعبة
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

# منسمحش إلا بالدومين بتاع سيرفر اللعبة، عشان الـ proxy ميتحولش
# لأداة يقدر أي حد يستخدمها يجيب أي رابط عايزه من خلال سيرفرنا
ALLOWED_HOST = "res353loar.creaction-network.com"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/proxy_swf')
def proxy_swf():
    # استلام الرابط من الواجهة
    swf_url = request.args.get('url')

    if not swf_url:
        return "لم يتم توفير رابط", 400

    if urlparse(swf_url).hostname != ALLOWED_HOST:
        return "رابط غير مسموح به", 403

    try:
        # الذهاب لسيرفر اللعبة لجلب الملف
        res = session.get(swf_url, timeout=10)
        res.raise_for_status()

        response = Response(res.content, mimetype='application/x-shockwave-flash')
        # الملفات دي ثابتة ومش بتتغير، فخلي المتصفح (وشبكة Vercel نفسها)
        # يكاشوا الرد لمدة سنة، عشان الطلبات اللي بعد كده متعملش راوند-تريب
        # لسيرفر اللعبة تاني خالص
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        return response
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
