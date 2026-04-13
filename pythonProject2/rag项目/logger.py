# -*- coding: utf-8 -*-
#日志系统
import logging
import os
from datetime import datetime

log_path = "./logs"
os.makedirs(log_path, exist_ok=True)

log_file = os.path.join(log_path, f"rag_log_{datetime.now().strftime('%Y%m%d')}.log")

logger = logging.getLogger("rag_system")
logger.setLevel(logging.INFO)

# 避免重复添加 handler
if not logger.handlers:
    fh = logging.FileHandler(log_file, encoding="utf-8")
    ch = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)