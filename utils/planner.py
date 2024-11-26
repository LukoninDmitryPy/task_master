import asyncio
import traceback
from datetime import datetime

from utils.log import get_logger
from config import MAX_ERR


logger = get_logger(__name__)
def planner(interval):
        ''' Simple regular async jobs planner
        If job complete faster then interval
        it starts again immediately
        else sleep while interval time
            interval: int (minutes)
        '''
        def deco(f):
            async def wrapped(self, *args, **kwargs):
                logger.info(f"Interval of {f.__name__}: {interval} minutes")
                errCount = 0
                while errCount < MAX_ERR:
                    start = datetime.now()
                    logger.info(f'Start {f.__name__} at: {start.isoformat()}')
                    try:
                        await f(self, *args, **kwargs)
                    except:
                        e = traceback.format_exc()
                        errCount += 1
                        logger.error(f"Runtime error: {e}. Errors count {errCount} from max {MAX_ERR}")
                        continue
                    logger.info(f'End {f.__name__} at: {start.isoformat()}')
                    logger.debug(f'Delta {f.__name__}: {datetime.now() - start}')
                    downtime = interval * 60 - (datetime.now() - start).seconds
                    if downtime > 0:
                        logger.info(f'Sleep {f.__name__} for {downtime} seconds')
                        await asyncio.sleep(downtime)
                else:
                    logger.error(f"Max runtime errors exceeded on job {f.__name__}! Stop service")
                    raise KeyboardInterrupt

            return wrapped

        return deco
