from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    data_file_path: str

@dataclass
class DataTransformationArtifact:
    transform_file_path: str

@dataclass
class ModelTrainerArtifact:
    model1_file_path: str
    model2_file_path: str
    model3_file_path: str
    model4_file_path: str