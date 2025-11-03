from datetime import datetime
from typing import List, Dict, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CourseValidationError(Exception):
    """Excepción personalizada para errores de validación de cursos"""
    pass


class Course:
    """
    Representa un curso en la plataforma educativa.
    
    Attributes:
        course_id (str): Identificador único del curso
        title (str): Título del curso
        description (str): Descripción detallada
        instructor_id (str): ID del instructor propietario
        price (float): Precio del curso
        level (str): Nivel de dificultad
        category (str): Categoría del curso
    """
    
    VALID_LEVELS = ['principiante', 'intermedio', 'avanzado']
    VALID_CATEGORIES = [
        'programacion', 'diseno', 'negocios', 'marketing', 
        'desarrollo-personal', 'idiomas', 'ciencias'
    ]
    
    def __init__(
        self, 
        course_id: str,
        title: str,
        description: str,
        instructor_id: str,
        price: float = 0.0,
        level: str = 'principiante',
        category: str = 'programacion'
    ):
        """Inicializa un nuevo curso con sus atributos básicos"""
        self.course_id = course_id
        self.title = title
        self.description = description
        self.instructor_id = instructor_id
        self.price = price
        self.level = level
        self.category = category
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.modules: List[Dict] = []
        self.students_enrolled: List[str] = []
        self.rating: float = 0.0
        self.total_reviews: int = 0
        
    def to_dict(self) -> Dict:
        """Convierte el curso a un diccionario para serialización"""
        return {
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'instructor_id': self.instructor_id,
            'price': self.price,
            'level': self.level,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'modules': self.modules,
            'students_count': len(self.students_enrolled),
            'rating': self.rating,
            'total_reviews': self.total_reviews
        }