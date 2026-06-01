from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # 解析请求参数
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        code = params.get('code', [''])[0].strip()

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        if not code:
            self.wfile.write(json.dumps({'error': '缺少股票代码'}).encode())
            return

        try:
            data = fetch_sina(code)
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
        except Exception as e:
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        pass  # 关闭日志输出


def fetch_sina(code):
    """
    从新浪财经拉取A股实时行情
    上证: sh600519  深证: sz000858
    自动补前缀
    """
    if code.startswith('6'):
        symbol = 'sh' + code
    elif code.startswith(('0', '3')):
        symbol = 'sz' + code
    elif code.lower().startswith(('sh', 'sz')):
        symbol = code.lower()
    else:
        symbol = 'sh' + code  # 默认上证

    url = f'http://hq.sinajs.cn/list={symbol}'
    req = urllib.request.Request(url, headers={
        'Referer': 'https://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0'
    })
    with urllib.request.urlopen(req, timeout=5) as resp:
        raw = resp.read().decode('gbk')

    # 解析新浪返回格式:
    # var hq_str_sh600519="贵州茅台,1820.00,1818.00,1825.00,1835.00,1810.00,..."
    inner = raw.split('"')[1]
    if not inner:
        raise ValueError(f'未找到股票: {code}')

    fields = inner.split(',')
    # 字段顺序: 名称,昨收,今开,现价,最高,最低,买1...卖5,成交量,成交额,...
    name     = fields[0]
    prev_close = float(fields[2])
    open_p   = float(fields[1])
    current  = float(fields[3])
    high     = float(fields[4])
    low      = float(fields[5])
    volume   = int(fields[8])    # 手
    amount   = float(fields[9])  # 元
    date     = fields[30] if len(fields) > 30 else ''
    time_str = fields[31] if len(fields) > 31 else ''

    change     = round(current - prev_close, 2)
    change_pct = round((current - prev_close) / prev_close * 100, 2) if prev_close else 0

    return {
        'code': code,
        'symbol': symbol,
        'name': name,
        'current': current,
        'open': open_p,
        'prev_close': prev_close,
        'high': high,
        'low': low,
        'change': change,
        'change_pct': change_pct,
        'volume': volume,
        'amount': round(amount / 1e8, 4),  # 转为亿元
        'date': date,
        'time': time_str,
    }
