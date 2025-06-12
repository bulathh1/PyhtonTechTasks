from pydantic import BaseModel, HttpUrl, validator, Field
from typing import Optional, List, Dict
from datetime import datetime

class Artwork(BaseModel):
    """Модель для объекта произведения искусства"""
    objectID: int = Field(..., description="Уникальный идентификатор объекта")
    title: str = Field(..., description="Название произведения")
    artistDisplayName: Optional[str] = Field(None, description="Имя художника")
    artistNationality: Optional[str] = Field(None, description="Национальность художника")
    objectDate: Optional[str] = Field(None, description="Дата создания")
    primaryImage: Optional[HttpUrl] = Field(None, description="URL основного изображения")
    primaryImageSmall: Optional[HttpUrl] = Field(None, description="URL уменьшенного изображения")
    department: Optional[str] = Field(None, description="Отдел музея")
    objectName: Optional[str] = Field(None, description="Тип объекта")
    culture: Optional[str] = Field(None, description="Культура/период")
    period: Optional[str] = Field(None, description="Исторический период")
    dynasty: Optional[str] = Field(None, description="Династия")
    reign: Optional[str] = Field(None, description="Правление")
    portfolio: Optional[str] = Field(None, description="Портфолио")
    artistRole: Optional[str] = Field(None, description="Роль художника")
    artistBeginDate: Optional[str] = Field(None, description="Начало деятельности художника")
    artistEndDate: Optional[str] = Field(None, description="Окончание деятельности художника")
    objectBeginDate: Optional[int] = Field(None, description="Год начала создания")
    objectEndDate: Optional[int] = Field(None, description="Год окончания создания")
    medium: Optional[str] = Field(None, description="Материал")
    dimensions: Optional[str] = Field(None, description="Размеры")
    creditLine: Optional[str] = Field(None, description="Кредитная линия")
    geographyType: Optional[str] = Field(None, description="Тип географии")
    country: Optional[str] = Field(None, description="Страна")
    region: Optional[str] = Field(None, description="Регион")
    subregion: Optional[str] = Field(None, description="Подрегион")
    locale: Optional[str] = Field(None, description="Локация")
    locus: Optional[str] = Field(None, description="Местонахождение")
    excavation: Optional[str] = Field(None, description="Раскопки")
    river: Optional[str] = Field(None, description="Река")
    classification: Optional[str] = Field(None, description="Классификация")
    isHighlight: Optional[bool] = Field(None, description="Является ли хитом")
    isPublicDomain: Optional[bool] = Field(None, description="Является ли общественным достоянием")
    accessionNumber: Optional[str] = Field(None, description="Инвентарный номер")
    accessionYear: Optional[str] = Field(None, description="Год поступления")
    
    @validator('objectBeginDate', 'objectEndDate')
    def validate_year(cls, v):
        if v is not None and (v < 1000 or v > datetime.now().year):
            raise ValueError(f"Invalid year: {v}")
        return v

class ArtworkList(BaseModel):
    """Модель для списка произведений"""
    total: int = Field(..., description="Общее количество объектов")
    objectIDs: List[int] = Field(default_factory=list, description="Список ID объектов")
    hasMore: Optional[bool] = Field(None, description="Есть ли еще объекты")
    nextCursor: Optional[str] = Field(None, description="Курсор для пагинации")

class Department(BaseModel):
    """Модель для отдела музея"""
    departmentId: int = Field(..., description="ID отдела")
    displayName: str = Field(..., description="Название отдела")
    primaryImage: Optional[HttpUrl] = Field(None, description="URL изображения отдела")
    description: Optional[str] = Field(None, description="Описание отдела")