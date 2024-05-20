from src.constants import *
import os
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    DATA_INGESTION_ARTIFACT_DIR = os.path.join (ARTIFACT_DIR, DATA_INGESTION_ARTIFACT_DIR)
    DATA_FILE_PATH = os.path.join(DATA_INGESTION_ARTIFACT_DIR, DATA_FILE_NAME)

@dataclass
class DataTransformationConfig:
    DATA_TRANSFORMATION_ARTIFACT_DIR = os.path.join (ARTIFACT_DIR, DATA_TRANSFORMATION_ARTIFACT_DIR)
    TRANSFORM_FILE_PATH = os.path.join(DATA_TRANSFORMATION_ARTIFACT_DIR, TRANSFORM_FILE_NAME)

@dataclass
class ModelTrainerConfig:
    MODEL_TRAINER_ARTIFACT_DIR = os.path.join (ARTIFACT_DIR, MODEL_TRAINER_ARTIFACT_DIR)
    TRANSFORM_FILE_PATH = os.path.join(MODEL_TRAINER_ARTIFACT_DIR, TRANSFORM_FILE_NAME)

