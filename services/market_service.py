from typing import Dict, Optional
from datetime import datetime, timedelta
from utils.logger import setup_logger
from core.database import get_sync_connection

logger = setup_logger(__name__, 'market_service.log')

WAN_TO_WAN_YI = 1e8


class MarketService:
    _overview_cache: Optional[Dict] = None
    _cache_expire_time: Optional[datetime] = None
    _cache_duration = timedelta(minutes=30)

    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = get_sync_connection()
        except Exception as e:
            logger.error(f"获取数据库连接失败: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()

    @classmethod
    def _is_cache_valid(cls) -> bool:
        if cls._overview_cache is None or cls._cache_expire_time is None:
            return False
        return datetime.now() < cls._cache_expire_time

    @classmethod
    def _update_cache(cls, data: Dict):
        cls._overview_cache = data
        cls._cache_expire_time = datetime.now() + cls._cache_duration

    def get_market_overview(self, force_refresh: bool = False) -> Dict:
        if not force_refresh and self._is_cache_valid():
            return self._overview_cache

        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("SELECT MAX(trade_date) as latest FROM stk_factor_pro_data")
            row = cursor.fetchone()
            trade_date = (row[0] or "").strip() if row and row[0] else ""

            if not trade_date:
                cursor.close()
                self.close()
                result = {"activeMarketCap": 0.0, "totalMarketCap": 0.0, "tradeDate": ""}
                self._update_cache(result)
                return result

            cursor.execute(
                """
                SELECT
                  COALESCE(SUM(CASE WHEN amount > 0 THEN circ_mv ELSE 0 END), 0) as active_mv,
                  COALESCE(SUM(total_mv), 0) as total_mv
                FROM stk_factor_pro_data
                WHERE trade_date = %s
                """,
                (trade_date,),
            )
            row = cursor.fetchone()
            cursor.close()
            self.close()

            active_mv_wan = float(row[0] or 0)
            total_mv_wan = float(row[1] or 0)
            result = {
                "activeMarketCap": round(active_mv_wan / WAN_TO_WAN_YI, 4),
                "totalMarketCap": round(total_mv_wan / WAN_TO_WAN_YI, 4),
                "tradeDate": trade_date,
            }
            self._update_cache(result)
            return result
        except Exception as e:
            logger.error(f"get_market_overview 失败: {e}")
            if self.conn:
                self.close()
            raise
