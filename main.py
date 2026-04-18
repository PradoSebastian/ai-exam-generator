import asyncio
import logging

from app.business.image_service import image_service

logger = logging.getLogger(__name__)

async def main():
    logger.info("El programa ha iniciado correctamente.")

    await image_service.trigger_image_processing_runner()

    logger.info("El programa ha finalizado correctamente.")

if __name__ == "__main__":
    asyncio.run(main())
