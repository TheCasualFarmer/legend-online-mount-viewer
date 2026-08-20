from flask import Flask, request, Response, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/proxy_swf')
def proxy_swf():
    # استلام الرابط من الواجهة
    swf_url = request.args.get('url')
    
    if not swf_url:
        return "لم يتم توفير رابط", 400
        
    try:
        # الذهاب لسيرفر اللعبة لجلب الملف
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(swf_url, headers=headers, timeout=10)
        
        # إرجاع الملف للمتصفح كملف فلاش (SWF)
        return Response(res.content, mimetype='application/x-shockwave-flash')
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)