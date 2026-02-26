from fastapi import APIRouter, HTTPException
from services.market_service import MarketService
from utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__, 'market_api.log')


@router.get("/overview")
async def get_market_overview():
    service = MarketService()
    try:
        return service.get_market_overview()
    except Exception as e:
        logger.error(f"市场概览接口失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
