from pydantic import BaseModel, HttpUrl, validator, Field
from typing import Optional, List, Dict
from datetime import datetime

class Artwork(BaseModel):
    """������ ��� ������� ������������ ���������"""
    objectID: int = Field(..., description="���������� ������������� �������")
    title: str = Field(..., description="�������� ������������")
    artistDisplayName: Optional[str] = Field(None, description="��� ���������")
    artistNationality: Optional[str] = Field(None, description="�������������� ���������")
    objectDate: Optional[str] = Field(None, description="���� ��������")
    primaryImage: Optional[HttpUrl] = Field(None, description="URL ��������� �����������")
    primaryImageSmall: Optional[HttpUrl] = Field(None, description="URL ������������ �����������")
    department: Optional[str] = Field(None, description="����� �����")
    objectName: Optional[str] = Field(None, description="��� �������")
    culture: Optional[str] = Field(None, description="��������/������")
    period: Optional[str] = Field(None, description="������������ ������")
    dynasty: Optional[str] = Field(None, description="��������")
    reign: Optional[str] = Field(None, description="���������")
    portfolio: Optional[str] = Field(None, description="���������")
    artistRole: Optional[str] = Field(None, description="���� ���������")
    artistBeginDate: Optional[str] = Field(None, description="������ ������������ ���������")
    artistEndDate: Optional[str] = Field(None, description="��������� ������������ ���������")
    objectBeginDate: Optional[int] = Field(None, description="��� ������ ��������")
    objectEndDate: Optional[int] = Field(None, description="��� ��������� ��������")
    medium: Optional[str] = Field(None, description="��������")
    dimensions: Optional[str] = Field(None, description="�������")
    creditLine: Optional[str] = Field(None, description="��������� �����")
    geographyType: Optional[str] = Field(None, description="��� ���������")
    country: Optional[str] = Field(None, description="������")
    region: Optional[str] = Field(None, description="������")
    subregion: Optional[str] = Field(None, description="���������")
    locale: Optional[str] = Field(None, description="�������")
    locus: Optional[str] = Field(None, description="���������������")
    excavation: Optional[str] = Field(None, description="��������")
    river: Optional[str] = Field(None, description="����")
    classification: Optional[str] = Field(None, description="�������������")
    isHighlight: Optional[bool] = Field(None, description="�������� �� �����")
    isPublicDomain: Optional[bool] = Field(None, description="�������� �� ������������ ����������")
    accessionNumber: Optional[str] = Field(None, description="����������� �����")
    accessionYear: Optional[str] = Field(None, description="��� �����������")
    
    @validator('objectBeginDate', 'objectEndDate')
    def validate_year(cls, v):
        if v is not None and (v < 1000 or v > datetime.now().year):
            raise ValueError(f"Invalid year: {v}")
        return v

class ArtworkList(BaseModel):
    """������ ��� ������ ������������"""
    total: int = Field(..., description="����� ���������� ��������")
    objectIDs: List[int] = Field(default_factory=list, description="������ ID ��������")
    hasMore: Optional[bool] = Field(None, description="���� �� ��� �������")
    nextCursor: Optional[str] = Field(None, description="������ ��� ���������")

class Department(BaseModel):
    """������ ��� ������ �����"""
    departmentId: int = Field(..., description="ID ������")
    displayName: str = Field(..., description="�������� ������")
    primaryImage: Optional[HttpUrl] = Field(None, description="URL ����������� ������")
    description: Optional[str] = Field(None, description="�������� ������")