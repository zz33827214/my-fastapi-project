from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# 設定 TDX 的 Client ID 和 Client Secret
token_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
client_id = "s11127079-a351144b-2414-44a8"  # 替換為你的 Client ID
client_secret = "34d757ac-fdf7-4d15-a4a1-16c4961fca90"  # 替換為你的 Client Secret

# 函數：取得 TDX 的 Access Token
def get_access_token():
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    try:
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        return response.json()['access_token']
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"獲取 Token 失敗: {e}")

# 新增根路由
@app.get("/")
def read_root():
    return {"message": "Welcome to the THSR timetable API!"}

# API 端點：取得高鐵時刻表
@app.get("/thsr_timetable")
def thsr_timetable():
    access_token = get_access_token()
    url = "https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/DailyTimetable/Today?$top=1000&$format=JSON"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"請求 TDX 資料失敗: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
