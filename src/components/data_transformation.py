import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from src.entity.config_entity import DataTransformationConfig
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

class DataTransformation:
    def __init__(self, 
                 data_ingestion_artifact:DataIngestionArtifact, 
                 data_transformation_config:DataTransformationConfig
                 ):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_config = data_transformation_config

    def data_transformation(self, df):
        try:
            X = df.drop(columns='expenses',axis=1)
            y = df[['expenses']]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            X_df = X_train.reset_index().drop('index', axis=1)
            X_test = X_test.reset_index().drop('index', axis=1)
            Y_df = y_train.reset_index().drop('index', axis=1)
            y_test = y_test.reset_index().drop('index', axis=1)
            

            """Encoding region column"""
            region_column = X_df['region']
            # Initialize the LabelEncoder
            label_encoder = LabelEncoder()
            # Fit and transform the data
            encoded_gender = label_encoder.fit(region_column)
            region_df = pd.DataFrame(encoded_gender.transform(region_column), columns=['region'])
            
            """Encoding sex, smoker, age, bmi columns """
            # Splitting the data into features and target
            One_hot_df = X_df[['sex', 'smoker']]  
            data = X_df[['age', 'bmi']]
            # Define preprocessing steps for each type of column
            categorical_features = ['sex', 'smoker']
            categorical_transformer = Pipeline(steps=[
                ('onehot', OneHotEncoder(drop='first'))
            ])
            num_features = ['age', 'bmi']
            num_transformer = Pipeline(steps=[
                ('scaler', StandardScaler())
            ])
            # Create a ColumnTransformer to apply different preprocessing steps to different columns
            preprocessor = ColumnTransformer(
                transformers=[
                    ('cat', categorical_transformer, categorical_features),
                    ('num', num_transformer, num_features)
                ])
            # Fit and transform the data
            transformed_data = preprocessor.fit_transform(X_df[['sex', 'smoker', 'age', 'bmi']])
            # Get the feature names after transformation
            feature_names = preprocessor.get_feature_names_out()
            # Convert the transformed data to a DataFrame
            transformed_df = pd.DataFrame(transformed_data, columns=feature_names)

            cat_df = pd.concat([transformed_df,region_df, X_df[['children']], Y_df[['expenses']]], axis=1)
            
            return cat_df
        
        except Exception as e:
            CustomException(e, sys)

    def initiate_data_transformation(self):
        try:
            logging.info("Data transformation initiated...")
            df = pd.read_csv(self.data_ingestion_artifact.data_file_path)
            transform_df = self.data_transformation(df)
            os.makedirs(self.data_transformation_config.DATA_TRANSFORMATION_ARTIFACT_DIR, exist_ok=True)
            transform_df.to_csv(self.data_transformation_config.TRANSFORM_FILE_PATH)
            data_transformation_artifact = DataTransformationArtifact(
                self.data_transformation_config.TRANSFORM_FILE_PATH
            )
            logging.info("Data Transformation completed...")
            return data_transformation_artifact
        
        except Exception as e:
            CustomException(e, sys)
