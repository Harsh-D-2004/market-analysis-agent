from fastapi import FastAPI
from service import yfinance_scraping
from fastapi.responses import JSONResponse
from fastapi import status



app = FastAPI(port = 8001)

@app.get("/scrape")
async def scrape():
    ret = await yfinance_scraping()

    if not ret:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "No data found"}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"data": ret}
        )