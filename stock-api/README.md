# 股票行情 API — Vercel 免费部署

## 部署步骤（5分钟搞定）

### 第一步：上传到 GitHub
1. 打开 https://github.com，注册/登录账号
2. 点右上角「+」→「New repository」，名字填 `stock-api`，点 Create
3. 把这个文件夹里的所有文件上传（拖进去即可）

### 第二步：部署到 Vercel
1. 打开 https://vercel.com，用 GitHub 账号登录
2. 点「Add New Project」→ 选择刚才的 `stock-api` 仓库
3. 直接点「Deploy」，等1分钟
4. 部署成功后你会得到一个地址，比如：`https://stock-api-xxx.vercel.app`

### 第三步：测试接口
在浏览器打开：
```
https://你的地址.vercel.app/api/quote?code=600519
```
如果看到 JSON 数据就成功了！

---

## 接口说明

**请求**
```
GET /api/quote?code=股票代码
```

**股票代码规则**
- 上证 6 开头：600519（贵州茅台）、601318（中国平安）
- 深证 0/3 开头：000858（五粮液）、300750（宁德时代）

**返回示例**
```json
{
  "code": "600519",
  "name": "贵州茅台",
  "current": 1825.00,
  "open": 1818.00,
  "prev_close": 1820.00,
  "high": 1835.00,
  "low": 1810.00,
  "change": 5.00,
  "change_pct": 0.27,
  "volume": 12345,
  "amount": 2.25,
  "date": "2026-05-31",
  "time": "15:00:00"
}
```

---

## 把真实数据接入 AI 分析工具

部署成功后，把你的 Vercel 地址填入上面的 AI 分析工具中，
工具就会自动拉取真实行情来做分析。
